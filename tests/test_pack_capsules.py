import hashlib
import io
import json
import shutil
import zipfile
from pathlib import Path

import yaml

from scripts import capsule_screen, pack_capsules, zenodo_deposit

FIXTURE = Path(__file__).parent / "fixtures" / "capsules"
DATE = "2026-11-09"


def arguments(out, **overrides):
    values = {
        "view": FIXTURE / "view",
        "collection": FIXTURE / "collection",
        "out": out,
        "date": DATE,
        "access_records": None,
        "limit": None,
        "with_indicium": False,
        "deny_patterns_file": None,
        "strict": False,
        "pipeline_public": False,
    }
    values.update(overrides)
    return type("Arguments", (), values)()


def file_digests(root):
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file() and "capsules-stage-" not in path.parts
    }


def test_packs_screened_archives_receipts_metadata_and_benchmark(tmp_path):
    out = tmp_path / "packed"
    assert pack_capsules.run(arguments(out, strict=True)) == 0
    manifest = json.loads((out / "MANIFEST.json").read_text())
    screen = json.loads((out / "SCREEN.json").read_text())
    rows = [json.loads(line) for line in (out / "capsules.jsonl").read_text().splitlines()]
    benchmark = json.loads((out / "benchmark-manifest.json").read_text())
    assert manifest["schema"] == "asb-capsules-manifest/1"
    assert manifest["build_count"] == 4
    assert manifest["builds_packed"] == 4
    assert manifest["builds_left_out"] == 0
    assert manifest["capsule_count"] == 6
    assert manifest["capsules_left_out"] == 0
    assert screen["schema"] == "asb-capsules-screen/1"
    assert screen["totals"]["spans_truncated"] >= 1
    assert screen["totals"]["spans_dropped"] >= 1
    assert screen["totals"]["emails_redacted"] == 1
    assert screen["totals"]["phones_redacted"] == 2
    assert screen["totals"]["paths_rewritten"] >= 7
    assert screen["totals"]["crates_pruned"] >= 1
    assert screen["totals"]["deny_hits"] == 0
    assert screen["totals"]["failures"] == 0
    retention = {row["build_slug"]: row["quote_retention"] for row in screen["builds"]}
    assert retention == {"closed": "dropped", "open": "full", "open_capped": "capped", "preprint": "dropped"}
    quotes = {row["build_slug"]: row["screen"]["quote_retention"] for row in manifest["builds"]}
    assert quotes == retention
    assert [row["validation_state"] for row in rows].count("strict") == 4
    assert len(benchmark["capsules"]) == 4
    metadata = json.loads((out / "zenodo" / "metadata.json").read_text())
    assert zenodo_deposit.validate_metadata(metadata) == []
    assert metadata["related_identifiers"][0]["identifier"] == "10.1234/example.collection"
    assert metadata["related_identifiers"][1] == {
        "relation": "references", "identifier": pack_capsules.TOOLING_URL, "scheme": "url",
    }
    assert "references" not in metadata
    serialized = json.dumps(metadata) + (out / "hf" / "README.md").read_text()
    assert "HolobiomicsLab/asb-skills-metabolomics" not in serialized
    assert "capsules.jsonl" in (out / "hf" / "README.md").read_text()
    archive_texts = []
    for build in manifest["builds"]:
        archive = out / "hf" / build["zip_member"]
        assert archive.is_file()
        with zipfile.ZipFile(archive) as zipped:
            assert zipped.namelist() == sorted(zipped.namelist())
            assert "indicium.jsonld" not in zipped.namelist()
            assert all(info.date_time == zenodo_deposit.ZIP_EPOCH for info in zipped.infolist())
            text = "\n".join(zipped.read(name).decode() for name in zipped.namelist() if name.endswith((".json", ".md", ".txt", ".yaml")))
        assert "person@example.org" not in text
        archive_texts.append(text)
    all_text = "\n".join(archive_texts)
    assert "peak@123.45" in all_text
    assert "info@lab.example.org" in all_text
    assert "/Users/" not in all_text
    assert "/Volumes/" not in all_text
    assert "C:\\Users\\" not in all_text
    # A drive path that leads to no home directory is the paper's text and is kept.
    assert "C:\\outputs\\closed\\evaluation.txt" in all_text


def test_second_run_is_byte_identical(tmp_path):
    first = tmp_path / "first"
    second = tmp_path / "second"
    pack_capsules.run(arguments(first, strict=True))
    pack_capsules.run(arguments(second, strict=True))
    assert file_digests(first) == file_digests(second)


def test_limit_uses_sorted_build_order(tmp_path):
    out = tmp_path / "limited"
    pack_capsules.run(arguments(out, limit=2, strict=True))
    manifest = json.loads((out / "MANIFEST.json").read_text())
    assert [build["build_slug"] for build in manifest["builds"]] == ["closed", "open"]


