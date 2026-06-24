# License tiers

`license_tier` answers a consumer question — *what may I do with the tool this skill
grounds on?* — and is **separate** from the paper open-access axis (`access.type`),
which answers *may we redistribute the source?*

| Tier | Meaning | Examples |
|---|---|---|
| `open` | Commercial use OK | MIT, Apache-2.0, BSD, MPL-2.0, CC-BY/CC0, **GPL/AGPL/LGPL** |
| `noncommercial` | Academic / noncommercial only | CC-BY-NC-*, PolyForm-Noncommercial, Masster NC&CS-1.0.0 |
| `restricted` | No grant / proprietary | no license, all-rights-reserved, proprietary, non-OSI custom |

Copyleft maps to `open`: it governs derivative *distribution*, not whether a consumer
may use the tool commercially. Canonical SPDX→tier map: `governance/license_tiers.yaml`.
Fallback: unknown license → `restricted`, unless its text contains a noncommercial
keyword → `noncommercial`.

Non-open tiers are **link-only** in shipped grounding bundles (referenced, never
embedded) and trigger a runtime acknowledgment when their skill is used.
