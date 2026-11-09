#!/usr/bin/env python3
"""Measure, apply, and revert deterministic EDAM corrections."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.edam_vocabulary import EDAM_IRI, load, resolve
from scripts.normalize_skill import parse_skill_md
from scripts.tag_techniques import index_row_spans
from scripts.domain_rules import resolve_rules_path
from asb_skill_collections.layout import leaf_dir


RECEIPT_SCHEMA = "asb-edam-remap/1"
TIERS = ("T1", "T2", "T3", "T3b", "T4")
DOMAIN_RULE_TIERS = {"T3", "T3b", "T4"}


def load_domain_rules(path):
    """Load and validate the foreign vocabulary for tiers T3 through T4."""
    document = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    required = ("rules_version", "foreign_text_pattern", "foreign_tools", "t3b_operations", "t4_operations")
    missing = [key for key in required if key not in document]
    if missing:
        raise ValueError(f"rules file {path} is missing: {', '.join(missing)}")
    return {
        "rules_version": str(document["rules_version"]),
        "foreign_text_pattern": re.compile(document["foreign_text_pattern"], re.IGNORECASE),
        "foreign_tools": set(document["foreign_tools"]),
        "t3b_operations": set(document["t3b_operations"]),
        "t4_operations": set(document["t4_operations"]),
    }


def sha256(path: Path) -> str:
    """Return the hexadecimal SHA256 digest of a file."""
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def proteomics_signal(row: dict, body: str, rules) -> bool:
    """Reproduce the audit's tool, name, description, and body signal."""
    text = " ".join((row.get("name") or "", row.get("description") or "", body))
    tools = {str(tool).strip().lower() for tool in row.get("tools") or []}
    return bool(rules["foreign_text_pattern"].search(text) or tools & rules["foreign_tools"])


def remap_topics(values, vocabulary, tier, row, body, counts, rules=None):
    """Apply topic rules while preserving order and valid identifiers."""
    result = []
    for iri in values or []:
        resolution = resolve(iri, vocabulary)
        if resolution.status in ("wrong_branch", "ghost", "malformed"):
            counts[f"R1_topic_{resolution.status}"] += 1
            counts["R1_topic_removed"] += 1
            continue
        if tier != "T1" and resolution.status == "obsolete":
            replacement = resolution.replaced_by
            if replacement:
                result.append(EDAM_IRI + replacement)
                counts["R2_topic_replaced"] += 1
            else:
                counts["R2_topic_removed"] += 1
            continue
        if tier in DOMAIN_RULE_TIERS and resolution.id == "topic_0121" and not proteomics_signal(row, body, rules):
            counts["R3_topic_0121_removed"] += 1
            continue
        result.append(iri)
    return list(dict.fromkeys(result))


def remap_operation(value, vocabulary, tier, counts, rules=None):
    """Apply operation rules to one nullable scalar value."""
    if not value:
        return value
    resolution = resolve(value, vocabulary)
    if resolution.status in ("wrong_branch", "ghost", "malformed"):
        counts[f"R1_operation_{resolution.status}"] += 1
        counts["R1_operation_removed"] += 1
        return None
    if tier != "T1" and resolution.status == "obsolete":
        if resolution.replaced_by:
            counts["R2_operation_replaced"] += 1
            return EDAM_IRI + resolution.replaced_by
        counts["R2_operation_removed"] += 1
        return None
    removals = rules["t4_operations"] if tier == "T4" else rules["t3b_operations"] if tier == "T3b" else set()
    if resolution.id in removals:
        counts["R5_operation_removed"] += 1
        return None
    return value


def plan_remap(collection: Path, vocabulary_path: Path, tier="T2", rules_path=None):
    """Return every proposed field change without modifying the collection."""
    collection = Path(collection)
    vocabulary = load(vocabulary_path)
    if tier in DOMAIN_RULE_TIERS:
        rules_path = resolve_rules_path(collection, "edam_remap_rules.yaml", rules_path)
        domain_rules = load_domain_rules(rules_path)
    else:
        domain_rules = None
    rows = json.loads((collection / "skills_index.json").read_text(encoding="utf-8"))
    counts = Counter()
    changes = []
    output_rows = []
    touched_papers = set()
    for row in rows:
        leaf = leaf_dir(collection) / row["slug"] / "SKILL.md"
        frontmatter, body = parse_skill_md(leaf.read_text(encoding="utf-8"))
        if frontmatter is None:
            raise ValueError(f"missing frontmatter: {leaf}")
        before = {"edam_topics": row.get("edam_topics") or [], "edam_operation": row.get("edam_operation")}
        after = {
            "edam_topics": remap_topics(before["edam_topics"], vocabulary, tier, row, body or "", counts, domain_rules),
            "edam_operation": remap_operation(before["edam_operation"], vocabulary, tier, counts, domain_rules),
        }
        output_row = dict(row, **after)
        output_rows.append(output_row)
        if after == before:
            continue
        touched_papers.update(row.get("dois") or [])
        for field in ("edam_topics", "edam_operation"):
            if before[field] != after[field]:
                changes.append({
                    "slug": row["slug"], "field": field, "before": before[field],
                    "after": after[field], "rules": field_rules(before[field], after[field], vocabulary, tier, domain_rules),
                })
    counts["R4_topic_3520_removed"] = 0
    totals = {
        "leaves": len(rows), "leaves_touched": len({change["slug"] for change in changes}),
        "papers_touched": len(touched_papers),
        "topic_fields_empty_before": sum(not row.get("edam_topics") for row in rows),
        "topic_fields_empty_after": sum(not row.get("edam_topics") for row in output_rows),
        "operation_fields_empty_before": sum(not row.get("edam_operation") for row in rows),
        "operation_fields_empty_after": sum(not row.get("edam_operation") for row in output_rows),
    }
    return {"vocabulary": vocabulary, "changes": changes, "rule_counts": dict(sorted(counts.items())), "totals": totals, "rows": output_rows, "domain_rules": domain_rules, "rules_path": rules_path}


