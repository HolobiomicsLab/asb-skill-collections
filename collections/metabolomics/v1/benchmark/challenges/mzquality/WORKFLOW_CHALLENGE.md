# Workflow Challenge: `coll_mzquality_workflow`


> mzQuality is a user-friendly R package that performs quality control of targeted metabolomics data through outlier detection, batch correction using pooled study quality control samples, and compound filtering, with support for internal standard recommendation and absolute concentration calculation.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

mzQuality provides a comprehensive workflow for quality control of targeted mass spectrometry metabolomics data. The package implements data import from tab-delimited and vendor formats, constructs SummarizedExperiment objects with automatic calculation of compound/internal standard ratios, and performs quality control analysis that tests pooled QC samples for outliers using compound/internal standard ratio and study samples for mis-injections using internal standard peak areas. Following analysis, mzQuality exhaustively calculates relative standard deviation of batch-corrected ratios (RSDQC) across all internal standard candidates for each compound to identify and recommend the internal standard yielding the lowest RSDQC. The package generates multiple visualization types including aliquot plots, compound plots, PCA plots, and violin plots for inspecting batch effects and data quality. Results are exported via the createReports function into organized folders containing plots and tab-delimited reports alongside human-friendly Excel summaries. The package supports optional absolute concentration calculation when calibration samples with known spiked concentrations are supplied, enabling downstream metabolic pathway modeling and between-cohort analyses.

## Research questions

- Does the buildExperiment function correctly construct a SummarizedExperiment object with a computed ratio assay when given a data frame with specified column mappings for compounds, samples, and internal standards?
- How does the doAnalysis function process a SummarizedExperiment object to identify outliers and mis-injections, and what corrected assay does it produce?
- Which internal standard achieves the lowest Relative Standard Deviation of QC samples (RSDQC) for each compound when calculated across all internal standard candidates on batch-corrected data?
- Does the createReports function generate the expected directory structure with Plots and Reports sub-folders and the correct file types when called with specified parameters?
- When the secondaryAssay column is not provided to buildExperiment, does the resulting 'ratio' assay equal the primary assay values unchanged?

## Methods overview

Load example.tsv from mzQuality package using readData function with built-in column validation. Map required columns (aliquot, compound, area, type, injection_time, batch) and optional concentration column to data frame. Call buildExperiment to construct a SummarizedExperiment object with features (compounds) as rows and samples (aliquots) as columns. Verify SummarizedExperiment structure: rowData contains compound identifiers, colData contains sample metadata, and assays include the computed ratio (area / area_is). Validation: SummarizedExperiment object can be created without errors, contains non-empty rowData and colData frames, and ratio assay is present and numeric. Load SummarizedExperiment object containing raw compound areas, internal standard areas, and sample metadata. Apply outlier detection on QC samples by evaluating Compound/Internal Standard ratios against control thresholds (qcPercentage=80). Test study samples for mis-injections using internal standard area thresholds (backgroundPercentage=40). Perform batch correction of Compound/Internal Standard ratios using pooled SQC samples within batch strata (useWithinBatch=TRUE). Filter out compounds with batch-corrected ratio RSD exceeding nonReportableRSD=30 threshold (removeBadCompounds=TRUE). Optionally calculate absolute concentrations via linear regression from calibration samples (single sample type only). Validation: output SummarizedExperiment contains 'ratio_corrected' assay with numeric batch-corrected ratio values, and metadata annotations identify all flagged outliers and mis-injections; concentration column (if input provided) contains numeric or NA values matching calibration line sample counts. Load batch-corrected SummarizedExperiment containing QC sample assays and compound/internal standard ratios. For each compound, compute relative standard deviation (RSD) of QC sample ratios across all internal standard candidates. Construct RSDQC matrix with compounds as rows and internal standards as columns. Identify minimum RSDQC internal standard for each compound. Validation: recommendation table contains all compounds with non-missing RSDQC values and internal standard assignments; RSDQC matrix is complete and consistent with recommendation selections. Load the pre-processed SummarizedExperiment object from the mzQuality analysis pipeline. Invoke createReports with summary and compound report flags enabled, quality thresholds (backgroundPercent=40, cautionRSD=15, nonReportableRSD=30), and assay specification (area). Generate Plots subdirectory containing quality-control visualizations and Reports subdirectory containing text and Excel files. Validation: Confirm directory structure exists with expected subdirectories and file extensions (*.png in Plots; *.txt and *.xlsx in Reports). Load example.tsv using readData function to validate column structure and data integrity. Construct SummarizedExperiment object via buildExperiment without secondaryAssay parameter. Extract 'ratio' and primary assays from the experiment object. Perform element-wise numerical comparison of ratio assay to primary assay values. Validation: all ratio values must equal primary assay values within double-precision floating-point tolerance (relative difference < 1e-14).

