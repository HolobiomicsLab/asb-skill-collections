# Workflow Challenge: `coll_archr_workflow`


> ArchR is an R package for processing and analyzing single-cell ATAC-seq data that describes mechanisms for paired scATAC-seq and scRNA-seq multiome analysis, trajectory analysis via Monocle3 and Slingshot, and peak matrix export for STREAM compatibility.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 3-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

ArchR describes three analytical mechanisms for single-cell ATAC-seq analysis. For paired multiome workflows, the package outlines a four-step process: importFeatureMatrix ingests the feature matrix, addGeneExpressionMatrix adds scRNA-seq gene expression data, addIterativeLSI performs iterative dimensionality reduction, and addCombinedDims produces a joint reduced-dimension embedding integrating both modalities. For trajectory analysis, ArchR describes support for two complementary approaches through three functions: getMonocleTrajectories and addMonocleTrajectory enable Monocle3-based analysis, while addSlingShotTrajectories enables Slingshot-based analysis, allowing users to select their preferred trajectory method. Additionally, the package describes the exportPeakMatrixForSTREAM function to enable export of peak matrices compatible with STREAM.

## Research questions

- How does ArchR ingest paired scRNA-seq gene expression data alongside scATAC-seq chromatin accessibility data and produce a unified reduced-dimension embedding for joint analysis?
- How does ArchR conditionally invoke monocle3 versus Slingshot trajectory analysis functions based on user selection?
- What function does ArchR provide to export a peak-by-cell matrix in a format compatible with the STREAM trajectory analysis tool?

## Methods overview

Load scATAC-seq peak matrix and cell metadata into ArchR project object via importFeatureMatrix. Append scRNA-seq gene expression matrix to the same project via addGeneExpressionMatrix, aligning cells across modalities. Compute joint iterative LSI decomposition on accessibility and expression data via addIterativeLSI. Generate unified reduced-dimension embedding integrating both modalities via addCombinedDims. Validation: Confirm multiome project object contains both scATAC-seq and scRNA-seq assays with non-null LSI and combined dimension slots. Load a prepared ArchR project with precomputed reduced dimensions and cluster assignments. Evaluate the user-specified method selection parameter (Monocle3 or Slingshot). Conditionally invoke addMonocleTrajectory or addSlingShotTrajectories on the project based on selection. Return the modified ArchR project object containing the trajectory embedding result. Validation: confirm the output ArchR project object contains trajectory metadata and is compatible with downstream ArchR analyses. Load a preprocessed ArchR project containing single-cell ATAC-seq data with peak calls and cell annotations. Call the exportPeakMatrixForSTREAM function on the ArchR project object to generate a peak-by-cell matrix. Write the exported matrix to disk in STREAM-compatible CSV or TSV format (rows=peaks, columns=cells). Validation: confirm the output file exists, contains expected dimensions (peak count × cell count), and is readable by STREAM downstream analysis tools.

**Domain:** genomics

**Techniques:** clustering, dimensionality-reduction

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** ArchR now supports paired scATAC-seq and scRNA-seq analysis. _[grounded: archr_system]_
- **(finding)** ArchR provides the function importFeatureMatrix for paired analysis. _[grounded: archr_system]_
- **(finding)** ArchR provides the function addGeneExpressionMatrix for paired analysis. _[grounded: archr_system]_
- **(finding)** ArchR provides the function addIterativeLSI for paired analysis. _[grounded: archr_system]_
- **(finding)** ArchR provides the function addCombinedDims for paired analysis. _[grounded: archr_system]_
- **(finding)** ArchR now directly supports monocle3-based trajectory analysis. _[grounded: archr_system]_
- **(finding)** ArchR now directly supports Slingshot-based trajectory analysis. _[grounded: archr_system]_
- **(finding)** ArchR provides the function getMonocleTrajectories for trajectory analysis. _[grounded: archr_system]_
- **(finding)** ArchR provides the function addMonocleTrajectory for trajectory analysis. _[grounded: archr_system]_
- **(finding)** ArchR provides the function addSlingShotTrajectories for trajectory analysis. _[grounded: archr_system]_
- **(finding)** ArchR enables export of a peak matrix that is compatible with STREAM. _[grounded: archr_system]_
- **(finding)** ArchR provides the function exportPeakMatrixForSTREAM. _[grounded: archr_system]_
- **(finding)** ArchR is currently in Beta. _[grounded: archr_system]_
- **(finding)** ArchR is a full-featured R package for processing and analyzing single-cell ATAC-seq data. _[grounded: archr_system]_

## Sanctioned method substitutions
Using any of these instead of the source method is **not penalized**:
- monocle3 or Slingshot for trajectory analysis

## Steps

### Step `task_001`
- Title: Reconstruct the paired scATAC-seq and scRNA-seq multiome analysis pipeline in ArchR
- Task kind: `component_reconstruction`
- Task: Ingest paired scRNA-seq and scATAC-seq data into ArchR using importFeatureMatrix and addGeneExpressionMatrix, then compute joint reduced-dimension embeddings via addIterativeLSI and addCombinedDims to enable integrated multiome analysis.
- Inputs:
  - scATAC-seq peak matrix and cell metadata
  - scRNA-seq gene expression matrix aligned to the same cells
- Expected outputs:
  - ArchR project object containing both scATAC-seq and scRNA-seq data with joint LSI reduction and combined dimensional embedding
- Tools: ArchR, R
- Landmark output files: archR_project_with_scatac.rds, archR_project_with_scrna.rds, archR_project_with_lsi.rds

### Step `task_002`
- Depends on: `task_001`
- Title: Reconstruct trajectory analysis using Monocle3 and Slingshot dispatch in ArchR
- Task kind: `component_reconstruction`
- Task: Implement conditional trajectory analysis on a prepared ArchR project by invoking either addMonocleTrajectory (Monocle3) or addSlingShotTrajectories (Slingshot) based on user selection, producing a trajectory embedding object.
- Inputs:
  - Prepared ArchR project object with reduced dimensions and cluster assignments
  - User-specified trajectory method selection (monocle3 or Slingshot)
- Expected outputs:
  - ArchR project object with embedded trajectory result from selected method
- Tools: ArchR, monocle3, Slingshot, R

### Step `task_003`
- Depends on: `task_001`
- Title: Reconstruct peak matrix export for STREAM compatibility via exportPeakMatrixForSTREAM
- Task kind: `component_reconstruction`
- Task: Export a peak-by-cell matrix from an ArchR project using the exportPeakMatrixForSTREAM function and save the output in the format required by STREAM trajectory analysis.
- Inputs:
  - ArchR project object (RDS or in-memory R object) with preprocessed scATAC-seq data, including peak calls and cell barcodes
- Expected outputs:
  - Peak-by-cell matrix file in STREAM-compatible format (typically CSV or TSV with peaks as rows and cells as columns)
- Tools: ArchR, R, STREAM
- Landmark output files: archr_project_checkpoint.rds
- Primary expected artifact: `stream_peak_matrix.csv`

## Final expected outputs

- `ArchR project object with embedded trajectory result from selected method` (type: file, tolerance: hash)
- `Peak-by-cell matrix file in STREAM-compatible format (typically CSV or TSV with peaks as rows and cells as columns)` (type: file, tolerance: hash)

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
  "workflow_id": "coll_archr_workflow",
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
    "ArchR project object with embedded trajectory result from selected method": "<locator>",
    "Peak-by-cell matrix file in STREAM-compatible format (typically CSV or TSV with peaks as rows and cells as columns)": "<locator>"
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
