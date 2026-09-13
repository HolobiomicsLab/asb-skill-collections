# Using the ASB Metabolomics Collection (v2)

5,859 evidence-grounded skills + 909 software-tool records for computational
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
| Ground via the **Perspicacité KB** (`perspicacite_kb_bind.py prepare`/`query`) | **Python ≥ 3.8** (stdlib only — no pip installs) **and** a running **Perspicacité** instance reachable at `PERSPICACITE_BASE` (default `http://127.0.0.1:8000`). Perspicacité can use whatever embedding + LLM provider you configure (OpenAI, Anthropic, OpenRouter, local, …); the specific models are **not** prescribed — only that Perspicacité is running. *(HolobiomicsLab literature-RAG engine; public availability TBD.)* |
| Ground via the **serverless `local` mode** (`perspicacite_kb_bind.py local`) | **Python ≥ 3.8** (stdlib only) **+ `git` + network**. **No Perspicacité, no server** — clones the skill's source repo(s) and best-effort fetches the open-access paper, which you then read directly. |
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
`tools_index.json`. To list everything a skill requires:

```bash
jq '.[] | select(.slug=="<slug>") | .tools' skills_index.json
```

---

## 1. Install one domain collection

The release perimeter verified here is deliberately narrow: a managed local
installation, Claude Code's local-checkout marketplace route and the checkout
CLI. Other adapters are listed under pending verification rather than presented
as working instructions.

The complete managed snapshot behaviour below was exercised on
`int/collections-release-2026-09-13` at `777671bc3`. Source revision
`600f4a5dc` predates the installer fixes and creates incomplete source symlinks;
do not use that pre-fix behaviour as the release experience.

### Managed, source-independent installation

Start from an existing checkout with Python 3.12 or later and PyYAML available.
From the repository root, install the full metabolomics domain into the shared
skill-native location:

```bash
python3 -m asb_skill_collections.asbb_cli install metabolomics --runtime agents
```

The clean temporary-HOME rehearsal returned:

```text
installed 3 skill(s) from metabolomics -> /private/tmp/asbcoll-release-docs-20260913/leaf-install/home/.agents/skills
```

The installation contains:

- three host-visible adapters under `$HOME/.agents/skills`: `_router`,
  `asb-metabolomics` and `asb-contribute`;
- a content-addressed snapshot under
  `$HOME/.agents/skills/.asbb-units/<content-id>`; and
- an ownership receipt at `$HOME/.asbb/installed.json`.

The snapshot census was 5,859 leaf `SKILL.md` files, 21 composite workflow
skills plus the workflow router, 909 tool records and 6,867 files in total
(70 MB on the rehearsal filesystem). It also contained the indexes, search and
grounding helpers, and no internal symlinks.

| File | What it is |
|---|---|
| `skills_index.json` | one row/skill: `slug, name, description, edam_operation, edam_topics, tools, dois` |
| `tools_index.json` | one row/tool: `slug, name, edam_topics, dois, entry_kind, license_tier, license_subject, repo_url, source_paper_repos` |
| `kb_bundle.json` | skill → source DOIs + tools + `asb-paper-<doi>` KB slugs (grounding map) |
| `collection.yaml` | the SkillCollection record (counts, curators, license) |
| `corpus.yaml` | per-paper access basis (`repo-oa`) |

To test the installed copy itself, change to the installed router and run its
packaged search helper:

```bash
cd "$HOME/.agents/skills/_router"
python3 ../../bin/search_skills.py --collection ../.. --query "untargeted LC-MS/MS annotation" --target workflows --json -k 1
```

In the rehearsal the temporary source path was moved away first. The command
still exited 0 without `PYTHONPATH` or `ASB_COLLECTIONS_ROOT`; its first result
contained these fields:

```text
qualified_slug: metabolomics/v2/workflows/untargeted-lcmsms-annotation
score: 12.0
selector: asb-keyword / 1.0.0 / package
```

There is no separate `asbb update` command. After updating the checkout through
your normal source-control process, rerun the same `install` command to refresh
the managed snapshot. A same-revision refresh was exercised and returned the
same successful install line.

Uninstall from the checkout that supplies the CLI:

```bash
python3 -m asb_skill_collections.asbb_cli uninstall metabolomics --runtime agents
```

