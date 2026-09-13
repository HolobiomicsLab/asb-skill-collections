"""Keyword fallback, documented choices and regeneration are executable contracts."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

from asb_skill_collections import asb_skill_index as idx
from scripts import router_shape

ROOT = Path(__file__).resolve().parent.parent
COLLECTION = ROOT / "collections/metabolomics/v2"
LABELS = json.loads((ROOT / "tests/fixtures/selector_queries.json").read_text())


@pytest.fixture(autouse=True)
def default_selector(monkeypatch):
    """Default-rule checks must not inherit a user's compatibility override."""
    monkeypatch.delenv(idx.SELECTOR_ENV, raising=False)


@pytest.fixture
def semantic_module():
    """Load the actual collection wrapper without an embedding request."""
    path = COLLECTION / "bin/semantic_search.py"
    spec = importlib.util.spec_from_file_location("collection_semantic", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("inside_workflows", [False, True])
@pytest.mark.parametrize(
    ("target", "query"),
    [("skills", "untargeted annotation"), ("workflows", "MZmine2"), ("tools", "XCMS")],
)
def test_explicit_keyword_mode_uses_the_shared_results(
    semantic_module, target, query, inside_workflows, monkeypatch, capsys
):
    def forbidden_embedding(*args):
        pytest.fail("explicit keyword mode must not try an embedding backend")

    monkeypatch.setattr(semantic_module, "semantic_search", forbidden_embedding)
    start = COLLECTION / "workflows" if inside_workflows else COLLECTION
    semantic_module.main([
        "--collection", str(start), "--target", target, "--query", query,
        "--mode", "keyword", "--k", "3",
    ])
    actual = json.loads(capsys.readouterr().out)
    assert actual["mode"] == "keyword"
    expected = idx.search("metabolomics/v2", target, query, k=3, root=ROOT)
    assert expected
    assert actual["results"] == expected
    if target == "workflows":
        assert "mzmine2" in expected[0]["matched_fields"]["member_tools"]


@pytest.mark.parametrize("mode", ["auto", "semantic"])
def test_unavailable_semantic_result_has_an_explicit_keyword_fallback(
    semantic_module, mode, monkeypatch, capsys
):
    monkeypatch.setattr(semantic_module, "semantic_search", lambda *args: None)
    semantic_module.main([
        "--collection", str(COLLECTION), "--query", "untargeted annotation",
        "--target", "skills", "--mode", mode, "--k", "3",
    ])
    actual = json.loads(capsys.readouterr().out)
    expected = idx.search(
        "metabolomics/v2", "skills", "untargeted annotation", k=3, root=ROOT,
        fallback="keyword-after-semantic",
    )
    assert actual["mode"] == "keyword"
    assert actual["results"] == expected


def test_generator_refreshes_scripts_without_changing_unit_assets(tmp_path):
    unit = tmp_path / "installed-unit"
    unit.mkdir()
    index = unit / "skills_index.json"
    index.write_bytes(b"[]\n")
    leaf = unit / "leaves/untouched/SKILL.md"
    leaf.parent.mkdir(parents=True)
    leaf.write_bytes(b"a read-only test asset\n")
    before = {path: path.read_bytes() for path in (index, leaf)}

    assert router_shape.refresh_scripts(unit)["updated"] == [str(unit / "bin/search_skills.py")]
    assert router_shape.refresh_scripts(unit)["updated"] == []
    assert {path: path.read_bytes() for path in before} == before
    assert (unit / "bin/search_skills.py").read_bytes() == (
        COLLECTION / "bin/search_skills.py"
    ).read_bytes()


@pytest.mark.parametrize("label", LABELS, ids=lambda row: row["id"])
def test_measured_default_retains_documented_workflow_choices(label):
    source = label["source"]
    lines = (ROOT / source["path"]).read_text().splitlines()
    excerpt_lines = source["excerpt"].splitlines()
    # The recorded line is a hint: documentation above the excerpt may grow or
    # shrink on other branches, so the excerpt is located by content and the
    # label is only tied to the text it quotes.
    starts = [
        number for number, line in enumerate(lines, start=1)
        if line.startswith(excerpt_lines[0])
    ]
    assert starts, f"{source['path']} no longer contains: {excerpt_lines[0]!r}"
    start = source["line"] if source["line"] in starts else starts[0]
    for offset, excerpt in enumerate(excerpt_lines):
        assert lines[start - 1 + offset].startswith(excerpt)
    hits = idx.search(
        label["collection"], label["target"], label["query"],
        technique=label["technique"], k=3, root=ROOT,
    )
    assert hits[0]["slug"] in label["expected_slugs"]
    assert hits[0]["selector"]["rule"] == "package"


def test_collection_qualification_is_stable_for_colliding_slugs(tmp_path):
    for domain in ("proteomics", "astronomy"):
        collection = tmp_path / "collections" / domain / "v1"
        collection.mkdir(parents=True)
        (collection / "skills_index.json").write_text(json.dumps([
            {"slug": "spectrum-analysis", "name": "Spectrum analysis"},
        ]))
    hits = idx.search(None, "skills", "spectrum", root=tmp_path)
    assert [hit["qualified_slug"] for hit in hits] == [
        "astronomy/v1/skills/spectrum-analysis", "proteomics/v1/skills/spectrum-analysis",
    ]


def test_flat_workflow_unit_resolves_its_own_index(tmp_path):
    index = tmp_path / "workflows_index.json"
    index.write_text('[{"slug": "workflow", "member_tools": ["SkyFit"]}]')
    assert idx.index_path(tmp_path, "workflows") == index
    rows = idx.load_rows(tmp_path, "workflows")
    hits = idx.keyword_search(rows, "SkyFit", collection="astronomy/v1", target="workflows")
    assert hits[0]["matched_fields"] == {"member_tools": ["skyfit"]}


def test_resolver_can_leave_a_workflow_directory_without_a_workflow_index(tmp_path):
    workflows = tmp_path / "workflows"
    workflows.mkdir()
    tools = tmp_path / "tools_index.json"
    tools.write_text('[{"slug": "skyfit", "name": "SkyFit"}]')
    assert idx.index_path(workflows, "tools") == tools


def test_a_complete_unit_named_workflows_keeps_its_own_tools_index(tmp_path):
    unit = tmp_path / "workflows"
    unit.mkdir()
    tools = unit / "tools_index.json"
    tools.write_text('[{"slug": "skyfit", "name": "SkyFit"}]')
    (unit / "workflows_index.json").write_text("[]")
    assert idx.index_path(unit, "tools") == tools


@pytest.mark.parametrize("rule", idx.SELECTORS)
def test_filter_only_requests_and_no_match_are_distinct(rule):
    rows = [{"slug": "stellar", "name": "Stellar light curves", "tools": ["SkyFit"]}]
    options = {"collection": "astronomy/v1", "selector": rule}
    hits = idx.keyword_search(rows, "", tool="skyfit", **options)
    assert [hit["slug"] for hit in hits] == ["stellar"]
    assert hits[0]["matched_fields"] == {}
    assert idx.keyword_search(rows, "rainfall", **options) == []
    assert idx.keyword_search(rows, "the and for", **options) == []
    assert idx.keyword_search(rows, "", tool="unrelated", **options) == []
    assert idx.keyword_search(rows, "stellar", k=0, **options) == []
    assert idx.keyword_search(rows, "stellar", k=-1, **options) == []


def test_unknown_options_fail_explicitly():
    with pytest.raises(ValueError, match="unknown search target"):
        idx.index_path(COLLECTION, "typo")
    with pytest.raises(ValueError, match="unknown selector"):
        idx.keyword_search([], "stellar", selector="typo")
    with pytest.raises(ValueError, match="nonnegative"):
        idx.keyword_search([], "stellar", max_tools=-1)


def test_cli_compatibility_option_is_explicit_and_overridable(monkeypatch, capsys):
    from asb_skill_collections.asbb_cli import main

    monkeypatch.setenv(idx.SELECTOR_ENV, "router")
    assert main([
        "search", "untargeted LC-MS/MS annotation", "--collection", "metabolomics/v2",
        "--target", "workflows", "--repo", str(ROOT), "--k", "3",
    ]) == 0
    results = json.loads(capsys.readouterr().out)["results"]
    expected = idx.search(
        "metabolomics/v2", "workflows", "untargeted LC-MS/MS annotation", k=3,
        root=ROOT, selector="router",
    )
    assert results == expected
    assert all(hit["selector"]["rule"] == "router" for hit in results)
    assert idx.resolve_selector("package") == "package"


def test_tool_guard_never_excludes_curated_composites():
    tools = ["SkyFit", *[f"tool-{number}" for number in range(30)]]
    row = {"slug": "workflow", "name": "SkyFit analysis", "member_tools": tools}
    hits = idx.keyword_search([row], "SkyFit", target="workflows", collection="astronomy/v1")
    assert hits and hits[0]["filters"]["max_tools"] == 0
    assert idx.keyword_search([row], "SkyFit", collection="astronomy/v1") == []
    assert idx.keyword_search([row], "SkyFit", max_tools=0, collection="astronomy/v1")
