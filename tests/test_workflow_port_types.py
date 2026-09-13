"""Composite workflow ports and declared layout counts stay internally consistent."""

from __future__ import annotations

import pathlib
import sys

import pytest
import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts import release_gate, validate_workflows  # noqa: E402


def _step(
    step_id: str,
    *,
    inputs: tuple[str, ...] = (),
    outputs: tuple[str, ...] = (),
    inputs_from: dict[str, list[str]] | None = None,
) -> dict:
    """Build one minimal step in the composite-workflow document shape."""
    step = {
        "id": step_id,
        "skills": [],
        "inputs": [{"type": port_type} for port_type in inputs],
        "outputs": [{"type": port_type} for port_type in outputs],
        "after": list(inputs_from or {}),
    }
    if inputs_from is not None:
        step["inputs_from"] = inputs_from
    return step


def _chain(
    *,
    producer_outputs: tuple[str, ...] = ("raw-table",),
    consumer_inputs: tuple[str, ...] = ("raw-table",),
    transferred_types: tuple[str, ...] = ("raw-table",),
) -> list[dict]:
    """Build a two-step producer/consumer chain."""
    return [
        _step("produce", outputs=producer_outputs),
        _step(
            "consume",
            inputs=consumer_inputs,
            outputs=("result-table",),
            inputs_from={"produce": list(transferred_types)},
        ),
    ]


def _write_collection(
    root: pathlib.Path,
    steps: list[dict],
    *,
    workflows_count: int | None = None,
    workflow_name: str = "synthetic-chain",
) -> pathlib.Path:
    """Write a minimal collection and workflow beneath ``root``."""
    collection = root / "collection"
    workflow_dir = collection / "workflows" / workflow_name
    workflow_dir.mkdir(parents=True)
    (collection / "skills_index.json").write_text("[]\n", encoding="utf-8")
    if workflows_count is not None:
        (collection / "collection.yaml").write_text(
            yaml.safe_dump({"workflows_count": workflows_count}), encoding="utf-8"
        )
    frontmatter = {
        "name": workflow_name,
        "schema_version": "0.3.0",
        "metadata": {
            "kind": "composite-workflow",
            "member_skills": [],
            "member_tools": [],
        },
    }
    (workflow_dir / "SKILL.md").write_text(
        "---\n" + yaml.safe_dump(frontmatter) + "---\n# Synthetic workflow\n",
        encoding="utf-8",
    )
    workflow = {
        "schema_version": "0.3.0",
        "kind": "composite-workflow",
        "steps": steps,
        "verification": {
            "final_outputs": [{"path": "result/report.pdf", "type": "publication-pdf"}]
        },
    }
    (workflow_dir / "workflow.yaml").write_text(
        yaml.safe_dump(workflow, sort_keys=False), encoding="utf-8"
    )
    return collection


def _validator_errors(collection: pathlib.Path) -> list[str]:
    workflow_dir = next((collection / "workflows").iterdir())
    return validate_workflows.validate_one(str(workflow_dir), set())


def _gate_messages(collection: pathlib.Path) -> list[str]:
    result = release_gate.check_workflows(collection)
    return [detail["message"] for detail in result.details]


def _assert_valid_in_both(collection: pathlib.Path) -> None:
    assert _validator_errors(collection) == []
    result = release_gate.check_workflows(collection)
    assert result.status == release_gate.PASS, _gate_messages(collection)


def _assert_error_in_both(collection: pathlib.Path, expected: str) -> None:
    assert _validator_errors(collection) == [expected]
    result = release_gate.check_workflows(collection)
    assert result.status == release_gate.FAIL
    assert _gate_messages(collection) == [expected]


def _run_script(
    collection: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> tuple[int, str, str]:
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "validate_workflows.py",
            "--workflows",
            str(collection / "workflows"),
            "--collection",
            str(collection),
        ],
    )
    with pytest.raises(SystemExit) as raised:
        validate_workflows.main()
    captured = capsys.readouterr()
    return raised.value.code, captured.out, captured.err


def test_valid_two_step_chain_passes_both_validators(tmp_path):
    collection = _write_collection(tmp_path, _chain())
    _assert_valid_in_both(collection)
    assert not any(
        "publication-pdf" in message for message in _gate_messages(collection)
    )


