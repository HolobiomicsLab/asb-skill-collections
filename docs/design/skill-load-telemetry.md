# Design: opt-in skill-load telemetry

**Status:** design draft (v1.1+).
**Author:** Holobiomics Lab.
**Last revised:** 2026-05-25.

## Problem

The v1 release ships 106 skills derived from 5 papers. We have no signal about which skills are actually loaded and used by downstream agents in real workflows. Curation for v2 (deciding which skills to deprecate, merge, refine, or expand) is therefore blind — we have to guess instead of measure.

Two concrete pains:
- Lead Curator review cycles can't prioritize. A skill that's loaded 500×/month deserves more attention than one loaded 0×.
- The router (`_router/SKILL.md`) ranks skills by description-keyword matching only. Real usage data would let it boost frequently-loaded skills.

## Approach

Opt-in HTTP beacon emitted by the Claude Code plugin runtime when a skill is loaded. **Disabled by default.** Enabled per-user via `asb-config telemetry on` (or equivalent in the plugin manifest).

Privacy guarantees, non-negotiable:
- No user ID. No prompt content. No file paths.
- IPs stripped at the edge by a Cloudflare Worker before reaching origin.
- Timestamps rounded to the hour so individual sessions can't be reconstructed.
- Aggregated rollups published openly; nothing per-user persisted.

## API sketch

```http
POST https://telemetry.holobiomicslab.cnrs.fr/v1/skill-load
Content-Type: application/json

{
  "skill_slug": "feature-detection-xcms",
  "collection": "metabolomics/v1",
  "asb_version": "0.1.0",
  "ts": "2026-05-25T09:00:00Z"
}
```

Response: 204 No Content. Beacon is fire-and-forget; failures are silent (don't degrade user experience).

## Aggregation

Weekly job emits `collections/<slug>/v<N>/usage.json`:

```json
{
  "schema_version": "0.1",
  "collection": "metabolomics", "collection_version": 1,
  "period_start": "2026-05-20", "period_end": "2026-05-27",
  "skill_loads": {
    "feature-detection-xcms": 524,
    "annotation-error-rate-calculation": 312,
    "...": "..."
  },
  "total_unique_skills_loaded": 87,
  "n_skill_loads_total": 2419
}
```

Published as part of the next routine release. No user-level data ever stored beyond the 7-day raw-event retention at the edge.

## Phased rollout

| Phase | When | What ships |
|---|---|---|
| 1 | v1.1 | Beacon endpoint up, opt-in flag in plugin config |
| 2 | v1.2 | Weekly `usage.json` published to each collection |
| 3 | v2.0 | Router L1 ranking incorporates usage signal |

## Open questions

1. **GDPR compliance audit.** CNRS legal counsel review required before launch. Even with IP stripping + no PII, the act of beaconing is a data-transfer event.
2. **Self-hosting vs third-party.** Plausible / Umami / PostHog all have privacy-respecting modes. Self-hosting is full control but full operational burden. Recommendation: start with Plausible.io's hosted free-for-OSS tier in phase 1, migrate to self-hosted if scale demands.
3. **Granularity of "skill load" event.** Definition: emitted ONCE per Claude Code session when a SKILL.md is fetched, NOT per inference call. This avoids inflating numbers for chatty agents.
4. **Negative signal.** Do we capture "skill loaded but task failed"? Would help curation but raises the bar for what counts as PII (failure mode might reveal user context). Defer to phase 3.

## Tracking issue

(Placeholder — file when launching phase 1.)

## See also

- `OPEN_ACCESS_POLICY.md` for the privacy stance on source content (no PII captured from contributors).
- The Claude Code plugin manifest spec for how user-level config persists.
