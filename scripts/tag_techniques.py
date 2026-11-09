#!/usr/bin/env python3
"""Tag collection leaves by platform mentions without reformatting content."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import yaml

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.normalize_skill import parse_skill_md
from scripts.domain_rules import resolve_rules_path


GENERATOR_VERSION = "1.0.0"
RULES_PATH = Path(__file__).parent / "rules" / "metabolomics" / "technique_rules.yaml"
FIELDS = ("name", "description", "tools", "body")


@dataclass(frozen=True)
class TechniqueRule:
    tag: str
    name: str
    regex: str
    fields: tuple[str, ...]
    pattern: re.Pattern


@dataclass(frozen=True)
class Rules:
    version: str
    vocabulary: tuple[str, ...]
    rules: tuple[TechniqueRule, ...]


@dataclass
class Row:
    slug: str
    leaf: Path
    text: str
    frontmatter: dict
    body: str
    fields: dict[str, str]
    existing_tags: list[str]
    matches: dict[str, list[dict[str, str]]]

    @property
    def tags(self):
        return sorted(self.matches)


def load_rules(path):
    document = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    vocabulary = tuple(document["vocabulary"])
    rules = []
    for tag, entries in document["vocabulary"].items():
        for entry in entries:
            fields = tuple(entry["fields"])
            if not fields or any(field not in FIELDS for field in fields):
                raise ValueError(f"Unknown or empty fields for {tag}/{entry['rule']}")
            rules.append(
                TechniqueRule(
                    tag=tag,
                    name=entry["rule"],
                    regex=entry["regex"],
                    fields=fields,
                    pattern=re.compile(entry["regex"], re.IGNORECASE),
                )
            )
    return Rules(str(document["rules_version"]), vocabulary, tuple(rules))


def tool_names(value):
    names = []
    for entry in value or []:
        if isinstance(entry, dict):
            entry = entry.get("name", "")
        if entry is not None:
            names.append(str(entry))
    return names


def find_leaf(collection, slug):
    candidates = [collection / "leaves" / slug / "SKILL.md", collection / "skills" / slug / "SKILL.md"]
    matches = [path for path in candidates if path.is_file()]
    if len(matches) != 1:
        raise ValueError(f"Expected one leaf for {slug}, found {len(matches)}")
    return matches[0]


def load_rows(collection, rules=None, selected=None):
    collection = Path(collection)
    index_rows = json.loads((collection / "skills_index.json").read_text(encoding="utf-8"))
    rows = []
    for index_row in index_rows:
        leaf = find_leaf(collection, index_row["slug"])
        text = leaf.read_text(encoding="utf-8")
        frontmatter, body = parse_skill_md(text)
        if frontmatter is None:
            raise ValueError(f"Missing frontmatter: {leaf}")
        metadata = frontmatter.get("metadata") or {}
        tools = metadata.get("tools") or frontmatter.get("tools") or index_row.get("tools") or []
        fields = {
            "name": str(frontmatter.get("name") or index_row.get("name") or index_row["slug"]),
            "description": str(frontmatter.get("description") or index_row.get("description") or ""),
            "tools": " ".join(tool_names(tools)),
            "body": body,
        }
        existing = metadata.get("techniques")
        if existing is None:
            existing = frontmatter.get("techniques", index_row.get("techniques", []))
        row = Row(index_row["slug"], leaf, text, frontmatter, body, fields, existing or [], {})
        if rules is not None:
            row.matches = match_row(row, rules, selected)
        rows.append(row)
    return rows


def match_row(row, rules, selected=None):
    selected = set(rules.vocabulary if selected is None else selected)
    unknown = selected.difference(rules.vocabulary)
    if unknown:
        raise ValueError(f"Tags outside declared vocabulary: {', '.join(sorted(unknown))}")
    matches = {}
    for rule in rules.rules:
        if rule.tag not in selected:
            continue
        for field in rule.fields:
            match = rule.pattern.search(row.fields[field])
            if match:
                matches.setdefault(rule.tag, []).append(
                    {
                        "rule": rule.name,
                        "field": field,
                        "match": match.group(0),
                        "start": match.start(),
                        "end": match.end(),
                    }
                )
    return matches


def annotate(text, rules):
    fields = {field: text for field in FIELDS}
    row = Row("example", Path("SKILL.md"), "", {}, text, fields, [], {})
    return {tag: [match["rule"] for match in matches] for tag, matches in match_row(row, rules).items()}


def replace_yaml_list(text, tags, target="metadata"):
    lines = text.splitlines(keepends=True)
    if len(lines) < 2 or lines[0].strip() != "---":
        raise ValueError("Leaf has no frontmatter")
    end = next((number for number in range(1, len(lines)) if lines[number].strip() == "---"), None)
    if end is None:
        raise ValueError("Unterminated frontmatter")
    frontmatter = yaml.safe_load("".join(lines[1:end])) or {}
    if target == "metadata" and not isinstance(frontmatter.get("metadata"), dict):
        raise ValueError("Leaf has no metadata mapping")
    if target == "inline":
        match = re.search(r"\btechniques:\s*[^}\r\n]+", text[: sum(map(len, lines[:end]))])
        if not match:
            raise ValueError("Leaf has no inline techniques field")
        rendered = "[" + ", ".join(tags) + "]"
        return text[: match.start()] + "techniques: " + rendered + text[match.end():]
    indent = "  " if target == "metadata" else ""
    start = None
    inline = re.compile(rf"^{re.escape(indent)}techniques:(.*?)(\r?\n)?$")
    for number in range(1, end):
        match = inline.match(lines[number])
        if not match:
            continue
        remainder = match.group(1)
        if remainder.strip():
            rendered = json.dumps(tags, ensure_ascii=False)
            lines[number] = f"{indent}techniques: {rendered}{match.group(2) or ''}"
            return "".join(lines)
        start = number
        break
    if start is not None:
        next_number = start + 1
        while next_number < end:
            stripped = lines[next_number].lstrip(" \t")
            current_indent = len(lines[next_number]) - len(stripped)
            if stripped.strip() and current_indent == len(indent) and not stripped.startswith("- "):
                break
            if stripped.strip() and current_indent < len(indent):
                break
            next_number += 1
        newline = "\r\n" if lines[start].endswith("\r\n") else "\n"
        replacement = [f"{indent}techniques: []{newline}" if not tags else f"{indent}techniques:{newline}"]
        replacement.extend(f"{indent}- {tag}{newline}" for tag in tags)
        lines[start:next_number] = replacement
        return "".join(lines)
    insertion = end
    if target == "metadata":
        metadata_line = re.compile(r"^metadata:\s*(?:#.*)?(?:\r?\n)?$")
        metadata_start = next(
            (number for number in range(1, end) if metadata_line.match(lines[number])), None
        )
        if metadata_start is None:
            raise ValueError("Leaf has no block metadata mapping")
        insertion = metadata_start + 1
        while insertion < end:
            stripped = lines[insertion].lstrip(" \t")
            if stripped.strip() and not lines[insertion].startswith((" ", "\t")):
                break
            insertion += 1
    newline = "\r\n" if text.startswith("---\r\n") else "\n"
    addition = [f"{indent}techniques: []{newline}" if not tags else f"{indent}techniques:{newline}"]
    addition.extend(f"{indent}- {tag}{newline}" for tag in tags)
    lines[insertion:insertion] = addition
    return "".join(lines)


def strip_techniques(text):
    inline = re.compile(r"^(metadata:\s*\{)(.*)(\}\s*(?:\r?\n)?)$")
    lines = text.splitlines(keepends=True)
    for number, line in enumerate(lines):
        if re.match(r"^\s*techniques:\s*\[\]\s*(?:\r?\n)?$", line):
            return "".join(lines[:number] + lines[number + 1:])
    for number, line in enumerate(lines):
        match = inline.match(line)
        if match and re.search(r"(?:^|,\s*)techniques:\s*\[[^]]*\]", match.group(2)):
            content = re.sub(r"(?:^|,\s*)techniques:\s*\[[^]]*\]", "", match.group(2), count=1)
            content = re.sub(r",\s*,", ",", content).strip()
            content = re.sub(r",\s*$", "", content)
            lines[number] = match.group(1) + content + match.group(3)
            return "".join(lines)
    lines = text.splitlines(keepends=True)
    end = next(number for number in range(1, len(lines)) if lines[number].strip() == "---")
    start = next(
        (number for number in range(1, end) if re.match(r"^\s*techniques:\s*(?:\r?\n)?$", lines[number])),
        None,
    )
    if start is None:
        return text
    indent = len(lines[start]) - len(lines[start].lstrip())
    stop = start + 1
    while stop < end:
        stripped = lines[stop].lstrip()
        current_indent = len(lines[stop]) - len(stripped)
        if stripped.strip() and current_indent == indent and not stripped.startswith("- "):
            break
        if stripped.strip() and current_indent < indent:
            break
        stop += 1
    return "".join(lines[:start] + lines[stop:])


def replace_json_field(text, slug, field, value):
    opening, row_end = index_row_spans(text)[slug]
    return replace_json_field_at(text, opening, row_end, slug, field, value)


def replace_json_field_at(text, opening, row_end, slug, field, value):
    match = re.search(rf'{re.escape(json.dumps(field))}\s*:', text[opening:row_end])
    if match is None:
        raise ValueError(f"Index row {slug} has no {field} field")
    colon = opening + match.end() - 1
    start = colon + 1 + len(text[colon + 1:]) - len(text[colon + 1:].lstrip())
    _, end = json.JSONDecoder().raw_decode(text, start)
    replacement = json.dumps(value, ensure_ascii=False)
    return text[:start] + replacement + text[end:]


def index_row_spans(text):
    decoder = json.JSONDecoder()
    spans = {}
    depth = 0
    in_string = False
    escaped = False
    opening = None
    for position, character in enumerate(text):
        if in_string:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
            continue
        if character == '"':
            in_string = True
        elif character in "[{":
            depth += 1
            if character == "{" and depth == 2:
                opening = position
        elif character in "]}":
            if character == "}" and depth == 2:
                row, end = decoder.raw_decode(text, opening)
                if isinstance(row.get("slug"), str):
                    spans[row["slug"]] = (opening, end)
                opening = None
            depth -= 1
    return spans


def insert_json_field(text, slug, field, value):
    opening, end = index_row_spans(text)[slug]
    row_text = text[opening:end]
    key_match = re.search(r"\n(\s*)\"", row_text)
    if key_match:
        indent = key_match.group(1)
        line_start = opening + key_match.start() + 1
        addition = f'{indent}{json.dumps(field)}: {json.dumps(value, ensure_ascii=False)},\n'
        return text[:line_start] + addition + text[line_start:]
    insertion = end - 1
    prefix = ", " if row_text.strip() != "{}" else ""
    return text[:insertion] + f'{prefix}{json.dumps(field)}: {json.dumps(value, ensure_ascii=False)}' + text[insertion:]


def set_json_techniques(text, row, tags):
    return set_json_techniques_at(text, index_row_spans(text), row, tags)


def set_json_techniques_at(text, spans, row, tags):
    opening, end = spans[row.slug]
    row_text = text[opening:end]
    if not re.search(r'"techniques"\s*:', row_text):
        return insert_json_field(text, row.slug, "techniques", tags)
    return replace_json_field_at(text, opening, end, row.slug, "techniques", tags)


def excerpt(field_text, match):
    start = max(0, match["start"] - 120)
    end = min(len(field_text), match["end"] + 180)
    return " ".join(field_text[start:end].split())


def investigation_samples(path=None):
    """Read the investigation's spot-check slugs per tag when a receipt is given."""
    if path is None or not Path(path).is_file():
        return {}
    document = json.loads(path.read_text(encoding="utf-8"))
    return {
        tag: [entry["slug"] for entry in entries]
        for tag, entries in document.get("v3_spot_check", {}).items()
    }


