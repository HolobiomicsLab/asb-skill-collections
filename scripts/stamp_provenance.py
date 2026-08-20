"""Propagate provenance_tier onto the committed artifacts.

Backfills ``provenance_tier`` onto every skills_index entry and kb_bundle skill
record whose origin can be shown -- ``literature`` from a doi, ``repository``
from a tool repository where there is no paper -- and stamps
``metadata.provenance_tier`` into each SKILL.md frontmatter. Field-only — no
banner. Idempotent, indent / key-order preserving. Orthogonal to license_tier
(see scripts/license_tier.py / scripts/propagate_license_tiers.py).
"""
from __future__ import annotations

import json
import pathlib

import yaml
# Invoked by path (`python scripts/x.py`), only `scripts/` lands on sys.path, so
# the repo root has to be added before the sibling package can be imported.
if __package__ in (None, ""):
    import os.path as _p
    import sys as _sys

    _sys.path.insert(0, _p.dirname(_p.dirname(_p.abspath(__file__))))


from asb_skill_collections import layout
from scripts.propagate_license_tiers import detect_indent
from scripts.provenance_tier import DEFAULT, REPOSITORY
from scripts.stamp_skill_license import _split


def _origin_tier(dois, repo_url) -> str | None:
    """Where this skill's content came from, or None when nothing shows it."""
    if dois:
        return DEFAULT
    return REPOSITORY if str(repo_url or "").strip() else None


def repo_urls(collection_dir) -> dict[str, str]:
    """Each skill's own ``metadata.repo_url``, keyed by slug.

    A skill grounded on a tool's repository rather than on a paper carries no
    DOI, so the literature default cannot describe it -- but the skill knows
    where its content came from.
    """
    out: dict[str, str] = {}
    for md in layout.iter_skill_md(collection_dir):
        try:
            fm = yaml.safe_load(md.read_text(encoding="utf-8").split("---\n", 2)[1]) or {}
        except (OSError, IndexError, yaml.YAMLError):
            continue
        url = (fm.get("metadata") or {}).get("repo_url")
        if str(url or "").strip():
            out[md.parent.name] = url
    return out


def propagate_indices(skills_index_path, kb_bundle_path, repos=None) -> dict:
    """Set each skills_index entry's and kb_bundle record's ``provenance_tier``.

    An entry with >=1 doi is ``literature``; one with no doi but a known
    repository is ``repository``. An entry with neither is left unset, so the
    gate reports it rather than the corpus claiming an origin it cannot show.
    Preserves JSON indent (``detect_indent``) and key order. Idempotent."""
    si_path, kb_path = pathlib.Path(skills_index_path), pathlib.Path(kb_bundle_path)
    si_raw = si_path.read_text(encoding="utf-8")
    kb_raw = kb_path.read_text(encoding="utf-8")
    si = json.loads(si_raw)
    kb = json.loads(kb_raw)
    si_indent = detect_indent(si_raw)
    kb_indent = detect_indent(kb_raw)
    repos = repos or {}
    summary: dict[str, int] = {}
    for entry in si:
        tier = _origin_tier(entry.get("dois"), repos.get(entry.get("slug")))
        if tier:
            entry["provenance_tier"] = tier
            summary[tier] = summary.get(tier, 0) + 1
    for slug, rec in (kb.get("skills") or {}).items():
        tier = _origin_tier(rec.get("dois"), repos.get(slug))
        if tier:
            rec["provenance_tier"] = tier
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


def stamp_all(collection_dir, index_path) -> dict:
    """Stamp each skill's SKILL.md with its index ``provenance_tier``.

    Resolves through the canonical layout: a router-shaped collection keeps its
    corpus in ``leaves/``, and sweeping a hardcoded ``skills/`` there would stamp
    nothing while still reporting a clean run.

    Returns ``{"changed": n, "tiers": {...}, "indexed_but_absent": n}``."""
    si = json.loads(pathlib.Path(index_path).read_text(encoding="utf-8"))
    roots = layout.skill_dirs(pathlib.Path(collection_dir))
    changed = 0
    tiers: dict[str, int] = {}
    missing = 0
    for e in si:
        tier = e.get("provenance_tier")
        if not tier:
            continue
        md = next((r / e["slug"] / "SKILL.md" for r in roots
                   if (r / e["slug"] / "SKILL.md").is_file()), None)
        if md is None:
            missing += 1
            continue
        changed += 1 if stamp_skill_provenance(md, tier) else 0
        tiers[tier] = tiers.get(tier, 0) + 1
    return {"changed": changed, "tiers": tiers, "indexed_but_absent": missing}


def main(argv=None):
    import argparse

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--collection",
        required=True,
        help="collection dir (holds skills_index.json + kb_bundle.json)",
    )
    a = ap.parse_args(argv)
    prop = propagate_indices(
        f"{a.collection}/skills_index.json", f"{a.collection}/kb_bundle.json",
        repo_urls(a.collection),
    )
    res = stamp_all(a.collection, f"{a.collection}/skills_index.json")
    print(json.dumps({"propagated": prop, **res}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
