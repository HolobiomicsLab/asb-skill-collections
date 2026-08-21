"""The description lint must be runnable before pushing, and agree with CI.

It lived as an inline heredoc in `validate.yml`, so the only way to run it was
to push. `asb-contribute` shipped 69 characters over the limit and the build
caught what the author's own test run could not — the rule was fine, its
reachability was not.

These tests pin the rules themselves and, in both directions, which files the
lint claims authority over.
"""

from __future__ import annotations

import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from scripts import lint_skill_descriptions as lint  # noqa: E402

GOOD = "Use when aligning retention times across batches acquired on one instrument."


def _skill(tmp_path, rel, description):
    path = tmp_path / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f'---\nname: x\ndescription: "{description}"\n---\nbody\n', encoding="utf-8")
    return path


# --------------------------------------------------------------------------- #
# The rules                                                                    #
# --------------------------------------------------------------------------- #

def test_a_well_formed_description_passes():
    assert lint.check_description(GOOD) == []


@pytest.mark.parametrize("prefix", lint.APPROVED_PREFIXES)
def test_every_approved_prefix_is_accepted(prefix):
    assert lint.check_description(f"{prefix} " + "x" * lint.MIN_LEN) == []


def test_a_description_that_does_not_say_when_is_rejected():
    problems = lint.check_description("This skill does retention time alignment across batches.")
    assert any("must start with" in p for p in problems)


def test_a_description_over_the_limit_is_rejected():
    """The exact rule `asb-contribute` broke."""
    problems = lint.check_description("Use when " + "x" * lint.MAX_LEN)
    assert any("too long" in p for p in problems)


def test_a_description_under_the_limit_is_rejected():
    problems = lint.check_description("Use when x")
    assert any("too short" in p for p in problems)


@pytest.mark.parametrize("term", lint.MARKETING_TERMS)
def test_a_marketing_term_is_rejected_in_any_case(term):
    problems = lint.check_description(f"Use when you want the {term.upper()} way to align batches.")
    assert any("marketing term" in p for p in problems)


def test_an_empty_description_is_one_clear_failure_not_four():
    assert lint.check_description("   ") == ["missing description"]


# --------------------------------------------------------------------------- #
# Which files it governs — both directions                                     #
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize("rel", [
    "collections/m/v2/leaves/a-skill/SKILL.md",
    "collections/m/v2/skills/a-skill/SKILL.md",
])
def test_a_leaf_is_linted_in_either_layout(tmp_path, rel):
    _skill(tmp_path, rel, "Use when x")
    assert lint.lint([str(tmp_path / "collections")]), "a bad leaf must be reported"


@pytest.mark.parametrize("rel", [
    "collections/m/v2/workflows/a-workflow/SKILL.md",
    "collections/m/v2/skills/_router/SKILL.md",
])
def test_a_composite_or_scaffold_is_exempt(tmp_path, rel):
    """The other side. `release_gate` is the release authority and exempts both;
    a lint stricter than the gate would block a build the gate would pass."""
    _skill(tmp_path, rel, "Use when x")
    assert lint.lint([str(tmp_path / "collections")]) == []


def test_a_file_with_no_frontmatter_is_skipped_not_reported(tmp_path):
    """Structure belongs to the gate that owns structure, not to this lint."""
    path = tmp_path / "collections/m/v2/leaves/raw/SKILL.md"
    path.parent.mkdir(parents=True)
    path.write_text("# no fence here\n", encoding="utf-8")
    assert lint.lint([str(tmp_path / "collections")]) == []


def test_a_missing_root_does_not_crash_the_run(tmp_path):
    assert lint.lint([str(tmp_path / "nope")]) == []


# --------------------------------------------------------------------------- #
# The published corpus                                                         #
# --------------------------------------------------------------------------- #

def test_every_published_description_passes_the_lint():
    """What CI enforces, enforced here too — so it fails before the push."""
    roots = [r for r in lint.DEFAULT_ROOTS
             if (pathlib.Path(__file__).parent.parent / r).is_dir()]
    failures = lint.lint([str(pathlib.Path(__file__).parent.parent / r) for r in roots])
    assert not failures, failures[:10]


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
