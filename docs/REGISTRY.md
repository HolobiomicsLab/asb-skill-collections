# Registry Contract: ASB-Skill-Collections Public Interface

**Status:** v0.1 · **Date:** 2026-06-14 · **Stability:** evolving with Phase 1 · **Owner:** release + registry machinery

## Overview

The ASB-Skill-Collections registry is the **public installation front door** for scientific-agent skills, tools, benchmarks, and capsules produced by the [AgenticScienceBuilder](https://github.com/HolobiomicsLab/AgenticScienceBuilder) pipeline. This document specifies the three layers of the registry:

1. **Claude Code plugin marketplace** (`.claude-plugin/marketplace.json`) — the install surface, the user-facing UX
2. **Semantic catalogue** (`catalogue.jsonld`) — the authoritative registry, machine-queryable, linked-data native
3. **Collection filesystem** (`collections/` + `staged-collections/`) — the backing storage for versioned skill bundles, benchmarks, and provenance

It also clarifies the non-install roles of the `asbb` CLI helper (registry operations, verification, doctor checks — not the install path).

---

## 1. The Claude Code Plugin Marketplace (User Interface)

### 1.1 Install command syntax

Users discover and install collections via the Claude Code `/plugin install` command:

```bash
/plugin install <slug>-v<N>@HolobiomicsLab/asb-skill-collections
```

**Example:**
```bash
/plugin install metabolomics-v1@HolobiomicsLab/asb-skill-collections
```

This command:
1. **Resolves the plugin source:** looks up `<slug>-v<N>` in the marketplace.json on GitHub (`https://raw.githubusercontent.com/HolobiomicsLab/asb-skill-collections/main/.claude-plugin/marketplace.json`)
2. **Fetches the skill bundle:** downloads the skill files, tools, and metadata from `collections/<slug>/v<N>/`
3. **Registers locally:** links the bundle into the user's `~/.claude/skills/` directory for Claude Code discovery
4. **Sets up MCP tools** (optional): if the bundle declares tools in `mcp/tools.json`, registers them in the user's MCP server config
5. **Links the KB** (optional): if `kb.yaml` specifies a Perspicacité or snapshot URL, provisions access to the grounding knowledge base

### 1.2 The marketplace.json schema

**Location:** `.claude-plugin/marketplace.json` (NOT the repo root — the manifest lives under the `.claude-plugin/` directory)

**Schema:**

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
| `plugins[].skills_count` | int | Y | Count of SKILL.md files in `skills/` |
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
├── CONTRIBUTING.md               # Curator workflow
├── COI_POLICY.md                 # Conflict-of-interest rules
├── MAINTAINERS.md                # Lead curator + team
├── LICENSE.md                    # Apache-2.0 + fair-use clause
└── README.md                     # Quick start + badges
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

**Install behavior:** The `asb-skills install` command reads `kb.yaml` and either:
- **MCP:** registers the endpoint in the user's MCP config and points skills to it
- **Snapshot:** downloads and unpacks the KB archive to `~/.claude/skills/<slug>-v<N>/kb/`
- **Fallback:** logs a warning and allows skills to run without grounding (graceful degrade)

---

## 4. The asbb CLI Helper (Registry Operations)

> **Caveat (locked):** The `asbb` CLI is **to-build (Phase 1.7)** and is scoped to **`registry` / `verify` / `doctor` ONLY**. It is a **registry utility, NOT the install surface**. The install surface is the Claude Code plugin marketplace (`/plugin install <slug>-v<N>@HolobiomicsLab/asb-skill-collections`, resolved via `.claude-plugin/marketplace.json`). Commands beyond `registry`/`verify`/`doctor` shown elsewhere in this doc (e.g. `export-sssom`) are aspirational/post-Phase-1.7 and are not part of the v0 surface.

The `asbb` command-line tool provides operations that do not go through Claude Code's `/plugin install`:

```bash
# Install path (Claude Code native — the ONLY install surface):
/plugin install metabolomics-v1@HolobiomicsLab/asb-skill-collections
#   resolved via .claude-plugin/marketplace.json

# Registry operations (asbb CLI — Phase 1.7, registry/verify/doctor only):
asbb registry ...   # registry subcommands (list / validate published collections)
asbb verify ...     # validate a collection / catalogue / marketplace before release
asbb doctor         # health check: DOI resolution, KB reachability, manifest availability
```

### 4.1 asbb registry commands

**`asbb registry list`**
Lists all published collections from the catalogue.

```
Metabolomics Skills Collection (metabolomics-v1)
  Skills: 42  Tools: 8  DOI: 10.5281/zenodo.PLACEHOLDER
  Released: 2026-06-30  Lead: Curator Name (ORCID)
  Openness: open
  Install: /plugin install metabolomics-v1@HolobiomicsLab/asb-skill-collections
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
4. Users can now install via `/plugin install <slug>-v<N>@...`

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
│              metabolomics-v1@HolobiomicsLab/asb-skills          │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ├──> Resolve in marketplace.json (GitHub raw)
                         │    ↓
                         ├──> Fetch from collections/metabolomics/v1/
                         │    ├─ skills/, tools.json, mcp/
                         │    ├─ kb.yaml (grounding config)
                         │    └─ ro-crate-metadata.json
                         │    ↓
                         ├──> Link to ~/.claude/skills/metabolomics-v1/
                         ├──> Register MCP tools (if present)
                         └──> Set up KB access (MCP or snapshot)
                         
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
                              
    → Now users can `/plugin install metabolomics-v1@...`
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
| **Install surface** | `.claude-plugin/marketplace.json` | JSON (schema 1.0) | Users: `/plugin install <slug>-v<N>@...` | Manual (maintainer) | Lead curator approval |
| **Machine registry** | `catalogue.jsonld` | JSON-LD (w3id IRIs) | Bots, linked-data clients, citation systems | Auto (regen_catalogue.py on tag) | Deterministic algorithm |
| **Collection metadata** | `collections/<slug>/v<N>/collection.yaml` | YAML (LinkML schema) | Release gate, regen_catalogue.py | Manual (collection author) | LinkML validation (gate 1) |
| **KB grounding** | `collections/<slug>/v<N>/kb.yaml` | YAML | Install script, skill runtime | Manual (collection author) | Optional (fail-soft if absent) |
| **Registry helper** | `asbb` CLI | shell commands | Maintainers, CI/CD, power users | Manual command invocation | No auto trigger |

---

## 9. References

- **§Specification:** `/Users/nothiasl/git/agenticsciencebuilder_dev/docs/asbb/SPEC.md` § 6–7 (Distribution & Installation)
- **§Implementation Plan:** `/Users/nothiasl/git/agenticsciencebuilder_dev/docs/asbb/PLAN.md` § Phase 0–1
- **§Release gate:** `POLICY-content.md` (authored Phase 0.1)
- **§Content policies:** `COI_POLICY.md`, `CONTRIBUTING.md`, `LICENSE.md`
- **§Linked data:** `catalogue.jsonld` context, w3id.org namespaces, indicium `uri-scheme.md`
- **§Workflows:** `.github/workflows/release.yml`, `.github/workflows/validate.yml`
- **§Scripts:** `scripts/regen_catalogue.py`, `scripts/check_coi.py`, `scripts/validate_leaderboard.py`

---

**Version history:**
- 2026-06-14 v0.1 — initial draft (Phase 0 deliverable)
