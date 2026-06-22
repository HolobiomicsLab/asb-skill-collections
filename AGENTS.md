# AGENTS.md — install & use the ASB Metabolomics skills

Instructions for coding/research agents (Claude Code, OpenAI Codex, GitHub
Copilot, or any SKILL-aware agent) to **install and use** the ASB Metabolomics
Skill Collection. The public release is the **metabolomics** collection at
`collections/metabolomics/v2/` (5,865 evidence-grounded skills over 909
software tools for computational LC-MS/MS; tag `metabolomics-v0.1.0`).

> Full human guide: [`collections/metabolomics/v2/USAGE.md`](collections/metabolomics/v2/USAGE.md).

## Requirements

- **Browse / search / read skills:** nothing — plain Markdown + JSON.
- **Helper scripts** (`collect`, `release_gate`, `regen_catalogue`): Python ≥ 3.8 + PyYAML (`pip install -r scripts/requirements.txt`).
- **Grounding binder** (`perspicacite_kb_bind.py`): Python ≥ 3.8 (stdlib only) **and** a running **Perspicacité** instance at `PERSPICACITE_BASE` (default `http://127.0.0.1:8000`). Perspicacité can be configured with whatever embedding + LLM provider you have (OpenAI, Anthropic, OpenRouter, local, …) — the specific models are not prescribed; only a reachable Perspicacité is required. *(Perspicacité is HolobiomicsLab's literature-RAG engine; public availability TBD.)*
- **Running a given skill's tool:** install what that skill's frontmatter `tools:` lists (R/Bioconductor, Python pkgs, or standalone tools like SIRIUS/MZmine) — see `USAGE.md` §0 and `tools_index.json`.

---

## Install

### Claude Code — plugin marketplace (native)

```bash
/plugin marketplace add HolobiomicsLab/asb-skill-collections
/plugin install metabolomics@asb-skill-collections
```

Skills are auto-discovered from `collections/metabolomics/v2/skills/<slug>/SKILL.md`;
the entry point is `skills/_router/SKILL.md`. Nothing else to configure.

### OpenAI Codex — clone + reference (AGENTS.md aware)

```bash
git clone https://github.com/HolobiomicsLab/asb-skill-collections.git
# (or add as a submodule of your project)
```

Codex reads this `AGENTS.md` automatically. The skills are plain Markdown — to
use one, open `collections/metabolomics/v2/skills/<slug>/SKILL.md` and follow it.
Start from the search step below.

### GitHub Copilot — repo instructions

Clone the repo (or add it to your workspace). Copilot reads
[`.github/copilot-instructions.md`](.github/copilot-instructions.md), which
points here. The skills are Markdown files under `collections/metabolomics/v2/skills/`.

### Any other agent — direct consumption

The collection is self-describing, IDE-agnostic Markdown + JSON. Point your agent
at `collections/metabolomics/v2/` and use the machine indexes below. No runtime,
no build step.

### Chat assistants via the web UI (Claude · ChatGPT · Mistral)

For end users without a CLI: upload `skills_index.json` + `tools_index.json` and
your chosen `skills/<slug>/SKILL.md` files as the assistant's **knowledge**
(Claude *Projects*, ChatGPT *Custom GPT / Project*, Mistral *Agent / Library*),
then paste a short routing instruction. Don't upload all 5,865 skills — upload
the indexes plus the few skills you need. Full steps:
[`collections/metabolomics/v2/USAGE.md`](collections/metabolomics/v2/USAGE.md) →
"Chat assistants via the web UI".

---

## Use (all agents): search → apply → ground

**1. Search** the indexes at `collections/metabolomics/v2/` (most precise first):

- `skills_index.json` — `slug, name, description, edam_operation, edam_topics, tools, dois`
- `tools_index.json` — `slug, name, canonical_url, edam_topics, dois`

```bash
# skills that use a given tool
jq -r '.[] | select(.tools[]? | ascii_downcase | test("sirius")) | .slug' \
  collections/metabolomics/v2/skills_index.json
# skills by EDAM topic (Metabolomics = topic_3172)
jq '.[] | select(.edam_topics[]? | test("topic_3172")) | {slug,name}' \
  collections/metabolomics/v2/skills_index.json
# keyword over name+description
jq -r '.[] | select(.description | test("library match";"i")) | .slug' \
  collections/metabolomics/v2/skills_index.json
```

**2. Apply** — read `skills/<slug>/SKILL.md`. Its body is the procedure; its
frontmatter lists `tools` (install/invoke targets), `derived_from` (source DOIs),
and `evidence_spans` (verbatim anchors). Use `tools_index.json` for canonical
install URLs.

**3. Ground (recommended)** — before trusting a parameter, threshold, or claim,
verify it against the source paper. The skill → KB map is precomputed in
`kb_bundle.json`. With a running **Perspicacité** instance
(`PERSPICACITE_BASE`, default `http://127.0.0.1:8000`), the binder
generates the KB on first use and answers grounded, cited questions:

```bash
python scripts/perspicacite_kb_bind.py resolve --collection collections/metabolomics/v2 --skill <slug>
python scripts/perspicacite_kb_bind.py prepare --collection collections/metabolomics/v2 --skill <slug>
python scripts/perspicacite_kb_bind.py query   --collection collections/metabolomics/v2 --skill <slug> \
       --question "What threshold does the method recommend?"
```

Tiers (`--tier`): `paper` (full text + supplementary info, default) · `si`
(supplementary emphasised) · `repo` (read the tool's source repo directly).

**Recommended agent loop:** on activating a skill, run `prepare` once to warm
its KB, then `query` whenever a claim needs verification before acting.

---

## Notes

- License **CC-BY-4.0**; every skill is `derived_from` a source DOI with verbatim
  `evidence_spans`, EDAM-annotated, and passed the release gate
  (`collections/metabolomics/v2/gate_report.json`).
- The public release is **metabolomics only**. Other domains under `collections/`
  are staged/internal and not part of this release.
