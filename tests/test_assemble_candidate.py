"""Contract tests for the deterministic S4 through S6 candidate driver."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import yaml


REPO = Path(__file__).resolve().parent.parent
FIXTURE = REPO / "tests" / "fixtures" / "cut_three_outputs"
SCRIPT = REPO / "scripts" / "assemble_candidate.py"
MODEL = "BAAI/bge-small-en-v1.5"
COMMITS = {
    "asb": "0123456789abcdef0123456789abcdef01234567",
    "tooling": "1123456789abcdef0123456789abcdef01234567",
    "corpus": "2123456789abcdef0123456789abcdef01234567",
}
EXPECTED_RECEIPTS = {
    "bootstrap.txt",
    "bootstrap_receipt.json",
    "check_license_tiers.txt",
    "check_provenance_tiers.txt",
    "check_tools_index.txt",
    "checks.json",
    "collect.txt",
    "collect_receipt.json",
    "corpus.yaml",
    "corpus_join_receipt.json",
    "evidence_trim_receipt.json",
    "gate.txt",
    "gate_report.json",
    "gates.txt",
    "join.txt",
    "lint.txt",
    "mapping.json",
    "same_paper.txt",
    "same_paper_pairs.json",
    "source.json",
    "verify.txt",
}
STAGE_SCRIPTS = {
    "join_corpus_records.py",
    "collect_from_cut.py",
    "bootstrap_indexes.py",
    "run_candidate_gates.py",
    "same_paper_pairs.py",
}


def _environment() -> dict[str, str]:
    """Return the release pipeline's credential-free offline environment."""
    environment = dict(os.environ)
    for key in ("OPENAI_API_KEY", "OPENROUTER_API_KEY", "ANTHROPIC_API_KEY"):
        environment.pop(key, None)
    environment.update(
        HF_HUB_OFFLINE="1",
        TRANSFORMERS_OFFLINE="1",
        ASB_EMBED_MODEL="bge-small-en-v1.5",
        PYTHONDONTWRITEBYTECODE="1",
    )
    return environment


def _copy_fixture(tmp_path: Path) -> Path:
    """Copy every driver input so tests never alter the tracked fixture."""
    destination = tmp_path / "fixture"
    shutil.copytree(FIXTURE, destination)
    return destination


def _arguments(
    fixture: Path,
    output: Path,
    receipts: Path,
    *,
    asb_commit: str = COMMITS["asb"],
    tiered: Path | None = None,
) -> list[str]:
    """Build one complete public CLI invocation."""
    return [
        "--cut",
        str(fixture / "corpus"),
        "--builds",
        str(fixture / "builds"),
        "--tiered",
        str(tiered or fixture / "metabarcoding_tiered.json"),
        "--domain",
        "metabarcoding",
        "--version",
        "v1",
        "--out",
        str(output),
        "--receipts",
        str(receipts),
        "--asb-commit",
        asb_commit,
        "--tooling-commit",
        COMMITS["tooling"],
        "--corpus-commit",
        COMMITS["corpus"],
        "--verified-on",
        "2026-09-18",
        "--view-source",
        str(fixture / "FIXTURE.md"),
    ]


