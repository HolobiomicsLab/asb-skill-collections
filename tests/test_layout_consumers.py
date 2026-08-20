"""Every consumer of the corpus must resolve its location, not hardcode one.

The corpus moved from ``skills/`` to ``leaves/`` when the collection became
router-shaped. A consumer that names one of those directories literally keeps
working — it just silently returns a fraction of the corpus, which is
indistinguishable from a clean pass. That failure has now happened three
times: the docs-site indexer dropped 5,859 of 7,714 skills, the curation
auditor graded 2 leaves out of 5,859 and reported healthy, and the shipped
retrieval library could not fetch a single leaf.

Two guards, because either alone has a hole. The behavioural one runs the real
consumers against both layouts and cannot be fooled by how a path is spelled.
The textual one catches a consumer nobody remembered to add to the first.
"""

from __future__ import annotations

import importlib.util
import json
import pathlib
import re
import sys

import pytest

from asb_skill_collections import asb_skill_index, layout

REPO = pathlib.Path(__file__).resolve().parent.parent
V2 = REPO / "collections" / "metabolomics" / "v2"
sys.path.insert(0, str(REPO / "scripts"))  # curate imports its siblings bare

import check_license_tiers  # noqa: E402
import curate  # noqa: E402


# --------------------------------------------------------------------------- #
# behavioural: the real consumers, both layouts                                #
# --------------------------------------------------------------------------- #
def _collection(root: pathlib.Path, leaf_dirname: str) -> pathlib.Path:
    """A minimal collection holding one leaf, in the layout named."""
    root.mkdir(parents=True, exist_ok=True)
    leaf = root / leaf_dirname / "alpha"
    leaf.mkdir(parents=True)
    (leaf / "SKILL.md").write_text(
        "---\nname: alpha\nlicense: CC-BY-4.0\n---\nbody\n", encoding="utf-8"
    )
    router = root / layout.ADVERTISED_DIRNAME / "_router"
    router.mkdir(parents=True, exist_ok=True)
    (router / "SKILL.md").write_text("---\nname: r\n---\n", encoding="utf-8")
    (root / "corpus.yaml").write_text("papers: []\n", encoding="utf-8")
    (root / "skills_index.json").write_text(
        json.dumps([{"slug": "alpha", "license_tier": "open"}]), encoding="utf-8"
    )
    return root


def _slugs_from_curate(col: pathlib.Path) -> set[str]:
    return {slug for slug, _, _ in curate.iter_leaf_frontmatter(str(col))}


def _slugs_from_retrieval(col: pathlib.Path) -> set[str]:
    path = asb_skill_index.item_source_path(col, "skills", "alpha")
    return {path.parent.name} if path.is_file() else set()


def _slugs_from_licence_gate(col: pathlib.Path) -> set[str]:
    # The fixture leaf declares no metadata.license_tier, so a sweep that
    # reaches it complains by name; a sweep that misses it says nothing.
    return {v.split("/alpha/")[0] and "alpha"
            for v in check_license_tiers.check_collection(col) if "/alpha/" in v}


CONSUMERS = {
    "layout.slugs": layout.slugs,
    "curate.iter_leaf_frontmatter": _slugs_from_curate,
    "asb_skill_index.item_source_path": _slugs_from_retrieval,
    "check_license_tiers.check_collection": _slugs_from_licence_gate,
}


@pytest.mark.parametrize("leaf_dirname", [layout.LEAF_DIRNAME, layout.ADVERTISED_DIRNAME])
@pytest.mark.parametrize("name", sorted(CONSUMERS))
def test_every_consumer_sees_the_corpus_in_either_layout(name, leaf_dirname, tmp_path):
    """A consumer blind to one layout returns a clean, empty, wrong answer."""
    col = _collection(tmp_path / leaf_dirname, leaf_dirname)
    assert "alpha" in CONSUMERS[name](col), (
        f"{name} sees no corpus when the leaves live in {leaf_dirname}/ — it "
        "resolves the directory itself instead of asking the layout resolver"
    )