def test_strict_deny_failure_writes_receipts_but_no_archives(tmp_path):
    out = tmp_path / "denied"
    deny = tmp_path / "deny.txt"
    deny.write_text("quoted synthetic evidence\n")
    assert pack_capsules.run(arguments(out, deny_patterns_file=deny, strict=True)) == 1
    assert not (out / "hf" / "builds").exists()
    assert not list((out / "zenodo").glob("*.zip"))
    screen_text = (out / "SCREEN.json").read_text()
    assert json.loads(screen_text)["totals"]["deny_hits"] == 4
    assert "synthetic-partner" not in screen_text


def test_with_indicium_is_explicitly_recorded(tmp_path):
    out = tmp_path / "indicium"
    pack_capsules.run(arguments(out, with_indicium=True, strict=True))
    manifest = json.loads((out / "MANIFEST.json").read_text())
    assert manifest["inclusion_policy"]["with_indicium"] is True
    archive = out / "hf" / manifest["builds"][0]["zip_member"]
    with zipfile.ZipFile(archive) as zipped:
        assert "indicium.jsonld" in zipped.namelist()


def test_staging_marks_artifact_membership_from_final_capsule_contents(tmp_path):
    source = tmp_path / "source"
    shutil.copytree(FIXTURE / "view" / "build__coll_open", source)
    capsule = sorted((source / "capsules").iterdir())[0]
    provenance = capsule / "artifact_provenance.json"
    provenance.write_text(json.dumps({
        "task_id": "task_001",
        "artifacts": [
            {"path": "artifact_provenance.json", "kind": "self"},
            {"path": "eval.json#checks", "kind": "evaluation"},
            {"path": "task_card.json", "kind": "full_build"},
        ],
    }))

    staged = tmp_path / "staged"
    pack_capsules.stage_build(source, staged, with_indicium=False)

    projected = json.loads(
        (staged / "capsules" / capsule.name / "artifact_provenance.json").read_text()
    )
    assert projected["artifact_membership_note"] == pack_capsules.ARTIFACT_MEMBERSHIP_NOTE
    assert projected["artifacts"] == [
        {"path": "artifact_provenance.json", "kind": "self", "included_in_capsule": True},
        {"path": "eval.json#checks", "kind": "evaluation", "included_in_capsule": True},
        {"path": "task_card.json", "kind": "full_build", "included_in_capsule": False},
    ]


def test_staging_projects_nested_git_state_only(tmp_path):
    source = tmp_path / "source"
    shutil.copytree(FIXTURE / "view" / "build__coll_open", source)
    manifest_path = source / "build_manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest.update({
        "branch": "scientific-branch",
        "is_dirty": "scientific-value",
        "git": {
            "sha": "outer-commit",
            "branch": "private-branch",
            "is_dirty": True,
            "remote_url": "private-repository",
            "cwd_git": {
                "sha": "nested-commit",
                "branch": "private-worktree",
                "is_dirty": False,
            },
            "sources": [
                {"sha": "list-commit", "branch": "private-list", "is_dirty": True},
                None,
            ],
        },
    })
    manifest_path.write_text(json.dumps(manifest))

    staged = tmp_path / "staged"
    pack_capsules.stage_build(source, staged, with_indicium=False)

    projected = json.loads((staged / "build_manifest.json").read_text())
    assert projected["branch"] == "scientific-branch"
    assert projected["is_dirty"] == "scientific-value"
    assert projected["git"] == {
        "sha": "outer-commit",
        "remote_url": "private-repository",
        "cwd_git": {"sha": "nested-commit"},
        "sources": [{"sha": "list-commit"}, None],
    }


def test_access_override_is_same_doi_and_does_not_echo_secrets(tmp_path):
    out = tmp_path / "override"
    records = tmp_path / "access.json"
    records.write_text(json.dumps([{"doi": "10.1234/example.closed", "access": {"type": "closed", "license": "publisher"}}]))
    pack_capsules.run(arguments(out, access_records=records, strict=True))
    manifest = json.loads((out / "MANIFEST.json").read_text())
    closed = next(build for build in manifest["builds"] if build["build_slug"] == "closed")
    assert closed["access_source"] == "access_override"


def test_non_strict_keeps_passing_archives_and_reports_failures(tmp_path):
    view = tmp_path / "view"
    shutil.copytree(FIXTURE / "view", view, symlinks=True)
    (view / "build__coll_open" / "capsules" / "10_1234_example_open__task_001" / "eval.json").write_text("bad")
    out = tmp_path / "advisory"
    assert pack_capsules.run(arguments(out, view=view, strict=False)) == 0
    assert json.loads((out / "SCREEN.json").read_text())["totals"]["failures"] > 0


