"""The PR-time description lint and the release gate must agree on what they lint.

`release_gate.py::_iter_skill_md` (the release authority) exempts workflow super-skills
and `_`-prefixed scaffolds from leaf-level checks — they are composites, gated separately
by `check_workflows`. The `validate.yml` Gate 5 description lint must exempt the same set,
or a merge of legitimate super-skills (whose descriptions are longer by design) turns CI
red on a contract the release gate never enforced. This regression was found by the
forge-merge adversarial verification (18 workflow descriptions > 300 chars, 0 leaves).
"""
import pathlib
import re
import sys

REPO_ROOT = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT))
from scripts import release_gate  # noqa: E402

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


def test_validate_gate5_exempts_workflows_and_underscore():
    """The Gate 5 lint step must define AND apply the workflows/_ exemption."""
    # Extract the description-lint step: from its name to the next step's `- name:`.
    text = VALIDATE.read_text()
    start = text.index("Lint skill descriptions")
    nxt = text.find("\n      - name:", start)
    step = text[start:] if nxt == -1 else text[start:nxt]
    assert "_is_leaf" in step and "workflows" in step, (
        "validate.yml Gate 5 must define a workflows/_ exemption (consistent with "
        "release_gate._iter_skill_md) — see test_ci_gate_consistency"
    )
    # the filter must actually be applied to the file list, not just defined
    assert re.search(r"skill_files\s*=\s*\[p for p in skill_files if _is_leaf\(p\)\]", step), (
        "the _is_leaf filter is defined but not applied to skill_files"
    )


def test_the_two_exemptions_describe_the_same_set(tmp_path):
    """Behaviourally: the predicate validate.yml uses and release_gate's skip agree."""
    def _is_leaf(p):  # mirror of the validate.yml Gate 5 predicate
        return "workflows" not in p.parts and not any(s.startswith("_") for s in p.parts[:-1])

    col = tmp_path / "collections" / "metabolomics" / "v2"
    paths = []
    for rel in ("skills/leaf-a", "skills/leaf-b", "skills/_router", "workflows/super-x"):
        d = col / rel
        d.mkdir(parents=True)
        f = d / "SKILL.md"
        f.write_text("---\nname: x\n---\n")
        paths.append(f)
    rg = {p.parent.name for p in release_gate._iter_skill_md(col)}
    vy = {p.parent.name for p in paths if _is_leaf(p)}
    assert rg == vy == {"leaf-a", "leaf-b"}, f"gates disagree: release_gate={rg} validate={vy}"


if __name__ == "__main__":
    import pytest

    raise SystemExit(pytest.main([__file__, "-q"]))