# --------------------------------------------------------------------------- #
# textual: a net for consumers not listed above                                #
# --------------------------------------------------------------------------- #
# Three spellings of the same mistake. The first two build the path from
# separate segments, which is how both shipped bugs evaded the original guard.
LAYOUT_LITERAL = {
    name: [
        re.compile(rf"""join\([^)]*["']{name}["']"""),          # os.path.join(d, "skills", …)
        re.compile(rf"""/\s*["']{name}["']\s*/"""),             # d / "skills" / slug
        re.compile(rf"""["'][^"']*{name}/[^"']*\*[^"']*SKILL\.md["']"""),
        # f"{collection}/skills" — the shape that let stamp_skill_license.py
        # sweep an empty directory and report a clean run. Anchored on the
        # interpolation so a fixed path like "~/.claude/skills", which is a
        # runtime install target rather than a corpus, is not swept up.
        re.compile(rf"""\{{[^}}]*\}}/{name}["']"""),
    ]
    for name in (layout.ADVERTISED_DIRNAME, layout.LEAF_DIRNAME)
}
# The resolver is allowed to name the directories; nothing else is.
EXEMPT = {"asb_skill_collections/layout.py"}


def _tracked_python() -> list[pathlib.Path]:
    """Production modules only — tests build fixtures in both layouts."""
    return [
        p for p in sorted(REPO.rglob("*.py"))
        if not {".venv", "node_modules", ".git", "tests"} & set(p.parts)
    ]


def _names_layout(text: str, name: str) -> re.Match | None:
    for pattern in LAYOUT_LITERAL[name]:
        hit = pattern.search(text)
        if hit:
            return hit
    return None


@pytest.mark.parametrize("path", _tracked_python(), ids=lambda p: p.name)
def test_no_module_builds_a_corpus_path_from_a_layout_literal(path):
    """A production module must not name one layout directory on its own.

    Tests are exempt: they build fixtures in both layouts deliberately, and the
    behavioural check above is what actually covers them. A module naming
    *both* directories is layout-aware, just not via the resolver.
    """
    rel = path.relative_to(REPO).as_posix()
    if rel in EXEMPT:
        pytest.skip("the canonical resolver may name the directories")
    text = path.read_text(encoding="utf-8", errors="replace")
    hits = {name: _names_layout(text, name) for name in LAYOUT_LITERAL}
    for name, hit in hits.items():
        other = next(n for n in LAYOUT_LITERAL if n != name)
        assert not (hit and not hits[other]), (
            f"{rel} builds a corpus path from the literal {name!r} "
            f"({hit.group()!r}); a {other}-shaped collection then yields "
            "nothing. Resolve it through asb_skill_collections.layout."
        )


# --------------------------------------------------------------------------- #
# corpus-level: the published artifacts                                        #
# --------------------------------------------------------------------------- #
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


def test_every_published_skill_is_retrievable():
    """Search finds a slug; fetch must then return that slug's file."""
    rows = json.loads((V2 / "skills_index.json").read_text())
    missing = [r["slug"] for r in rows
               if not asb_skill_index.item_source_path(V2, "skills", r["slug"]).is_file()]
    assert not missing, (
        f"{len(missing)} of {len(rows)} published skills cannot be fetched, "
        f"e.g. {missing[:3]}"
    )


def test_workflows_are_not_treated_as_paper_derived_leaves(tmp_path):
    """A composite has no single source paper; the leaf gates must skip it.

    The skip only bites on the root-fallback path — a ``workflows/`` sibling of
    a populated ``leaves/`` is never walked, so a fixture shaped that way
    asserts nothing.
    """
    collection = tmp_path / "v1"
    (collection / "workflows" / "pipeline").mkdir(parents=True)
    (collection / "workflows" / "pipeline" / "SKILL.md").write_text("---\nname: p\n---\n")
    (collection / "solo").mkdir()
    (collection / "solo" / "SKILL.md").write_text("---\nname: solo\n---\n")
    assert layout.slugs(collection) == {"solo"}


def test_the_release_gate_still_checks_every_shipped_workflow():
    """check_workflows must see the workflows the collection actually ships."""
    from scripts.release_gate import check_workflows
    shipped = {d.name for d in (V2 / "workflows").iterdir()
               if d.is_dir() and not d.name.startswith("_") and d.name != "bin"}
    result = check_workflows(V2)
    assert f"({len(shipped)} workflows checked)" in result.summary, result.summary