def test_failing_build_stays_in_receipt_but_not_record_tables_or_counts(tmp_path, monkeypatch):
    view = tmp_path / "view"
    shutil.copytree(FIXTURE / "view", view, symlinks=True)
    failed = view / "build__coll_open" / "capsules" / "10_1234_example_open__task_001" / "eval.json"
    failed.write_text("bad")
    out = tmp_path / "advisory"
    parquet_rows = []
    monkeypatch.setattr(pack_capsules, "maybe_write_parquet",
                        lambda rows, path: parquet_rows.extend(rows) or True)

    assert pack_capsules.run(arguments(out, view=view, strict=False)) == 0

    manifest = json.loads((out / "MANIFEST.json").read_text())
    rows = [json.loads(line) for line in (out / "capsules.jsonl").read_text().splitlines()]
    benchmark = json.loads((out / "benchmark-manifest.json").read_text())
    assert manifest["build_count"] == manifest["builds_packed"] + manifest["builds_left_out"] == 4
    assert manifest["capsule_count"] + manifest["capsules_left_out"] == 6
    assert manifest["builds_packed"] == 3 and manifest["builds_left_out"] == 1
    assert manifest["capsule_count"] == 4 and manifest["capsules_left_out"] == 2
    assert any(build["build_slug"] == "open" and build["sha256"] is None for build in manifest["builds"])
    assert {row["build_slug"] for row in rows} == {"closed", "open_capped", "preprint"}
    assert {row["build_slug"] for row in parquet_rows} == {"closed", "open_capped", "preprint"}
    assert "open" not in {row["build_slug"] for row in benchmark["capsules"]}
    assert "open" not in {build["build_slug"] for build in benchmark["builds"]}
    assert "Builds considered: 4. Builds packed: 3. Builds left out by the screen: 1." in (out / "README.md").read_text()


# provenance members, shards, readiness and dataset configurations -------------

PNG = b"\x89PNG\r\n\x1a\n" + bytes(range(256))
PAPER_SPAN = "The final version of our synthetic database contains 1996 predicted structures"


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(value, bytes):
        path.write_bytes(value)
    elif isinstance(value, str):
        path.write_text(value)
    else:
        path.write_text(json.dumps(value))


def add_provenance(build, capsule_name, doi):
    """Give one fixture build every new member type, each carrying something to screen."""
    write(build / "cards" / "task_001.json", {"task_id": "task_001", "finding_evidence_span": PAPER_SPAN,
                                               "evidence_snippets": [{"snippet_id": "ev_001", "text": f"[results] claim: '{PAPER_SPAN}'"}],
                                               "reproducibility_tier": "type-checked"})
    write(build / "cards" / "task_001.md",
          "# Card\n\n## Evidence Snippets\n"
          f"- `ev_001` from `agent` (traced): [results] A generated claim: '{PAPER_SPAN}'\n\n"
          "## Evaluation Strategy\n- count rows\n")
    write(build / "astra" / "provenance.myst.md", "Source package: `/Users/someone/outputs/wave/coll_x/synthesized_package`\n"
          f"- task_001 \u00b7 `claim_001` \u2014 A generated claim.\n  - evidence: doi `{doi}` \u2014 \"{PAPER_SPAN}\"\n")
    write(build / "astra" / "astra.yaml", {"findings": [{"quote": {"exact": PAPER_SPAN, "prefix": "then"}}]})
    write(build / "exports" / "nextflow" / "w" / "main.nf", "// emitted by person@example.org from /Users/someone/run\n")
    write(build / "exports" / "snakemake" / "w" / "Snakefile", "rule a:\n    shell: 'cd /Users/someone/run'\n")
    write(build / "deps.lock", "-e file:///Users/someone/git/pipeline\nrequests==2.0\n")
    write(build / "certification_report.json", {"host": "machine.local", "run_dir": "/Users/someone/outputs/w/coll_x",
                                                "status": "ok"})
    write(build / "run_summary.md", "Run in /Users/someone/outputs/w/coll_x\n")
    for name in ("validation_summary.md",):
        write(build / name, "summary\n")
    write(build / "reproducibility_score.json", {"tasks": [{"open_data": {"evidence": PAPER_SPAN, "value": True}}]})
    for name in ("build_fidelity.json", "workflow_score.json", "data_accessions.json", "package_index.json"):
        write(build / name, {"name": name})
    write(build / "entity_spine.json", {"entities": {"e": {"evidence": [{"evidence_span": PAPER_SPAN}]}},
                                        "section_text": {"methods": PAPER_SPAN}})
    write(build / "external_enrichment.json", {"github_repos": [
        {"full_name": "example/other", "default_branch": "dev", "license_spdx": "GPL-3.0", "pushed_at": "2025-01-01T00:00:00Z"},
        {"full_name": "example/tool", "default_branch": "main", "license_spdx": "MIT", "pushed_at": "2026-01-01T00:00:00Z"},
    ]})
    write(build / "repo_relationship.json", {"repo": "example/tool", "doi": doi, "signals": [{"snippet": PAPER_SPAN}]})
    write(build / "anchor_corpus" / "manifest.json", {"hashes": {"article": "sha256:" + "a" * 64, "repo": "sha256:" + "b" * 64},
                                                      "source_kind": "github", "partitions": ["article", "repo"]})
    write(build / "anchor_corpus" / "anchor_results.json", {"artifacts": [{"artifact_id": "f1", "status": "exact"}]})
    for name in ("article.txt", "repo.txt", "enrichment_docs.txt"):
        write(build / "anchor_corpus" / name, f"{PAPER_SPAN}\n")
    write(build / "certification" / "20260101T000000Z" / "report.json", {"hostname": "machine.local", "ok": True})
    capsule = build / "capsules" / capsule_name
    write(capsule / "scripts" / "run.sh", "#!/bin/sh\ncd /Users/someone/outputs/w\n")
    write(capsule / "tables" / "index.json", [{"name": "table1.csv"}])
    write(capsule / "tables" / "table1.csv", "a,b\n1,2\n")
    write(capsule / "figures" / "index.json", [{"name": "fig1.png"}])
    write(capsule / "figures" / "fig1.png", PNG)
    write(capsule / "outputs" / "generated_outputs_placeholder.md", "placeholder\n")
    write(capsule / "nanopubs" / "claim_001.jsonld", {"@graph": [
        {"@graph": [{"rdfs:label": "A generated claim.", "dct:description": PAPER_SPAN}]},
        {"@graph": [{"prov:wasGeneratedBy": {"dct:description": PAPER_SPAN}}]}]})
    write(capsule / "task_card.json", {"reproducibility_tier": "type-checked", "finding_evidence_span": PAPER_SPAN})
    write(capsule / "task_card.md", f"## Evidence Snippets\n- `ev_001` from `agent` (traced): [abstract] claim: '{PAPER_SPAN}'\n")
    for name in ("metadata.json", "rubric.json", "resources.json", "resolved_inputs.json"):
        write(capsule / name, {"name": name})
    write(capsule / "artifact_provenance.json", {"artifacts": [{"path": "figures/fig1.png"}, {"path": "scripts/run.sh"}]})


