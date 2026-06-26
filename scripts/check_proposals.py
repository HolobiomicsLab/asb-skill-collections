"""CI gate: every staged skill proposal is structurally valid.

Validates each ``proposals/skills/*/SKILL.md`` against the SAME discipline a
published skill must satisfy, plus the proposal invariants, so a maintainer's
review is about quality/fit — not structure. A staged proposal is valid under ANY
of the three provenance origins (reusing the ``scripts.provenance_tier`` kernel):

* **community** — ``metadata.provenance_tier == "community"`` and a
  ``related_skills`` key is present (the community provenance invariant);
* **synthetic** — ``metadata.provenance_tier == "synthetic"`` and
  ``metadata.synthesized_from`` is a non-empty list (auto-derived from other
  skills; see governance/PROVENANCE_TIERS.md);
* **literature** — ``metadata.provenance_tier == "literature"`` and
  ``metadata.dois`` carries >=1 source DOI (e.g. a review-grounded super-skill
  whose pipeline is distilled from a review article).

For every staged skill, regardless of origin:

* top-level ``status == "hold"`` (the proposal-rail invariant);
* ``normalize_skill.frontmatter_violations`` is empty (description discipline,
  EDAM IRI shape, valid ``license_tier``);
* every ``metadata.tools_used`` slug resolves in ``tools_index.json``;
* ``metadata.skill_kind`` ∈ {``skill``, ``super``} (default ``skill`` when
  absent). A ``super`` skill orchestrates sub-skills: ``metadata.orchestrates``
  must be a non-empty list and EVERY orchestrated slug must resolve to a real
  skill in ``skills_index.json``.
* an OPTIONAL top-level ``contributors`` block (co-authorship attribution); when
  present each entry must be a mapping with a non-empty ``name`` and a ``role``
  ∈ {``author``, ``reviewer``, ``curator``}. Absence is fine (not required).

A collection with no ``proposals/`` (or no staged skills) yields no violations.
``main`` exits 1 on any violation, 0 otherwise. Mirrors
scripts/check_tools_index.py and scripts/check_provenance_tiers.py.
"""
from __future__ import annotations

import json
import pathlib
import sys

import yaml

from scripts.normalize_skill import contributor_violations, frontmatter_violations
from scripts.provenance_tier import validate_entry as validate_provenance

# A super-skill orchestrates other skills; a plain skill stands alone.
VALID_SKILL_KINDS = {"skill", "super"}
DEFAULT_SKILL_KIND = "skill"


def check_collection(collection_dir) -> list:
    d = pathlib.Path(collection_dir)
    violations: list = []

    skills_dir = d / "proposals" / "skills"
    if not skills_dir.is_dir():
        return violations

    md_files = sorted(skills_dir.glob("*/SKILL.md"))
    if not md_files:
        return violations

    # tool slugs available to resolve tools_used against.
    tool_slugs: set = set()
    tools_path = d / "tools_index.json"
    if tools_path.is_file():
        tools = json.loads(tools_path.read_text(encoding="utf-8"))
        tool_slugs = {t.get("slug") for t in tools}

    # skill slugs available to resolve a super-skill's orchestrates against.
    skill_slugs: set = set()
    skills_path = d / "skills_index.json"
    if skills_path.is_file():
        idx = json.loads(skills_path.read_text(encoding="utf-8"))
        skill_slugs = {s.get("slug") for s in idx}

    for md in md_files:
        slug = md.parent.name
        text = md.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            violations.append(f"{md}: no frontmatter block")
            continue
        try:
            fm = yaml.safe_load(text.split("---\n", 2)[1]) or {}
        except yaml.YAMLError as e:
            violations.append(f"{md}: invalid frontmatter YAML: {e}")
            continue
        if not isinstance(fm, dict):
            violations.append(f"{md}: frontmatter is not a mapping")
            continue

        meta = fm.get("metadata") if isinstance(fm.get("metadata"), dict) else {}

        # provenance invariant: valid under community, synthetic, OR literature
        # (review-grounded super-skills) origin. Reuses the provenance_tier kernel
        # semantics: literature ⇒ >=1 doi, synthetic ⇒ synthesized_from,
        # community ⇒ related_skills key present.
        prov = meta.get("provenance_tier")
        prov_violations = validate_provenance(
            prov,
            dois=meta.get("dois"),
            synthesized_from=meta.get("synthesized_from"),
            related_skills=fm.get("related_skills") if "related_skills" in fm else None,
        )
        for msg in prov_violations:
            violations.append(f"{md}: {msg}")

        # skill_kind invariant (default 'skill' when absent); a 'super' skill
        # must orchestrate a non-empty list of resolvable sub-skill slugs.
        kind = meta.get("skill_kind", DEFAULT_SKILL_KIND)
        if kind not in VALID_SKILL_KINDS:
            violations.append(
                f"{md}: metadata.skill_kind {kind!r} not in "
                f"{sorted(VALID_SKILL_KINDS)}"
            )
        elif kind == "super":
            orchestrates = meta.get("orchestrates")
            if not (isinstance(orchestrates, list) and orchestrates):
                violations.append(
                    f"{md}: super skill requires non-empty metadata.orchestrates list"
                )
            else:
                for ref in orchestrates:
                    if ref not in skill_slugs:
                        violations.append(
                            f"{md}: orchestrates {ref!r} not in skills_index.json"
                        )

        # proposal-rail invariant
        status = fm.get("status")
        if status != "hold":
            violations.append(f"{md}: status {status!r} != 'hold'")

        # description + EDAM + license_tier discipline (CI parity)
        for msg in frontmatter_violations(fm):
            violations.append(f"{md}: {msg}")

        # tools_used slugs must resolve in the tool catalog
        for ref in meta.get("tools_used") or []:
            if ref not in tool_slugs:
                violations.append(
                    f"{md}: tools_used {ref!r} not in tools_index.json"
                )

        # contributors (co-authorship attribution) — OPTIONAL; validate shape
        # only when present (top-level key; absence is fine).
        if "contributors" in fm:
            for msg in contributor_violations(fm.get("contributors")):
                violations.append(f"{md}: {msg}")

    return violations


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print("usage: check_proposals <collection_dir> [...]", file=sys.stderr)
        return 2
    failed = False
    for col in argv:
        v = check_collection(col)
        if v:
            failed = True
            print(f"FAIL {col}:")
            for x in v:
                print(f"  - {x}")
        else:
            print(f"OK   {col}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
