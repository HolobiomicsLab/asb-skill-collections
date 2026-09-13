"""Regression matrix for shipped-unit index closure and helper containment."""

from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys

import pytest
import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts import release_gate, unit_closure  # noqa: E402


SCIENCE_CASES = (
    ("metabolomics", "metabolite-annotation"),
    ("proteomics", "protein-fold-comparison"),
    ("astronomy", "stellar-photometry"),
    ("climate-science", "climate-model-calibration"),
)
NO_VALUE = object()


@pytest.fixture(params=SCIENCE_CASES, ids=[case[0] for case in SCIENCE_CASES])
def science_case(request):
    """Return unrelated domain/skill names to guard the general contract."""
    return request.param


def _write_skill(
    unit: pathlib.Path,
    relative: str,
    *,
    helper=NO_VALUE,
    role: str | None = None,
    issue_templates=NO_VALUE,
) -> pathlib.Path:
    skill = unit / relative
    skill.parent.mkdir(parents=True, exist_ok=True)
    metadata = {}
    if helper is not NO_VALUE:
        metadata["helper"] = helper
    if role is not None:
        metadata["role"] = role
    if issue_templates is not NO_VALUE:
        metadata["issue_templates"] = issue_templates
    frontmatter = {"name": skill.parent.name}
    if metadata:
        frontmatter["metadata"] = metadata
    body = "---\n" + yaml.safe_dump(frontmatter, sort_keys=False) + "---\n# Skill\n"
    skill.write_text(body, encoding="utf-8")
    return skill


def _write_indexes(
    unit: pathlib.Path,
    index_slugs: list[str],
    kb_slugs: list[str] | None = None,
) -> None:
    unit.mkdir(parents=True, exist_ok=True)
    rows = [{"slug": slug} for slug in index_slugs]
    (unit / "skills_index.json").write_text(json.dumps(rows), encoding="utf-8")
    if kb_slugs is not None:
        bundle = {"skills": {slug: {} for slug in kb_slugs}}
        (unit / "kb_bundle.json").write_text(json.dumps(bundle), encoding="utf-8")


def _router_unit(tmp_path: pathlib.Path, science_case) -> tuple[pathlib.Path, str]:
    domain, slug = science_case
    unit = tmp_path / "collections" / domain / "v9"
    _write_skill(unit, f"leaves/{slug}/SKILL.md")
    _write_indexes(unit, [slug], [slug])
    return unit, slug


def _finding_tuples(findings):
    return [(item.file, item.slug, item.direction) for item in findings]


def test_clean_router_unit_has_exact_closure(tmp_path, science_case):
    unit, slug = _router_unit(tmp_path, science_case)

    closure = unit_closure.inspect_indexes(unit)

    assert closure.has_index is True
    assert closure.indexed == {slug}
    assert closure.on_disk == {slug}
    assert closure.violations == []
    assert unit_closure.check_unit(unit) == []


def test_dangling_skills_index_row_is_reported(tmp_path, science_case):
    unit, slug = _router_unit(tmp_path, science_case)
    ghost = f"{slug}-absent"
    _write_indexes(unit, [slug, ghost], [slug])

    findings = unit_closure.inspect_indexes(unit).violations

    assert _finding_tuples(findings) == [("skills_index.json", ghost, "index-to-disk")]


def test_unindexed_leaf_is_reported(tmp_path, science_case):
    unit, slug = _router_unit(tmp_path, science_case)
    _write_indexes(unit, [], [slug])

    findings = unit_closure.inspect_indexes(unit).violations

    assert _finding_tuples(findings) == [("skills_index.json", slug, "disk-to-index")]


def test_dangling_kb_bundle_key_is_reported(tmp_path, science_case):
    unit, slug = _router_unit(tmp_path, science_case)
    ghost = f"{slug}-kb-only"
    _write_indexes(unit, [slug], [slug, ghost])

    findings = unit_closure.inspect_indexes(unit).violations

    assert _finding_tuples(findings) == [("kb_bundle.json", ghost, "index-to-disk")]


