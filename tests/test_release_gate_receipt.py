"""INT-ASB-025 regressions for empty release-gate measurements.

These exercise the existing CLI and report rather than a replacement gate.
Every collection is synthetic and lives under pytest's temporary directory.
"""

import hashlib
import json
import shutil

import pytest
import yaml

from scripts import release_gate


def _write_collection(collection, *, paper_status="included", with_skill=True):
    collection.mkdir()
    papers = [{
        "doi": "10.0000/synthetic-receipt",
        "status": paper_status,
        "access": {"type": "gold-oa"},
    }]
    (collection / "corpus.yaml").write_text(yaml.safe_dump({"papers": papers}))
    if with_skill:
        leaf = collection / "leaves" / "synthetic-operation" / "SKILL.md"
        leaf.parent.mkdir(parents=True)
        frontmatter = {
            "name": "synthetic-operation",
            "license": "CC-BY-4.0",
            "derived_from": [{"doi": papers[0]["doi"]}],
            "evidence_spans": [{"doi": papers[0]["doi"], "text": "Synthetic evidence."}],
        }
        leaf.write_text("---\n" + yaml.safe_dump(frontmatter) + "---\n# Procedure\n")
    return collection


@pytest.mark.parametrize("target", ["empty", "excluded_papers", "no_skills", "missing_corpus"])
def test_strict_gate_cannot_verify_an_empty_or_skipped_target(tmp_path, target):
    collection = tmp_path / "collection"
    if target == "empty":
        collection.mkdir()
    else:
        _write_collection(
            collection,
            paper_status="excluded" if target == "excluded_papers" else "included",
            with_skill=target != "no_skills",
        )
        if target == "missing_corpus":
            (collection / "corpus.yaml").unlink()

    exit_code = release_gate.main([str(collection), "--strict", "--quiet"])
    report = json.loads((collection / "gate_report.json").read_text())

    assert exit_code == 1, report
    assert report["overall_status"] == "uncheckable"
    assert report["blocking"] is True
    empty_checks = [check for check in report["checks"] if check["counts"]["checked"] == 0]
    assert empty_checks, "The receipt must identify the checks with no measured items."
    assert any(check["status"] == "uncheckable" for check in empty_checks)


def test_receipt_and_human_summary_report_item_counts(tmp_path, capsys):
    collection = _write_collection(tmp_path / "collection")
    report = release_gate.run_gate(collection, None, True)
    release_gate._print_human_summary(report)
    summary = capsys.readouterr().out

    for check in report["checks"]:
        counts = check.get("counts")
        assert counts is not None, f"{check['name']}: item counts missing"
        assert set(counts) == {"checked", "skipped", "missing", "failed"}
        assert all(isinstance(value, int) and value >= 0 for value in counts.values())
        line = next(line for line in summary.splitlines() if check["name"] in line)
        for label, value in counts.items():
            assert f"{label}={value}" in line


def _check(report, name):
    return next(check for check in report["checks"] if check["name"] == name)


def _edit_frontmatter(collection, edit):
    leaf = collection / "leaves/synthetic-operation/SKILL.md"
    fm, body = release_gate._read_frontmatter(leaf.read_text())
    edit(fm)
    leaf.write_text("---\n" + yaml.safe_dump(fm) + "---\n" + body)


@pytest.mark.parametrize("strict", [False, True])
def test_no_spans_is_uncheckable_even_when_a_file_was_inspected(tmp_path, strict):
    collection = _write_collection(tmp_path / "collection")
    _edit_frontmatter(collection, lambda fm: fm.pop("evidence_spans"))
    report = release_gate.run_gate(collection, None, strict)

    assert report["exit_code"] == 1
    assert report["overall_status"] == "uncheckable"
    assert report["release_verified"] is False
    for name in ("strip_verbatim_similarity", "pii_dual_use"):
        check = _check(report, name)
        assert check["status"] == "uncheckable"
        assert check["counts"]["checked"] == 0
        assert check["coverage"]["inspected_files"] == 1
        assert check["coverage"]["files_without_spans"] == 1


def test_advisory_empty_target_also_blocks(tmp_path):
    report = release_gate.run_gate(tmp_path, None, False)
    assert report["exit_code"] == 1
    assert report["overall_status"] == "uncheckable"


def test_advisory_content_failure_is_explicitly_diagnostic(tmp_path, capsys):
    collection = _write_collection(tmp_path / "collection")
    _edit_frontmatter(collection, lambda fm: fm.pop("license"))
    assert release_gate.main([str(collection)]) == 0
    report = json.loads((collection / "gate_report.json").read_text())
    assert report["overall_status"] == "fail"
    assert report["release_verified"] is False
    assert report["verification_scope"] == "diagnostic run, not a release verification"
    assert report["verification_scope"] in capsys.readouterr().out
    assert release_gate.main([str(collection), "--verify", "--quiet"]) == 1


