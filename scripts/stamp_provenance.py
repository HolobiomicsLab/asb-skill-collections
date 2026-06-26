"""Propagate provenance_tier onto the committed artifacts.

Backfills ``provenance_tier`` (DEFAULT = ``literature``) onto every skills_index
entry and kb_bundle skill record that carries >=1 doi, and stamps
``metadata.provenance_tier`` into each SKILL.md frontmatter. Field-only — no
banner. Idempotent, indent / key-order preserving. Orthogonal to license_tier
(see scripts/license_tier.py / scripts/propagate_license_tiers.py).
"""
from __future__ import annotations

import json
import pathlib

import yaml

from scripts.propagate_license_tiers import detect_indent
from scripts.provenance_tier import DEFAULT
from scripts.stamp_skill_license import _split


def propagate_indices(skills_index_path, kb_bundle_path) -> dict:
    """Set ``provenance_tier=DEFAULT`` on every skills_index entry and kb_bundle
    skill record that has >=1 doi. Returns ``{tier: count}`` over skills_index.
    Preserves JSON indent (``detect_indent``) and key order. Idempotent."""
    si_path, kb_path = pathlib.Path(skills_index_path), pathlib.Path(kb_bundle_path)
    si_raw = si_path.read_text(encoding="utf-8")
    kb_raw = kb_path.read_text(encoding="utf-8")
    si = json.loads(si_raw)
    kb = json.loads(kb_raw)
    si_indent = detect_indent(si_raw)
    kb_indent = detect_indent(kb_raw)
    summary: dict[str, int] = {}
    for entry in si:
        if entry.get("dois"):
            entry["provenance_tier"] = DEFAULT
            summary[DEFAULT] = summary.get(DEFAULT, 0) + 1
    for rec in (kb.get("skills") or {}).values():
        if rec.get("dois"):
            rec["provenance_tier"] = DEFAULT
    si_path.write_text(
        json.dumps(si, indent=si_indent, ensure_ascii=False), encoding="utf-8"
    )
    kb_path.write_text(
        json.dumps(kb, indent=kb_indent, ensure_ascii=False), encoding="utf-8"
    )
    return summary


def stamp_skill_provenance(md_path, tier: str) -> bool:
    """Set ``metadata.provenance_tier`` in SKILL.md frontmatter (no banner).

    Creates the ``metadata`` dict if missing, guarding a ``metadata: null``
    frontmatter. Round-trips via the license stamper's conventions
    (``yaml.safe_dump(sort_keys=False, allow_unicode=True)``). Returns True iff
    the file changed. Idempotent."""
    p = pathlib.Path(md_path)
    text = p.read_text(encoding="utf-8")
    fm_raw, body = _split(text)
    if fm_raw is None:
        return False
    fm = yaml.safe_load(fm_raw) or {}
    if not isinstance(fm.get("metadata"), dict):
        fm["metadata"] = {}
    fm["metadata"]["provenance_tier"] = tier
    new_text = (
        "---\n"
        + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True)
        + "---\n"
        + body
    )
    if new_text == text:
        return False
    p.write_text(new_text, encoding="utf-8")
    return True


def stamp_all(skills_dir, index_path) -> dict:
    """Stamp each skill's SKILL.md with its index ``provenance_tier``.

    Returns ``{"changed": n, "tiers": {...}}``."""
    si = json.loads(pathlib.Path(index_path).read_text(encoding="utf-8"))
    base = pathlib.Path(skills_dir)
    changed = 0
    tiers: dict[str, int] = {}
    for e in si:
        tier = e.get("provenance_tier")
        md = base / e["slug"] / "SKILL.md"
        if tier and md.is_file():
            changed += 1 if stamp_skill_provenance(md, tier) else 0
            tiers[tier] = tiers.get(tier, 0) + 1
    return {"changed": changed, "tiers": tiers}


def main(argv=None):
    import argparse

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--collection",
        required=True,
        help="dir containing skills/ + skills_index.json + kb_bundle.json",
    )
    a = ap.parse_args(argv)
    prop = propagate_indices(
        f"{a.collection}/skills_index.json", f"{a.collection}/kb_bundle.json"
    )
    res = stamp_all(f"{a.collection}/skills", f"{a.collection}/skills_index.json")
    print(json.dumps({"propagated": prop, **res}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
