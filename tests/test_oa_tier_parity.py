"""The two open-access gates must admit the same tiers.

`scripts/release_gate.py` is the release authority; `.github/workflows/verify-paper.yml`
gates pushes and PRs. When they disagree, one of them silently rejects (or admits) a
whole tier -- which is how every `repo-oa` paper came to fail CI on main while the
release gate passed them.
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


def _workflow_open_access_types() -> set[str]:
    """Evaluate the workflow's OPEN_ACCESS_TYPES without executing the whole gate."""
    namespace: dict[str, object] = {}
    for node in ast.parse(_inline_gate_source()).body:
        if isinstance(node, (ast.Assign, ast.AugAssign)):
            target = node.targets[0] if isinstance(node, ast.Assign) else node.target
            if isinstance(target, ast.Name) and target.id in {
                "OPEN_ACCESS_TYPES",
                "REPO_OA_TYPES",
            }:
                exec(compile(ast.Module([node], []), "<workflow>", "exec"), namespace)
    return set(namespace["OPEN_ACCESS_TYPES"])


def test_workflow_admits_every_repo_oa_tier():
    assert release_gate._REPO_OA_TIERS <= _workflow_open_access_types()


def test_workflow_admits_every_release_gate_tier():
    normalized = {
        release_gate._normalize_access_type(t) for t in _workflow_open_access_types()
    }
    assert release_gate._NORMALIZED_OA_TIERS <= normalized


if __name__ == "__main__":
    test_workflow_admits_every_repo_oa_tier()
    test_workflow_admits_every_release_gate_tier()
    print(f"PASS: gates agree on {len(_workflow_open_access_types())} access tiers")
