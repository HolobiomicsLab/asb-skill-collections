"""A corpus manifest must not advertise more papers than it carries.

Regression for the drift found on metabolomics/v2: commit 9f0682e17 dropped two
merged DOI entries (568 -> 566 papers) and left ``summary`` untouched, so the
released manifest overstated the corpus while every other gate check stayed
green. ``check_catalogue_membership`` reconciled ``collection.yaml`` only.
"""

import pathlib
import sys

import yaml

REPO_ROOT = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT))
from scripts import release_gate  # noqa: E402


def _write_collection(root: pathlib.Path, *, summary, papers) -> pathlib.Path:
    """A minimal, otherwise-consistent collection plus the corpus under test."""
    collection = root / "science" / "v1"
    (collection / "skills" / "alpha").mkdir(parents=True)
    (collection / "skills" / "alpha" / "SKILL.md").write_text("# alpha\n", encoding="utf-8")
    (collection / "tools").mkdir()
    (collection / "tools" / "tool-a.yaml").write_text(
        yaml.safe_dump({"slug": "tool-a"}), encoding="utf-8"
    )
    (collection / "collection.yaml").write_text(
        yaml.safe_dump(
            {
                "skills_count": 1,
                "tools_count": 1,
                "skills": ["alpha"],
                "tools": ["tool-a"],
            }
        ),
        encoding="utf-8",
    )
    (collection / "corpus.yaml").write_text(
        yaml.safe_dump({"summary": summary, "papers": papers}), encoding="utf-8"
    )
    return root


def _messages(result):
    return [d["message"] for d in result.details]


def _papers(n, status="included"):
    return [{"name": f"10.1000/{i}", "doi": f"10.1000/{i}", "status": status} for i in range(n)]


def test_consistent_summary_passes(tmp_path):
    root = _write_collection(
        tmp_path, summary={"total": 3, "included": 3, "hold": 0}, papers=_papers(3)
    )
    result = release_gate.check_catalogue_membership(root)
    assert result.status == release_gate.PASS, _messages(result)


def test_total_overstating_the_array_fails(tmp_path):
    root = _write_collection(
        tmp_path, summary={"total": 5, "included": 5, "hold": 0}, papers=_papers(3)
    )
    result = release_gate.check_catalogue_membership(root)
    assert result.status == release_gate.FAIL
    assert any("summary.total is 5" in m and "3 entries" in m for m in _messages(result))


def test_included_count_must_match_paper_status(tmp_path):
    papers = _papers(3) + _papers(2, status="hold")
    root = _write_collection(
        tmp_path, summary={"total": 5, "included": 5, "hold": 0}, papers=papers
    )
    result = release_gate.check_catalogue_membership(root)
    assert result.status == release_gate.FAIL
    joined = " ".join(_messages(result))
    assert "summary.included is 5" in joined and "3 papers carry status='included'" in joined
    assert "summary.hold is 0" in joined and "2 papers carry status='hold'" in joined


def test_hold_split_that_agrees_passes(tmp_path):
    """metabolomics/v1's shape: total counts every paper, included excludes holds."""
    papers = _papers(3) + _papers(2, status="hold")
    root = _write_collection(
        tmp_path, summary={"total": 5, "included": 3, "hold": 2}, papers=papers
    )
    result = release_gate.check_catalogue_membership(root)
    assert result.status == release_gate.PASS, _messages(result)


def test_status_absent_counts_as_included(tmp_path):
    papers = [{"name": "10.1000/x", "doi": "10.1000/x"} for _ in range(4)]
    root = _write_collection(
        tmp_path, summary={"total": 4, "included": 4, "hold": 0}, papers=papers
    )
    result = release_gate.check_catalogue_membership(root)
    assert result.status == release_gate.PASS, _messages(result)


def test_collection_without_a_corpus_is_not_checked(tmp_path):
    root = _write_collection(
        tmp_path, summary={"total": 1, "included": 1, "hold": 0}, papers=_papers(1)
    )
    (root / "science" / "v1" / "corpus.yaml").unlink()
    result = release_gate.check_catalogue_membership(root)
    assert result.status == release_gate.PASS, _messages(result)
