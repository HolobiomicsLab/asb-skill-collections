# Registry Contract: ASB-Skill-Collections Public Interface

**Status:** v0.1 · **Date:** 2026-06-14 · **Stability:** evolving with Phase 1 · **Owner:** release + registry machinery

## Overview

The ASB-Skill-Collections registry is the **public installation front door** for scientific-agent skills, tools, benchmarks, and capsules produced by the [AgenticScienceBuilder](https://github.com/HolobiomicsLab/AgenticScienceBuilder) pipeline. This document specifies the three layers of the registry:

1. **Claude Code plugin marketplace** (`.claude-plugin/marketplace.json`) — the install surface, the user-facing UX
2. **Semantic catalogue** (`catalogue.jsonld`) — the authoritative registry, machine-queryable, linked-data native
3. **Collection filesystem** (`collections/` + `staged-collections/`) — the backing storage for versioned skill bundles, benchmarks, and provenance

The local `asbb install` / `uninstall` materializer is described in §4. The
remaining registry and release sections retain historical design material;
`registry`, `verify` and `doctor` currently print stubs.

---

## 1. The Claude Code Plugin Marketplace (User Interface)

### 1.1 Install command syntax

Users discover and install collections via the Claude Code `/plugin install` command:

```bash
/plugin marketplace add HolobiomicsLab/asb-skill-collections
/plugin install <marketplace-name>@asb-skill-collections
```

**Example:**
```bash
/plugin install metabolomics@asb-skill-collections
# Or a technique pack:
/plugin install metabolomics-lc-ms@asb-skill-collections
```

Use `plugins[].name` from `.claude-plugin/marketplace.json`, such as
`metabolomics` or `metabolomics-lc-ms`. Its `source` points to the versioned
collection or pack directory; the plugin host handles installation and discovery.
Release tags such as `<slug>-v<N>` are separate from install names. Native host
storage and grounding setup are not performed by the local materializer below.

### 1.2 The marketplace.json schema

**Location:** `.claude-plugin/marketplace.json` (NOT the repo root — the manifest lives under the `.claude-plugin/` directory)

**Historical proposed schema** (current install names and sources come from the
actual `plugins[].name` and `plugins[].source` fields):

```json
{
  "schema_version": "1.0",
  "name": "ASB Skill Collections",
  "description": "Curated scientific-agent skill and benchmark collections from the AgenticScienceBuilder pipeline.",
  "publisher": {
    "name": "Holobiomics Lab",
    "url": "https://github.com/HolobiomicsLab",
    "orcid_org": "https://orcid.org/0000-0002-XXXX-XXXX"
  },
  "plugins": [
    {
      "id": "metabolomics-v1",
      "name": "Metabolomics Skills",
      "version": "1",
      "slug": "metabolomics",
      "description": "Curated skills for computational metabolomics and mass spectrometry analysis.",
      "repository": "https://github.com/HolobiomicsLab/asb-skill-collections",
      "location": "collections/metabolomics/v1",
      "require_open_access": true,
      "openness": "open",
      "skills_count": 42,
      "tools_count": 8,
      "doi": "10.5281/zenodo.PLACEHOLDER-metabolomics-v1",
      "released_at": "2026-06-30T00:00:00Z",
      "lead_curator": {
        "name": "Curator Name",
        "orcid": "0000-0000-0000-0000",
        "github": "curator-handle"
      }
    }
  ]
}
```

**Fields:**

| Field | Type | Req | Description |
|-------|------|-----|---|
| `schema_version` | string | Y | Marketplace schema version (currently `1.0`) |
| `name` | string | Y | Publisher-level name |
| `description` | string | Y | Publisher-level description |
| `publisher.name` | string | Y | Publisher name (e.g., "Holobiomics Lab") |
| `publisher.url` | string | Y | Publisher GitHub URL |
| `publisher.orcid_org` | string | Y | Org-level ORCID (TODO: real ORCID; placeholder for v0) |
| `plugins[].id` | string | Y | Unique plugin ID, format `<slug>-v<N>` |
| `plugins[].name` | string | Y | Human-readable plugin name |
| `plugins[].version` | string | Y | Semantic version string (e.g., `"1"`, `"2.1"`) |
| `plugins[].slug` | string | Y | Collection slug, lower-case, matches `collections/<slug>/` |
| `plugins[].description` | string | Y | Collection description (50–300 chars, no marketing terms) |
| `plugins[].repository` | string | Y | GitHub repo URL (points to `asb-skill-collections`) |
| `plugins[].location` | string | Y | Path inside repo to the collection root, e.g., `collections/metabolomics/v1` |
| `plugins[].require_open_access` | bool | Y | **v0 policy: always `true`** — excludes non-OA sources from public catalogue |
| `plugins[].openness` | enum | Y | `"open"` \| `"mixed"` \| `"closed"` — the benchmark_tier.openness of all benchmarks in the collection |
| `plugins[].skills_count` | int | Y | Count of SKILL.md files in the unit's leaf dir (`leaves/`, or `skills/` for legacy units) |
| `plugins[].tools_count` | int | Y | Count of tools in `tools.json` |
| `plugins[].doi` | string | N | Zenodo DOI minted at release (see §2.4); TODO for v0 |
| `plugins[].released_at` | string (ISO 8601) | N | Release timestamp (UTC with Z suffix) |
| `plugins[].lead_curator` | object | N | Lead curator contact info (name, ORCID, GitHub handle) |

**Regeneration:** Marketplace.json is NOT automatically regenerated; it is **manually curated** alongside catalogue.jsonld. The `regen_catalogue.py` script handles catalogue.jsonld only. A maintainer updates marketplace.json when a collection is ready to be advertised for public install.

### 1.3 Non-OA exclusion rule

**V0 Policy (locked 2026-06-14):** The public marketplace advertises **open-access collections only**.

A collection is publicly advertised **if and only if:**
1. `require_open_access: true` in marketplace.json (enforced during release-gate review)
2. All source papers carry an explicit OA/permissive-license tag verified in the collection's `sources.jsonld`
3. Every skill carries `derived_from` DOIs pointing only to OA sources

**Enforcement points:**
- **PR stage (validate.yml):** warns if `require_open_access: false` in a collection candidate
- **Release gate (asb release-gate):** hard-blocks publication if any source fails OA verification
- **Marketplace curation:** the maintainer does not add an entry to `plugins[]` unless both checks pass

**Post-v0 path:** Closed-source collections can be built privately (following §POLICY-content.md expansion post-v0) and stored in a **private registry** (e.g., Koda artifact store) accessible only to authorized users. The public marketplace remains OA-only in v0; a second "institutional" distribution layer is designed in Phase 3.

---

## 2. The Semantic Catalogue (Machine Interface)

### 2.1 catalogue.jsonld

**Location:** `catalogue.jsonld` (repo root, committed)

**Purpose:** Machine-queryable, linked-data native registry. Supports discovery, dependency resolution, and FAIR data citation.

**Schema:** JSON-LD, `@context` with ASB + EDAM + standard vocabularies (schema.org, xsd, w3id.org)

**Structure:**

```json
{
  "@context": {
    "@vocab": "https://schema.org/",
    "asb": "https://w3id.org/holobiomicslab/asb-skill/",
    "edam": "http://edamontology.org/",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "collections": {"@id": "asb:collections", "@container": "@set"},
    "domain_topics": {"@id": "asb:domainTopics", "@type": "@id", "@container": "@set"},
    "lead_curators": {"@id": "asb:leadCurators", "@container": "@set"},
    "skills_count": {"@id": "asb:skillsCount", "@type": "xsd:integer"},
    "tools_count": {"@id": "asb:toolsCount", "@type": "xsd:integer"},
    "generated_at": {"@id": "asb:generatedAt", "@type": "xsd:dateTime"},
    "released_at": {"@id": "asb:releasedAt", "@type": "xsd:dateTime"},
    "slug": "asb:slug"
  },
  "@type": "asb:SkillCollectionRegistry",
  "@id": "https://w3id.org/holobiomicslab/asb-skill/registry",
  "name": "ASB Skill Collection Registry",
  "description": "Auto-generated registry of all released ASB Skill Collections.",
  "generated_at": "2026-06-14T10:30:45Z",
  "collections": [
    {
      "@id": "https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1",
      "title": "Metabolomics Skills Collection",
      "version": "1",
      "slug": "metabolomics",
      "skills_count": 42,
      "tools_count": 8,
      "domain_topics": [
        "http://edamontology.org/topic_3172",
        "http://edamontology.org/topic_0121"
      ],
      "doi": "10.5281/zenodo.PLACEHOLDER-metabolomics-v1",
      "released_at": "2026-06-30T00:00:00Z",
      "lead_curators": [
        {
          "name": "Curator Name",
          "orcid": "https://orcid.org/0000-0000-0000-0000"
        }
      ]
    }
  ]
}
```

### 2.2 Generation and publication

**Generated by:** `scripts/regen_catalogue.py`, which walks `collections/*/v*/collection.yaml` and builds the registry

**Invoked by:**
- `release.yml` on every tag matching `<slug>-v[0-9]*`
- Manual invocation: `python scripts/regen_catalogue.py --repo-root . --output catalogue.jsonld`

**Publication:** Committed to the repo, served by GitHub Pages and Zenodo (as part of collection releases; see §2.4)

**Determinism:** Collections are sorted alphabetically by slug + version; timestamps use UTC ISO 8601 (Z suffix); no non-deterministic ordering

### 2.3 Querying the catalogue

**Common queries** (examples for linked-data consumers):

```sparql
# Find all open-access metabolomics collections
SELECT ?collection ?version ?doi
WHERE {
  ?collection rdf:type asb:SkillCollectionRegistry ;
    asb:slug "metabolomics" ;
    asb:releasedAt ?released .
  ?collection asb:version ?version ;
    schema:identifier ?doi .
}
ORDER BY DESC(?released)
LIMIT 1
```

```python
# Python: fetch and parse the catalogue
import json
import urllib.request

url = "https://raw.githubusercontent.com/HolobiomicsLab/asb-skill-collections/main/catalogue.jsonld"
with urllib.request.urlopen(url) as response:
    catalogue = json.loads(response.read())

for col in catalogue.get("collections", []):
    print(f"{col['slug']} v{col['version']}: {col['skills_count']} skills")
```

### 2.4 DOI and versioning

**One Zenodo concept-DOI per collection-release** (locked decision 2026-06-14):

- A **collection-release** is a tagged commit matching `<slug>-v<N>` (e.g., `metabolomics-v1`)
- On tag, `release.yml` creates a **new Zenodo deposition**, uploads `collections/<slug>/v<N>/`, and mints a **versioned DOI** (e.g., `10.5281/zenodo.1234567`)
- The **concept-DOI** (e.g., `10.5281/zenodo.1234566`) links all versions; the README badge points to the concept
- Every version's DOI is stored in `CITATION.cff` and the catalogue
- Indicium exports (claims, SSSOM, PROV, etc.) are attached as **FILES inside the Zenodo deposition**, not separate DOIs

**Why one concept per collection:** Simplifies citation, enables "latest version" resolution, and keeps the DOI tree flat (no matrix explosion from multi-LLM variants).

---

## 3. Collection Filesystem Structure

### 3.1 Directory layout

```
asb-skill-collections/
├── collections/                  # Released, tagged collections
│   ├── metabolomics/
│   │   └── v1/
│   │       ├── collection.yaml            # collection metadata + skills/tools lists
│   │       ├── SKILL.md                   # router skill (entrypoint)
│   │       ├── skills/
│   │       │   ├── skill-name-1/SKILL.md
│   │       │   └── skill-name-2/SKILL.md
│   │       ├── tools.json                 # deduped tool registry
│   │       ├── mcp/
│   │       │   └── tools.json             # optional: MCP tool descriptors
│   │       ├── benchmark/
│   │       │   ├── README.md
│   │       │   ├── tasks.jsonl
│   │       │   ├── claims/
│   │       │   └── leaderboard.jsonld
│   │       ├── kb.yaml                    # KB dependency + pinned profile
│   │       ├── CITATION.cff               # per-collection citation (updated at release)
│   │       ├── ro-crate-metadata.json     # RO-Crate 1.1 + Workflow Run 0.5
│   │       └── README.md
│   └── epigenomics/
│       └── v1/ ...
│
├── staged-collections/           # In-progress, under review
│   └── transcriptomics/
│       └── v1/ ...
│
├── .claude-plugin/
│   └── marketplace.json          # Plugin manifest (user-facing install surface)
│
├── catalogue.jsonld              # Machine-readable registry (auto-generated)
├── CITATION.cff                  # Root-level citation (updated per release)
├── governance/                   # policy & governance (COI · content · OA · dispute · opt-out · maintainers · rollback)
├── .github/CONTRIBUTING.md       # curator workflow
├── AGENTS.md · CLAUDE.md         # agent-facing guides
├── LICENSE · LICENSING.md        # Apache-2.0 (code) + CC-BY-4.0 (content)
└── README.md                     # quick start + badges
```

### 3.2 collection.yaml schema

**Per-collection metadata file** at `collections/<slug>/v<N>/collection.yaml`

**Required fields:**

```yaml
# Metadata
title: "Metabolomics Skills Collection"
slug: metabolomics
version: "1"
description: "Curated procedural knowledge for computational metabolomics."

# Content counts
skills_count: 42
tools_count: 8

# FAIR metadata
@id: "https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1"
domain_topics:
  - "http://edamontology.org/topic_3172"  # Metabolomics
  - "http://edamontology.org/topic_0121"  # Computational biology

# Release + provenance
doi: "10.5281/zenodo.PLACEHOLDER-metabolomics-v1"
released_at: "2026-06-30T00:00:00Z"
require_open_access: true
openness: "open"

# Leadership
lead_curators:
  - name: "Curator Name"
    orcid: "https://orcid.org/0000-0000-0000-0000"
    github: "curator-handle"
    affiliation: "Institution Name"

# Source corpus + generation
corpus_doi: "TODO: asb-corpus-metabolomics release DOI"  # TODO: Phase 1
generation_manifest_sha: "TODO: MANIFEST.gen.json SHA256"  # TODO: Phase 1

# Gate report + provenance
gate_report_doi: "TODO: linked from Zenodo FILES"  # TODO: Phase 1
benchmark_tier: "silver"  # bronze | silver | gold — from ASB eval rubric
openness_axis: "open"  # closed | mixed | open — per WORKFLOW_CHALLENGE.md
```

### 3.3 kb.yaml schema

**KB dependency declaration** at `collections/<slug>/v<N>/kb.yaml`

Specifies how the skill bundle accesses its grounding knowledge base (Perspicacité embeddings, paper snapshots, claims ledger).

```yaml
# Grounding profile (pinned at release)
kb_profile: "openai-large"  # immutable once released
kb_model: "text-embedding-3-large"
asb_version: "2026-06-14"  # ASB version that built this collection

# Access mode (mutually exclusive)
access:
  # Option 1: remote Perspicacité MCP endpoint
  mcp_endpoint: "http://localhost:8002/mcp"
  mcp_namespace: "asb-paper-metabolomics"  # optional; if omitted, uses asb-paper-*
  
  # Option 2: local snapshot (auto-downloaded at install)
  snapshot_url: "https://zenodo.org/records/SNAPSHOT-DOI/files/kb-metabolomics-v1.zip"
  snapshot_sha256: "abc123def456..."  # for integrity check

# Fallback (if neither above resolves)
fallback: "warn"  # warn | skip_grounding | fail
```

**Current local install behavior:** `asbb install` copies published grounding
metadata and bundled scripts; it does not register MCP endpoints, download a KB,
or install scientific tools. Keyword search is offline. Optional grounding uses
the unit's `bin/perspicacite_kb_bind.py`: `resolve` is offline, `prepare`/`query`
require Perspicacité, and `local` retrieves source material over the network.

---

## 4. The asbb CLI Helper (Local Installation)

Use the CLI from an importable local checkout. `install` resolves the marketplace
name and a source contained in that checkout; it does not fetch the collection. The Claude Code native
plugin marketplace remains the recommended Claude install route.

```bash
python3 -m asb_skill_collections.asbb_cli install --list-runtimes
python3 -m asb_skill_collections.asbb_cli install metabolomics --runtime agents --copy
python3 -m asb_skill_collections.asbb_cli install metabolomics-lc-ms --dest /path/to/skills
python3 -m asb_skill_collections.asbb_cli uninstall metabolomics-lc-ms --dest /path/to/skills --dry-run
```

**Roots:** `agents`, `codex`, `copilot` and `gemini` use their respective
`~/.<runtime>/skills` directories. `claude` uses the current project's
`.claude/skills`, or `~/.claude/skills` with `--user`. Rules targets use project
`.cursor/rules`, `.clinerules` and `.github/instructions`. `--dest` uses exactly
the supplied directory. From another project, make the checkout importable and
pass `--repo /path/to/checkout` (examples in [README.md](../README.md)).

**Managed unit:** `--copy`, `--dest` and all rules targets copy the selected
marketplace source into `<target-root>/.asbb-units/<marketplace-name>/`. The
source's directory structure is retained, including advertised `skills/`, leaf
data, indexes, `bin/` and supporting content. Every non-hidden regular file and
directory is included except `__pycache__`, `*.pyc`, `*.pyo`, `proposals` and
`outputs`. Hidden local content is excluded
except published `.claude-plugin` and `.zenodo.json` metadata. These exclusions
apply recursively; published runtime assets must not depend on excluded paths.
Source symlinks and special files are rejected rather than dereferenced. The
installer does not establish grounding quality or copy external dependencies.

Keep the source unit and destination in separate, non-overlapping directories.
Each owned directory includes its whole subtree; keep personal files outside it.
Skill targets retain small `SKILL.md` adapters at the original advertised names.
Rules targets retain their existing filenames and renderer metadata, adding a
relative collection-root instruction to the body. Both locate the original
skill and tell the consumer to resolve paths and run commands from the installed
unit. Leaves remain data. Default skill-target symlinks instead depend on the
source checkout remaining in place; the CLI prints that dependency explicitly.

**Receipt and cleanup:** `~/.asbb/installed.json` stores the canonical destination,
mode, owned entries, and `source` (`path`, `version`, `sha256`). Version comes from
`collection.yaml`, then plugin metadata, then the marketplace, or is `null` if
undeclared. SHA256 covers distributable relative paths, directory markers and
file content hashes, excluding local content. It describes the source at install
time, not later edits to a symlinked checkout.

Re-run `install` with the same target to synchronize and remove stale owned
entries; there is no separate `sync` command. Both installation and uninstallation
preflight all recorded paths before mutation. Parent traversal, absolute entries,
root entries, redirected symlinks and conflicting ownership are refused.
An original recorded source symlink can be unlinked, even if its source is gone;
its target is never deleted. Older external symlinks without a recorded target
are refused. Ordinary legacy copy records can be upgraded by reinstalling.
`--force` only permits overwriting unmanaged collisions. `--dry-run` previews
writes/removals and leaves the receipt unchanged. Match the original destination,
project cwd and Claude `--user` setting when uninstalling. Moving a copy preserves
retrieval, but management refuses a changed recorded destination.

The local adapter and filesystem contract is tested with synthetic units. It is
not a claim of a version-pinned native host smoke test. The following registry,
verification and export subsections describe historical planned behavior, not
implemented commands beyond the current stubs.

### 4.1 asbb registry commands

**`asbb registry list`**
Lists all published collections from the catalogue.

```
Metabolomics Skills Collection (metabolomics-v1)
  Skills: 42  Tools: 8  DOI: 10.5281/zenodo.PLACEHOLDER
  Released: 2026-06-30  Lead: Curator Name (ORCID)
  Openness: open
  Install: /plugin install metabolomics@asb-skill-collections
```

**`asbb registry validate [--remote]`**
Validates local catalogue.jsonld + marketplace.json against schemas.
- `--remote`: also checks Zenodo DOI resolution + w3id.org IRI reachability

**`asbb registry doctor`**
Health check: Perspicacité KB endpoint reachability, marketplace.json HTTP availability, Zenodo API status.

### 4.2 asbb verify-collection

Pre-release validation for a collection directory (used in the release gate):

```bash
asbb verify-collection collections/metabolomics/v1 \
  --require-open-access \
  --check-dois \
  --validate-ro-crate
```

Checks:
- collection.yaml schema compliance
- All derived_from DOIs resolve
- RO-Crate metadata validity
- SKILL.md frontmatter discipline (description length, no marketing terms)
- Open-access source tags (if `--require-open-access`)

### 4.3 asbb export-sssom

Experimental: exports SSSOM (Simple Standard for Sharing Ontology Mappings) from a collection's claims + predicates, mapping ASB/indicium terms to standard vocabularies (ECO, CiTO, PROV).

```bash
asbb export-sssom collections/metabolomics/v1 --format tsv > metabolomics-v1.sssom.tsv
```

Output is SSSOM 1.0.2 TSV, ready for ingestion into OLS Bioregistry or OBO Foundry.

---

## 5. The Release Pipeline (Release Gate + Marketplace Update)

### 5.1 Release tag format

```
<slug>-v<N>

Examples: metabolomics-v1, epigenomics-v2, transcriptomics-v1-claude-opus
```

Triggering a tag matching this pattern initiates:
1. **CI validation** (`release.yml` → tests + validate.yml gates)
2. **Catalogue regeneration** (`regen_catalogue.py`)
3. **Zenodo upload** (create deposition, mint DOI, attach indicium exports as FILES)
4. **CITATION.cff update** (record Zenodo DOI)
5. **Marketplace curation** (maintainer manually adds entry to marketplace.json)
6. **HuggingFace mirror** (dispatch to `mirror-to-hf.yml`)

### 5.2 Marketplace.json update workflow

The `release.yml` does **not** auto-update marketplace.json; instead:

1. `release.yml` completes (catalogue regenerated, DOI minted)
2. **Maintainer manually updates** `.claude-plugin/marketplace.json`:
   - Adds a new entry to `plugins[]` with the slug, version, DOI, and released_at timestamp
   - Or updates an existing entry if this is a patch release
3. Commits + pushes the marketplace update
4. Users can now install via `/plugin install <marketplace-name>@asb-skill-collections`

**Rationale:** Marketplace entries are declarations of public readiness; they should not be auto-populated from every tag. A maintainer's explicit sign-off ensures quality.

### 5.3 Staged-to-collections promotion

Collections incubate in `staged-collections/` for review before moving to `collections/`:

```
staged-collections/metabolomics/v1/  ──[PR: gate passes, maintainer approval]──>  collections/metabolomics/v1/
                                                                                    (tagged metabolomics-v1)
```

The promotion step is manual (move the directory), not automated. This allows:
- Review of the full collection before public tagging
- Graceful handling of failed gates (stay in staged, revert, iterate)
- Explicit decision points for tier assignment

---

## 6. Integration Points & Governance

### 6.1 Workflow diagram: install → catalogue → release

```
┌─────────────────────────────────────────────────────────────────┐
│                       User: /plugin install                     │
│              metabolomics@asb-skill-collections                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ├──> Resolve in marketplace.json (GitHub raw)
                         │    ↓
                         ├──> Fetch the marketplace entry's source unit
                         │    ├─ skills/ (advertisements)
                         │    ├─ leaves/, indexes, bin/ (retrieval assets)
                         │    └─ grounding metadata
                         │    ↓
                         └──> Plugin host installs and discovers the unit
                         
┌─────────────────────────────────────────────────────────────────┐
│                  release.yml (on tag)                           │
│              metabolomics-v1 tag created                        │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ├──> Validate (tests + gates)
                         ├──> regen_catalogue.py
                         │    └─> catalogue.jsonld updated
                         ├──> Zenodo upload + mint DOI
                         ├──> Update CITATION.cff
                         └──> Trigger mirror-to-hf.yml
                         
┌─────────────────────────────────────────────────────────────────┐
│              Maintainer: Curate marketplace.json                │
│              (manual step, not auto)                            │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         └──> Add entry to plugins[]
                              ├─ version, DOI, released_at
                              ├─ skills_count, tools_count
                              └─ lead_curator info
                              
                              Commit + push
                              
    → Now users can `/plugin install metabolomics@asb-skill-collections`
```

### 6.2 Quality gates

| Gate | Checked by | Blocks? | When |
|------|-----------|---------|------|
| **LinkML schema** | `validate.yml` gate 1 | PR | every commit to collections/ or staged-collections/ |
| **DOI resolution** | `validate.yml` gate 2 | PR | every commit |
| **Description discipline** | `validate.yml` gate 5 | PR | every commit |
| **EDAM IRI resolution** | `validate.yml` gate 6 | PR | every commit |
| **RO-Crate validity** | `validate.yml` gate 8 | PR | every commit |
| **indicium round-trip** | `validate.yml` gate 9 | PR | every commit (warn-only if indicium-adapters unavailable) |
| **Marketplace.json schema** | `validate.yml` gate 10 | PR | every commit |
| **Release-gate (release.yml)** | `release.yml` + human sign-off | tag | on `<slug>-v[0-9]*` tag |
| **Open-access requirement** | release-gate + marketplace curation | marketplace entry | at maintainer sign-off |
| **Community review** | (deferred to Phase 2) | N/A | future: before staged → collections promotion |

### 6.3 Governance: who can merge

**To `collections/` (release path):**
- Lead curator (`MAINTAINERS.md`) only
- All CI gates must pass
- One human sign-off (maintainer)

**To `staged-collections/` (incubation):**
- Any Curator tier or above (per COI_POLICY.md)
- All CI gates must pass
- Promotion to `collections/` requires maintainer approval + release tag

---

## 7. Grounded Current State (2026-06-14)

### 7.1 What exists now

- ✅ `marketplace.json` (schema, empty plugins list)
- ✅ `regen_catalogue.py` (deterministic catalogue builder)
- ✅ `release.yml` (Zenodo deposit, DOI mint, CITATION.cff update; double-fire known bug with mirror-to-hf.yml)
- ✅ `validate.yml` (gates 1, 2, 5, 6, 8, 9, 10 wired; gates 3, 4, 7, 11–14 not yet implemented)
- ✅ `collections/` + `staged-collections/` (empty, .gitkeep)
- ✅ `CONTRIBUTING.md`, `COI_POLICY.md`, `MAINTAINERS.md` (existing policies)
- ✅ `.claude/settings.json` (project-level plugin cache read permission)

### 7.2 TODO (human input required, Phase 0–1)

| Task | Owner | Input | When |
|------|-------|-------|------|
| **Populate org ORCID** | human | Real ORCID for Holobiomics Lab | Phase 0.2 |
| **First corpus DOI** | human | `asb-corpus-metabolomics` Zenodo DOI | Phase 1.1 |
| **Lead curator ORCID/affiliation** | human | Real ORCID + institution name per collection | Phase 1.3 |
| **Gate report schema** | agent | Formal schema for `gate_report.json` | Phase 0.3 |
| **MANIFEST.gen.json schema** | agent | Manifest format (corpus SHA, ASB ver, KB profile, LLM, seed) | Phase 0.4 |
| **Zenodo PLACEHOLDER DOI** | human | Replace `10.5281/zenodo.PLACEHOLDER*` with real concept DOIs | Phase 1.9 |
| **asbb CLI bootstrap** | agent | Skeleton `asbb` CLI with `registry list` + `verify-collection` | Phase 1.7 |

### 7.3 Known issues

- **Double-fire bug:** `release.yml` and `mirror-to-hf.yml` both trigger on `*-v[0-9]*` tags. `mirror-to-hf.yml` should become dispatch-only. (Not fixed in this doc; flagged for a separate step.)
- **indicium-adapters availability:** Gate 9 (verify-claims) skips gracefully if the package is not published yet. Expected to resolve during Phase 1.
- **OPEN_ACCESS_POLICY.md missing:** Referenced in `AgenticScienceBuilder/release/promote.py` but not yet committed. Will be authored as part of Phase 0.1 (`POLICY-content.md`).

---

## 8. Summary Table: Registry Layers & Contracts

| Layer | File | Format | Audience | Update trigger | Governance |
|-------|------|--------|----------|---|---|
| **Native install surface** | `.claude-plugin/marketplace.json` | JSON | Users: `/plugin install <marketplace-name>@asb-skill-collections` | Manual (maintainer) | Lead curator approval |
| **Machine registry** | `catalogue.jsonld` | JSON-LD (w3id IRIs) | Bots, linked-data clients, citation systems | Auto (regen_catalogue.py on tag) | Deterministic algorithm |
| **Collection metadata** | `collections/<slug>/v<N>/collection.yaml` | YAML (LinkML schema) | Release gate, regen_catalogue.py | Manual (collection author) | LinkML validation (gate 1) |
| **KB grounding** | `collections/<slug>/v<N>/kb.yaml` | YAML | Install script, skill runtime | Manual (collection author) | Optional (fail-soft if absent) |
| **Registry helper** | `asbb` CLI | shell commands | Maintainers, CI/CD, power users | Manual command invocation | No auto trigger |

---

## 9. References

- **§Specification:** `/Users/nothiasl/git/agenticsciencebuilder_dev/docs/asbb/SPEC.md` § 6–7 (Distribution & Installation)
- **§Implementation Plan:** `/Users/nothiasl/git/agenticsciencebuilder_dev/docs/asbb/PLAN.md` § Phase 0–1
- **§Release gate:** `POLICY-content.md` (authored Phase 0.1)
- **§Content policies:** `governance/COI_POLICY.md`, `.github/CONTRIBUTING.md`, `LICENSING.md`
- **§Linked data:** `catalogue.jsonld` context, w3id.org namespaces, indicium `uri-scheme.md`
- **§Workflows:** `.github/workflows/release.yml`, `.github/workflows/validate.yml`
- **§Scripts:** `scripts/regen_catalogue.py`, `scripts/check_coi.py`, `scripts/validate_leaderboard.py`

---

**Version history:**
- 2026-06-14 v0.1 — initial draft (Phase 0 deliverable)
