"""Deterministic normalizer for a community-contributed ASB skill.

Mirrors the CI gates so a contributed SKILL.md can be checked + assembled into a
schema-correct, community-tier frontmatter *before* a human reviews it. Pure
logic + frontmatter parsing — no network, no fabrication of content. The EDAM
IRIs and the description prose are the contributor's (or the command's LLM)
responsibility; this module asserts/assembles structure only.

Reuses ``scripts.stamp_skill_license._split`` for frontmatter parsing and the
tier vocabularies from ``scripts.license_tier`` / ``scripts.provenance_tier``.

See governance/PROVENANCE_TIERS.md and governance/LICENSE_TIERS.md.
"""
from __future__ import annotations

import copy
import re

import yaml

from scripts.provenance_tier import VALID as VALID_PROVENANCE
from scripts.stamp_skill_license import _split

# CI parity (see plan "## Global Constraints" + governance gates).
EDAM_PREFIX = "http://edamontology.org/"
DESC_PREFIXES = ("Use when", "Reference for", "Explains", "Decision support for")
DESC_MIN, DESC_MAX = 50, 300
MARKETING_TERMS = ("best", "state-of-the-art", "revolutionary", "leading", "superior")
VALID_LICENSE_TIERS = {"open", "noncommercial", "restricted"}
# Co-authorship attribution roles for the optional ``contributors`` block:
# ``author`` (a tool's author who contributed the skill), ``reviewer`` (vetted
# it), ``curator`` (a maintainer who staged/shaped it). See governance/AUTHORSHIP.md.
VALID_CONTRIBUTOR_ROLES = {"author", "reviewer", "curator"}
# Well-formed contributor keys: ``name``/``role`` required, ``orcid``/``github``
# optional. Only these keys are emitted into a normalized block.
CONTRIBUTOR_KEYS = ("name", "role", "orcid", "github")


def slugify(name: str) -> str:
    """Lowercase, hyphenate, strip non-alphanumerics. Idempotent on slugs."""
    s = (name or "").lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def valid_edam(iri) -> bool:
    """True iff ``iri`` is a canonical EDAM IRI (``http://edamontology.org/...``)."""
    return isinstance(iri, str) and iri.startswith(EDAM_PREFIX) and len(iri) > len(EDAM_PREFIX)


def check_description(desc) -> list[str]:
    """Return violation strings for the description discipline (empty = valid).

    Checks: allowed prefix, 50–300 chars, no marketing terms.
    """
    violations: list[str] = []
    if not isinstance(desc, str) or not desc.strip():
        return ["description missing"]
    text = desc.strip()
    if not text.startswith(DESC_PREFIXES):
        violations.append(
            f"description prefix must be one of {DESC_PREFIXES}"
        )
    n = len(text)
    if n < DESC_MIN:
        violations.append(f"description too short ({n} < {DESC_MIN} chars)")
    elif n > DESC_MAX:
        violations.append(f"description too long ({n} > {DESC_MAX} chars)")
    low = text.lower()
    # Substring match for CI parity with validate.yml Gate 5
    # (`if term.lower() in desc.lower()`), not word-boundary — the gate the
    # contributed skill must satisfy after the PR is opened uses substrings.
    for term in MARKETING_TERMS:
        if term in low:
            violations.append(f"description uses marketing term {term!r}")
    return violations


def parse_skill_md(text: str) -> tuple[dict | None, str | None]:
    """Split a SKILL.md into ``(frontmatter_dict, body)``.

    Returns ``(None, None)`` when there is no leading ``---`` frontmatter block
    (reuses ``stamp_skill_license._split``).
    """
    fm_raw, body = _split(text)
    if fm_raw is None:
        return None, None
    return (yaml.safe_load(fm_raw) or {}), body


def frontmatter_violations(fm: dict) -> list[str]:
    """Validate description + EDAM IRIs + license_tier against the CI gates."""
    violations: list[str] = []
    fm = fm or {}
    violations.extend(check_description(fm.get("description")))

    meta = fm.get("metadata") or {}

    op = meta.get("edam_operation")
    if op is not None and not valid_edam(op):
        violations.append(f"invalid EDAM operation IRI: {op!r}")
    topics = meta.get("edam_topics") or []
    if not isinstance(topics, list):
        # A bare string (or other scalar) would iterate per-character and emit
        # one violation per char; emit a single clear message instead.
        violations.append("edam_topics must be a list")
    else:
        for topic in topics:
            if not valid_edam(topic):
                violations.append(f"invalid EDAM topic IRI: {topic!r}")

    tier = meta.get("license_tier")
    if tier not in VALID_LICENSE_TIERS:
        violations.append(
            f"invalid license_tier {tier!r} (must be one of {sorted(VALID_LICENSE_TIERS)})"
        )
    return violations


