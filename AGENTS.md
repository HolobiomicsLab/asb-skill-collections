# AGENTS.md: install and use the ASB skill collections

Instructions for coding and research agents to install and use the ASB skill
collections. The registry `collections.yaml` lists the released collections of
ten domains; each is released from a private domain repository
`asb-skills-<domain>`. The worked examples use metabolomics v3: 11,830 skills
over 1,989 tools, released as `metabolomics-v3.0.2` in `asb-skills-metabolomics`.
This master repository holds the tooling, governance, documentation and release
registry, not the released content.

> Human guide for metabolomics v3: `<domain checkout>/collections/metabolomics/v3/USAGE.md`
> (the other nine collections ship no `USAGE.md`).
> Verified install routes and their dates: [`docs/STATUS.md`](docs/STATUS.md).
> Release source, commit, tree digest and DOI: [`collections.yaml`](collections.yaml).

## Requirements

- **Browse, search and read skills:** plain Markdown and JSON in an installed
  plugin, a domain checkout, a fetched leaf directory or the Zenodo archive.
- **Search script** (`bin/search_skills.py`, shipped in every released
  collection): Python 3.9 or later, standard library only, no network.
- **Helper scripts of this repository:** Python 3.8 or later and PyYAML
  (`pip install -r scripts/requirements.txt` from this master checkout).
- **Grounding binder** (`scripts/perspicacite_kb_bind.py` in this repository;
  none of the ten released collections ships it): Python 3.8 or later, standard
  library only. The `kb` backend needs Perspicacité at `PERSPICACITE_BASE`
  (default `http://127.0.0.1:8000`). The `local` backend needs `git` and network.
- **Running a skill's tool:** install what its frontmatter `tools` lists. See
  `tools_index.json` in the collection and, for metabolomics v3, section 0 of
  its `USAGE.md`.

## Install

### Claude Code: plugin marketplace

```bash
/plugin marketplace add HolobiomicsLab/asb-skill-collections
/plugin install metabolomics@asb-skill-collections
```

Other released domains install the same way under their domain name, for
example `/plugin install genomics@asb-skill-collections`. Each marketplace entry
points at its private domain repository; installation needs read access to that
repository. The nine
domains released on 2026-11-09 were installed this way on 2026-11-10; the
`metabolomics` entry was last installed before its source moved to the domain
repository (routes and dates: [`docs/STATUS.md`](docs/STATUS.md)).

Each collection advertises one skill, `<domain>-router`, at
`skills/_router/SKILL.md`. The corpus ships beside it as data and is read on
demand, so installation costs negligible context: the skills under
`leaves/<slug>/SKILL.md`, `skills_index.json`, `tools_index.json` with the tool
records under `tools/`, the composite workflows under `workflows/` with
`workflows/workflows_index.json` and a workflow router
`workflows/_workflow_router/SKILL.md` (not advertised), `kb_bundle.json` and
the search script `bin/search_skills.py`.

### Codex: plugin marketplace

```bash
codex plugin marketplace add HolobiomicsLab/asb-skill-collections
codex plugin add metabolomics@asb-skill-collections
```

The same marketplace serves Codex, under the same domain names and with the
same read access to the private domain repository.

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

A selection installed this way ships the grounding binder in its own `bin/`.

### Zenodo archive and direct consumption

