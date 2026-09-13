"""An install must refuse plans whose destinations collide, before writing."""

import json
from dataclasses import replace

import pytest

from asb_skill_collections.asbb.installer import install
from asb_skill_collections.asbb.repo import resolve_pack
from asb_skill_collections.asbb.targets import (
    InstallOpts,
    generic_dest_target,
    get_target,
)
from asb_skill_collections.asbb_cli import main
from tests.test_asbb_install import make_repo


def _rules_target(dest, filename):
    return replace(get_target("cline"), dest=lambda o: dest, filename=filename)


@pytest.mark.parametrize(
    "filename",
    [
        pytest.param(lambda name: "same.md", id="duplicate"),
        pytest.param(
            lambda name: "rules" if name == "alpha" else "rules/beta.md", id="nested"
        ),
        pytest.param(
            lambda name: "rules/alpha.md" if name == "alpha" else "rules", id="reversed"
        ),
    ],
)
def test_entries_sharing_a_destination_are_refused(tmp_path, filename):
    repo = make_repo(tmp_path / "repo", skills=("alpha", "beta"))
    dest = tmp_path / "dest"
    opts = InstallOpts(
        home=tmp_path / "home", project=tmp_path, copy=True, dest_override=dest
    )
    with pytest.raises(ValueError, match="overlaps the destination"):
        install(resolve_pack(repo, "demo-pack"), _rules_target(dest, filename), opts)
    assert not dest.exists()
    assert not opts.home.exists()


def test_distinct_destinations_still_install(tmp_path):
    repo = make_repo(tmp_path / "repo", skills=("alpha", "beta"))
    dest = tmp_path / "dest"
    opts = InstallOpts(
        home=tmp_path / "home", project=tmp_path, copy=True, dest_override=dest
    )
    target = _rules_target(dest, lambda name: f"{name}.md")
    assert sorted(install(resolve_pack(repo, "demo-pack"), target, opts)) == [
        "alpha.md",
        "beta.md",
    ]
    assert (dest / "alpha.md").is_file() and (dest / "beta.md").is_file()


@pytest.mark.parametrize("placement", ["same", "descendant", "ancestor"])
def test_destination_overlapping_its_source_is_refused(tmp_path, placement):
    repo = make_repo(tmp_path / "repo", skills=("alpha-skill",))
    pack = resolve_pack(repo, "demo-pack")
    source = pack.source_dir
    dest = {
        "same": source,
        "descendant": source / "nested-destination",
        "ancestor": source.parent,
    }[placement]
    original = (pack.skills_dir / "alpha-skill" / "SKILL.md").read_bytes()
    opts = InstallOpts(
        home=tmp_path / "home", project=tmp_path, copy=True, dest_override=dest
    )
    with pytest.raises(ValueError, match="source pack"):
        install(pack, generic_dest_target(), opts)
    assert (pack.skills_dir / "alpha-skill" / "SKILL.md").read_bytes() == original
    assert not (dest / ".asbb-units").exists()
    assert not opts.home.exists()


def test_cli_reports_an_unsafe_marketplace_source_without_a_traceback(tmp_path, capsys):
    repo = make_repo(tmp_path / "repo")
    outside = tmp_path / "private-unit"
    (outside / "skills" / "secret").mkdir(parents=True)
    (outside / "skills" / "secret" / "SKILL.md").write_text("private procedure")
    (repo / ".claude-plugin" / "marketplace.json").write_text(
        json.dumps({"plugins": [{"name": "demo-pack", "source": "../private-unit"}]})
    )
    assert (
        main(
            [
                "install",
                "demo-pack",
                "--repo",
                str(repo),
                "--dest",
                str(tmp_path / "dest"),
                "--home",
                str(tmp_path / "home"),
            ]
        )
        == 1
    )
    assert "error:" in capsys.readouterr().err
    assert not (tmp_path / "dest").exists()