**Domain:** metabolomics

**Techniques:** quality-control, feature-detection, lc-ms, normalization, statistical-analysis

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** mzQuality features outlier detection, batch-correction using pooled study quality control samples (SQC), filters for removing unreliable compounds, various plots for inspecting, and generating reports for further processing. _[grounded: mzQuality_system]_
- **(finding)** mzQuality is available as an interactive Shiny dashboard application called mzQualityDashboard. _[grounded: mzQuality_system]_
- **(finding)** Quality Control is an important step in the analysis of mass spectrometry data.
- **(finding)** Existing tools phenomis and qmtools are designed with access to a phenotype in mind. _[grounded: tool_phenomis]_
- **(finding)** mzQuality was developed to perform outlier detection, batch correction and other quality control steps without the need for defined phenotypes. _[grounded: mzQuality_system]_
- **(finding)** mzQuality follows the recommendations of the mQACC for quality control by leveraging on proper batch design and the addition of various quality control samples. _[grounded: mzQuality_system]_
- **(finding)** mzQuality is capable of recommending different internal standards by exhaustively calculating the Relative Standard Deviation of QC samples (RSDQC) of batch-corrected ratios. _[grounded: mzQuality_system]_
- **(finding)** By supplying calibration line samples and known concentrations for spiked compounds, mzQuality is able to calculate absolute concentrations. _[grounded: mzQuality_system]_
- **(finding)** mzQuality features import of data from a variety of formats, including a generalized tab-delimited format and Sciex OS text exports. _[grounded: mzQuality_system]_
- **(finding)** phenomis provides tools for post-processing like quality control and normalization, as well as univariate statistics. _[grounded: tool_phenomis]_
- **(finding)** qmtools contains functions for processing quantitative metabolomics data, including imputation, normalization and filtering. _[grounded: tool_qmtools]_
- **(finding)** MatrixQCvis features interactive visualization of data quality metrics for various -omics datasets and uses the SummarizedExperiment object. _[grounded: comp_summarized_experiment]_
- **(finding)** mQACC is the Metabolomics Quality Assurance and Control Consortium. _[grounded: org_mqacc]_
- **(finding)** HUPO is the Human Proteome Organization.
- **(finding)** HUPO has a Quality Control working group that focuses on quality control in proteomics.
- **(finding)** mzQuality requires input data to be in a tab-delimited format. _[grounded: mzQuality_system]_
- **(finding)** The required columns for mzQuality input data include aliquot, compound, area, type, injection_time, and batch. _[grounded: mzQuality_system]_
- **(finding)** The readData function reads in data and checks for any missing or incorrect columns. _[grounded: tool_readData]_
- **(finding)** The buildExperiment function creates a SummarizedExperiment object from a data frame. _[grounded: comp_summarized_experiment]_
- **(finding)** In the current version of mzQuality, only one sample type can be used for calculating concentrations. _[grounded: mzQuality_system]_
- **(finding)** mzQuality internally uses Bioconductor's SummarizedExperiment object to store data. _[grounded: mzQuality_system]_
- **(finding)** The buildExperiment function automatically calculates the compound / Internal Standard ratio for each sample and stores it in the ratio assay. _[grounded: tool_buildExperiment]_
- **(finding)** The convertExperiment function converts names in an already built SummarizedExperiment object to the ones mzQuality uses. _[grounded: mzQuality_system]_
- **(finding)** The doAnalysis function tests QC samples for outliers using their Compound / Internal Standard ratio. _[grounded: tool_doAnalysis]_
- **(finding)** The doAnalysis function tests Study Samples for mis-injections using their Internal Standard areas. _[grounded: tool_doAnalysis]_
- **(finding)** aliquotPlot shows the distribution of the selected assay per aliquot, colored per sample type. _[grounded: tool_aliquotPlot]_
- **(finding)** The aliquotPlot can be used to inspect technical replicates for similar peak areas and peak ratios within a batch. _[grounded: tool_aliquotPlot]_
- **(finding)** All plots in mzQuality can be faceted using the facetPlot function. _[grounded: mzQuality_system]_
- **(finding)** The facetPlot function allows faceting by any column present in colData. _[grounded: tool_facetPlot]_
- **(finding)** compoundPlot is a scatter plot of a selected compound across samples. _[grounded: tool_compoundPlot]_
- **(finding)** PCA plot can be used to inspect variation within- and between batches.
- **(finding)** In the PCA plot, Quality Control samples used for batch correction should ideally be centered and form a tight cluster.
- **(finding)** The violin plot can be used to inspect the distribution of sample types.
- **(finding)** The Concentration Plot shows a linear model based on calculated ratio and known concentration. _[grounded: comp_ratio_assay]_
- **(finding)** The createReports function creates a folder containing the results of analysis separated by Plots and Reports. _[grounded: tool_createReports]_
- **(finding)** mzQuality is designed to be used by anyone with basic knowledge of R. _[grounded: mzQuality_system]_