def write_packet(rows, rules, output, sample_size, seed, selected, spot_check_evidence=None):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    by_slug = {row.slug: row for row in rows}
    spot_checks = investigation_samples(spot_check_evidence)
    rng = random.Random(seed)
    for tag in selected:
        tagged = [row for row in rows if tag in row.matches]
        sampled = rng.sample(tagged, min(sample_size, len(tagged)))
        chosen = list(sampled)
        seen = {row.slug for row in chosen}
        for slug in spot_checks.get(tag, []):
            if slug in by_slug and slug not in seen and tag in by_slug[slug].matches:
                chosen.append(by_slug[slug])
                seen.add(slug)
        filename = tag.lower().replace("/", "-") + ".md"
        lines = [f"# Review packet: {tag}", "", f"Rules version: {rules.version}", ""]
        for row in chosen:
            source = "investigation spot-check" if row.slug in spot_checks.get(tag, []) else "random sample"
            lines.extend([f"## {row.slug}", "", f"Source: {source}", ""])
            for match in row.matches[tag]:
                lines.extend(
                    [
                        f"- Rule `{match['rule']}`, field `{match['field']}`: "
                        f"{excerpt(row.fields[match['field']], match)}",
                        "",
                    ]
                )
        (output / filename).write_text("\n".join(lines), encoding="utf-8")


