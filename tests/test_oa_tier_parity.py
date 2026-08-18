"""The two open-access gates must admit exactly the same tiers.

`scripts/release_gate.py` is the release authority; `.github/workflows/verify-paper.yml`
gates pushes and PRs. When they disagree, one of them silently rejects (or admits) a
whole tier -- which is how every `repo-oa` paper came to fail CI on main while the
release gate passed them.

Both directions matter. Missing a tier the release gate admits turns CI red on valid
content; admitting a tier the release gate rejects lets non-open content reach the
public branch, and only fails later at release time.
"""

import ast
import pathlib
import re
import sys

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from scripts import release_gate

REPO_ROOT = pathlib.Path(__file__).parent.parent
VERIFY_PAPER_WORKFLOW = REPO_ROOT / ".github" / "workflows" / "verify-paper.yml"
TIER_NAMES = {"OPEN_ACCESS_TYPES", "REPO_OA_TYPES", "LINK_ONLY_TYPES"}


def _inline_gate_source() -> str:
    """Return the python heredoc embedded in the verify-paper access-tier step."""
    workflow = yaml.safe_load(VERIFY_PAPER_WORKFLOW.read_text())
    for job in workflow["jobs"].values():
        for step in job.get("steps", []):
            run = step.get("run") or ""
            if "OPEN_ACCESS_TYPES" in run:
                match = re.search(r"<<'([A-Z]+)'\n(.*?)\n\s*\1\s*$", run, re.S | re.M)
                if match:
                    return match.group(2)
    raise AssertionError("no verify-paper step defines OPEN_ACCESS_TYPES")


def _assignments_to(tree: ast.Module, name: str) -> list[ast.stmt]:
    """Every Assign/AugAssign binding `name`, at any nesting depth."""
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            targets = node.targets
        elif isinstance(node, ast.AugAssign):
            targets = [node.target]
        else:
            continue
        if any(isinstance(t, ast.Name) and t.id == name for t in targets):
            found.append(node)
    return found


def _workflow_open_access_types() -> set[str]:
    """Evaluate the workflow's OPEN_ACCESS_TYPES without executing the whole gate."""
    tree = ast.parse(_inline_gate_source())
    namespace: dict[str, object] = {}
    for node in tree.body:
        is_binding = isinstance(node, (ast.Assign, ast.AugAssign))
        if is_binding and _binds_a_tier_name(node):
            exec(compile(ast.Module([node], []), "<workflow>", "exec"), namespace)
    return set(namespace["OPEN_ACCESS_TYPES"])


def _binds_a_tier_name(node: ast.stmt) -> bool:
    targets = node.targets if isinstance(node, ast.Assign) else [node.target]
    return any(isinstance(t, ast.Name) and t.id in TIER_NAMES for t in targets)


def _normalized_workflow_tiers() -> set[str]:
    return {release_gate._normalize_access_type(t) for t in _workflow_open_access_types()}


def test_tier_sets_are_bound_only_at_module_level():
    """A nested rebind would diverge from what this test statically evaluates."""
    tree = ast.parse(_inline_gate_source())
    for name in TIER_NAMES:
        for node in _assignments_to(tree, name):
            assert node in tree.body, f"{name} rebound outside module level; parity test would go stale"


def test_workflow_admits_every_repo_oa_tier():
    assert release_gate._REPO_OA_TIERS <= _workflow_open_access_types()


def test_workflow_admits_every_link_only_tier():
    assert release_gate._LINK_ONLY_TIERS <= _workflow_open_access_types()


def test_workflow_admits_every_release_gate_tier():
    assert release_gate._NORMALIZED_OA_TIERS <= _normalized_workflow_tiers()


def test_workflow_admits_nothing_the_release_gate_rejects():
    assert _normalized_workflow_tiers() <= release_gate._NORMALIZED_OA_TIERS


if __name__ == "__main__":
    test_tier_sets_are_bound_only_at_module_level()
    test_workflow_admits_every_repo_oa_tier()
    test_workflow_admits_every_release_gate_tier()
    test_workflow_admits_nothing_the_release_gate_rejects()
    print(f"PASS: gates agree on {len(_workflow_open_access_types())} access tiers")
