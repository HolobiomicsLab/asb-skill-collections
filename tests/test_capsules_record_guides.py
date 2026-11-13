"""Truth and reader guidance of generated capsule-record tables."""

import json
from pathlib import Path

from scripts import capsules_deposit, pack_capsules


FIXTURE = Path(__file__).parent / "fixtures" / "capsules"


def write_json(path, value):
    """Write one test JSON document."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value))


def pack(tmp_path, capsules_doi=None):
    """Pack the capsule fixture with the public CLI arguments."""
    values = {
        "view": FIXTURE / "view", "collection": FIXTURE / "collection",
        "out": tmp_path / "pack", "date": "2026-11-11", "access_records": None,
        "limit": None, "with_indicium": False, "deny_patterns_file": None,
        "strict": True, "pipeline_public": False, "capsules_doi": capsules_doi,
    }
    assert pack_capsules.run(type("Arguments", (), values)()) == 0
    return values["out"]


def test_validation_label_is_lowered_when_entries_contradict_summary(tmp_path):
    path = tmp_path / "validation.json"
    write_json(path, {
        "summary": {"n_claims_checked": 1, "n_supported": 1, "n_partial": 0,
                    "n_unsupported": 0, "n_drift": 0},
        "claims_checked": [{"supported": "partial"}],
    })

    state, claims, consistent = pack_capsules.validation_state(path)

    assert state == "clean"
    assert consistent is False
    assert claims == {
        "from_entries": {"checked": 1, "supported": 0, "partial": 1,
                         "unsupported": 0, "drift": 0, "unknown": 0},
        "declared_summary": {"checked": 1, "supported": 1, "partial": 0,
                             "unsupported": 0, "drift": 0},
    }


def test_validation_counts_unknown_supported_values_apart(tmp_path):
    path = tmp_path / "validation.json"
    write_json(path, {
        "summary": {"n_claims_checked": 2, "n_supported": 2, "n_partial": 0,
                    "n_unsupported": 0, "n_drift": 0},
        "claims_checked": [{"supported": "yes"}, {"supported": "unclear"}],
    })

    state, claims, consistent = pack_capsules.validation_state(path)

    assert state == "clean"
    assert consistent is False
    assert claims["from_entries"]["unknown"] == 1
    assert claims["from_entries"]["checked"] == 2


def test_benchmark_rows_and_totals_expose_evaluation_readiness(tmp_path):
    path = tmp_path / "eval.json"
    write_json(path, {
        "task_id": "task_1", "inputs": [
            {"sha256": "abc", "download_hint": "registry"},
            {"sha256": None, "download_hint": None},
        ],
        "expected_outputs": {},
        "checks": [{"kind": "expert_review"}, {"kind": "expert_review"}, {"kind": "file_exists"}],
        "unresolved_references": ["input:a", "output:b"], "validation_errors": [],
    })
    state, details = pack_capsules.eval_state(path)
    row = {
        "build_slug": "build", "capsule_id": "capsule", "eval_state": state,
        "eval_checks_by_kind": details["checks_by_kind"],
        "eval_unresolved_references": details["unresolved_references"],
        "eval_input_assets": details["input_assets"],
        "eval_input_assets_with_hash": details["input_assets_with_hash"],
        "eval_input_assets_with_download_hint": details["input_assets_with_download_hint"],
    }
    build = {"build_slug": "build", "capsule_ids": ["capsule"], "sha256": "abc"}

    benchmark = pack_capsules.make_benchmark([build], [row], "10.1234/collection")

    assert benchmark["capsules"] == [dict(sorted(row.items()))]
    assert benchmark["totals"] == {
        "checks_by_kind": {"expert_review": 2, "file_exists": 1},
        "unresolved_references": 2, "input_assets": 2,
        "input_assets_with_hash": 1, "input_assets_with_download_hint": 1,
    }
    assert benchmark["listing_statement"] == pack_capsules.EVALUATION_LISTING_STATEMENT


def test_provenance_projection_marks_shipped_members(tmp_path):
    capsule = tmp_path / "capsule"
    write_json(capsule / "artifact_provenance.json", {
        "artifacts": [{"path": "eval.json#checks"}, {"path": "task_card.json"}],
    })
    write_json(capsule / "eval.json", {})

    pack_capsules.mark_artifact_membership(capsule)

    projected = json.loads((capsule / "artifact_provenance.json").read_text())
    assert [item["included_in_capsule"] for item in projected["artifacts"]] == [True, False]
    assert projected["artifact_membership_note"] == pack_capsules.ARTIFACT_MEMBERSHIP_NOTE


def test_manifest_projection_removes_nested_git_state_only():
    manifest = {
        "branch": "scientific", "git": {
            "commit": "outer", "branch": "private", "is_dirty": True,
            "nested": [{"commit": "inner", "branch": "worktree", "is_dirty": False}],
        },
    }

    projected = pack_capsules.project_build_manifest(manifest)

    assert projected == {
        "branch": "scientific",
        "git": {"commit": "outer", "nested": [{"commit": "inner"}]},
    }


def row_paths(value, prefix=""):
    """Return documented paths, treating arbitrary check kinds as one mapping."""
    paths = set()
    for key, item in value.items():
        path = f"{prefix}.{key}" if prefix else key
        paths.add(path)
        if isinstance(item, dict) and path != "eval_checks_by_kind":
            paths.update(row_paths(item, path))
    return paths


def test_field_dictionary_covers_every_written_row_field(tmp_path):
    packed = pack(tmp_path)
    rows = [json.loads(line) for line in (packed / "capsules.jsonl").read_text().splitlines()]
    benchmark = json.loads((packed / "benchmark-manifest.json").read_text())
    defined = set(pack_capsules.CAPSULE_FIELD_DEFINITIONS)
    benchmark_defined = set(pack_capsules.BENCHMARK_FIELD_DEFINITIONS)

    assert all(row_paths(row) <= defined for row in rows)
    assert all(row_paths(row) <= benchmark_defined for row in benchmark["capsules"])
    rendered = pack_capsules.render_field_dictionary()
    assert all(f"`{name}`" in rendered for name in defined | benchmark_defined)


def test_huggingface_card_has_citation_with_and_without_capsules_doi(tmp_path):
    without = pack(tmp_path / "without")
    with_doi = pack(tmp_path / "with", capsules_doi="10.5281/zenodo.2002")
    generic = (without / "hf" / "README.md").read_text()
    cited = (with_doi / "hf" / "README.md").read_text()

    assert "listed on the collection's registry row" in generic
    assert "https://doi.org/10.5281/zenodo.2002" in cited
    assert "https://doi.org/10.1234/example.collection" in cited
    assert "PLACEHOLDER" not in generic + cited and "RESERVED_AFTER_PUBLICATION" not in generic + cited
    assert pack_capsules.EVALUATION_LISTING_STATEMENT in generic


def test_record_and_pack_guides_share_the_dictionary_and_licence_layers(tmp_path):
    packed = pack(tmp_path)
    manifest = json.loads((packed / "MANIFEST.json").read_text())
    screen = json.loads((packed / "SCREEN.json").read_text())
    counts = capsules_deposit.plan_counts(
        manifest,
        [json.loads(line) for line in (packed / "capsules.jsonl").read_text().splitlines()],
        json.loads((packed / "benchmark-manifest.json").read_text()),
    )
    record = capsules_deposit.make_record_readme(manifest, counts, ["asb-synthetic-v1-builds-001.zip"], screen)
    local = (packed / "README.md").read_text()

    assert pack_capsules.render_field_dictionary() in record
    assert pack_capsules.render_field_dictionary() in local
    assert "source paper's licence" in record
    assert "Tools retain their own licences" in record
    assert pack_capsules.EVALUATION_LISTING_STATEMENT in record


def test_refresh_refuses_legacy_rows_missing_current_fields(tmp_path, capsys):
    packed = pack(tmp_path)
    rows_path = packed / "capsules.jsonl"
    rows = [json.loads(line) for line in rows_path.read_text().splitlines()]
    rows[0].pop("validation_summary_consistent")
    rows_path.write_text("\n".join(json.dumps(row) for row in rows) + "\n")

    status = capsules_deposit.main([
        "refresh", "--pack", str(packed), "--collection", str(FIXTURE / "collection"),
        "--out", str(tmp_path / "refreshed"), "--date", "2026-11-11",
    ])

    assert status == 1
    assert "lacks current fields validation_summary_consistent; run a full pack" in capsys.readouterr().err

