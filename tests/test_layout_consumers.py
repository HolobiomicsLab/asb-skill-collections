"""Every consumer of the corpus must resolve its location, not hardcode one.

The corpus moved from ``skills/`` to ``leaves/`` when the collection became
router-shaped. Any consumer that globs one of those names literally keeps
working — it just silently returns a fraction of the corpus. That is the
failure this module guards: the docs-site search index dropped 5,859 of 7,714
skills that way, and nothing went red.
"""

from __future__ import annotations

import importlib.util
import json
import pathlib
import re

import pytest

from scripts import layout

REPO = pathlib.Path(__file__).resolve().parent.parent
V2 = REPO / "collections" / "metabolomics" / "v2"

# The anti-pattern is *enumerating* a corpus out of one hardcoded layout
# directory: a wildcard in the slug position under `skills/` or `leaves/`.
# Naming one fixed advertised file (`skills/_router/SKILL.md`) is fine — that
# path is the layout, not a guess about it. Naming both directories is fine
# too: such a consumer is layout-aware, just not via the resolver.
CORPUS_GLOB = {
    "skills": re.compile(r"""["'][^"']*skills/[^"']*\*[^"']*SKILL\.md["']"""),
    "leaves": re.compile(r"""["'][^"']*leaves/[^"']*\*[^"']*SKILL\.md["']"""),
}
EXEMPT = {"scripts/layout.py", "tests/test_layout_consumers.py"}


def _tracked_python() -> list[pathlib.Path]:
    return [
        p for p in sorted(REPO.rglob("*.py"))
        if ".venv" not in p.parts and "node_modules" not in p.parts
        and ".git" not in p.parts
    ]


@pytest.mark.parametrize("path", _tracked_python(), ids=lambda p: p.name)
def test_no_module_globs_a_layout_directory_literally(path):
    rel = path.relative_to(REPO).as_posix()
    if rel in EXEMPT:
        pytest.skip("the canonical resolver is allowed to name the directories")
    text = path.read_text(encoding="utf-8", errors="replace")
    seen = {name: pattern.search(text) for name, pattern in CORPUS_GLOB.items()}
    for name, hit in seen.items():
        other = "leaves" if name == "skills" else "skills"
        assert not (hit and not seen[other]), (
            f"{rel} enumerates the corpus out of {name}/ only ({hit.group()}); "
            f"a {other}-shaped collection silently yields nothing. Use "
            "scripts.layout, or cover both directories."
        )


def _build_search_index():
    spec = importlib.util.spec_from_file_location(
        "build_search_index", REPO / "docs-site" / "build_search_index.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_docs_site_indexer_covers_the_whole_published_corpus():
    """Everything a collection publishes must reach the public search index."""
    found = {p.parent.name for p in _build_search_index()._iter_skill_files()}
    indexed = {e["slug"] for e in json.loads((V2 / "skills_index.json").read_text())}
    missing = indexed - found
    assert not missing, (
        f"{len(missing)} published skills are invisible to the docs site, "
        f"e.g. {sorted(missing)[:3]}"
    )


def test_workflows_are_not_treated_as_paper_derived_leaves(tmp_path):
    """A composite has no single source paper; the leaf gates must skip it."""
    collection = tmp_path / "v1"
    (collection / "leaves" / "leaf").mkdir(parents=True)
    (collection / "leaves" / "leaf" / "SKILL.md").write_text("---\nname: leaf\n---\n")
    (collection / "workflows" / "pipeline").mkdir(parents=True)
    (collection / "workflows" / "pipeline" / "SKILL.md").write_text("---\nname: p\n---\n")
    assert layout.slugs(collection) == {"leaf"}


def test_the_release_gate_still_checks_every_shipped_workflow():
    """check_workflows must see the workflows the collection actually ships."""
    from scripts.release_gate import check_workflows
    shipped = {d.name for d in (V2 / "workflows").iterdir()
               if d.is_dir() and not d.name.startswith("_") and d.name != "bin"}
    result = check_workflows(V2)
    assert f"({len(shipped)} workflows checked)" in result.summary, result.summary
