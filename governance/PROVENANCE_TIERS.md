# Provenance tiers

`provenance_tier` answers an origin question — *where did this skill's content come
from?* — and is **orthogonal** to the consumer `license_tier`
([`LICENSE_TIERS.md`](LICENSE_TIERS.md), *what may I do with the tool this skill
grounds on?*) and to the paper open-access axis (`access.type`, *may we
redistribute the source?*). A single skill carries one value on each axis; they do
not constrain each other.

| Tier | Meaning | Invariant (enforced) |
|---|---|---|
| `literature` | Synthesized from one or more peer-reviewed source papers | requires ≥1 `doi` |
| `synthetic` | Derived from other skills (composed / specialized / merged), not from a paper directly | requires `synthesized_from` (the source skill slugs) |
| `community` | Contributed or curated outside the ASB literature pipeline | requires a `related_skills` key to be present (an empty list is allowed) |

The canonical kernel is `scripts/provenance_tier.py` (`VALID`, `DEFAULT="literature"`,
`validate_entry(...)`); the CI gate `scripts/check_provenance_tiers.py` enforces both
the per-tier invariant above and that each `SKILL.md` frontmatter
`metadata.provenance_tier` equals the `skills_index.json` value.

## Current state

Every shipped skill in `collections/metabolomics/v2` is **`literature`** — each is
distilled from a peer-reviewed method paper and carries ≥1 source DOI. The
`synthetic` and `community` tiers exist so the schema can admit those skills later
without a migration; no skill carries them yet.

The field is set **field-only** — there is no in-body banner for provenance (unlike
the non-open `license_tier` banner). `provenance_tier` lives in
`skills_index.json`, in `kb_bundle.json` skill records, and in each `SKILL.md`
frontmatter `metadata.provenance_tier`.

## Orthogonality to `license_tier`

The two axes are independent and answer different questions:

- `provenance_tier` (this file) — **origin**: was the content distilled from a
  paper, composed from other skills, or community-contributed?
- `license_tier` ([`LICENSE_TIERS.md`](LICENSE_TIERS.md)) — **permission**: may a
  consumer use the underlying tool commercially (`open` / `noncommercial` /
  `restricted`)?

A `literature` skill can ground on an `open`, `noncommercial`, or `restricted`
tool; a future `community` skill could ground on an `open` tool. Neither value is
derivable from the other, so they are stored and gated separately.

## Forward path — admitting `synthetic` and `community` skills

The tiers are wired end-to-end (kernel + propagation + gate) ahead of need so the
first non-`literature` skill is a data change, not a code change:

- **`synthetic`** — when a skill is composed from existing skills (e.g. a higher-level
  workflow stitched from several procedures), stamp `provenance_tier: synthetic` and
  populate `synthesized_from:` with the contributing skill slugs. The gate then
  requires that key; the skill needs no source DOI.
- **`community`** — when a skill is contributed or curated outside the ASB pipeline
  (see [`CONTRIBUTING`](../.github/CONTRIBUTING.md) and
  [`SOURCES.md`](SOURCES.md)), stamp `provenance_tier: community` and include a
  `related_skills:` key (empty list allowed) so the lineage is explicit. Such skills
  carry their own attribution and are not required to derive from a paper.

In all cases the invariant in the table above is what the CI gate checks; the
default for backfill remains `literature`.
