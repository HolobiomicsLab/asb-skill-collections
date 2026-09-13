"""Advertised collection members must match every published representation."""

import json
import pathlib
import sys

import yaml

REPO_ROOT = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT))
from scripts import release_gate  # noqa: E402


def _write_collection(
    root: pathlib.Path,
    *,
    listed_skills=("alpha",),
    disk_skills=("alpha",),
    indexed_skills=("alpha",),
    skills_count=None,
    listed_tools=("tool-a",),
    disk_tools=("tool-a",),
    indexed_tools=("tool-a",),
) -> pathlib.Path:
    """Create one complete synthetic collection under an arbitrary tree."""
    collection = root / "nested" / "science" / "v9"
    (collection / "skills").mkdir(parents=True)
    (collection / "tools").mkdir()
    for slug in disk_skills:
        skill_dir = collection / "skills" / slug
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(f"# {slug}\n", encoding="utf-8")
    for slug in disk_tools:
        (collection / "tools" / f"{slug}.yaml").write_text(
            yaml.safe_dump({"slug": slug}), encoding="utf-8"
        )
    metadata = {
        "skills_count": len(listed_skills) if skills_count is None else skills_count,
        "tools_count": len(listed_tools),
        "skills": list(listed_skills),
        "tools": list(listed_tools),
    }
    (collection / "collection.yaml").write_text(
        yaml.safe_dump(metadata), encoding="utf-8"
    )
    (collection / "skills_index.json").write_text(
        json.dumps([{"slug": slug} for slug in indexed_skills]), encoding="utf-8"
    )
    (collection / "tools_index.json").write_text(
        json.dumps([{"slug": slug} for slug in indexed_tools]), encoding="utf-8"
    )
    return collection


def _messages(result) -> str:
    return " | ".join(detail["message"] for detail in result.details)


def test_corrected_repository_catalogues_pass():
    result = release_gate.check_catalogue_membership(REPO_ROOT / "collections")
    assert result.status == release_gate.PASS, _messages(result)


def test_membership_check_is_a_hard_release_gate(tmp_path):
    collection = _write_collection(tmp_path)
    report = release_gate.run_gate(collection, None, strict=True)
    check = next(
        item for item in report["checks"] if item["name"] == "catalogue_membership"
    )
    assert check["status"] == release_gate.PASS
    assert check["gates"] == [10]
    assert check["hard_gate"] is True


def test_member_missing_from_advertised_list_fails(tmp_path):
    _write_collection(
        tmp_path,
        disk_skills=("alpha", "beta"),
        indexed_skills=("alpha", "beta"),
    )
    result = release_gate.check_catalogue_membership(tmp_path)
    assert result.status == release_gate.FAIL
    assert "beta" in _messages(result)
    assert "missing from collection.yaml skills" in _messages(result)


def test_count_mismatch_fails(tmp_path):
    _write_collection(tmp_path, skills_count=2)
    result = release_gate.check_catalogue_membership(tmp_path)
    assert result.status == release_gate.FAIL
    assert "skills_count is 2 but skills has 1 member" in _messages(result)


def test_extra_advertised_member_without_a_disk_leaf_fails(tmp_path):
    _write_collection(
        tmp_path,
        listed_skills=("alpha", "ghost"),
        indexed_skills=("alpha", "ghost"),
    )
    result = release_gate.check_catalogue_membership(tmp_path)
    assert result.status == release_gate.FAIL
    assert "ghost" in _messages(result)
    assert "collection.yaml skills missing from skills/" in _messages(result)


def test_tools_use_the_same_count_disk_and_index_rules(tmp_path):
    _write_collection(tmp_path, listed_tools=("tool-a", "tool-ghost"))
    result = release_gate.check_catalogue_membership(tmp_path)
    assert result.status == release_gate.FAIL
    messages = _messages(result)
    assert "tool-ghost" in messages
    assert "collection.yaml tools missing from tools/" in messages
    assert "collection.yaml tools missing from tools_index.json" in messages