def test_type_missing_from_producer_outputs_reports_the_edge(tmp_path):
    collection = _write_collection(
        tmp_path,
        _chain(
            producer_outputs=("catalogue-fits",),
            consumer_inputs=("catalogue-fits", "visibility-table"),
            transferred_types=("catalogue-fits", "visibility-table"),
        ),
    )
    expected = (
        "synthetic-chain/consume: inputs_from producer 'produce' requests type "
        "'visibility-table', but producer outputs declare ['catalogue-fits']"
    )
    _assert_error_in_both(collection, expected)


def test_type_missing_from_consumer_inputs_reports_the_edge(tmp_path):
    collection = _write_collection(
        tmp_path,
        _chain(
            producer_outputs=("calibration-model", "visibility-table"),
            consumer_inputs=("calibration-model",),
            transferred_types=("calibration-model", "visibility-table"),
        ),
    )
    expected = (
        "synthetic-chain/consume: inputs_from producer 'produce' requests type "
        "'visibility-table', but consumer inputs do not declare it; producer outputs "
        "declare ['calibration-model', 'visibility-table']"
    )
    _assert_error_in_both(collection, expected)


def test_empty_inputs_from_type_list_is_valid(tmp_path):
    collection = _write_collection(tmp_path, _chain(transferred_types=()))
    _assert_valid_in_both(collection)


def test_one_matching_type_among_several_producer_outputs_is_valid(tmp_path):
    collection = _write_collection(
        tmp_path,
        _chain(
            producer_outputs=("diagnostic-plot", "visibility-table", "quality-log"),
            consumer_inputs=("visibility-table",),
            transferred_types=("visibility-table",),
        ),
    )
    _assert_valid_in_both(collection)


def test_flavoured_port_reference_matches_declared_type_and_flavour(tmp_path):
    steps = _chain(
        producer_outputs=("visibility-table",),
        consumer_inputs=("visibility-table",),
        transferred_types=("visibility-table:calibrated",),
    )
    steps[0]["outputs"][0]["flavour"] = "calibrated"
    steps[1]["inputs"][0]["flavour"] = "calibrated"
    collection = _write_collection(tmp_path, steps)
    _assert_valid_in_both(collection)


def test_declared_workflow_count_match_passes(tmp_path, monkeypatch, capsys):
    collection = _write_collection(tmp_path, _chain(), workflows_count=1)
    return_code, stdout, stderr = _run_script(collection, monkeypatch, capsys)
    assert return_code == 0, stderr
    assert "1/1 workflows valid; 0 errors" in stdout
    assert "workflows_count mismatch" not in stderr
    assert not any(
        "workflows_count mismatch" in message for message in _gate_messages(collection)
    )


def test_declared_workflow_count_mismatch_names_both_counts(
    tmp_path, monkeypatch, capsys
):
    collection = _write_collection(tmp_path, _chain(), workflows_count=2)
    expected = (
        "collection.yaml workflows_count mismatch: declared 2, "
        "on-disk workflow directories 1"
    )
    return_code, _stdout, stderr = _run_script(collection, monkeypatch, capsys)
    assert return_code == 1
    assert f"ERR {expected}" in stderr
    result = release_gate.check_workflows(collection)
    assert result.status == release_gate.WARN
    assert _gate_messages(collection) == [expected]


def test_declared_count_detects_an_absent_workflows_subtree(
    tmp_path, monkeypatch, capsys
):
    collection = tmp_path / "collection"
    collection.mkdir()
    (collection / "skills_index.json").write_text("[]\n", encoding="utf-8")
    (collection / "collection.yaml").write_text(
        yaml.safe_dump({"workflows_count": 1}), encoding="utf-8"
    )
    expected = (
        "collection.yaml workflows_count mismatch: declared 1, "
        "on-disk workflow directories 0"
    )
    return_code, _stdout, stderr = _run_script(collection, monkeypatch, capsys)
    assert return_code == 1
    assert f"ERR {expected}" in stderr
    result = release_gate.check_workflows(collection)
    assert result.status == release_gate.WARN
    assert expected in _gate_messages(collection)


def test_foreign_discipline_port_vocabulary_is_checked_by_shape(tmp_path):
    collection = _write_collection(
        tmp_path,
        _chain(
            producer_outputs=("calibrated-visibilities", "antenna-gain-table"),
            consumer_inputs=("calibrated-visibilities",),
            transferred_types=("calibrated-visibilities",),
        ),
        workflow_name="radio-interferometry-imaging",
    )
    _assert_valid_in_both(collection)
