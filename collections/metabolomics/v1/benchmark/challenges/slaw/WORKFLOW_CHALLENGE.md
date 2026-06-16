# Workflow Challenge: `coll_slaw_workflow`


> SLAW is a scalable, containerized workflow for untargeted LC-MS processing that integrates peak picking, sample alignment, isotopologue and adduct grouping, gap-filling by data recursion, and extraction of consolidated MS2 spectra and isotopic data.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 3-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

SLAW implements a complete untargeted LC-MS processing pipeline with multiple integrated components. The workflow incorporates peak picking algorithms (Centwave, FeatureFinderMetabo, ADAP), followed by sample alignment and grouping of isotopologues and adducts. The pipeline includes gap-filling by data recursion as a processing step and extraction of consolidated MS2 spectra and isotopic data. SLAW is designed for scalability to efficiently process thousands of samples and features automated parameter optimization for peak picking, alignment, and gap-filling operations.

## Research questions

- How does SLAW implement gap-filling by data recursion to recover missing feature intensities across samples in untargeted LC-MS processing?
- How does SLAW group detected LC-MS features into isotopologue and adduct clusters after peak picking?
- How does SLAW extract and consolidate MS2 spectra and isotopic data from grouped feature ions across samples?

## Methods overview

Load aligned feature table containing missing (NA or zero) feature intensities from the alignment step Identify gaps: enumerate all missing feature intensity entries and their sample-feature coordinates Execute data recursion: for each missing entry, search across samples using retention time and m/z proximity windows to locate the same feature in alternate sample batches Retrieve and populate: fill missing intensities with values recovered from recursively matched samples Validation: confirm that all recoverable gaps have been filled and feature table dimensions match input (same samples and features) References: source article (DOI: 10.1021/acs.analchem.1c02687) Load aligned feature table with m/z, retention time, and intensity data. Define isotopologue mass differences (C13, N15, O18, D) and adduct mass transformations for the ionization mode. Cluster features by binning on retention time windows and linking features within mass tolerance of theoretical isotopologue/adduct masses. Assign group identifiers to isotopologues and adducts sharing the same molecular ion. Validation: grouped feature table contains all input features, each assigned a unique or shared group ID; mass differences between clustered features match theoretical isotopologue or adduct masses within specified ppm tolerance. References: source article (DOI: 10.1021/acs.analchem.1c02687) Load feature-grouped data structure and MS2 scan metadata from preceding processing steps. Map MS2 spectra to feature groups using retention time, m/z, and scan index linkages. Consolidate multiple MS2 scans per feature group by merging peak lists and intensities. Annotate isotopic relationships and adduct assignments within consolidated spectrum records. Validation: consolidated spectra file contains one entry per feature group with non-null MS2 mass list and isotope annotations present where applicable. References: source article (DOI: 10.1021/acs.analchem.1c02687)

**Domain:** metabolomics

**Techniques:** lc-ms, feature-detection, chromatogram-alignment, quality-control, normalization

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** SLAW is a scalable, containerized workflow for untargeted LC-MS processing. _[grounded: SLAW_system]_
- **(finding)** SLAW was developed by Alexis Delabriere in the Zamboni Lab at ETH Zurich. _[grounded: SLAW_system]_
- **(finding)** SLAW performs complete processing including peak picking, sample alignment, pick picking, grouping of isotopologues and adducts, gap-filling by data recursion, extraction of consolidated MS2 spectra and isotopic data. _[grounded: SLAW_system]_
- **(finding)** SLAW can process thousands of samples efficiently. _[grounded: SLAW_system]_
- **(finding)** SLAW wraps three main peak picking algorithms: Centwave, FeatureFinderMetabo, and ADAP. _[grounded: SLAW_system]_
- **(finding)** SLAW provides automated parameter optimization for picking, alignment, and gap-filling. _[grounded: SLAW_system]_
- **(finding)** The stable version of this repository is 1.0.0.
- **(finding)** The latest development version can be found on adelabriere/slaw:dev. _[grounded: SLAW_system]_
- **(finding)** The development version includes a fix for low memory/processor settings.
- **(finding)** SLAW development is continuing in the zamboni-lab GitHub. _[grounded: SLAW_system]_
- **(finding)** The recommended citation for SLAW is: Delabriere A, Warmer P, Brennsteiner V and Zamboni N, SLAW: A scalable and self-optimizing processing workflow for untargeted LC-MS, 2021. _[grounded: SLAW_system]_

## Sanctioned method substitutions
Using any of these instead of the source method is **not penalized**:
- Centwave, FeatureFinderMetabo, or ADAP can be used as alternative peak picking algorithms