def contributor_violations(contributors) -> list[str]:
    """Validate an optional ``contributors`` block (empty = valid/absent).

    The block is OPTIONAL: ``None`` (absent) yields no violations. When present
    it must be a list of mappings, each with a non-empty ``name`` and a ``role``
    in :data:`VALID_CONTRIBUTOR_ROLES`. ``orcid``/``github`` are optional and not
    further validated here. See governance/AUTHORSHIP.md.
    """
    if contributors is None:
        return []
    violations: list[str] = []
    if not isinstance(contributors, list):
        return ["contributors must be a list"]
    for i, entry in enumerate(contributors):
        if not isinstance(entry, dict):
            violations.append(f"contributor[{i}] must be a mapping")
            continue
        name = entry.get("name")
        if not (isinstance(name, str) and name.strip()):
            violations.append(f"contributor[{i}] missing non-empty name")
        role = entry.get("role")
        if role not in VALID_CONTRIBUTOR_ROLES:
            violations.append(
                f"contributor[{i}] role {role!r} not in {sorted(VALID_CONTRIBUTOR_ROLES)}"
            )
    return violations


def normalized_frontmatter(
    raw_fm: dict,
    *,
    related_skills,
    tools_used,
    license_tier: str,
    provenance_tier: str = "community",
    status: str = "hold",
    derived_from=None,
    contributors=None,
) -> dict:
    """Assemble a schema-correct community frontmatter from ``raw_fm``.

    Preserves the contributor's ``name``/``description`` and the provided EDAM
    block (does NOT fabricate them). Sets the metadata tier block plus
    ``related_skills``/``tools_used``/``status``/``provenance_tier``/
    ``license_tier``. ``derived_from`` is included only when provided. Does not
    mutate ``raw_fm``.

    ``contributors`` (the co-authorship attribution block) is emitted only when
    provided. Each entry is reduced to its well-formed keys
    (:data:`CONTRIBUTOR_KEYS`: ``name``/``role`` required, ``orcid``/``github``
    optional; unknown keys dropped); the input is not mutated.
    """
    if provenance_tier not in VALID_PROVENANCE:
        raise ValueError(f"invalid provenance_tier {provenance_tier!r}")
    src = copy.deepcopy(raw_fm or {})
    src_meta = src.get("metadata") if isinstance(src.get("metadata"), dict) else {}

    meta: dict = {}
    # Preserve provided EDAM/tool/technique content (do not fabricate).
    for key in ("edam_operation", "edam_topics", "tools", "techniques"):
        if key in src_meta:
            meta[key] = src_meta[key]
    meta["license_tier"] = license_tier
    meta["provenance_tier"] = provenance_tier
    meta["tools_used"] = list(tools_used)

    fm: dict = {}
    if "name" in src:
        fm["name"] = src["name"]
    if "description" in src:
        fm["description"] = src["description"]
    fm["license"] = src.get("license", "CC-BY-4.0")
    fm["metadata"] = meta
    fm["status"] = status
    # provenance_tier == community requires the related_skills KEY present (even if empty).
    fm["related_skills"] = list(related_skills)
    if derived_from is not None:
        fm["derived_from"] = copy.deepcopy(derived_from)
    if contributors is not None:
        emitted: list[dict] = []
        for entry in contributors:
            src_entry = entry if isinstance(entry, dict) else {}
            emitted.append(
                {k: src_entry[k] for k in CONTRIBUTOR_KEYS if k in src_entry}
            )
        fm["contributors"] = emitted
    return fm


def main(argv=None) -> int:
    import argparse
    import json
    import pathlib

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--skill-md", required=True, help="path to a SKILL.md to validate")
    a = ap.parse_args(argv)
    fm, _ = parse_skill_md(pathlib.Path(a.skill_md).read_text(encoding="utf-8"))
    if fm is None:
        print(json.dumps({"violations": ["no frontmatter block"]}, indent=2))
        return 1
    v = frontmatter_violations(fm)
    print(json.dumps({"violations": v}, indent=2))
    return 1 if v else 0


if __name__ == "__main__":
    raise SystemExit(main())