def provenance_view(tmp_path):
    view = tmp_path / "view"
    shutil.copytree(FIXTURE / "view", view, symlinks=True)
    add_provenance(view / "build__coll_open", "10_1234_example_open__task_001", "10.1234/example.open")
    add_provenance(view / "build__coll_closed", "10_1234_example_closed__task_001", "10.1234/example.closed")
    return view


def members(out, slug):
    with zipfile.ZipFile(out / "hf" / "builds" / f"{slug}.zip") as zipped:
        return {name: zipped.read(name) for name in zipped.namelist()}


NEW_BUILD_MEMBERS = {
    "cards/task_001.json", "cards/task_001.md", "astra/provenance.myst.md", "astra/astra.yaml",
    "exports/nextflow/w/main.nf", "exports/snakemake/w/Snakefile", "deps.lock", "certification_report.json",
    "run_summary.md", "validation_summary.md", "build_fidelity.json", "workflow_score.json",
    "reproducibility_score.json", "data_accessions.json", "package_index.json", "entity_spine.json",
    "external_enrichment.json", "repo_relationship.json", "anchor_corpus/manifest.json",
    "anchor_corpus/anchor_results.json", "certification/20260101T000000Z/report.json", "anchor_recipe.json",
    "indicium.jsonld",
}
NEW_CAPSULE_MEMBERS = {
    "scripts/run.sh", "tables/index.json", "figures/index.json", "outputs/generated_outputs_placeholder.md",
    "nanopubs/claim_001.jsonld", "task_card.json", "task_card.md", "metadata.json", "rubric.json",
    "resources.json", "resolved_inputs.json",
}


def test_provenance_members_are_packed_and_screened(tmp_path):
    out = tmp_path / "out"
    assert pack_capsules.run(arguments(out, view=provenance_view(tmp_path), with_indicium=True, strict=True)) == 0
    for slug, capsule in (("open", "10_1234_example_open__task_001"), ("closed", "10_1234_example_closed__task_001")):
        files = members(out, slug)
        assert NEW_BUILD_MEMBERS <= set(files), NEW_BUILD_MEMBERS - set(files)
        assert {f"capsules/{capsule}/{name}" for name in NEW_CAPSULE_MEMBERS} <= set(files)
        text = "\n".join(data.decode() for name, data in files.items() if not name.endswith(".png"))
        assert "/Users/" not in text and "person@example.org" not in text and "machine.local" not in text
        assert '"host"' not in files["certification_report.json"].decode()
    screen = json.loads((out / "SCREEN.json").read_text())
    counts = {build["build_slug"]: build["counts"] for build in screen["builds"]}
    assert counts["open"]["paths_rewritten"] >= 7 and counts["open"]["emails_redacted"] >= 1
    manifest = json.loads((out / "MANIFEST.json").read_text())
    open_entry = next(build for build in manifest["builds"] if build["build_slug"] == "open")
    assert {"deps.lock", "astra/astra.yaml", "anchor_corpus/article.txt"} <= set(open_entry["input_sha256"])
    closed_entry = next(build for build in manifest["builds"] if build["build_slug"] == "closed")
    assert "anchor_corpus/article.txt" not in closed_entry["input_sha256"]


