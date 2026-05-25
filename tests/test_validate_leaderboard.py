"""Unit tests for validate_leaderboard.py."""
import json
import pathlib
import pytest
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

FIXTURES = pathlib.Path(__file__).parent / "fixtures"


@pytest.fixture()
def valid_lb(tmp_path):
    src = FIXTURES / "leaderboard_valid.jsonld"
    dst = tmp_path / "leaderboard.jsonld"
    import shutil
    shutil.copy(src, dst)
    return dst


@pytest.fixture()
def invalid_lb(tmp_path):
    src = FIXTURES / "leaderboard_invalid.jsonld"
    dst = tmp_path / "leaderboard.jsonld"
    import shutil
    shutil.copy(src, dst)
    return dst


def test_valid_leaderboard_passes(valid_lb):
    from scripts.validate_leaderboard import validate_leaderboard
    errors = validate_leaderboard(valid_lb)
    assert errors == [], f"Unexpected validation errors: {errors}"


def test_invalid_result_type_fails(invalid_lb):
    from scripts.validate_leaderboard import validate_leaderboard
    errors = validate_leaderboard(invalid_lb)
    assert len(errors) > 0
    assert any("result_type" in e for e in errors)


def test_missing_required_fields_fails(tmp_path):
    from scripts.validate_leaderboard import validate_leaderboard
    lb = {
        "@context": {"asb": "https://w3id.org/holobiomicslab/asb-skill/"},
        "@type": "asb:Leaderboard",
        "entries": [
            {
                "result_type": "agent",
                # missing: submitter_handle, agent_or_system_name, image_digest, submitted_at, scores
            }
        ]
    }
    path = tmp_path / "lb.jsonld"
    path.write_text(json.dumps(lb))
    errors = validate_leaderboard(path)
    assert len(errors) > 0


def test_all_three_result_types_accepted(tmp_path):
    from scripts.validate_leaderboard import validate_leaderboard
    entries = []
    for rt in ("agent", "rag_system", "hybrid"):
        entries.append({
            "result_type": rt,
            "submitter_handle": f"user-{rt}",
            "agent_or_system_name": f"System {rt}",
            "image_digest": "sha256:" + "a" * 64,
            "submitted_at": "2026-05-25T00:00:00Z",
            "scores": {"q1": 0.9},
            "metrics": {},
        })
    lb = {
        "@context": {"asb": "https://w3id.org/holobiomicslab/asb-skill/"},
        "@type": "asb:Leaderboard",
        "entries": entries,
    }
    path = tmp_path / "lb.jsonld"
    path.write_text(json.dumps(lb))
    errors = validate_leaderboard(path)
    assert errors == [], f"Unexpected errors: {errors}"


def test_scores_must_be_numeric(tmp_path):
    from scripts.validate_leaderboard import validate_leaderboard
    lb = {
        "@context": {"asb": "https://w3id.org/holobiomicslab/asb-skill/"},
        "@type": "asb:Leaderboard",
        "entries": [
            {
                "result_type": "agent",
                "submitter_handle": "user1",
                "agent_or_system_name": "Sys",
                "image_digest": "sha256:" + "b" * 64,
                "submitted_at": "2026-05-25T00:00:00Z",
                "scores": {"q1": "high"},  # invalid: string not numeric
                "metrics": {},
            }
        ],
    }
    path = tmp_path / "lb.jsonld"
    path.write_text(json.dumps(lb))
    errors = validate_leaderboard(path)
    assert len(errors) > 0
    assert any("scores" in e for e in errors)


def test_cli_exit_zero_on_valid(valid_lb):
    import subprocess
    result = subprocess.run(
        [sys.executable, "scripts/validate_leaderboard.py", str(valid_lb)],
        capture_output=True,
        text=True,
        cwd=str(pathlib.Path(__file__).parent.parent),
    )
    assert result.returncode == 0, f"stdout={result.stdout}\nstderr={result.stderr}"


def test_cli_exit_nonzero_on_invalid(invalid_lb):
    import subprocess
    result = subprocess.run(
        [sys.executable, "scripts/validate_leaderboard.py", str(invalid_lb)],
        capture_output=True,
        text=True,
        cwd=str(pathlib.Path(__file__).parent.parent),
    )
    assert result.returncode != 0, "Expected non-zero exit on invalid leaderboard"
