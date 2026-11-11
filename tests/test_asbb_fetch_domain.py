"""Resolve a released collection through the master collections manifest."""

from __future__ import annotations

import json

import pytest

from asb_skill_collections.asbb import fetch
from asb_skill_collections.asbb_cli import main
from tests.test_asbb_fetch import COLLECTION, COMMIT, TIERS, FakeHost


DOMAIN_REPOSITORY = "ExampleOrg/astronomy-skills"
DOMAIN_COMMIT = "4567def" + "0" * 33
MANIFEST = f"""schema: asb-collections-manifest/1
domains:
  astronomy:
    repository: {DOMAIN_REPOSITORY}
    releases:
      - version: 3
        path: collections/astronomy/v3
        tag: astronomy-v3.0.0
        commit: {DOMAIN_COMMIT}
        version_doi: 10.5281/zenodo.1234567
"""


class ManifestHost(FakeHost):
    def __init__(self, manifest=MANIFEST, manifest_ref="main", **kwargs):
        super().__init__(**kwargs)
        self.manifest_url = fetch.raw_url(COMMIT, "collections.yaml")
        if manifest is not None:
            self.files[self.manifest_url] = manifest.encode()
        elif manifest is None:
            del self.files[self.manifest_url]
        base = f"{fetch.RAW_HOST}/{DOMAIN_REPOSITORY}/{DOMAIN_COMMIT}/collections/{COLLECTION}"
        index = [{"slug": slug, "license_tier": tier} for slug, tier in TIERS.items()]
        self.files[f"{base}/skills_index.json"] = json.dumps(index).encode()
        self.files.update({
            f"{base}/leaves/{slug}/SKILL.md": body.encode()
            for slug, body in {
                slug: f"---\nname: {slug}\n---\n" for slug in TIERS
            }.items()
        })
        self.headers = {}

    def __call__(self, url, accept=None, headers=None):
        self.headers[url] = headers
        return super().__call__(url, accept=accept)


def request(*slugs, **kwargs):
    return fetch.FetchRequest(COLLECTION, slugs or tuple(TIERS), **kwargs)


def test_manifest_selects_the_domain_repository_at_its_pinned_commit(tmp_path):
    host = ManifestHost()

    provenance = fetch.fetch(request(), tmp_path / "out", host)

    base = f"{fetch.RAW_HOST}/{DOMAIN_REPOSITORY}/{DOMAIN_COMMIT}/collections/{COLLECTION}"
    assert host.seen == [
        fetch.commit_url("main"),
        host.manifest_url,
        f"{base}/skills_index.json",
        f"{base}/leaves/stellar-photometry/SKILL.md",
        f"{base}/leaves/radio-interferometry/SKILL.md",
    ]
    assert provenance["repository"] == f"https://github.com/{DOMAIN_REPOSITORY}"
    assert provenance["commit"] == DOMAIN_COMMIT
    assert provenance["tag"] == "astronomy-v3.0.0"
    assert provenance["version_doi"] == "10.5281/zenodo.1234567"
    assert provenance["manifest"] == {
        "repository": fetch.REPOSITORY,
        "ref": "main",
        "commit": COMMIT,
    }


def test_an_unlisted_collection_never_uses_the_master_landing_directory(tmp_path):
    manifest = "schema: asb-collections-manifest/1\ndomains: {}\n"
    host = ManifestHost(manifest=manifest)
    dest = tmp_path / "out"

    with pytest.raises(fetch.FetchError, match="not listed") as error:
        fetch.fetch(request(), dest, host)

    assert "--repository OWNER/NAME" in str(error.value)
    assert host.seen == [fetch.commit_url("main"), host.manifest_url]
    assert not dest.exists()


