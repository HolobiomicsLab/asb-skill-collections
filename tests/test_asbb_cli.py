"""Tests for the shared skill-index library + the asbb search/get CLI + MCP guard."""
import importlib
import json
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))


@pytest.fixture()
def demo_root(tmp_path):
    """A synthetic 2-version collection checkout (no network, no numpy)."""
    col = tmp_path / "collections" / "demo" / "v2"
    (col / "skills" / "alpha-detect").mkdir(parents=True)
    (col / "skills" / "beta-annotate").mkdir(parents=True)
    (col / "workflows" / "full-pipeline").mkdir(parents=True)
    (col / "tools").mkdir(parents=True)

    (col / "skills_index.json").write_text(json.dumps([
        {"slug": "alpha-detect", "name": "alpha detection",
         "description": "detect features in LC-MS data", "tools": ["XCMS"],
         "techniques": ["LC-MS"]},
        {"slug": "beta-annotate", "name": "beta annotation",
         "description": "annotate spectra by NMR shift", "tools": ["tool"],
         "techniques": ["NMR"]},
        # registry/meta artifact: >25 tools -> must be dropped from skills search
        {"slug": "junk-meta", "name": "everything", "description": "detect annotate",
         "tools": [f"t{i}" for i in range(40)], "techniques": ["LC-MS"]},
    ]))
    (col / "workflows" / "workflows_index.json").write_text(json.dumps([
        {"slug": "full-pipeline", "name": "full pipeline",
         "description": "end to end annotation pipeline", "techniques": ["LC-MS"],
         "stages": ["a", "b"], "member_tools": ["XCMS", "SIRIUS"]},
    ]))
    (col / "tools_index.json").write_text(json.dumps([
        {"slug": "xcms", "name": "XCMS", "edam_topics": []},
    ]))
    (col / "skills" / "alpha-detect" / "SKILL.md").write_text("# alpha\nbody\n")
    (col / "workflows" / "full-pipeline" / "SKILL.md").write_text("# pipeline\nstages\n")

    (tmp_path / "catalogue.jsonld").write_text(json.dumps({
        "collections": [{"slug": "demo", "version": "2", "title": "Demo v2",
                         "skills_count": 3, "tools_count": 1}]
    }))
    return tmp_path


def test_ver_key_mixed_no_typeerror():
    from asb_skill_collections.asb_skill_index import _ver_key
    # mixed numeric/alpha components must compare without TypeError
    assert _ver_key("2") > _ver_key("2-rc")
    assert _ver_key("10") > _ver_key("2")


def test_discover_and_resolve(demo_root):
    from asb_skill_collections import asb_skill_index as idx
    cols = idx.discover_collections(demo_root)
    assert len(cols) == 1 and cols[0]["id"] == "demo/v2"
    assert cols[0]["has_workflows"] and cols[0]["title"] == "Demo v2"
    assert idx.resolve_collection_dir("demo", demo_root).name == "v2"      # bare slug -> latest
    assert idx.resolve_collection_dir("demo/v2", demo_root) is not None
    assert idx.resolve_collection_dir("nope", demo_root) is None


def test_search_ranks_and_drops_junk(demo_root):
    from asb_skill_collections import asb_skill_index as idx
    hits = idx.search(None, "skills", "detect features", root=demo_root)  # None = all collections
    slugs = [h["slug"] for h in hits]
    assert "alpha-detect" in slugs
    assert "junk-meta" not in slugs          # >25-tool artifact filtered


def test_search_technique_filter(demo_root):
    from asb_skill_collections import asb_skill_index as idx
    nmr = idx.search("demo", "skills", "annotate", technique="NMR", root=demo_root)
    assert [h["slug"] for h in nmr] == ["beta-annotate"]


def test_search_workflows_no_junk_guard(demo_root):
    from asb_skill_collections import asb_skill_index as idx
    wf = idx.search("demo", "workflows", "annotation pipeline", root=demo_root)
    assert wf and wf[0]["slug"] == "full-pipeline"


def test_get_item_text(demo_root):
    from asb_skill_collections import asb_skill_index as idx
    assert "alpha" in idx.get_item_text("demo/v2", "skills", "alpha-detect", root=demo_root)
    assert idx.get_item_text("demo/v2", "skills", "missing", root=demo_root) is None


def test_cli_search_and_get(demo_root, capsys):
    from asb_skill_collections.asbb_cli import main
    rc = main(["search", "detect", "--repo", str(demo_root), "--target", "skills"])
    assert rc == 0
    out = json.loads(capsys.readouterr().out)
    assert any(r["slug"] == "alpha-detect" for r in out["results"])

    rc = main(["get", "alpha-detect", "--collection", "demo/v2",
               "--repo", str(demo_root), "--target", "skills"])
    assert rc == 0
    assert "alpha" in capsys.readouterr().out


def test_mcp_server_requires_extra():
    """Without the mcp extra, importing the server exits cleanly with guidance."""
    try:
        import mcp  # noqa: F401
        pytest.skip("mcp extra installed; import-guard path not exercised")
    except ModuleNotFoundError:
        sys.modules.pop("asb_skill_collections.asb_mcp_server", None)
        with pytest.raises(SystemExit):
            importlib.import_module("asb_skill_collections.asb_mcp_server")
