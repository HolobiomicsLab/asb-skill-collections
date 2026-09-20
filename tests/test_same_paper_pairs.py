"""Contract tests for the deterministic S6 same-paper duplicate report."""

from __future__ import annotations

import ast
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
FIXTURE = REPO / "tests" / "fixtures" / "cut_three_outputs" / "corpus"
SCRIPT = REPO / "scripts" / "same_paper_pairs.py"
MODEL = "BAAI/bge-small-en-v1.5"
SOURCE_OUTPUT = "amplicon-sequence-denoising"
DUPLICATE_OUTPUT = "amplicon-sequence-denoising--0123456789abcdef"
FORBIDDEN_REPORT_KEYS = {
    "seconds",
    "timestamp",
    "generated_at",
    "rehearsal",
    "filter",
    "source_provenance",
    "layout",
    "embedding_diagnostics",
    "diagnostics",
}


def _environment() -> dict[str, str]:
    """Return the required credential-free offline subprocess environment."""
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


def _copy_cut(tmp_path: Path) -> Path:
    """Copy the tracked three-output cut so variants stay test-local."""
    destination = tmp_path / "corpus"
    shutil.copytree(FIXTURE, destination)
    return destination


def _write_json(path: Path, payload: object) -> None:
    """Write stable JSON used only to construct a temporary input cut."""
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _plant_duplicate(cut: Path) -> list[str]:
    """Add one distinct output with the same name, tools, and source runs."""
    skills = cut / "skills"
    source = skills / SOURCE_OUTPUT
    duplicate = skills / DUPLICATE_OUTPUT
    shutil.copytree(source, duplicate)
    coverage_path = duplicate / "coverage.json"
    coverage = json.loads(coverage_path.read_text(encoding="utf-8"))
    coverage["output_id"] = DUPLICATE_OUTPUT
    _write_json(coverage_path, coverage)
    summary_path = skills / "coverage_summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    summary[DUPLICATE_OUTPUT] = coverage
    _write_json(summary_path, summary)
    return coverage["capsules"]


def _run(cut: Path, output: Path, *extra: str) -> subprocess.CompletedProcess[str]:
    """Invoke the public command under the release offline environment."""
    return subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--view",
            str(cut),
            "--out",
            str(output),
            *extra,
        ],
        cwd=REPO,
        env=_environment(),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def _last_json(output: str) -> dict:
    """Decode the command's final structured status line."""
    lines = [line for line in output.splitlines() if line.strip()]
    assert lines, "command produced no status output"
    return json.loads(lines[-1])


def test_duplicate_pair_is_reported_once_per_shared_run_and_is_deterministic(
    tmp_path: Path,
) -> None:
    """Score the planted duplicate per shared run and preserve identical bytes."""
    cut = _copy_cut(tmp_path)
    shared_runs = _plant_duplicate(cut)
    output = tmp_path / "same_paper_pairs.json"

    first = _run(cut, output)
    assert first.returncode == 0, first.stdout
    first_bytes = output.read_bytes()
    report = json.loads(first_bytes)

    assert FORBIDDEN_REPORT_KEYS.isdisjoint(report)
    assert report["model"] == MODEL
    assert report["thresholds"] == {
        "auto_merge": 0.95,
        "suggest": 0.90,
        "embed_view": "name_tools",
        "pair_scope": "same_run_full_pairwise",
    }
    assert report["view"] == str(cut.resolve())
    assert report["input_digests"] == {
        "coverage_summary_sha256": hashlib.sha256(
            (cut / "skills" / "coverage_summary.json").read_bytes()
        ).hexdigest(),
        "outputs": 4,
    }
    assert report["skills"] == 4
    assert report["runs"] == 3
    assert report["auto_merges_applied"] is False
    assert report["pairs_0_90_to_0_95"] == []
    assert report["components_ge_0_95"] == 1
    assert report["components_ge_0_90"] == 1
    assert report["surplus_leaves"] == {"ge_0_90": 1, "ge_0_95": 1}

    pairs = report["pairs_ge_0_95"]
    assert len(pairs) == len(shared_runs) == 2
    assert [pair["run"] for pair in pairs] == sorted(shared_runs)
    for pair in pairs:
        assert set(pair) == {"score", "run", "left", "right"}
        assert pair["score"] >= 0.95
        assert pair["score"] == round(pair["score"], 6)
        assert pair["left"] == {
            "output_id": SOURCE_OUTPUT,
            "canonical_slug": SOURCE_OUTPUT,
            "merge_kind": "semantic_auto",
        }
        assert pair["right"] == {
            "output_id": DUPLICATE_OUTPUT,
            "canonical_slug": SOURCE_OUTPUT,
            "merge_kind": "semantic_auto",
        }

    second = _run(cut, output)
    assert second.returncode == 0, second.stdout
    assert _last_json(second.stdout)["output_status"] == "identical"
    assert output.read_bytes() == first_bytes


def test_unmodified_cut_has_no_high_pair_and_dry_run_writes_nothing(
    tmp_path: Path,
) -> None:
    """Keep unrelated same-paper outputs separate and make dry run read-only."""
    cut = _copy_cut(tmp_path)
    output = tmp_path / "same_paper_pairs.json"

    result = _run(cut, output)
    assert result.returncode == 0, result.stdout
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["pairs_ge_0_95"] == []
    assert report["components_ge_0_95"] == 0
    assert report["surplus_leaves"]["ge_0_95"] == 0

    dry_output = tmp_path / "dry" / "same_paper_pairs.json"
    dry_run = _run(cut, dry_output, "--dry-run")
    assert dry_run.returncode == 0, dry_run.stdout
    assert not dry_output.exists()
    assert not dry_output.parent.exists()
    summary = _last_json(dry_run.stdout)
    assert summary["dry_run"] is True
    assert summary["skills"] == 3
    assert summary["runs"] == 3
    assert summary["pairs_ge_0_95"] == 0
    assert isinstance(summary["pairs_0_90_to_0_95"], int)


def test_conflict_and_invalid_calibration_options_do_not_replace_output(
    tmp_path: Path,
) -> None:
    """Return the 1/2 contract for invalid calibration and differing bytes."""
    cut = _copy_cut(tmp_path)
    output = tmp_path / "same_paper_pairs.json"
    foreign = b'{"owned": "elsewhere"}\n'
    output.write_bytes(foreign)

    conflict = _run(cut, output)
    assert conflict.returncode == 2, conflict.stdout
    assert output.read_bytes() == foreign

    invalid_model_output = tmp_path / "invalid-model.json"
    invalid_model = _run(
        cut,
        invalid_model_output,
        "--model",
        "text-embedding-3-large",
    )
    assert invalid_model.returncode == 1, invalid_model.stdout
    assert not invalid_model_output.exists()

    invalid_threshold_output = tmp_path / "invalid-threshold.json"
    invalid_threshold = _run(
        cut,
        invalid_threshold_output,
        "--thresholds",
        "0.89,0.90",
    )
    assert invalid_threshold.returncode == 1, invalid_threshold.stdout
    assert not invalid_threshold_output.exists()


def test_same_paper_script_has_no_agentic_science_builder_import() -> None:
    """Keep the shipped duplicate stage independent of the ASB checkout."""
    tree = ast.parse(SCRIPT.read_text(encoding="utf-8"))
    imported = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    imported.update(
        node.module or "" for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)
    )
    assert all(not name.startswith("agentic_science_builder") for name in imported)
