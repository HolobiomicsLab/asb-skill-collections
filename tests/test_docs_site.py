"""Guards for the static site under docs-site/, which Pages serves as is.

The site went unserved for months, so its defects were never seen: it listed
three historical collections as released with a DOI of "TODO-zenodo". These
checks hold the committed pages to what the site promises once Pages is
enabled.
"""

from __future__ import annotations

import importlib.util
import json
import pathlib
import re
import subprocess
import sys
from html.parser import HTMLParser
from urllib.parse import urlsplit

import pytest
import yaml

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
# Search-index status (unreleased trees are staged, not shown as released)    #
# --------------------------------------------------------------------------- #
def test_indexer_status_follows_the_marketplace():
    released = released_collection_dirs(REPO)
    labels = [p.parent.relative_to(REPO / "collections").as_posix()
              for p in sorted((REPO / "collections").glob("*/v*/collection.yaml"))]
    statuses = _build_search_index().collection_statuses(labels)
    assert statuses == {label: collection_status(f"collections/{label}", released) for label in labels}


def test_committed_search_index_labels_every_collection():
    """Each domain file labels its collections, all of them registry releases of that domain."""
    index_dir = SITE / "search_index"
    manifest = json.loads((index_dir / "manifest.json").read_text(encoding="utf-8"))
    registry = yaml.safe_load((REPO / "collections.yaml").read_text(encoding="utf-8"))
    assert set(manifest["domains"]) == set(registry["domains"])
    for slug, entry in manifest["domains"].items():
        releases = {f"{slug}/v{release['version']}" for release in registry["domains"][slug]["releases"]}
        index = json.loads((index_dir / entry["file"]).read_text(encoding="utf-8"))
        assert index["domain"] == slug
        status = index.get("collection_status")
        assert isinstance(status, dict), f"{entry['file']} has no collection_status: rebuild it"
        assert set(status) == set(index["collections"])
        assert sorted(c["label"] for c in entry["collections"]) == sorted(index["collections"])
        for label, value in status.items():
            assert value in {"released", "staged"}, label
            assert label in releases, label
        for key in ("papers", "skills", "tools", "workflows"):
            assert entry["counts"][key] == len(index[key]), (slug, key)


def test_search_page_reads_the_per_domain_index():
    script = (SITE / "search.js").read_text(encoding="utf-8")
    assert '"./search_index/"' in script and '"manifest.json"' in script
    assert "search_index.json" not in script
    assert "search_index.json" not in (SITE / "search.html").read_text(encoding="utf-8")


def test_catalogue_pages_show_release_identity_lifecycle_and_four_counts():
    app = (SITE / "app.js").read_text(encoding="utf-8")
    browse = (SITE / "collections.js").read_text(encoding="utf-8")
    index = (SITE / "index.html").read_text(encoding="utf-8")
    for field in (
        "release_label",
        "skills_count",
        "tools_count",
        "papers_count",
        "workflows_count",
    ):
        assert field in app
        assert field in browse
    assert 'c.status === "legacy"' in browse
    assert '"legacy"' in app
    assert "Legacy entries are historical majors" in index


# --------------------------------------------------------------------------- #
# Public data only: the collection trees are in private domain repositories    #
# --------------------------------------------------------------------------- #
# The pages once fetched collections/<slug>/v<N>/ files, corpus.yaml and
# _workflow_index.json from raw URLs; after the trees moved to private
# repositories every one of them answered 404. The pages read search_index/
# and the registry instead, and never link a private domain repository.
PRIVATE_TREE_REFS = re.compile(
    r"staged-collections/|skills_index\.json|corpus\.yaml|_workflow_index"
    r"|github\.com/HolobiomicsLab/asb-skills-"
)


def test_site_scripts_and_pages_read_no_private_tree():
    hits = [
        f"{path.name}:{number}: {line.strip()}"
        for path in sorted([*SITE.glob("*.js"), *SITE.glob("*.html")])
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1)
        if PRIVATE_TREE_REFS.search(line)
    ]
    assert not hits, "references to private or removed collection trees:\n  " + "\n  ".join(hits)


def test_edam_topic_labels_are_current_and_cover_the_index():
    """build_edam_topic_labels.py --check: the committed file is what it generates,
    and every topic of the search index has a label."""
    result = subprocess.run(
        [sys.executable, str(SITE / "build_edam_topic_labels.py"), "--check"],
        cwd=REPO, capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


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


# --------------------------------------------------------------------------- #
# Brand: every page carries the favicon and the mark from assets/brand/       #
# --------------------------------------------------------------------------- #
# Pages serves docs-site/ alone, so the site keeps copies of the two files it
# uses; they must stay byte-identical to the brand kit.
BRAND_KIT = REPO / "assets" / "brand"
SITE_BRAND = SITE / "brand"
SITE_BRAND_FILES = ("favicon.svg", "favicon.ico", "apple-touch-icon.png", "asb-mark.svg")


@pytest.mark.parametrize("name", SITE_BRAND_FILES)
def test_site_brand_files_match_the_kit(name):
    assert (SITE_BRAND / name).read_bytes() == (BRAND_KIT / name).read_bytes()


@pytest.mark.parametrize("page", PAGES, ids=[p.name for p in PAGES])
def test_page_carries_favicon_and_mark(page):
    refs = {(tag, ref) for _line, tag, ref in page_refs(page)}
    assert ("link", "brand/favicon.svg") in refs, f"{page.name}: no favicon link"
    assert ("link", "brand/favicon.ico") in refs, f"{page.name}: no ICO favicon link"
    assert ("link", "brand/apple-touch-icon.png") in refs, f"{page.name}: no apple-touch-icon link"
    assert ("img", "brand/asb-mark.svg") in refs, f"{page.name}: no brand mark"