def receipt(collection, rules_path, rules, rows, selected, write, generated_at):
    collection = Path(collection)
    counts = Counter(tag for row in rows for tag in row.matches)
    return {
        "generator": {"name": "scripts/tag_techniques.py", "version": GENERATOR_VERSION},
        "generated_at": generated_at,
        "mode": "write" if write else "dry-run",
        "input": {
            "collection": str(collection),
            "skills_index_sha256": hashlib.sha256((collection / "skills_index.json").read_bytes()).hexdigest(),
            "leaf_count": len(rows),
        },
        "rules": {
            "path": str(rules_path),
            "version": rules.version,
            "sha256": hashlib.sha256(Path(rules_path).read_bytes()).hexdigest(),
        },
        "selection": list(selected),
        "per_tag": {tag: counts[tag] for tag in selected},
        "totals": {
            "leaves": len(rows),
            "tagged": sum(bool(row.matches) for row in rows),
            "untagged": sum(not row.matches for row in rows),
        },
        "leaves": [
            {
                "slug": row.slug,
                "tags": row.tags,
                "matches": [
                    {"tag": tag, **match}
                    for tag in rules.vocabulary
                    for match in row.matches.get(tag, [])
                ],
            }
            for row in rows
        ],
    }


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--collection", type=Path, required=True)
    parser.add_argument("--rules", type=Path, default=RULES_PATH)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--only")
    parser.add_argument("--sample", type=int)
    parser.add_argument("--seed", type=int, default=45045)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--spot-check-evidence", type=Path)
    arguments = parser.parse_args(argv)
    if (arguments.sample is None) != (arguments.out is None):
        parser.error("--sample and --out must be used together")
    if arguments.sample is not None and arguments.sample < 0:
        parser.error("--sample must be nonnegative")
    return arguments


