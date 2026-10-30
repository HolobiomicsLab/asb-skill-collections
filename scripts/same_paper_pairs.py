#!/usr/bin/env python3
"""Report same-paper near-duplicate cut outputs without merging them (S6)."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np


MODEL = "BAAI/bge-small-en-v1.5"
MODEL_ALIASES = frozenset({"bge-small-en-v1.5", MODEL})
DEFAULT_THRESHOLDS = "0.95,0.90"
EMBED_VIEW = "name_tools"
PAIR_SCOPE = "same_run_full_pairwise"


class ReportError(RuntimeError):
    """The cut or calibrated report options are invalid."""


class ConflictError(ReportError):
    """The output path contains bytes not owned by this invocation."""


@dataclass(frozen=True)
class CutOutput:
    """The cut fields needed for one embedding and same-paper comparison."""

    output_id: str
    canonical_slug: str
    merge_kind: str
    capsules: tuple[str, ...]
    tools: tuple[str, ...]

    def embedding_text(self) -> str:
        """Render ASB's calibrated name_tools embedding view."""
        name = self.canonical_slug.replace("-", " ").replace("_", " ")
        if not self.tools:
            return name
        return name + "\ntools: " + ", ".join(self.tools)

    def pair_side(self) -> dict[str, str]:
        """Return the stable public identity kept in each pair record."""
        return {
            "output_id": self.output_id,
            "canonical_slug": self.canonical_slug,
            "merge_kind": self.merge_kind,
        }


def _json_bytes(value: Any) -> bytes:
    """Render deterministic human-readable JSON."""
    return (
        json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    ).encode("utf-8")


