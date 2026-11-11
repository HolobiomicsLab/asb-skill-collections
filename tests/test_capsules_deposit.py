"""Build-capsules deposit path: refresh, archive, plan, draft creation and registry record.

Nothing here reaches the network: `zenodo_deposit._request` is replaced by the
recorder of tests/test_zenodo_deposit.py whenever a Zenodo call is expected,
and by a function that fails the test everywhere else.
"""

import hashlib
import json
import shutil
import zipfile
from pathlib import Path

import pytest
import yaml

from scripts import capsule_screen, capsules_deposit, check_collections_manifest, pack_capsules, regen_catalogue, release_domain, zenodo_deposit
from tests.test_zenodo_deposit import FakeZenodo

FIXTURE = Path(__file__).parent / "fixtures" / "capsules"
DATE = "2026-11-09"
LATER = "2026-11-11"
ZENODO_DOI = "10.5281/zenodo.1001"
PIPELINE_LINK = "github.com/HolobiomicsLab/AgenticScienceBuilder"
README_ROW = ("| synthetic | `synthetic-v1.0.0` | 1 | 1 | 0 | 4 | "
              f"[{ZENODO_DOI}](https://doi.org/{ZENODO_DOI}) |\n")


def pack(out, view=FIXTURE / "view", collection=FIXTURE / "collection", **overrides):
    values = {
        "view": view, "collection": collection, "out": out, "date": DATE,
        "access_records": None, "limit": None, "with_indicium": False,
        "deny_patterns_file": None, "strict": True, "pipeline_public": False,
    }
    values.update(overrides)
    pack_capsules.run(type("Arguments", (), values)())
    return out


def digests(root):
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*")) if path.is_file()
    }


def collection_copy(tmp_path, name="collection", doi=None, extra_paper=None, exclude=None):
    """A copy of the fixture collection, optionally with a new DOI or a changed corpus."""
    root = tmp_path / name
    shutil.copytree(FIXTURE / "collection", root)
    if doi:
        citation = yaml.safe_load((root / "CITATION.cff").read_text())
        citation["doi"] = doi
        (root / "CITATION.cff").write_text(yaml.safe_dump(citation, sort_keys=False))
    corpus = yaml.safe_load((root / "corpus.yaml").read_text())
    if extra_paper:
        corpus["papers"].append({"name": extra_paper, "doi": "10.1234/example.extra", "status": "included",
                                 "access": {"type": "gold", "license": "CC-BY-4.0"}})
    for paper in corpus["papers"]:
        if paper["name"] == exclude:
            paper["status"] = "excluded"
    (root / "corpus.yaml").write_text(yaml.safe_dump(corpus, sort_keys=False))
    return root


def view_with_extra(tmp_path):
    """The fixture view plus one build whose paper the fixture corpus does not include."""
    view = tmp_path / "view"
    shutil.copytree(FIXTURE / "view", view, symlinks=True)
    shutil.copytree(view / "build__coll_open", view / "build__coll_extra")
    return view


def tooling_root(tmp_path, version_doi=ZENODO_DOI):
    """A tooling root with a registry, release creators, catalogue and README table."""
    root = tmp_path / "tooling"
    (root / "scripts").mkdir(parents=True)
    (root / "scripts" / "release_creators.yaml").write_text("creators:\n- name: Synthetic Author\n")
    registry = {
        "schema": "asb-collections-manifest/1",
        "domains": {"synthetic": {
            "repository": "HolobiomicsLab/asb-skills-metabolomics",
            "concept_doi": "10.5281/zenodo.1000",
            "releases": [{
                "version": 1, "path": "collections/synthetic/v1", "tag": "synthetic-v1.0.0",
                "commit": "a" * 40, "source_commit": None, "tree_digest": "sha256:" + "b" * 64,
                "version_doi": version_doi, "released": "2026-11-09",
                "skills": 1, "tools": 1, "workflows": 0, "papers": 4,
            }],
        }},
    }
    (root / "collections.yaml").write_text("# registry\n" + yaml.safe_dump(registry, sort_keys=False))
    regen_catalogue.write_catalogue(regen_catalogue.build_catalogue(root), root / "catalogue.jsonld")
    (root / "README.md").write_text("| Domain | Release | Skills | Tools | Workflows | Papers | Version DOI |\n"
                                    "|---|---|---:|---:|---:|---:|---|\n" + README_ROW)
    return root


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("a request was sent")
    monkeypatch.setattr(zenodo_deposit, "_request", forbidden)


@pytest.fixture
def packed(tmp_path):
    return pack(tmp_path / "pack")


def plan(tmp_path, pack_dir, collection=FIXTURE / "collection", tooling=None, out=None):
    tooling = tooling or tooling_root(tmp_path)
    out = out or tmp_path / "plan"
    status = capsules_deposit.main(["plan", "--pack", str(pack_dir), "--collection", str(collection),
                                    "--out", str(out), "--date", LATER, "--tooling-root", str(tooling)])
    return status, json.loads((out / capsules_deposit.PLAN_FILE).read_text())