def test_leaf_missing_from_kb_bundle_is_reported(tmp_path, science_case):
    unit, slug = _router_unit(tmp_path, science_case)
    _write_indexes(unit, [slug], [])

    findings = unit_closure.inspect_indexes(unit).violations

    assert _finding_tuples(findings) == [("kb_bundle.json", slug, "disk-to-index")]


def test_meta_and_underscore_leaves_are_excluded(tmp_path, science_case):
    unit, slug = _router_unit(tmp_path, science_case)
    _write_skill(unit, "leaves/_router/SKILL.md")
    _write_skill(unit, "leaves/catalogue-curator/SKILL.md", role="meta")

    closure = unit_closure.inspect_indexes(unit)

    assert closure.on_disk == {slug}
    assert closure.violations == []


def test_only_direct_leaf_children_form_the_index(tmp_path, science_case):
    unit, slug = _router_unit(tmp_path, science_case)
    _write_skill(unit, "leaves/group/nested-skill/SKILL.md")

    closure = unit_closure.inspect_indexes(unit)

    assert closure.on_disk == {slug}
    assert closure.violations == []


def test_indexless_unit_has_no_closure_requirement(tmp_path, science_case):
    domain, slug = science_case
    unit = tmp_path / "collections" / domain / "v1"
    _write_skill(unit, f"leaves/{slug}/SKILL.md")

    closure = unit_closure.inspect_indexes(unit)

    assert closure.has_index is False
    assert closure.violations == []
    assert unit_closure.check_unit(unit) == []


def test_malformed_skills_index_is_loud(tmp_path, science_case):
    unit, _ = _router_unit(tmp_path, science_case)
    (unit / "skills_index.json").write_text("{not json", encoding="utf-8")

    findings = unit_closure.inspect_indexes(unit).violations

    assert any(
        item.file == "skills_index.json" and item.direction == "invalid-index"
        for item in findings
    )


@pytest.mark.parametrize(
    ("filename", "payload"),
    (
        ("skills_index.json", {"skills": {"not": "a list"}}),
        ("skills_index.json", [{"name": "missing-slug"}]),
        ("kb_bundle.json", {"skills": ["not-an-object"]}),
    ),
    ids=("skills-wrong-shape", "skills-row-without-slug", "kb-wrong-shape"),
)
def test_malformed_index_forms_are_loud(tmp_path, filename, payload):
    unit = tmp_path / "unit"
    _write_skill(unit, "leaves/analysis/SKILL.md")
    _write_indexes(unit, ["analysis"], ["analysis"])
    (unit / filename).write_text(json.dumps(payload), encoding="utf-8")

    findings = unit_closure.inspect_indexes(unit).violations

    assert any(
        item.file == filename and item.direction == "invalid-index" for item in findings
    )


def test_discovery_uses_both_default_tree_shapes(tmp_path, science_case):
    domain, _ = science_case
    collection = tmp_path / "collections" / domain / "v7"
    pack = tmp_path / "packs" / domain / "field-method"
    ignored = tmp_path / "archive" / domain / "v7"
    unindexed = tmp_path / "collections" / domain / "v8"
    for unit in (collection, pack, ignored):
        _write_indexes(unit, [])
    unindexed.mkdir(parents=True)

    assert unit_closure.discover_units(tmp_path) == sorted([collection, pack])


def test_present_scalar_helper_passes(tmp_path):
    unit = tmp_path / "unit"
    _write_skill(unit, "skills/entry/SKILL.md", helper="scripts/run.py")
    helper = unit / "scripts/run.py"
    helper.parent.mkdir()
    helper.write_text("print('ok')\n", encoding="utf-8")

    assert unit_closure.check_helpers(unit) == []
    assert unit_closure.check_unit(unit) == []