def test_counts_are_items_not_findings_and_workflows_are_optional(tmp_path):
    collection = _write_collection(tmp_path / "collection")
    _edit_frontmatter(collection, lambda fm: fm["evidence_spans"].append({
        "text": "MRN 4820193; synthetic.person@example.net", "doi": "10.0000/synthetic-receipt",
    }))
    corpus = yaml.safe_load((collection / "corpus.yaml").read_text())
    corpus["papers"].append({"doi": "10.0000/skipped", "status": "excluded"})
    (collection / "corpus.yaml").write_text(yaml.safe_dump(corpus))
    report = release_gate.run_gate(collection, None, True)
    pii = _check(report, "pii_dual_use")
    assert pii["counts"] == {"checked": 2, "skipped": 0, "missing": 0, "failed": 1}
    assert len([d for d in pii["details"] if d["status"] == "fail"]) >= 2
    access = _check(report, "access_tier_oa")
    assert access["counts"] == {"checked": 1, "skipped": 1, "missing": 0, "failed": 0}
    workflows = _check(report, "composite_workflows")
    assert workflows["status"] == "not_applicable"
    assert workflows["counts"]["checked"] == 0


def _digest(value):
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(encoded.encode()).hexdigest()


def _entries(root, excluded=()):
    entries = []
    for path in sorted(root.rglob("*")):
        name = path.relative_to(root).as_posix()
        if name in excluded:
            continue
        entry = {"path": name}
        if path.is_dir():
            entry["directory"] = True
        else:
            payload = path.read_bytes()
            entry.update(bytes=len(payload), sha256=hashlib.sha256(payload).hexdigest())
        entries.append(entry)
    return entries


def test_receipt_binds_exact_payload_and_reverifies_without_writing(tmp_path):
    collection = _write_collection(tmp_path / "collection")
    assert release_gate.main([str(collection), "--strict", "--quiet"]) == 0
    receipt = collection / "gate_report.json"
    report = json.loads(receipt.read_text())
    payload = report["binding"]["payload"]
    expected = _entries(collection, ("gate_report.json", "MANIFEST.gen.json"))
    assert payload["entries"] == expected
    assert payload["sha256"] == _digest(expected)
    assert report["binding"]["manifest"] is None
    assert report["inventory"] == {"skills": 1, "papers": 1, "dois": 1, "tools": 0, "workflows": 0}
    assert report["policy"]["version"]
    assert len(report["policy"]["config_sha256"]) == 64
    assert report["release_verified"] is True
    before = _entries(collection)
    assert release_gate.main([str(collection), "--verify", "--quiet"]) == 0
    assert _entries(collection) == before
    leaf = collection / "leaves/synthetic-operation/SKILL.md"
    leaf.write_bytes(leaf.read_bytes() + b"x")
    assert release_gate.main([str(collection), "--verify", "--quiet"]) == 1
    assert json.loads(receipt.read_text()) == report


@pytest.mark.parametrize("change", ["add", "remove", "rename", "metadata", "policy", "receipt"])
def test_reverification_rejects_target_or_policy_or_receipt_changes(tmp_path, monkeypatch, change):
    collection = _write_collection(tmp_path / "collection")
    assert release_gate.main([str(collection), "--strict", "--quiet"]) == 0
    leaf = collection / "leaves/synthetic-operation/SKILL.md"
    if change == "add":
        (collection / "extra.txt").write_text("Added payload")
    elif change == "remove":
        leaf.unlink()
    elif change == "rename":
        leaf.parent.rename(leaf.parent.with_name("renamed-operation"))
    elif change == "metadata":
        (collection / "corpus.yaml").write_text((collection / "corpus.yaml").read_text() + "# change\n")
    elif change == "policy":
        monkeypatch.setitem(release_gate.PII_CONFIG, "version", "changed")
    else:
        receipt = collection / "gate_report.json"
        report = json.loads(receipt.read_text())
        report["checks"][0]["counts"]["checked"] += 1
        receipt.write_text(json.dumps(report))
    assert release_gate.main([str(collection), "--verify", "--quiet"]) == 1


@pytest.mark.parametrize("external_report", [False, True])
def test_report_override_excludes_only_the_selected_receipt(tmp_path, external_report):
    collection = _write_collection(tmp_path / "collection")
    report_path = (tmp_path if external_report else collection) / "custom.json"
    (collection / "gate_report.json").write_text('{"older": "payload"}')
    args = [str(collection), "--report", str(report_path), "--quiet"]
    assert release_gate.main(args + ["--strict"]) == 0
    report = json.loads(report_path.read_text())
    assert "gate_report.json" in {entry["path"] for entry in report["binding"]["payload"]["entries"]}
    assert release_gate.main(args + ["--verify"]) == 0