def refusals_of(tmp_path, pack_dir, **kwargs):
    status, written = plan(tmp_path, pack_dir, **kwargs)
    assert status == 1
    return "\n".join(written["refusals"])


# pack ----------------------------------------------------------------------

def test_pack_leaves_out_builds_of_papers_not_in_the_released_corpus(tmp_path):
    out = pack(tmp_path / "pack", view=view_with_extra(tmp_path))
    manifest = json.loads((out / "MANIFEST.json").read_text())
    rows = [json.loads(line) for line in (out / "capsules.jsonl").read_text().splitlines()]
    assert manifest["not_released"] == ["extra"]
    assert manifest["not_released_count"] == 1
    assert "extra" not in {build["build_slug"] for build in manifest["builds"]}
    assert "extra" not in {row["build_slug"] for row in rows}
    assert not (out / "builds" / "extra.zip").exists()
    assert "not an included paper of the released corpus: 1" in (out / "README.md").read_text()


def test_pack_names_the_private_pipeline_without_linking_it(packed):
    metadata = json.loads((packed / "zenodo" / "metadata.json").read_text())
    texts = [json.dumps(metadata), (packed / "hf" / "README.md").read_text(), (packed / "README.md").read_text()]
    assert all(PIPELINE_LINK not in text for text in texts)
    assert "AgenticScienceBuilder pipeline" in metadata["description"]
    assert [item["relation"] for item in metadata["related_identifiers"]] == ["isSupplementTo", "references"]


def test_pack_links_the_pipeline_only_when_declared_public(tmp_path):
    out = pack(tmp_path / "pack", pipeline_public=True)
    metadata = json.loads((out / "zenodo" / "metadata.json").read_text())
    assert {"relation": "isCompiledBy", "identifier": pack_capsules.PIPELINE_URL, "scheme": "url"} in metadata["related_identifiers"]
    assert PIPELINE_LINK in (out / "hf" / "README.md").read_text()


URL_FORMS = {
    "web": "https://github.com/HolobiomicsLab/AgenticScienceBuilder",
    "web_git": "https://github.com/HolobiomicsLab/AgenticScienceBuilder.git",
    "web_path": "https://github.com/HolobiomicsLab/AgenticScienceBuilder/blob/abc123/src/run.py#L4",
    "raw": "https://raw.githubusercontent.com/HolobiomicsLab/AgenticScienceBuilder/abc123/README.md",
    "ssh": "git@github.com:HolobiomicsLab/AgenticScienceBuilder.git",
    "ssh_url": "ssh://git@github.com/HolobiomicsLab/AgenticScienceBuilder",
    "domain": "https://github.com/HolobiomicsLab/asb-skills-metabolomics/tree/main",
    "bare": "HolobiomicsLab/AgenticScienceBuilder",
    "public": "https://github.com/HolobiomicsLab/asb-skill-collections",
}


def view_with_urls(tmp_path):
    """The fixture view with every URL form in one build's manifest and a commit hash beside them."""
    view = tmp_path / "view"
    shutil.copytree(FIXTURE / "view", view, symlinks=True)
    manifest = view / "build__coll_open" / "build_manifest.json"
    value = json.loads(manifest.read_text())
    value["git"] = {"commit": "abc123", **URL_FORMS}
    value["prose"] = f"Built from {URL_FORMS['web']}/tree/main. See {URL_FORMS['ssh']}; done."
    manifest.write_text(json.dumps(value))
    return view


def build_member(pack_dir, slug, member):
    with zipfile.ZipFile(pack_dir / "builds" / f"{slug}.zip") as zipped:
        return zipped.read(member).decode()


def test_screen_rewrites_every_private_url_form_to_owner_and_name(tmp_path):
    out = pack(tmp_path / "pack", view=view_with_urls(tmp_path))
    text = build_member(out, "open", "build_manifest.json")
    value = json.loads(text)
    git = value["git"]
    for form in ("web", "web_git", "web_path", "raw", "ssh", "ssh_url", "bare"):
        assert git[form] == "HolobiomicsLab/AgenticScienceBuilder", form
    assert git["domain"] == "HolobiomicsLab/asb-skills-metabolomics"
    assert git["public"] == URL_FORMS["public"]
    assert git["commit"] == "abc123"
    assert value["prose"] == "Built from HolobiomicsLab/AgenticScienceBuilder. See HolobiomicsLab/AgenticScienceBuilder; done."
    screen = json.loads((out / "SCREEN.json").read_text())
    counts = {build["build_slug"]: build["counts"]["private_urls_rewritten"] for build in screen["builds"]}
    assert counts == {"closed": 0, "open": 9, "open_capped": 0, "preprint": 0}
    assert screen["totals"]["private_urls_rewritten"] == 9
    assert screen["totals"]["failures"] == 0
    assert "github.com" not in text.replace(URL_FORMS["public"], "")


