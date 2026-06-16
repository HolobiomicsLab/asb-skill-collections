# Workflow Challenge: `coll_metaboanalystr_workflow`


> MetaboAnalystR 4.0 is a unified LC-MS workflow software for global metabolomics. The paper describes this integrated pipeline but provides insufficient detail to characterize its feature table outputs.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 2-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

MetaboAnalystR 4.0 implements a unified LC-MS data processing pipeline for global metabolomics workflows. Analysis of feature table outputs produced by the MetaboAnalystR 4.0 workflow on public metabolomics data was performed; however, insufficient evidence is available in the provided text to characterize specific output metrics such as the number of features, samples, or intensity statistics.

## Research questions

- What is the architecture and workflow of MetaboAnalystR 4.0 for processing LC-MS data in global metabolomics?
- What are the dimensions and intensity statistics of the feature table produced by the MetaboAnalystR 4.0 LC-MS workflow when applied to a public LC-MS dataset?

## Methods overview

Initialize MetaboAnalystR environment and load raw LC-MS spectral files Apply peak detection algorithm to identify ion features across all samples Align detected peaks using retention-time and m/z matching criteria Consolidate aligned peaks into a quantitative feature table with sample-wise intensity values Validation: feature table contains ≥1 feature, intensity columns match sample count, and m/z and retention-time columns are populated without null values in feature identifiers Load raw LC-MS spectral data (mzML format) from public metabolomics repositories Apply MetaboAnalystR 4.0 unified workflow to detect peaks and quantify feature intensities Extract feature table structure and compute summary metrics (row/column counts, intensity statistics) Validation: Feature table row count ≥ 100 detected features, column count matching deposited sample count, peak intensity values reported as non-negative numeric ranges

**Domain:** metabolomics

**Techniques:** lc-ms, feature-detection, database-annotation, metabolite-identification, multivariate-statistics, statistical-analysis

## Steps

### Step `task_001`
- Title: Reconstruct the unified LC-MS data processing pipeline in MetaboAnalystR 4.0
- Task kind: `component_reconstruction`
- Task: Implement the complete MetaboAnalystR 4.0 LC-MS workflow from raw spectral data ingestion through peak detection, alignment, and quantitative feature table generation using the xia-lab/MetaboAnalystR GitHub repository.
- Inputs:
  - xia-lab/MetaboAnalystR GitHub repository (source code and configuration)
  - Raw LC-MS spectral data in mzML or mzXML format
- Expected outputs:
  - Quantitative feature table with m/z, retention time, and sample intensities
  - Peak detection and alignment quality report including feature count and missing value summary
- Tools: MetaboAnalystR
- Landmark output files: raw_peaks.csv, aligned_peaks.csv, feature_table.csv, qc_report.txt
- Primary expected artifact: `feature_table.csv`

### Step `task_002`
- Depends on: `task_001`
- Title: Analyze feature table output produced by the MetaboAnalystR 4.0 LC-MS workflow on a public metabolomics dataset
- Task kind: `analysis`
- Task: Execute the MetaboAnalystR 4.0 LC-MS workflow on a public metabolomics dataset and characterize the resulting feature table by reporting sample count, feature count, and peak intensity summary statistics.
- Inputs:
  - Raw LC-MS data in mzML format from a public metabolomics repository (MetaboLights or MassIVE accession)
- Expected outputs:
  - Feature table with rows as detected metabolite features and columns as samples, including peak intensity values
  - Summary statistics report containing feature count, sample count, and peak intensity descriptive statistics (mean, median, SD, min, max)
- Tools: MetaboAnalystR
- Landmark output files: raw_feature_table.csv, feature_summary_statistics.csv
- Primary expected artifact: `feature_summary_statistics.csv`

## Final expected outputs

- `Feature table with rows as detected metabolite features and columns as samples, including peak intensity values` (type: file, tolerance: hash)
- `Summary statistics report containing feature count, sample count, and peak intensity descriptive statistics (mean, median, SD, min, max)` (type: file, tolerance: hash)

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

- **Abstraction level:** implicit

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
  "workflow_id": "coll_metaboanalystr_workflow",
  "agent_order": [
    "task_001",
    "task_002"
  ],
  "intermediate_outputs": {
    "task_001": {
      "<output_name>": "<locator>"
    },
    "task_002": {
      "<output_name>": "<locator>"
    }
  },
  "final_outputs": {
    "Feature table with rows as detected metabolite features and columns as samples, including peak intensity values": "<locator>",
    "Summary statistics report containing feature count, sample count, and peak intensity descriptive statistics (mean, median, SD, min, max)": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>",
    "task_002": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._
