# Workflow Challenge: `coll_microbemasst_workflow`


> Six domain-specific MASST web applications (microbeMASST, plantMASST, tissueMASST, microbiomeMASST, foodMASST, and metadataMASST) are available with documented live URLs and associated peer-reviewed or preprint publications. The repository contains code and data for these applications, which operate as standalone spectrum-search tools with underlying routing logic in the GNPS_MASST codebase and aggregation capabilities in metadataMASST.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 3-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

This repository provides code and data for six domain-specific MASST web applications developed in the Dorrestein Lab. The applications—microbeMASST, plantMASST, tissueMASST, microbiomeMASST, foodMASST, and metadataMASST—each have documented live URLs and associated publications in peer-reviewed or preprint venues. The standalone web applications allow users to search one spectrum at a time; the underlying routing code is available in the GNPS_MASST codebase. metadataMASST functions as an aggregation layer that accepts search outputs from one or more domain-specific MASST runs and produces visualizable summary artifacts.

## Research questions

- What are the complete set of domain-specific MASST standalone web applications, their live URLs, and their associated publications as documented in the domainMASSTs repository?
- How does the routing mechanism direct a user-submitted spectrum to the appropriate domain-specific MASST application based on the user-selected domain context?
- How does metadataMASST ingest and combine search output files from multiple domain-specific MASST tools into a unified, visualizable summary?

## Methods overview

Retrieve the domainMASSTs repository from Zenodo or GitHub source Parse the README file to locate documented standalone web applications Extract application names, live URLs, and publication metadata Validate URL accessibility for each application Compile structured inventory with verification status Validation: Confirm all six applications (microbeMASST, plantMASST, tissueMASST, microbiomeMASST, foodMASST, metadataMASST) are present in the inventory with accessible URLs and documented publication links where available Define domain-to-application mapping: microbial → microbeMASST, plant → plantMASST, tissue → tissueMASST, microbiome → microbiomeMASST, food → foodMASST, metadata aggregation → metadataMASST. Implement conditional routing logic that parses user-submitted domain context metadata and selects the target application endpoint. Integrate routing module with GNPS_MASST codebase architecture and validate compatibility with existing spectrum submission workflows. Test routing module with representative spectrum submissions across all six domain categories to confirm correct application dispatch. Validation: all test spectra are routed to their designated domain-specific application with 100% accuracy; routing module executes without errors on the GNPS_MASST codebase. Load search output files from one or more domain-specific MASST tools Parse and normalize metadata and match results across domain-specific formats Merge records from multiple MASST outputs into a unified structure Generate combined visualizable summary artifact for metadataMASST interface Validation: verify aggregated output contains all input records and is compatible with metadataMASST web interface rendering

**Domain:** metabolomics

**Techniques:** molecular-networking, spectral-library-matching, database-annotation, cosine-similarity-scoring

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** The domainMASSTs repository contains code and data for microbeMASST, plantMASST, tissueMASST, microbiomeMASST, and foodMASST. _[grounded: domainMASST_system]_
- **(finding)** Aggregated search outputs can be generated and visualized using metadataMASST. _[grounded: metadataMASST]_
- **(finding)** The code for different standalone web applications can be found in GNPS_MASST repository. _[grounded: GNPS_MASST_tool]_
- **(finding)** microbeMASST is available as a standalone web application at https://masst.gnps2.org/microbemasst/. _[grounded: microbeMASST]_
- **(finding)** plantMASST is available as a standalone web application at https://masst.gnps2.org/plantmasst/. _[grounded: plantMASST]_
- **(finding)** tissueMASST is available as a standalone web application at https://masst.gnps2.org/tissuemasst/. _[grounded: tissueMASST]_
- **(finding)** microbiomeMASST is available as a standalone web application at https://masst.gnps2.org/microbiomemasst/. _[grounded: microbiomeMASST]_
- **(finding)** foodMASST is available as a standalone web application at https://masst.gnps2.org/foodmasst2/. _[grounded: foodMASST]_
- **(finding)** metadataMASST is available as a standalone web application at https://masst.gnps2.org/metadatamasst/. _[grounded: metadataMASST]_
- **(finding)** microbeMASST has a publication in Nature Microbiology. _[grounded: microbeMASST]_
- **(finding)** plantMASST has a publication in bioRxiv. _[grounded: plantMASST]_
- **(finding)** tissueMASST has a publication in bioRxiv. _[grounded: tissueMASST]_
- **(finding)** microbiomeMASST has a publication in bioRxiv. _[grounded: microbiomeMASST]_
- **(finding)** foodMASST has a publication in npj Science of Food. _[grounded: foodMASST]_

## Steps

### Step `task_001`
- Title: Reproduce the enumeration of domain-specific MASST components and their published URLs from the repository README
- Task kind: `reproduction`
- Task: Extract and verify the complete list of standalone web applications (microbeMASST, plantMASST, tissueMASST, microbiomeMASST, foodMASST, metadataMASST) from the domainMASSTs repository README, documenting their live URLs and associated publication links.
- Inputs:
  - domainMASSTs repository README file
- Expected outputs:
  - Structured inventory of standalone web applications with live URLs and publication links
- Tools: microbeMASST, plantMASST, tissueMASST, microbiomeMASST, foodMASST, metadataMASST, GNPS_MASST
- Landmark output files: readme_extracted_text.txt, application_urls_raw.json
- Primary expected artifact: `masst_applications_inventory.csv`