def test_present_helper_list_passes(tmp_path):
    unit = tmp_path / "unit"
    helpers = ["scripts/prepare.py", "bin/run.sh"]
    _write_skill(unit, "skills/entry/SKILL.md", helper=helpers)
    for relative in helpers:
        helper = unit / relative
        helper.parent.mkdir(parents=True, exist_ok=True)
        helper.write_text("# helper\n", encoding="utf-8")

    assert unit_closure.check_helpers(unit) == []


@pytest.mark.parametrize(
    "skill_relative",
    (
        "leaves/analysis/SKILL.md",
        "skills/advertised/SKILL.md",
        "skills/_router/SKILL.md",
        "workflows/full-pipeline/SKILL.md",
    ),
    ids=("leaf", "advertised", "underscore", "workflow"),
)
def test_missing_helpers_are_checked_in_every_skill_tree(tmp_path, skill_relative):
    unit = tmp_path / "unit"
    _write_skill(unit, skill_relative, helper="scripts/missing.py")

    findings = unit_closure.check_helpers(unit)

    assert len(findings) == 1
    assert _finding_tuples(findings) == [
        (skill_relative, pathlib.Path(skill_relative).parent.name, "helper-to-unit")
    ]
    assert "scripts/missing.py" in findings[0].message


def test_issue_templates_may_point_outside_the_unit(tmp_path):
    unit = tmp_path / "unit"
    outside = tmp_path / ".github/ISSUE_TEMPLATE/report.md"
    outside.parent.mkdir(parents=True)
    outside.write_text("template\n", encoding="utf-8")
    _write_skill(
        unit,
        "skills/contribute/SKILL.md",
        issue_templates=["../.github/ISSUE_TEMPLATE/report.md"],
    )

    assert unit_closure.check_helpers(unit) == []


def test_helper_parent_escape_is_rejected_even_when_target_exists(tmp_path):
    unit = tmp_path / "unit"
    outside = tmp_path / "outside.py"
    outside.write_text("print('outside')\n", encoding="utf-8")
    _write_skill(unit, "skills/entry/SKILL.md", helper="../outside.py")

    findings = unit_closure.check_helpers(unit)

    assert len(findings) == 1
    assert findings[0].direction == "helper-to-unit"
    assert "inside the unit" in findings[0].message


def test_helper_symlink_escape_is_rejected(tmp_path):
    unit = tmp_path / "unit"
    outside = tmp_path / "outside.py"
    outside.write_text("print('outside')\n", encoding="utf-8")
    link = unit / "scripts/linked.py"
    link.parent.mkdir(parents=True)
    link.symlink_to(outside)
    _write_skill(unit, "skills/entry/SKILL.md", helper="scripts/linked.py")

    findings = unit_closure.check_helpers(unit)

    assert len(findings) == 1
    assert findings[0].direction == "helper-to-unit"
    assert "inside the unit" in findings[0].message


@pytest.mark.parametrize(
    "invalid_helper", ("scripts", 17), ids=("directory", "non-string")
)
def test_helper_must_be_a_regular_file_path(tmp_path, invalid_helper):
    unit = tmp_path / "unit"
    (unit / "scripts").mkdir(parents=True)
    _write_skill(unit, "skills/entry/SKILL.md", helper=invalid_helper)

    findings = unit_closure.check_helpers(unit)

    assert len(findings) == 1
    assert findings[0].direction == "helper-to-unit"


def test_cli_fails_loudly_when_no_indexed_units_exist(tmp_path, capsys):
    assert unit_closure.main(["--root", str(tmp_path)]) == 1
    assert "no indexed units matched" in capsys.readouterr().out


def test_cli_fails_on_a_malformed_index(tmp_path, capsys):
    unit = tmp_path / "collections/astronomy/v1"
    _write_skill(unit, "leaves/photometry/SKILL.md")
    _write_indexes(unit, ["photometry"], ["photometry"])
    (unit / "skills_index.json").write_text('{"skills": {}}', encoding="utf-8")

    assert unit_closure.main(["--root", str(tmp_path)]) == 1
    output = capsys.readouterr().out
    assert "invalid-index" in output
    assert "skills_index.json" in output


