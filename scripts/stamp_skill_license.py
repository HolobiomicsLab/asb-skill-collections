"""Stamp metadata.license_tier into every SKILL.md frontmatter and a one-line
license banner (for non-open tiers) just after the H1. Idempotent. Presentation
only — tiers come from a collection index or source leaf; none are inferred here."""

from __future__ import annotations

# Invoked by path (`python scripts/x.py`), only `scripts/` lands on sys.path, so
# the repo root has to be added before the sibling package can be imported.
if __package__ in (None, ""):
    import os.path as _p
    import sys as _sys

    _sys.path.insert(0, _p.dirname(_p.dirname(_p.abspath(__file__))))

import json
import pathlib

import yaml

from asb_skill_collections import layout
from scripts.skill_index import parse_frontmatter

BANNER_MARKER = "<!-- asb-license-banner -->"
_NOTE = {
    "noncommercial": (
        "**License: noncommercial** — confirm your use is a permitted "
        "(noncommercial) purpose before applying; commercial use requires a separate "
        "license (see `metadata.tool_license`)."
    ),
    "restricted": (
        "**License: restricted** — no clear open-source license detected for "
        "the underlying tool; verify licensing before commercial use or redistribution."
    ),
}


def license_banner(tier: str) -> str | None:
    """Return the canonical notice for a tier, or None when no notice applies."""
    note = _NOTE.get(tier)
    return None if note is None else f"> {note} {BANNER_MARKER}"


def _split(text):
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].rstrip("\r\n") != "---":
        return None, None
    for end, line in enumerate(lines[1:], start=1):
        if line.rstrip("\r\n") == "---":
            return "".join(lines[1:end]), "".join(lines[end + 1 :])
    return None, None


def _value_token(tokens, key):
    at = next(
        i
        for i, token in enumerate(tokens)
        if isinstance(token, yaml.ValueToken)
        and token.start_mark.index >= key.end_mark.index
    )
    return tokens[at + 1]


def _guard_shared_anchor(tokens, token):
    if isinstance(token, yaml.AnchorToken) and any(
        isinstance(other, yaml.AliasToken) and other.value == token.value
        for other in tokens
    ):
        raise ValueError(
            "cannot change a shared YAML anchor without altering unrelated fields"
        )


def _value_span(node, key, tokens):
    token = _value_token(tokens, key)
    _guard_shared_anchor(tokens, token)
    if isinstance(token, yaml.AliasToken):
        return token.start_mark.index, token.end_mark.index
    return node.start_mark.index, node.end_mark.index


def _insert_field(fm_raw, mapping, field):
    if mapping.flow_style:
        at = fm_raw.index("{", mapping.start_mark.index, mapping.end_mark.index) + 1
        return fm_raw[:at] + field + (", " if mapping.value else "") + fm_raw[at:]
    first_key = mapping.value[0][0]
    line_start = fm_raw.rfind("\n", 0, first_key.start_mark.index) + 1
    prefix = fm_raw[line_start : first_key.start_mark.index]
    indent = len(prefix) - len(prefix.lstrip())
    at = line_start + indent
    newline = "\r\n" if "\r\n" in fm_raw else "\n"
    return fm_raw[:at] + field + newline + " " * indent + fm_raw[at:]


def _set_mapping_tier(fm_raw, metadata_entry, tier):
    key, metadata = metadata_entry
    field = yaml.safe_dump({"license_tier": tier}, allow_unicode=True).rstrip("\n")
    tier_entry = next(
        ((key, value) for key, value in metadata.value if key.value == "license_tier"),
        None,
    )
    if tier_entry and tier_entry[1].value == tier:
        return fm_raw
    tokens = list(yaml.scan(fm_raw))
    token = _value_token(tokens, key)
    _guard_shared_anchor(tokens, token)
    if isinstance(token, yaml.AliasToken):
        at, end = token.start_mark.index, token.end_mark.index
        return (
            fm_raw[:at] + "{<<: " + fm_raw[at:end] + ", " + field + "}" + fm_raw[end:]
        )
    if tier_entry:
        tier_key, value = tier_entry
        at, end = _value_span(value, tier_key, tokens)
        replacement = field.split(": ", 1)[1]
        if value.style in ("|", ">") and fm_raw[end - 1 : end] == "\n":
            replacement += "\r\n" if "\r\n" in fm_raw else "\n"
        return fm_raw[:at] + replacement + fm_raw[end:]
    return _insert_field(fm_raw, metadata, field)


