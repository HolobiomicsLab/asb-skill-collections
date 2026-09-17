# Metabolomics technique packs

Lighter per-technique installs of the ASB metabolomics collection.

| Plugin | Skills |
|---|---|
| `metabolomics-lc-ms` | 2617 |
| `metabolomics-gc-ms` | 367 |
| `metabolomics-ce-ms` | 113 |
| `metabolomics-direct-infusion` | 97 |
| `metabolomics-ms-imaging` | 291 |
| `metabolomics-ion-mobility` | 385 |
| `metabolomics-nmr` | 276 |
| `metabolomics-ms-generic` | 804 |

Every pack is **derived**, never edited: its leaves are byte copies of
`collections/metabolomics/v2/leaves/<slug>/SKILL.md`, and both its indexes are
that collection's rows filtered to the pack's members. Membership is declared in
[`packs.yaml`](packs.yaml) as one technique tag per pack, and the rule is exactly
`tag ∈ skills_index[slug].techniques`.

To add a pack, retag one, or pull in leaves the collection has gained:

```bash
python -m scripts.build_packs           # re-derive every declared pack
python -m scripts.build_packs --check   # report drift, write nothing (CI gate)
```

A hand edit inside a pack is reverted by the next build and fails
`--check` before then. Change the collection, or change the map.

> Packs overlap (a multi-technique skill is in several); install the full `metabolomics` plugin OR a few packs, not both. **Grounding is packaged in every pack** — `bin/perspicacite_kb_bind.py` + `kb_bundle.json` + the `/ground` command — and works against a Perspicacité KB or, with no server, a serverless `local` clone of the source repo. Full guide: [USAGE §4](../../collections/metabolomics/v2/USAGE.md).