## Sanctioned method substitutions
Using any of these instead of the source method is **not penalized**:
- phenomis or qmtools can be used as alternatives for post-processing and quality control

## Invariants (must not change)
Changing any of these **is** a failure regardless of openness:
- mzQuality is designed for use without access to defined phenotypes to remain unbiased, distinguishing it from tools like phenomis and qmtools.

## Steps

### Step `task_001`
- Title: Reconstruct the buildExperiment SummarizedExperiment construction step from a tab-delimited input file
- Task kind: `component_reconstruction`
- Task: Load the example.tsv file using readData, then construct a SummarizedExperiment object via buildExperiment with documented column mappings (aliquot, compound, area, type, injection_time, batch, concentration) to produce an experiment object containing the 'ratio' assay. Verify object structure including rowData, colData, and assays.
- Inputs:
  - example.tsv file from mzQuality package (extdata/example.tsv)
- Expected outputs:
  - SummarizedExperiment object with rowData, colData, and assays including 'ratio'
- Tools: mzQuality, R, SummarizedExperiment
- Landmark output files: cleaned_data_frame.tsv, se_object.rds

### Step `task_002`
- Depends on: `task_001`
- Title: Reconstruct the doAnalysis quality-control and batch-correction step to produce the ratio_corrected assay
- Task kind: `component_reconstruction`
- Task: Apply the doAnalysis function with default parameters (removeOutliers=TRUE, useWithinBatch=TRUE, removeBadCompounds=TRUE, qcPercentage=80, backgroundPercentage=40, nonReportableRSD=30) to a SummarizedExperiment object to perform quality control analysis, producing an experiment with ratio-corrected assays and outlier/mis-injection annotations.
- Inputs:
  - task_001.expected_outputs[0]: SummarizedExperiment object with rowData, colData, and assays including 'ratio'
  - SummarizedExperiment object with raw compound area and internal standard area assays, sample metadata (type, batch, injection_time), and compound annotations
- Expected outputs:
  - SummarizedExperiment object with 'ratio_corrected' assay containing batch-corrected Compound/Internal Standard ratios
  - Outlier annotations on QC samples flagged by Compound/Internal Standard ratio analysis
  - Mis-injection annotations on study samples identified via Internal Standard area thresholds
  - Optional: absolute concentration values calculated via linear regression for compounds in calibration samples with known spike concentrations
- Tools: mzQuality, R, SummarizedExperiment
- Landmark output files: ratio_corrected_assay.tsv, outlier_annotations.csv, mis_injection_flags.csv, concentrations.csv

### Step `task_003`
- Depends on: `task_002`
- Title: Reproduce the RSDQC-based internal standard recommendation output from the analysed experiment
- Task kind: `reproduction`
- Task: Extract relative standard deviation of QC samples (RSDQC) values for each compound across all internal standard candidates from a batch-corrected experiment object, and identify the internal standard achieving the lowest RSDQC per compound. Produce a recommendation table.
- Inputs:
  - task_002.expected_outputs[0]: SummarizedExperiment object with 'ratio_corrected' assay containing batch-corrected Compound/Internal Standard ratios
  - Batch-corrected SummarizedExperiment object with QC sample assays and internal standard ratio data
- Expected outputs:
  - Recommendation table (tab-delimited or CSV) with columns: compound, recommended_internal_standard, min_RSDQC
  - Full RSDQC matrix (tab-delimited or CSV) with compounds as rows and internal standard candidates as columns, showing RSDQC for each pair
