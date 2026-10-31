"""`asbb fetch`: chosen leaves from the published repository, no checkout.

Every case runs on a fake transport that resolves the ref to a commit, serves a
miniature index and leaves at that commit, and records the URLs asked for. One
live case, opt-in through ``ASBB_NETWORK_TESTS=1``, fetches a real leaf from
``main`` and compares it with this checkout's copy.
"""

from __future__ import annotations

import datetime
import hashlib
import json
import os
import pathlib
import re

import pytest

from asb_skill_collections.asbb import fetch
from asb_skill_collections.asbb_cli import main

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
COLLECTION = "astronomy/v3"
TIERS = {"stellar-photometry": "open", "radio-interferometry": "noncommercial"}
LEAVES = {slug: f"---\nname: {slug}\n---\n\n# {slug}\n".encode() for slug in TIERS}
#: The commit the fake commits API resolves every known ref to.
COMMIT = "0123abc" + "9" * 33


class FakeHost:
    """Resolves one ref to COMMIT and serves the collection there; else a 404."""

    def __init__(self, ref="main", missing=(), commit=COMMIT):
        base = f"{fetch.RAW_HOST}/{fetch.REPOSITORY}/{commit}/collections/{COLLECTION}"
        index = [{"slug": slug, "license_tier": tier} for slug, tier in TIERS.items()]
        self.files = {fetch.commit_url(ref): commit.encode()}
        self.files[f"{base}/skills_index.json"] = json.dumps(index).encode()
        self.files.update({
            f"{base}/leaves/{slug}/SKILL.md": body
            for slug, body in LEAVES.items() if slug not in missing
        })
        self.seen = []
        self.accepted = {}

    def __call__(self, url, accept=None):
        self.seen.append(url)
        self.accepted[url] = accept
        if url not in self.files:
            raise fetch.FetchError(f"{url}: HTTP 404")
        return self.files[url]


def _request(*slugs, ref="main", collection=COLLECTION):
    return fetch.FetchRequest(collection, slugs, ref)


def test_fetch_writes_each_leaf_and_its_provenance(tmp_path):
    host = FakeHost()
    dest = tmp_path / "skills"

    provenance = fetch.fetch(_request(*TIERS), dest, host)

    for slug, body in LEAVES.items():
        assert (dest / slug / "SKILL.md").read_bytes() == body
    written = json.loads((dest / fetch.PROVENANCE_FILE).read_text(encoding="utf-8"))
    assert written == provenance
    assert written["repository"] == "https://github.com/HolobiomicsLab/asb-skill-collections"
    assert written["ref"] == "main"
    assert written["collection"] == COLLECTION
    assert written["slugs"] == list(TIERS)
    assert written["license_tiers"] == TIERS
    assert datetime.datetime.fromisoformat(written["date"]).tzinfo is not None
    for slug, body in LEAVES.items():
        record = written["files"][f"{slug}/SKILL.md"]
        assert record["sha256"] == hashlib.sha256(body).hexdigest()
        assert record["url"].endswith(f"/leaves/{slug}/SKILL.md")


def test_fetch_reads_the_index_then_only_the_requested_leaves(tmp_path):
    host = FakeHost(ref="0123abc")

    fetch.fetch(_request("radio-interferometry", ref="0123abc"), tmp_path / "out", host)

    base = f"https://raw.githubusercontent.com/HolobiomicsLab/asb-skill-collections/{COMMIT}/collections/{COLLECTION}"
    assert host.seen == [
        "https://api.github.com/repos/HolobiomicsLab/asb-skill-collections/commits/0123abc",
        f"{base}/skills_index.json",
        f"{base}/leaves/radio-interferometry/SKILL.md",
    ]


@pytest.mark.parametrize(
    ("request_", "message"),
    (
        (_request("stellar-photometry", "no-such", "nor-this"),
         "2 slug(s) not in astronomy/v3 at main: no-such, nor-this"),
        (_request(), "the selection is empty"),
        (_request("../escape"), "not a skill slug: ../escape"),
        (_request("stellar-photometry", collection="astronomy"), "must be <slug>/v<N>"),
        (_request("stellar-photometry", ref="x/../main"), "not a git ref"),
    ),
    ids=("unknown-slugs", "empty", "path-in-slug", "unversioned-collection", "dot-segment-ref"),
)
def test_a_request_that_cannot_be_served_writes_nothing(tmp_path, request_, message):
    host = FakeHost()
    dest = tmp_path / "out"

    with pytest.raises(fetch.FetchError, match=re.escape(message)):
        fetch.fetch(request_, dest, host)

    assert not dest.exists()
    assert not any("/leaves/" in url for url in host.seen)


def test_a_failed_download_writes_nothing(tmp_path):
    dest = tmp_path / "out"

    with pytest.raises(fetch.FetchError, match="HTTP 404"):
        fetch.fetch(_request(*TIERS), dest, FakeHost(missing={"radio-interferometry"}))

    assert not dest.exists()


def test_fetch_never_overwrites_an_earlier_fetch(tmp_path):
    dest = tmp_path / "out"
    fetch.fetch(_request("stellar-photometry"), dest, FakeHost())
    host = FakeHost()

    with pytest.raises(fetch.FetchError, match="already holds PROVENANCE.json"):
        fetch.fetch(_request("radio-interferometry"), dest, host)

    assert host.seen == []
    assert not (dest / "radio-interferometry").exists()


def test_the_cli_prints_each_skill_with_its_licence_tier(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(fetch, "_request", FakeHost())
    dest = tmp_path / "out"

    rc = main(["fetch", "stellar-photometry,radio-interferometry",
               "--collection", COLLECTION, "--dest", str(dest)])

    assert rc == 0
    out = capsys.readouterr().out
    assert re.search(r"stellar-photometry\s+open", out)
    assert re.search(r"radio-interferometry\s+noncommercial", out)
    assert str(dest / fetch.PROVENANCE_FILE) in out
    assert "LICENSE_TIERS.md" in out


def test_the_cli_reports_a_refusal_without_a_traceback(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(fetch, "_request", FakeHost())

    rc = main(["fetch", "no-such", "--collection", COLLECTION, "--dest", str(tmp_path / "o")])

    assert rc == 1
    assert "1 slug(s) not in astronomy/v3 at main: no-such" in capsys.readouterr().err


@pytest.mark.skipif(
    os.environ.get("ASBB_NETWORK_TESTS") != "1",
    reason="live network test; set ASBB_NETWORK_TESTS=1 to run it",
)
def test_a_live_fetch_from_main_matches_the_checkout(tmp_path):
    collection_dir = REPO_ROOT / "collections" / "metabolomics" / "v2"
    rows = json.loads((collection_dir / "skills_index.json").read_text(encoding="utf-8"))
    slug = rows[0]["slug"]

    provenance = fetch.fetch(fetch.FetchRequest("metabolomics/v2", (slug,)), tmp_path)

    fetched = (tmp_path / slug / "SKILL.md").read_bytes()
    assert fetched == (collection_dir / "leaves" / slug / "SKILL.md").read_bytes()
    assert provenance["license_tiers"][slug] == rows[0]["license_tier"]
    assert provenance["ref"] == "main"
    assert re.fullmatch(r"[0-9a-f]{40}", provenance["commit"])