def test_screen_rewrite_is_deterministic(tmp_path):
    view = view_with_urls(tmp_path)
    assert digests(pack(tmp_path / "a", view=view)) == digests(pack(tmp_path / "b", view=view))


def test_screen_keeps_the_pipeline_url_when_declared_public(tmp_path):
    out = pack(tmp_path / "pack", view=view_with_urls(tmp_path), pipeline_public=True)
    git = json.loads(build_member(out, "open", "build_manifest.json"))["git"]
    assert git["web"] == URL_FORMS["web"]
    assert git["domain"] == "HolobiomicsLab/asb-skills-metabolomics"
    assert json.loads((out / "SCREEN.json").read_text())["totals"]["private_urls_rewritten"] == 1
    assert json.loads((out / "MANIFEST.json").read_text())["inclusion_policy"]["pipeline_public"] is True


def test_a_private_url_left_after_the_screen_is_a_failure(tmp_path, monkeypatch):
    monkeypatch.setattr(capsule_screen, "rewrite_private_urls", lambda text, repositories, counts: text)
    out = tmp_path / "pack"
    values = {"view": view_with_urls(tmp_path), "collection": FIXTURE / "collection", "out": out, "date": DATE,
              "access_records": None, "limit": None, "with_indicium": False, "deny_patterns_file": None,
              "strict": True, "pipeline_public": False}
    assert pack_capsules.run(type("Arguments", (), values)()) == 1
    failures = next(build for build in json.loads((out / "SCREEN.json").read_text())["builds"]
                    if build["build_slug"] == "open")["failures"]
    assert "build_manifest.json: residual_private_urls_rewritten" in failures


def test_a_rewrite_runs_on_decoded_values_so_it_cannot_break_json(monkeypatch):
    context = capsule_screen.context_for("10.1234/x", {"type": "gold", "license": "CC-BY-4.0"})
    context.private_repositories = ("HolobiomicsLab/AgenticScienceBuilder",)
    result = capsule_screen.screen_text('{"a": "x"}', "doc.json", context, capsule_screen.QuoteBudget())
    assert result.failures == []
    monkeypatch.setattr(capsule_screen, "rewrite_private_urls", lambda text, repositories, counts: text[:-3])
    mangled = capsule_screen.screen_text('{"a\\"b": "x\\ny\\\\z"}', "doc.json", context, capsule_screen.QuoteBudget())
    assert json.loads(mangled.text) == {"": "x\n"}
    assert mangled.failures == []
    assert capsule_screen._still_parses('{"a": "x', ".json", "doc.json") == ["doc.json: invalid_json_after_rewrite"]


def test_the_screen_and_the_plan_read_one_list_of_private_repositories():
    listed = pack_capsules.private_repositories()
    assert "HolobiomicsLab/AgenticScienceBuilder" in listed
    assert "HolobiomicsLab/asb-skills-metabolomics" in listed
    assert "HolobiomicsLab/asb-skill-collections" not in listed
    assert "HolobiomicsLab/AgenticScienceBuilder" not in pack_capsules.private_repositories(pipeline_public=True)


# refresh -------------------------------------------------------------------

def refresh(pack_dir, collection, out, date=DATE):
    return capsules_deposit.main(["refresh", "--pack", str(pack_dir), "--collection", str(collection),
                                  "--out", str(out), "--date", date])


def test_refresh_with_the_same_inputs_is_byte_identical_to_the_pack(tmp_path, packed):
    assert refresh(packed, FIXTURE / "collection", tmp_path / "refreshed") == 0
    assert digests(tmp_path / "refreshed") == digests(packed)


def test_refresh_against_a_new_collection_doi_matches_a_full_pack(tmp_path, packed):
    patched = collection_copy(tmp_path, doi=ZENODO_DOI)
    full = pack(tmp_path / "full", collection=patched, date=LATER)
    before = digests(packed)
    assert refresh(packed, patched, tmp_path / "refreshed", date=LATER) == 0
    assert digests(tmp_path / "refreshed") == digests(full)
    assert digests(packed) == before


def test_refresh_drops_builds_of_papers_no_longer_released(tmp_path):
    view = view_with_extra(tmp_path)
    wide = collection_copy(tmp_path, name="wide", extra_paper="build__coll_extra")
    old = pack(tmp_path / "old", view=view, collection=wide)
    assert (old / "builds" / "extra.zip").is_file()
    narrow = collection_copy(tmp_path, name="collection")
    full = pack(tmp_path / "full", view=view, collection=narrow)
    assert refresh(old, narrow, tmp_path / "refreshed") == 0
    refreshed = tmp_path / "refreshed"
    assert not (refreshed / "builds" / "extra.zip").exists()
    assert json.loads((refreshed / "MANIFEST.json").read_text())["not_released"] == ["extra"]
    assert digests(refreshed) == digests(full)


