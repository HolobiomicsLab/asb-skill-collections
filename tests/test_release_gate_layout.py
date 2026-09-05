"""The layout gate: one file per skill, two at most (INT-ASB-010, R6).

Before this check existed the release gate ran five *content* checks and no
packaging check at all — no required-files list, no forbidden-files list, no
byte budget, and nothing reconciling ``skills_index.json`` against the skills
actually on disk. The one-file-per-skill invariant was a convention, so a build
that leaked a ``docs/`` tree or a private intermediate into a promoted bundle
would have shipped it, and an index entry pointing at a skill that was never
written would have advertised a 404.

The four cases the spec names are pinned below, plus the two things a gate
like this most easily gets wrong:

* **It must not fail on the tree that is already shipped.** All four published
  collections hold exactly ``SKILL.md`` in every skill directory, and
  ``collections/epigenomics/v1`` is driven through ``--strict`` by an existing
  test that requires exit 0. A gate that reddens the current release is not a
  gate, it is an outage, so the real collections are asserted to pass.
* **It must refuse rather than truncate.** Both budgets FAIL. A truncated
  sidecar still parses, so truncating would ship a knowledge-base manifest that
  silently understates itself — the exact confusion the status enum exists to
  prevent.
"""

import json
import pathlib
import sys

import pytest
import yaml

REPO_ROOT = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT))
from scripts import release_gate  # noqa: E402

CLEAN_BODY = "# skill\nChromatographic separation improved analyte resolution.\n"
LEAF_FM = {"name": "s1", "derived_from": [{"doi": "10.1/x"}], "license": "CC-BY-4.0"}
PAPERS = [{"doi": "10.1/x", "status": "included", "access": {"type": "gold-oa"}, "repo_url": ""}]


def _collection(tmp_path, slugs=("s1",), leaf_dirname="skills"):
    """A minimal collection that passes every other check in the gate."""
    col = tmp_path / "col"
    (col / leaf_dirname).mkdir(parents=True)
    (col / "corpus.yaml").write_text(yaml.safe_dump({"papers": PAPERS}))
    for slug in slugs:
        d = col / leaf_dirname / slug
        d.mkdir()
        fm = dict(LEAF_FM, name=slug)
        (d / "SKILL.md").write_text("---\n" + yaml.safe_dump(fm) + "---\n" + CLEAN_BODY)
    return col


def _sidecar(n_entries=1):
    return {
        "schema_version": 1,
        "n_entries": n_entries,
        "total_bytes": 0,
        "notes": "pointer form",
        "entries": [
            {"path": f"e{i}.md", "kind": "readme", "source_url": "", "sha256": "0" * 64, "bytes": 0}
            for i in range(n_entries)
        ],
    }


def _layout(col, **kwargs):
    return release_gate.check_layout(col, **kwargs)


def _messages(res):
    return " | ".join(d["message"] for d in res.details)


# --------------------------------------------------------------------------- #
# The four cases of the spec table.                                            #
# --------------------------------------------------------------------------- #
def test_skill_md_alone_passes(tmp_path):
    res = _layout(_collection(tmp_path))
    assert res.status == release_gate.PASS, _messages(res)


def test_skill_md_plus_sidecar_passes(tmp_path):
    col = _collection(tmp_path)
    (col / "skills" / "s1" / "skill_kb.json").write_text(json.dumps(_sidecar()))
    res = _layout(col)
    assert res.status == release_gate.PASS, _messages(res)


def test_an_extra_file_fails(tmp_path):
    col = _collection(tmp_path)
    (col / "skills" / "s1" / "README.md").write_text("# leaked intermediate\n")
    res = _layout(col)
    assert res.status == release_gate.FAIL
    assert "README.md" in _messages(res)


def test_a_leaked_docs_tree_fails_by_its_nested_path(tmp_path):
    """The shape promote now measures and refuses to copy — named, not just counted."""
    col = _collection(tmp_path)
    docs = col / "skills" / "s1" / "docs"
    docs.mkdir()
    (docs / "page.md").write_text("text\n")
    res = _layout(col)
    assert res.status == release_gate.FAIL
    assert "docs/page.md" in _messages(res)


def test_an_over_budget_sidecar_fails(tmp_path):
    col = _collection(tmp_path)
    (col / "skills" / "s1" / "skill_kb.json").write_text(json.dumps(_sidecar(2000)))
    res = _layout(col)
    assert res.status == release_gate.FAIL
    over = [d for d in res.details if "per-skill budget" in d["message"]]
    assert over and over[0]["bytes"] > release_gate._KB_SIDECAR_MAX_BYTES
    assert over[0]["budget"] == release_gate._KB_SIDECAR_MAX_BYTES


def test_the_over_budget_sidecar_is_refused_not_truncated(tmp_path):
    """The gate reports; it must not rewrite the collection it is inspecting."""
    col = _collection(tmp_path)
    sidecar = col / "skills" / "s1" / "skill_kb.json"
    sidecar.write_text(json.dumps(_sidecar(2000)))
    before = sidecar.read_bytes()
    _layout(col)
    assert sidecar.read_bytes() == before
    assert "do not truncate" in _messages(_layout(col))


def test_index_mismatch_fails_in_both_directions(tmp_path):
    col = _collection(tmp_path, slugs=("alpha", "beta"), leaf_dirname="leaves")
    (col / "skills").mkdir()
    (col / "skills_index.json").write_text(
        json.dumps([{"slug": "alpha"}, {"slug": "never-written"}])
    )
    res = _layout(col)
    assert res.status == release_gate.FAIL
    msgs = _messages(res)
    assert "never-written" in msgs, "an index entry with no skill on disk must fail"
    assert "leaves/beta" in msgs, "a leaf the index never names must fail"
    assert "alpha" not in msgs.replace("leaves/beta", ""), "the matching slug must not be flagged"