def field_rules(before, after, vocabulary, tier, domain_rules=None):
    """Name every rule contributing to one changed field."""
    values = before if isinstance(before, list) else [before] if before else []
    rules = set()
    for value in values:
        resolution = resolve(value, vocabulary)
        if resolution.status in ("wrong_branch", "ghost", "malformed"):
            rules.add("R1")
        elif tier != "T1" and resolution.status == "obsolete":
            rules.add("R2")
        elif tier in ("T3", "T3b", "T4") and resolution.id == "topic_0121":
            rules.add("R3")
        elif domain_rules is not None and resolution.id in (domain_rules["t4_operations"] if tier == "T4" else domain_rules["t3b_operations"] if tier == "T3b" else set()):
            rules.add("R5")
    return sorted(rules)


def replace_yaml_field(text, field, value, indent=""):
    """Replace one frontmatter scalar or list without reformatting its neighbors."""
    lines = text.splitlines(keepends=True)
    end = next(number for number, line in enumerate(lines[1:], 1) if line.strip() == "---")
    pattern = re.compile(rf"^{re.escape(indent)}{re.escape(field)}:(.*?)(\r?\n)?$")
    start = next((number for number in range(1, end) if pattern.match(lines[number])), None)
    if start is None:
        raise ValueError(f"missing {indent}{field} frontmatter field")
    stop = start + 1
    while stop < end:
        stripped = lines[stop].lstrip(" \t")
        current = len(lines[stop]) - len(stripped)
        if stripped.strip() and current == len(indent) and not stripped.startswith("- "):
            break
        if stripped.strip() and current < len(indent):
            break
        stop += 1
    newline = "\r\n" if lines[start].endswith("\r\n") else "\n"
    if isinstance(value, list):
        replacement = [f"{indent}{field}: []{newline}" if not value else f"{indent}{field}:{newline}"]
        replacement.extend(f"{indent}- {item}{newline}" for item in value)
    else:
        rendered = "null" if value is None else str(value)
        replacement = [f"{indent}{field}: {rendered}{newline}"]
    return "".join(lines[:start] + replacement + lines[stop:])


def rewrite_leaf(path, fields):
    """Rewrite all four mirrored EDAM fields in one leaf."""
    text = path.read_text(encoding="utf-8")
    frontmatter, _ = parse_skill_md(text)
    for field, value in fields.items():
        if field in frontmatter:
            text = replace_yaml_field(text, field, value)
        text = replace_yaml_field(text, field, value, indent="  ")
    path.write_text(text, encoding="utf-8")


def rewrite_index(path, changes):
    """Apply row-local JSON field replacements from bottom to top."""
    text = path.read_text(encoding="utf-8")
    spans = index_row_spans(text)
    edits = []
    for change in changes:
        opening, end = spans[change["slug"]]
        match = re.search(rf'{json.dumps(change["field"])}\s*:', text[opening:end])
        if not match:
            raise ValueError(f"index row {change['slug']} has no {change['field']}")
        colon = opening + match.end() - 1
        start = colon + 1 + len(text[colon + 1:]) - len(text[colon + 1:].lstrip())
        _, finish = json.JSONDecoder().raw_decode(text, start)
        edits.append((start, finish, json.dumps(change["after"], ensure_ascii=False)))
    for start, finish, value in sorted(edits, reverse=True):
        text = text[:start] + value + text[finish:]
    path.write_text(text, encoding="utf-8")


