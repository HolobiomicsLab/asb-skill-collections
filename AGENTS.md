# AGENTS.md: install and use the ASB Metabolomics skills

Instructions for coding and research agents to install and use the ASB
Metabolomics Skill Collection. The public release is metabolomics v3: 11,830
skills over 1,989 tools, released as `metabolomics-v3.0.0` in the private domain
repository `asb-skills-metabolomics`. This master repository holds the tooling,
governance, documentation and release registry, not the released content.

> Full human guide: `<domain checkout>/collections/metabolomics/v3/USAGE.md`.
> Verified install routes and their dates: [`docs/STATUS.md`](docs/STATUS.md).
> Release source, commit, tree digest and DOI: [`collections.yaml`](collections.yaml).

## Requirements

- **Browse, search and read skills:** plain Markdown and JSON in a domain
  checkout, a fetched leaf directory or the Zenodo archive.
- **Helper scripts:** Python 3.8 or later and PyYAML
  (`pip install -r scripts/requirements.txt` from this master checkout).
- **Grounding binder** (`perspicacite_kb_bind.py`, bundled at `bin/` in every
  plugin and pack): Python 3.8 or later, standard library only. The `kb`
  backend needs Perspicacité at `PERSPICACITE_BASE` (default
  `http://127.0.0.1:8000`). The `local` backend needs `git` and network.
- **Running a skill's tool:** install what its frontmatter `tools:` lists. See
  `<domain checkout>/collections/metabolomics/v3/USAGE.md`, section 0, and
  `tools_index.json` in that collection.

## Install

### Claude Code: plugin marketplace

```bash
/plugin marketplace add HolobiomicsLab/asb-skill-collections
/plugin install metabolomics@asb-skill-collections
```

The marketplace entries point at `asb-skills-metabolomics`; installation needs
read access to that private repository until its visibility is opened. Earlier
CLI measurements predate these sources and are not a verification of them.

The entry point is `skills/_router/SKILL.md`. The corpus ships beside it as data
under `leaves/<slug>/SKILL.md` and is read on demand, so installation costs
negligible context.

### Fetch chosen leaves with `asbb`

```bash
asbb fetch <slugs> --collection metabolomics/v3 --dest <directory>
```

`asbb fetch` reads `collections.yaml` and downloads leaves from the domain
repository at the pinned commit. Set `GITHUB_TOKEN` while that repository is
private.

### Install a selection from a domain checkout

```bash
asbb install --repo <domain checkout> --skills <slug-a>,<slug-b> \
  --collection metabolomics/v3 --runtime agents
```

### Zenodo archive and direct consumption

The complete v3 release is at
[10.5281/zenodo.24054446](https://doi.org/10.5281/zenodo.24054446); v2 is at
[10.5281/zenodo.20794027](https://doi.org/10.5281/zenodo.20794027).

For Codex, GitHub Copilot or another agent, read the collection from a domain
checkout or extracted archive. Start at
`<domain checkout>/collections/metabolomics/v3/skills/_router/SKILL.md` and use
the machine indexes below. No runtime or build step is needed to read them.

For a chat assistant through a web UI, upload the chosen collection's
`skills_index.json`, `tools_index.json` and the few required leaf `SKILL.md`
files as knowledge, then paste a short routing instruction. Do not upload the
whole collection. This route was not verified end to end.

## Use: search, apply, ground

Run the search in the domain checkout or another unpacked collection. The
examples below use the v3 collection at
`<domain checkout>/collections/metabolomics/v3/`.

**1. Search** the indexes, most precise first:

- `skills_index.json`: `slug`, `name`, `description`, `edam_operation`,
  `edam_topics`, `tools`, `dois`.
- `tools_index.json`: `slug`, `name`, `edam_topics`, `dois`, `entry_kind`,
  `license_tier`, `license_subject`, `repo_url`, `source_paper_repos`.
  `entry_kind` is `software`, `vendor_product` or `artefact`. `repo_url` is the
  tool repository where a licence was resolved there; `source_paper_repos` are
  repositories of citing papers, not necessarily the tool's home.

```bash
# skills that use a given tool
jq -r '.[] | select(.tools[]? | ascii_downcase | test("sirius")) | .slug' \
  <domain checkout>/collections/metabolomics/v3/skills_index.json
# skills by EDAM topic (Metabolomics = topic_3172)
jq '.[] | select(.edam_topics[]? | test("topic_3172")) | {slug,name}' \
  <domain checkout>/collections/metabolomics/v3/skills_index.json
# keyword over name and description
jq -r '.[] | select(.description | test("library match";"i")) | .slug' \
  <domain checkout>/collections/metabolomics/v3/skills_index.json
```

**2. Apply:** read
`<domain checkout>/collections/metabolomics/v3/leaves/<slug>/SKILL.md`. Its body
is the procedure with verbatim evidence lines from the source. Its frontmatter
lists `metadata.tools` and `derived_from` source DOIs. Use `tools_index.json`
for canonical install URLs.

**3. Ground, recommended:** verify a parameter, threshold or claim against the
source paper or repository. The skill-to-source map, including `asb-paper-<doi>`
KB slugs and `repo_urls`, is precomputed in `kb_bundle.json`. The binder is
bundled in every plugin and pack at `bin/perspicacite_kb_bind.py`. Pass the
domain collection path to `--collection` and run from the unit directory:

```bash
# KB backend: Perspicacité at PERSPICACITE_BASE
python bin/perspicacite_kb_bind.py prepare \
  --collection <domain checkout>/collections/metabolomics/v3 --skill <slug>
python bin/perspicacite_kb_bind.py query \
  --collection <domain checkout>/collections/metabolomics/v3 --skill <slug> \
  --question "What threshold does the method recommend?"

# Serverless backend: clone source repositories and fetch an OA paper where possible
python bin/perspicacite_kb_bind.py local \
  --collection <domain checkout>/collections/metabolomics/v3 --skill <slug> --paper

# Offline map only
python bin/perspicacite_kb_bind.py resolve \
  --collection <domain checkout>/collections/metabolomics/v3 --skill <slug>
```

Tiers (`--tier`) are `paper` (full text and supplementary information, default),
`si` (supplementary information emphasised) and `repo` (read the tool source).
In Claude Code, `/ground` does this on the skill in play.

**Recommended agent loop:** prefer `kb` when Perspicacité is available. Use
`prepare` to warm it, then `query` before acting on a claim. When the server is
down, use `local` to clone and read the source directly.

## Licence tiers

Every skill carries a `license_tier`: `open`, `noncommercial`, `restricted` or
`unknown`, in `skills_index.json` and its `SKILL.md` frontmatter. The
`asb-metabolomics` meta-skill enforces the noncommercial acknowledgement gate
and routes tier logic. See
[`governance/LICENSE_TIERS.md`](governance/LICENSE_TIERS.md) for the policy.

## Notes

- Collection content is CC-BY-4.0. Every skill names its source DOI through
  `derived_from`, carries verbatim evidence lines and EDAM annotations, and
  passed the release gate recorded in
  `<domain checkout>/collections/metabolomics/v3/gate_report.json`.
- [`collections.yaml`](collections.yaml) is the release registry. It currently
  records metabolomics v2 and v3 in `asb-skills-metabolomics`; other domain
  repositories are private and to follow.