def test_refresh_drops_capsule_rows_of_builds_without_a_zip(tmp_path):
    view = tmp_path / "view"
    shutil.copytree(FIXTURE / "view", view, symlinks=True)
    failed = view / "build__coll_open" / "capsules" / "10_1234_example_open__task_001" / "eval.json"
    failed.write_text("bad")
    old = pack(tmp_path / "old", view=view, strict=False)

    assert refresh(old, FIXTURE / "collection", tmp_path / "refreshed") == 0

    refreshed = tmp_path / "refreshed"
    manifest = json.loads((refreshed / "MANIFEST.json").read_text())
    rows = [json.loads(line) for line in (refreshed / "capsules.jsonl").read_text().splitlines()]
    benchmark = json.loads((refreshed / "benchmark-manifest.json").read_text())
    assert manifest["build_count"] == 4 and manifest["builds_packed"] == 3
    assert manifest["capsule_count"] == 4 and manifest["capsules_left_out"] == 2
    assert "open" not in {row["build_slug"] for row in rows}
    assert "open" not in {row["build_slug"] for row in benchmark["capsules"]}


def test_refresh_refuses_a_zip_whose_digest_differs(tmp_path, packed, capsys):
    target = packed / "builds" / "open.zip"
    data = bytearray(target.read_bytes())
    data[-1] ^= 1
    target.write_bytes(bytes(data))
    assert refresh(packed, FIXTURE / "collection", tmp_path / "refreshed") == 1
    assert "builds/open.zip: sha256 differs" in capsys.readouterr().err


def test_refresh_never_writes_into_the_pack(packed, capsys):
    before = digests(packed)
    assert refresh(packed, FIXTURE / "collection", packed / "inside") == 1
    assert "inside the pack" in capsys.readouterr().err
    assert digests(packed) == before


# archive -------------------------------------------------------------------

def archive(pack_dir, out):
    return capsules_deposit.main(["archive", "--pack", str(pack_dir), "--out", str(out)])


def test_archive_is_deterministic_and_stores_build_zips_unchanged(tmp_path, packed):
    assert archive(packed, tmp_path / "a") == 0
    assert archive(packed, tmp_path / "b") == 0
    name = "asb-synthetic-v1-build-capsules.zip"
    assert (tmp_path / "a" / name).read_bytes() == (tmp_path / "b" / name).read_bytes()
    with zipfile.ZipFile(tmp_path / "a" / name) as zipped:
        names = zipped.namelist()
        assert names == sorted(names)
        assert all(info.date_time == zenodo_deposit.ZIP_EPOCH for info in zipped.infolist())
        builds = [info for info in zipped.infolist() if info.filename.startswith("builds/")]
        assert len(builds) == 4
        assert all(info.compress_type == zipfile.ZIP_STORED for info in builds)
        assert all(zipped.read(info) == (packed / info.filename).read_bytes() for info in builds)
        assert {"MANIFEST.json", "README.md", "capsules.jsonl", "SCREEN.json", "benchmark-manifest.json",
                "zenodo/metadata.json", "hf/README.md"} <= set(names)


@pytest.mark.parametrize("damage, message", [
    (lambda pack: shutil.copy(pack / "builds" / "open.zip", pack / "builds" / "stray.zip"), "builds/stray.zip: zip absent from MANIFEST.json"),
    (lambda pack: (pack / "builds" / "open.zip").write_bytes(b"short"), "builds/open.zip: 5 bytes on disk"),
    (lambda pack: (pack / "builds" / "open.zip").unlink(), "builds/open.zip: listed in MANIFEST.json, zip missing"),
])
def test_archive_refuses_a_pack_whose_zips_disagree_with_the_manifest(tmp_path, packed, capsys, damage, message):
    damage(packed)
    assert archive(packed, tmp_path / "a") == 1
    assert message in capsys.readouterr().err
    assert not list((tmp_path / "a").glob("*.zip"))


def test_archive_refuses_a_zip_with_the_wrong_digest_and_leaves_no_partial(tmp_path, packed, capsys):
    target = packed / "builds" / "open.zip"
    data = bytearray(target.read_bytes())
    data[-1] ^= 1
    target.write_bytes(bytes(data))
    assert archive(packed, tmp_path / "a") == 1
    assert "sha256 differs" in capsys.readouterr().err
    assert not list((tmp_path / "a").iterdir())


# plan ----------------------------------------------------------------------

