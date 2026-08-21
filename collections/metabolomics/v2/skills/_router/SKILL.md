---
name: metabolomics-collection-router
description: Use when an agent needs to find and apply a computational-metabolomics / LC-MS-MS skill from this collection, and optionally ground it against the source paper via Perspicacité before acting.
license: CC-BY-4.0
metadata:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  skills_count: 5859
  tools_count: 909
  workflows_count: 21
  leaf_dir: leaves
  workflow_dir: workflows
  retrieval: bin/search_skills.py
  semantic_retrieval: bin/semantic_search.py
  indexes:
  - skills_index.json
  - tools_index.json
  - kb_bundle.json
  - workflows/workflows_index.json
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: ''
  all_source_dois: []
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ASB Metabolomics Skill Collection — router

This is the default entry point for the ASB Metabolomics collection (v2): **5,859
evidence-grounded skills**, **21 composite workflows** and **909 software-tool records** for computational
metabolomics — predominantly LC-MS/MS, but also LC-MS, GC-MS, mass-spectrometry
imaging, ion mobility, lipidomics, and some NMR / multi-omics — each derived from
a peer-reviewed method paper and its public code repository.

You (the agent) use this router in three steps: **search → apply → (optionally) ground**.

## How this collection is laid out

The 5,859 leaf skills live in **`leaves/<slug>/SKILL.md`**, and the 21 composite
workflows in **`workflows/<slug>/SKILL.md`** — neither is under `skills/`.
That is deliberate: a plugin host loads the name and description of every skill
under `skills/` into the session prompt, so advertising all of them would cost
several hundred thousand tokens before you have done anything. Only this router
and the `asb-metabolomics` licence gate are advertised; the corpus ships beside
them as data and you retrieve from it on demand.

So: **do not enumerate `leaves/`, and do not read `skills_index.json` whole**
(it is several megabytes). Search it with the script below, then read the one
skill you need.

## 1. Search — find the right skill

```bash
python bin/search_skills.py --query "<the user's task>" -k 10
```

Standard library only — no network, no API key. It prints a handful of
candidates with their tools, techniques, licence tier, and the exact path to
read. Narrow it with exact-match filters when the user has already been
specific:

- `--technique LC-MS` — analytical platform tag: `LC-MS` (incl. LC-MS/MS),
  `GC-MS`, `CE-MS`, `direct-infusion-MS`, `MS-imaging`, `ion-mobility-MS`,
  `NMR`, `mass-spectrometry` (generic).
- `--tool SIRIUS` — the user already names a tool ("run XCMS", "use SIRIUS",
  "GNPS molecular networking", "MZmine", "matchms").
- `--edam operation_3215` — exact ontology match (e.g. peak picking, spectral
  library matching, formula prediction).

### Whole pipelines: search the workflows first

When the request spans a whole study rather than one step — *"annotate my
untargeted LC-MS/MS run"*, *"lipidomics from mzML to a feature table"* — a
composite workflow already chains the right leaves in the right order:

```bash
python bin/search_skills.py --target workflows --query "<the user's task>" -k 5
```

Each hit prints its stages and the path to `workflows/<slug>/SKILL.md`. Read
that, follow its stages, and use the leaf skills it names. Fall back to a leaf
search when no workflow covers the request.

### Optional: semantic ranking

`bin/semantic_search.py` ranks by meaning rather than keyword overlap, using
`text-embedding-3-large` when an embedding backend is available (set
`OPENAI_API_KEY`, and point `ASB_LEAF_EMB_CACHE` at the leaf embedding cache or
drop it at `.cache/leafemb_v2.npz`). It falls back to a keyword search when no
backend is configured, and the `mode` field in its output says which ran. It
takes the same `--target skills|workflows`.

Three machine indexes back both scripts, and are worth querying directly with
`jq` when you need a field they do not print:

- **`skills_index.json`** — one row per skill: `slug`, `name`, `description`,
  `edam_operation`, `edam_topics`, `tools`, `dois`, `techniques`,
  `license_tier`.
- **`tools_index.json`** — one row per tool: `slug`, `name`, `edam_topics`,
  `dois`, `license_tier`, `license_subject`, `repo_url`, `source_paper_repos`.
  `repo_url` is the tool's own repository, present only where a licence was
  resolved from it. `source_paper_repos` holds the repositories of the papers
  that *cite* the tool — not the tool's home, and never to be offered as one.
- **`workflows/workflows_index.json`** — one row per composite workflow: `slug`,
  `name`, `description`, `techniques`, `stages`, `member_tools`.

Then read that skill's `leaves/<slug>/SKILL.md` and follow it.

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

## License tier

When routing or presenting candidate skills, read each candidate's `license_tier`
from `skills_index.json` or the skill's `SKILL.md` frontmatter
(`metadata.license_tier`). Apply the following rules, in addition to normal
routing logic:

- **`open`** — surface freely; no gate required. Discovery defaults to `open`-tier
  skills whenever the consumer has not expressed a specific tier preference.
- **`noncommercial`** — flag the **blocking acknowledgment** before applying the
  skill: commercial use is forbidden without a separate license. Defer to the
  `asb-metabolomics` gate (which checks `metadata.tool_license`) — the user must
  explicitly confirm a permitted (academic / noncommercial) purpose. Do not apply
  a `noncommercial` skill until the acknowledgment is confirmed.
- **`restricted`** — show the soft note: *"licence established and it constrains
  reuse — check it before commercial use or redistribution"* (non-blocking).
  Proceed only after surfacing this caveat.
- **`unknown`** — no tool-level licence evidence was found. Show the soft note:
  *"no tool-level licence evidence — verify before redistributing"* (non-blocking).
  This is an open question, not a verdict: do not present it as a restriction on
  using the tool, and do not treat it as permission to redistribute the tool's
  code. 693 of the 909 tools in this collection are `unknown`, of which 39 are
  extraction artefacts rather than tools; 654 are software still awaiting a
  licence lookup.

Tools also carry **`entry_kind`** — `software`, `vendor_product` or `artefact`.
A `vendor_product` is an instrument or a proprietary application: fine to
recommend and fine to use, `restricted` because there is an agreement rather than
an open licence behind it. An `artefact` is an extraction defect (a module path,
a bare URL, a sentence fragment) and should not be offered as a tool at all.

All other routing behavior (technique, EDAM, tool name, keyword matching) is
unchanged; tier-awareness is an additional layer applied after candidate
selection.

## Provenance

Each skill is grounded (`derived_from` DOIs + `evidence_spans`), license-tagged
(CC-BY-4.0), and EDAM-annotated. Non-open-access sources and ungrounded skills
were held out at release. See `corpus.yaml` for the per-paper access basis
(`repo-oa`: the redistributable source repository was cloned at build time) and
`gate_report.json` for the passing release-gate verdict.
