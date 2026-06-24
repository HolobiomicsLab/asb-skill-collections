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

Both `noncommercial` and `restricted` tiers are **link-only** in shipped grounding
bundles (referenced, never embedded). Beyond that, they differ:

- **`noncommercial`** additionally triggers a **blocking runtime acknowledgment**
  (commercial use is forbidden without a separate license; the consumer must
  explicitly confirm a permitted purpose before the skill is applied).
- **`restricted`** instead carries a **non-blocking soft note**: "no clear license
  detected — verify before commercial use or redistribution." Absence of a license
  is an unknown, not an explicit prohibition, so no blocking gate is required.
