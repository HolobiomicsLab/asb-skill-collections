"""The PR-time description lint and the release gate must agree on what they lint.

`release_gate.py::_iter_skill_md` (the release authority) exempts workflow super-skills
and `_`-prefixed scaffolds from leaf-level checks — they are composites, gated separately
by `check_workflows`. The PR-time description lint must exempt the same set, or a merge of
legitimate super-skills (whose descriptions are longer by design) turns CI red on a
contract the release gate never enforced. This regression was found by the forge-merge
adversarial verification (18 workflow descriptions > 300 chars, 0 leaves).

The lint used to be a heredoc in `validate.yml`, so agreement could only be checked by
grepping the YAML for the predicate's source. Both sides are importable modules now, so
the check runs them against the same tree instead — a textual match could pass while the
two behaviours drifted apart.
"""
import pathlib
import re
import sys

REPO_ROOT = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT))
from scripts import lint_skill_descriptions, release_gate  # noqa: E402

VALIDATE = REPO_ROOT / ".github" / "workflows" / "validate.yml"


def test_release_gate_skips_workflows_and_underscore(tmp_path):
    """release_gate._iter_skill_md must yield leaves only, not workflows/_ scaffolds."""
    col = tmp_path / "collections" / "metabolomics" / "v2"
    for rel in ("skills/real-leaf", "skills/_router", "workflows/a-super-skill"):
        d = col / rel
        d.mkdir(parents=True)
        (d / "SKILL.md").write_text("---\nname: x\n---\n# x\n")
    yielded = {p.parent.name for p in release_gate._iter_skill_md(col)}
    assert yielded == {"real-leaf"}, f"expected only the leaf, got {yielded}"


def test_validate_runs_the_lint_module_rather_than_an_inline_copy():
    """A second copy of the rules in YAML is a second thing to keep in sync, and
    the copy in CI is the one nobody can run before pushing."""
    text = VALIDATE.read_text()
    start = text.index("Lint skill descriptions")
    nxt = text.find("\n      - name:", start)
    step = text[start:] if nxt == -1 else text[start:nxt]
    assert "scripts.lint_skill_descriptions" in step, (
        "validate.yml must call the lint module, not reimplement it inline"
    )
    assert "MAX_LEN" not in step and "_is_leaf" not in step, (
        "the rules must live in the module only — this step is reimplementing them"
    )


def test_the_two_gates_lint_exactly_the_same_files(tmp_path):
    """Run both over one tree. No mirrored predicate, no textual proxy.

    A leaf the lint checks but the gate exempts turns CI red on a contract the
    release never enforced; a leaf the gate checks but the lint skips ships
    unlinted. Both directions matter, so this is set equality.
    """
    col = tmp_path / "collections" / "metabolomics" / "v2"
    for rel in ("leaves/leaf-a", "skills/leaf-b", "skills/_router", "workflows/super-x"):
        d = col / rel
        d.mkdir(parents=True)
        (d / "SKILL.md").write_text("---\nname: x\n---\n")
    from_gate = {p.parent.name for p in release_gate._iter_skill_md(col)}
    from_lint = {p.parent.name for p in lint_skill_descriptions.skill_files([str(col)])}
    assert from_gate == from_lint == {"leaf-a", "leaf-b"}, (
        f"gates disagree: release_gate={from_gate} lint={from_lint}")


if __name__ == "__main__":
    import pytest

    raise SystemExit(pytest.main([__file__, "-q"]))
