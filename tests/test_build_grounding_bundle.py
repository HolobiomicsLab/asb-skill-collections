"""Unit tests for build_grounding_bundle.py."""
import json, pathlib, sys
import pytest, yaml

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
FIX = pathlib.Path(__file__).parent / "fixtures" / "mini_grounding"


def _corpus():
    return yaml.safe_load((FIX / "corpus.yaml").read_text())["papers"]

def _tools():
    return json.loads((FIX / "tools_index.json").read_text())


def test_resolve_repo_urls_merges_corpus_and_tools_dedup():
    from scripts.build_grounding_bundle import resolve_repo_urls
    urls = resolve_repo_urls(["10.1021/acs.jnatprod.7b00737"], _corpus(), _tools())
    assert urls == [
        "https://github.com/DorresteinLaboratory/Bioactive_Molecular_Networks",
        "https://github.com/CCMS-UCSD/GNPS_Workflows",
    ]


def test_resolve_repo_urls_drops_empty():
    from scripts.build_grounding_bundle import resolve_repo_urls
    assert resolve_repo_urls(["10.1000/norepo"], _corpus(), _tools()) == []


def test_filter_and_enrich_bundle():
    from scripts.build_grounding_bundle import filter_and_enrich_bundle
    full = json.loads((FIX / "kb_bundle.json").read_text())
    out = filter_and_enrich_bundle(full, {"bioactivity-score-aggregation", "norepo-skill"}, _corpus(), _tools())
    assert set(out["skills"]) == {"bioactivity-score-aggregation", "norepo-skill"}
    assert out["skills"]["bioactivity-score-aggregation"]["repo_urls"] == [
        "https://github.com/DorresteinLaboratory/Bioactive_Molecular_Networks",
        "https://github.com/CCMS-UCSD/GNPS_Workflows",
    ]
    assert out["skills"]["norepo-skill"]["repo_urls"] == []
    assert out["distinct_dois"] == ["10.1000/norepo", "10.1021/acs.jnatprod.7b00737"]
    assert out["kb_prefix"] == "asb-paper-"


def test_render_ground_command_has_frontmatter_and_both_modes():
    from scripts.build_grounding_bundle import render_ground_command
    md = render_ground_command()
    assert md.startswith("---\n")
    assert "description:" in md and "argument-hint:" in md
    assert "perspicacite_kb_bind.py" in md
    assert "query" in md and "local" in md          # both backends referenced
    assert "$ARGUMENTS" in md

def test_render_grounding_doc_names_unit():
    from scripts.build_grounding_bundle import render_grounding_doc
    doc = render_grounding_doc("metabolomics-lc-ms")
    assert "metabolomics-lc-ms" in doc
    assert "PERSPICACITE_BASE" in doc and "git clone" in doc


def test_resolve_repo_urls_normalizes_and_dedups_shorthand():
    from scripts.build_grounding_bundle import resolve_repo_urls
    urls = resolve_repo_urls(
        ["10.x/y"],
        [{"doi": "10.x/y", "repo_url": "owner/repo"}],
        [{"dois": ["10.x/y"], "canonical_url": "https://github.com/owner/repo"}],
    )
    assert urls == ["https://github.com/owner/repo"]


def test_real_lcms_pack_builds(tmp_path):
    import shutil
    from scripts.build_grounding_bundle import build_unit
    root = pathlib.Path(__file__).parent.parent
    src_unit = root / "packs" / "metabolomics" / "lc-ms"
    col = root / "collections" / "metabolomics" / "v2"
    if not src_unit.exists() or not (col / "kb_bundle.json").exists():
        pytest.skip("real pack/collection not present in this checkout")
    unit = tmp_path / "lc-ms"
    shutil.copytree(src_unit, unit, symlinks=True)
    build_unit(unit, col, root / "scripts" / "perspicacite_kb_bind.py")
    b = json.loads((unit / "kb_bundle.json").read_text())
    assert b["skills"] and (unit / "commands" / "ground.md").exists()
    # binder covers only this pack's skills
    pack_slugs = {d.name for d in (unit / "skills").iterdir() if d.is_dir()}
    assert set(b["skills"]).issubset(pack_slugs)