def test_plan_lists_metadata_files_and_digests_without_any_request(tmp_path, packed, capsys):
    status, written = plan(tmp_path, packed)
    assert status == 0, written["refusals"]
    assert written["refusals"] == []
    assert written["metadata"]["publication_date"] == LATER
    names = [item["name"] for item in written["files"]]
    assert names == ["asb-synthetic-v1-build-capsules.zip", *capsules_deposit.BROWSABLE_FILES]
    for item in written["files"]:
        data = (tmp_path / "plan" / item["path"]).read_bytes()
        assert item["md5"] == hashlib.md5(data).hexdigest()
        assert item["sha256"] == hashlib.sha256(data).hexdigest()
        assert item["bytes"] == len(data)
    assert written["counts"] == {"builds_packed": 4, "builds_left_out": 0, "builds_not_released": 0,
                                 "capsules": 6, "capsules_left_out": 0, "benchmark_capsules": 4}
    assert "refusals: none" in capsys.readouterr().out
    assert "/Users/" not in json.dumps(written) and str(tmp_path) not in json.dumps(written)


def edit_json(path, change):
    value = json.loads(path.read_text())
    change(value)
    path.write_text(json.dumps(value, indent=2))


def test_plan_refuses_a_screen_failure_on_a_build_with_a_zip(tmp_path, packed):
    edit_json(packed / "SCREEN.json", lambda screen: screen["builds"][0]["failures"].append("residual"))
    assert "has a zip and 1 screen failures" in refusals_of(tmp_path, packed)


def test_plan_refuses_a_deny_hit_on_a_build_with_a_zip(tmp_path, packed):
    edit_json(packed / "SCREEN.json", lambda screen: screen["builds"][0]["counts"].update(deny_hits=1))
    assert "has a zip and deny hits" in refusals_of(tmp_path, packed)


def test_plan_refuses_a_manifest_and_zip_disagreement(tmp_path, packed):
    (packed / "builds" / "open.zip").unlink()
    assert "archive: builds/open.zip: listed in MANIFEST.json, zip missing" in refusals_of(tmp_path, packed)


def test_plan_refuses_metadata_the_api_would_reject(tmp_path, packed):
    edit_json(packed / "zenodo" / "metadata.json", lambda metadata: metadata.update(upload_type="bogus"))
    assert "upload_type not accepted: bogus" in refusals_of(tmp_path, packed)


def test_plan_refuses_creators_that_differ_from_the_release_list(tmp_path, packed):
    edit_json(packed / "zenodo" / "metadata.json", lambda metadata: metadata.update(creators=[{"name": "Someone Else"}]))
    assert "creators differ from scripts/release_creators.yaml" in refusals_of(tmp_path, packed)


def test_plan_refuses_a_pack_that_supplements_an_older_version_doi(tmp_path, packed):
    patched = collection_copy(tmp_path, doi=ZENODO_DOI)
    refusals = refusals_of(tmp_path, packed, collection=patched)
    assert f"the collection's current version DOI is {ZENODO_DOI}; run refresh" in refusals
    assert "MANIFEST.json: collection_version_doi is 10.1234/example.collection" in refusals


def test_plan_refuses_a_link_to_the_private_pipeline(tmp_path, packed):
    link = {"relation": "isCompiledBy", "identifier": pack_capsules.PIPELINE_URL, "scheme": "url"}
    edit_json(packed / "zenodo" / "metadata.json", lambda metadata: metadata["related_identifiers"].append(link))
    with (packed / "hf" / "README.md").open("a") as stream:
        stream.write(f"Pipeline: {pack_capsules.PIPELINE_URL}\n")
    refusals = refusals_of(tmp_path, packed)
    assert f"zenodo/metadata.json: private repository URL https://{PIPELINE_LINK}" in refusals
    assert f"hf/README.md: private repository URL https://{PIPELINE_LINK}" in refusals


def test_plan_accepts_the_pipeline_link_of_a_pack_declared_public(tmp_path):
    public = pack(tmp_path / "pack", pipeline_public=True)
    status, written = plan(tmp_path, public)
    assert status == 0, written["refusals"]


def test_plan_refuses_a_link_to_a_private_domain_repository(tmp_path, packed):
    with (packed / "hf" / "README.md").open("a") as stream:
        stream.write("Source: git@github.com:HolobiomicsLab/asb-skills-metabolomics.git\n")
    assert "hf/README.md: private repository URL git@github.com:HolobiomicsLab/asb-skills-metabolomics.git" in refusals_of(tmp_path, packed)


def test_plan_refuses_a_private_link_inside_a_build_zip(tmp_path, packed):
    target = packed / "builds" / "open.zip"
    with zipfile.ZipFile(target, "a") as zipped:
        zipped.writestr("notes.md", f"built by https://{PIPELINE_LINK}\n")
    data = target.read_bytes()
    edit_json(packed / "MANIFEST.json", lambda manifest: next(
        entry for entry in manifest["builds"] if entry["build_slug"] == "open").update(
        bytes=len(data), sha256=hashlib.sha256(data).hexdigest()))
    expected = f"notes.md in 1 build zips: private repository URL https://{PIPELINE_LINK} (first: builds/open.zip)"
    assert expected in refusals_of(tmp_path, packed)