def test_permissive_paper_ships_anchor_text_and_figures_others_ship_hashes(tmp_path):
    out = tmp_path / "out"
    assert pack_capsules.run(arguments(out, view=provenance_view(tmp_path), strict=True)) == 0
    opened, closed = members(out, "open"), members(out, "closed")
    capsule_open, capsule_closed = "capsules/10_1234_example_open__task_001", "capsules/10_1234_example_closed__task_001"
    assert {"anchor_corpus/article.txt", "anchor_corpus/repo.txt", "anchor_corpus/enrichment_docs.txt"} <= set(opened)
    assert opened[f"{capsule_open}/figures/fig1.png"] == PNG
    assert f"{capsule_open}/tables/table1.csv" in opened
    assert not any(name.startswith("anchor_corpus/") and name.endswith(".txt") for name in closed)
    assert f"{capsule_closed}/figures/fig1.png" not in closed and f"{capsule_closed}/tables/table1.csv" not in closed
    withheld = json.loads(closed[f"{capsule_closed}/figures/withheld_files.json"])
    assert withheld["files"] == [{"name": "fig1.png", "sha256": hashlib.sha256(PNG).hexdigest(), "bytes": len(PNG)}]
    assert json.loads(closed[f"{capsule_closed}/tables/withheld_files.json"])["files"][0]["name"] == "table1.csv"
    provenance = json.loads(closed[f"{capsule_closed}/artifact_provenance.json"])
    assert [entry["included_in_capsule"] for entry in provenance["artifacts"]] == [False, True]
    assert [entry["included_in_capsule"] for entry in json.loads(opened[f"{capsule_open}/artifact_provenance.json"])["artifacts"]] == [True, True]
    crate = json.loads(closed[f"{capsule_closed}/ro-crate-metadata.json"])
    described = {entity["@id"] for entity in crate["@graph"]}
    assert "figures/withheld_files.json" in described and "figures/fig1.png" not in described
    recipes = {slug: json.loads(files["anchor_recipe.json"]) for slug, files in (("open", opened), ("closed", closed))}
    for slug, shipped in (("open", True), ("closed", False)):
        recipe = recipes[slug]
        assert recipe["text_shipped"] is shipped and recipe["commit_pinned"] is False
        assert recipe["partition_sha256"] == {"article": "sha256:" + "a" * 64, "repo": "sha256:" + "b" * 64}
        assert recipe["repository"] == {"full_name": "example/tool", "default_branch": "main",
                                        "pushed_at": "2026-01-01T00:00:00Z", "license_spdx": "MIT"}
        assert recipe["statement"] == pack_capsules.ANCHOR_RECIPE_STATEMENT
        assert "github.com" not in json.dumps(recipe)
    assert recipes["closed"]["doi"] == "10.1234/example.closed"
    screen = {build["build_slug"]: build for build in json.loads((out / "SCREEN.json").read_text())["builds"]}
    assert screen["closed"]["counts"]["paper_files_withheld"] == 2 and screen["open"]["counts"]["paper_files_withheld"] == 0
    assert screen["closed"]["anchor_text_shipped"] is False and screen["open"]["anchor_text_shipped"] is True
    # The closed paper's spans are dropped in every new member type.
    assert json.loads(closed["cards/task_001.json"])["finding_evidence_span"] == ""
    assert PAPER_SPAN not in "\n".join(data.decode() for name, data in closed.items() if not name.endswith(".png"))
    assert "[redacted-quote]" in closed["cards/task_001.md"].decode()
    assert "[redacted-quote]" in closed["astra/provenance.myst.md"].decode()
    assert json.loads(closed["cards/task_001.json"])["evidence_snippets"][0]["text"] == ""
    assert PAPER_SPAN in opened["cards/task_001.md"].decode()


def bypass(text, relative_path, context, budget, capsule_dir=None):
    return capsule_screen.ScreenResult(text, capsule_screen.empty_counts(), capsule_screen.empty_quotes(), [])


def test_a_leak_in_a_new_member_type_leaves_the_build_out(tmp_path, monkeypatch):
    view = provenance_view(tmp_path)
    (view / "build__coll_open" / "exports" / "nextflow" / "w" / "main.nf").write_text('path "/Users/"x\n')
    out = tmp_path / "out"
    assert pack_capsules.run(arguments(out, view=view, strict=True)) == 1
    failures = {build["build_slug"]: build["failures"] for build in json.loads((out / "SCREEN.json").read_text())["builds"]}
    assert "exports/nextflow/w/main.nf: residual_paths_rewritten" in failures["open"]
    monkeypatch.setattr(capsule_screen, "screen_text", bypass)
    out = tmp_path / "bypassed"
    assert pack_capsules.run(arguments(out, view=provenance_view(tmp_path / "again"), strict=False)) == 0
    failures = {build["build_slug"]: build["failures"] for build in json.loads((out / "SCREEN.json").read_text())["builds"]}
    for member in ("cards/task_001.md", "cards/task_001.json", "entity_spine.json", "astra/astra.yaml",
                   "astra/provenance.myst.md", "reproducibility_score.json",
                   "capsules/10_1234_example_closed__task_001/nanopubs/claim_001.jsonld",
                   "capsules/10_1234_example_closed__task_001/task_card.md"):
        assert f"{member}: residual_source_text" in failures["closed"], member