def _prune_fixture(
    tmp_path: pathlib.Path,
    *,
    parent_state: str = "clean",
) -> tuple[pathlib.Path, pathlib.Path, str, str]:
    root = tmp_path / "repository"
    parent = root / "collections/astronomy/v3"
    pack = root / "packs/astronomy/photometry"
    kept, stale = "stellar-photometry", "obsolete-calibration"
    _write_skill(pack, f"leaves/{kept}/SKILL.md")
    parent.mkdir(parents=True)
    parent_rows = [{"slug": kept}]
    if parent_state == "contains-stale":
        parent_rows.append({"slug": stale})
    if parent_state == "invalid":
        (parent / "skills_index.json").write_text("{not json", encoding="utf-8")
    elif parent_state != "missing":
        (parent / "skills_index.json").write_text(
            json.dumps(parent_rows, indent=1) + "\n", encoding="utf-8"
        )
    pack.mkdir(parents=True, exist_ok=True)
    (pack / "skills_index.json").write_text(
        json.dumps([{"slug": kept}, {"slug": stale}], indent=1) + "\n",
        encoding="utf-8",
    )
    bundle = {
        "collection": "astronomy",
        "version": 3,
        "skills": {kept: {"source": "paper"}, stale: {"source": "paper"}},
    }
    (pack / "kb_bundle.json").write_text(
        json.dumps(bundle, indent=2) + "\n", encoding="utf-8"
    )
    return root, pack, kept, stale


def test_prune_drops_only_rows_absent_from_declared_parent(tmp_path):
    root, pack, kept, stale = _prune_fixture(tmp_path)
    leaf = pack / f"leaves/{kept}/SKILL.md"
    leaf_before = leaf.read_bytes()

    changed = unit_closure.prune_pack(pack, root)

    assert changed == {
        "skills_index.json": [stale],
        "kb_bundle.json": [stale],
    }
    assert leaf.read_bytes() == leaf_before
    assert json.loads((pack / "skills_index.json").read_text()) == [{"slug": kept}]
    bundle = json.loads((pack / "kb_bundle.json").read_text())
    assert set(bundle["skills"]) == {kept}
    assert "\n {\n" in (pack / "skills_index.json").read_text()
    assert '\n  "skills"' in (pack / "kb_bundle.json").read_text()


@pytest.mark.parametrize(
    "parent_state",
    ("contains-stale", "missing", "invalid"),
    ids=("dangling-still-in-parent", "missing-parent", "invalid-parent"),
)
def test_prune_refusal_does_not_mutate_either_index(tmp_path, parent_state):
    root, pack, _, _ = _prune_fixture(tmp_path, parent_state=parent_state)
    before = {
        name: (pack / name).read_bytes()
        for name in ("skills_index.json", "kb_bundle.json")
    }

    with pytest.raises(ValueError):
        unit_closure.prune_pack(pack, root)

    assert {
        name: (pack / name).read_bytes()
        for name in ("skills_index.json", "kb_bundle.json")
    } == before


def test_layout_keeps_closure_messages_and_count_suffix(tmp_path):
    unit = tmp_path / "collections/astronomy/v1"
    _write_skill(unit, "leaves/photometry/SKILL.md")
    _write_indexes(unit, ["photometry", "absent"], ["photometry"])

    result = release_gate.check_layout(unit)

    assert result.status == release_gate.FAIL
    assert any(
        detail["message"]
        == "skills_index.json names 'absent', which has no SKILL.md under leaves/."
        for detail in result.details
    )
    assert result.summary.endswith("(2 indexed, 1 on disk)  (1 skills checked)")


