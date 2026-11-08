"""Measure offline corroboration signals for exact registry name matches."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import re
from collections import Counter
from pathlib import Path
from typing import Iterable

import yaml


REGISTRY_DETECTIONS = {
    "bioconductor-package": "bioconductor",
    "bioconda-package": "bioconda",
}
MIN_DOMAIN_TOKENS = 3
DEFAULT_SEED = 48
DEFAULT_HELD_OUT_FRACTION = 0.30
REGISTRY_SOURCES = {
    "bioconda": "https://conda.anaconda.org/bioconda/channeldata.json",
    "bioconductor": "https://bioc.r-universe.dev/api/packages/{name}",
}


def _class_metrics_schema() -> dict:
    integer = {"type": "integer", "minimum": 0}
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["true_positive", "predicted", "actual", "precision", "recall", "f1"],
        "properties": {
            "true_positive": integer,
            "predicted": integer,
            "actual": integer,
            "precision": {"type": "number"},
            "recall": {"type": "number"},
            "f1": {"type": "number"},
        },
    }


RESULT_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["method", "dataset", "measurements", "records"],
    "properties": {
        "method": {"type": "object"},
        "dataset": {"type": "object"},
        "measurements": {
            "type": "object",
            "additionalProperties": False,
            "required": ["tuning", "held_out"],
            "properties": {
                split: {
                    "type": "object",
                    "additionalProperties": False,
                    "required": [
                        "accepted_matches", "wrong_matches", "contradicted_wrong_matches",
                        "corroborated_accepted_matches", "insufficient", "verdict_counts",
                    ],
                    "properties": {
                        "accepted_matches": {"type": "integer", "minimum": 0},
                        "wrong_matches": {"type": "integer", "minimum": 0},
                        "contradicted_wrong_matches": _class_metrics_schema(),
                        "corroborated_accepted_matches": _class_metrics_schema(),
                        "insufficient": {"type": "integer", "minimum": 0},
                        "verdict_counts": {
                            "type": "object",
                            "additionalProperties": {"type": "integer", "minimum": 0},
                        },
                    },
                }
                for split in ("tuning", "held_out")
            },
        },
        "records": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "tool_slug", "tool_name", "registry", "registry_package", "label",
                    "texts", "signals", "score", "verdict",
                ],
                "properties": {
                    "tool_slug": {"type": "string"},
                    "tool_name": {"type": "string"},
                    "registry": {"enum": list(REGISTRY_SOURCES)},
                    "registry_package": {"type": "string"},
                    "label": {"enum": ["accepted_match", "wrong_match"]},
                    "texts": {
                        "type": "object",
                        "additionalProperties": {"type": "string"},
                    },
                    "signals": {"type": "object"},
                    "score": {"type": "number"},
                    "verdict": {"enum": ["corroborated", "contradicted", "insufficient"]},
                },
            },
        },
        "inputs": {
            "type": "object",
            "additionalProperties": False,
            "required": list(REGISTRY_SOURCES),
            "properties": {
                registry: {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["source", "snapshot_date", "file", "sha256", "retained"],
                    "properties": {
                        "source": {"type": "string"},
                        "snapshot_date": {"type": ["string", "null"]},
                        "file": {"type": ["string", "null"]},
                        "sha256": {"type": ["string", "null"], "pattern": "^[0-9a-f]{64}$"},
                        "retained": {"type": "boolean"},
                    },
                }
                for registry in REGISTRY_SOURCES
            },
        },
    },
}
STOPWORDS = frozenset(
    """
    a about after again against all also am an and any are as at be because been before
    being between both but by can could did do does doing down during each few for from
    further had has have having he her here hers herself him himself his how i if in into
    is it its itself just me more most my myself no nor not now of off on once only or other
    our ours ourselves out over own same she should so some such than that the their theirs
    them themselves then there these they this those through to too under until up very was
    we were what when where which while who whom why will with you your yours yourself
    yourselves using use used uses based provides provide including include includes
    software tool tools package packages application applications method methods approach
    framework system systems implementation open source available new version
    data analysis analyses perform performs performed allow allows inference
    """.split()
)

_TOKEN_PATTERN = re.compile(r"[a-z][a-z0-9]+")
_EVIDENCE_ECOSYSTEM_PATTERNS = {
    "r": (
        re.compile(r"\b(?:library|require)\s*\(", re.I),
        re.compile(r"\b(?:biocmanager::install|install\.packages)\s*\(", re.I),
        re.compile(r"\b(?:in\s+r|r\s+package)\b", re.I),
        re.compile(r"(?:cran\.r-project\.org|bioconductor\.org)", re.I),
        re.compile(r"\.(?:r|rmd)(?:\b|$)", re.I),
    ),
    "python": (
        re.compile(r"\b(?:python|pip\s+install|pip3\s+install)\b", re.I),
        re.compile(r"(?:pypi\.org|pypi\.io|pypi\.python\.org)", re.I),
        re.compile(r"\.py(?:\b|$)", re.I),
    ),
    "conda": (
        re.compile(r"\b(?:conda|mamba|micromamba)\s+install\b", re.I),
        re.compile(r"\benvironment\.ya?ml\b", re.I),
    ),
    "java": (
        re.compile(r"\b(?:java|maven|gradle)\b", re.I),
        re.compile(r"\.jar(?:\b|$)", re.I),
    ),
    "ruby": (
        re.compile(r"\b(?:ruby|gem\s+install)\b", re.I),
        re.compile(r"\.rb(?:\b|$)", re.I),
    ),
}


def normalize_name(value: object) -> str:
    """Return the resolver-compatible comparison key for a package name."""
    return re.sub(r"[^a-z0-9]", "", str(value or "").lower())


def detect_ecosystems(text: str) -> set[str]:
    """Return ecosystems explicitly named by commands, URLs, or file extensions."""
    return {
        ecosystem
        for ecosystem, patterns in _EVIDENCE_ECOSYSTEM_PATTERNS.items()
        if any(pattern.search(text) for pattern in patterns)
    }


def ecosystem_signal(evidence_text: str, registry: str, registry_record: dict) -> dict:
    """Compare explicit ecosystem hints in corpus and registry evidence."""
    evidence_ecosystems = detect_ecosystems(evidence_text)
    registry_ecosystems = _registry_ecosystems(registry, registry_record)
    verdict = _compare_ecosystems(evidence_ecosystems, registry_ecosystems)
    return {
        "evidence_ecosystems": sorted(evidence_ecosystems),
        "registry_ecosystems": sorted(registry_ecosystems),
        "verdict": verdict,
    }


def domain_signal(
    evidence_text: str,
    registry_text: str,
    identity_values: Iterable[str],
    threshold: float,
) -> dict:
    """Compare identity-free informative token sets with binary cosine overlap."""
    identity_tokens = _identity_tokens(identity_values)
    evidence_tokens = _tokens(evidence_text) - identity_tokens
    registry_tokens = _tokens(registry_text) - identity_tokens
    overlap = evidence_tokens & registry_tokens
    score = _cosine_overlap(evidence_tokens, registry_tokens, overlap)
    verdict = _domain_verdict(evidence_tokens, registry_tokens, score, threshold)
    return {
        "score": round(score, 6),
        "threshold": round(threshold, 6),
        "verdict": verdict,
        "evidence_token_count": len(evidence_tokens),
        "registry_token_count": len(registry_tokens),
        "overlap_tokens": sorted(overlap),
    }


def combined_verdict(ecosystem_verdict: str, domain_verdict: str) -> str:
    """Combine two signals, preserving contradiction and explicit insufficiency."""
    verdicts = {ecosystem_verdict, domain_verdict}
    if {"contradicted", "corroborated"} <= verdicts:
        return "insufficient"
    if "contradicted" in verdicts:
        return "contradicted"
    if "corroborated" in verdicts:
        return "corroborated"
    return "insufficient"


def load_labelled_records(
    collection: Path,
    registry_config: Path,
    bioconda_path: Path,
    bioconductor_path: Path,
) -> list[dict]:
    """Reconstruct accepted and excluded matches with their comparison texts."""
    config = _load_yaml(registry_config)
    accepted = _accepted_matches(collection / "tools_index.json")
    excluded = config.get("excluded_matches") or []
    registries = _load_registry_inputs(bioconda_path, bioconductor_path)
    records = [_make_record(collection, item, registries, False) for item in accepted]
    records.extend(_make_record(collection, item, registries, True) for item in excluded)
    return sorted(records, key=lambda item: item["tool_slug"])


def analyse_records(
    records: list[dict],
    seed: int = DEFAULT_SEED,
    held_out_fraction: float = DEFAULT_HELD_OUT_FRACTION,
    inputs: dict | None = None,
) -> dict:
    """Tune a domain threshold and report tuning and held-out measurements."""
    tuning_slugs, held_out_slugs = _split_positive_slugs(records, seed, held_out_fraction)
    threshold, candidates = _choose_threshold(records, tuning_slugs)
    scored = [_score_record(record, threshold) for record in records]
    result = {
        "method": _method_metadata(seed, held_out_fraction, threshold, candidates),
        "dataset": _dataset_metadata(records, tuning_slugs, held_out_slugs),
        "measurements": {
            "tuning": _measure(scored, tuning_slugs),
            "held_out": _measure(scored, held_out_slugs),
        },
        "records": scored,
    }
    if inputs is not None:
        result["inputs"] = inputs
    validate_result(result)
    return result


def main(argv: list[str] | None = None) -> int:
    """Run the offline measurement and write JSON to a file or standard output."""
    args = _parse_args(argv)
    records = load_labelled_records(
        args.collection,
        args.registry_config,
        args.bioconda,
        args.bioconductor,
    )
    result = analyse_records(records, args.seed, args.held_out_fraction)
    result["inputs"] = _input_metadata(args)
    validate_result(result)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--collection", type=Path, required=True)
    parser.add_argument("--registry-config", type=Path, required=True)
    parser.add_argument("--bioconda", type=Path, required=True)
    parser.add_argument("--bioconductor", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--held-out-fraction", type=float, default=DEFAULT_HELD_OUT_FRACTION)
    parser.add_argument("--bioconda-snapshot-date")
    parser.add_argument("--bioconductor-snapshot-date")
    return parser.parse_args(argv)


def _input_metadata(args: argparse.Namespace) -> dict:
    return {
        registry: {
            "source": REGISTRY_SOURCES[registry],
            "snapshot_date": getattr(args, f"{registry}_snapshot_date"),
            "file": getattr(args, registry).name,
            "sha256": _sha256(getattr(args, registry)),
            "retained": True,
        }
        for registry in REGISTRY_SOURCES
    }


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_result(result: dict) -> None:
    """Validate a measurement against the script's JSON output schema."""
    errors = list(_schema_errors(result, RESULT_SCHEMA, "result"))
    if errors:
        raise ValueError("invalid corroboration result: " + "; ".join(errors))


