"""Integration test for the promotion hard-gate (`promote-collection.yml` §7.2).

`promote-collection.yml` runs `python scripts/release_gate.py <dir> --strict`, so its
promote/block decision IS `release_gate.main([dir, "--strict"])`'s exit code. This drives
that real CLI over tiny synthetic collections and asserts the code for a promotable
collection and for each blocking condition — the regression test the gate had only as a
one-off manual check. It also pins the strict-vs-advisory split promote-collection.yml
relies on (staged PRs advisory → exit 0; promotion strict → exit 1 on any FAIL).
"""
import json
import pathlib
import sys

import pytest
import yaml

REPO_ROOT = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT))
from scripts import release_gate  # noqa: E402

_CLEAN_BODY = "# skill\nChromatographic separation improved analyte resolution.\n"
_LEAF = {"name": "s1", "derived_from": [{"doi": "10.1/x"}], "license": "CC-BY-4.0"}


def _collection(tmp_path, papers, skills):
    col = tmp_path / "col"
    (col / "skills").mkdir(parents=True)
    (col / "corpus.yaml").write_text(yaml.safe_dump({"papers": papers}))
    for slug, fm, body in skills:
        d = col / "skills" / slug
        d.mkdir()
        (d / "SKILL.md").write_text("---\n" + yaml.safe_dump(fm) + "---\n" + body)
    return col


def _run(col, strict):
    args = [str(col)] + (["--strict"] if strict else [])
    return release_gate.main(args)


# (id, papers, skills, blocks_under_strict)
CASES = [
    ("promotable",
     [{"doi": "10.1/x", "status": "included", "access": {"type": "gold-oa"}, "repo_url": ""}],
     [("s1", _LEAF, _CLEAN_BODY)], False),
    ("repo_oa_without_repo_url",
     [{"doi": "10.1/x", "status": "included", "access": {"type": "repo-oa"}, "repo_url": ""}],
     [("s1", _LEAF, _CLEAN_BODY)], True),
    ("non_oa_access_type",
     [{"doi": "10.1/x", "status": "included", "access": {"type": "paywalled"}, "repo_url": ""}],
     [("s1", _LEAF, _CLEAN_BODY)], True),
    ("skill_without_source_doi",
     [{"doi": "10.1/x", "status": "included", "access": {"type": "gold-oa"}, "repo_url": ""}],
     [("s1", {"name": "s1", "license": "CC-BY-4.0"}, _CLEAN_BODY)], True),
]


@pytest.mark.parametrize("cid,papers,skills,blocks", CASES, ids=[c[0] for c in CASES])
def test_strict_promotion_gate_exit_code(tmp_path, cid, papers, skills, blocks):
    """Under --strict (promotion), a FAIL blocks (exit 1); a clean collection promotes (0)."""
    col = _collection(tmp_path, papers, skills)
    rc = _run(col, strict=True)
    assert rc == (1 if blocks else 0), f"{cid}: strict rc {rc}, expected {1 if blocks else 0}"


@pytest.mark.parametrize("cid,papers,skills,blocks", CASES, ids=[c[0] for c in CASES])
def test_advisory_never_blocks(tmp_path, cid, papers, skills, blocks):
    """Without --strict (staged PRs), even a FAIL is advisory → exit 0."""
    col = _collection(tmp_path, papers, skills)
    assert _run(col, strict=False) == 0, f"{cid}: advisory must exit 0"


def test_the_repo_oa_evidence_fail_is_what_blocks(tmp_path):
    """The repo-oa-without-repo_url block is the evidence gate, not some other check."""
    col = _collection(
        tmp_path,
        [{"doi": "10.1/x", "status": "included", "access": {"type": "repo-oa"}, "repo_url": ""}],
        [("s1", _LEAF, _CLEAN_BODY)],
    )
    _run(col, strict=True)
    report = json.loads((col / "gate_report.json").read_text())
    access = next(c for c in report["checks"] if c["name"] == "access_tier_oa")
    assert any("repo_url is empty" in d["message"] for d in access["details"]), (
        "expected the repo_url-evidence FAIL to be the blocking finding"
    )


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