def test_new_member_text_is_found_by_content_not_suffix():
    assert capsule_screen.is_text_member("exports/snakemake/w/Snakefile", b"rule a:\n")
    assert capsule_screen.is_text_member("deps.lock", b"requests==2\n")
    assert not capsule_screen.is_text_member("figures/fig1.png", b"text")
    assert not capsule_screen.is_text_member("blob", b"\x00\x01")
    assert not capsule_screen.is_text_member("blob", b"\xff\xfe")


def test_shards_group_sorted_builds_and_rows_locate_their_capsule(tmp_path):
    out = tmp_path / "out"
    assert pack_capsules.run(arguments(out, shard_size=3, strict=True)) == 0
    manifest = json.loads((out / "MANIFEST.json").read_text())
    layout = manifest["layout"]
    assert [shard["name"] for shard in layout["shards"]] == ["asb-synthetic-v1-builds-001.zip", "asb-synthetic-v1-builds-002.zip"]
    assert [shard["builds"] for shard in layout["shards"]] == [["closed", "open", "open_capped"], ["preprint"]]
    assert layout["zenodo_files"] == 2 + len(pack_capsules.ZENODO_RECEIPTS)
    assert sorted(path.name for path in (out / "zenodo").glob("*.zip")) == [shard["name"] for shard in layout["shards"]]
    for shard in layout["shards"]:
        assert hashlib.sha256((out / "zenodo" / shard["name"]).read_bytes()).hexdigest() == shard["sha256"]
    rows = [json.loads(line) for line in (out / "capsules.jsonl").read_text().splitlines()]
    for row in rows:
        with zipfile.ZipFile(out / "zenodo" / row["shard"]) as shard:
            inner = shard.read(row["member"])
        assert inner == (out / "hf" / row["member"]).read_bytes()
        with zipfile.ZipFile(io.BytesIO(inner)) as build:
            assert f"capsules/{row['capsule_id']}/eval.json" in build.namelist()
    entries = {build["build_slug"]: build for build in manifest["builds"]}
    assert entries["preprint"]["shard"] == "asb-synthetic-v1-builds-002.zip"
    assert entries["preprint"]["member"] == "builds/preprint.zip"


def test_a_record_over_the_file_budget_is_refused(tmp_path, monkeypatch):
    monkeypatch.setattr(pack_capsules, "ZENODO_FILE_BUDGET", 8)
    try:
        pack_capsules.run(arguments(tmp_path / "out", shard_size=1, strict=True))
    except ValueError as error:
        assert "9 files (4 shards and 5 receipts), over the budget of 8; raise --shard-size" in str(error)
    else:
        raise AssertionError("an over-budget layout was accepted")
    assert not list((tmp_path / "out" / "zenodo").glob("*.zip")) if (tmp_path / "out" / "zenodo").exists() else True


def readiness_row(validation, evaluation, inputs=0, hashed=0, hinted=0, tier=None):
    return {"validation_state": validation, "eval_state": evaluation, "eval_input_assets": inputs,
            "eval_input_assets_with_hash": hashed, "eval_input_assets_with_download_hint": hinted,
            "reproducibility_tier": tier}


def test_readiness_rule():
    readiness = pack_capsules.capsule_readiness
    assert readiness(readiness_row("present", "complete", 1, 1, 1, "certified")) == "documented"
    assert readiness(readiness_row("present", "partial")) == "documented"
    assert readiness(readiness_row("clean", "partial")) == "validated"
    assert readiness(readiness_row("strict", "partial", 1, 1, 1, "certified")) == "validated"
    assert readiness(readiness_row("strict", "complete")) == "evaluable"
    assert readiness(readiness_row("clean", "complete", 2, 2, 2, "type-checked")) == "evaluable"
    assert readiness(readiness_row("clean", "complete", 2, 2, 1, "certified")) == "evaluable"
    assert readiness(readiness_row("clean", "complete", 0, 0, 0, "certified")) == "evaluable"
    assert readiness(readiness_row("clean", "complete", 2, 2, 2, "certified")) == "executable"
    assert readiness(readiness_row("strict", "invalid")) is None