### Step `task_002`
- Depends on: `task_001`
- Title: Reconstruct the conditional dispatch routing mechanism that maps a spectrum query to the appropriate domain-specific MASST component
- Task kind: `component_reconstruction`
- Task: Implement the routing logic that directs user-submitted mass spectra to the appropriate domain-specific MASST web application (microbeMASST, plantMASST, tissueMASST, microbiomeMASST, foodMASST, or metadataMASST) based on user-selected domain context. Produce a routing decision module compatible with the GNPS_MASST codebase.
- Inputs:
  - User spectrum submission with domain context metadata
  - GNPS_MASST codebase and routing configuration
- Expected outputs:
  - Routing decision module specifying domain-to-application mappings
  - Routing test results confirming correct spectrum dispatch to each domain-specific application
- Tools: microbeMASST, plantMASST, tissueMASST, microbiomeMASST, foodMASST, metadataMASST, GNPS_MASST
- Landmark output files: domain_mapping_config.json, routing_logic_test_cases.csv, routing_test_results.txt
- Primary expected artifact: `routing_module.py`

### Step `task_003`
- Depends on: `task_002`
- Title: Reconstruct the metadataMASST aggregation step that collects and visualizes search outputs across domain-specific MASST results
- Task kind: `component_reconstruction`
- Task: Implement the metadataMASST aggregation operation that ingests search output files from one or more domain-specific MASST runs (microbeMASST, plantMASST, tissueMASST, microbiomeMASST, foodMASST) and produces a combined, visualizable summary artifact.
- Inputs:
  - Search output file(s) from one or more domain-specific MASST tools (microbeMASST, plantMASST, tissueMASST, microbiomeMASST, foodMASST)
- Expected outputs:
  - Combined, visualizable summary artifact aggregating results from domain-specific MASST searches
- Tools: metadataMASST, microbeMASST, plantMASST, tissueMASST, microbiomeMASST, foodMASST
- Landmark output files: parsed_masst_outputs.csv, normalized_metadata.csv, aggregated_masst_summary.json
- Primary expected artifact: `aggregated_masst_summary.json`

## Final expected outputs

- `Combined, visualizable summary artifact aggregating results from domain-specific MASST searches` (type: file, tolerance: hash)

## How your attempt will be scored

ASB defines seven rubrics in `workflow_rubric.py` (STEP_ORDERING, INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT, TOOL_SELECTION, EFFICIENCY, CLAIM_VALIDATION, ADVERSARIAL_TRAP_AVOIDANCE). Which of them bind for *this* challenge depends on the tier and openness below.

### Tier evaluation profile

**Evaluator:** automated — filesystem presence + type-port resolution; END_TO_END_OUTPUT with declared per-output tolerance.
**Binding rubrics:** STEP_ORDERING, END_TO_END_OUTPUT (typed/tolerance), TOOL_SELECTION, CLAIM_VALIDATION.

### Openness stance

**Openness: open — validity-first.** The deterministic match-rubrics above are demoted to *informational*. The binding evaluator is **SCIENTIFIC_VALIDITY** (below). Any scientifically sound method that addresses the research question is valid, and novel findings or unexplored aspects can score positively — **different is not wrong**.

## SCIENTIFIC_VALIDITY (binding for open / mixed tasks)
Open/mixed steps are graded at **EvalTier** granularity by the shared card judge (`runner_checks` llm_judge), not by exact match. The judge assigns one of `reproduced` / `replicated` / `re_analyzed` / `consistent` / `improved`; `consistent` and `re_analyzed` earn partial credit per the tier multipliers (0.60 / 0.75), so a scientifically sound but different result is credited rather than failed. Exact-match rubrics (INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT) are **informational** for these tasks. Three axes the judge weighs:

1. **Addresses the research question** — does the attempt answer it?
2. **Defensible method** — sound, and respects the *Invariants* above?
3. **Results validity** — consistent with the claims, or a valid, evidenced extension? New supported claims earn credit, not penalty.

## Workflow characterisation

_Suter et al. 2025 (DOI 10.1016/j.future.2025.107974)._

- **Coupling:** loose

- **Composition modularity:** flat

- **Abstraction level:** intermediate

- **Orchestration planning:** dynamic

- **Data transport:** file

- **Characterisation confidence:** inferred


## Submission

Produce two artifacts in your output directory:

1. The output files at the paths declared under **Final expected outputs**.
2. An `attempt.json` matching the schema below.
3. _(Optional)_ `attempt_metrics.json` with `wall_time_s`, `total_tokens`, `cost_usd` for the EFFICIENCY rubric.

### `attempt.json` schema

```json
{
  "workflow_id": "coll_microbemasst_workflow",
  "agent_order": [
    "task_001",
    "task_002",
    "task_003"
  ],
  "intermediate_outputs": {
    "task_001": {
      "<output_name>": "<locator>"
    },
    "task_002": {
      "<output_name>": "<locator>"
    },
    "task_003": {
      "<output_name>": "<locator>"
    }
  },
  "final_outputs": {
    "Combined, visualizable summary artifact aggregating results from domain-specific MASST searches": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>",
    "task_002": "<tool_name>",
    "task_003": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._
