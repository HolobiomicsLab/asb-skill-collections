"""RO-Crate validation runs against the release-capsule truth module."""

import json
import shutil

import pytest

from scripts.release_capsule_truth import CRATE, crate_problems, released_capsules


def _crate(files):
    return {
        "@context": ["https://w3id.org/ro/crate/1.1/context"],
        "@graph": [
            {
                "@id": CRATE,
                "@type": "CreativeWork",
                "about": {"@id": "./"},
                "conformsTo": [{"@id": "https://w3id.org/ro/crate/1.1"}],
            },
            {"@id": "./", "@type": "Dataset", "hasPart": [{"@id": name} for name in files]},
            *({"@id": name, "@type": "File", "name": name} for name in files),
        ],
    }


@pytest.fixture
def repo(tmp_path):
    collection = tmp_path / "collections" / "alpha" / "v1"
    for task in ("task_001", "task_002"):
        capsule = collection / "capsules" / "tool" / task
        evidence = capsule / "evidence"
        evidence.mkdir(parents=True)
        (evidence / "source_snippets.md").write_text("evidence\n", encoding="utf-8")
        (capsule / CRATE).write_text(json.dumps(_crate(["evidence/source_snippets.md"])))
    return collection


def test_sound_crates_pass(repo):
    capsules = released_capsules(repo)
    assert len(capsules) == 2
    assert [crate_problems(capsule) for capsule in capsules] == [[], []]


def test_a_capsule_without_a_crate_fails(repo):
    capsule = repo / "capsules" / "tool" / "task_002"
    (capsule / CRATE).unlink()
    assert f"no {CRATE}" in crate_problems(capsule)


def test_a_crate_naming_a_file_the_capsule_does_not_hold_fails(repo):
    capsule = repo / "capsules" / "tool" / "task_001"
    files = ["evidence/source_snippets.md", "logs/run.md"]
    (capsule / CRATE).write_text(json.dumps(_crate(files)), encoding="utf-8")
    assert any("logs/run.md" in problem for problem in crate_problems(capsule))


def test_a_crate_outside_a_capsule_is_not_a_released_capsule(repo):
    (repo / CRATE).write_text(json.dumps(_crate([])), encoding="utf-8")
    assert len(released_capsules(repo)) == 2
    assert all(not crate_problems(capsule) for capsule in released_capsules(repo))


def test_no_released_capsule_is_detected(repo):
    shutil.rmtree(repo / "capsules")
    assert released_capsules(repo) == []