def test_a_certified_capsule_with_ready_inputs_is_executable_and_configs_filter_by_readiness(tmp_path):
    view = tmp_path / "view"
    shutil.copytree(FIXTURE / "view", view, symlinks=True)
    capsule = view / "build__coll_open" / "capsules" / "10_1234_example_open__task_001"
    evaluation = json.loads((capsule / "eval.json").read_text())
    evaluation["inputs"] = [{"name": "a", "sha256": "c" * 64, "download_hint": "registry:a"}]
    write(capsule / "eval.json", evaluation)
    write(capsule / "task_card.json", {"reproducibility_tier": "certified"})
    out = tmp_path / "out"
    assert pack_capsules.run(arguments(out, view=view, strict=True)) == 0
    rows = [json.loads(line) for line in (out / "capsules.jsonl").read_text().splitlines()]
    assert all("grade" not in row for row in rows)
    levels = {row["capsule_id"]: row["readiness"] for row in rows}
    assert levels["10_1234_example_open__task_001"] == "executable"
    tiers = {row["capsule_id"]: row["reproducibility_tier"] for row in rows}
    assert tiers["10_1234_example_open__task_001"] == "certified" and tiers["10_1234_example_open__task_002"] is None
    manifest = json.loads((out / "MANIFEST.json").read_text())
    assert manifest["readiness_counts"] == {"documented": 2, "validated": 0, "evaluable": 3, "executable": 1}
    assert "grade_counts" not in manifest
    hf = out / "hf"
    def table(name):
        return [json.loads(line) for line in (hf / name).read_text().splitlines()]
    assert table("capsules.jsonl") == rows
    evaluable = table("evaluable_plus.jsonl")
    assert {row["readiness"] for row in evaluable} == {"evaluable", "executable"} and len(evaluable) == 4
    assert len(table("validated_plus.jsonl")) == 4
    assert not (hf / "silver_plus.jsonl").exists() and not (hf / "gold_plus.jsonl").exists()
    benchmark = json.loads((out / "benchmark-manifest.json").read_text())
    assert table("benchmark.jsonl") == benchmark["capsules"]
    card = (hf / "README.md").read_text()
    for name, stem, _, _ in pack_capsules.HF_CONFIGS:
        assert f"config_name: {name}\n    data_files: \"{stem}\"" in card
    assert "Zenodo is the archival record" in card and pack_capsules.READINESS_STATEMENT in card
    assert "documented 2, validated 0, evaluable 3, executable 1" in card
    readme = (out / "README.md").read_text()
    assert pack_capsules.READINESS_STATEMENT in readme and "Expert review is a separate axis" in readme
    statement = pack_capsules.READINESS_STATEMENT
    assert "No capsule has been executed under a workflow engine" in statement
    assert "Readiness is not the maturity scale" in statement and "at most Iron" in statement
    for word in ("bronze", "silver", "gold", "platinum"):
        assert word not in json.dumps(manifest["readiness_counts"]).lower()


def test_indicium_ships_by_default_with_an_escape():
    base = ["--view", str(FIXTURE / "view"), "--collection", str(FIXTURE / "collection"), "--out", "x", "--date", DATE]
    assert pack_capsules.parse_args(base).with_indicium is True
    assert pack_capsules.parse_args(base + ["--no-indicium"]).with_indicium is False
    assert pack_capsules.parse_args(base).shard_size == pack_capsules.SHARD_SIZE == 40


# overlap trim -----------------------------------------------------------------

ARTICLE = (
    "Introduction. We measured the retention of seventeen synthetic compounds across four columns, "
    "and the shift between runs stayed below two seconds for every compound in every batch we recorded. "
    "Methods. Samples were injected in triplicate with a gradient of thirty minutes, the flow rate was "
    "held constant throughout, and each injection was followed by a blank to estimate carry-over."
)
COPIED = ARTICLE[14:214]          # 200 characters copied from the article
SHORT = ARTICLE[14:173]           # 159 characters: under the bar


def trim_context(article=ARTICLE):
    context = capsule_screen.context_for("10.1234/closed", {"type": "closed", "license": "publisher"})
    context.article = capsule_screen.ArticleIndex(article)
    return context


def screen(text, name, context=None):
    return capsule_screen.screen_text(text, name, context or trim_context(), capsule_screen.QuoteBudget())


def test_runs_match_after_normalising_case_and_whitespace():
    index = capsule_screen.ArticleIndex(ARTICLE)
    variant = "  " + COPIED.upper().replace(" ", " \n  ") + " tail"
    [(start, end)] = index.runs(variant)
    assert variant[start:end].split() == COPIED.upper().split()
    assert index.runs(SHORT) == [] and index.runs("unrelated " * 40) == []
    # Two copies joined by whitespace stay two runs; a 159-character copy beside a run is kept.
    assert len(index.runs(f"{SHORT}\n\n{COPIED}")) == 1 and len(index.runs(f"{COPIED}\n\n{SHORT}")) == 1
    [(start, end)] = index.runs(f"{SHORT}\n\n{COPIED}")
    assert f"{SHORT}\n\n{COPIED}"[start:end] == COPIED