def _sha256_file(path: Path) -> str:
    """Return the hexadecimal SHA-256 digest of one regular file."""
    if not path.is_file() or path.is_symlink():
        raise ReportError(f"required regular file is missing: {path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _read_json(path: Path) -> Any:
    """Read one required UTF-8 JSON file."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ReportError(f"invalid JSON in {path}: {exc}") from exc


def _required_string(document: dict[str, Any], key: str, path: Path) -> str:
    """Return one required non-empty string field."""
    value = document.get(key)
    if not isinstance(value, str) or not value:
        raise ReportError(f"{path} requires non-empty string {key}")
    return value


def _string_list(value: Any, label: str) -> tuple[str, ...]:
    """Validate an ordered list of non-empty strings."""
    if not isinstance(value, list) or any(
        not isinstance(item, str) or not item for item in value
    ):
        raise ReportError(f"{label} must be a list of non-empty strings")
    return tuple(value)


def _load_output(directory: Path) -> tuple[CutOutput, dict[str, Any]]:
    """Load one output's coverage identity and name_tools inputs."""
    coverage_path = directory / "coverage.json"
    coverage = _read_json(coverage_path)
    tools = _read_json(directory / "tools.json")
    if not isinstance(coverage, dict):
        raise ReportError(f"coverage must be an object: {coverage_path}")
    output_id = _required_string(coverage, "output_id", coverage_path)
    if output_id != directory.name:
        raise ReportError(f"coverage output_id differs from directory: {directory}")
    record = CutOutput(
        output_id=output_id,
        canonical_slug=_required_string(coverage, "canonical_slug", coverage_path),
        merge_kind=_required_string(coverage, "merge_kind", coverage_path),
        capsules=tuple(sorted(set(_string_list(coverage.get("capsules"), "capsules")))),
        tools=_string_list(tools, f"tools in {directory / 'tools.json'}"),
    )
    if not record.capsules:
        raise ReportError(f"coverage has no capsules: {coverage_path}")
    return record, coverage


def _load_cut(view: Path) -> tuple[Path, list[CutOutput], str]:
    """Load and cross-check every output below a cut corpus."""
    resolved = view.resolve(strict=True)
    skills = resolved / "skills"
    if not resolved.is_dir() or not skills.is_dir() or skills.is_symlink():
        raise ReportError(f"view is not a cut corpus: {resolved}")
    summary_path = skills / "coverage_summary.json"
    summary = _read_json(summary_path)
    if not isinstance(summary, dict):
        raise ReportError(f"coverage summary must be an object: {summary_path}")
    loaded = [_load_output(path) for path in sorted(skills.iterdir()) if path.is_dir()]
    outputs = [item[0] for item in loaded]
    coverage = {item[0].output_id: item[1] for item in loaded}
    if summary != coverage:
        raise ReportError("coverage_summary.json differs from output coverage files")
    if not outputs:
        raise ReportError(f"no cut outputs found under {skills}")
    return resolved, outputs, _sha256_file(summary_path)


def _parse_thresholds(value: str) -> tuple[float, float]:
    """Parse calibrated auto-merge and suggestion thresholds."""
    try:
        fields = value.split(",")
        if len(fields) != 2:
            raise ValueError
        auto_merge, suggest = (float(field) for field in fields)
    except ValueError as exc:
        raise ReportError("thresholds must be two comma-separated numbers") from exc
    if not 1.0 >= auto_merge >= suggest > 0.0:
        raise ReportError("thresholds must satisfy 1 >= auto_merge >= suggest > 0")
    return auto_merge, suggest


def _validate_model(value: str) -> str:
    """Require the model on which Decision 7 thresholds were calibrated."""
    if value not in MODEL_ALIASES:
        raise ReportError("model must be bge-small-en-v1.5 or BAAI/bge-small-en-v1.5")
    return MODEL


def _offline_environment() -> None:
    """Pin local model loading and remove provider credentials."""
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    os.environ["ASB_EMBED_MODEL"] = "bge-small-en-v1.5"
    for key in ("OPENAI_API_KEY", "OPENROUTER_API_KEY", "ANTHROPIC_API_KEY"):
        os.environ.pop(key, None)


def _embed(outputs: list[CutOutput]) -> np.ndarray:
    """Embed all output views with the pinned local sentence transformer."""
    _offline_environment()
    from sentence_transformers import SentenceTransformer

    encoder = SentenceTransformer(MODEL)
    vectors = encoder.encode(
        [output.embedding_text() for output in outputs],
        normalize_embeddings=True,
        batch_size=64,
        show_progress_bar=False,
    )
    matrix = np.asarray(vectors, dtype=np.float64)
    if matrix.ndim != 2 or matrix.shape[0] != len(outputs):
        raise ReportError(f"unexpected embedding shape: {matrix.shape}")
    if not np.isfinite(matrix).all():
        raise ReportError("embedding matrix contains non-finite values")
    norms = np.linalg.norm(matrix, axis=1)
    if np.any(norms <= 0.0):
        raise ReportError("embedding matrix contains a zero-norm row")
    return matrix / norms[:, None]


def _edges(
    outputs: list[CutOutput], matrix: np.ndarray, suggest: float
) -> list[tuple[float, int, int, str]]:
    """Score each unordered output pair once per shared source run."""
    by_run: dict[str, list[int]] = defaultdict(list)
    for index, output in enumerate(outputs):
        for run in output.capsules:
            by_run[run].append(index)
    edges: list[tuple[float, int, int, str]] = []
    for run in sorted(by_run):
        indices = by_run[run]
        if len(indices) < 2:
            continue
        similarities = matrix[indices] @ matrix[indices].T
        rows, columns = np.triu_indices(len(indices), 1)
        for row, column in zip(rows, columns, strict=True):
            score = float(similarities[row, column])
            if score >= suggest:
                edges.append((score, indices[row], indices[column], run))
    edges.sort(key=lambda edge: _edge_key(edge, outputs))
    return edges


def _edge_key(
    edge: tuple[float, int, int, str], outputs: list[CutOutput]
) -> tuple[Any, ...]:
    """Return the deterministic score, run, and identity ordering key."""
    score, left, right, run = edge
    return (-score, run, outputs[left].output_id, outputs[right].output_id)


def _pair_record(
    edge: tuple[float, int, int, str], outputs: list[CutOutput]
) -> dict[str, Any]:
    """Render one threshold-qualified same-paper edge."""
    score, left, right, run = edge
    return {
        "score": round(score, 6),
        "run": run,
        "left": outputs[left].pair_side(),
        "right": outputs[right].pair_side(),
    }


def _component_counts(
    output_count: int,
    edges: list[tuple[float, int, int, str]],
    threshold: float,
) -> tuple[int, int]:
    """Count connected components and removable surplus at one threshold."""
    parent = list(range(output_count))
    involved: set[int] = set()

    def find(node: int) -> int:
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    for score, left, right, _ in edges:
        if score < threshold:
            continue
        involved.update((left, right))
        left_root, right_root = find(left), find(right)
        if left_root != right_root:
            parent[right_root] = left_root
    components = len({find(node) for node in involved})
    return components, len(involved) - components


def _build_report(
    view: Path,
    model: str,
    auto_merge: float,
    suggest: float,
) -> dict[str, Any]:
    """Measure a complete deterministic same-paper report."""
    resolved, outputs, coverage_digest = _load_cut(view)
    matrix = _embed(outputs)
    edges = _edges(outputs, matrix, suggest)
    high = [edge for edge in edges if edge[0] >= auto_merge]
    band = [edge for edge in edges if edge[0] < auto_merge]
    high_components, high_surplus = _component_counts(len(outputs), edges, auto_merge)
    suggest_components, suggest_surplus = _component_counts(
        len(outputs), edges, suggest
    )
    runs = {run for output in outputs for run in output.capsules}
    return {
        "model": model,
        "thresholds": {
            "auto_merge": auto_merge,
            "suggest": suggest,
            "embed_view": EMBED_VIEW,
            "pair_scope": PAIR_SCOPE,
        },
        "view": str(resolved),
        "input_digests": {
            "coverage_summary_sha256": coverage_digest,
            "outputs": len(outputs),
        },
        "skills": len(outputs),
        "runs": len(runs),
        "pairs_ge_0_95": [_pair_record(edge, outputs) for edge in high],
        "pairs_0_90_to_0_95": [_pair_record(edge, outputs) for edge in band],
        "components_ge_0_95": high_components,
        "components_ge_0_90": suggest_components,
        "surplus_leaves": {
            "ge_0_95": high_surplus,
            "ge_0_90": suggest_surplus,
        },
        "auto_merges_applied": False,
    }


def _output_status(path: Path, expected: bytes) -> str:
    """Classify the requested output without changing it."""
    if not path.exists() and not path.is_symlink():
        return "absent"
    if path.is_symlink() or not path.is_file():
        return "conflict"
    return "identical" if path.read_bytes() == expected else "conflict"


def _write_new(path: Path, payload: bytes) -> None:
    """Create a new report without replacing a concurrent writer's bytes."""
    if path.parent.exists() and not path.parent.is_dir():
        raise ConflictError(f"output parent is not a directory: {path.parent}")
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("xb") as handle:
            handle.write(payload)
    except FileExistsError as exc:
        raise ConflictError(f"output appeared during write: {path}") from exc


def _summary(report: dict[str, Any], status: str, dry_run: bool) -> dict[str, Any]:
    """Return the concise command status without timing metadata."""
    return {
        "dry_run": dry_run,
        "output_status": status,
        "model": report["model"],
        "skills": report["skills"],
        "runs": report["runs"],
        "pairs_ge_0_95": len(report["pairs_ge_0_95"]),
        "pairs_0_90_to_0_95": len(report["pairs_0_90_to_0_95"]),
        "components_ge_0_95": report["components_ge_0_95"],
        "components_ge_0_90": report["components_ge_0_90"],
        "surplus_leaves": report["surplus_leaves"],
    }


def _parser() -> argparse.ArgumentParser:
    """Build the public S6 command-line parser."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--view", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--model", default="bge-small-en-v1.5")
    parser.add_argument("--thresholds", default=DEFAULT_THRESHOLDS)
    parser.add_argument("--dry-run", action="store_true")
    return parser


def _run(options: argparse.Namespace) -> int:
    """Validate, measure, and conditionally write one duplicate report."""
    model = _validate_model(options.model)
    auto_merge, suggest = _parse_thresholds(options.thresholds)
    report = _build_report(options.view, model, auto_merge, suggest)
    payload = _json_bytes(report)
    output = Path(os.path.abspath(options.out))
    status = _output_status(output, payload)
    if status == "conflict":
        raise ConflictError(f"existing output differs: {output}")
    if not options.dry_run and status == "absent":
        _write_new(output, payload)
        status = "written"
    print(json.dumps(_summary(report, status, options.dry_run), sort_keys=True))
    return 0


def main(argv: list[str] | None = None) -> int:
    """Run S6 with exit 0 success, 1 failure, and 2 conflict."""
    try:
        return _run(_parser().parse_args(argv))
    except ConflictError as exc:
        print(f"CONFLICT: {exc}", file=sys.stderr)
        return 2
    except (ReportError, OSError, UnicodeError, TypeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
