"""Installed synthetic units must work without their source checkout."""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from asb_skill_collections.asbb import manifest
from asb_skill_collections.asbb.repo import resolve_pack
from asb_skill_collections.asbb.targets import InstallOpts, generic_dest_target
from asb_skill_collections.asbb.installer import install, uninstall
from asb_skill_collections.asbb_cli import main
from tests.test_asbb_install import make_repo


def make_unit(root, source="collections/example/v3", slug="example-unit"):
    """A tiny corpus using the shipped standalone keyword-search executable."""
    make_repo(root, source=source, slug=slug, skills=("entry-point",))
    unit = root / source
    (unit / "collection.yaml").write_text('version: "3.2.1"\n')
    (unit / "leaves" / "feature-align").mkdir(parents=True)
    (unit / "leaves" / "feature-align" / "SKILL.md").write_text(
        "---\nname: feature-align\nlicense: CC-BY-4.0\n"
        "derived_from:\n- doi: 10.0000/synthetic\n---\nAlign features.\n"
    )
    (unit / "skills_index.json").write_text(json.dumps([
        {"slug": "feature-align", "name": "Feature alignment",
         "description": "align features", "tools": [], "license_tier": "open"}
    ]))
    (unit / "bin").mkdir()
    script = Path(__file__).resolve().parents[1] / (
        "collections/metabolomics/v2/bin/search_skills.py"
    )
    shutil.copyfile(script, unit / "bin" / "search_skills.py")
    (unit / "skills" / "entry-point" / "SKILL.md").write_text(
        "---\nname: entry-point\ndescription: Find a feature method.\n---\n"
        "Run `python bin/search_skills.py --query alignment`, then read the hit.\n"
    )
    (unit / "kb_bundle.json").write_text('{"skills": {}}\n')
    (unit / ".cache").mkdir()
    (unit / ".cache" / "private.txt").write_text("private cache sentinel")
    return unit


@pytest.mark.parametrize("source", ["collections/example/v3", "packs/example/technique"])
@pytest.mark.parametrize("runtime", ["dest", "cursor", "cline", "vscode-copilot"])
def test_cli_copied_unit_search_survives_source_removal(tmp_path, monkeypatch, source, runtime):
    repo = tmp_path / "source checkout"
    make_unit(repo, source)
    project = tmp_path / "project with spaces"
    project.mkdir()
    monkeypatch.chdir(project)
    dest = tmp_path / "installed skills"
    selection = ["--dest", str(dest)] if runtime == "dest" else ["--runtime", runtime]
    args = ["install", "example-unit", "--repo", str(repo),
            "--home", str(tmp_path / "home"), "--copy", *selection]
    assert main(args) == 0
    rec = manifest.get(tmp_path / "home", "example-unit", runtime)
    dest = Path(rec["dest_root"])
    unit = dest / ".asbb-units" / "example-unit"
    assert (unit / "skills" / "entry-point" / "SKILL.md").is_file()
    assert (unit / "skills_index.json").is_file()
    assert (unit / "kb_bundle.json").is_file()
    assert not (unit / ".cache").exists()
    adapter_rel = {"dest": "entry-point/SKILL.md", "cursor": "entry-point.mdc",
                   "cline": "entry-point.md", "vscode-copilot": "entry-point.instructions.md"}[runtime]
    adapter = (dest / adapter_rel).read_text()
    assert ".asbb-units/example-unit" in adapter
    assert str(repo) not in adapter
    assert rec["source"]["version"] == "3.2.1"
    assert len(rec["source"]["sha256"]) == 64
    assert rec["source"]["path"] == source
    assert ".asbb-units/example-unit" in rec["entries"]

    shutil.rmtree(repo)
    relocated = tmp_path / "moved install"
    shutil.move(str(dest), relocated)
    unit = relocated / ".asbb-units" / "example-unit"
    elsewhere = tmp_path / "unrelated cwd"
    elsewhere.mkdir()
    result = subprocess.run(
        [sys.executable, str(unit / "bin" / "search_skills.py"), "--query", "alignment"],
        cwd=elsewhere, env={"PATH": os.environ["PATH"], "PYTHONDONTWRITEBYTECODE": "1"},
        capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "feature-align" in result.stdout
    leaf = result.stdout.split("read: ", 1)[1].strip()
    body = (unit / leaf).read_text()
    assert "Align features." in body and "CC-BY-4.0" in body and "10.0000/synthetic" in body


def test_copy_reinstall_updates_digest_cleans_stale_entries_and_preserves_neighbors(tmp_path):
    repo = tmp_path / "repo"
    source = make_unit(repo)
    target = generic_dest_target()
    opts = InstallOpts(home=tmp_path / "home", project=tmp_path,
                       copy=True, dest_override=tmp_path / "dest")
    install(resolve_pack(repo, "example-unit"), target, opts)
    original = manifest.get(opts.home, "example-unit", "dest")
    neighbor = opts.dest_override / "personal.txt"
    neighbor.write_text("keep")
    (source / ".cache" / "private.txt").write_text("changed private cache")
    install(resolve_pack(repo, "example-unit"), target, opts)
    assert manifest.get(opts.home, "example-unit", "dest")["source"] == original["source"]
    (source / "skills" / "entry-point").rename(source / "skills" / "new-entry")
    (source / "leaves" / "feature-align" / "SKILL.md").write_text("Updated procedure.\n")
    install(resolve_pack(repo, "example-unit"), target, opts)
    current = manifest.get(opts.home, "example-unit", "dest")
    assert current["source"]["sha256"] != original["source"]["sha256"]
    assert not (opts.dest_override / "entry-point").exists()
    assert (opts.dest_override / "new-entry" / "SKILL.md").exists()
    assert neighbor.read_text() == "keep"
    uninstall("example-unit", target, opts)
    assert not (opts.dest_override / ".asbb-units" / "example-unit").exists()
    assert neighbor.read_text() == "keep"
    assert uninstall("example-unit", target, opts) == []


def test_copy_dry_run_and_unit_collision(tmp_path):
    repo = tmp_path / "repo"
    make_unit(repo)
    pack = resolve_pack(repo, "example-unit")
    target = generic_dest_target()
    opts = InstallOpts(home=tmp_path / "home", project=tmp_path, copy=True,
                       dry_run=True, dest_override=tmp_path / "dest")
    install(pack, target, opts)
    assert not opts.dest_override.exists()
    assert not opts.home.exists()
    unit = opts.dest_override / ".asbb-units" / "example-unit"
    unit.mkdir(parents=True)
    (unit / "personal.txt").write_text("keep")
    opts.dry_run = False
    with pytest.raises(FileExistsError):
        install(pack, target, opts)
    assert (unit / "personal.txt").read_text() == "keep"
    opts.force = True
    install(pack, target, opts)
    assert (unit / "skills_index.json").is_file()


def test_symlink_install_documents_and_retains_source_dependency(tmp_path):
    repo = tmp_path / "repo"
    source = make_unit(repo)
    opts = InstallOpts(home=tmp_path / "home", project=tmp_path,
                       dest_override=tmp_path / "dest")
    target = generic_dest_target()
    install(resolve_pack(repo, "example-unit"), target, opts)
    link = opts.dest_override / "entry-point"
    assert link.is_symlink() and (link / "SKILL.md").is_file()
    assert link.resolve() == source / "skills" / "entry-point"
    shutil.rmtree(repo)
    assert not (link / "SKILL.md").exists()
    uninstall("example-unit", target, opts)
    assert not link.is_symlink()