def replace_collection_topics(path, topics):
    """Regenerate the top-level edam_topics block and preserve all other YAML bytes."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    start = next(number for number, line in enumerate(lines) if re.match(r"^edam_topics:\s*(?:\r?\n)?$", line))
    stop = start + 1
    while stop < len(lines) and (not lines[stop].strip() or lines[stop].startswith((" ", "\t", "- "))):
        stop += 1
    newline = "\r\n" if lines[start].endswith("\r\n") else "\n"
    replacement = [f"edam_topics:{newline}"] + [f"- {topic}{newline}" for topic in sorted(set(topics))]
    path.write_text("".join(lines[:start] + replacement + lines[stop:]), encoding="utf-8")


def restore_collection_topics(path, block):
    """Restore the exact original aggregate block captured in the receipt."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    start = next(number for number, line in enumerate(lines) if re.match(r"^edam_topics:\s*(?:\r?\n)?$", line))
    stop = start + 1
    while stop < len(lines) and (not lines[stop].strip() or lines[stop].startswith((" ", "\t", "- "))):
        stop += 1
    path.write_text("".join(lines[:start]) + block + "".join(lines[stop:]), encoding="utf-8")


def collection_topics_block(text):
    """Extract the exact top-level aggregate block for reversible writes."""
    aggregate_start = text.index("edam_topics:")
    lines = text[aggregate_start:].splitlines(keepends=True)
    block = []
    for line in lines:
        if block and line.strip() and not line.startswith((" ", "\t", "- ")):
            break
        block.append(line)
    return "".join(block)


def leaf_original_fields(text):
    """Read the original metadata fields needed to reverse a touched leaf."""
    frontmatter, _ = parse_skill_md(text)
    metadata = frontmatter.get("metadata") or {}
    return {field: metadata.get(field) for field in ("edam_operation", "edam_topics")}


def top_counts(rows):
    """Return the five most frequent topic and operation identifiers."""
    topics = Counter(iri for row in rows for iri in row.get("edam_topics") or [])
    operations = Counter(row["edam_operation"] for row in rows if row.get("edam_operation"))
    return {
        "topics": [{"iri": iri, "id": iri.rsplit("/", 1)[-1], "count": count} for iri, count in topics.most_common(5)],
        "operations": [{"iri": iri, "id": iri.rsplit("/", 1)[-1], "count": count} for iri, count in operations.most_common(5)],
    }


def make_receipt(collection, vocabulary_path, plan, tier, write, generated_at):
    """Build a complete dry-run or write receipt."""
    leaves = sorted(leaf_dir(collection).glob("*/SKILL.md"))
    leaf_hashes = {path.relative_to(collection).as_posix(): sha256(path) for path in leaves}
    combined = hashlib.sha256("".join(f"{name}\0{digest}\n" for name, digest in leaf_hashes.items()).encode()).hexdigest()
    tools_path = Path(collection) / "tools_index.json"
    tool_changes = plan_tools(tools_path, plan["vocabulary"], tier) if tools_path.is_file() else []
    manifest_text = (Path(collection) / "collection.yaml").read_text(encoding="utf-8")
    manifest = yaml.safe_load(manifest_text)
    leaf_texts = {slug: (leaf_dir(collection) / slug / "SKILL.md").read_text(encoding="utf-8") for slug in {change["slug"] for change in plan["changes"]}}
    tools_text = tools_path.read_text(encoding="utf-8") if tools_path.is_file() else None
    rules_receipt = None
    if plan.get("rules_path") is not None:
        rules_receipt = {"path": str(plan["rules_path"]), "sha256": sha256(plan["rules_path"]), "version": plan["domain_rules"]["rules_version"]}
    return {
        "schema": RECEIPT_SCHEMA, "generated_at": generated_at, "tier": tier, "write": write,
        "rules": rules_receipt,
        "vocabulary": {"release": plan["vocabulary"]["release"], "release_inferred": plan["vocabulary"]["release_inferred"], "sha256": sha256(vocabulary_path)},
        "input_sha256": {"skills_index.json": sha256(Path(collection) / "skills_index.json"), "collection.yaml": sha256(Path(collection) / "collection.yaml"), "leaves": combined},
        "rule_counts": plan["rule_counts"], "totals": plan["totals"], "changes": plan["changes"],
        "tools_changes": tool_changes, "collection_edam_topics_before": manifest.get("edam_topics") or [],
        "collection_edam_topics_block_before": collection_topics_block(manifest_text),
        "revert": {
            "leaves": {slug: leaf_original_fields(text) for slug, text in leaf_texts.items()},
            "tools_index_text_before": tools_text,
            "skills_index_text_before": (Path(collection) / "skills_index.json").read_text(encoding="utf-8"),
        },
        "top_five": top_counts(plan["rows"]),
    }