def test_plan_refuses_a_local_absolute_path_in_a_descriptive_file(tmp_path, packed):
    with (packed / "README.md").open("a") as stream:
        stream.write("Written from /Volumes/somewhere\n")
    assert "README.md: local absolute path /Volumes/" in refusals_of(tmp_path, packed)


def test_plan_refuses_zips_and_rows_of_builds_not_in_the_released_corpus(tmp_path, packed):
    narrowed = collection_copy(tmp_path, exclude="build__coll_open")
    refusals = refusals_of(tmp_path, packed, collection=narrowed)
    assert "MANIFEST.json: build open has a zip and its paper is not an included paper" in refusals
    assert "capsules.jsonl: rows of build open, whose paper is not an included paper" in refusals


def test_plan_refuses_capsule_rows_of_a_build_the_manifest_does_not_list(tmp_path, packed):
    with (packed / "capsules.jsonl").open("a") as stream:
        stream.write(json.dumps({"build_slug": "ghost", "capsule_id": "x", "eval_state": "partial"}) + "\n")
    assert "capsules.jsonl: rows of build ghost, which MANIFEST.json does not list" in refusals_of(tmp_path, packed)


def test_plan_refuses_tables_that_name_a_build_without_a_zip(tmp_path, packed):
    (packed / "builds" / "open.zip").unlink()
    edit_json(packed / "MANIFEST.json", lambda manifest: next(
        entry for entry in manifest["builds"] if entry["build_slug"] == "open").update(bytes=0, sha256=None))
    refusals = refusals_of(tmp_path, packed)
    assert "capsules.jsonl: rows of build open, which has no zip in the record" in refusals
    assert "benchmark-manifest.json: rows of build open, which has no zip in the record" in refusals
    assert "benchmark-manifest.json: build open has no zip in the record" in refusals


def test_plan_writes_a_public_record_readme_from_the_plan_counts(tmp_path, packed):
    status, written = plan(tmp_path, packed)
    assert status == 0, written["refusals"]
    readme = (tmp_path / "plan" / "upload" / "README.md").read_text()
    archive = written["archive"]["name"]
    assert f"`{archive}`: the archive" in readme
    assert "Local screened archive set" not in readme
    assert "No deposit, upload" not in readme
    assert "`zenodo/metadata.json`" not in readme and "`hf/README.md`" not in readme
    assert "`builds/<build_slug>.zip`" in readme and "`capsules/<capsule_id>/`" in readme
    assert "Builds packed: 4." in readme and "Capsules packed: 6." in readme
    assert "Benchmark capsules: 4." in readme and "Capsules left out with those builds: 0." in readme
    assert "cite this record by its doi" in readme.lower()
    assert capsules_deposit.TAKEDOWN_URL in readme
    assert "/Users/" not in readme and "/Volumes/" not in readme


def test_plan_refuses_a_pack_of_another_collection(tmp_path, packed):
    edit_json(packed / "MANIFEST.json", lambda manifest: manifest.update(collection_version="2"))
    assert "MANIFEST.json describes synthetic v2, the collection is synthetic v1" in refusals_of(tmp_path, packed)


# create --------------------------------------------------------------------

def good_plan(tmp_path, packed):
    patched = collection_copy(tmp_path, doi=ZENODO_DOI)
    refreshed = tmp_path / "refreshed"
    assert refresh(packed, patched, refreshed, date=LATER) == 0
    status, written = plan(tmp_path, refreshed, collection=patched)
    assert status == 0, written["refusals"]
    return tmp_path / "plan" / capsules_deposit.PLAN_FILE, written


def create(plan_path, monkeypatch, fake):
    monkeypatch.setenv("ZENODO_SANDBOX_TOKEN", "tok-sandbox-test")
    monkeypatch.setattr(zenodo_deposit, "_request", fake)
    return capsules_deposit.main(["create", "--plan", str(plan_path), "--sandbox"])


def test_create_uploads_every_planned_file_and_never_publishes(tmp_path, packed, monkeypatch, capsys):
    plan_path, written = good_plan(tmp_path, packed)
    fake = FakeZenodo(zenodo_deposit.SANDBOX_URL)
    assert create(plan_path, monkeypatch, fake) == 0
    steps = fake.steps()
    assert steps[0] == ("POST", "/api/deposit/depositions")
    uploads = [url.rsplit("/", 1)[1] for method, url in steps if url.startswith("/api/files/bkt/")]
    assert uploads == [item["name"] for item in written["files"]]
    assert steps[-1] == ("PUT", "/api/deposit/depositions/777")
    assert fake.calls[-1][3] == {"metadata": written["metadata"]}
    assert not any("publish" in url for _, url in steps)
    output = capsys.readouterr().out
    assert "not published" in output and "tok-sandbox-test" not in output


