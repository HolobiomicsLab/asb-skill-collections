import json
import os
from pathlib import Path

import pytest


def make_repo(root: Path, slug="demo-pack", source="packs/demo/pack",
              skills=("alpha-skill", "beta-skill")):
    """Build a minimal fake asb-skill-collections checkout under `root`."""
    mp = root / ".claude-plugin"
    mp.mkdir(parents=True)
    (mp / "marketplace.json").write_text(json.dumps({
        "schema_version": 1, "name": "demo", "plugins": [
            {"name": slug, "source": f"./{source}"},
        ],
    }), encoding="utf-8")
    skills_dir = root / source / "skills"
    for name in skills:
        d = skills_dir / name
        d.mkdir(parents=True)
        (d / "SKILL.md").write_text(
            "---\n"
            f"name: {name}\n"
            "description: 'Use when testing: do the thing.'\n"
            "license: CC-BY-4.0\n"
            "---\n\n"
            f"# {name}\n\nBody for {name}.\n",
            encoding="utf-8",
        )
    return root


def test_find_repo_root_walks_up(tmp_path):
    from scripts.asbb.repo import find_repo_root
    make_repo(tmp_path)
    deep = tmp_path / "packs" / "demo" / "pack" / "skills" / "alpha-skill"
    assert find_repo_root(deep) == tmp_path.resolve()


def test_find_repo_root_missing_raises(tmp_path):
    from scripts.asbb.repo import find_repo_root
    with pytest.raises(FileNotFoundError):
        find_repo_root(tmp_path)


def test_resolve_pack_and_skill_dirs(tmp_path):
    from scripts.asbb.repo import resolve_pack, iter_skill_dirs, list_pack_slugs
    make_repo(tmp_path)
    assert list_pack_slugs(tmp_path) == ["demo-pack"]
    pack = resolve_pack(tmp_path, "demo-pack")
    assert pack.source == "packs/demo/pack"
    names = [d.name for d in iter_skill_dirs(pack)]
    assert names == ["alpha-skill", "beta-skill"]


def test_resolve_pack_unknown_raises(tmp_path):
    from scripts.asbb.repo import resolve_pack
    make_repo(tmp_path)
    with pytest.raises(KeyError):
        resolve_pack(tmp_path, "nope")


def test_parse_skill_md_frontmatter_and_body(tmp_path):
    from scripts.asbb.skillmd import parse_skill_md
    make_repo(tmp_path)
    p = tmp_path / "packs/demo/pack/skills/alpha-skill/SKILL.md"
    fm, body = parse_skill_md(p)
    assert fm["name"] == "alpha-skill"
    assert fm["description"] == "Use when testing: do the thing."
    assert body.startswith("# alpha-skill")
    assert "Body for alpha-skill." in body


def test_parse_skill_md_no_frontmatter(tmp_path):
    from scripts.asbb.skillmd import parse_skill_md
    p = tmp_path / "plain.md"
    p.write_text("just text\n", encoding="utf-8")
    fm, body = parse_skill_md(p)
    assert fm == {}
    assert body == "just text\n"


def test_manifest_round_trip(tmp_path):
    from scripts.asbb import manifest
    home = tmp_path / "home"
    assert manifest.get(home, "demo-pack", "agents") is None
    manifest.record(home, "demo-pack", "agents", home / "d", ["alpha-skill"], "symlink")
    rec = manifest.get(home, "demo-pack", "agents")
    assert rec["entries"] == ["alpha-skill"]
    assert rec["mode"] == "symlink"
    assert rec["dest_root"] == str(home / "d")


def test_manifest_remove_prunes_empty(tmp_path):
    from scripts.asbb import manifest
    home = tmp_path / "home"
    manifest.record(home, "demo-pack", "agents", home / "d", ["x"], "symlink")
    manifest.remove(home, "demo-pack", "agents")
    assert manifest.get(home, "demo-pack", "agents") is None
    assert manifest.load(home) == {}


def _opts(tmp_path, **kw):
    from scripts.asbb.targets import InstallOpts
    return InstallOpts(home=tmp_path / "home", project=tmp_path / "proj", **kw)


def test_skill_native_dests(tmp_path):
    from scripts.asbb.targets import get_target
    o = _opts(tmp_path)
    assert get_target("agents").dest(o) == o.home / ".agents" / "skills"
    assert get_target("codex").dest(o) == o.home / ".codex" / "skills"
    assert get_target("gemini").dest(o) == o.home / ".gemini" / "skills"
    assert get_target("claude").dest(o) == o.project / ".claude" / "skills"
    assert get_target("claude").dest(_opts(tmp_path, user=True)) == o.home / ".claude" / "skills"


def test_rules_dests_and_filenames(tmp_path):
    from scripts.asbb.targets import get_target
    o = _opts(tmp_path)
    cur = get_target("cursor")
    assert cur.kind == "rules"
    assert cur.dest(o) == o.project / ".cursor" / "rules"
    assert cur.filename("alpha-skill") == "alpha-skill.mdc"
    assert get_target("cline").filename("alpha-skill") == "alpha-skill.md"
    assert get_target("vscode-copilot").filename("a") == "a.instructions.md"


def test_rules_render_carries_description_and_body():
    from scripts.asbb.targets import get_target
    fm = {"name": "alpha-skill", "description": "Use when X."}
    body = "# alpha-skill\n\nDo the thing.\n"
    out = get_target("cursor").render(fm, body, "alpha-skill")
    assert "Use when X." in out
    assert "Do the thing." in out
    assert "alwaysApply" in out
    vs = get_target("vscode-copilot").render(fm, body, "alpha-skill")
    assert "applyTo" in vs and "Do the thing." in vs
    cl = get_target("cline").render(fm, body, "alpha-skill")
    assert "Do the thing." in cl