The rehearsal returned `removed 3 entry(ies) for metabolomics`. It removed all
three adapters and the managed snapshot. It deliberately left the empty
`$HOME/.agents/skills` directory and `$HOME/.asbb/installed.json` containing
`{}`.

### Claude Code: verified local marketplace route

Claude Code 2.1.241 was exercised with both `HOME` and `CLAUDE_CONFIG_DIR`
redirected to temporary directories. From the checkout root:

```bash
claude --version
claude plugin marketplace add "$PWD"
claude plugin install metabolomics@asb-skill-collections
claude plugin list
claude plugin details metabolomics@asb-skill-collections
```

The host reported version `2.1.241`, added marketplace
`asb-skill-collections`, installed `metabolomics` at user scope, and listed
version 0.1.0 as enabled. Its component inventory reported `_router`,
`asb-contribute`, `asb-metabolomics` and the `ground` command as four skills,
with an estimated 244-token always-on cost. The cached plugin independently
returned the same workflow hit as the managed installation, with 5,859 leaves
and 909 tools.

The host's lifecycle commands were also exercised:

```bash
claude plugin update metabolomics@asb-skill-collections
claude plugin uninstall metabolomics@asb-skill-collections
```

Update reported that 0.1.0 was current. Uninstall removed the host registration,
but Claude retained the 70 MB plugin cache with an `.orphaned_at` marker and
retained its local marketplace registration. Those files are host-managed cache,
not an active plugin.

### Checkout CLI: verified programmatic route

This route needs Python, PyYAML and the checkout; it intentionally does not
survive removal of that checkout. From the repository root:

```bash
python3 -m asb_skill_collections.asbb_cli search "untargeted LC-MS/MS annotation" --collection metabolomics --target workflows --k 1
python3 -m asb_skill_collections.asbb_cli get untargeted-lcmsms-annotation --collection metabolomics/v2 --target workflows | sed -n '1,24p'
python3 -m asb_skill_collections.asbb_cli search --list-collections
```

All three commands exited 0. Search returned
`metabolomics/v2/workflows/untargeted-lcmsms-annotation` with score 12 and
selector `asb-keyword/1.0.0/package`; `get` opened that workflow; and the host
visibility check printed:

```text
metabolomics/v2    5859 skills    +workflows
```

### Pending verification

- The public GitHub transport for Claude Code was not exercised: the verified
  route added the same marketplace from a local checkout, while this environment
  had no usable DNS. It is therefore pending rather than inferred from the local
  result.
- The MCP server was successfully exercised by the pinned release audit, but a
  fresh rehearsal here could not install the optional `mcp` dependency because
  PyPI name resolution failed. Invoking the server without that dependency
  exited 1 with its installation guidance. No current stdio handshake or host
  integration is claimed.
- The `agents` adapter materialisation was verified, but Codex, Copilot CLI and
  Gemini CLI were not launched against it. Their host integrations are
  **experimental, not verified end to end**.
- Cursor, Cline, VS Code/Copilot instructions, arbitrary-destination adapters
  and web-UI uploads were not exercised. They are **experimental, not verified
  end to end** for this release perimeter.

---

## 2. Search — find the right skill

For the selector actually shared by the router, checkout CLI and MCP surface,
including score explanations, tie handling, measured limits and executed
examples, see [How offline skill selection works](../../../docs/selection.md).

The shared selector is the normal route. If you inspect the JSON indexes
manually, the following is a useful narrowing order; it is not the selector's
scoring order:

1. **Technique** (`skills_index.json` → `techniques`) — analytical platform tags.
2. **EDAM operation/topic IRI** (`edam_operation` / `edam_topics`).
3. **Tool name** (`tools` field, or `tools_index.json`) — "XCMS", "SIRIUS", "GNPS", "MZmine", "matchms".
4. **Keyword** over `name` + `description`.

### Filter by technique

Each skill is tagged with a `techniques` list (heuristic, from its content). The
vocabulary and current counts:

| tag | skills | | tag | skills |
|---|---|---|---|---|
| `LC-MS` (incl. LC-MS/MS) | 2617 | | `MS-imaging` | 291 |
| `GC-MS` | 367 | | `NMR` | 276 |
| `ion-mobility-MS` | 385 | | `CE-MS` | 113 |
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