def test_external_corpus_is_bound_and_required_on_reverification(tmp_path):
    collection = _write_collection(tmp_path / "collection")
    corpus = tmp_path / "source-corpus.yaml"
    (collection / "corpus.yaml").rename(corpus)
    args = [str(collection), "--corpus", str(corpus), "--quiet"]
    assert release_gate.main(args + ["--strict"]) == 0
    corpus.write_text(corpus.read_text() + "# changed\n")
    assert release_gate.main(args + ["--verify"]) == 1
    corpus.unlink()
    assert release_gate.main(args + ["--verify"]) == 1


@pytest.mark.parametrize("unit_type", ["data-only", "empty"])
def test_declared_nonskill_unit_never_claims_skill_validation(tmp_path, unit_type):
    (tmp_path / "collection.yaml").write_text(yaml.safe_dump({"unit_type": unit_type}))
    report = release_gate.run_gate(tmp_path, None, True)
    assert report["unit_type"] == unit_type
    assert report["release_verified"] is False
    assert report["exit_code"] == 1
    assert "skill validation" in report["verification_scope"]
    assert _check(report, "provenance_doi_license")["counts"]["checked"] == 0


def test_inventory_uses_source_identities_and_files_and_checks_declarations(tmp_path):
    collection = _write_collection(tmp_path / "collection")
    corpus = yaml.safe_load((collection / "corpus.yaml").read_text())
    corpus["source_capsules"] = [{"id": "run/a"}, {"id": "run/a"}, {"id": "run/b"}]
    (collection / "corpus.yaml").write_text(yaml.safe_dump(corpus))
    (collection / "tools").mkdir()
    (collection / "tools/a.yaml").write_text("name: Tool A\n")
    task = collection / "benchmark/tasks/a"
    task.mkdir(parents=True)
    (task / "workflow.cwl").write_text("class: CommandLineTool\n")
    descriptor = collection / "collection.yaml"
    descriptor.write_text("n_skills: 1\nn_papers: 2\nn_dois: 1\nn_tools: 1\nn_workflows: 1\n")
    report = release_gate.run_gate(collection, None, True)
    assert report["exit_code"] == 0
    assert report["inventory"] == {"skills": 1, "papers": 2, "dois": 1, "tools": 1, "workflows": 1}
    descriptor.write_text(descriptor.read_text().replace("n_skills: 1", "n_skills: 9"))
    report = release_gate.run_gate(collection, None, True)
    assert report["exit_code"] == 1
    assert _check(report, "collection_inventory")["counts"]["failed"] == 1


def _write_cut_manifest(collection, source):
    roots = [{"name": source.name, "excluded_paths": [], "entries": _entries(source), "ancestors": []}]
    output = _entries(collection, ("MANIFEST.gen.json", "gate_report.json"))
    record = {
        "schema": "asb-cut/v0",
        "inputs": {"roots": roots, "sha256": _digest(roots)},
        "output": {"entries": output, "sha256": _digest(output), "excluded_paths": ["MANIFEST.gen.json"]},
        "inventory": {"skills": 1, "papers": 1, "dois": 1, "tools": 0, "workflows": 0},
    }
    record["sha256"] = _digest(record)
    path = collection / "MANIFEST.gen.json"
    path.write_text(json.dumps(record, sort_keys=True))
    return path


@pytest.mark.parametrize("mutation", ["manifest", "source", "source_missing"])
def test_cut_manifest_and_source_closure_are_bound(tmp_path, mutation):
    collection = _write_collection(tmp_path / "collection")
    source = tmp_path / "source"
    source.mkdir()
    (source / "card.json").write_text('{"doi": "10.0000/synthetic-receipt"}')
    manifest = _write_cut_manifest(collection, source)
    args = [str(collection), "--inputs", str(source), "--quiet"]
    assert release_gate.main(args + ["--strict"]) == 0
    report = json.loads((collection / "gate_report.json").read_text())
    assert report["binding"]["manifest"]["sha256"] == hashlib.sha256(manifest.read_bytes()).hexdigest()
    assert release_gate.main(args + ["--verify"]) == 0
    if mutation == "manifest":
        manifest.write_bytes(manifest.read_bytes() + b" ")
    elif mutation == "source":
        (source / "card.json").write_text("{}")
    else:
        shutil.rmtree(source)
    assert release_gate.main(args + ["--verify"]) == 1


def test_cut_without_its_required_inputs_is_uncheckable(tmp_path):
    collection = _write_collection(tmp_path / "collection")
    source = tmp_path / "source"
    source.mkdir()
    (source / "card.json").write_text("{}")
    _write_cut_manifest(collection, source)
    report = release_gate.run_gate(collection, None, True)
    assert report["exit_code"] == 1
    assert report["overall_status"] == "uncheckable"
    assert _check(report, "cut_input_closure")["counts"]["missing"] == 1