def _schema_errors(value: object, schema: dict, path: str) -> Iterable[str]:
    expected = schema.get("type")
    if expected and not _matches_type(value, expected):
        yield f"{path} has the wrong type"
        return
    if "enum" in schema and value not in schema["enum"]:
        yield f"{path} is not an allowed value"
    if "pattern" in schema and isinstance(value, str) and not re.fullmatch(schema["pattern"], value):
        yield f"{path} has the wrong format"
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if value < schema.get("minimum", value):
            yield f"{path} is below its minimum"
    if isinstance(value, dict):
        yield from _object_schema_errors(value, schema, path)
    if isinstance(value, list) and "items" in schema:
        for index, item in enumerate(value):
            yield from _schema_errors(item, schema["items"], f"{path}[{index}]")


def _object_schema_errors(value: dict, schema: dict, path: str) -> Iterable[str]:
    properties = schema.get("properties", {})
    for key in schema.get("required", []):
        if key not in value:
            yield f"{path}.{key} is required"
    for key, item in value.items():
        if key in properties:
            yield from _schema_errors(item, properties[key], f"{path}.{key}")
        elif schema.get("additionalProperties") is False:
            yield f"{path}.{key} is not allowed"
        elif isinstance(schema.get("additionalProperties"), dict):
            yield from _schema_errors(item, schema["additionalProperties"], f"{path}.{key}")


