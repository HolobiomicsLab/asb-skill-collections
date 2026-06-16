# Workflow Challenge: `coll_mobilipid_workflow`


> MobiLipid is a tool that streamlines lipidomics workflows by automating collision cross section (CCS) bias assessment and correction in ion mobility-mass spectrometry analyses through internal standardization using a newly established DTCCSN2 library for U13C labeled lipids.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 4-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

MobiLipid provides a newly established DTCCSN2 library for U13C labeled lipids distributed with the code and implements CCS bias assessment and correction mechanisms within an R Markdown workflow that integrates into IM-MS lipidomics analyses. The tool employs internal standardization with U13C labeled lipids to enable CCS bias calculation and correction without requiring additional external calibration beyond vendor-specific requirements. Analysis of the tool demonstrates that effective CCS bias calculation and correction can be achieved while requiring only a low number of lipids detected per lipid class.

## Research questions

- What is the structure, lipid class coverage, and range of CCS values contained in the DTCCSN2 library for U13C labeled lipids that is distributed with MobiLipid?
- How does MobiLipid calculate CCS bias in IM-MS lipidomics data using internal standardization with U13C labeled lipids?
- How does MobiLipid apply CCS bias correction using the automated R Markdown workflow to transform assessed bias measurements into corrected CCS values?
- What is the minimum number of lipids per lipid class required to achieve effective CCS bias estimation and correction using the MobiLipid workflow?

## Methods overview

Clone or download the MobiLipid repository from GitHub. Locate and open the DTCCSN2 library file and inspect its file format (e.g., CSV, TSV, or R data object). Parse and extract all records, verifying presence of required fields (lipid identifier, class, CCS value, measurement conditions). Enumerate and count lipid classes and verify CCS value distributions are consistent with expected ranges for ion mobility data. Compare observed library composition against specifications stated in project documentation and paper abstract. Validation: confirm file loads without error, all required fields are populated, CCS values are numeric and physically plausible, and lipid class coverage matches documented scope. Load IM-MS experimental data and DTCCSN2 reference library into R environment. Match experimental lipid features to reference library entries by m/z, retention time, and lipid class annotation. Calculate per-lipid CCS bias as measured CCS minus theoretical CCS value from library. Aggregate bias metrics by lipid class and compute summary statistics (mean, SD, range, quartiles). Validation: Report generated with per-class bias means and confidence intervals; bias values within expected instrument calibration tolerance (typically ±2–3%) indicate acceptable CCS quality. Load bias assessment output containing calculated bias factors and correction statistics stratified by lipid class. Apply class-specific CCS bias correction factors to measured CCS values using the MobiLipid correction algorithm. Generate output table with original CCS, corrected CCS, applied bias factor, and lipid identifiers. Validation: corrected CCS values are produced for all lipids with assigned bias factors; output matches expected tabular structure and contains no missing values in corrected CCS column. Load the DTCCSN2 reference library and experimental IM-MS lipidomics data into R. Systematically subsample detected lipids per class across a range of counts (e.g., 1–10 lipids per class). Apply MobiLipid internal standardization with U13C labeled lipids to calculate CCS bias at each subsampling level without external calibration. Compute bias estimation quality metrics (residual error, accuracy, or deviation) for each lipid class and count level. Generate a summary table and visualization showing how CCS bias estimation quality stabilizes with increasing lipid counts per class. Validation: confirm that effective CCS bias correction is achieved with a low number of lipids per class, as indicated by convergence of bias metrics and acceptable residual error (acceptance criterion to be determined by reported thresholds in the paper).

**Domain:** lipidomics

**Techniques:** ion-mobility, quality-control, stable-isotope-labeling, high-resolution-ms

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** MobiLipid aims to streamline lipidomics workflows by offering a fully automated solution for assessing and correcting collision cross section (CCS) bias in ion mobility-mass spectrometry (IM-MS) analyses. _[grounded: mobil_lipid_system]_
- **(finding)** MobiLipid employs a newly established DT CCS N2 library for U13C labeled lipids. _[grounded: mobil_lipid_system]_
- **(finding)** MobiLipid eliminates the need to measure additional external calibration besides vendor specific calibration requirements by internal standardization. _[grounded: mobil_lipid_system]_
- **(finding)** MobiLipid enhances CCS quality control by providing an R Markdown that integrates into IM-MS lipidomics workflows. _[grounded: mobil_lipid_system]_
- **(finding)** CCS bias calculation and correction can be implemented effectively with a low number of lipids detected per lipid class.

## Steps

### Step `task_001`
- Title: Reproduce the DTCCSN2 library for U13C labeled lipids as provided with MobiLipid
- Task kind: `reproduction`
- Task: Load the DTCCSN2 library file from the MobiLipid GitHub repository and validate its structure, lipid class coverage, and CCS values against the specifications described in the project documentation and abstract.
- Inputs:
  - MobiLipid GitHub repository (FelinaHildebrand/MobiLipid)
- Expected outputs:
  - Validation report documenting DTCCSN2 library structure, lipid class coverage, CCS value statistics, and conformance to specifications
- Tools: R
- Landmark output files: library_structure.json, lipid_class_summary.csv, ccs_statistics.txt
- Primary expected artifact: `dtccsn2_library_validation_report.txt`