def test_list_runtimes_lists_all_ids():
    from scripts.asbb.targets import list_runtimes
    text = list_runtimes()
    for rid in ("agents", "codex", "copilot", "gemini", "claude",
                "cursor", "cline", "vscode-copilot"):
        assert rid in text


def test_resolve_rejects_escape(tmp_path):
    from scripts.asbb.installer import _resolve
    root = tmp_path / "dest"
    assert _resolve(root, "alpha-skill") == (root / "alpha-skill").resolve()
    with pytest.raises(ValueError):
        _resolve(root, "../evil")


def test_install_skill_native_symlinks(tmp_path):
    from scripts.asbb.repo import resolve_pack
    from scripts.asbb.targets import get_target, InstallOpts
    from scripts.asbb.installer import install
    make_repo(tmp_path)
    pack = resolve_pack(tmp_path, "demo-pack")
    o = InstallOpts(home=tmp_path / "home", project=tmp_path / "proj")
    written = install(pack, get_target("agents"), o)
    assert sorted(written) == ["alpha-skill", "beta-skill"]
    link = o.home / ".agents" / "skills" / "alpha-skill"
    assert link.is_symlink()
    assert (link / "SKILL.md").is_file()


def test_install_copy_makes_real_dirs(tmp_path):
    from scripts.asbb.repo import resolve_pack
    from scripts.asbb.targets import get_target, InstallOpts
    from scripts.asbb.installer import install
    make_repo(tmp_path)
    pack = resolve_pack(tmp_path, "demo-pack")
    o = InstallOpts(home=tmp_path / "home", project=tmp_path / "proj", copy=True)
    install(pack, get_target("agents"), o)
    d = o.home / ".agents" / "skills" / "alpha-skill"
    assert d.is_dir() and not d.is_symlink()


def test_install_idempotent_reinstall(tmp_path):
    from scripts.asbb.repo import resolve_pack
    from scripts.asbb.targets import get_target, InstallOpts
    from scripts.asbb.installer import install
    make_repo(tmp_path)
    pack = resolve_pack(tmp_path, "demo-pack")
    o = InstallOpts(home=tmp_path / "home", project=tmp_path / "proj")
    install(pack, get_target("agents"), o)
    written = install(pack, get_target("agents"), o)  # no conflict, no error
    assert sorted(written) == ["alpha-skill", "beta-skill"]


def test_install_dest_override(tmp_path):
    from scripts.asbb.repo import resolve_pack
    from scripts.asbb.targets import generic_dest_target, InstallOpts
    from scripts.asbb.installer import install
    make_repo(tmp_path)
    pack = resolve_pack(tmp_path, "demo-pack")
    dest = tmp_path / "anywhere"
    o = InstallOpts(home=tmp_path / "home", project=tmp_path / "proj",
                    copy=True, dest_override=dest)
    install(pack, generic_dest_target(), o)
    assert (dest / "alpha-skill" / "SKILL.md").is_file()


def test_install_rules_renders_files(tmp_path):
    from scripts.asbb.repo import resolve_pack
    from scripts.asbb.targets import get_target, InstallOpts
    from scripts.asbb.installer import install
    make_repo(tmp_path)
    pack = resolve_pack(tmp_path, "demo-pack")
    o = InstallOpts(home=tmp_path / "home", project=tmp_path / "proj")
    install(pack, get_target("cursor"), o)
    f = o.project / ".cursor" / "rules" / "alpha-skill.mdc"
    assert f.is_file()
    assert "Body for alpha-skill." in f.read_text(encoding="utf-8")


def test_install_unmanaged_conflict_needs_force(tmp_path):
    from scripts.asbb.repo import resolve_pack
    from scripts.asbb.targets import get_target, InstallOpts
    from scripts.asbb.installer import install
    make_repo(tmp_path)
    pack = resolve_pack(tmp_path, "demo-pack")
    o = InstallOpts(home=tmp_path / "home", project=tmp_path / "proj")
    dest = o.home / ".agents" / "skills" / "alpha-skill"
    dest.mkdir(parents=True)
    (dest / "SKILL.md").write_text("foreign", encoding="utf-8")
    with pytest.raises(FileExistsError):
        install(pack, get_target("agents"), o)
    o.force = True
    install(pack, get_target("agents"), o)  # now succeeds
    assert (o.home / ".agents" / "skills" / "alpha-skill").is_symlink()


def test_install_dry_run_writes_nothing(tmp_path):
    from scripts.asbb.repo import resolve_pack
    from scripts.asbb.targets import get_target, InstallOpts
    from scripts.asbb.installer import install
    make_repo(tmp_path)
    pack = resolve_pack(tmp_path, "demo-pack")
    o = InstallOpts(home=tmp_path / "home", project=tmp_path / "proj", dry_run=True)
    install(pack, get_target("agents"), o)
    assert not (o.home / ".agents").exists()


def test_uninstall_removes_recorded_entries(tmp_path):
    from scripts.asbb.repo import resolve_pack
    from scripts.asbb.targets import get_target, InstallOpts
    from scripts.asbb.installer import install, uninstall
    make_repo(tmp_path)
    pack = resolve_pack(tmp_path, "demo-pack")
    o = InstallOpts(home=tmp_path / "home", project=tmp_path / "proj")
    install(pack, get_target("agents"), o)
    removed = uninstall("demo-pack", get_target("agents"), o)
    assert sorted(removed) == ["alpha-skill", "beta-skill"]
    assert not (o.home / ".agents" / "skills" / "alpha-skill").exists()
    assert uninstall("demo-pack", get_target("agents"), o) == []  # no-op second time
