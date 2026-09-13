"""A gate that cannot be triggered is not a gate (INT-ASB-038 sweep, finding 8).

``governance/COMMUNITY_SKILLS.md`` §2 stages a community skill at
``collections/<slug>/v<N>/proposals/skills/<skill-slug>/SKILL.md``, and
``scripts/check_proposals.py`` reads exactly ``<collection_dir>/proposals/skills``.
The workflow that runs that driver was triggered on ``collections/*/proposals/**``
— and a ``*`` in a GitHub path filter does not cross a ``/``, so the pattern
matched only the legacy unversioned directory. The four proposals actually staged
in this repo live under ``collections/metabolomics/v2/proposals/skills/``, so the
job never ran on a real proposal PR: a contributor got a silent green.

Nothing was red, which is why this needs a test rather than a fix alone. The
check below is deliberately written against the *shipped* proposal paths rather
than against a hard-coded string, so a future collection staged at a new version
directory keeps the trigger honest.
"""

import fnmatch
import pathlib

import pytest
import yaml

REPO_ROOT = pathlib.Path(__file__).parent.parent
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "proposals.yml"
DRIVER = "scripts/check_proposals.py"


def _triggers():
    # `on:` is YAML 1.1 `true`; both spellings are accepted so the test does not
    # depend on which loader the environment brings.
    doc = yaml.safe_load(WORKFLOW.read_text())
    section = doc.get("on", doc.get(True))
    return list(section["pull_request"]["paths"])


def _glob(pattern: str, path: str) -> bool:
    """Match one GitHub path filter: `*` stops at a separator, `**` crosses them.

    `fnmatch` alone cannot express this — its `*` matches separators too, which
    is exactly the distinction the broken trigger turned on, so borrowing it
    wholesale would make this test agree with the bug.
    """

    def walk(pats, parts):
        if not pats:
            return not parts
        head, rest = pats[0], pats[1:]
        if head == "**":
            return any(walk(rest, parts[i:]) for i in range(len(parts) + 1))
        return bool(parts) and fnmatch.fnmatchcase(parts[0], head) and walk(rest, parts[1:])

    return walk(pattern.split("/"), path.split("/"))


def _matches(path: str) -> bool:
    return any(_glob(pattern, path) for pattern in _triggers())


SHIPPED_PROPOSALS = sorted(
    str(p.relative_to(REPO_ROOT))
    for p in REPO_ROOT.glob("collections/*/*/proposals/skills/*/SKILL.md")
)


def test_the_repo_still_stages_proposals_where_the_policy_says():
    """An empty parametrisation below would pass for the wrong reason."""
    assert SHIPPED_PROPOSALS, (
        "no proposal found at collections/<slug>/v<N>/proposals/skills/*/SKILL.md"
    )


@pytest.mark.parametrize("path", SHIPPED_PROPOSALS)
def test_every_staged_proposal_triggers_the_gate(path):
    assert _matches(path), (
        f"{path} would not trigger .github/workflows/proposals.yml "
        f"(paths: {_triggers()})"
    )


def test_the_glob_semantics_this_test_relies_on():
    """Two-sided: the matcher must actually refuse a single-`*` crossing.

    Without this, a matcher that treated `*` as `**` would call the old broken
    trigger correct and the test above would pass against the very bug it pins.
    """
    staged = "collections/metabolomics/v2/proposals/skills/x/SKILL.md"
    assert not _glob("collections/*/proposals/**", staged), "the old trigger"
    assert _glob("collections/*/v*/proposals/**", staged), "the corrected trigger"
    assert _glob("collections/*/proposals/**", "collections/metabolomics/proposals/a.yaml")
    assert not _glob("collections/*/v*/proposals/**", "collections/metabolomics/v2/corpus.yaml")


def test_editing_the_driver_reruns_the_gate():
    """The check must re-run when the rules it enforces change, not only the data."""
    assert _matches(DRIVER), f"{DRIVER} does not re-trigger its own workflow"


def test_the_workflow_checks_the_collection_whose_proposals_it_watches():
    """The trigger and the invocation must name the same tree.

    They were allowed to disagree once already: the body has always run
    `collections/metabolomics/v2` while the trigger could only fire on
    `collections/metabolomics`.
    """
    body = WORKFLOW.read_text()
    # collections/<slug>/v<N>/proposals/skills/<slug>/SKILL.md -> the collection dir
    collections = sorted({str(pathlib.Path(p).parents[3]) for p in SHIPPED_PROPOSALS})
    checked = [c for c in collections if f"check_proposals {c}" in body]
    assert checked, (
        "the workflow body invokes check_proposals on no collection that holds "
        f"staged proposals; staged: {collections}"
    )


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