def test_unknown_or_malformed_receipt_cannot_verify(tmp_path):
    collection = _write_collection(tmp_path / "collection")
    receipt = collection / "gate_report.json"
    for value in ("not JSON", "[]", '{"schema": "asbb-release-gate/1.0"}'):
        receipt.write_text(value)
        assert release_gate.main([str(collection), "--verify", "--quiet"]) == 1


def test_report_cannot_overwrite_a_payload_or_manifest_file(tmp_path):
    collection = _write_collection(tmp_path / "collection")
    corpus = collection / "corpus.yaml"
    original = corpus.read_bytes()
    assert release_gate.main([str(collection), "--strict", "--report", str(corpus), "--quiet"]) == 2
    assert corpus.read_bytes() == original


def test_report_override_normalizes_equivalent_paths(tmp_path):
    collection = _write_collection(tmp_path / "collection")
    report_path = collection / ".." / "collection" / "custom.json"
    args = [str(collection), "--report", str(report_path), "--quiet"]
    assert release_gate.main(args + ["--strict"]) == 0
    assert release_gate.main(args + ["--verify"]) == 0


def test_missing_individual_cut_input_is_counted(tmp_path):
    collection = _write_collection(tmp_path / "collection")
    source = tmp_path / "source"
    source.mkdir()
    card = source / "card.json"
    card.write_text("{}")
    (source / "context.txt").write_text("Source context")
    _write_cut_manifest(collection, source)
    card.unlink()
    report = release_gate.run_gate(collection, None, True, inputs=[source])
    counts = _check(report, "cut_input_closure")["counts"]
    assert counts == {"checked": 1, "skipped": 0, "missing": 1, "failed": 0}
    assert report["overall_status"] == "uncheckable"


def test_advertised_index_cannot_hide_a_missing_leaf(tmp_path):
    collection = _write_collection(tmp_path / "collection")
    (collection / "skills_index.json").write_text(json.dumps([
        {"slug": "synthetic-operation"}, {"slug": "missing-operation"},
    ]))
    report = release_gate.run_gate(collection, None, True)
    assert report["exit_code"] == 1
    assert _check(report, "collection_inventory")["counts"]["failed"] == 1


def test_gate_detects_corpus_change_between_loading_and_measuring(tmp_path, monkeypatch):
    collection = _write_collection(tmp_path / "collection")
    original_loader = release_gate._load_yaml
    corpus_path = collection / "corpus.yaml"

    def change_after_read(path):
        value = original_loader(path)
        if path == corpus_path:
            path.write_text(path.read_text() + "# changed during gate\n")
        return value

    monkeypatch.setattr(release_gate, "_load_yaml", change_after_read)
    report = release_gate.run_gate(collection, None, True)
    assert report["exit_code"] == 1
    assert _check(report, "target_stability")["counts"]["failed"] == 1


def test_empty_optional_workflow_directory_is_not_a_passing_measurement(tmp_path):
    collection = _write_collection(tmp_path / "collection")
    (collection / "workflows").mkdir()
    check = release_gate.check_workflows(collection)
    assert check.status == "not_applicable"
    assert check.counts["checked"] == 0


@pytest.mark.parametrize("scope", ["payload", "manifest"])
def test_output_symlinks_cannot_escape_the_target_binding(tmp_path, scope):
    collection = _write_collection(tmp_path / "collection")
    outside = tmp_path / "external.txt"
    outside.write_text("External payload")
    target = "external.txt" if scope == "payload" else "MANIFEST.gen.json"
    (collection / target).symlink_to(outside)
    report = release_gate.run_gate(collection, None, True)
    assert report["exit_code"] == 1
    assert report["overall_status"] == "uncheckable"


def test_receipt_exclusion_cannot_be_a_whole_payload_directory(tmp_path):
    collection = _write_collection(tmp_path / "collection")
    report = release_gate.run_gate(collection, None, True, report_path=collection / "leaves")
    assert report["exit_code"] == 1
    assert report["overall_status"] == "uncheckable"


def test_boolean_manifest_count_is_not_an_integer_inventory(tmp_path):
    collection = _write_collection(tmp_path / "collection")
    source = tmp_path / "source"
    source.mkdir()
    (source / "card.json").write_text("{}")
    manifest = _write_cut_manifest(collection, source)
    record = json.loads(manifest.read_text())
    record["inventory"]["skills"] = True
    record.pop("sha256")
    record["sha256"] = _digest(record)
    manifest.write_text(json.dumps(record))
    report = release_gate.run_gate(collection, None, True, inputs=[source])
    assert report["exit_code"] == 1
    assert report["overall_status"] == "uncheckable"
