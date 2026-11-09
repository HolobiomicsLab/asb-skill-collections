"""Advisory and strict EDAM resolution gate behavior."""

import os
import subprocess
import sys
from pathlib import Path

from scripts.domain_content_gates import check_edam, gate_commands


REPO = Path(__file__).resolve().parents[1]
VOCABULARY = REPO / "tests" / "fixtures" / "edam_remap" / "edam_vocabulary.json"


def make_collection(tmp_path):
    collection = tmp_path / "collection"
    leaf = collection / "leaves" / "bad" / "SKILL.md"
    leaf.parent.mkdir(parents=True)
    leaf.write_text(
        "---\nmetadata:\n  edam_operation: http://edamontology.org/operation_9999\n"
        "  edam_topics:\n  - http://edamontology.org/topic_0001\n"
        "  - not-an-edam-iri\n---\nBody\n"
    )
    return collection


def test_advisory_resolution_and_strict_failure(tmp_path, capsys):
    collection = make_collection(tmp_path)
    failures = check_edam(collection, vocabulary_path=VOCABULARY, strict=False)
    output = capsys.readouterr().out
    assert len(failures) == 1
    assert "obsolete: 1" in output
    assert "ghost: 1" in output
    assert "topic_0001" in output
    strict_failures = check_edam(collection, vocabulary_path=VOCABULARY, strict=True)
    assert len(strict_failures) == 4


def test_orchestrator_propagates_strict_flag(tmp_path):
    tooling = tmp_path / "tooling"
    content = tmp_path / "content"
    tooling.mkdir()
    content.mkdir()
    commands = gate_commands(tooling, content, "collections/test/v1", edam_strict=True)
    edam = next(command for name, command in commands if name == "Check EDAM IRIs")
    assert "--edam-strict" in edam
    assert "--edam-vocabulary" in edam


def test_cli_advisory_and_strict(tmp_path):
    collection = make_collection(tmp_path)
    base = [sys.executable, "scripts/domain_content_gates.py", "--edam-only", str(collection),
            "--edam-vocabulary", str(VOCABULARY)]
    advisory = subprocess.run(base, cwd=REPO, text=True, capture_output=True,
                              env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    strict = subprocess.run([*base, "--edam-strict"], cwd=REPO, text=True, capture_output=True,
                            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    assert advisory.returncode == 1
    assert "NOTE: EDAM resolution is advisory" in advisory.stdout
    assert strict.returncode == 1
    assert "ghost" in strict.stderr


def test_advisory_only_passes_when_prefixes_pass(tmp_path):
    collection = tmp_path / "collection"
    leaf = collection / "leaves" / "obsolete" / "SKILL.md"
    leaf.parent.mkdir(parents=True)
    leaf.write_text("---\nmetadata:\n  edam_operation: null\n  edam_topics:\n  - http://edamontology.org/topic_0001\n---\nBody\n")
    result = subprocess.run(
        [sys.executable, "scripts/domain_content_gates.py", "--edam-only", str(collection),
         "--edam-vocabulary", str(VOCABULARY)], cwd=REPO, text=True, capture_output=True,
    )
    assert result.returncode == 0
    assert "obsolete: 1" in result.stdout
