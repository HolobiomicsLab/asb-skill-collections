"""`asbb fetch` pins its provenance to the commit it read, not only the ref.

A branch such as ``main`` moves, so a PROVENANCE.json that names only the ref
cannot say which tree the files came from. The ref is resolved once through
the GitHub commits API, every file is read at that commit, and both are
recorded.
"""

from __future__ import annotations

import json
import re

import pytest

from asb_skill_collections.asbb import fetch
from asb_skill_collections.asbb_cli import main
from tests.test_asbb_fetch import COLLECTION, COMMIT, TIERS, FakeHost


def _request(*slugs, ref="main"):
    return fetch.FetchRequest(COLLECTION, slugs, ref)


def test_provenance_records_the_ref_and_the_commit(tmp_path):
    dest = tmp_path / "out"

    provenance = fetch.fetch(_request(*TIERS), dest, FakeHost())

    written = json.loads((dest / fetch.PROVENANCE_FILE).read_text(encoding="utf-8"))
    assert written == provenance
    assert written["ref"] == "main"
    assert written["commit"] == COMMIT


def test_every_file_is_read_at_the_resolved_commit(tmp_path):
    host = FakeHost()

    provenance = fetch.fetch(_request(*TIERS), tmp_path / "out", host)

    resolve, *reads = host.seen
    assert resolve == fetch.commit_url("main")
    assert host.accepted[resolve] == "application/vnd.github.sha"
    raw = f"{fetch.RAW_HOST}/{fetch.REPOSITORY}/{COMMIT}/"
    assert reads and all(url.startswith(raw) for url in reads)
    assert all(record["url"].startswith(raw) for record in provenance["files"].values())


def test_the_ref_is_resolved_once(tmp_path):
    host = FakeHost()

    fetch.fetch(_request(*TIERS), tmp_path / "out", host)

    assert host.seen.count(fetch.commit_url("main")) == 1


@pytest.mark.parametrize(
    ("answer", "message"),
    ((None, "cannot resolve ref 'main' to a commit"),
     (b"<html>rate limited</html>", "expected a commit id")),
    ids=("unknown-ref", "not-a-commit-id"),
)
def test_a_ref_that_does_not_resolve_writes_nothing(tmp_path, answer, message):
    host = FakeHost()
    if answer is None:
        del host.files[fetch.commit_url("main")]
    else:
        host.files[fetch.commit_url("main")] = answer
    dest = tmp_path / "out"

    with pytest.raises(fetch.FetchError, match=re.escape(message)):
        fetch.fetch(_request(*TIERS), dest, host)

    assert not dest.exists()
    assert host.seen == [fetch.commit_url("main")]


def test_a_full_commit_ref_needs_no_api_call(tmp_path):
    host = FakeHost(ref=COMMIT)
    del host.files[fetch.commit_url(COMMIT)]

    provenance = fetch.fetch(_request(*TIERS, ref=COMMIT), tmp_path / "out", host)

    assert (provenance["ref"], provenance["commit"]) == (COMMIT, COMMIT)
    assert not any(url.startswith(fetch.API_HOST) for url in host.seen)


@pytest.mark.parametrize("status", (403, 429))
def test_a_rate_limited_resolve_names_the_limit(tmp_path, status):
    def limited(url, accept=None):
        raise fetch.FetchError(f"{url}: HTTP {status}")

    dest = tmp_path / "out"
    with pytest.raises(fetch.FetchError, match="60 requests an hour"):
        fetch.fetch(_request(*TIERS), dest, limited)
    assert not dest.exists()


def test_the_cli_writes_the_commit_into_provenance(tmp_path, monkeypatch):
    monkeypatch.setattr(fetch, "_request", FakeHost(ref="v0.2.0"))
    dest = tmp_path / "out"

    rc = main(["fetch", "stellar-photometry", "--collection", COLLECTION,
               "--dest", str(dest), "--ref", "v0.2.0"])

    assert rc == 0
    written = json.loads((dest / fetch.PROVENANCE_FILE).read_text(encoding="utf-8"))
    assert (written["ref"], written["commit"]) == ("v0.2.0", COMMIT)