def _matches_type(value: object, expected: str | list[str]) -> bool:
    types = [expected] if isinstance(expected, str) else expected
    checks = {
        "object": lambda: isinstance(value, dict),
        "array": lambda: isinstance(value, list),
        "string": lambda: isinstance(value, str),
        "integer": lambda: isinstance(value, int) and not isinstance(value, bool),
        "number": lambda: isinstance(value, (int, float)) and not isinstance(value, bool),
        "boolean": lambda: isinstance(value, bool),
        "null": lambda: value is None,
    }
    return any(checks[item]() for item in types)


def _load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _accepted_matches(index_path: Path) -> list[dict]:
    tools = json.loads(index_path.read_text(encoding="utf-8"))
    return [tool for tool in tools if tool.get("license_detection") in REGISTRY_DETECTIONS]


def _load_registry_inputs(bioconda_path: Path, bioconductor_path: Path) -> dict:
    bioconda = json.loads(bioconda_path.read_text(encoding="utf-8"))
    bioconductor = json.loads(bioconductor_path.read_text(encoding="utf-8"))
    return {
        "bioconda": _normalized_records((bioconda.get("packages") or {}).items()),
        "bioconductor": _normalized_records(
            (record.get("Package"), record) for record in bioconductor
        ),
    }


def _normalized_records(items: Iterable[tuple[object, dict]]) -> dict:
    return {normalize_name(name): (str(name), record) for name, record in items if name}


