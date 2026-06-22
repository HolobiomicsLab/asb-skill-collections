---
name: metabolomics-collection-router
description: Use when an agent needs to find and apply a computational-metabolomics / LC-MS-MS skill from this collection, and optionally ground it against the source paper via Perspicacité before acting.
license: CC-BY-4.0
metadata:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  skills_count: 5865
  tools_count: 909
  indexes:
  - skills_index.json
  - tools_index.json
  - kb_bundle.json
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: ''
  all_source_dois: []
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ASB Metabolomics Skill Collection — router

This is the default entry point for the ASB Metabolomics collection (v2): **5,865
evidence-grounded skills** and **909 software-tool records** for computational
mass spectrometry / LC-MS/MS, each derived from a peer-reviewed method paper and
its public code repository.

You (the agent) use this router in three steps: **search → apply → (optionally) ground**.

## 1. Search — find the right skill

Every skill is one `skills/<slug>/SKILL.md` with YAML frontmatter. Two machine
indexes at the collection root make lookup cheap — load whichever fits:

- **`skills_index.json`** — one row per skill: `slug`, `name`, `description`,
  `edam_operation`, `edam_topics`, `tools`, `dois`.
- **`tools_index.json`** — one row per tool: `slug`, `name`, `canonical_url`,
  `edam_topics`, `dois`.

Pick a skill by matching the user's task against, in order of precision:

1. **EDAM operation/topic IRI** — exact ontology match (e.g. peak picking =
   `operation_3215`, spectral library matching, formula prediction).
2. **Tool name** — the user already names a tool ("run XCMS", "use SIRIUS",
   "GNPS molecular networking", "MZmine", "matchms").
3. **Keyword** over `name` + `description`.

Then read that skill's `skills/<slug>/SKILL.md` and follow it.

## 2. Apply — use the skill

The skill body carries the procedure; its frontmatter carries `tools` (what to
install/invoke), `derived_from` (source paper DOIs), and `evidence_spans`
(verbatim anchors from the paper/repo). Use the tool records in
`tools_index.json` for canonical install URLs.

## 3. Ground (recommended) — verify against the source via Perspicacité

Before trusting a parameter, claim, or default, **ground the skill against the
paper it was built from**. The mapping skill → source DOI(s) → KB is precomputed
in **`kb_bundle.json`** (each skill's `kb_slugs` are the SAME `asb-paper-<doi>`
KBs the collection was assembled against). A running Perspicacité instance plus
`scripts/perspicacite_kb_bind.py` makes this one command:

```bash
# auto-create + ingest the skill's KB (paper full text + supplementary info),
# then ask a grounded, cited question against it:
python scripts/perspicacite_kb_bind.py query \
  --collection collections/metabolomics/v2 \
  --skill <slug> \
  --question "<what you need to verify>"
```

The KB is **generated on first use** (idempotent — reused thereafter). Choose the
grounding **tier** with `--tier`:

| tier | grounds against | use for |
|---|---|---|
| `paper` (default) | paper full text **+ supplementary information** | parameters, claims, methods |
| `si` | supplementary tables/figures emphasised | exact thresholds, benchmark numbers |
| `repo` | the tool's source repo (no KB; returns repo URLs) | implementation details, CLI flags |

`prepare` (build the KB without querying) and `resolve` (print the grounding map
offline) are the other two subcommands.

## Provenance

Each skill is grounded (`derived_from` DOIs + `evidence_spans`), license-tagged
(CC-BY-4.0), and EDAM-annotated. Non-open-access sources and ungrounded skills
were held out at release. See `corpus.yaml` for the per-paper access basis
(`repo-oa`: the redistributable source repository was cloned at build time) and
`gate_report.json` for the passing release-gate verdict.
