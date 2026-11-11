import hashlib
import json
import shutil
import zipfile
from pathlib import Path

from scripts import pack_capsules, zenodo_deposit

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
    assert manifest["capsule_count"] == 6
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
    serialized = json.dumps(metadata) + (out / "hf" / "README.md").read_text()
    assert "HolobiomicsLab/asb-skills-metabolomics" not in serialized
    assert "capsules.jsonl" in (out / "hf" / "README.md").read_text()
    archive_texts = []
    for build in manifest["builds"]:
        archive = out / build["zip_member"]
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
    assert "C:\\" not in all_text


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
    assert not (out / "builds").exists()
    screen_text = (out / "SCREEN.json").read_text()
    assert json.loads(screen_text)["totals"]["deny_hits"] == 4
    assert "synthetic-partner" not in screen_text


def test_with_indicium_is_explicitly_recorded(tmp_path):
    out = tmp_path / "indicium"
    pack_capsules.run(arguments(out, with_indicium=True, strict=True))
    manifest = json.loads((out / "MANIFEST.json").read_text())
    assert manifest["inclusion_policy"]["with_indicium"] is True
    archive = out / manifest["builds"][0]["zip_member"]
    with zipfile.ZipFile(archive) as zipped:
        assert "indicium.jsonld" in zipped.namelist()


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