def test_an_unreadable_manifest_is_refused_with_an_override_hint(tmp_path):
    host = ManifestHost(manifest=None)
    dest = tmp_path / "out"

    with pytest.raises(fetch.FetchError, match="cannot read collections manifest") as error:
        fetch.fetch(request(), dest, host)

    assert "--repository OWNER/NAME" in str(error.value)
    assert host.seen == [fetch.commit_url("main"), host.manifest_url]
    assert not dest.exists()


def test_a_repository_override_does_not_read_the_manifest(tmp_path):
    host = FakeHost()

    provenance = fetch.fetch(
        request(repository=fetch.REPOSITORY), tmp_path / "out", host
    )

    assert provenance["repository"] == fetch.REPOSITORY_URL
    assert host.seen == [
        fetch.commit_url("main"),
        f"{fetch.RAW_HOST}/{fetch.REPOSITORY}/{COMMIT}/collections/{COLLECTION}/skills_index.json",
        f"{fetch.RAW_HOST}/{fetch.REPOSITORY}/{COMMIT}/collections/{COLLECTION}/leaves/stellar-photometry/SKILL.md",
        f"{fetch.RAW_HOST}/{fetch.REPOSITORY}/{COMMIT}/collections/{COLLECTION}/leaves/radio-interferometry/SKILL.md",
    ]


def test_a_manifest_ref_is_resolved_and_recorded(tmp_path):
    host = ManifestHost()
    manifest_commit = "7890abc" + "1" * 33
    host.files[fetch.commit_url("release-index")] = manifest_commit.encode()
    host.manifest_url = fetch.raw_url(manifest_commit, "collections.yaml")
    host.files[host.manifest_url] = MANIFEST.encode()

    provenance = fetch.fetch(
        request("stellar-photometry", manifest_ref="release-index"),
        tmp_path / "out",
        host,
    )

    assert host.seen[0] == fetch.commit_url("release-index")
    assert host.seen[1] == host.manifest_url
    assert provenance["manifest"] == {
        "repository": fetch.REPOSITORY,
        "ref": "release-index",
        "commit": manifest_commit,
    }


@pytest.mark.parametrize("token", (None, "secret-token"))
def test_the_token_is_sent_on_every_request_only_when_set(tmp_path, monkeypatch, token):
    if token is None:
        monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    else:
        monkeypatch.setenv("GITHUB_TOKEN", token)
    host = ManifestHost()

    fetch.fetch(request("stellar-photometry"), tmp_path / "out", host)

    for url in host.seen:
        expected = {"Authorization": f"Bearer {token}"} if token else None
        assert host.headers[url] == expected


def test_a_404_on_a_manifest_repository_suggests_a_token(tmp_path):
    host = ManifestHost()
    url = (
        f"{fetch.RAW_HOST}/{DOMAIN_REPOSITORY}/{DOMAIN_COMMIT}/"
        f"collections/{COLLECTION}/skills_index.json"
    )
    del host.files[url]

    with pytest.raises(fetch.FetchError) as error:
        fetch.fetch(request(), tmp_path / "out", host)

    assert DOMAIN_REPOSITORY in str(error.value)
    assert "404" in str(error.value)
    assert "private" in str(error.value)
    assert "GITHUB_TOKEN" in str(error.value)


def test_the_cli_passes_both_overrides_and_the_manifest_ref(tmp_path, monkeypatch):
    seen = {}

    def fake_fetch(request, dest):
        seen["request"] = request
        return {"license_tiers": {"stellar-photometry": "open"}}

    monkeypatch.setattr(fetch, "fetch", fake_fetch)
    rc = main([
        "fetch", "stellar-photometry", "--collection", COLLECTION,
        "--dest", str(tmp_path), "--repository", DOMAIN_REPOSITORY,
        "--ref", "v3.0.0", "--manifest-ref", "release-index",
    ])

    assert rc == 0
    assert seen["request"] == fetch.FetchRequest(
        COLLECTION, ("stellar-photometry",), "v3.0.0", DOMAIN_REPOSITORY, "release-index"
    )