def _run(arguments: list[str]) -> subprocess.CompletedProcess[str]:
    """Invoke the candidate driver through its supported CLI."""
    return subprocess.run(
        [sys.executable, str(SCRIPT), *arguments],
        cwd=REPO,
        env=_environment(),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def _last_json(output: str) -> dict:
    """Decode the driver's final structured status line."""
    lines = [line for line in output.splitlines() if line.strip()]
    assert lines, "driver produced no status output"
    return json.loads(lines[-1])


def _tree_bytes(root: Path) -> dict[str, bytes]:
    """Snapshot every regular file below a possibly absent tree."""
    if not root.exists():
        return {}
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def _tree_digest(root: Path) -> str:
    """Match the collector's sorted path plus content-digest algorithm."""
    digest = hashlib.sha256()
    for relative, content in sorted(_tree_bytes(root).items()):
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(hashlib.sha256(content).digest())
    return digest.hexdigest()


def _sha256(path: Path) -> str:
    """Return a file's hexadecimal SHA-256 digest."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_driver_dry_run_prints_six_real_commands_and_writes_nothing(
    tmp_path: Path,
) -> None:
    """Describe join, collect, copy, bootstrap, gates, and duplicate stages."""
    fixture = _copy_fixture(tmp_path)
    output = tmp_path / "candidate"
    output.mkdir()
    receipts = tmp_path / "receipts"
    before = _tree_bytes(output)

    result = _run([*_arguments(fixture, output, receipts), "--dry-run"])

    assert result.returncode == 0, result.stdout
    assert _tree_bytes(output) == before == {}
    assert output.is_dir()
    assert not receipts.exists()
    plan = _last_json(result.stdout)
    assert plan["dry_run"] is True
    assert (
        plan["cut_id"]
        == _sha256(fixture / "corpus" / "skills" / "coverage_summary.json")[:12]
    )
    assert [entry["stage"] for entry in plan["commands"]] == [
        "join",
        "collect",
        "copy_corpus",
        "bootstrap",
        "gates",
        "same_paper",
    ]
    commands = {entry["stage"]: entry["command"] for entry in plan["commands"]}
    assert Path(commands["join"][1]).name == "join_corpus_records.py"
    assert Path(commands["collect"][1]).name == "collect_from_cut.py"
    assert commands["copy_corpus"] == [
        "copy",
        str(receipts / "corpus.yaml"),
        str(output / "corpus.yaml"),
    ]
    assert Path(commands["bootstrap"][1]).name == "bootstrap_indexes.py"
    assert Path(commands["gates"][1]).name == "run_candidate_gates.py"
    assert Path(commands["same_paper"][1]).name == "same_paper_pairs.py"
    assert all(
        command[0] == sys.executable
        for stage, command in commands.items()
        if stage != "copy_corpus"
    )
    assert "--verified-on" in commands["join"]
    assert str(receipts / "corpus.yaml") in commands["join"]
    assert str(receipts / "corpus.yaml") in commands["collect"]
    assert str(output / "corpus.yaml") in commands["bootstrap"]
    assert str(output / "corpus.yaml") in commands["gates"]
    assert str(receipts / "same_paper_pairs.json") in commands["same_paper"]


def test_driver_builds_complete_candidate_and_second_run_is_identical(
    tmp_path: Path,
) -> None:
    """Run the fixture through every stage and preserve the completed trees."""
    fixture = _copy_fixture(tmp_path)
    output = tmp_path / "candidate"
    output.mkdir()
    receipts = tmp_path / "receipts"
    arguments = _arguments(fixture, output, receipts)

    first = _run(arguments)
    assert first.returncode == 0, first.stdout
    assert {path.name for path in receipts.iterdir()} == EXPECTED_RECEIPTS
    assert (output / "corpus.yaml").is_file()
    assert (receipts / "mapping.json").read_bytes() == (
        output / "mapping.json"
    ).read_bytes()

    gate_report = json.loads(
        (receipts / "gate_report.json").read_text(encoding="utf-8")
    )
    checks = json.loads((receipts / "checks.json").read_text(encoding="utf-8"))
    assert gate_report["release_verified"] is True
    assert checks == {
        "stage": "S5",
        "exit_code": 0,
        "checks": {
            "gate": 0,
            "lint": 0,
            "check_license_tiers": 0,
            "check_provenance_tiers": 0,
            "check_tools_index": 0,
            "verify": 0,
        },
    }

    coverage = fixture / "corpus" / "skills" / "coverage_summary.json"
    source = json.loads((receipts / "source.json").read_text(encoding="utf-8"))
    expected_cut_id = _sha256(coverage)[:12]
    assert expected_cut_id == "c631e4625159"
    assert set(source) == {
        "status",
        "asb_commit",
        "tooling_commit",
        "corpus_commit",
        "view",
        "view_source_sha256",
        "cut_id",
        "domain",
        "version",
        "model",
        "thresholds",
        "stage_script_sha256",
        "output_tree_sha256",
        "receipts",
    }
    assert source["status"] == "complete"
    assert source["cut_id"] == expected_cut_id
    assert source["domain"] == "metabarcoding"
    assert source["version"] == "v1"
    assert source["view"] == str(fixture / "corpus")
    assert source["view_source_sha256"] == _sha256(fixture / "FIXTURE.md")
    assert source["asb_commit"] == COMMITS["asb"]
    assert source["tooling_commit"] == COMMITS["tooling"]
    assert source["corpus_commit"] == COMMITS["corpus"]
    assert source["model"] == MODEL
    assert source["thresholds"] == {
        "auto_merge": 0.95,
        "suggest": 0.90,
        "embed_view": "name_tools",
    }
    assert source["stage_script_sha256"] == {
        name: _sha256(REPO / "scripts" / name) for name in sorted(STAGE_SCRIPTS)
    }
    assert source["output_tree_sha256"] == _tree_digest(output)
    assert source["receipts"] == sorted(EXPECTED_RECEIPTS)

    corpus = yaml.safe_load((output / "corpus.yaml").read_text(encoding="utf-8"))
    assert {paper["access"]["verified_on"] for paper in corpus["papers"]} == {
        "2026-09-18"
    }
    before = (_tree_bytes(output), _tree_bytes(receipts))

    second = _run(arguments)
    assert second.returncode == 0, second.stdout
    assert _last_json(second.stdout) == {
        "cut_id": expected_cut_id,
        "status": "identical",
    }
    assert (_tree_bytes(output), _tree_bytes(receipts)) == before


def test_driver_refuses_wrong_cut_source_before_join(tmp_path: Path) -> None:
    """Stop before every stage when an existing source names another cut."""
    fixture = _copy_fixture(tmp_path)
    output = tmp_path / "candidate"
    receipts = tmp_path / "receipts"
    receipts.mkdir()
    source_path = receipts / "source.json"
    foreign = b'{"cut_id":"ffffffffffff","status":"complete"}\n'
    source_path.write_bytes(foreign)

    result = _run(_arguments(fixture, output, receipts))

    assert result.returncode == 2, result.stdout
    assert "cut_id" in result.stdout
    assert source_path.read_bytes() == foreign
    assert not (receipts / "join.txt").exists()
    assert not output.exists()


def test_driver_records_first_stage_failure_and_preserves_its_exit_code(
    tmp_path: Path,
) -> None:
    """Keep the join log and a failed source receipt when S4 cannot parse."""
    fixture = _copy_fixture(tmp_path)
    output = tmp_path / "candidate"
    receipts = tmp_path / "receipts"
    invalid_tiered = tmp_path / "invalid-tiered.json"
    invalid_tiered.write_text("not json\n", encoding="utf-8")

    result = _run(_arguments(fixture, output, receipts, tiered=invalid_tiered))

    assert result.returncode == 1, result.stdout
    assert (receipts / "join.txt").is_file()
    assert not (receipts / "collect.txt").exists()
    source = json.loads((receipts / "source.json").read_text(encoding="utf-8"))
    assert source["status"] == "failed"
    assert source["failed_stage"] == "join"
    assert source["exit_code"] == 1


def test_driver_validates_commit_pins_and_fresh_output_before_stages(
    tmp_path: Path,
) -> None:
    """Reject malformed pins and populated candidates without invoking S4."""
    fixture = _copy_fixture(tmp_path)
    for index, commit in enumerate(("123456", "g123456", "1" * 41)):
        output = tmp_path / f"candidate-{index}"
        receipts = tmp_path / f"receipts-{index}"
        result = _run(
            _arguments(
                fixture,
                output,
                receipts,
                asb_commit=commit,
            )
        )
        assert result.returncode == 1, result.stdout
        assert not output.exists()
        assert not receipts.exists()

    output = tmp_path / "owned-candidate"
    output.mkdir()
    marker = output / "owned.txt"
    marker.write_text("keep\n", encoding="utf-8")
    receipts = tmp_path / "owned-receipts"
    result = _run(_arguments(fixture, output, receipts))
    assert result.returncode == 2, result.stdout
    assert marker.read_text(encoding="utf-8") == "keep\n"
    assert not receipts.exists()