def test_create_records_the_draft_and_refuses_a_second_run(tmp_path, packed, monkeypatch, capsys):
    plan_path, _ = good_plan(tmp_path, packed)
    assert create(plan_path, monkeypatch, FakeZenodo(zenodo_deposit.SANDBOX_URL)) == 0
    receipt = json.loads((plan_path.parent / "draft-sandbox.json").read_text())
    assert receipt == {"draft_id": 777, "conceptrecid": "444", "url": f"{zenodo_deposit.SANDBOX_URL}/deposit/777",
                       "host": zenodo_deposit.SANDBOX_URL, "complete": True}
    assert not (plan_path.parent / "draft.json").exists()
    second = FakeZenodo(zenodo_deposit.SANDBOX_URL)
    assert create(plan_path, monkeypatch, second) == 1
    assert "a draft was already created from this plan" in capsys.readouterr().err
    assert second.calls == []
    third = FakeZenodo(zenodo_deposit.SANDBOX_URL)
    monkeypatch.setattr(zenodo_deposit, "_request", third)
    assert capsules_deposit.main(["create", "--plan", str(plan_path), "--sandbox", "--again"]) == 0
    assert third.steps()[0] == ("POST", "/api/deposit/depositions")


def test_create_failing_halfway_still_blocks_a_rerun(tmp_path, packed, monkeypatch, capsys):
    plan_path, _ = good_plan(tmp_path, packed)
    fake = FakeZenodo(zenodo_deposit.SANDBOX_URL, stored_override={"checksum": "md5:" + "0" * 32})
    assert create(plan_path, monkeypatch, fake) == 1
    assert json.loads((plan_path.parent / "draft-sandbox.json").read_text())["complete"] is False
    rerun = FakeZenodo(zenodo_deposit.SANDBOX_URL)
    assert create(plan_path, monkeypatch, rerun) == 1
    assert rerun.calls == []


def test_create_refuses_a_stale_plan_before_any_request(tmp_path, packed, monkeypatch, capsys):
    plan_path, _ = good_plan(tmp_path, packed)
    with (tmp_path / "plan" / "upload" / "README.md").open("a") as stream:
        stream.write("changed\n")
    monkeypatch.setenv("ZENODO_SANDBOX_TOKEN", "tok-sandbox-test")
    assert capsules_deposit.main(["create", "--plan", str(plan_path), "--sandbox"]) == 1
    assert "stale plan: upload/README.md changed" in capsys.readouterr().err


def test_create_refuses_a_plan_with_refusals(tmp_path, packed, monkeypatch, capsys):
    plan(tmp_path, packed, collection=collection_copy(tmp_path, doi=ZENODO_DOI))
    monkeypatch.setenv("ZENODO_SANDBOX_TOKEN", "tok-sandbox-test")
    assert capsules_deposit.main(["create", "--plan", str(tmp_path / "plan" / capsules_deposit.PLAN_FILE), "--sandbox"]) == 1
    assert "the plan carries refusals" in capsys.readouterr().err


def test_create_stops_when_zenodo_stores_another_md5(tmp_path, packed, monkeypatch, capsys):
    plan_path, _ = good_plan(tmp_path, packed)
    fake = FakeZenodo(zenodo_deposit.SANDBOX_URL, stored_override={"checksum": "md5:" + "0" * 32})
    assert create(plan_path, monkeypatch, fake) == 1
    assert "Zenodo stored md5:000" in capsys.readouterr().err
    assert ("PUT", "/api/deposit/depositions/777") not in fake.steps()


# record-doi ----------------------------------------------------------------

def record(plan_path, tooling, record_id="2002", *extra):
    return capsules_deposit.main([
        "record-doi", "--plan", str(plan_path), "--doi", f"10.5281/zenodo.{record_id}",
        "--concept-doi", "10.5281/zenodo.2001", "--record-id", "2002",
        "--manifest", str(tooling / "collections.yaml"), *extra,
    ])


def test_record_doi_writes_the_publication_date_given(tmp_path, packed):
    plan_path, _ = good_plan(tmp_path, packed)
    tooling = tmp_path / "tooling"
    assert record(plan_path, tooling, "2002", "--published", "2026-11-14") == 0
    block = yaml.safe_load((tooling / "collections.yaml").read_text())["domains"]["synthetic"]["releases"][0]["capsules"]
    assert str(block["published"]) == "2026-11-14"


