"""Promote a staged skill proposal into the published collection.

The maintainer-side, mechanical half of the curation flow: a staged
``proposals/skills/<slug>/SKILL.md`` (``status: hold``) that has passed review is
*moved* into ``skills/<slug>/SKILL.md`` with ``status: included``, and the three
committed indices are updated so the promoted skill is indistinguishable from a
pipeline-built one:

* ``skills_index.json`` — a new entry derived from the frontmatter
  (``slug, name, description, edam_operation, edam_topics, techniques, tools,
  dois, provenance_tier, tools_used, license_tier``);
* ``kb_bundle.json`` — a new skill record (``dois, tools, kb_slugs, repo_urls,
  license_tier, provenance_tier, tools_used``);
* the SKILL.md is re-stamped (``metadata.provenance_tier`` /
  ``metadata.license_tier``) so it matches its index entry under the
  provenance / license CI gates.

Reuses the existing machinery rather than re-implementing it:
``normalize_skill.parse_skill_md`` (frontmatter parse), ``propose_skill``'s
rendering conventions, ``perspicacite_kb_bind.kb_slug`` (KB-slug derivation),
``propagate_license_tiers.detect_indent`` (indent-preserving JSON),
``stamp_provenance.stamp_skill_provenance`` (frontmatter re-stamp).

Invariants:

* **Idempotent.** An already-promoted slug (present in ``skills_index.json``) is a
  no-op and reported under ``skipped``; JSON files are written only when content
  changes.
* **No git/gh side effects.** A maintainer runs git/gh after reviewing the move.
* **No ``Date.now`` in importable code.** ``promote`` takes ``date`` as an
  argument; only :func:`main` may default it.

See governance/PROVENANCE_TIERS.md and governance/COMMUNITY_SKILLS.md.
"""
from __future__ import annotations

import json
import pathlib

from scripts.normalize_skill import parse_skill_md
from scripts.perspicacite_kb_bind import kb_slug
from scripts.propagate_license_tiers import detect_indent
from scripts.propose_skill import render_skill_md
from scripts.stamp_provenance import stamp_skill_provenance

# skills_index entry fields derived from frontmatter (order = output key order).
_INDEX_KEYS = (
    "slug",
    "name",
    "description",
    "edam_operation",
    "edam_topics",
    "tools",
    "dois",
    "techniques",
    "license_tier",
    "provenance_tier",
    "tools_used",
)


def staged_slugs(collection_dir) -> list[str]:
    """Slugs under ``proposals/skills/`` whose SKILL.md is held (``status: hold``).

    Sorted, deduplicated. A collection with no ``proposals/skills/`` yields []."""
    d = pathlib.Path(collection_dir)
    base = d / "proposals" / "skills"
    if not base.is_dir():
        return []
    out: list[str] = []
    for md in sorted(base.glob("*/SKILL.md")):
        fm, _ = parse_skill_md(md.read_text(encoding="utf-8"))
        if isinstance(fm, dict) and fm.get("status") == "hold":
            out.append(md.parent.name)
    return out


def _index_entry(slug: str, fm: dict) -> dict:
    """Build the skills_index entry for ``slug`` from its frontmatter.

    Pulls the top-level ``description``/``name`` and the ``metadata`` block
    (EDAM, tools, techniques, dois, tiers, tools_used). For a community proposal
    the ``related_skills`` key is carried onto the index so the provenance gate's
    ``validate_entry(community, related_skills=...)`` is satisfied.
    """
    meta = fm.get("metadata") if isinstance(fm.get("metadata"), dict) else {}
    src = {
        "slug": slug,
        "name": fm.get("name") or slug,
        "description": fm.get("description"),
        "edam_operation": meta.get("edam_operation"),
        "edam_topics": list(meta.get("edam_topics") or []),
        "tools": list(meta.get("tools") or []),
        "dois": list(meta.get("dois") or fm.get("dois") or []),
        "techniques": list(meta.get("techniques") or []),
        "license_tier": meta.get("license_tier"),
        "provenance_tier": meta.get("provenance_tier"),
        "tools_used": list(meta.get("tools_used") or []),
    }
    entry = {k: src[k] for k in _INDEX_KEYS}
    # provenance-tier invariants carried onto the index entry.
    if "related_skills" in fm:
        entry["related_skills"] = list(fm.get("related_skills") or [])
    if "synthesized_from" in meta:
        entry["synthesized_from"] = list(meta.get("synthesized_from") or [])
    return entry


def _kb_record(fm: dict) -> dict:
    """Build the kb_bundle skill record from frontmatter (KB slugs from dois)."""
    meta = fm.get("metadata") if isinstance(fm.get("metadata"), dict) else {}
    dois = list(meta.get("dois") or fm.get("dois") or [])
    return {
        "dois": dois,
        "tools": list(meta.get("tools") or []),
        "kb_slugs": [kb_slug(d) for d in dois],
        "repo_urls": list(meta.get("repo_urls") or []),
        "license_tier": meta.get("license_tier"),
        "provenance_tier": meta.get("provenance_tier"),
        "tools_used": list(meta.get("tools_used") or []),
    }


def _load_json(path):
    raw = path.read_text(encoding="utf-8")
    return json.loads(raw), detect_indent(raw)


def _write_json_if_changed(path, obj, indent) -> bool:
    """Write ``obj`` only when the serialization differs. Returns True if written."""
    new = json.dumps(obj, indent=indent, ensure_ascii=False)
    if path.exists() and path.read_text(encoding="utf-8") == new:
        return False
    path.write_text(new, encoding="utf-8")
    return True