def main(argv=None):
    arguments = parse_args(argv)
    try:
        arguments.rules = resolve_rules_path(arguments.collection, "technique_rules.yaml", arguments.rules)
        rules = load_rules(arguments.rules)
    except ValueError as exc:
        raise SystemExit(f"error: {exc}") from exc
    selected = arguments.only.split(",") if arguments.only else list(rules.vocabulary)
    selected_set = set(selected)
    rows = load_rows(arguments.collection, rules, selected)
    if arguments.write:
        index_path = arguments.collection / "skills_index.json"
        index_text = index_path.read_text(encoding="utf-8")
        index_rows = {row["slug"]: row for row in json.loads(index_text)}
        spans = index_row_spans(index_text)
        for row in rows:
            preserved = sorted(
                set(row.existing_tags).intersection(rules.vocabulary).difference(selected_set).union(row.tags)
            )
            metadata = row.frontmatter.get("metadata")
            metadata_tags = (metadata.get("techniques") or []) if isinstance(metadata, dict) else []
            if set(preserved) == set(metadata_tags) and set(preserved) == set(
                index_rows[row.slug].get("techniques") or []
            ):
                continue
            has_metadata = isinstance(metadata, dict) and (
                "techniques" in metadata or re.search(r"^metadata:\s*(?:#.*)?$", row.text, re.MULTILINE)
            )
            if has_metadata:
                updated = replace_yaml_list(row.text, preserved)
            elif isinstance(metadata, dict) and "techniques" in metadata:
                updated = replace_yaml_list(row.text, row.tags, target="inline")
            else:
                updated = strip_techniques(row.text)
            if updated != row.text:
                row.leaf.write_text(updated, encoding="utf-8")
            previous_length = len(index_text)
            index_text = set_json_techniques_at(index_text, spans, row, preserved)
            difference = len(index_text) - previous_length
            if difference:
                opening, _ = spans[row.slug]
                spans = {
                    slug: (start + difference if start > opening else start, end + difference)
                    for slug, (start, end) in spans.items()
                }
        if index_text != index_path.read_text(encoding="utf-8"):
            index_path.write_text(index_text, encoding="utf-8")
    generated_at = datetime.now(timezone.utc).isoformat()
    summary = receipt(arguments.collection, arguments.rules, rules, rows, selected, arguments.write, generated_at)
    print(json.dumps({key: summary[key] for key in ("per_tag", "totals")}, indent=2))
    if arguments.report:
        arguments.report.parent.mkdir(parents=True, exist_ok=True)
        arguments.report.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if arguments.sample is not None:
        write_packet(
            rows, rules, arguments.out, arguments.sample, arguments.seed, selected,
            arguments.spot_check_evidence,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