### Semantic retrieval & the embedding cache

For offline retrieval, the collection-level `bin/search_skills.py`,
`bin/semantic_search.py --mode keyword`, `asbb search` and MCP use one versioned
selector. Add `--json` to the router command for the same result dictionaries,
including matched fields, filters and qualified collection/target/slug. See
[the selector contract and measured comparison](../../../docs/selection.md).
The package rule is the measured default; the previous router rule remains
available through `--selector router` (or `ASB_SELECTOR_RULE=router` for `asbb`)
for one release and is deprecated.

`bin/semantic_search.py` ranks by **meaning** (`text-embedding-3-large`, the model
Perspicacité uses) when an embedding cache is present, and falls back to a keyword
index search otherwise — so it always works offline (the `mode` field in the output
says which ran). Two things switch semantic mode on:

1. **The cache** — a `.npz` of precomputed leaf embeddings. Either:
   - **Download it** from the collection's Zenodo record (file
     `metabolomics-v<N>-leafemb.npz`) — no re-embedding, no API cost for the corpus.
     Drop it at `collections/metabolomics/v2/.cache/leafemb_v2.npz`, or point
     `ASB_LEAF_EMB_CACHE` at it.
   - **Build it** from a source embedding set (or from scratch with an API key):
     ```bash
     python scripts/build_leaf_embedding_cache.py \
       --collection collections/metabolomics/v2 --source <full_embeddings.npz>   # align (no key)
     python scripts/build_leaf_embedding_cache.py \
       --collection collections/metabolomics/v2 --embed                          # bootstrap (needs key)
     ```
2. **`OPENAI_API_KEY`** — needed only to embed the *query* at run time (≈free per
   call). The corpus is already embedded in the cache; the key never re-embeds the
   5,859 leaves.

So: cache present + key set → semantic ranking; cache present, no key → keyword;
no cache → keyword. Nothing is required for the collection to be usable.

### Whole-pipeline goals → composite workflows

