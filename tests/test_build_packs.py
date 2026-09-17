"""The pack generator: the declared map, the membership rule, and idempotence.

Every case here is built on a miniature collection rather than the shipped one,
so the contract is stated in terms any domain could satisfy — the packs this
repository happens to ship are a consequence of the rule, not its definition.
The real tree is checked once, at the end, against the same rule.
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import shutil
import sys

import pytest
import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts import build_packs  # noqa: E402
from scripts.stamp_skill_license import stamp_skill  # noqa: E402

# Unrelated domains and techniques: the rule is `techniques ∋ tag`, and nothing
# in the generator may depend on which domain or which tag it is applied to.
DOMAIN = "astronomy"
COLLECTION_VERSION = 3


def _write_leaf(collection: pathlib.Path, slug: str, tier: str = "open") -> None:
    """One canonical collection leaf: front matter, a tier, and its own banner."""
    path = collection / "leaves" / slug / "SKILL.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    frontmatter = {
        "name": slug,
        "description": f"Use when a task needs {slug}.",
        "license": "CC-BY-4.0",
        "metadata": {
            "license_tier": tier,
            "provenance_tier": "literature",
            "grounding_tier": "paper",
        },
        "schema_version": "0.2.0",
    }
    path.write_text(
        "---\n" + yaml.safe_dump(frontmatter, sort_keys=False) + "---\n\n# " + slug + "\n",
        encoding="utf-8",
    )
    # The shipped collection leaves are stamped, so a byte copy of one arrives
    # already stamped. Stamping the fixture makes it the same kind of source.
    stamp_skill(path, tier)


def _collection(root: pathlib.Path, membership: dict[str, list[str]]) -> pathlib.Path:
    """A router-shaped collection whose index carries the techniques of each leaf."""
    collection = root / "collections" / DOMAIN / f"v{COLLECTION_VERSION}"
    for slug in membership:
        _write_leaf(collection, slug)
    index = [
        {
            "slug": slug,
            "license_tier": "open",
            "provenance_tier": "literature",
            "techniques": techniques,
        }
        for slug, techniques in sorted(membership.items())
    ]
    (collection / "skills_index.json").write_text(
        json.dumps(index, indent=1, ensure_ascii=False), encoding="utf-8"
    )
    bundle = {
        "collection": DOMAIN,
        "version": COLLECTION_VERSION,
        "skills": {slug: {"dois": [f"10.1234/{slug}"]} for slug in sorted(membership)},
    }
    (collection / "kb_bundle.json").write_text(
        json.dumps(bundle, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return collection


def _write_map(root: pathlib.Path, entries: list[dict], **overrides) -> pathlib.Path:
    document = {
        "schema": build_packs.SCHEMA,
        "collection": DOMAIN,
        "version": COLLECTION_VERSION,
        "source": f"collections/{DOMAIN}/v{COLLECTION_VERSION}",
        "packs": entries,
    }
    document.update(overrides)
    path = root / "packs" / DOMAIN / build_packs.MAP_FILENAME
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")
    return path


@pytest.fixture
def repository(tmp_path):
    """A collection of four leaves and one declared pack selecting two of them."""
    root = tmp_path / "repository"
    _collection(
        root,
        {
            "stellar-photometry": ["optical", "survey"],
            "radio-interferometry": ["radio"],
            "spectral-fitting": ["optical"],
            "catalogue-crossmatch": [],
        },
    )
    _write_map(root, [{"dir": "optical", "tag": "optical"}])
    return root


def _manifest(tree: pathlib.Path) -> dict[str, str]:
    """Every file under a tree, by path, by content — the idempotence witness."""
    return {
        str(path.relative_to(tree)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(tree.rglob("*"))
        if path.is_file()
    }


def _only_map(root: pathlib.Path) -> build_packs.PackMap:
    (pack_map,) = build_packs.discover_maps(root)
    return pack_map


# --------------------------------------------------------------------------- #
# The map is data, and it is validated.                                         #
# --------------------------------------------------------------------------- #


def test_declared_map_resolves_its_collection_and_pack_directories(repository):
    pack_map = _only_map(repository)

    assert pack_map.collection_dir == (
        repository / "collections" / DOMAIN / f"v{COLLECTION_VERSION}"
    ).resolve()
    assert [(spec.name, spec.tag) for spec in pack_map.packs] == [("optical", "optical")]
    assert pack_map.packs[0].directory == repository / "packs" / DOMAIN / "optical"


def test_a_tree_without_a_map_declares_no_packs(tmp_path):
    """Discovery is by declaration: an undeclared pack tree yields nothing."""
    root = tmp_path / "repository"
    _collection(root, {"stellar-photometry": ["optical"]})
    (root / "packs" / DOMAIN / "optical" / "leaves").mkdir(parents=True)

    assert build_packs.discover_maps(root) == []


@pytest.mark.parametrize(
    ("mutation", "message"),
    (
        ({"schema": "asb-pack-map/99"}, "schema is not"),
        ({"source": ""}, "no source collection declared"),
        ({"source": "../elsewhere"}, "is not a directory inside"),
        ({"source": "collections/astronomy/v9"}, "is not a directory inside"),
        ({"packs": []}, "packs must be a non-empty list"),
        ({"packs": {"dir": "optical"}}, "packs must be a non-empty list"),
    ),
    ids=(
        "wrong-schema",
        "no-source",
        "source-escapes-root",
        "source-absent",
        "no-packs",
        "packs-not-a-list",
    ),
)
def test_a_map_that_cannot_be_trusted_is_refused(tmp_path, mutation, message):
    root = tmp_path / "repository"
    _collection(root, {"stellar-photometry": ["optical"]})
    path = _write_map(root, [{"dir": "optical", "tag": "optical"}], **mutation)

    with pytest.raises(ValueError, match=message):
        build_packs.load_map(path, root)


@pytest.mark.parametrize(
    ("packs", "message"),
    (
        ([{"dir": "../escape", "tag": "optical"}], "is not a single directory name"),
        ([{"dir": "..", "tag": "optical"}], "is not a single directory name"),
        ([{"dir": "", "tag": "optical"}], "is not a single directory name"),
        ([{"tag": "optical"}], "is not a single directory name"),
        ([{"dir": "optical"}], "declares no technique tag"),
        ([{"dir": "optical", "tag": "  "}], "declares no technique tag"),
        (
            [{"dir": "optical", "tag": "optical"}, {"dir": "optical", "tag": "radio"}],
            "declared twice",
        ),
    ),
    ids=(
        "dir-escapes",
        "dir-is-parent",
        "dir-empty",
        "dir-absent",
        "tag-absent",
        "tag-blank",
        "duplicate-dir",
    ),
)
def test_a_pack_entry_that_cannot_be_trusted_is_refused(tmp_path, packs, message):
    root = tmp_path / "repository"
    _collection(root, {"stellar-photometry": ["optical"]})
    path = _write_map(root, packs)

    with pytest.raises(ValueError, match=message):
        build_packs.load_map(path, root)


# --------------------------------------------------------------------------- #
# The membership rule.                                                          #
# --------------------------------------------------------------------------- #


def test_membership_is_exactly_the_declared_technique_tag():
    index = [
        {"slug": "both", "techniques": ["optical", "radio"]},
        {"slug": "optical-only", "techniques": ["optical"]},
        {"slug": "radio-only", "techniques": ["radio"]},
        {"slug": "untagged", "techniques": []},
        {"slug": "no-key"},
        {"slug": "null-techniques", "techniques": None},
        {"techniques": ["optical"]},
        "not-a-row",
    ]

    assert build_packs.selected_slugs(index, "optical") == {"both", "optical-only"}
    assert build_packs.selected_slugs(index, "radio") == {"both", "radio-only"}
    assert build_packs.selected_slugs(index, "infrared") == set()


def test_the_tag_is_matched_whole_and_is_not_the_directory_name(tmp_path):
    """`ms-generic` selects `mass-spectrometry`: the tag is declared, not derived."""
    root = tmp_path / "repository"
    _collection(root, {"a": ["optical"], "b": ["optical-polarimetry"]})
    _write_map(root, [{"dir": "generic", "tag": "optical"}])

    build_packs.build_map(_only_map(root))

    leaves = root / "packs" / DOMAIN / "generic" / "leaves"
    assert sorted(path.name for path in leaves.iterdir()) == ["a"]


# --------------------------------------------------------------------------- #
# The build.                                                                    #
# --------------------------------------------------------------------------- #


def test_a_pack_built_from_scratch_is_the_collection_leaf_byte_for_byte(repository):
    pack_map = _only_map(repository)

    (build,) = build_packs.build_map(pack_map)

    assert build.selected == 2
    assert build.added == ["spectral-fitting", "stellar-photometry"]
    assert build.removed == []
    assert build.restamped == []
    pack = repository / "packs" / DOMAIN / "optical"
    for slug in build.added:
        assert (pack / "leaves" / slug / "SKILL.md").read_bytes() == (
            pack_map.collection_dir / "leaves" / slug / "SKILL.md"
        ).read_bytes()


def test_a_derived_pack_takes_its_collections_layout_not_the_legacy_one(repository):
    """An empty pack has no shape of its own; publishing leaves into `skills/`
    would inject every one of them into the session prompt."""
    build_packs.build_map(_only_map(repository))

    pack = repository / "packs" / DOMAIN / "optical"
    assert (pack / "leaves").is_dir()
    assert not (pack / "skills").exists()


def test_both_indexes_are_the_collections_rows_filtered_to_the_selection(repository):
    pack_map = _only_map(repository)

    build_packs.build_map(pack_map)

    pack = repository / "packs" / DOMAIN / "optical"
    index = json.loads((pack / "skills_index.json").read_text(encoding="utf-8"))
    collection_rows = {
        row["slug"]: row
        for row in json.loads(
            (pack_map.collection_dir / "skills_index.json").read_text(encoding="utf-8")
        )
    }
    assert [row["slug"] for row in index] == ["spectral-fitting", "stellar-photometry"]
    # Whole rows, not a chosen subset of their fields: the pack indexes lost
    # provenance_tier and grounding_tier exactly by being rebuilt field by field.
    assert all(row == collection_rows[row["slug"]] for row in index)
    bundle = json.loads((pack / "kb_bundle.json").read_text(encoding="utf-8"))
    assert set(bundle["skills"]) == {"spectral-fitting", "stellar-photometry"}
    assert bundle["collection"] == DOMAIN


def test_a_leaf_added_to_the_collection_reaches_the_pack(repository):
    pack_map = _only_map(repository)
    build_packs.build_map(pack_map)
    _write_leaf(pack_map.collection_dir, "coronagraphy")
    index = json.loads(
        (pack_map.collection_dir / "skills_index.json").read_text(encoding="utf-8")
    )
    index.append({"slug": "coronagraphy", "techniques": ["optical"]})
    (pack_map.collection_dir / "skills_index.json").write_text(
        json.dumps(index, indent=1, ensure_ascii=False), encoding="utf-8"
    )

    (build,) = build_packs.build_map(pack_map)

    assert build.added == ["coronagraphy"]
    assert (
        repository / "packs" / DOMAIN / "optical/leaves/coronagraphy/SKILL.md"
    ).is_file()


def test_a_leaf_the_rule_no_longer_selects_is_removed(repository):
    pack_map = _only_map(repository)
    build_packs.build_map(pack_map)
    stray = repository / "packs" / DOMAIN / "optical/leaves/radio-interferometry"
    stray.mkdir(parents=True)
    (stray / "SKILL.md").write_text("---\nname: radio\n---\n", encoding="utf-8")

    (build,) = build_packs.build_map(pack_map)

    assert build.removed == ["radio-interferometry"]
    assert not stray.exists()


def test_a_copy_edited_in_place_is_restored_from_the_collection(repository):
    pack_map = _only_map(repository)
    build_packs.build_map(pack_map)
    copy = repository / "packs" / DOMAIN / "optical/leaves/spectral-fitting/SKILL.md"
    copy.write_text(copy.read_text(encoding="utf-8") + "\nlocal edit\n", encoding="utf-8")

    (build,) = build_packs.build_map(pack_map)

    assert build.refreshed == ["spectral-fitting"]
    assert copy.read_bytes() == (
        pack_map.collection_dir / "leaves/spectral-fitting/SKILL.md"
    ).read_bytes()


def test_the_index_keeps_the_destinations_own_json_shape(repository):
    """`skills_index.json` ships at indent 1 and `kb_bundle.json` at indent 2;
    a rebuild that normalised them would rewrite every pack on every run."""
    pack_map = _only_map(repository)
    build_packs.build_map(pack_map)
    pack = repository / "packs" / DOMAIN / "optical"

    index = (pack / "skills_index.json").read_text(encoding="utf-8")
    bundle = (pack / "kb_bundle.json").read_text(encoding="utf-8")
    assert index.startswith("[\n {\n")
    assert '\n  "skills"' in bundle
    assert bundle.endswith("\n")


def test_a_dry_run_reports_the_same_work_and_writes_nothing(repository):
    pack_map = _only_map(repository)
    before = _manifest(repository)

    (build,) = build_packs.build_map(pack_map, dry_run=True)

    assert build.added == ["spectral-fitting", "stellar-photometry"]
    assert build.rewritten == ["skills_index.json", "kb_bundle.json"]
    assert _manifest(repository) == before


def test_the_build_does_not_touch_what_it_does_not_own(repository):
    """`bin/`, `commands/`, `skills/` and `.claude-plugin/` are hand-maintained
    or owned by build_grounding_bundle; the generator manages leaves and indexes."""
    pack = repository / "packs" / DOMAIN / "optical"
    owned_elsewhere = {
        "bin/search_skills.py": "# retrieval helper\n",
        "commands/ground.md": "---\ndescription: ground\n---\n",
        "skills/_router/SKILL.md": "---\nname: optical-router\n---\n",
        ".claude-plugin/plugin.json": '{\n  "name": "astronomy-optical"\n}\n',
        "GROUNDING.md": "# Grounding\n",
    }
    for relative, text in owned_elsewhere.items():
        path = pack / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    before = {
        relative: (pack / relative).read_bytes() for relative in owned_elsewhere
    }

    build_packs.build_map(_only_map(repository))

    assert {
        relative: (pack / relative).read_bytes() for relative in owned_elsewhere
    } == before


def test_the_collection_is_never_written_to(repository):
    pack_map = _only_map(repository)
    before = _manifest(pack_map.collection_dir)

    build_packs.build_map(pack_map)

    assert _manifest(pack_map.collection_dir) == before


def test_an_index_row_with_no_leaf_on_disk_stops_the_build(repository):
    pack_map = _only_map(repository)
    index = json.loads(
        (pack_map.collection_dir / "skills_index.json").read_text(encoding="utf-8")
    )
    index.append({"slug": "never-written", "techniques": ["optical"]})
    (pack_map.collection_dir / "skills_index.json").write_text(
        json.dumps(index, indent=1, ensure_ascii=False), encoding="utf-8"
    )

    with pytest.raises(ValueError, match="never-written"):
        build_packs.build_map(pack_map)


# --------------------------------------------------------------------------- #
# Idempotence.                                                                  #
# --------------------------------------------------------------------------- #


def test_building_twice_changes_nothing_the_second_time(repository):
    pack_map = _only_map(repository)

    build_packs.build_map(pack_map)
    first = _manifest(repository)
    (second,) = build_packs.build_map(pack_map)

    assert second.changed is False
    assert second.as_dict() == {
        "pack": "optical",
        "tag": "optical",
        "selected": 2,
        "added": [],
        "removed": [],
        "refreshed": [],
        "rewritten": [],
        "restamped": [],
    }
    assert _manifest(repository) == first


def test_a_built_tree_passes_the_check_that_a_drifted_one_fails(repository):
    pack_map = _only_map(repository)

    assert build_packs.check_map(pack_map)  # nothing built yet: two leaves missing
    build_packs.build_map(pack_map)
    assert build_packs.check_map(pack_map) == {}


def test_stamping_a_byte_copy_is_an_assertion_and_not_a_repair(repository):
    """A copy arrives stamped because its source is. `restamped` is therefore
    empty on a healthy build, and names the source leaves whose own tier and
    banner disagree when it is not."""
    pack_map = _only_map(repository)
    (build,) = build_packs.build_map(pack_map)
    assert build.restamped == []

    source = pack_map.collection_dir / "leaves/spectral-fitting/SKILL.md"
    source.write_text(
        source.read_text(encoding="utf-8").replace(
            "license_tier: open", "license_tier: noncommercial"
        ),
        encoding="utf-8",
    )

    (rebuilt,) = build_packs.build_map(pack_map)

    assert rebuilt.refreshed == ["spectral-fitting"]
    assert rebuilt.restamped == ["leaves/spectral-fitting/SKILL.md"]


# --------------------------------------------------------------------------- #
# Divergence, the three kinds.                                                  #
# --------------------------------------------------------------------------- #


def test_a_selected_leaf_absent_from_the_pack_is_a_divergence(repository):
    pack_map = _only_map(repository)
    build_packs.build_map(pack_map)
    shutil.rmtree(repository / "packs" / DOMAIN / "optical/leaves/spectral-fitting")

    (found,) = build_packs.pack_divergences(pack_map.packs[0], pack_map.collection_dir)

    assert found.slug == "spectral-fitting"
    assert found.where == "leaves/spectral-fitting/SKILL.md"
    assert "absent from the pack" in found.reason


def test_a_leaf_the_rule_does_not_select_is_a_divergence(repository):
    pack_map = _only_map(repository)
    build_packs.build_map(pack_map)
    intruder = repository / "packs" / DOMAIN / "optical/leaves/radio-interferometry"
    intruder.mkdir(parents=True)
    (intruder / "SKILL.md").write_text("---\nname: radio\n---\n", encoding="utf-8")

    (found,) = build_packs.pack_divergences(pack_map.packs[0], pack_map.collection_dir)

    assert found.slug == "radio-interferometry"
    assert "not selected by techniques" in found.reason


def test_a_front_matter_key_dropped_from_the_copy_is_named(repository):
    """The defect that hid: 4,949 copies lost three metadata keys and stayed
    well-formed, self-consistent, and green under every index check."""
    pack_map = _only_map(repository)
    build_packs.build_map(pack_map)
    copy = repository / "packs" / DOMAIN / "optical/leaves/stellar-photometry/SKILL.md"
    copy.write_text(
        copy.read_text(encoding="utf-8").replace("  provenance_tier: literature\n", ""),
        encoding="utf-8",
    )

    (found,) = build_packs.pack_divergences(pack_map.packs[0], pack_map.collection_dir)

    assert found.slug == "stellar-photometry"
    assert found.reason == (
        "front matter absent from the copy: metadata.provenance_tier"
    )


def test_a_front_matter_value_that_drifted_is_named(repository):
    pack_map = _only_map(repository)
    build_packs.build_map(pack_map)
    copy = repository / "packs" / DOMAIN / "optical/leaves/stellar-photometry/SKILL.md"
    copy.write_text(
        copy.read_text(encoding="utf-8").replace(
            "license: CC-BY-4.0", "license: CC-BY-4.0-stale"
        ),
        encoding="utf-8",
    )

    (found,) = build_packs.pack_divergences(pack_map.packs[0], pack_map.collection_dir)

    assert found.reason == "front matter differs from the collection: license"


def test_a_body_that_drifted_is_named(repository):
    pack_map = _only_map(repository)
    build_packs.build_map(pack_map)
    copy = repository / "packs" / DOMAIN / "optical/leaves/stellar-photometry/SKILL.md"
    copy.write_text(
        copy.read_text(encoding="utf-8") + "\nan extra paragraph\n", encoding="utf-8"
    )

    (found,) = build_packs.pack_divergences(pack_map.packs[0], pack_map.collection_dir)

    assert found.reason == "body differs from the collection"


# --------------------------------------------------------------------------- #
# The command line.                                                             #
# --------------------------------------------------------------------------- #


def test_check_exits_nonzero_on_a_drifted_tree_and_writes_nothing(repository, capsys):
    before = _manifest(repository)

    code = build_packs.main(["--root", str(repository), "--check"])

    output = capsys.readouterr().out
    assert code == 1
    assert "FAIL: 1 of 1 declared pack(s) differ from their collection." in output
    assert "spectral-fitting" in output
    assert _manifest(repository) == before


def test_check_exits_zero_on_a_built_tree(repository, capsys):
    build_packs.main(["--root", str(repository)])
    capsys.readouterr()

    code = build_packs.main(["--root", str(repository), "--check"])

    assert code == 0
    assert "PASS: 0 of 1 declared pack(s)" in capsys.readouterr().out


def test_a_root_declaring_no_map_fails_loudly_rather_than_passing(tmp_path, capsys):
    code = build_packs.main(["--root", str(tmp_path), "--check"])

    assert code == 1
    assert "no pack map matched" in capsys.readouterr().out


# --------------------------------------------------------------------------- #
# The tree this repository actually ships.                                      #
# --------------------------------------------------------------------------- #

SHIPPED = [
    (pack_map, spec)
    for pack_map in build_packs.discover_maps(REPO_ROOT)
    for spec in pack_map.packs
]


@pytest.mark.parametrize(
    ("pack_map", "spec"),
    SHIPPED,
    ids=[str(spec.directory.relative_to(REPO_ROOT)) for _, spec in SHIPPED],
)
def test_every_declared_pack_is_the_view_of_its_collection_it_claims(pack_map, spec):
    found = build_packs.pack_divergences(spec, pack_map.collection_dir)

    assert found == [], "\n".join(str(divergence) for divergence in found[:20])


def test_the_shipped_maps_cover_every_advertised_pack_directory():
    """A pack directory outside the map is a pack nothing re-derives or checks."""
    declared = {spec.directory for _, spec in SHIPPED}
    on_disk = {
        path
        for path in REPO_ROOT.glob("packs/*/*")
        if path.is_dir() and (path / "skills_index.json").is_file()
    }

    assert on_disk == declared
