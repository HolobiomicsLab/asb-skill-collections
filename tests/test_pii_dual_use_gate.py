"""Red-team recall harness for the PII / dual-use content-safety gate.

CONTENT_POLICY.md §6 (line 295) requires the gate to catch the HARD_FAIL category
with high recall on a red-team fixture before any release. This harness runs the
*real* gate (`release_gate.check_pii_dual_use`) over `fixtures/pii_dual_use_red_team.jsonl`,
reports measured recall + precision, and asserts recall >= the target.

**The target is human-owned and currently unreconciled** (CONTENT_POLICY=0.95 vs
asbb-v0=0.80 — the `pii-recall-target` gate item). Until a single number is written
into `fixtures/pii_recall_target.json`, the recall assertion is skipped (but recall is
still measured and reported, and precision on benign controls is always enforced). No
threshold is hardcoded here.

The fixture is synthetic and benign-by-construction: the HARD_FAIL rows only carry the
*structure* the regexes key on (a fake MRN, a reserved-domain email, a generic
DURC-framed sentence), never real personal data or an actionable dual-use payload.
"""
import json
import pathlib
import sys

import pytest
import yaml

REPO_ROOT = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT))
from scripts import release_gate  # noqa: E402
from scripts.release_gate import FAIL  # noqa: E402

FIXTURE = pathlib.Path(__file__).parent / "fixtures" / "pii_dual_use_red_team.jsonl"
TARGET_CFG = pathlib.Path(__file__).parent / "fixtures" / "pii_recall_target.json"


def _rows():
    return [json.loads(l) for l in FIXTURE.read_text().splitlines() if l.strip()]


def _build_collection(tmp_path, rows):
    """Write one synthetic skill per fixture row; return the collection dir."""
    for row in rows:
        skill_dir = tmp_path / "skills" / row["id"]
        skill_dir.mkdir(parents=True, exist_ok=True)
        fm = {"evidence_spans": [{"text": row["text"], "doi": "10.0000/synthetic", "section": "fixture"}]}
        (skill_dir / "SKILL.md").write_text(
            "---\n" + yaml.safe_dump(fm, sort_keys=False) + "---\n# fixture\n",
            encoding="utf-8",
        )
    return tmp_path


def _fail_ids(tmp_path, rows):
    """Run the real gate; return the set of row ids that produced >=1 FAIL."""
    collection = _build_collection(tmp_path, rows)
    result = release_gate.check_pii_dual_use(collection, {})
    failed = set()
    for finding in result.details:
        if finding.get("status") != FAIL:
            continue
        f = finding.get("file", "")
        parts = pathlib.Path(f).parts
        if len(parts) >= 2:
            failed.add(parts[-2])  # skills/<id>/SKILL.md
    return failed


def _load_target():
    return json.loads(TARGET_CFG.read_text()).get("hard_fail_recall_target")


def test_benign_controls_do_not_hard_fail(tmp_path):
    """Precision: clean spans (notation email, allowlisted email, plain method text)
    must not produce a FAIL. Over-firing manufactures phantom safety violations."""
    rows = _rows()
    benign = [r for r in rows if not r["should_flag"]]
    assert benign, "fixture has no benign controls"
    failed = _fail_ids(tmp_path, benign)
    over = sorted(r["id"] for r in benign if r["id"] in failed)
    assert not over, f"benign controls wrongly FAILed (false positives): {over}"


def test_hard_fail_recall(tmp_path, capsys):
    """Recall: measure the fraction of HARD_FAIL red-team rows the gate catches.
    Assert against the target only when a human has reconciled it."""
    rows = _rows()
    positives = [r for r in rows if r["should_flag"]]
    assert positives, "fixture has no positive (should_flag) rows"

    failed = _fail_ids(tmp_path, positives)
    caught = [r["id"] for r in positives if r["id"] in failed]
    missed = [r["id"] for r in positives if r["id"] not in failed]
    recall = len(caught) / len(positives)

    with capsys.disabled():
        print(f"\n[pii-recall] {len(caught)}/{len(positives)} caught "
              f"(recall={recall:.3f}); missed={missed or 'none'}")

    target = _load_target()
    if target is None:
        pytest.skip(
            f"recall={recall:.3f} measured, but the target is unreconciled "
            "(CONTENT_POLICY=0.95 vs asbb-v0=0.80). Set hard_fail_recall_target in "
            "tests/fixtures/pii_recall_target.json to activate this gate — see pii-recall-target."
        )
    assert recall >= target, (
        f"recall {recall:.3f} < target {target}; missed HARD_FAIL rows: {missed}"
    )


def test_fixture_is_well_formed():
    rows = _rows()
    assert len(rows) >= 10
    ids = [r["id"] for r in rows]
    assert len(ids) == len(set(ids)), "duplicate fixture ids"
    for r in rows:
        assert set(r) >= {"id", "category", "should_flag", "text"}
        assert isinstance(r["should_flag"], bool)


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q", "-s"]))