def _set_tier(fm_raw: str, tier: str) -> str:
    """Preserve YAML bytes; refuse shared anchors that require unrelated edits."""
    root = yaml.compose(fm_raw) or yaml.MappingNode("tag:yaml.org,2002:map", [])
    entry = next(
        ((key, value) for key, value in root.value if key.value == "metadata"), None
    )
    field = yaml.safe_dump({"license_tier": tier}, allow_unicode=True).rstrip("\n")
    if entry is None:
        if root.flow_style:
            return _insert_field(fm_raw, root, "metadata: {" + field + "}")
        newline = "\r\n" if "\r\n" in fm_raw else "\n"
        return fm_raw + "metadata:" + newline + "  " + field + newline
    key, metadata = entry
    if isinstance(metadata, yaml.MappingNode):
        return _set_mapping_tier(fm_raw, entry, tier)
    at, end = _value_span(metadata, key, list(yaml.scan(fm_raw)))
    prefix = " " if fm_raw[at - 1 : at] == ":" else ""
    return fm_raw[:at] + prefix + "{" + field + "}" + fm_raw[end:]


def _set_banner(body: str, banner: str | None) -> str:
    lines = body.splitlines(keepends=True)
    banner_heads = tuple(license_banner(tier).split(" — ", 1)[0] for tier in _NOTE)
    lines = [
        ln
        for ln in lines
        if not (ln.lstrip().startswith(banner_heads) and BANNER_MARKER in ln)
    ]
    if banner is None:
        return "".join(lines)
    idx = next((i for i, ln in enumerate(lines) if ln.lstrip().startswith("# ")), -1)
    at = idx + 1 if idx >= 0 else 0
    if at < len(lines) and not lines[at].strip():
        at += 1
    newline = "\r\n" if "\r\n" in body else "\n"
    if at and not lines[at - 1].endswith(("\n", "\r")):
        lines[at - 1] += newline
    lines.insert(
        at, banner + (newline if at < len(lines) or body.endswith("\n") else "")
    )
    return "".join(lines)


def stamp_skill(md_path, tier: str) -> bool:
    """Set a leaf's tier and canonical notice, changing only the licence signal."""
    p = pathlib.Path(md_path)
    text = p.read_bytes().decode("utf-8")
    fm_raw, body = _split(text)
    if fm_raw is None:
        return False
    new_fm = _set_tier(fm_raw, tier)
    new_body = _set_banner(body, license_banner(tier))
    newline = "\r\n" if text.startswith("---\r\n") else "\n"
    new_text = "---" + newline + new_fm + "---" + newline + new_body
    if new_text == text:
        return False
    p.write_bytes(new_text.encode("utf-8"))
    return True


def stamp_copies(unit_dir, collection_dir) -> list[str]:
    """Refresh copied leaves from their source tier; leave absent declarations alone."""
    unit_dir, collection_dir = pathlib.Path(unit_dir), pathlib.Path(collection_dir)
    if unit_dir.resolve() == collection_dir.resolve():
        return []
    source_root = layout.leaf_dir(collection_dir)
    changed = []
    for copied in sorted(layout.leaf_dir(unit_dir).glob("*/SKILL.md")):
        source = source_root / copied.parent.name / "SKILL.md"
        if not source.is_file():
            continue
        tier = (parse_frontmatter(source).get("metadata") or {}).get("license_tier")
        if tier and stamp_skill(copied, tier):
            changed.append(str(copied.relative_to(unit_dir)))
    return changed


def stamp_all(collection_dir, index_path) -> dict:
    """Stamp every indexed skill, wherever this collection keeps its corpus.

    A router-shaped collection holds its leaves in `leaves/` and only entry
    points in `skills/`. Resolving through the canonical layout means the sweep
    cannot silently stamp nothing and report a clean run, which is what a
    hardcoded `skills/` did here.
    """
    si = json.loads(pathlib.Path(index_path).read_text(encoding="utf-8"))
    roots = list(layout.skill_dirs(pathlib.Path(collection_dir)))
    changed = 0
    tiers: dict[str, int] = {}
    missing: list[str] = []
    for e in si:
        tier = e.get("license_tier")
        md = next(
            (
                r / e["slug"] / "SKILL.md"
                for r in roots
                if (r / e["slug"] / "SKILL.md").is_file()
            ),
            None,
        )
        if not tier:
            continue
        if md is None:
            missing.append(e["slug"])
            continue
        changed += 1 if stamp_skill(md, tier) else 0
        tiers[tier] = tiers.get(tier, 0) + 1
    return {"changed": changed, "tiers": tiers, "indexed_but_absent": len(missing)}


def main(argv=None):
    import argparse

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--collection", required=True, help="collection dir (holds skills_index.json)"
    )
    a = ap.parse_args(argv)
    res = stamp_all(a.collection, f"{a.collection}/skills_index.json")
    print(json.dumps(res, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
