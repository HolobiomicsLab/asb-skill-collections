"""Stage a community-contributed skill into a collection's ``proposals/`` rail.

The deterministic, mechanical half of the ``propose-skill`` flow (the agentic
``commands/propose-skill.md`` does the matching/grounding/normalization and then
invokes this to write files). This module:

* writes ``proposals/skills/<slug>/SKILL.md`` (frontmatter + body), and
* appends/updates an entry in ``proposals/wave-skills-<date>.yaml`` — the skill
  proposal ledger, schema ``asb-skill-proposals/1.0`` (the skill analogue of the
  paper ``wave-*.yaml`` ledgers).

Invariants:

* **Idempotent.** Re-staging the same slug rewrites the SKILL.md only when the
  content changed and replaces (never duplicates) the slug's ledger entry; the
  ledger ``proposals`` list is kept slug-sorted for byte-stable output.
* **No git/gh side effects.** The shipped command runs git/gh *after* a human
  reviews what this wrote.
* **No ``Date.now`` in importable code.** ``stage_proposal`` requires the wave
  ``date`` as an argument; only :func:`main` (the CLI) may default it.

Reuses :func:`scripts.normalize_skill.slugify` for the proposal directory name.
See governance/COMMUNITY_SKILLS.md and the design doc.
"""
from __future__ import annotations

import pathlib

import yaml

from scripts.normalize_skill import slugify

LEDGER_SCHEMA = "asb-skill-proposals/1.0"


def _skill_slug(frontmatter: dict, ledger_meta: dict) -> str:
    """The proposal slug: explicit ``ledger_meta['slug']`` wins, else slugified
    frontmatter ``name``."""
    slug = (ledger_meta or {}).get("slug")
    if slug:
        return slug
    return slugify((frontmatter or {}).get("name") or "")


def render_skill_md(frontmatter: dict, body: str) -> str:
    """Render ``SKILL.md`` text from frontmatter + body (deterministic)."""
    fm_yaml = yaml.safe_dump(frontmatter or {}, sort_keys=False, allow_unicode=True)
    body = body or ""
    if body and not body.endswith("\n"):
        body += "\n"
    return "---\n" + fm_yaml + "---\n" + body


def _ledger_entry(slug: str, ledger_meta: dict, date: str) -> dict:
    """Build the ledger entry for ``slug`` from ``ledger_meta`` (schema 1.0).

    Stamps ``slug``/``status``/``submitted_on`` from the explicit inputs;
    ``status`` defaults to ``hold`` (the proposal-rail invariant), and a missing
    ``submitted_on`` is filled from the passed wave ``date``.
    """
    entry = dict(ledger_meta or {})
    entry["slug"] = slug
    entry.setdefault("status", "hold")
    entry.setdefault("submitted_on", date)
    return entry


def _merge_ledger(existing: dict, entry: dict) -> dict:
    """Return a ledger dict with ``entry`` inserted/replaced by slug.

    The ``proposals`` list is kept slug-sorted so the serialized file is stable
    regardless of staging order (idempotence).
    """
    ledger = dict(existing or {})
    ledger["schema"] = LEDGER_SCHEMA
    proposals = list(ledger.get("proposals") or [])
    proposals = [e for e in proposals if e.get("slug") != entry["slug"]]
    proposals.append(entry)
    proposals.sort(key=lambda e: e.get("slug") or "")
    ledger["proposals"] = proposals
    return ledger


def stage_proposal(
    collection_dir,
    frontmatter: dict,
    body: str,
    ledger_meta: dict,
    *,
    date: str,
    dry_run: bool = False,
) -> dict:
    """Write the staged SKILL.md + append/update the wave ledger. Idempotent.

    Parameters
    ----------
    collection_dir : path-like
        The collection root (e.g. ``collections/metabolomics/v2``); files land
        under ``<collection_dir>/proposals/``.
    frontmatter, body : dict, str
        The normalized SKILL.md frontmatter and markdown body.
    ledger_meta : dict
        The proposal ledger entry fields (``contributor``, ``related_skills``,
        ``tools_used``, ``license_tier``, ``grounding``, ...). ``slug``/``status``/
        ``submitted_on`` are stamped here.
    date : str
        The wave date (``YYYY-MM-DD``) — selects ``wave-skills-<date>.yaml`` and
        the default ``submitted_on``. Required (no ``Date.now`` here).
    dry_run : bool
        When True, write nothing; return the plan (paths + ``dry_run: True``).

    Returns the written/planned paths: ``{slug, skill_md, ledger, dry_run}``.
    """
    if not date:
        raise ValueError("stage_proposal requires an explicit date (YYYY-MM-DD)")

    root = pathlib.Path(collection_dir)
    slug = _skill_slug(frontmatter, ledger_meta)
    if not slug:
        raise ValueError("cannot determine proposal slug (no name/slug provided)")

    skill_md = root / "proposals" / "skills" / slug / "SKILL.md"
    ledger_path = root / "proposals" / f"wave-skills-{date}.yaml"

    result = {
        "slug": slug,
        "skill_md": str(skill_md),
        "ledger": str(ledger_path),
        "dry_run": bool(dry_run),
    }
    if dry_run:
        return result

    # --- SKILL.md (write only when content changed: idempotent) --------------
    skill_md.parent.mkdir(parents=True, exist_ok=True)
    new_text = render_skill_md(frontmatter, body)
    if not (skill_md.exists() and skill_md.read_text(encoding="utf-8") == new_text):
        skill_md.write_text(new_text, encoding="utf-8")

    # --- wave ledger (insert/replace by slug, slug-sorted) -------------------
    existing = {}
    if ledger_path.exists():
        existing = yaml.safe_load(ledger_path.read_text(encoding="utf-8")) or {}
    entry = _ledger_entry(slug, ledger_meta, date)
    ledger = _merge_ledger(existing, entry)
    new_ledger_text = yaml.safe_dump(ledger, sort_keys=False, allow_unicode=True)
    if not (
        ledger_path.exists()
        and ledger_path.read_text(encoding="utf-8") == new_ledger_text
    ):
        ledger_path.parent.mkdir(parents=True, exist_ok=True)
        ledger_path.write_text(new_ledger_text, encoding="utf-8")

    return result


def main(argv=None) -> int:
    import argparse
    import json

    from scripts.normalize_skill import parse_skill_md

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--collection", required=True, help="collection root (proposals/ written here)"
    )
    ap.add_argument(
        "--skill-md", required=True, help="path to the normalized SKILL.md to stage"
    )
    ap.add_argument(
        "--date",
        default=None,
        help="wave date YYYY-MM-DD (default: today, only in the CLI)",
    )
    ap.add_argument(
        "--dry-run", action="store_true", help="print the plan; write nothing"
    )
    a = ap.parse_args(argv)

    # Date.now lives ONLY here (the importable stage_proposal takes date as arg).
    date = a.date
    if not date:
        import datetime

        date = datetime.date.today().isoformat()

    text = pathlib.Path(a.skill_md).read_text(encoding="utf-8")
    fm, body = parse_skill_md(text)
    if fm is None:
        print(json.dumps({"error": "no frontmatter block in --skill-md"}, indent=2))
        return 1

    meta = fm.get("metadata") or {}
    ledger_meta = {
        "slug": slugify(fm.get("name") or ""),
        "related_skills": list(fm.get("related_skills") or []),
        "tools_used": list(meta.get("tools_used") or []),
        "license_tier": meta.get("license_tier"),
        "status": fm.get("status", "hold"),
    }
    res = stage_proposal(
        a.collection, fm, body, ledger_meta, date=date, dry_run=a.dry_run
    )
    print(json.dumps(res, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