# --------------------------------------------------------------------------- #
# Boundaries and the two-sided checks.                                         #
# --------------------------------------------------------------------------- #
def test_the_budget_boundary_is_the_declared_constant(tmp_path):
    col = _collection(tmp_path, slugs=("s1", "s2"))
    exact = col / "skills" / "s1" / "skill_kb.json"
    exact.write_bytes(b"x" * release_gate._KB_SIDECAR_MAX_BYTES)
    assert _layout(col).status == release_gate.PASS

    one_over = col / "skills" / "s2" / "skill_kb.json"
    one_over.write_bytes(b"x" * (release_gate._KB_SIDECAR_MAX_BYTES + 1))
    assert _layout(col).status == release_gate.FAIL


def test_the_collection_budget_fails_even_when_every_sidecar_is_legal(tmp_path):
    """Two budgets, two failure modes: many small sidecars still add up."""
    col = _collection(tmp_path, slugs=("s1", "s2", "s3"))
    for slug in ("s1", "s2", "s3"):
        (col / "skills" / slug / "skill_kb.json").write_bytes(b"x" * 1000)

    generous = _layout(col, collection_max_bytes=10_000)
    assert generous.status == release_gate.PASS

    tight = _layout(col, collection_max_bytes=2_500)
    assert tight.status == release_gate.FAIL
    total = [d for d in tight.details if "collection budget" in d["message"]]
    assert total and total[0]["bytes"] == 3000
    assert not [d for d in tight.details if "per-skill budget" in d["message"]], (
        "no single sidecar is over its own budget; only the collection total is"
    )


def test_a_collection_without_an_index_is_not_applicable_rather_than_failing(tmp_path):
    """Three of the four shipped collections have no index; absence is not drift."""
    res = _layout(_collection(tmp_path))
    assert res.status == release_gate.PASS
    assert "not applicable" in _messages(res)


def test_an_unreadable_index_fails_rather_than_passing_quietly(tmp_path):
    col = _collection(tmp_path, slugs=("alpha",), leaf_dirname="leaves")
    (col / "skills_index.json").write_text("{not json")
    res = _layout(col)
    assert res.status == release_gate.FAIL
    assert "unreadable" in _messages(res)


def test_infrastructure_and_workflow_dirs_are_not_leaf_bundles(tmp_path):
    """`_router` and `workflows/` are composites; the leaf file-set rule is not theirs."""
    col = _collection(tmp_path, slugs=("s1",), leaf_dirname="leaves")
    for rel in ("skills/_router", "workflows/a-super-skill"):
        d = col / rel
        d.mkdir(parents=True)
        (d / "SKILL.md").write_text("---\nname: x\n---\n")
        (d / "workflow.yaml").write_text("steps: []\n")
    assert _layout(col).status == release_gate.PASS


# --------------------------------------------------------------------------- #
# The gate is wired in, and the shipped collections still pass it.             #
# --------------------------------------------------------------------------- #
def test_the_check_runs_as_part_of_the_gate(tmp_path):
    col = _collection(tmp_path)
    report = release_gate.run_gate(col, None, strict=True)
    names = [c["name"] for c in report["checks"]]
    assert "layout_packaging" in names
    entry = next(c for c in report["checks"] if c["name"] == "layout_packaging")
    assert entry["gates"] == [10] and entry["hard_gate"] is True
    assert 10 in report["hard_gate_ids"]
    assert report["policy"]["kb_sidecar_max_bytes"] == release_gate._KB_SIDECAR_MAX_BYTES
    assert report["policy"]["allowed_skill_files"] == ["SKILL.md", "skill_kb.json"]


def test_a_layout_failure_blocks_a_strict_promotion(tmp_path):
    """The gate's promote/block decision is main()'s exit code."""
    col = _collection(tmp_path)
    assert release_gate.main([str(col), "--strict", "--report", str(tmp_path / "r1.json")]) == 0

    (col / "skills" / "s1" / "tools.json").write_text("[]")
    assert release_gate.main([str(col), "--strict", "--report", str(tmp_path / "r2.json")]) == 1

    report = json.loads((tmp_path / "r2.json").read_text())
    failed = [c["name"] for c in report["checks"] if c["status"] == release_gate.FAIL]
    assert failed == ["layout_packaging"], f"the layout check must be what blocks, got {failed}"


def test_a_layout_failure_is_advisory_without_strict(tmp_path):
    col = _collection(tmp_path)
    (col / "skills" / "s1" / "tools.json").write_text("[]")
    assert release_gate.main([str(col), "--report", str(tmp_path / "r.json")]) == 0


SHIPPED = sorted(p.parent for p in REPO_ROOT.glob("collections/*/v*/collection.yaml"))


@pytest.mark.parametrize("col", SHIPPED, ids=[f"{p.parent.name}-{p.name}" for p in SHIPPED])
def test_every_shipped_collection_already_satisfies_the_layout_gate(col):
    """Read-only over the real tree: a new gate that reddens the release is an outage.

    `test_scripts_are_path_invocable` drives `collections/epigenomics/v1` through
    `--strict` and requires exit 0, so this is not merely nice to have.
    """
    res = _layout(col)
    assert res.status == release_gate.PASS, _messages(res)


def test_the_shipped_set_is_not_empty():
    """A parametrized guard over an empty list passes for the wrong reason."""
    assert len(SHIPPED) >= 4


def test_the_check_is_not_vacuous_on_the_shipped_tree():
    """It really walked those skills rather than finding nothing to walk."""
    counts = [int(_layout(c).summary.split("(")[-1].split()[0]) for c in SHIPPED]
    assert all(n > 0 for n in counts), counts
    assert sum(counts) > 1000


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