def test_build_unit_emits_all_artifacts(tmp_path):
    from scripts.build_grounding_bundle import build_unit
    # arrange a fake unit with two skills, one present in the binder
    unit = tmp_path / "unit"
    (unit / "skills" / "bioactivity-score-aggregation").mkdir(parents=True)
    (unit / "skills" / "norepo-skill").mkdir(parents=True)
    (unit / ".claude-plugin").mkdir()
    (unit / ".claude-plugin" / "plugin.json").write_text(json.dumps({"name": "u", "description": "Subset."}))
    bind = tmp_path / "src_bind.py"; bind.write_text("# vendored bind\n")
    written = build_unit(unit, FIX, bind)
    assert set(written) == {"kb_bundle.json", "bin/perspicacite_kb_bind.py", "commands/ground.md", "GROUNDING.md", ".claude-plugin/plugin.json"}
    b = json.loads((unit / "kb_bundle.json").read_text())
    assert set(b["skills"]) == {"bioactivity-score-aggregation", "norepo-skill"}
    assert "repo_urls" in b["skills"]["bioactivity-score-aggregation"]
    assert (unit / "bin" / "perspicacite_kb_bind.py").read_text() == "# vendored bind\n"
    assert (unit / "commands" / "ground.md").exists()
    assert (unit / "GROUNDING.md").exists()
    desc = json.loads((unit / ".claude-plugin" / "plugin.json").read_text())["description"]
    assert desc.endswith("Packaged auto-grounding (kb+local).")
    # idempotent: second run does not double-append
    written2 = build_unit(unit, FIX, bind)
    assert ".claude-plugin/plugin.json" not in written2
    desc2 = json.loads((unit / ".claude-plugin" / "plugin.json").read_text())["description"]
    assert desc2 == desc


def _make_unit(tmp_path):
    unit = tmp_path / "unit"
    (unit / "skills" / "bioactivity-score-aggregation").mkdir(parents=True)
    (unit / ".claude-plugin").mkdir()
    (unit / ".claude-plugin" / "plugin.json").write_text(json.dumps({"name": "u", "description": "Subset."}))
    bind = tmp_path / "src_bind.py"; bind.write_text("# vendored bind\n")
    return unit, bind


def _make_collection_with_commands(tmp_path):
    col = tmp_path / "col"
    col.mkdir()
    shutil_copy_fixture(col)
    cmds = col / "commands"
    cmds.mkdir()
    (cmds / "ground.md").write_text("STALE ground content — should be overwritten\n")
    (cmds / "propose-skill.md").write_text("# propose-skill\nbody\n")
    (cmds / "synthesize-meta-skill.md").write_text("# synthesize-meta-skill\nbody\n")
    return col


def shutil_copy_fixture(col):
    import shutil
    for name in ("corpus.yaml", "kb_bundle.json", "tools_index.json"):
        shutil.copyfile(FIX / name, col / name)


def test_build_unit_ships_all_collection_commands(tmp_path):
    from scripts.build_grounding_bundle import build_unit, render_ground_command
    unit, bind = _make_unit(tmp_path)
    col = _make_collection_with_commands(tmp_path)
    written = build_unit(unit, col, bind)
    cmd_dir = unit / "commands"
    # all three commands ship
    assert (cmd_dir / "ground.md").exists()
    assert (cmd_dir / "propose-skill.md").exists()
    assert (cmd_dir / "synthesize-meta-skill.md").exists()
    # ground.md comes from render_ground_command(), not the collection's stale copy
    assert (cmd_dir / "ground.md").read_text() == render_ground_command()
    # other commands copied verbatim
    assert (cmd_dir / "propose-skill.md").read_text() == "# propose-skill\nbody\n"
    assert (cmd_dir / "synthesize-meta-skill.md").read_text() == "# synthesize-meta-skill\nbody\n"
    # writes are reported relative to the unit
    assert "commands/ground.md" in written
    assert "commands/propose-skill.md" in written
    assert "commands/synthesize-meta-skill.md" in written


def test_build_unit_without_collection_commands_dir(tmp_path):
    # When the collection has no commands/ dir, only ground.md is shipped.
    from scripts.build_grounding_bundle import build_unit
    unit, bind = _make_unit(tmp_path)
    written = build_unit(unit, FIX, bind)
    assert (unit / "commands" / "ground.md").exists()
    assert "commands/ground.md" in written
    assert not any(w.startswith("commands/") and w != "commands/ground.md" for w in written)