def test_each_format_is_trimmed_at_160_and_still_parses():
    for name, text, load in (
        ("ledger/claims.json", json.dumps({"claim": f"Claim: {COPIED}", "short": SHORT}), json.loads),
        ("ledger/claims.jsonl", json.dumps({"text": COPIED}) + "\n" + json.dumps({"text": SHORT}) + "\n",
         lambda text: [json.loads(line) for line in text.splitlines()]),
        ("workflow.yaml", yaml.safe_dump({"narrative": {"abstract": COPIED}, "short": SHORT}), yaml.safe_load),
        ("indicium.jsonld", json.dumps({"@graph": [{"schema:name": {"@value": COPIED}, "rdfs:label": SHORT}]}), json.loads),
        ("run_summary.md", f"# Run\n\n{COPIED}\n\n{SHORT}\n", None),
        ("exports/nextflow/w/main.nf", f"// {COPIED}\n// {SHORT}\n", None),
    ):
        result = screen(text, name)
        assert result.failures == [], (name, result.failures)
        assert result.counts["overlap_runs_trimmed"] == 1, name
        assert result.counts["overlap_characters_trimmed"] >= 200, name
        assert "[trimmed-overlap" in result.text, name
        flat = " ".join(json.dumps(load(result.text)) .split()) if load else " ".join(result.text.split())
        assert COPIED not in flat and SHORT in flat, name
        if name.endswith(".md"):
            assert '"redacted_reason": "article_overlap"' in result.text
        if name.endswith(".nf"):
            assert "[trimmed-overlap length=" in result.text
        assert screen(text, name).text == result.text, name  # deterministic


def test_json_anchor_names_the_cut_without_its_text():
    result = screen(json.dumps({"claim": f"Claim: {COPIED}"}), "ledger/claims.json")
    value = json.loads(result.text)
    assert value["claim"] == f"Claim: {capsule_screen.OVERLAP_MARKER}"
    [anchor] = value["_screen_redactions"]
    assert anchor["redacted_reason"] == "article_overlap" and anchor["location"] == "ledger/claims.json#/claim"
    assert anchor["sha256"] == hashlib.sha256(COPIED.encode()).hexdigest() and anchor["length"] == len(COPIED)


def test_quotation_fields_follow_the_quote_rule_not_the_trim():
    capped = capsule_screen.context_for("10.1234/capped", {"type": "green", "license": "other-oa"})
    capped.article = capsule_screen.ArticleIndex(ARTICLE)
    result = screen(json.dumps({"quote": COPIED, "text": COPIED}), "ledger/claims.json", capped)
    value = json.loads(result.text)
    assert value["quote"] == COPIED and value["text"] == capsule_screen.OVERLAP_MARKER
    snippets = f"## Evidence Snippets\n- `ev_001` from `agent` (traced): [results] claim: '{COPIED}'\n\n{COPIED}\n"
    text = screen(snippets, "cards/task_001.md", capped).text
    assert f"'{COPIED}'" in text and text.count(capsule_screen.OVERLAP_MARKER) == 1


def overlap_view(tmp_path):
    view = provenance_view(tmp_path)
    for slug in ("build__coll_open", "build__coll_closed"):
        write(view / slug / "synthesized_package" / "article_fulltext.md", ARTICLE)
        write(view / slug / "run_summary.md", f"Summary: {COPIED}\n")
        write(view / slug / "workflow.yaml", {"narrative": {"pseudo_abstract": COPIED}})
    return view


def test_the_pack_trims_copied_runs_only_for_papers_not_kept_in_full(tmp_path):
    first, second = tmp_path / "first", tmp_path / "second"
    assert pack_capsules.run(arguments(first, view=overlap_view(tmp_path / "a"), strict=True)) == 0
    assert pack_capsules.run(arguments(second, view=overlap_view(tmp_path / "b"), strict=True)) == 0
    assert file_digests(first) == file_digests(second)
    closed, opened = members(first, "closed"), members(first, "open")
    assert COPIED not in closed["run_summary.md"].decode() and COPIED not in closed["workflow.yaml"].decode()
    yaml.safe_load(closed["workflow.yaml"])
    assert COPIED in opened["run_summary.md"].decode() and COPIED in opened["workflow.yaml"].decode()
    assert not any(name.startswith("synthesized_package/") for name in closed)
    counts = {build["build_slug"]: build["counts"] for build in json.loads((first / "SCREEN.json").read_text())["builds"]}
    assert counts["closed"]["overlap_runs_trimmed"] == 2 and counts["open"]["overlap_runs_trimmed"] == 0
    assert counts["closed"]["overlap_characters_trimmed"] >= 400
    readme = (first / "README.md").read_text()
    assert "`overlap_runs_trimmed` (2)" in readme and "`overlap_characters_trimmed`" in readme


def test_a_build_whose_article_is_missing_fails_instead_of_shipping_untrimmed(tmp_path):
    view = provenance_view(tmp_path)
    shutil.rmtree(view / "build__coll_closed" / "synthesized_package")
    out = tmp_path / "out"
    assert pack_capsules.run(arguments(out, view=view, strict=True)) == 1
    failures = {build["build_slug"]: build["failures"] for build in json.loads((out / "SCREEN.json").read_text())["builds"]}
    assert "missing:article_text" in failures["closed"] and failures["open"] == []