- Tools: R, mzQuality, SummarizedExperiment
- Landmark output files: rsdqc_full_matrix.csv, internal_standard_recommendations.csv
- Primary expected artifact: `internal_standard_recommendations.csv`

### Step `task_004`
- Depends on: `task_002`
- Title: Reproduce the createReports file-system export from the analysed experiment
- Task kind: `reproduction`
- Task: Call createReports on an analysed mzQuality experiment object with parameters makeSummaryReport=TRUE, makeCompoundReport=TRUE, backgroundPercent=40, cautionRSD=15, nonReportableRSD=30, and assays='area', then verify that the expected Plots and Reports directory structure and file types are generated.
- Inputs:
  - task_002.expected_outputs[0]: SummarizedExperiment object with 'ratio_corrected' assay containing batch-corrected Compound/Internal Standard ratios
  - Pre-processed SummarizedExperiment object output from doAnalysis
- Expected outputs:
  - Plots subdirectory containing quality-control visualization files
  - Reports subdirectory containing tab-delimited text files and Excel exports
- Tools: mzQuality, R, SummarizedExperiment
- Landmark output files: Plots/*.png, Reports/*.txt, Reports/*.xlsx

### Step `task_005`
- Depends on: `task_001`
- Title: Extend mzQuality to support a no-internal-standard condition and verify ratio assay defaults to 1
- Task kind: `extension`
- Task: Load a tab-delimited metabolomics data file (example.tsv) using readData, construct a SummarizedExperiment object via buildExperiment without the secondaryAssay column, and verify that the resulting 'ratio' assay entries equal the raw primary assay values (divisor = 1 throughout).
- Inputs:
  - example.tsv — tab-delimited metabolomics data file containing columns: aliquot, compound, area, compound_is, area_is, type, injection_time, batch, and concentration
- Expected outputs:
  - Validation report (CSV or text) confirming that all 'ratio' assay values equal corresponding primary assay values within numerical tolerance (machine epsilon)
- Tools: R, mzQuality, SummarizedExperiment
- Landmark output files: cleaned_data_frame.csv, experiment_object_summary.txt
- Primary expected artifact: `ratio_assay_validation.csv`

## Final expected outputs

- `Recommendation table (tab-delimited or CSV) with columns: compound, recommended_internal_standard, min_RSDQC` (type: file, tolerance: hash)
- `Full RSDQC matrix (tab-delimited or CSV) with compounds as rows and internal standard candidates as columns, showing RSDQC for each pair` (type: file, tolerance: hash)
- `Plots subdirectory containing quality-control visualization files` (type: file, tolerance: hash)
- `Reports subdirectory containing tab-delimited text files and Excel exports` (type: file, tolerance: hash)
- `Validation report (CSV or text) confirming that all 'ratio' assay values equal corresponding primary assay values within numerical tolerance (machine epsilon)` (type: file, tolerance: hash)

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

- **Composition modularity:** flat

- **Abstraction level:** concrete

- **Orchestration planning:** static

- **Data transport:** in_memory

- **Characterisation confidence:** inferred


## Submission

Produce two artifacts in your output directory:

1. The output files at the paths declared under **Final expected outputs**.
2. An `attempt.json` matching the schema below.
3. _(Optional)_ `attempt_metrics.json` with `wall_time_s`, `total_tokens`, `cost_usd` for the EFFICIENCY rubric.

### `attempt.json` schema

```json
{
  "workflow_id": "coll_mzquality_workflow",
  "agent_order": [
    "task_001",
    "task_002",
    "task_003",
    "task_004",
    "task_005"
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
    },
    "task_004": {
      "<output_name>": "<locator>"
    },
    "task_005": {
      "<output_name>": "<locator>"
    }
  },
  "final_outputs": {
    "Recommendation table (tab-delimited or CSV) with columns: compound, recommended_internal_standard, min_RSDQC": "<locator>",
    "Full RSDQC matrix (tab-delimited or CSV) with compounds as rows and internal standard candidates as columns, showing RSDQC for each pair": "<locator>",
    "Plots subdirectory containing quality-control visualization files": "<locator>",
    "Reports subdirectory containing tab-delimited text files and Excel exports": "<locator>",
    "Validation report (CSV or text) confirming that all 'ratio' assay values equal corresponding primary assay values within numerical tolerance (machine epsilon)": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>",
    "task_002": "<tool_name>",
    "task_003": "<tool_name>",
    "task_004": "<tool_name>",
    "task_005": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._
