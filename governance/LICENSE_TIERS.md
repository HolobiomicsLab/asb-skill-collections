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

## The source-reuse axis

`license_tier` answers *"what may I do with the tool?"*. It does **not** answer
*"what may we do with the source text?"* — and the two disagree. CC-BY-ND permits
commercial use of a tool (so it is not `noncommercial`) while forbidding derivative
text (so it is not `open`). Reading a paper's licence through the tool tier would
call such a source open, which is the mistake the blanket "pre-prints are always
CC-BY" rule made.

The second canonical table, `source_reuse` in `license_tiers.yaml`, answers the
source question. Reach it via `scripts/license_tier.py::source_reuse_for_license`.

| Value | Meaning | Examples |
|---|---|---|
| `full` | Redistribute, quote at length, derive — the open-access bar | CC-BY, CC-BY-SA, CC0 |
| `limited` | Some grant, but not full reuse; link-only | CC-BY-NC-*, CC-BY-ND-* |
| `none` | No reuse rights granted | arXiv `nonexclusive-distrib` |
| *(absent)* | **Unknown** — blocks admission, reported loudly | any unlisted licence |

An unlisted licence returns `None`, never a default. `None` (unknown) and `none`
(a known refusal) are different answers and must not be collapsed: one means we
failed to establish the rights, the other means the rights were withheld. Only
`full` admits a source at an open `access.type`. See
`scripts/preprint_license.py` and `governance/OPEN_ACCESS_POLICY.md` § Pre-prints.
