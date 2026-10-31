"""Every script a doc tells a reader to run must exist.

The call for curators told contributors to run ``scripts/expert_review_form.py``,
a file that was never written: the first command a new reviewer typed failed.
This guard reads every Markdown file under ``docs/`` and checks that each
``scripts/<name>.py`` path, and each ``python -m scripts.<name>`` module, names
a tracked file.

A document whose header declares it a design draft (``**Status:** design
draft``) describes scripts it proposes, so it is not held to this check.
"""

from __future__ import annotations

import pathlib
import re

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
DOCS = REPO / "docs"

SCRIPT_PATH = re.compile(r"(?<![\w/.-])scripts/[A-Za-z0-9_/.-]+?\.py\b")
SCRIPT_MODULE = re.compile(r"python3? -m scripts\.([A-Za-z0-9_.]+)")
DESIGN_DRAFT = re.compile(r"^\*\*Status:\*\*\s*design draft", re.IGNORECASE | re.MULTILINE)


def is_design_draft(text: str) -> bool:
    head = "\n".join(text.splitlines()[:15])
    return bool(DESIGN_DRAFT.search(head))


def script_refs(text: str) -> set[str]:
    refs = set(SCRIPT_PATH.findall(text))
    refs.update("scripts/" + m.replace(".", "/") + ".py" for m in SCRIPT_MODULE.findall(text))
    return refs


@pytest.mark.parametrize(
    "text, expected",
    [
        ("run `python scripts/release_gate.py --strict`", {"scripts/release_gate.py"}),
        ("python -m scripts.build_packs --check", {"scripts/build_packs.py"}),
        ("copy to `collections/x/v1/scripts/helper.py`", set()),
    ],
)
def test_script_refs(text, expected):
    assert script_refs(text) == expected


def test_design_draft_header_is_recognised():
    assert is_design_draft("# Design: x\n\n**Status:** design draft (v1.1+).\n")
    assert not is_design_draft("# Call\n\n**Status:** open.\n")


def test_every_script_named_in_docs_exists():
    pages = sorted(DOCS.rglob("*.md"))
    assert pages, "no Markdown under docs/"
    missing = []
    for page in pages:
        text = page.read_text(encoding="utf-8")
        if is_design_draft(text):
            continue
        for ref in sorted(script_refs(text)):
            if not (REPO / ref).is_file():
                missing.append(f"{page.relative_to(REPO)}: {ref}")
    assert not missing, "docs name scripts that do not exist:\n  " + "\n  ".join(missing)