def _make_record(collection: Path, item: dict, registries: dict, is_excluded: bool) -> dict:
    slug = item["tool"] if is_excluded else item["slug"]
    tool = _load_yaml(collection / "tools" / f"{slug}.yaml")
    registry = item["registry"] if is_excluded else REGISTRY_DETECTIONS[item["license_detection"]]
    package_name, registry_record = _find_registry_record(tool, registry, registries)
    evidence_text = _tool_evidence_text(tool)
    registry_text = _registry_description(registry_record)
    return {
        "tool_slug": slug,
        "tool_name": tool.get("name") or slug,
        "registry": registry,
        "registry_package": package_name,
        "label": "wrong_match" if is_excluded else "accepted_match",
        "texts": {
            "tool_evidence": evidence_text,
            "registry_description": registry_text,
            "registry_ecosystem_hints": _registry_hint_text(registry_record),
        },
        "identity_values": [slug, tool.get("name") or "", package_name],
        "registry_record": registry_record,
    }


def _find_registry_record(tool: dict, registry: str, registries: dict) -> tuple[str, dict]:
    index = registries[registry]
    for name in (tool.get("slug"), tool.get("name")):
        match = index.get(normalize_name(name))
        if match:
            return match
    raise ValueError(f"no {registry} record for {tool.get('slug') or tool.get('name')}")


def _tool_evidence_text(tool: dict) -> str:
    parts: list[str] = []
    description = tool.get("description")
    if description:
        parts.append(str(description))
    parts.extend(str(span) for span in tool.get("evidence_spans") or [])
    parts.extend(str(item.get("title")) for item in tool.get("derived_from") or [] if item.get("title"))
    return "\n".join(parts)


def _registry_description(record: dict) -> str:
    fields = ("Title", "Description", "summary", "description")
    return "\n".join(str(record[field]) for field in fields if record.get(field))


def _flatten_values(value: object) -> Iterable[str]:
    if isinstance(value, dict):
        for nested in value.values():
            yield from _flatten_values(nested)
    elif isinstance(value, (list, tuple, set)):
        for nested in value:
            yield from _flatten_values(nested)
    elif value is not None:
        yield str(value)


def _registry_ecosystems(registry: str, record: dict) -> set[str]:
    if registry == "bioconductor":
        return {"r"}
    return detect_ecosystems(_registry_hint_text(record))


def _registry_hint_text(record: dict) -> str:
    hint_fields = ("summary", "description", "home", "dev_url", "source_url", "depends", "requires")
    return "\n".join(_flatten_values({field: record.get(field) for field in hint_fields}))


def _compare_ecosystems(evidence: set[str], registry: set[str]) -> str:
    if not evidence or not registry:
        return "insufficient"
    return "corroborated" if evidence & registry else "contradicted"


def _tokens(text: str) -> set[str]:
    return {token for token in _TOKEN_PATTERN.findall(text.lower()) if token not in STOPWORDS}


def _identity_tokens(values: Iterable[str]) -> set[str]:
    tokens: set[str] = set()
    for value in values:
        tokens.update(_TOKEN_PATTERN.findall(str(value).lower()))
        normalized = normalize_name(value)
        if len(normalized) > 1:
            tokens.add(normalized)
    return tokens


def _cosine_overlap(left: set[str], right: set[str], overlap: set[str]) -> float:
    if not left or not right:
        return 0.0
    return len(overlap) / math.sqrt(len(left) * len(right))


def _domain_verdict(left: set[str], right: set[str], score: float, threshold: float) -> str:
    if len(left) < MIN_DOMAIN_TOKENS or len(right) < MIN_DOMAIN_TOKENS:
        return "insufficient"
    return "corroborated" if score >= threshold else "contradicted"


def _split_positive_slugs(records: list[dict], seed: int, fraction: float) -> tuple[set[str], set[str]]:
    positives = sorted(record["tool_slug"] for record in records if record["label"] == "accepted_match")
    random.Random(seed).shuffle(positives)
    held_out_count = max(1, round(len(positives) * fraction))
    return set(positives[held_out_count:]), set(positives[:held_out_count])


