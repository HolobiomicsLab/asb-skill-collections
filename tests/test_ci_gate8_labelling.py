"""Gate 8 (RO-Crate) blocks, over every released capsule, and cannot pass over nothing.

History. The step globbed for `ro-crate-metadata.json`, found none anywhere in the
repository, printed "PASS: RO-Crate validation OK (0 crates checked)" and sat behind
`continue-on-error: true`. The four `collection.yaml` files declared
`ro_crate_path: ro-crate-metadata.json` regardless; that field was dropped, and the
step was relabelled to say it had measured nothing. Real crates were left to v1.

They now ship: every released capsule carries the crate its build wrote, pruned at
promotion to what the capsule holds (`scripts/release_capsule_truth.py`). The step
holds each one to `crate_problems` and fails the job on any problem. Finding no
released capsule fails too, so a moved layout cannot turn the gate back into a pass
over zero files.

The static tests pin the step's text. The behavioural tests run the step's own
script over a small tree, with the real rule module copied beside it.
"""
import json
import pathlib
import re
import shutil
import subprocess
import sys
import textwrap

import pytest

ROOT = pathlib.Path(__file__).parent.parent
VALIDATE = ROOT / ".github" / "workflows" / "validate.yml"
CRATE = "ro-crate-metadata.json"


def _gate8_step() -> str:
    """Return the gate-8 section (its comment block + the step body)."""
    text = VALIDATE.read_text()
    start_marker = "# -- Gate 8:"
    assert start_marker in text, "gate-8 section comment not found"
    start = text.index(start_marker)
    rest = text[start:]
    nxt = rest.find("\n      # -- Gate", 1)
    return rest if nxt == -1 else rest[:nxt]


def _gate8_script() -> str:
    match = re.search(r"python - <<'EOF'\n(.*?)\n\s*EOF\n", _gate8_step(), re.S)
    assert match, "gate-8 python heredoc not found"
    return textwrap.dedent(match.group(1))


# -- static contract ----------------------------------------------------------


def test_gate8_is_not_behind_continue_on_error():
    assert not re.search(r"^\s*continue-on-error:", _gate8_step(), re.M), (
        "gate 8 must be able to fail the job; continue-on-error is what kept its "
        "pass over zero files green"
    )


def test_gate8_applies_the_rule_the_tests_use():
    step = _gate8_step()
    assert "from release_capsule_truth import CRATE, crate_problems, released_capsules" in step, (
        "the gate must import the one rule rather than re-implement a weaker one"
    )


def test_header_describes_gate8_as_it_now_behaves():
    """The description has to sit on gate 8's own entry, not merely somewhere above it."""
    header = VALIDATE.read_text().split("name: Validate", 1)[0]
    start = header.index("#   8.")
    entry = header[start:header.index("#   9.", start)]
    assert "BLOCKING" in entry
    assert "WARN-ONLY" not in entry
    assert "RO-Crate 1.1" in entry
    assert "not checked" in entry, "the header must say the run-profile claim is not checked"


def test_every_released_capsule_ships_a_crate():
    """The premise of the gate, asserted rather than assumed."""
    sys.path.insert(0, str(ROOT / "scripts"))
    from release_capsule_truth import released_capsules

    capsules = [
        c for p in sorted((ROOT / "collections").glob("*/*/collection.yaml"))
        for c in released_capsules(p.parent)
    ]
    assert len(capsules) == 417, f"expected the 417 released capsules, found {len(capsules)}"
    without = [str(c.relative_to(ROOT)) for c in capsules if not (c / CRATE).is_file()]
    assert not without, f"{len(without)} released capsule(s) ship no crate: {without[:5]}"


def test_no_collection_manifest_declares_a_collection_level_crate():
    """The crates are per capsule. No collection ships a crate at its root, so a
    manifest declaring `ro_crate_path` would re-create the dangling path that
    dropping the field removed."""
    manifests = sorted((ROOT / "collections").rglob("collection.yaml"))
    assert manifests, "no collection manifest found"
    declaring = [m for m in manifests if "ro_crate_path" in m.read_text()]
    assert not declaring, (
        f"{[str(m.relative_to(ROOT)) for m in declaring]} declare ro_crate_path; "
        f"no collection ships {CRATE} at its root"
    )
    assert not [m.parent / CRATE for m in manifests if (m.parent / CRATE).exists()]


def test_the_generator_does_not_reintroduce_the_field():
    """Dropping it from the four manifests is undone by the next generation run
    unless the generator stops writing it."""
    gen = (ROOT / "scripts" / "collect_metabolomics_collection.py").read_text()
    assert "ro_crate_path" not in gen, (
        "the collection generator still writes ro_crate_path; the field would come "
        "back on the next run"
    )


# -- behaviour, over a small tree ----------------------------------------------


def _crate(files):
    return {
        "@context": ["https://w3id.org/ro/crate/1.1/context"],
        "@graph": [
            {"@id": CRATE, "@type": "CreativeWork", "about": {"@id": "./"},
             "conformsTo": [{"@id": "https://w3id.org/ro/crate/1.1"}]},
            {"@id": "./", "@type": "Dataset", "hasPart": [{"@id": f} for f in files]},
            *({"@id": f, "@type": "File", "name": f} for f in files),
        ],
    }


@pytest.fixture
def repo(tmp_path):
    (tmp_path / "scripts").mkdir()
    shutil.copy2(ROOT / "scripts" / "release_capsule_truth.py", tmp_path / "scripts")
    (tmp_path / "gate8.py").write_text(_gate8_script())
    collection = tmp_path / "collections" / "alpha" / "v1"
    collection.mkdir(parents=True)
    (collection / "collection.yaml").write_text("slug: alpha\n")
    for task in ("task_001", "task_002"):
        capsule = collection / "capsules" / "tool" / task
        (capsule / "evidence").mkdir(parents=True)
        (capsule / "evidence" / "source_snippets.md").write_text("evidence\n")
        (capsule / CRATE).write_text(json.dumps(_crate(["evidence/source_snippets.md"])))
    return tmp_path


def _run(repo):
    return subprocess.run(
        [sys.executable, "gate8.py"], cwd=repo, capture_output=True, text=True
    )


def test_sound_crates_pass(repo):
    result = _run(repo)
    assert result.returncode == 0, result.stdout + result.stderr
    assert result.stdout.startswith("PASS: 2 released capsules")


def test_a_capsule_without_a_crate_fails(repo):
    (repo / "collections/alpha/v1/capsules/tool/task_002" / CRATE).unlink()
    result = _run(repo)
    assert result.returncode == 1
    assert f"task_002: no {CRATE}" in result.stdout


def test_a_crate_naming_a_file_the_capsule_does_not_hold_fails(repo):
    capsule = repo / "collections/alpha/v1/capsules/tool/task_001"
    (capsule / CRATE).write_text(json.dumps(_crate(["evidence/source_snippets.md", "logs/run.md"])))
    result = _run(repo)
    assert result.returncode == 1
    assert "names 'logs/run.md', which the capsule does not hold" in result.stdout


def test_a_crate_outside_a_capsule_fails(repo):
    (repo / "collections/alpha/v1" / CRATE).write_text(json.dumps(_crate([])))
    result = _run(repo)
    assert result.returncode == 1
    assert "a crate outside a released capsule" in result.stdout


def test_no_released_capsule_fails_rather_than_passing_over_nothing(repo):
    shutil.rmtree(repo / "collections/alpha/v1/capsules")
    result = _run(repo)
    assert result.returncode == 1
    assert "found no released capsule" in result.stdout


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
