"""Description discipline for published skills, runnable outside CI.

A skill's description is the only thing a host loads before deciding whether to
read the skill, so it carries a real budget: it must say when to use the skill,
in a bounded number of characters, without marketing.

This lived as an inline heredoc in `validate.yml` and so could only be run by
pushing. A description that broke it therefore failed the build rather than the
author's own test run -- which is how `asb-contribute` shipped 69 characters over
the limit. The rules are unchanged; only their reachability is.

    python scripts/lint_skill_descriptions.py
    python scripts/lint_skill_descriptions.py collections staged-collections
"""
from __future__ import annotations

# Invoked by path (`python scripts/x.py`), only `scripts/` lands on sys.path, so
# the repo root has to be added before the sibling package can be imported.
if __package__ in (None, ""):
    import os.path as _p
    import sys as _sys

    _sys.path.insert(0, _p.dirname(_p.dirname(_p.abspath(__file__))))

import argparse
import pathlib
import sys

import yaml

from asb_skill_collections import layout

# A description answers "when would I reach for this?", so it opens by saying so.
APPROVED_PREFIXES = ("Use when", "Reference for", "Explains", "Decision support for")
MIN_LEN = 50
MAX_LEN = 300
MARKETING_TERMS = ("best", "state-of-the-art", "revolutionary", "leading", "superior")

DEFAULT_ROOTS = ("collections", "staged-collections")


def is_leaf(path: pathlib.Path) -> bool:
    """Whether this SKILL.md is a leaf, and so subject to the leaf lint.

    Workflow super-skills compose leaves and legitimately carry longer,
    composite descriptions; `_`-prefixed scaffolds such as `_router` are
    infrastructure. `release_gate.py` is the release authority and exempts both,
    so this must agree with it -- `tests/test_ci_gate_consistency.py` pins that.
    """
    return (layout.WORKFLOW_DIRNAME not in path.parts
            and not any(part.startswith("_") for part in path.parts[:-1]))


def check_description(description: str) -> list[str]:
    """Every rule this description breaks. Empty list means it passes."""
    description = (description or "").strip()
    if not description:
        return ["missing description"]
    problems = []
    if not description.startswith(APPROVED_PREFIXES):
        problems.append(f"description must start with one of {APPROVED_PREFIXES}")
    if len(description) < MIN_LEN:
        problems.append(f"description too short ({len(description)} < {MIN_LEN})")
    if len(description) > MAX_LEN:
        problems.append(f"description too long ({len(description)} > {MAX_LEN})")
    problems += [f"marketing term {term!r} in description"
                 for term in MARKETING_TERMS if term in description.lower()]
    return problems


def skill_files(roots=DEFAULT_ROOTS) -> list[pathlib.Path]:
    """Every leaf SKILL.md under the given roots, in stable order."""
    found: list[pathlib.Path] = []
    for root in roots:
        found += sorted(pathlib.Path(root).rglob("SKILL.md"))
    return [p for p in found if is_leaf(p)]


def lint(roots=DEFAULT_ROOTS) -> list[str]:
    """Return one message per violation, prefixed by the file it came from.

    A file with no frontmatter fence is skipped rather than reported: this lint
    owns descriptions, and the missing-frontmatter case belongs to the gate that
    owns structure.
    """
    failures: list[str] = []
    for path in skill_files(roots):
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---"):
            continue
        try:
            frontmatter = yaml.safe_load(text.split("---", 2)[1]) or {}
        except yaml.YAMLError:
            continue
        failures += [f"{path}: {problem}"
                     for problem in check_description(frontmatter.get("description"))]
    return failures


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("roots", nargs="*", default=list(DEFAULT_ROOTS))
    args = parser.parse_args(argv)
    roots = [r for r in (args.roots or DEFAULT_ROOTS) if pathlib.Path(r).is_dir()]

    failures = lint(roots)
    if failures:
        print("FAIL: description discipline violations:")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"PASS: description discipline OK ({len(skill_files(roots))} skill files checked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