def promote(collection_dir, slugs, *, date: str, dry_run: bool = False) -> dict:
    """Promote staged proposal ``slugs`` into the published collection.

    For each slug: move ``proposals/skills/<slug>/SKILL.md`` →
    ``skills/<slug>/SKILL.md`` with ``status`` flipped to ``included``; append a
    ``skills_index.json`` entry + ``kb_bundle.json`` record; re-stamp the SKILL.md
    so it matches its index entry. Idempotent: a slug already present in
    ``skills_index.json`` is a no-op and reported under ``skipped`` (so are slugs
    that are not staged / not held).

    Parameters
    ----------
    collection_dir : path-like
        Collection root (``skills/``, ``proposals/``, the three indices).
    slugs : iterable[str]
        Proposal slugs to promote.
    date : str
        Curation date (``YYYY-MM-DD``). Required (no ``Date.now`` here). Recorded
        for symmetry with the proposal ledger; not embedded in the artifacts.
    dry_run : bool
        When True, write nothing; ``promoted`` lists the slugs that *would* be
        promoted (the plan).

    Returns ``{"promoted": [...], "skipped": [...]}``.
    """
    if not date:
        raise ValueError("promote requires an explicit date (YYYY-MM-DD)")

    d = pathlib.Path(collection_dir)
    si_path = d / "skills_index.json"
    kb_path = d / "kb_bundle.json"

    si, si_indent = _load_json(si_path)
    kb, kb_indent = _load_json(kb_path)
    existing_slugs = {e.get("slug") for e in si}

    promoted: list[str] = []
    skipped: list[str] = []
    promoted_tools: list = []  # (slug, tools_used) — for used_by_skills back-links

    for slug in slugs:
        proposal_md = d / "proposals" / "skills" / slug / "SKILL.md"
        # already published, not staged, or not held → skip (idempotent / safe).
        if slug in existing_slugs or not proposal_md.is_file():
            skipped.append(slug)
            continue
        fm, body = parse_skill_md(proposal_md.read_text(encoding="utf-8"))
        if not isinstance(fm, dict) or fm.get("status") != "hold":
            skipped.append(slug)
            continue

        promoted.append(slug)
        if dry_run:
            continue

        # --- move SKILL.md, flip status hold -> included --------------------- #
        fm = dict(fm)
        fm["status"] = "included"
        published_md = d / "skills" / slug / "SKILL.md"
        published_md.parent.mkdir(parents=True, exist_ok=True)
        published_md.write_text(render_skill_md(fm, body), encoding="utf-8")
        proposal_md.unlink()
        # drop the now-empty proposal directory (best-effort).
        try:
            proposal_md.parent.rmdir()
        except OSError:
            pass

        # --- append index entry + kb record --------------------------------- #
        si.append(_index_entry(slug, fm))
        existing_slugs.add(slug)
        kb.setdefault("skills", {})[slug] = _kb_record(fm)
        promoted_tools.append((slug, (fm.get("metadata") or {}).get("tools_used") or []))

        # --- re-stamp the SKILL.md to match the index (idempotent) ----------- #
        tier = (fm.get("metadata") or {}).get("provenance_tier")
        if tier:
            stamp_skill_provenance(published_md, tier)

    if not dry_run and promoted:
        _write_json_if_changed(si_path, si, si_indent)
        _write_json_if_changed(kb_path, kb, kb_indent)
        _link_used_by_skills(d / "tools_index.json", promoted_tools)

    return {"promoted": promoted, "skipped": skipped}


def _link_used_by_skills(tools_path, promoted_tools) -> None:
    """Keep the tool catalog's inverse index in sync after promotion.

    The forward ``tools_used`` is carried verbatim from the proposal frontmatter
    (curated by the matcher / synthesis); this adds each promoted skill to those
    tools' ``used_by_skills`` so the bidirectional link is consistent — without a
    full DOI re-derive (``enrich_tools_index``), which would drop curated
    community/synthetic links whose skills carry no matching corpus DOI.
    Idempotent: a slug already present is left untouched.
    """
    if not promoted_tools or not tools_path.is_file():
        return
    tools, indent = _load_json(tools_path)
    by_slug = {t.get("slug"): t for t in tools}
    for slug, tools_used in promoted_tools:
        for tool_slug in tools_used:
            tool = by_slug.get(tool_slug)
            if tool is None:
                continue
            ubs = tool.get("used_by_skills") or []
            if slug not in ubs:
                tool["used_by_skills"] = sorted([*ubs, slug])
    _write_json_if_changed(tools_path, tools, indent)


def main(argv=None) -> int:
    import argparse

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--collection",
        required=True,
        help="collection root (skills/ + proposals/ + the three indices)",
    )
    ap.add_argument(
        "--slug",
        action="append",
        default=None,
        dest="slugs",
        help="proposal slug to promote (repeatable; default: all staged/held)",
    )
    ap.add_argument(
        "--date",
        default=None,
        help="curation date YYYY-MM-DD (default: today, only in the CLI)",
    )
    ap.add_argument(
        "--dry-run", action="store_true", help="print the plan; write nothing"
    )
    a = ap.parse_args(argv)

    # Date.now lives ONLY here (the importable promote takes date as arg).
    date = a.date
    if not date:
        import datetime

        date = datetime.date.today().isoformat()

    slugs = a.slugs if a.slugs else staged_slugs(a.collection)
    res = promote(a.collection, slugs, date=date, dry_run=a.dry_run)
    print(json.dumps(res, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