def write_receipt(path, receipt):
    """Write a stable, human-reviewable JSON receipt."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def apply_plan(collection, plan):
    """Apply a plan to leaves, indexes, and the collection aggregate."""
    collection = Path(collection)
    changed = {change["slug"] for change in plan["changes"]}
    rows = {row["slug"]: row for row in plan["rows"]}
    for slug in sorted(changed):
        row = rows[slug]
        rewrite_leaf(leaf_dir(collection) / slug / "SKILL.md", {field: row[field] for field in ("edam_operation", "edam_topics")})
    rewrite_index(collection / "skills_index.json", plan["changes"])
    replace_collection_topics(collection / "collection.yaml", [iri for row in plan["rows"] for iri in row.get("edam_topics") or []])
    tools_path = collection / "tools_index.json"
    if tools_path.is_file():
        tool_changes = plan_tools(tools_path, plan["vocabulary"], plan.get("tier", "T2"))
        if tool_changes:
            rewrite_index(tools_path, tool_changes)


def plan_tools(path, vocabulary, tier):
    """Plan only the fields actually present in tools_index.json."""
    rows = json.loads(path.read_text(encoding="utf-8"))
    changes = []
    counts = Counter()
    for row in rows:
        if "edam_topics" in row:
            before = row.get("edam_topics") or []
            after = remap_topics(before, vocabulary, tier, row, "", counts)
            if before != after:
                changes.append({"slug": row["slug"], "field": "edam_topics", "before": before, "after": after, "rule": "R1/R2"})
        if "edam_operation" in row:
            before = row.get("edam_operation")
            after = remap_operation(before, vocabulary, tier, counts)
            if before != after:
                changes.append({"slug": row["slug"], "field": "edam_operation", "before": before, "after": after, "rule": "R1/R2"})
    return changes


def run_remap(options):
    """Measure a tier, optionally write it, and always emit its receipt."""
    plan = plan_remap(options.collection, options.vocabulary, options.tier, options.rules)
    plan["tier"] = options.tier
    receipt = make_receipt(options.collection, options.vocabulary, plan, options.tier, options.write, options.date)
    if not options.write:
        receipt.pop("revert", None)
    if not options.write:
        write_receipt(options.receipt, receipt)
        print(json.dumps({"tier": options.tier, **plan["totals"], "rule_counts": plan["rule_counts"]}, indent=2))
        return 0
    apply_plan(options.collection, plan)
    if plan["changes"] or not options.receipt.is_file():
        write_receipt(options.receipt, receipt)
    print(json.dumps({"tier": options.tier, **plan["totals"], "rule_counts": plan["rule_counts"]}, indent=2))
    return 0


def revert(options):
    """Restore before values from a write receipt, including the aggregate."""
    receipt = json.loads(options.receipt.read_text(encoding="utf-8"))
    if receipt.get("schema") != RECEIPT_SCHEMA or not receipt.get("write"):
        raise ValueError("revert requires a write receipt")
    if not receipt.get("collection_edam_topics_block_before") or "revert" not in receipt:
        raise ValueError("write receipt lacks the original bytes required for revert")
    collection = options.collection
    for slug, fields in receipt["revert"]["leaves"].items():
        rewrite_leaf(leaf_dir(collection) / slug / "SKILL.md", fields)
    inverse = [dict(change, after=change["before"], before=change["after"]) for change in receipt["changes"]]
    (collection / "skills_index.json").write_text(receipt["revert"]["skills_index_text_before"], encoding="utf-8")
    restore_collection_topics(collection / "collection.yaml", receipt["collection_edam_topics_block_before"])
    if receipt.get("tools_changes"):
        (collection / "tools_index.json").write_text(receipt["revert"]["tools_index_text_before"], encoding="utf-8")
    print(f"reverted {len(inverse)} field changes")


def parser():
    """Declare remap and receipt-only revert commands."""
    result = argparse.ArgumentParser(description=__doc__)
    subcommands = result.add_subparsers(dest="command")
    remap = subcommands.add_parser("remap")
    for target in (result, remap):
        target.add_argument("--collection", type=Path)
        target.add_argument("--vocabulary", type=Path, default=Path(__file__).parent / "data" / "edam_vocabulary.json")
        target.add_argument("--tier", choices=TIERS, default="T2")
        target.add_argument("--rules", type=Path)
        target.add_argument("--write", action="store_true")
        target.add_argument("--receipt", type=Path)
        target.add_argument("--date", required=target is remap)
    undo = subcommands.add_parser("revert")
    undo.add_argument("--receipt", type=Path, required=True)
    undo.add_argument("--collection", type=Path, required=True)
    return result


def main(argv=None):
    """Run the selected deterministic remap operation."""
    options = parser().parse_args(argv)
    if options.command == "revert":
        revert(options)
        return 0
    if not options.collection or not options.receipt:
        parser().error("--collection and --receipt are required")
    try:
        return run_remap(options)
    except ValueError as exc:
        raise SystemExit(f"error: {exc}") from exc


if __name__ == "__main__":
    raise SystemExit(main())