def test_gate_checks_collection_and_only_same_repository_packs(tmp_path):
    root = tmp_path / "repository"
    collection = root / "collections/astronomy/v1"
    same_pack = root / "packs/astronomy/photometry"
    unrelated = tmp_path / "other/packs/astronomy/photometry"
    _write_skill(
        collection,
        "skills/entry/SKILL.md",
        helper="scripts/missing-collection.py",
    )
    for pack, helper in (
        (same_pack, "scripts/missing-pack.py"),
        (unrelated, "scripts/missing-unrelated.py"),
    ):
        _write_skill(pack, "leaves/photometry/SKILL.md")
        _write_skill(pack, "skills/_router/SKILL.md", helper=helper)
        _write_indexes(pack, ["photometry"], ["photometry"])

    result = release_gate.check_unit_closure(collection)

    assert result.status == release_gate.FAIL
    messages = [detail["message"] for detail in result.details]
    assert len(messages) == 2
    assert any("missing-collection.py" in message for message in messages)
    assert any("missing-pack.py" in message for message in messages)
    assert not any("missing-unrelated.py" in message for message in messages)


REAL_UNITS = sorted(
    path
    for pattern in ("collections/*/v*", "packs/*/*")
    for path in REPO_ROOT.glob(pattern)
    if path.is_dir()
)


@pytest.mark.parametrize(
    "unit",
    REAL_UNITS,
    ids=[str(path.relative_to(REPO_ROOT)) for path in REAL_UNITS],
)
def test_every_shipped_unit_has_closure_and_contained_helpers(unit):
    findings = unit_closure.check_unit(unit)
    details = "\n".join(
        f"{item.file}: {item.direction}: {item.message}" for item in findings
    )
    assert findings == [], details


def test_real_unit_matrix_covers_collections_and_packs():
    relatives = [path.relative_to(REPO_ROOT).parts[0] for path in REAL_UNITS]
    assert "collections" in relatives
    assert "packs" in relatives


@pytest.mark.parametrize("filename", ("skill_feedback.py", "pii_config.py"))
def test_collection_feedback_helpers_are_byte_identical_to_root(filename):
    root_helper = REPO_ROOT / "scripts" / filename
    shipped_helper = REPO_ROOT / "collections/metabolomics/v2/scripts" / filename

    assert shipped_helper.read_bytes() == root_helper.read_bytes()


def _copy_feedback_unit(tmp_path: pathlib.Path) -> pathlib.Path:
    source = REPO_ROOT / "collections/metabolomics/v2"
    unit = tmp_path / "installed-unit"
    shutil.copytree(source / "skills/asb-contribute", unit / "skills/asb-contribute")
    shutil.copytree(source / "scripts", unit / "scripts")
    return unit


def _run_isolated_feedback(unit: pathlib.Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-I", "-S", str(unit / "scripts/skill_feedback.py"), *args],
        cwd="/",
        text=True,
        capture_output=True,
        check=False,
    )


ISOLATED_DRY_RUN_ARGS = (
    "--dry-run",
    "--kind",
    "defect",
    "--target",
    "/Users/example/collections/metabolomics/v2/leaves/example-skill",
    "--symptom",
    "failed at /Users/example/private/run.raw for reporter@example.org",
    "--collection",
    "/Users/example/collections/metabolomics/v2",
)


def test_feedback_helper_runs_from_an_isolated_unit(tmp_path):
    unit = _copy_feedback_unit(tmp_path)

    help_result = _run_isolated_feedback(unit, "--help")
    dry_run = _run_isolated_feedback(unit, *ISOLATED_DRY_RUN_ARGS)

    assert help_result.returncode == 0, help_result.stderr
    assert dry_run.returncode == 0, dry_run.stderr
    output = help_result.stdout + help_result.stderr + dry_run.stdout + dry_run.stderr
    assert "Traceback" not in output
    assert "/Users/example" not in dry_run.stdout
    assert "reporter@example.org" not in dry_run.stdout
    assert "<redacted:" in dry_run.stdout


def test_isolated_feedback_helper_requires_its_vendored_pii_module(tmp_path):
    unit = _copy_feedback_unit(tmp_path)
    (unit / "scripts/pii_config.py").unlink()

    result = _run_isolated_feedback(unit, *ISOLATED_DRY_RUN_ARGS)

    assert result.returncode != 0
    assert "ModuleNotFoundError" in result.stderr
    assert "scripts.pii_config" in result.stderr