def _threshold_candidates(records: list[dict]) -> list[float]:
    scores: set[float] = set()
    for record in records:
        signal = domain_signal(
            record["texts"]["tool_evidence"],
            record["texts"]["registry_description"],
            record["identity_values"],
            0.0,
        )
        if signal["score"] > 0:
            scores.add(signal["score"])
    return sorted(scores) or [1.0]


def _choose_threshold(records: list[dict], tuning_slugs: set[str]) -> tuple[float, list[float]]:
    tuning_records = [
        record for record in records
        if record["label"] == "wrong_match" or record["tool_slug"] in tuning_slugs
    ]
    candidates = _threshold_candidates(tuning_records)
    ranked: list[tuple[tuple[float, float, float, float], float]] = []
    for threshold in candidates:
        scored = [_score_record(record, threshold) for record in records]
        metrics = _measure(scored, tuning_slugs)
        objective = _threshold_objective(metrics, threshold)
        ranked.append((objective, threshold))
    return max(ranked)[1], candidates


def _threshold_objective(metrics: dict, threshold: float) -> tuple[float, float, float, float]:
    contradicted = metrics["contradicted_wrong_matches"]
    corroborated = metrics["corroborated_accepted_matches"]
    macro_f1 = (contradicted["f1"] + corroborated["f1"]) / 2
    return macro_f1, contradicted["precision"], corroborated["recall"], -threshold


def _score_record(record: dict, threshold: float) -> dict:
    ecosystem = ecosystem_signal(
        record["texts"]["tool_evidence"], record["registry"], record["registry_record"]
    )
    domain = domain_signal(
        record["texts"]["tool_evidence"],
        record["texts"]["registry_description"],
        record["identity_values"],
        threshold,
    )
    return {
        key: value
        for key, value in record.items()
        if key not in {"identity_values", "registry_record"}
    } | {
        "signals": {"ecosystem": ecosystem, "domain": domain},
        "score": domain["score"],
        "verdict": combined_verdict(ecosystem["verdict"], domain["verdict"]),
    }


def _measure(scored: list[dict], positive_slugs: set[str]) -> dict:
    selected = [
        item for item in scored
        if item["label"] == "wrong_match" or item["tool_slug"] in positive_slugs
    ]
    return {
        "accepted_matches": sum(item["label"] == "accepted_match" for item in selected),
        "wrong_matches": sum(item["label"] == "wrong_match" for item in selected),
        "contradicted_wrong_matches": _class_metrics(selected, "wrong_match", "contradicted"),
        "corroborated_accepted_matches": _class_metrics(selected, "accepted_match", "corroborated"),
        "insufficient": sum(item["verdict"] == "insufficient" for item in selected),
        "verdict_counts": dict(sorted(Counter(item["verdict"] for item in selected).items())),
    }


def _class_metrics(items: list[dict], label: str, verdict: str) -> dict:
    true_positive = sum(item["label"] == label and item["verdict"] == verdict for item in items)
    predicted = sum(item["verdict"] == verdict for item in items)
    actual = sum(item["label"] == label for item in items)
    precision = true_positive / predicted if predicted else 0.0
    recall = true_positive / actual if actual else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "true_positive": true_positive,
        "predicted": predicted,
        "actual": actual,
        "precision": round(precision, 6),
        "recall": round(recall, 6),
        "f1": round(f1, 6),
    }


def _method_metadata(seed: int, fraction: float, threshold: float, candidates: list[float]) -> dict:
    return {
        "seed": seed,
        "held_out_positive_fraction": fraction,
        "negative_split": "all five wrong matches appear in both splits",
        "domain_score": "binary cosine over identity-free informative token sets",
        "minimum_domain_tokens_per_text": MIN_DOMAIN_TOKENS,
        "stopwords": sorted(STOPWORDS),
        "threshold": round(threshold, 6),
        "threshold_candidates": candidates,
        "selection_objective": "macro F1, then contradiction precision, corroboration recall, lower threshold",
    }


def _dataset_metadata(records: list[dict], tuning: set[str], held_out: set[str]) -> dict:
    return {
        "accepted_matches": sum(item["label"] == "accepted_match" for item in records),
        "wrong_matches": sum(item["label"] == "wrong_match" for item in records),
        "accepted_by_registry": dict(sorted(Counter(
            item["registry"] for item in records if item["label"] == "accepted_match"
        ).items())),
        "tuning_positive_slugs": sorted(tuning),
        "held_out_positive_slugs": sorted(held_out),
        "wrong_match_slugs": sorted(
            item["tool_slug"] for item in records if item["label"] == "wrong_match"
        ),
    }


if __name__ == "__main__":
    raise SystemExit(main())