### Step `task_002`
- Depends on: `task_001`
- Title: Reconstruct the CCS bias assessment component of the MobiLipid R Markdown workflow
- Task kind: `component_reconstruction`
- Task: Execute the CCS bias calculation step from the MobiLipid R Markdown workflow on a representative IM-MS lipidomics dataset using the DTCCSN2 library to produce a bias assessment report quantifying systematic deviations in collision cross section measurements.
- Inputs:
  - IM-MS lipidomics dataset (mzML, mzXML, or tabular feature table with m/z, retention time, and measured CCS values)
  - DTCCSN2 library for U13C labeled lipids from MobiLipid repository
  - R Markdown file from MobiLipid repository implementing CCS bias calculation
- Expected outputs:
  - CCS bias assessment report containing per-lipid bias values, class-level bias statistics, and visualizations
- Tools: R
- Landmark output files: matched_lipid_features.csv, per_lipid_bias_values.csv, class_level_bias_statistics.csv
- Primary expected artifact: `ccs_bias_assessment_report.html`

### Step `task_003`
- Depends on: `task_002`
- Title: Reconstruct the CCS bias correction component of the MobiLipid R Markdown workflow
- Task kind: `component_reconstruction`
- Task: Execute the automated CCS bias correction step in MobiLipid using bias assessment output to produce corrected collision cross section values as a tabular file.
- Inputs:
  - Bias assessment output (bias factors, statistics, and class-level corrections per lipid class)
  - MobiLipid R Markdown script with correction implementation
- Expected outputs:
  - Corrected CCS values in tabular format (CSV or data frame) with original and corrected CCS per lipid, including bias correction metadata
- Tools: R
- Landmark output files: bias_factors_per_class.csv, corrected_ccs_values.csv
- Primary expected artifact: `corrected_ccs_values.csv`

### Step `task_004`
- Depends on: `task_001`
- Title: Analyze the minimum lipids-per-class requirement for effective CCS bias calculation in MobiLipid
- Task kind: `analysis`
- Task: Computationally evaluate the relationship between the number of detected lipids per lipid class and CCS bias estimation quality using MobiLipid and the bundled DTCCSN2 library, reproducing the reported finding that effective CCS bias correction requires only a low number of lipids per class.
- Inputs:
  - MobiLipid codebase and DTCCSN2 library for U13C labeled lipids
  - Ion mobility-mass spectrometry lipidomics experimental data
- Expected outputs:
  - Summary table of CCS bias estimation quality metrics (e.g., residual error, accuracy) as a function of lipid count per lipid class
  - Visualization (curve or heatmap) showing the relationship between number of detected lipids per class and CCS bias estimation quality
- Tools: R
- Landmark output files: lipid_subsampling_levels.txt, bias_estimates_per_class.csv, residual_error_by_count.csv, bias_quality_curve.png
- Primary expected artifact: `ccs_bias_quality_metrics.csv`

## Final expected outputs

- `Corrected CCS values in tabular format (CSV or data frame) with original and corrected CCS per lipid, including bias correction metadata` (type: file, tolerance: hash)
- `Summary table of CCS bias estimation quality metrics (e.g., residual error, accuracy) as a function of lipid count per lipid class` (type: file, tolerance: hash)
- `Visualization (curve or heatmap) showing the relationship between number of detected lipids per class and CCS bias estimation quality` (type: file, tolerance: hash)

## How your attempt will be scored

ASB defines seven rubrics in `workflow_rubric.py` (STEP_ORDERING, INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT, TOOL_SELECTION, EFFICIENCY, CLAIM_VALIDATION, ADVERSARIAL_TRAP_AVOIDANCE). Which of them bind for *this* challenge depends on the tier and openness below.

### Tier evaluation profile

**Evaluator:** automated — filesystem presence + type-port resolution; END_TO_END_OUTPUT with declared per-output tolerance.
**Binding rubrics:** STEP_ORDERING, END_TO_END_OUTPUT (typed/tolerance), TOOL_SELECTION, CLAIM_VALIDATION.

### Openness stance

**Openness: closed — reproduction-first.** The deterministic rubrics above bind. A different method is acceptable ONLY if it appears under *Sanctioned method substitutions*; outputs are compared with the declared tolerance. Different is wrong here only when it departs from the sanctioned set or breaks an invariant.

## Workflow characterisation

_Suter et al. 2025 (DOI 10.1016/j.future.2025.107974)._

- **Coupling:** loose

- **Composition modularity:** flat

- **Abstraction level:** concrete

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
  "workflow_id": "coll_mobilipid_workflow",
  "agent_order": [
    "task_001",
    "task_002",
    "task_003",
    "task_004"
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
    }
  },
  "final_outputs": {
    "Corrected CCS values in tabular format (CSV or data frame) with original and corrected CCS per lipid, including bias correction metadata": "<locator>",
    "Summary table of CCS bias estimation quality metrics (e.g., residual error, accuracy) as a function of lipid count per lipid class": "<locator>",
    "Visualization (curve or heatmap) showing the relationship between number of detected lipids per class and CCS bias estimation quality": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>",
    "task_002": "<tool_name>",
    "task_003": "<tool_name>",
    "task_004": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._
