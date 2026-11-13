"""The evaluation-definitions card is computed from the descriptive files of the capsule packs."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import render_evaluation_card as card  # noqa: E402


def write_pack(root: Path, domain: str, states: list[str], kinds: dict[str, int], listed: int | None = None) -> None:
    """Write the three descriptive files of one pack with the given evaluation states and check kinds."""
    pack = root / domain
    pack.mkdir(parents=True)
    complete = states.count("complete")
    (pack / "MANIFEST.json").write_text(json.dumps({
        "builds_packed": 2, "builds_left_out": 1, "capsule_count": len(states), "tooling_commit": "a" * 40,
        "collection_version_doi": f"10.5281/zenodo.{domain}", "generation_date": "2026-11-11",
    }), encoding="utf-8")
    rows = [
        {"eval_state": state, "validation_state": "clean" if state == "complete" else "present",
         "readiness": "evaluable" if state == "complete" else "documented"}
        for state in states
    ]
    (pack / "capsules.jsonl").write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
    (pack / "benchmark-manifest.json").write_text(json.dumps({
        "capsule_count": complete if listed is None else listed,
        "totals": {"checks_by_kind": kinds, "unresolved_references": 5, "input_assets": 4,
                   "input_assets_with_hash": 0, "input_assets_with_download_hint": 1},
    }), encoding="utf-8")


def all_domains(root: Path) -> None:
    for domain in card.DOMAINS:
        write_pack(root, domain, ["complete", "partial", "partial"], {"expert_review": 3, "script_runs": 1})


def test_card_states_definitions_only_and_adds_up(tmp_path):
    all_domains(tmp_path / "packs")
    out = tmp_path / "card.md"

    assert card.main(["--packs", str(tmp_path / "packs"), "--out", str(out)]) == 0

    text = out.read_text(encoding="utf-8")
    assert "**No validation of these definitions exists.**" in text
    assert "prepared and not deposited" in text
    assert "| proteomics | 2 | 1 | 3 | 1 | 2 | 4 | 3 | 1 | 5 | 4 | 0 | 1 |" in text
    assert "| **Total** | **20** | **10** | **30** | **10** | **20** | **40** | **30** | **10** | **50** | **40** | **0** | **10** |" in text
    assert "10 of 30 capsules (33.3 %)" in text
    assert "30 of their 40 checks (75.0 %)" in text
    assert "`script_runs` 10" in text
    assert "`present` 20, `clean` 10, `strict` 0" in text
    assert "| proteomics | 2 | 0 | 1 | 0 |" in text
    assert "| **Total** | **20** | **0** | **10** | **0** |" in text
    assert "## Using the capsules in an evaluation" in text
    assert "not on a workspace that already holds the" in text
    assert "Incomplete card" not in text


def test_missing_domain_is_refused_unless_allowed(tmp_path, capsys):
    write_pack(tmp_path / "packs", "proteomics", ["complete"], {"expert_review": 1})
    out = tmp_path / "card.md"

    assert card.main(["--packs", str(tmp_path / "packs"), "--out", str(out)]) == 1
    assert not out.exists()
    assert "not packed" in capsys.readouterr().err

    assert card.main(["--packs", str(tmp_path / "packs"), "--out", str(out), "--allow-missing"]) == 0
    text = out.read_text(encoding="utf-8")
    assert "**Incomplete card: not packed yet:" in text
    assert "Totals cover the other 1 of 10 domains." in text


def test_listing_that_disagrees_with_the_table_is_refused(tmp_path):
    all_domains(tmp_path / "packs")
    pack = tmp_path / "packs" / "genomics"
    for name in ("MANIFEST.json", "capsules.jsonl", "benchmark-manifest.json"):
        (pack / name).unlink()
    pack.rmdir()
    write_pack(tmp_path / "packs", "genomics", ["complete", "partial"], {"expert_review": 1}, listed=2)

    with pytest.raises(SystemExit, match="genomics: listing holds 2 capsules, table 1"):
        card.main(["--packs", str(tmp_path / "packs"), "--out", str(tmp_path / "card.md")])


def test_unknown_evaluation_state_is_refused(tmp_path):
    write_pack(tmp_path / "packs", "proteomics", ["complete", "invalid"], {"expert_review": 1})

    with pytest.raises(SystemExit, match="evaluation states outside complete and partial"):
        card.main(["--packs", str(tmp_path / "packs"), "--out", str(tmp_path / "card.md"), "--allow-missing"])


def test_deposited_records_are_said_deposited(tmp_path):
    all_domains(tmp_path / "packs")
    out = tmp_path / "card.md"

    assert card.main(["--packs", str(tmp_path / "packs"), "--out", str(out), "--deposited"]) == 0

    text = out.read_text(encoding="utf-8")
    assert "The capsules records are deposited" in text
    assert "not deposited" not in text


def test_pack_without_readiness_column_is_refused(tmp_path):
    write_pack(tmp_path / "packs", "proteomics", ["complete"], {"expert_review": 1})
    capsules = tmp_path / "packs" / "proteomics" / "capsules.jsonl"
    rows = [json.loads(line) for line in capsules.read_text(encoding="utf-8").splitlines()]
    for row in rows:
        del row["readiness"]
    capsules.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")

    with pytest.raises(SystemExit, match="no readiness column"):
        card.main(["--packs", str(tmp_path / "packs"), "--out", str(tmp_path / "card.md"), "--allow-missing"])


def test_unknown_readiness_value_is_refused(tmp_path):
    write_pack(tmp_path / "packs", "proteomics", ["complete"], {"expert_review": 1})
    capsules = tmp_path / "packs" / "proteomics" / "capsules.jsonl"
    capsules.write_text(json.dumps({"eval_state": "complete", "validation_state": "clean", "readiness": "gold"}) + "\n",
                        encoding="utf-8")

    with pytest.raises(SystemExit, match="readiness values outside"):
        card.main(["--packs", str(tmp_path / "packs"), "--out", str(tmp_path / "card.md"), "--allow-missing"])
