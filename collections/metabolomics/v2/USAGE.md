# Using the ASB Metabolomics Collection (v2)

5,865 evidence-grounded skills + 909 software-tool records for computational
metabolomics — predominantly LC-MS/MS, but also LC-MS, GC-MS, mass-spectrometry
imaging, ion mobility and lipidomics, with some NMR and multi-omics / statistics
/ pathway tools — each derived from a peer-reviewed method paper and its public
code repository. This guide covers **search → install → use → ground**. For what
the collection contains and how it was selected, see [ABOUT.md](ABOUT.md).

---

## 0. Requirements

You can **browse, search, and read** the collection with nothing installed — the
skills and indexes are plain Markdown + JSON. Each capability adds dependencies:

| To… | You need |
|---|---|
| Install in Claude Code | Claude Code with plugin support |
| Search the indexes (examples below) | [`jq`](https://jqlang.github.io/jq/) (optional; any JSON reader works) |
| Run the helper scripts (`collect`, `release_gate`, `regen_catalogue`) | **Python ≥ 3.8** + **PyYAML** (`pip install pyyaml`) |
| Run the grounding binder `perspicacite_kb_bind.py` | **Python ≥ 3.8** (stdlib only — no pip installs) **and** a running **Perspicacité** instance reachable at `PERSPICACITE_BASE` (default `http://127.0.0.1:8000`). Perspicacité can use whatever embedding + LLM provider you configure (OpenAI, Anthropic, OpenRouter, local, …); the specific models are **not** prescribed — only that Perspicacité is running. *(HolobiomicsLab literature-RAG engine; public availability TBD.)* |
| **Run a given skill's tool** | the libraries that skill lists in its frontmatter `tools` (see below) |

> A `requirements.txt` for the helper scripts lives at `scripts/requirements.txt`.

### Per-skill tool dependencies

Each skill's frontmatter `tools:` enumerates exactly what that procedure needs —
these vary per skill and are **not** bundled here. Common shapes:

- **R / Bioconductor** — e.g. `R (>=3.5)`, `BiocManager`, then
  `BiocManager::install("xcms")`, `pcaMethods`, `limma`, … (installed with
  `devtools::install_github(...)` or `BiocManager::install(...)` as the skill body shows).
- **Python** — `pip install matchms spectrum_utils pyteomics …` per the skill.
- **Standalone tools** — e.g. SIRIUS, GNPS/FBMN (web), MZmine (GUI/headless).

Resolve the canonical install target from the skill body and from
`tools_index.json` (`canonical_url`). To list everything a skill requires:

```bash
jq '.[] | select(.slug=="<slug>") | .tools' skills_index.json
```

---

## 1. Install

### Claude Code (recommended)

```bash
/plugin marketplace add HolobiomicsLab/asb-skill-collections
/plugin install metabolomics@asb-skill-collections          # full (5,865 skills)
# or a lighter per-technique pack (load only what you need):
/plugin install metabolomics-lc-ms@asb-skill-collections    # lc-ms · gc-ms · nmr · ms-imaging ·
                                                            # ion-mobility · ce-ms ·
                                                            # direct-infusion · ms-generic
```

Skills are auto-discovered from `skills/<slug>/SKILL.md` and become available to
the agent. The entry point is `skills/_router/SKILL.md`. The full plugin loads
all 5,865 skills eagerly; the technique packs are much smaller. Packs **overlap**
(a multi-technique skill is in several), so install one full plugin *or* a few
packs — not both — to avoid duplicate skills in context.

### Any other agent / IDE (IDE-agnostic)

Every skill is a plain `SKILL.md` (YAML frontmatter + markdown body) and every
tool is a `tools/<slug>.yaml`. Point your agent at this directory, or consume
the machine indexes directly:

| File | What it is |
|---|---|
| `skills_index.json` | one row/skill: `slug, name, description, edam_operation, edam_topics, tools, dois` |
| `tools_index.json` | one row/tool: `slug, name, canonical_url, edam_topics, dois` |
| `kb_bundle.json` | skill → source DOIs + tools + `asb-paper-<doi>` KB slugs (grounding map) |
| `collection.yaml` | the SkillCollection record (counts, curators, license) |
| `corpus.yaml` | per-paper access basis (`repo-oa`) |

### Chat assistants via the web UI (Claude · ChatGPT · Mistral)

No CLI needed — you attach the skills as **uploaded knowledge** and add a short
routing instruction. Because these UIs cap how many files you can upload, **do
not upload all 5,865 skills**. Upload instead:

1. `skills_index.json` + `tools_index.json` (the searchable catalogue), and
2. only the handful of `skills/<slug>/SKILL.md` files relevant to your work
   (find them first with the search in §2, then download those files).

Then paste this **routing instruction** into the assistant's
instructions/system prompt:

> You have an ASB metabolomics skill catalogue. To answer a metabolomics task:
> (1) search `skills_index.json` by EDAM topic, tool name, or keyword to pick
> the best `slug`; (2) open that skill's `SKILL.md` and follow its procedure;
> (3) cite the skill's `original_doi`. If a needed `SKILL.md` wasn't uploaded,
> say which `slug` to add.

Per-platform UI steps (menu names drift; the flow is what matters):

- **Claude (claude.ai):** *Projects → Create project → add files to **Project
  knowledge*** (drop the two index files + your chosen `SKILL.md`s), then put
  the routing instruction in *Project instructions*. If your workspace has the
  **Skills/Capabilities** panel, you can instead add a skill there. (Claude
  Desktop/Code users: prefer the native plugin in §1.)
- **ChatGPT (chatgpt.com):** *Explore GPTs → Create → Configure → **Knowledge***
  → upload the index files + your `SKILL.md`s (file-count limited, ~20), paste
  the routing instruction into *Instructions*. *Projects* with attached files
  work the same way.
- **Mistral (Le Chat):** *Agents → build an agent* (or a **Library**) → upload
  the index files + your `SKILL.md`s as the agent's documents, and paste the
  routing instruction as the agent's system prompt.

> Grounding (§4) via Perspicacité is CLI-only; the web-UI path gives you the
> distilled skills + citations, not the live KB query.

---

## 2. Search — find the right skill

Match the user's task against the indexes, most precise first:

1. **Technique** (`skills_index.json` → `techniques`) — analytical platform tags.
2. **EDAM operation/topic IRI** (`edam_operation` / `edam_topics`).
3. **Tool name** (`tools` field, or `tools_index.json`) — "XCMS", "SIRIUS", "GNPS", "MZmine", "matchms".
4. **Keyword** over `name` + `description`.

### Filter by technique

Each skill is tagged with a `techniques` list (heuristic, from its content). The
vocabulary and current counts:

| tag | skills | | tag | skills |
|---|---|---|---|---|
| `LC-MS` (incl. LC-MS/MS) | 2621 | | `MS-imaging` | 292 |
| `GC-MS` | 367 | | `NMR` | 276 |
| `ion-mobility-MS` | 390 | | `CE-MS` | 114 |
| `mass-spectrometry` (generic) | 804 | | `direct-infusion-MS` | 97 |

*(Tandem-MS / MS/MS is folded into `LC-MS` — a fragmentation mode, not a platform — except genuinely GC-MS/CE-MS/DI/imaging sources. ~1,520 skills are technique-agnostic.)*

```bash
# all LC-MS skills
jq -r '.[] | select(.techniques[]? == "LC-MS") | .slug' skills_index.json
# GC-MS skills, with names
jq '.[] | select(.techniques[]? == "GC-MS") | {slug,name}' skills_index.json
# combine facets: NMR skills that also mention a structure tool
jq -r '.[] | select((.techniques[]? == "NMR") and (.tools[]? | ascii_downcase | test("sirius"))) | .slug' skills_index.json
```

### Other facets

```bash
jq '.[] | select(.tools[]? | ascii_downcase | test("sirius")) | .slug' skills_index.json
jq '.[] | select(.edam_topics[]? | test("topic_3172")) | {slug,name}' skills_index.json   # Metabolomics
jq -r '.[] | select(.description | test("library match";"i")) | .slug' skills_index.json
```

---

## 3. Use — apply the skill

Read `skills/<slug>/SKILL.md`: the body is the procedure; the frontmatter lists
`tools` (install/invoke targets), `derived_from` (source DOIs), and
`evidence_spans` (verbatim anchors). Use `tools_index.json` for canonical
install URLs.

---

## 4. Ground (recommended) — verify against the source with Perspicacité

Skills carry distilled procedure; for an exact parameter, threshold, or claim,
**ground the skill against the paper it was built from**. The skill → KB mapping
is precomputed in `kb_bundle.json` (the `asb-paper-<doi>` KB slugs are the same
targets the collection was assembled against). With a running
**Perspicacité** instance (`PERSPICACITE_BASE`,
default `http://127.0.0.1:8000`) the binder does it in one command — the KB is
**generated on first use** (create + ingest paper full text **+ supplementary
information**), then reused:

```bash
# print the grounding map for a skill (offline, no Perspicacité needed)
python scripts/perspicacite_kb_bind.py resolve \
  --collection collections/metabolomics/v2 --skill <slug>

# build the skill's KB (create + ingest), without querying
python scripts/perspicacite_kb_bind.py prepare \
  --collection collections/metabolomics/v2 --skill <slug>

# ask a grounded, cited question against the skill's source paper
python scripts/perspicacite_kb_bind.py query \
  --collection collections/metabolomics/v2 --skill <slug> \
  --question "What spectral-similarity threshold does the method recommend?"
```

### Grounding tiers (`--tier`)

| tier | grounds against | use for |
|---|---|---|
| `paper` (default) | paper full text **+ supplementary information** | parameters, claims, methods |
| `si` | retrieval steered toward supplementary tables/figures | exact thresholds, benchmark numbers |
| `repo` | the tool's source repository (no KB; returns repo URLs) | implementation details, CLI flags |

**Agentic pattern:** on activating a skill, call `prepare` once to warm its KB,
then `query` whenever a claim needs verification before you act on it. This makes
every skill self-grounding without shipping a heavyweight vector dump — the KB is
reconstructed on demand from the same DOIs (+ SI) the build used.

**From the Zenodo archive (self-contained):** the deposit bundles the binder at
`scripts/perspicacite_kb_bind.py` alongside this collection. After extracting,
run it from the collection folder with `--collection .`, e.g.:

```bash
python scripts/perspicacite_kb_bind.py query --collection . --skill <slug> --question "..."
```

---

## Skill metadata & attribution

Every `SKILL.md` carries an `attribution:` block (collection-level mirror in
`collection.yaml → roles`). The roles are deliberately distinct:

| Field | Meaning |
|---|---|
| `generator` | what produced the skill — the **AgenticScienceBuilder** pipeline (not a human author) |
| `original_doi` / `all_source_dois` | the source paper(s) the skill was built from — **always cite these** |
| `curators` | person(s) who later **modify / validate** the skill (empty at v0.1.0 — none yet) |
| `promoter` | person who **suggests using** the skill — Louis-Félix Nothias |
| `sponsor` | who **paid the API cost** of generation — CNRS & Université Côte d'Azur |
| `zenodo_doi` | the collection's Zenodo deposition DOI (TODO until minted) |

The collection's **Zenodo authors** (see `CITATION.cff`) are, by policy,
**AgenticScienceBuilder Community** first, then for this collection
**Louis-Félix Nothias**, **HolobiomicsLab.cnrs.fr**, **MetaboLinkAI.net**.

> Cite both: the **collection** (CITATION.cff / Zenodo DOI once minted) **and**
> the **original paper** (`original_doi`) behind whichever skill you use.

## How it was generated

See [`PROVENANCE.md`](PROVENANCE.md) for the **exact ASB build command** and the
**mixed-model routing** used to generate the collection (Opus 4.8 for
outline/card-revise; Haiku 4.5 for the rest; OpenAI embeddings — recorded
per-build in `build_manifest.json`). The raw ASB capsules + benchmark layer
(full end-to-end traceability) will be released later.

> **IRIs:** the `w3id.org/holobiomicslab/…` identifiers in `collection.yaml` and
> the docs are **reserved names that do not resolve yet** — stable identifiers,
> not working links. The Zenodo DOI is likewise not minted yet (`10.5281/zenodo.20794027`).

## Provenance & policy

Skills are CC-BY-4.0, EDAM-annotated, and `derived_from` a source DOI with
verbatim `evidence_spans`. Non-open-access sources and ungrounded skills were
held out at release. `corpus.yaml` records the per-paper access basis
(`repo-oa` — the redistributable source repository was cloned at build time);
`gate_report.json` records the passing release-gate verdict (access-tier,
strip-verbatim, provenance, PII/dual-use).
