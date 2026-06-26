"""Synthesizer helper for auto-created **super-skills** (synthetic, or
review-grounded **literature**, provenance).

The deterministic half of the ``synthesize-meta-skill`` flow (the agentic
``commands/synthesize-meta-skill.md`` does the identify-the-pipeline + body
writing, then invokes this to cluster, assemble frontmatter, and stage). Three
pieces, all pure logic + the community pipeline's real APIs — no LLM, no git/gh,
no network beyond the *injected* matcher:

* :func:`cluster_subskills` — a thin wrapper over the matcher
  (:func:`scripts.skill_match.match_skills`, injectable for tests) that gathers
  the candidate sub-skills clustered around a pipeline seed plus the tools they
  ground on (via :func:`scripts.skill_match.match_tools`).
* :func:`meta_frontmatter` — assemble a schema-correct ``super`` frontmatter,
  reusing :func:`scripts.normalize_skill.normalized_frontmatter`
  (``status="hold"``) and adding ``metadata.skill_kind="super"`` +
  ``metadata.orchestrates``. The default origin is ``synthetic`` (derived from the
  orchestrated skills); passing a ``review_doi`` instead grounds the pipeline in a
  *review article* → ``provenance_tier="literature"`` with ``metadata.dois`` +
  ``derived_from`` carrying that DOI. ``related_skills`` mirrors ``orchestrates``
  so the result also satisfies the community ``related_skills``-key expectation.
  Yields zero :func:`scripts.normalize_skill.frontmatter_violations`.
* :func:`stage_meta_skill` — stage the synthesized SKILL.md + a
  ``wave-meta-skills-<date>.yaml`` ledger, **reusing
  :mod:`scripts.propose_skill`'s** idempotent writers (DRY; same proposals rail).
  No git/gh side effects.

See governance/META_SKILLS.md, governance/PROVENANCE_TIERS.md, and the design
doc (docs/superpowers/specs/2026-06-26-synthetic-meta-skill-design.md).
"""
from __future__ import annotations

import json
import pathlib

import yaml

from scripts import propose_skill
from scripts.normalize_skill import normalized_frontmatter
from scripts.skill_match import match_skills, match_tools


def _load_index(collection_dir, filename: str) -> list[dict]:
    """Load a JSON index file (``skills_index.json`` / ``tools_index.json``).

    Never raises — a missing/garbled file yields an empty index (callers degrade
    to no tool suggestions), tolerating a wrapped ``{"skills": [...]}`` shape.
    """
    p = pathlib.Path(str(collection_dir)) / filename
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001 — degrade gracefully like the matcher
        return []
    if isinstance(data, dict):
        data = data.get("skills") or data.get("tools") or data.get("entries") or []
    return data if isinstance(data, list) else []


def cluster_subskills(
    seed_text: str,
    collection_dir,
    *,
    k: int = 15,
    matcher=None,
) -> dict:
    """Cluster the candidate sub-skills + tools around a pipeline ``seed_text``.

    Runs the matcher (default :func:`scripts.skill_match.match_skills`, injectable
    so tests can pass a network-free fake) to gather up to ``k`` related sub-skills,
    then resolves the tools those sub-skills ground on (plus lexical tool-name hits
    in ``seed_text``) via :func:`scripts.skill_match.match_tools`.

    Returns ``{"subskills": [{slug, score, ...}], "tools": [{slug, score}]}`` —
    ``subskills`` is the matcher's output verbatim (so callers keep its ``score``/
    ``backend``); ``tools`` is the ``{slug, score}`` cluster from ``match_tools``.
    """
    matcher = matcher or match_skills
    subskills = list(matcher(seed_text, collection_dir, k=k) or [])

    skills_index = _load_index(collection_dir, "skills_index.json")
    tools_index = _load_index(collection_dir, "tools_index.json")
    matched_slugs = [s.get("slug") for s in subskills if s.get("slug")]
    tools = match_tools(matched_slugs, skills_index, tools_index, text=seed_text)

    return {"subskills": subskills, "tools": tools}