def test_record_doi_writes_the_block_the_catalogue_and_the_readme_cell(tmp_path, packed):
    plan_path, written = good_plan(tmp_path, packed)
    tooling = tmp_path / "tooling"
    assert record(plan_path, tooling) == 0
    registry = yaml.safe_load((tooling / "collections.yaml").read_text())
    block = registry["domains"]["synthetic"]["releases"][0]["capsules"]
    assert block["version_doi"] == "10.5281/zenodo.2002" and block["record_id"] == "2002"
    assert block["supplements"] == ZENODO_DOI
    assert block["archive_sha256"] == written["archive"]["sha256"]
    assert block["builds_packed"] == 4 and block["capsules"] == 6 and block["benchmark_capsules"] == 4
    assert set(block) == check_collections_manifest.CAPSULES_KEYS
    assert str(block["published"]) == LATER
    assert (tooling / "collections.yaml").read_text().startswith("# registry\n")
    catalogue = json.loads((tooling / "catalogue.jsonld").read_text())
    assert catalogue["collections"][0]["capsules_doi"] == "10.5281/zenodo.2002"
    readme = (tooling / "README.md").read_text()
    assert "(build capsules: [10.5281/zenodo.2002](https://doi.org/10.5281/zenodo.2002))" in readme
    assert record(plan_path, tooling) == 0
    assert (tooling / "README.md").read_text() == readme
    assert check_collections_manifest.audit(tooling / "collections.yaml", tooling / "catalogue.jsonld", {}) == []


def test_record_doi_refuses_a_record_id_the_doi_does_not_name(tmp_path, packed, capsys):
    plan_path, _ = good_plan(tmp_path, packed)
    before = (tmp_path / "tooling" / "collections.yaml").read_bytes()
    assert record(plan_path, tmp_path / "tooling", record_id="2003") == 1
    assert "--record-id must be the id" in capsys.readouterr().err
    assert (tmp_path / "tooling" / "collections.yaml").read_bytes() == before


def test_without_a_block_the_catalogue_and_readme_show_no_capsules(tmp_path):
    tooling = tooling_root(tmp_path)
    catalogue = json.loads((tooling / "catalogue.jsonld").read_text())
    assert "capsules_doi" not in catalogue["collections"][0]
    assert check_collections_manifest.audit(tooling / "collections.yaml", tooling / "catalogue.jsonld", {}) == []


def block(**overrides):
    value = {
        "version_doi": "10.5281/zenodo.2002", "concept_doi": "10.5281/zenodo.2001", "record_id": "2002",
        "supplements": ZENODO_DOI, "builds_packed": 4, "builds_left_out": 0, "builds_not_released": 0,
        "capsules": 6, "benchmark_capsules": 4, "archive_bytes": 10, "archive_sha256": "c" * 64,
        "published": "2026-11-11",
    }
    value.update(overrides)
    return value


@pytest.mark.parametrize("capsules, message", [
    (block(), None),
    (block(extra=1), "capsules keys must be"),
    (block(record_id="9"), "record_id '9' is not the record"),
    (block(supplements="10.5281/zenodo.9"), "supplements '10.5281/zenodo.9' is not a version DOI"),
    (block(capsules=-1), "invalid capsules -1"),
    (block(archive_sha256="x"), "invalid archive_sha256"),
    ("x", "capsules must be a mapping"),
])
def test_manifest_check_validates_the_capsules_block(capsules, message):
    release = {"version": 1, "version_doi": ZENODO_DOI, "capsules": capsules}
    failures = check_collections_manifest.validate_capsules("synthetic/v1", release)
    assert failures == [] if message is None else any(message in failure for failure in failures)


def test_a_patch_release_keeps_the_capsules_block():
    existing = {"tag": "synthetic-v1.0.0", "commit": "a" * 40, "tree_digest": "sha256:" + "b" * 64,
                "version_doi": ZENODO_DOI, "released": "2026-11-09", "capsules": block()}
    row = {"version": 1, "tag": "synthetic-v1.0.1", "commit": "d" * 40, "tree_digest": "sha256:" + "e" * 64,
           "version_doi": "10.5281/zenodo.1002", "released": "2026-11-12"}
    moved = release_domain.replace_release(existing, row)
    assert moved["capsules"] == block()
    assert moved["superseded"][0]["version_doi"] == ZENODO_DOI
    assert check_collections_manifest.validate_capsules("synthetic/v1", moved) == []
    assert release_domain.replace_release(existing, dict(row, tag="synthetic-v1.0.0"))["capsules"] == block()


def test_the_record_readme_names_failure_classes_in_reader_words():
    def left_out(*failures):
        return {"sha256": None, "screen": {"failures": list(failures)}}
    manifest = {"builds": [
        {"sha256": "abc", "screen": {"failures": []}},
        left_out("missing:capsules/c1/ledger", "missing:capsules/c2/ledger"),
        left_out("workflow.yaml: residual_paths_rewritten", "capsules/c1/ro-crate-metadata.json: carries 2 absolute filesystem path(s)"),
        left_out("evidence/a.md: residual_deny_hits"),
        left_out("ledger/x.json: parse_RewrittenKeyCollision", "something new"),
    ]}
    assert capsules_deposit.screen_failure_classes(manifest) == {
        "a capsule lacks a required member, such as its ledger": 1,
        "a document the screen could not rewrite safely": 1,
        "a machine path the screen could not rewrite": 1,
        "another screen failure": 1,
        "content withheld by the maintainers": 1,
    }
