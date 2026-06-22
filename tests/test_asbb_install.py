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