## Steps

### Step `task_001`
- Title: Reconstruct the Automated Parameter Optimization Layer for Peak Picking, Alignment, and Gap-Filling
- Task kind: `component_reconstruction`
- Task: Implement the gap-filling-by-data-recursion step to recover missing feature intensities across samples in an LC-MS feature table. Output a completed feature table with filled missing values.
- Inputs:
  - Aligned feature table with missing intensities from peak picking and sample alignment
- Expected outputs:
  - Feature table with filled missing feature intensities recovered via data recursion
- Tools: Centwave, manual expert review
- Landmark output files: missing_feature_summary.csv, filled_feature_table.csv
- Primary expected artifact: `filled_feature_table.csv`

### Step `task_002`
- Depends on: `task_001`
- Title: Reconstruct the Gap-Filling by Data Recursion Component
- Task kind: `component_reconstruction`
- Task: Reconstruct the post-picking grouping module that clusters aligned LC-MS features into isotopologue and adduct groups. Produce a grouped feature table with cluster assignments.
- Inputs:
  - Aligned feature table from sample alignment step (containing m/z, retention time, and peak intensities across samples)
- Expected outputs:
  - Grouped feature table with isotopologue and adduct cluster assignments for each detected feature
- Tools: Centwave, SLAW grouping module
- Landmark output files: aligned_features.csv, isotope_mass_differences.txt, adduct_definitions.txt, grouped_features.csv
- Primary expected artifact: `grouped_features.csv`

### Step `task_003`
- Depends on: `task_002`
- Title: Reconstruct the Isotopologue and Adduct Grouping Component
- Task kind: `component_reconstruction`
- Task: Extract and consolidate MS2 spectra and isotopic data per feature group from aligned LC-MS data. Produce a structured spectral output file containing MS2 spectra and isotope annotations keyed by feature group identifier.
- Inputs:
  - Feature-grouped data from peak picking, alignment, and grouping of isotopologues and adducts
  - Raw or processed LC-MS data files containing MS2 spectra
- Expected outputs:
  - Consolidated MS2 spectra and isotopic data file indexed by feature group
- Tools: Centwave, SLAW
- Landmark output files: feature_group_index.csv, ms2_scan_mapping.txt
- Primary expected artifact: `consolidated_spectra.json`

## Final expected outputs

- `Consolidated MS2 spectra and isotopic data file indexed by feature group` (type: file, tolerance: hash)

## How your attempt will be scored

ASB defines seven rubrics in `workflow_rubric.py` (STEP_ORDERING, INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT, TOOL_SELECTION, EFFICIENCY, CLAIM_VALIDATION, ADVERSARIAL_TRAP_AVOIDANCE). Which of them bind for *this* challenge depends on the tier and openness below.

### Tier evaluation profile

**Evaluator:** automated — filesystem presence + type-port resolution; END_TO_END_OUTPUT with declared per-output tolerance.
**Binding rubrics:** STEP_ORDERING, END_TO_END_OUTPUT (typed/tolerance), TOOL_SELECTION, CLAIM_VALIDATION.

### Openness stance

**Openness: mixed — per-step.** Closed steps must reproduce (rubrics above bind on them); open steps are judged by **SCIENTIFIC_VALIDITY** (below). Invariants bind everywhere; different is not wrong on the open steps.

## SCIENTIFIC_VALIDITY (binding for open / mixed tasks)
Open/mixed steps are graded at **EvalTier** granularity by the shared card judge (`runner_checks` llm_judge), not by exact match. The judge assigns one of `reproduced` / `replicated` / `re_analyzed` / `consistent` / `improved`; `consistent` and `re_analyzed` earn partial credit per the tier multipliers (0.60 / 0.75), so a scientifically sound but different result is credited rather than failed. Exact-match rubrics (INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT) are **informational** for these tasks. Three axes the judge weighs:

1. **Addresses the research question** — does the attempt answer it?
2. **Defensible method** — sound, and respects the *Invariants* above?
3. **Results validity** — consistent with the claims, or a valid, evidenced extension? New supported claims earn credit, not penalty.

## Workflow characterisation

_Suter et al. 2025 (DOI 10.1016/j.future.2025.107974)._

- **Coupling:** loose

- **Composition modularity:** hierarchical

- **Abstraction level:** intermediate

- **Orchestration planning:** static

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
  "workflow_id": "coll_slaw_workflow",
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
    "Consolidated MS2 spectra and isotopic data file indexed by feature group": "<locator>"
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
