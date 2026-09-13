"""Installed packs remain usable without their checkout and cannot delete neighbours."""

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from asb_skill_collections.asbb import manifest
from asb_skill_collections.asbb.installer import install, uninstall
from asb_skill_collections.asbb.repo import resolve_pack
from asb_skill_collections.asbb.targets import (
    TARGETS,
    InstallOpts,
    generic_dest_target,
)


def make_pack(repo, slug="stellar", version="1", entry="_router"):
    """Create a small marketplace pack with executable, relative-path assets."""
    marketplace = repo / ".claude-plugin" / "marketplace.json"
    marketplace.parent.mkdir(parents=True, exist_ok=True)
    data = (
        json.loads(marketplace.read_text()) if marketplace.exists() else {"plugins": []}
    )
    data["plugins"] = [p for p in data["plugins"] if p["name"] != slug]
    data["plugins"].append(
        {"name": slug, "version": version, "source": f"packs/{slug}"}
    )
    marketplace.write_text(json.dumps(data))
    source = repo / "packs" / slug
    files = {
        f"skills/{entry}/SKILL.md": (
            f"---\nname: {entry}\ndescription: Search this pack.\n---\n\n"
            "Run `python bin/search_skills.py --query signal` from the pack root.\n"
            "The feedback helper is `scripts/skill_feedback.py`.\n"
        ),
        "leaves/signal/SKILL.md": f"# {slug} {version}\n",
        "skills_index.json": json.dumps(
            [{"slug": "signal", "pack": slug, "version": version}]
        ),
        "bin/search_skills.py": (
            "import json\nfrom pathlib import Path\n"
            "root = Path(__file__).resolve().parent.parent\n"
            "rows = json.loads((root / 'skills_index.json').read_text())\n"
            "for row in rows:\n"
            "    assert (root / 'leaves' / row['slug'] / 'SKILL.md').is_file()\n"
            "print(json.dumps(rows))\n"
        ),
        "scripts/skill_feedback.py": "print('feedback helper available')\n",
        "workflows/workflows_index.json": "[]\n",
        "kb_bundle.json": '{"skills": {}}\n',
    }
    for rel, text in files.items():
        path = source / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    return resolve_pack(repo, slug)


def opts_for(tmp_path, **kwargs):
    home = tmp_path / "home"
    home.mkdir(exist_ok=True)
    project = home / "project"
    project.mkdir(exist_ok=True)
    return InstallOpts(home=home, project=project, **kwargs)


def entry_path(target, opts, name="_router"):
    rel = name if target.kind == "skill" else target.filename(name)
    path = target.dest(opts) / rel
    return path / "SKILL.md" if target.kind == "skill" else path


def installed_root(entry):
    marker = re.search(r"<!-- asbb-unit: (.+) -->", entry.read_text())
    assert marker, "the advertised entry must locate its installed asset root"
    root = Path(json.loads(marker[1]))
    assert root.is_dir()
    return root