For an end-to-end goal ("annotate an untargeted LC-MS/MS run", "GC-MS deconvolution
+ identification", "SIRIUS de-novo elucidation"), start from a **composite workflow
super-skill** instead of a single atomic skill. The 21 workflows live under
[`workflows/`](workflows/); each is an ordered DAG of stages that delegates to the
atomic skills above. Pick one with the workflow router:

```bash
# From the collection root; --mode keyword makes this explicitly offline.
python bin/semantic_search.py --query "<the user's goal>" \
  --collection . --target workflows --mode keyword --k 3
# Add --technique LC-MS when that technique is required.
# From inside workflows/, use the same collection-level script:
python ../bin/semantic_search.py --query "<the user's goal>" \
  --collection . --target workflows --mode keyword --k 3
# Or browse workflows/workflows_index.json from the collection root.
```

The shared resolver finds the same index from either location and searches
`member_tools`. The older `workflows/bin/semantic_search.py` copy is outside the
unified path; use the collection-level script above.

Then read that workflow's `workflows/<slug>/SKILL.md` and follow its stages, applying
each stage's `primary_skill` from the atomic collection. See
`workflows/_workflow_router/SKILL.md` for the full protocol.

---

## 3. Use — apply the skill

Read `leaves/<slug>/SKILL.md`: the body is the procedure; the frontmatter lists
`tools` (install/invoke targets), `derived_from` (source DOIs), and
`evidence_spans` (verbatim anchors). Use `tools_index.json` for canonical
install URLs.

---

## 4. Ground (recommended) — verify against the source (KB or serverless)

Skills carry distilled procedure; for an exact parameter, threshold, or claim,
**ground the skill against the paper/repo it was built from**. The skill → source
mapping is precomputed in `kb_bundle.json` (source DOIs, the `asb-paper-<doi>` KB
slugs — the same targets the collection was assembled against — and the source
`repo_urls`). **Grounding ships inside every plugin and pack**
(`bin/perspicacite_kb_bind.py` + `kb_bundle.json` + `commands/ground.md` +
`GROUNDING.md`), so it works from an installed plugin with no extra setup.

Two backends, **KB-primary with a serverless fallback**:

- **`kb` (Perspicacité)** — RAG over the paper full text **+ supplementary
  information**, persistent and citable; the KB is **generated on first use**
  (create + ingest), then reused. Needs a running **Perspicacité** at
  `PERSPICACITE_BASE` (default `http://127.0.0.1:8000`).
- **`local` (serverless)** — `git clone` the skill's source repo(s) + best-effort
  fetch the open-access paper, then read the files directly. **No server.**

**In Claude Code**, run the bundled command on the skill in play:

```
/ground                              # ground the skill you're using
/ground <skill-or-doi> "<question>"
```

**From the CLI** — the binder is bundled at `bin/perspicacite_kb_bind.py` in every
plugin/pack (and at `scripts/perspicacite_kb_bind.py` in this repo / the Zenodo
deposit). Run it against the unit dir (`--collection .` from inside a pack); the
KB is **generated on first use**:

```bash
# print the grounding map for a skill (offline — no server, no clone)
python bin/perspicacite_kb_bind.py resolve --collection . --skill <slug>

# KB backend: build the skill's KB (create + ingest), without querying
python bin/perspicacite_kb_bind.py prepare --collection . --skill <slug>

# KB backend: ask a grounded, cited question against the source paper
python bin/perspicacite_kb_bind.py query --collection . --skill <slug> \
  --question "What spectral-similarity threshold does the method recommend?"

# serverless backend: clone the source repo(s) + best-effort OA paper (no Perspicacité)
python bin/perspicacite_kb_bind.py local --collection . --skill <slug> --paper
```

### Grounding tiers (`--tier`)

| tier | grounds against | use for |
|---|---|---|
| `paper` (default) | paper full text **+ supplementary information** | parameters, claims, methods |
| `si` | retrieval steered toward supplementary tables/figures | exact thresholds, benchmark numbers |
| `repo` | the tool's source repository (no KB; returns repo URLs) | implementation details, CLI flags |

**Agentic pattern:** on activating a skill, prefer the **`kb`** backend when
Perspicacité is up (`prepare` to warm it, then `query` whenever a claim needs
verification before you act); when it's **down**, fall back to **`local`** to clone
the source and read it directly. Either way every skill is self-grounding — no
heavyweight vector dump ships: the KB is reconstructed on demand from the same DOIs
(+ SI) the build used, and the repos come straight from `repo_urls`.

**From the Zenodo archive (self-contained):** the deposit bundles the binder at
`scripts/perspicacite_kb_bind.py` alongside this collection. After extracting,
run it from the collection folder with `--collection .`, e.g.:

```bash
python scripts/perspicacite_kb_bind.py query --collection . --skill <slug> --question "..."
```

---

## License tiers

Every skill carries a `license_tier` field (in `skills_index.json` and in each
`SKILL.md` frontmatter `metadata.license_tier`) that answers *what may I do with
the underlying tool?*

| Tier | Meaning |
|---|---|
| `open` | Commercial use OK (MIT, Apache-2.0, GPL, CC-BY, …) |
| `noncommercial` | Academic / noncommercial only — **confirm permitted use before applying** the skill |
| `restricted` | Licence established and it constrains reuse — **check it before commercial use or redistribution** |
| `unknown` | No tool-level licence evidence — describing and using are unaffected; **never redistribute** the tool's code |

Discovery defaults to `open` skills; the `asb-metabolomics` meta-skill enforces
the `noncommercial` acknowledgment gate. Non-open skills carry a one-line banner
in their body. Full policy: [`governance/LICENSE_TIERS.md`](../../../governance/LICENSE_TIERS.md).

```bash
# list only open-tier skills
jq '[.[] | select(.license_tier=="open")]' collections/metabolomics/v2/skills_index.json
```

---

## Skill metadata & attribution

Every `SKILL.md` carries an `attribution:` block (collection-level mirror in
`collection.yaml → roles`). The roles are deliberately distinct:

| Field | Meaning |
|---|---|
| `generator` | what produced the skill — the **AgenticScienceBuilder** pipeline (not a human author) |
| `original_doi` / `all_source_dois` | the source paper(s) the skill was built from — **always cite these** |
| `curators` | person(s) who later **modify / validate** the skill (empty at v0.2.0 — none yet) |
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