Readers without access to the domain repositories use the release archives.
The complete metabolomics v3 release (`metabolomics-v3.0.2`) is at
[10.5281/zenodo.24122117](https://doi.org/10.5281/zenodo.24122117); the earlier
v3 deposits are [10.5281/zenodo.24093587](https://doi.org/10.5281/zenodo.24093587) (v3.0.1) and
[10.5281/zenodo.24054446](https://doi.org/10.5281/zenodo.24054446) (v3.0.0), and v2 is at
[10.5281/zenodo.20794027](https://doi.org/10.5281/zenodo.20794027). The DOIs of
the other domains are in `collections.yaml`.

For GitHub Copilot or another agent without a plugin host, read the collection
from a domain checkout or an extracted archive. Start at
`<collection root>/skills/_router/SKILL.md` and use the search script and the
machine indexes below. No runtime or build step is needed.

For a chat assistant through a web UI, upload the chosen collection's
`skills_index.json`, `tools_index.json` and the few required leaf `SKILL.md`
files as knowledge, then paste a short routing instruction. Do not upload the
whole collection. This route was not verified end to end.

## Use: search, apply, ground

`<collection root>` is the directory that holds `skills_index.json`: in a
domain checkout `<domain checkout>/collections/metabolomics/v3`, in an installed
plugin the directory two levels above the router's `SKILL.md`. Write it as an
absolute path; the commands then run from any working directory.

**1. Search** with the shipped script, then read the one file it names:

```bash
# one atomic skill
python3 "<collection root>/bin/search_skills.py" --query "<the task>" -k 10
# an end-to-end workflow for a whole analysis goal
python3 "<collection root>/bin/search_skills.py" --query "<the goal>" --target workflows -k 3
# a tool record
python3 "<collection root>/bin/search_skills.py" --query "<tool or task>" --target tools -k 5
```

Every hit prints the absolute `read:` path; a skill hit also its licence tier
and first source DOI, a tool hit its tier and recorded licence. `--json` adds
the scoring explanation. A search that matches nothing says what to try next.
(The scripts released on 2026-11-09, selector 1.0.0, print the explanation as a
JSON line under each hit and no DOI.)
Narrow with `--tool <name>` or `--edam <iri-substring>`; `--technique <tag>`
only matches where the index carries technique tags (95 of the metabolomics v3
skills, none in the other nine collections). The routers released on 2026-11-09 write the
command as `python bin/search_skills.py ...`, which fails without a `python`
executable (a stock macOS has only `python3`) and from any directory but the
collection root; run the absolute `python3` form above instead.

The indexes can also be queried directly:

- `skills_index.json`: `slug`, `name`, `description`, `edam_operation`,
  `edam_topics`, `tools`, `dois`, `techniques`, `license_tier`,
  `provenance_tier`.
- `tools_index.json`: `slug`, `name`, `edam_topics`, `dois`, `license`,
  `license_tier`, `license_detection`, `license_subject`, `repo_url`,
  `techniques`, `used_by_skills`. `repo_url` is the tool repository where one
  was resolved.

```bash
# skills that use a given tool
jq -r '.[] | select(.tools[]? | ascii_downcase | test("sirius")) | .slug' \
  <collection root>/skills_index.json
# skills by EDAM topic (Metabolomics = topic_3172)
jq '.[] | select(.edam_topics[]? | test("topic_3172")) | {slug,name}' \
  <collection root>/skills_index.json
# keyword over name and description
jq -r '.[] | select(.description | test("library match";"i")) | .slug' \
  <collection root>/skills_index.json
```

**2. Apply:** read `<collection root>/leaves/<slug>/SKILL.md`. Its body is the
procedure with verbatim evidence lines from the source. Its frontmatter carries
`description` and `when_to_use_negative`, `tools` (each with its `role` and,
where known, `repo`), `provenance.source_papers` (DOI and title of each source
paper) and `metadata` (`tools`, `license_tier`, `repo_url`, `edam_operation`,
`edam_topics`, `provenance_tier`). A workflow hit points to
`workflows/<slug>/SKILL.md`: follow its stages in order, each naming its
candidate leaf skills.

**3. Ground, recommended:** verify a parameter, threshold or claim against the
source paper or repository. The skill-to-source map, including `asb-paper-<doi>`
KB slugs and `repo_urls`, is precomputed in `kb_bundle.json` in every released
collection. Run the binder of this repository on the collection path. A
selection installed with `asbb install` carries a copy in its `bin/`, and the
deposit builder (`scripts/zenodo_deposit.py`) bundles one under `scripts/`
beside the collection, with this file:

```bash
# KB backend: Perspicacité at PERSPICACITE_BASE
python3 <master checkout>/scripts/perspicacite_kb_bind.py prepare \
  --collection "<collection root>" --skill <slug>
python3 <master checkout>/scripts/perspicacite_kb_bind.py query \
  --collection "<collection root>" --skill <slug> \
  --question "What threshold does the method recommend?"

# Serverless backend: clone source repositories and fetch an OA paper where possible
python3 <master checkout>/scripts/perspicacite_kb_bind.py local \
  --collection "<collection root>" --skill <slug> --paper

# Offline map only
python3 <master checkout>/scripts/perspicacite_kb_bind.py resolve \
  --collection "<collection root>" --skill <slug>
```

Tiers (`--tier`) are `paper` (full text and supplementary information, default),
`si` (supplementary information emphasised) and `repo` (read the tool source).
Without the binder, read the DOIs in the leaf's `provenance.source_papers`.

**Recommended agent loop:** prefer `kb` when Perspicacité is available. Use
`prepare` to warm it, then `query` before acting on a claim. When the server is
down, use `local` to clone and read the source directly.

## Licence tiers

Every skill carries a `license_tier` for the tool it relies on, in
`skills_index.json` and in its frontmatter `metadata.license_tier`; the skill
text itself is CC-BY-4.0. `open`: commercial use allowed. `noncommercial`:
academic or non-commercial use only; confirm a non-commercial purpose before
applying the skill. `restricted`: a licence was established and it constrains
reuse (for example a vendor licence); check it before commercial use or
redistribution. `unknown`: no licence for the tool was established; treat it as
all rights reserved until checked. See
[`governance/LICENSE_TIERS.md`](governance/LICENSE_TIERS.md) for the policy.

## Notes

- Collection content is CC-BY-4.0. Every skill names its source DOIs through
  `provenance.source_papers`, carries verbatim evidence lines and EDAM
  annotations, and passed the release gate. The gate report and the other
  release receipts are in the domain repository under `receipts/<cut-id>/`,
  not inside the collection.
- [`collections.yaml`](collections.yaml) is the release registry. It records
  the releases of ten domains, each in its private repository
  `asb-skills-<domain>`, and the legacy v1 trees of metabolomics, epigenomics
  and transcriptomics.

## Report and contribute

Offer the user a report yourself, without being asked, at each distinct
problem: a procedure failed or no longer matches the tool; the search returned
nothing usable and the work was done unaided; the user names a method paper
whose DOI the search does not find; the leaves existed but had to be composed by
hand; a command of the collection itself failed. Name one of four routes:

1. this skill is wrong or could be better;
2. a skill is missing: request it, or propose yours;
3. a paper is not referenced: propose it;
4. something technical failed: report it.

Offer once per problem and never again after a refusal. Draft the report, show
the user its exact title, labels and body, and post only on an explicit yes.
Never paste paths, credentials or sample names. Draft with
`asbb report <skill|missing|paper|fault>`, or with `bin/report_issue.py` where a
collection ships it. For routes 1 and 2 only,
`python3 scripts/skill_feedback.py` from this checkout is also a fallback. Each
helper redacts and prints a prefilled address, and none posts. With `gh`
and the user's yes, file with
`gh issue create --repo HolobiomicsLab/asb-skill-collections`; otherwise give the
user the address. Every route lands on the public registry's issue tracker: the
domain repositories are private, and a maintainer carries each report into them.
Routes, templates and triage: [`.github/CONTRIBUTING.md`](.github/CONTRIBUTING.md)
and [`docs/CONTRIBUTION_LOOP.md`](docs/CONTRIBUTION_LOOP.md).