def run_asset(root, script, home, cwd):
    result = subprocess.run(
        [sys.executable, str(root / script), "--query", "signal"],
        env={
            "HOME": str(home),
            "PATH": "/usr/bin:/bin",
            "PYTHONDONTWRITEBYTECODE": "1",
        },
        cwd=cwd,
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout


@pytest.mark.parametrize("runtime", [*TARGETS, "dest"])
@pytest.mark.parametrize("copy", [False, True])
def test_installed_unit_survives_source_removal_and_cwd(
    tmp_path, monkeypatch, runtime, copy
):
    repo = tmp_path / "checkout"
    pack = make_pack(repo)
    opts = opts_for(tmp_path, copy=copy, dest_override=tmp_path / "home" / "custom")
    monkeypatch.setenv("HOME", str(opts.home))
    target = generic_dest_target() if runtime == "dest" else TARGETS[runtime]
    install(pack, target, opts)
    source_text = (pack.skills_dir / "_router/SKILL.md").read_bytes()
    unit = installed_root(entry_path(target, opts))
    assert unit.is_relative_to(target.dest(opts).resolve())
    assert (unit / "skills/_router/SKILL.md").read_bytes() == source_text
    for rel in (
        "leaves/signal/SKILL.md",
        "kb_bundle.json",
        "workflows/workflows_index.json",
    ):
        assert (unit / rel).is_file()
    repo.rename(tmp_path / "source-unavailable")
    monkeypatch.chdir(opts.home)
    assert (
        json.loads(run_asset(unit, "bin/search_skills.py", opts.home, opts.home))[0][
            "pack"
        ]
        == "stellar"
    )
    assert "feedback helper available" in run_asset(
        unit, "scripts/skill_feedback.py", opts.home, opts.home
    )
    uninstall(pack.slug, target, opts)
    assert not unit.exists()


def test_corrupt_manifest_paths_preserve_neighbours(tmp_path, capsys):
    pack = make_pack(tmp_path / "repo")
    opts = opts_for(tmp_path)
    target = TARGETS["agents"]
    install(pack, target, opts)
    neighbour = target.dest(opts).parent / "neighbour"
    neighbour.write_text("keep")
    absolute = opts.home / "absolute-neighbour"
    absolute.write_text("keep absolute")
    data = manifest.load(opts.home)
    data[pack.slug][target.id]["entries"] += ["../neighbour", str(absolute)]
    manifest.save(opts.home, data)
    uninstall(pack.slug, target, opts)
    assert neighbour.read_text() == "keep"
    assert absolute.read_text() == "keep absolute"
    report = capsys.readouterr().err
    assert "../neighbour" in report and str(absolute) in report and "skipped" in report


@pytest.mark.parametrize(
    "runtime,copy", [("agents", False), ("agents", True), ("cursor", False)]
)
def test_takeover_and_upgrade_keep_only_the_current_owner(tmp_path, runtime, copy):
    repo = tmp_path / "repo"
    first = make_pack(repo, "stellar")
    second = make_pack(repo, "marine")
    opts = opts_for(tmp_path, copy=copy)
    target = TARGETS[runtime]
    install(first, target, opts)
    first_unit = installed_root(entry_path(target, opts))
    with pytest.raises(FileExistsError):
        install(second, target, opts)
    opts.force = True
    install(second, target, opts)
    second_unit = installed_root(entry_path(target, opts))
    uninstall(first.slug, target, opts)
    assert not first_unit.exists()
    assert (
        json.loads(
            run_asset(second_unit, "bin/search_skills.py", opts.home, opts.home)
        )[0]["pack"]
        == "marine"
    )
    assert entry_path(target, opts).is_file()
    uninstall(second.slug, target, opts)
    assert not entry_path(target, opts).exists()
    assert not second_unit.exists()
    opts.force = False
    previous = None
    for version in ("1", "2", "3"):
        first = make_pack(repo, "stellar", version)
        install(first, target, opts)
        unit = installed_root(entry_path(target, opts))
        if previous:
            assert not previous.exists()
        previous = unit
        assert len(list((target.dest(opts) / ".asbb-units").iterdir())) == 1
        rec = manifest.get(opts.home, first.slug, target.id)
        assert rec["version"] == version and rec["source_digest"]
        owner = rec["entry_owners"][rec["entries"][0]]
        assert (
            owner["pack"] == first.slug
            and owner["version"] == version
            and owner["sha256"]
        )
    uninstall(first.slug, target, opts)
    assert not list(target.dest(opts).iterdir())


@pytest.mark.parametrize("escape", ["final", "parent", "unit"])
def test_symlink_escape_is_preserved_and_reported(tmp_path, capsys, escape):
    pack = make_pack(tmp_path / "repo")
    opts = opts_for(tmp_path)
    target = TARGETS["agents"]
    install(pack, target, opts)
    unit = installed_root(entry_path(target, opts))
    dest = target.dest(opts)
    neighbour = opts.home / "neighbour"
    neighbour.mkdir()
    (neighbour / "sentinel").write_text("keep")
    if escape == "final":
        (dest / "_router").unlink()
        (dest / "_router").symlink_to(neighbour, target_is_directory=True)
    elif escape == "unit":
        shutil.rmtree(unit)
        unit.symlink_to(neighbour, target_is_directory=True)
    else:
        dest.rename(dest.with_name("saved-skills"))
        dest.symlink_to(neighbour, target_is_directory=True)
    uninstall(pack.slug, target, opts)
    assert (neighbour / "sentinel").read_text() == "keep"
    assert "skipped" in capsys.readouterr().err


def test_edited_copy_and_unrelated_files_survive_uninstall(tmp_path, capsys):
    pack = make_pack(tmp_path / "repo")
    opts = opts_for(tmp_path, copy=True)
    target = TARGETS["agents"]
    install(pack, target, opts)
    entry = entry_path(target, opts)
    entry.write_text("user replacement")
    neighbour = target.dest(opts) / "user-skill"
    neighbour.mkdir()
    uninstall(pack.slug, target, opts)
    assert entry.read_text() == "user replacement"
    assert neighbour.is_dir()
    assert "skipped" in capsys.readouterr().err


def test_stale_cleanup_reuses_containment(tmp_path, capsys):
    repo = tmp_path / "repo"
    pack = make_pack(repo)
    opts = opts_for(tmp_path)
    target = TARGETS["agents"]
    install(pack, target, opts)
    neighbour = target.dest(opts).parent / "neighbour"
    neighbour.write_text("keep")
    data = manifest.load(opts.home)
    data[pack.slug][target.id]["entries"].append("../neighbour")
    manifest.save(opts.home, data)
    make_pack(repo, version="2", entry="new-router")
    shutil.rmtree(pack.skills_dir / "_router")
    install(resolve_pack(repo, pack.slug), target, opts)
    assert neighbour.read_text() == "keep"
    assert "../neighbour" in capsys.readouterr().err


@pytest.mark.parametrize("rel", ["../escape", "/absolute", "inside/../escape"])
def test_installer_resolver_rejects_noncanonical_relative_paths(tmp_path, rel):
    from asb_skill_collections.asbb.installer import _resolve

    with pytest.raises(ValueError):
        _resolve(tmp_path, rel)


def test_install_refuses_destination_symlink_escape_even_with_force(tmp_path):
    pack = make_pack(tmp_path / "repo")
    opts = opts_for(tmp_path, force=True)
    target = TARGETS["agents"]
    dest = target.dest(opts)
    dest.mkdir(parents=True)
    neighbour = opts.home / "neighbour"
    neighbour.mkdir()
    (neighbour / "keep").write_text("keep")
    (dest / "_router").symlink_to(neighbour, target_is_directory=True)
    with pytest.raises(ValueError):
        install(pack, target, opts)
    assert (neighbour / "keep").read_text() == "keep"


@pytest.mark.parametrize("copy_unit", [False, True])
def test_corrupt_destination_cannot_claim_a_byte_identical_backup(
    tmp_path, capsys, copy_unit
):
    pack = make_pack(tmp_path / "repo")
    opts = opts_for(tmp_path, copy=True)
    target = TARGETS["agents"]
    install(pack, target, opts)
    original_root = target.dest(opts)
    backup = opts.home / "backup"
    shutil.copytree(original_root / "_router", backup / "_router")
    if copy_unit:
        shutil.copytree(original_root / ".asbb-units", backup / ".asbb-units")
    data = manifest.load(opts.home)
    data[pack.slug][target.id]["dest_root"] = str(backup)
    manifest.save(opts.home, data)
    uninstall(pack.slug, target, opts)
    assert (backup / "_router/SKILL.md").is_file()
    assert "skipped" in capsys.readouterr().err


def test_relocation_does_not_replace_an_unowned_identical_unit(tmp_path):
    pack = make_pack(tmp_path / "repo")
    opts = opts_for(tmp_path, copy=True, dest_override=tmp_path / "home/first")
    target = generic_dest_target()
    install(pack, target, opts)
    unit = installed_root(entry_path(target, opts))
    second = opts.home / "second"
    copied_unit = second / ".asbb-units" / unit.name
    shutil.copytree(unit, copied_unit)
    copied_entry = copied_unit / "skills/_router/SKILL.md"
    before = copied_entry.read_bytes()
    opts.dest_override = second
    with pytest.raises(FileExistsError):
        install(pack, target, opts)
    assert copied_entry.read_bytes() == before


def test_skipped_stale_copy_keeps_its_old_unit_and_receipt(tmp_path, capsys):
    repo = tmp_path / "repo"
    pack = make_pack(repo)
    opts = opts_for(tmp_path, copy=True)
    target = TARGETS["agents"]
    install(pack, target, opts)
    entry = entry_path(target, opts)
    original = entry.read_text()
    old_unit = installed_root(entry)
    entry.write_text(original + "\nUser annotation.\n")
    make_pack(repo, version="2", entry="new-router")
    shutil.rmtree(pack.skills_dir / "_router")
    install(resolve_pack(repo, pack.slug), target, opts)
    assert old_unit.is_dir()
    assert "User annotation." in entry.read_text()
    assert "skipped" in capsys.readouterr().err
    uninstall(pack.slug, target, opts)
    assert old_unit.is_dir() and manifest.get(opts.home, pack.slug, target.id)
    entry.write_text(original)
    uninstall(pack.slug, target, opts)
    assert not old_unit.exists() and not entry.exists()
    assert manifest.get(opts.home, pack.slug, target.id) is None


def test_modified_unit_keeps_its_receipt_until_cleanup_is_safe(tmp_path, capsys):
    pack = make_pack(tmp_path / "repo")
    opts = opts_for(tmp_path)
    target = TARGETS["agents"]
    install(pack, target, opts)
    unit = installed_root(entry_path(target, opts))
    note = unit / "user-note.txt"
    note.write_text("keep this note")
    uninstall(pack.slug, target, opts)
    assert note.read_text() == "keep this note"
    assert manifest.get(opts.home, pack.slug, target.id)
    assert "skipped" in capsys.readouterr().err
    note.unlink()
    uninstall(pack.slug, target, opts)
    assert not unit.exists() and manifest.get(opts.home, pack.slug, target.id) is None


def test_excluded_advertised_symlink_is_never_read_or_installed(tmp_path):
    pack = make_pack(tmp_path / "repo")
    opts = opts_for(tmp_path)
    outside = opts.home / "outside"
    outside.mkdir()
    (outside / "SKILL.md").write_text("External text must never be installed.")
    (pack.skills_dir / ".cache").symlink_to(outside, target_is_directory=True)
    with pytest.raises(ValueError):
        install(pack, TARGETS["agents"], opts)
    assert not TARGETS["agents"].dest(opts).exists()


def test_internal_alias_cannot_copy_excluded_local_state(tmp_path):
    pack = make_pack(tmp_path / "repo")
    opts = opts_for(tmp_path)
    cache = pack.skills_dir.parent / ".cache"
    cache.mkdir()
    (cache / "local-output.txt").write_text("Local cache must never ship.")
    (pack.skills_dir.parent / "support").symlink_to(cache, target_is_directory=True)
    with pytest.raises(ValueError):
        install(pack, TARGETS["agents"], opts)
    assert not TARGETS["agents"].dest(opts).exists()


@pytest.mark.parametrize(
    "domain", ["astronomy", "proteomics", "climate", "electrophysiology"]
)
def test_contained_source_aliases_materialise_and_direct_caches_stay_local(
    tmp_path, domain
):
    pack = make_pack(tmp_path / "repo", slug=domain)
    opts = opts_for(tmp_path)
    source = pack.skills_dir.parent
    (source / "support").symlink_to(source / "leaves", target_is_directory=True)
    (source / ".cache").mkdir()
    (source / ".cache/local-output.txt").write_text("do not ship")
    install(pack, TARGETS["agents"], opts)
    unit = installed_root(entry_path(TARGETS["agents"], opts))
    assert (unit / "support/signal/SKILL.md").read_text() == f"# {domain} 1\n"
    assert not (unit / "support").is_symlink()
    assert not (unit / ".cache").exists()


def test_same_version_content_upgrade_and_dry_run(tmp_path):
    pack = make_pack(tmp_path / "repo")
    opts = opts_for(tmp_path)
    target = TARGETS["agents"]
    install(pack, target, opts)
    old_unit = installed_root(entry_path(target, opts))
    receipt_before = manifest.manifest_path(opts.home).read_bytes()
    (pack.skills_dir.parent / "leaves/signal/SKILL.md").write_text(
        "# Corrected signal\n"
    )
    opts.dry_run = True
    install(pack, target, opts)
    assert manifest.manifest_path(opts.home).read_bytes() == receipt_before
    assert old_unit.is_dir()
    opts.dry_run = False
    install(pack, target, opts)
    new_unit = installed_root(entry_path(target, opts))
    assert new_unit != old_unit and not old_unit.exists()
    assert (new_unit / "leaves/signal/SKILL.md").read_text() == "# Corrected signal\n"


def test_takeover_across_runtime_ids_at_the_same_destination(tmp_path):
    repo = tmp_path / "repo"
    first = make_pack(repo)
    second = make_pack(repo, "marine")
    opts = opts_for(tmp_path, copy=True)
    agents = TARGETS["agents"]
    opts.dest_override = agents.dest(opts)
    generic = generic_dest_target()
    install(first, agents, opts)
    with pytest.raises(FileExistsError):
        install(second, generic, opts)
    opts.force = True
    install(second, generic, opts)
    unit = installed_root(entry_path(generic, opts))
    uninstall(first.slug, agents, opts)
    assert unit.is_dir() and entry_path(generic, opts).is_file()
    uninstall(second.slug, generic, opts)
    assert not list(generic.dest(opts).iterdir())


def test_retained_entry_takeover_drops_the_displaced_cleanup_claim(tmp_path, capsys):
    repo = tmp_path / "repo"
    first = make_pack(repo)
    second = make_pack(repo, "marine")
    opts = opts_for(tmp_path, copy=True)
    target = TARGETS["agents"]
    install(first, target, opts)
    entry = entry_path(target, opts)
    entry.write_text(entry.read_text() + "\nUser annotation.\n")
    make_pack(repo, version="2", entry="new-router")
    shutil.rmtree(first.skills_dir / "_router")
    install(resolve_pack(repo, first.slug), target, opts)
    opts.force = True
    install(second, target, opts)
    unit = installed_root(entry_path(target, opts))
    uninstall(first.slug, target, opts)
    assert unit.is_dir() and entry_path(target, opts).is_file()
    assert manifest.get(opts.home, first.slug, target.id) is None
    uninstall(second.slug, target, opts)
    assert not list(target.dest(opts).iterdir())


def test_destination_cannot_be_nested_inside_its_source_snapshot(tmp_path):
    pack = make_pack(tmp_path / "repo")
    opts = opts_for(tmp_path, dest_override=pack.skills_dir.parent / "installed")
    with pytest.raises(ValueError):
        install(pack, generic_dest_target(), opts)
    assert not opts.dest_override.exists()


def test_same_snapshot_reinstall_reports_corrupt_stale_entries(tmp_path, capsys):
    pack = make_pack(tmp_path / "repo")
    opts = opts_for(tmp_path)
    target = TARGETS["agents"]
    install(pack, target, opts)
    data = manifest.load(opts.home)
    data[pack.slug][target.id]["entries"].append("../neighbour")
    manifest.save(opts.home, data)
    install(pack, target, opts)
    assert "../neighbour" in capsys.readouterr().err


def test_repository_root_pack_retains_its_complete_assets(tmp_path):
    repo = tmp_path / "repo"
    pack = make_pack(repo)
    for child in list(pack.skills_dir.parent.iterdir()):
        child.rename(repo / child.name)
    marketplace = repo / ".claude-plugin/marketplace.json"
    data = json.loads(marketplace.read_text())
    data["plugins"][0]["source"] = "."
    marketplace.write_text(json.dumps(data))
    opts = opts_for(tmp_path)
    pack = resolve_pack(repo, pack.slug)
    install(pack, TARGETS["agents"], opts)
    unit = installed_root(entry_path(TARGETS["agents"], opts))
    assert (
        json.loads(run_asset(unit, "bin/search_skills.py", opts.home, opts.home))[0][
            "pack"
        ]
        == pack.slug
    )


def test_missing_unit_never_prunes_an_unowned_empty_parent(tmp_path):
    pack = make_pack(tmp_path / "repo")
    opts = opts_for(tmp_path)
    target = TARGETS["agents"]
    install(pack, target, opts)
    neighbour = opts.home / "neighbour/.asbb-units"
    neighbour.mkdir(parents=True)
    data = manifest.load(opts.home)
    data[pack.slug][target.id].update(dest_root=str(neighbour.parent), entries=[])
    manifest.save(opts.home, data)
    uninstall(pack.slug, target, opts)
    assert neighbour.is_dir()


def test_replaced_special_file_is_reported_without_opening_it(tmp_path):
    pack = make_pack(tmp_path / "repo")
    opts = opts_for(tmp_path, copy=True)
    target = TARGETS["agents"]
    install(pack, target, opts)
    replacement = target.dest(opts) / "_router"
    shutil.rmtree(replacement)
    os.mkfifo(replacement)
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "asb_skill_collections.asbb_cli",
            "uninstall",
            pack.slug,
            "--runtime",
            target.id,
        ],
        cwd=opts.home,
        env={
            "HOME": str(opts.home),
            "PATH": "/usr/bin:/bin",
            "PYTHONPATH": str(Path(__file__).resolve().parents[1]),
            "PYTHONDONTWRITEBYTECODE": "1",
        },
        text=True,
        capture_output=True,
        timeout=3,
        check=True,
    )
    assert replacement.exists() and "skipped" in result.stderr
