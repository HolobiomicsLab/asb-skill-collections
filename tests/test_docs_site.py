"""Guards for the static site under docs-site/, which Pages serves as is.

The site went unserved for months, so its defects were never seen: it listed
three staged collections as released with a DOI of "TODO-zenodo". These
checks hold the committed pages to what the site promises once Pages is
enabled.
"""

from __future__ import annotations

import importlib.util
import json
import pathlib
import re
import subprocess
from html.parser import HTMLParser
from urllib.parse import urlsplit

import pytest

from scripts.regen_catalogue import collection_status, released_collection_dirs

REPO = pathlib.Path(__file__).resolve().parent.parent
SITE = REPO / "docs-site"


def _build_search_index():
    spec = importlib.util.spec_from_file_location(
        "build_search_index", SITE / "build_search_index.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# --------------------------------------------------------------------------- #
# Release status (staged collections are labelled, not shown as released)     #
# --------------------------------------------------------------------------- #
def test_indexer_status_follows_the_marketplace():
    released = released_collection_dirs(REPO)
    labels = [p.parent.relative_to(REPO / "collections").as_posix()
              for p in sorted((REPO / "collections").glob("*/v*/collection.yaml"))]
    statuses = _build_search_index().collection_statuses(labels)
    assert statuses == {label: collection_status(f"collections/{label}", released) for label in labels}


def test_committed_search_index_labels_every_collection():
    index = json.loads((SITE / "search_index.json").read_text(encoding="utf-8"))
    released = released_collection_dirs(REPO)
    status = index.get("collection_status")
    assert isinstance(status, dict), "search_index.json has no collection_status: rebuild it"
    assert set(status) == set(index["collections"])
    for label, value in status.items():
        assert value == collection_status(f"collections/{label}", released), label


# --------------------------------------------------------------------------- #
# Links: every href and src in a page resolves                                #
# --------------------------------------------------------------------------- #
REPO_URL = "https://github.com/HolobiomicsLab/asb-skill-collections"
REPO_PATH = re.compile(re.escape(REPO_URL) + r"/(blob|tree)/main/([^?#]+)")
PAGES = sorted(SITE.glob("*.html"))


class _Refs(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs: list[tuple[int, str, str]] = []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in ("href", "src") and value is not None:
                self.refs.append((self.getpos()[0], tag, value.strip()))


def page_refs(page: pathlib.Path) -> list[tuple[int, str, str]]:
    parser = _Refs()
    parser.feed(page.read_text(encoding="utf-8"))
    return parser.refs


def _tracked() -> tuple[set[str], set[str]]:
    out = subprocess.run(["git", "ls-files"], cwd=REPO, capture_output=True, text=True, check=True)
    files = set(out.stdout.splitlines())
    dirs = {str(parent) for f in files for parent in pathlib.PurePosixPath(f).parents}
    return files, dirs


def broken_refs(page: pathlib.Path, files: set[str], dirs: set[str]) -> list[str]:
    """Each repository link must name a tracked path; each relative link a file in docs-site/."""
    broken = []
    for line, _tag, ref in page_refs(page):
        where = f"{page.name}:{line} {ref}"
        match = REPO_PATH.match(ref)
        if match:
            kind, path = match.group(1), match.group(2).rstrip("/")
            if not (path in files or (kind == "tree" and path in dirs)):
                broken.append(where)
            continue
        parts = urlsplit(ref)
        if parts.scheme or parts.netloc or ref.startswith(("#", "mailto:", "javascript:")):
            continue
        target = (page.parent / (parts.path or page.name)).resolve()
        if target.is_dir():
            target = target / "index.html"
        if SITE.resolve() not in target.parents or not target.is_file():
            broken.append(where)
    return broken


def test_link_guard_reports_a_moved_file(tmp_path):
    page = tmp_path / "x.html"
    page.write_text(
        f'<a href="{REPO_URL}/blob/main/OPEN_ACCESS_POLICY.md">a</a>'
        f'<a href="{REPO_URL}/blob/main/governance/OPEN_ACCESS_POLICY.md">b</a>'
        f'<a href="{REPO_URL}/tree/main/governance">c</a>'
    )
    files = {"governance/OPEN_ACCESS_POLICY.md"}
    assert broken_refs(page, files, {"governance"}) == [
        f"x.html:1 {REPO_URL}/blob/main/OPEN_ACCESS_POLICY.md"
    ]


@pytest.mark.parametrize("page", PAGES, ids=[p.name for p in PAGES])
def test_every_link_on_the_page_resolves(page):
    files, dirs = _tracked()
    broken = broken_refs(page, files, dirs)
    assert not broken, "links that do not resolve:\n  " + "\n  ".join(broken)


# --------------------------------------------------------------------------- #
# Third-party loads: a page fetches no font, script or style from another host #
# --------------------------------------------------------------------------- #
# Opening a page must not send the visitor's address to a font or script CDN.
# Navigation links (<a href>) are not loads; the JSON data the pages fetch at
# run time from this repository is not covered here.
LOADING_TAGS = {"script", "link", "img", "iframe", "source", "embed", "object"}
CSS_REMOTE = re.compile(r"@import\s+url\(\s*['\"]?(?:https?:)?//|url\(\s*['\"]?(?:https?:)?//", re.I)
FONT_HOSTS = re.compile(r"fonts\.googleapis\.com|fonts\.gstatic\.com")


def remote_loads(page: pathlib.Path) -> list[str]:
    hits = []
    for line, tag, ref in page_refs(page):
        parts = urlsplit(ref)
        if tag in LOADING_TAGS and (parts.scheme in ("http", "https") or ref.startswith("//")):
            hits.append(f"{page.name}:{line} <{tag}> {ref}")
    return hits


def test_remote_load_check_reports_a_cdn_script(tmp_path):
    page = tmp_path / "x.html"
    page.write_text(
        '<script src="https://cdn.jsdelivr.net/npm/lunr@2.3.9/lunr.min.js"></script>'
        '<script src="vendor/lunr-2.3.9.js"></script><a href="https://lunrjs.com/">lunr</a>'
    )
    assert remote_loads(page) == ["x.html:1 <script> https://cdn.jsdelivr.net/npm/lunr@2.3.9/lunr.min.js"]


@pytest.mark.parametrize("page", PAGES, ids=[p.name for p in PAGES])
def test_page_loads_nothing_from_another_host(page):
    assert not remote_loads(page)


def test_stylesheets_import_nothing_remote():
    for css in sorted(SITE.rglob("*.css")):
        text = css.read_text(encoding="utf-8")
        assert not CSS_REMOTE.search(text), css.name


def test_no_font_cdn_anywhere_in_the_site():
    tracked = subprocess.run(
        ["git", "ls-files", "--", "docs-site"], cwd=REPO, capture_output=True, text=True, check=True
    ).stdout.splitlines()
    hits = [
        path for path in tracked
        if path.endswith((".html", ".css", ".js", ".md"))
        and FONT_HOSTS.search((REPO / path).read_text(encoding="utf-8"))
    ]
    assert not hits, hits