def meta_frontmatter(
    *,
    name: str,
    description: str,
    orchestrates,
    synthesized_from,
    tools_used,
    license_tier: str = "open",
    review_doi: str | None = None,
) -> dict:
    """Assemble a schema-correct super-skill frontmatter (synthetic or literature).

    Reuses :func:`scripts.normalize_skill.normalized_frontmatter` and
    ``status="hold"`` (so the deterministic EDAM/tool/tier assembly is shared with
    the community rail), then layers the super-skill invariants the proposals gate
    checks:

    * ``metadata.skill_kind = "super"``,
    * ``metadata.orchestrates = orchestrates`` (the sub-skill slugs it sequences),
    * ``metadata.synthesized_from = synthesized_from`` (the source skill slugs;
      kept non-empty for the synthetic invariant and as provenance even for a
      review-grounded super-skill).

    Origin (``provenance_tier``):

    * **default (synthetic)** — ``review_doi is None``: the super-skill is derived
      from the skills it orchestrates (``provenance_tier="synthetic"``).
    * **literature** — when a ``review_doi`` is given, the pipeline is grounded in a
      *review article*: ``provenance_tier="literature"``, ``metadata.dois =
      [review_doi]`` (the literature ⇒ ≥1 doi invariant), and
      ``derived_from = [{"doi": review_doi}]``. The super orchestration
      (``skill_kind``/``orchestrates``/``synthesized_from``) is preserved.

    ``related_skills`` mirrors ``orchestrates`` so the super-skill also satisfies
    any community ``related_skills``-key expectation. The result yields zero
    :func:`scripts.normalize_skill.frontmatter_violations`. Inputs are not mutated.
    """
    raw = {"name": name, "description": description}
    if review_doi:
        provenance_tier = "literature"
        derived_from = [{"doi": review_doi}]
    else:
        provenance_tier = "synthetic"
        derived_from = None
    fm = normalized_frontmatter(
        raw,
        related_skills=list(orchestrates),
        tools_used=list(tools_used),
        license_tier=license_tier,
        provenance_tier=provenance_tier,
        status="hold",
        derived_from=derived_from,
    )
    meta = fm["metadata"]
    meta["skill_kind"] = "super"
    meta["orchestrates"] = list(orchestrates)
    meta["synthesized_from"] = list(synthesized_from)
    if review_doi:
        meta["dois"] = [review_doi]
    return fm


def _wave_date(ledger_meta: dict) -> str:
    """Resolve the wave date from ``ledger_meta`` (``date`` or ``submitted_on``).

    Required — there is **no** ``Date.now`` in importable code (mirrors
    :func:`scripts.propose_skill.stage_proposal`); the command/CLI supplies it.
    """
    date = (ledger_meta or {}).get("date") or (ledger_meta or {}).get("submitted_on")
    if not date:
        raise ValueError(
            "stage_meta_skill requires a wave date in ledger_meta "
            "('date' or 'submitted_on', YYYY-MM-DD)"
        )
    return date


def stage_meta_skill(collection_dir, frontmatter: dict, body: str, ledger_meta: dict) -> dict:
    """Stage a synthesized super-skill into the ``proposals/`` rail. Idempotent.

    Delegates to :mod:`scripts.propose_skill` (DRY — the SKILL.md slug/render and
    the ledger insert/merge/idempotence logic are reused, not reimplemented). The
    only difference from the community path is the ledger filename:
    ``proposals/wave-meta-skills-<date>.yaml`` (vs ``wave-skills-<date>.yaml``) so
    auto-synthesized meta-skills land in their own wave. No git/gh side effects.

    Parameters mirror :func:`scripts.propose_skill.stage_proposal`; the wave
    ``date`` is read from ``ledger_meta`` (``date`` / ``submitted_on``).

    Returns ``{"slug", "skill_md", "ledger"}`` — the written paths.
    """
    date = _wave_date(ledger_meta)
    root = pathlib.Path(collection_dir)

    # Reuse propose_skill to resolve the slug + render the SKILL.md text.
    slug = propose_skill._skill_slug(frontmatter, ledger_meta)
    if not slug:
        raise ValueError("cannot determine proposal slug (no name/slug provided)")

    skill_md = root / "proposals" / "skills" / slug / "SKILL.md"
    ledger_path = root / "proposals" / f"wave-meta-skills-{date}.yaml"

    # --- SKILL.md (write only when content changed: idempotent) --------------
    skill_md.parent.mkdir(parents=True, exist_ok=True)
    new_text = propose_skill.render_skill_md(frontmatter, body)
    if not (skill_md.exists() and skill_md.read_text(encoding="utf-8") == new_text):
        skill_md.write_text(new_text, encoding="utf-8")

    # --- wave-meta-skills ledger (insert/replace by slug, slug-sorted) -------
    existing = {}
    if ledger_path.exists():
        existing = yaml.safe_load(ledger_path.read_text(encoding="utf-8")) or {}
    entry = propose_skill._ledger_entry(slug, ledger_meta, date)
    ledger = propose_skill._merge_ledger(existing, entry)
    new_ledger_text = yaml.safe_dump(ledger, sort_keys=False, allow_unicode=True)
    if not (
        ledger_path.exists()
        and ledger_path.read_text(encoding="utf-8") == new_ledger_text
    ):
        ledger_path.write_text(new_ledger_text, encoding="utf-8")

    return {"slug": slug, "skill_md": str(skill_md), "ledger": str(ledger_path)}
