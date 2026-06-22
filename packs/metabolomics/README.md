# Metabolomics technique packs

Lighter, **per-technique** installs of the ASB metabolomics collection — each pack is the subset of skills carrying that technique tag, so you load only what you need instead of all 5,865 skills.

| Plugin | Skills |
|---|---|
| `metabolomics-lc-ms` | 1314 |
| `metabolomics-tandem-ms` | 2129 |
| `metabolomics-gc-ms` | 367 |
| `metabolomics-ce-ms` | 114 |
| `metabolomics-direct-infusion` | 97 |
| `metabolomics-ms-imaging` | 292 |
| `metabolomics-ion-mobility` | 390 |
| `metabolomics-nmr` | 276 |
| `metabolomics-ms-generic` | 804 |

> Packs **overlap**: a multi-technique skill (e.g. LC-MS + tandem-MS) appears in several packs, so installing overlapping packs loads that skill more than once. Install the full `metabolomics` plugin instead if you want everything once.

Install: `/plugin install metabolomics-<technique>@asb-skill-collections` (e.g. `metabolomics-lc-ms`). Grounding (Perspicacité binder + kb_bundle) lives in the full collection at `collections/metabolomics/v2/`.
