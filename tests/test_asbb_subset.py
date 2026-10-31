"""`asbb install` with a selection: a chosen set of skills installed as a pack.

The fixture is a miniature router-shaped collection in an unrelated domain, so
nothing here depends on which collection the repository ships. The last test
checks the real tree: a selection of a declared pack's own members derives that
pack, file for file.
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

import pytest
import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from asb_skill_collections.asbb import manifest, subset  # noqa: E402
from asb_skill_collections.asbb_cli import main  # noqa: E402
from scripts import build_packs  # noqa: E402
from scripts.stamp_skill_license import stamp_skill  # noqa: E402

DOMAIN = "astronomy"
VERSION = 3
COLLECTION = f"{DOMAIN}/v{VERSION}"
SKILLS = {
    "stellar-photometry": ("measure stellar brightness in survey images", "open"),
    "radio-interferometry": ("calibrate radio interferometer visibilities", "noncommercial"),
    "spectral-fitting": ("fit stellar spectra with templates", "open"),
    "catalogue-crossmatch": ("crossmatch source catalogues by position", "restricted"),
}


def _write_leaf(collection: pathlib.Path, slug: str, description: str, tier: str):
    path = collection / "leaves" / slug / "SKILL.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    frontmatter = {
        "name": slug,
        "description": f"Use when you need to {description}.",
        "license": "CC-BY-4.0",
        "metadata": {"license_tier": tier, "tools": ["skytool"]},
        "derived_from": [f"10.1234/{slug}"],
        "evidence_spans": ["a verbatim line"],
    }
    path.write_text(
        "---\n" + yaml.safe_dump(frontmatter, sort_keys=False) + "---\n\n# " + slug + "\n",
        encoding="utf-8",
    )
    stamp_skill(path, tier)


def _repository(root: pathlib.Path) -> pathlib.Path:
    """A checkout with one marketplace pack and one router-shaped collection."""
    collection = root / "collections" / DOMAIN / f"v{VERSION}"
    for slug, (description, tier) in SKILLS.items():
        _write_leaf(collection, slug, description, tier)
    index = [
        {
            "slug": slug,
            "name": slug,
            "description": f"Use when you need to {description}.",
            "tools": ["skytool"],
            "techniques": ["optical"],
            "license_tier": tier,
        }
        for slug, (description, tier) in sorted(SKILLS.items())
    ]
    (collection / "skills_index.json").write_text(json.dumps(index, indent=1), encoding="utf-8")
    bundle = {
        "collection": DOMAIN,
        "version": VERSION,
        "skills": {slug: {"dois": [f"10.1234/{slug}"]} for slug in sorted(SKILLS)},
    }
    (collection / "kb_bundle.json").write_text(json.dumps(bundle, indent=2), encoding="utf-8")
    descriptor = collection / ".claude-plugin" / "plugin.json"
    descriptor.parent.mkdir(parents=True)
    descriptor.write_text(
        json.dumps({"name": DOMAIN, "description": "ASB Astronomy. Test corpus.",
                    "version": "0.3.0", "license": "CC-BY-4.0"}),
        encoding="utf-8",
    )
    marketplace = root / ".claude-plugin" / "marketplace.json"
    marketplace.parent.mkdir(parents=True)
    marketplace.write_text(
        json.dumps({"name": "demo", "plugins": [
            {"name": DOMAIN, "source": f"./collections/{DOMAIN}/v{VERSION}"},
        ]}),
        encoding="utf-8",
    )
    return root


@pytest.fixture
def repo(tmp_path):
    return _repository(tmp_path / "repo")


def _install(repo, home, *selection):
    return main(["install", *selection, "--collection", COLLECTION, "--runtime", "agents",
                 "--repo", str(repo), "--home", str(home)])


def _only_record(home):
    ((name, runtimes),) = manifest.load(home).items()
    return name, runtimes["agents"]


def test_a_selection_installs_a_pack_shaped_unit(repo, tmp_path):
    home = tmp_path / "home"

    assert _install(repo, home, "--skills", "stellar-photometry,spectral-fitting") == 0

    name, record = _only_record(home)
    unit = pathlib.Path(record["dest_root"]) / record["unit"]
    chosen = ["spectral-fitting", "stellar-photometry"]
    assert sorted(path.name for path in (unit / "leaves").iterdir()) == chosen
    for slug in chosen:
        source = repo / "collections" / DOMAIN / f"v{VERSION}" / "leaves" / slug / "SKILL.md"
        assert (unit / "leaves" / slug / "SKILL.md").read_bytes() == source.read_bytes()
    index = json.loads((unit / "skills_index.json").read_text(encoding="utf-8"))
    assert sorted(row["slug"] for row in index) == chosen
    bundle = json.loads((unit / "kb_bundle.json").read_text(encoding="utf-8"))
    assert sorted(bundle["skills"]) == chosen
    assert (unit / "bin" / "search_skills.py").is_file()
    assert (unit / "bin" / "perspicacite_kb_bind.py").is_file()
    assert record["entries"] == ["_router"]
    router = (home / ".agents" / "skills" / "_router" / "SKILL.md").read_text(encoding="utf-8")
    assert f"name: {name}-router" in router
    assert "**2 evidence-grounded skills**" in router


def test_the_cli_reports_each_skill_with_its_licence_tier(repo, tmp_path, capsys):
    assert _install(repo, tmp_path / "home", "--skills",
                    "radio-interferometry,catalogue-crossmatch") == 0

    out = capsys.readouterr().out
    assert re.search(r"radio-interferometry\s+noncommercial", out)
    assert re.search(r"catalogue-crossmatch\s+restricted", out)
    assert "asbb uninstall" in out


def test_the_default_name_depends_on_the_set_not_its_order():
    collection_dir = pathlib.Path("collections") / DOMAIN / f"v{VERSION}"

    forward = subset.default_name(collection_dir, ["a", "b"])

    assert re.fullmatch(rf"{DOMAIN}-subset-[0-9a-f]{{8}}", forward)
    assert subset.default_name(collection_dir, ["b", "a", "a"]) == forward
    assert subset.default_name(collection_dir, ["a", "c"]) != forward


def test_a_skills_file_reads_one_slug_per_line_and_skips_comments(repo, tmp_path):
    listing = tmp_path / "chosen.txt"
    listing.write_text(
        "# my reduction set\nstellar-photometry\n\n  catalogue-crossmatch  # by position\n",
        encoding="utf-8",
    )
    home = tmp_path / "home"

    assert _install(repo, home, "--skills-file", str(listing), "--name", "my-set") == 0

    name, record = _only_record(home)
    unit = pathlib.Path(record["dest_root"]) / record["unit"]
    assert name == "my-set"
    assert sorted(path.name for path in (unit / "leaves").iterdir()) == [
        "catalogue-crossmatch", "stellar-photometry"
    ]


def test_a_query_selects_what_search_ranks_first(repo, tmp_path, capsys):
    assert main(["search", "stellar", "--collection", COLLECTION, "--k", "2",
                 "--repo", str(repo)]) == 0
    ranked = [hit["slug"] for hit in json.loads(capsys.readouterr().out)["results"]]
    home = tmp_path / "home"

    assert _install(repo, home, "--query", "stellar", "--top", "2") == 0

    _, record = _only_record(home)
    unit = pathlib.Path(record["dest_root"]) / record["unit"]
    index = json.loads((unit / "skills_index.json").read_text(encoding="utf-8"))
    assert len(ranked) == 2
    assert sorted(row["slug"] for row in index) == sorted(ranked)


@pytest.mark.parametrize(
    ("selection", "message"),
    (
        (("--skills", "stellar-photometry,no-such-skill,nor-this"),
         "2 slug(s) not in the collection index: no-such-skill, nor-this"),
        (("--skills", ","), "the selection is empty"),
        (("--query", "zzzz-matches-nothing"), "the selection is empty"),
        (("--skills", "stellar-photometry", "--name", DOMAIN), "is a marketplace pack"),
        (("--skills", "stellar-photometry", "--name", "Bad_Name"), "must be lower-case"),
    ),
    ids=("unknown-slugs", "empty-list", "query-without-hits", "pack-name", "malformed-name"),
)
def test_a_selection_that_cannot_be_installed_is_refused(
    repo, tmp_path, capsys, selection, message
):
    home = tmp_path / "home"

    assert _install(repo, home, *selection) == 1

    assert message in capsys.readouterr().err
    assert manifest.load(home) == {}
    assert not (home / ".agents").exists()


def test_a_pack_and_a_selection_together_are_refused(repo, tmp_path, capsys):
    rc = main(["install", DOMAIN, "--skills", "stellar-photometry", "--collection",
               COLLECTION, "--runtime", "agents", "--repo", str(repo),
               "--home", str(tmp_path / "home")])

    assert rc == 1
    assert "not both" in capsys.readouterr().err


def test_a_selection_needs_a_collection(repo, tmp_path, capsys):
    rc = main(["install", "--skills", "stellar-photometry", "--runtime", "agents",
               "--repo", str(repo), "--home", str(tmp_path / "home")])

    assert rc == 1
    assert "--collection" in capsys.readouterr().err


def test_a_dry_run_prints_the_writes_and_writes_nothing(repo, tmp_path, capsys):
    home = tmp_path / "home"

    assert _install(repo, home, "--skills", "stellar-photometry", "--dry-run") == 0

    out = capsys.readouterr().out
    assert "would copy complete unit to" in out
    assert f"would write {home.resolve() / '.agents' / 'skills' / '_router'}" in out
    assert not (home / ".agents").exists()
    assert manifest.load(home) == {}


def test_uninstall_removes_a_selection(repo, tmp_path):
    home = tmp_path / "home"
    assert _install(repo, home, "--skills", "stellar-photometry") == 0
    name, record = _only_record(home)
    unit = pathlib.Path(record["dest_root"]) / record["unit"]

    assert main(["uninstall", name, "--runtime", "agents", "--home", str(home)]) == 0

    assert not (home / ".agents" / "skills" / "_router").exists()
    assert not unit.exists()
    assert manifest.load(home) == {}


def test_a_selection_of_a_packs_members_derives_that_pack(tmp_path):
    """On the shipped tree: the subset route and the pack build agree.

    The smallest declared pack keeps this quick; any pack would do. Only the two
    files that name the unit differ: its plugin.json and its router.
    """
    declared = []
    for pack_map in build_packs.discover_maps(REPO_ROOT):
        index = build_packs.read_index(pack_map.collection_dir / build_packs.INDEX_FILENAME)
        declared += [(pack_map, spec, spec.members(index)) for spec in pack_map.packs]
    pack_map, spec, members = min(declared, key=lambda found: len(found[2]))
    selection = subset.Selection(
        REPO_ROOT, pack_map.collection_dir, spec.name, tuple(sorted(members))
    )

    derived = subset.derive(selection, tmp_path).source_dir

    def files(tree):
        return {str(path.relative_to(tree)) for path in tree.rglob("*") if path.is_file()}

    assert files(derived) == files(spec.directory)
    naming = {".claude-plugin/plugin.json", "skills/_router/SKILL.md"}
    differing = sorted(
        rel for rel in files(derived) - naming
        if (derived / rel).read_bytes() != (spec.directory / rel).read_bytes()
    )
    assert differing == []
