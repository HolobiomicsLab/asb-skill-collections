# Workflow Challenge: `coll_tardis_workflow`


> TARDIS is an R package for targeted peak integration in LC-MS data that automatically calculates area under the peak, max intensity, and quality metrics for chemical compounds. The workflow demonstrates screening mode to inspect extracted ion chromatograms, full peak detection to generate quantitative output tables, and integration with MsExperiment objects.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

This workflow demonstrates the complete targeted analysis pipeline in TARDIS for LC-MS data. Starting with a target compound list created from an input file, the workflow first runs tardisPeaks() in screening mode to generate diagnostic extracted ion chromatogram (EIC) plots for ten selected compounds across quality control (QC) runs, allowing visual inspection of peak detection and integration results. After adjusting retention time parameters based on the screening results, the workflow then executes tardisPeaks() with full peak detection (screening_mode=FALSE) to produce quantitative outputs: a data.frame containing per-target area-under-curve (AUC) values across all runs, a QC feature table with average metrics per target, and multiple CSV files reporting max intensity, signal-to-noise ratio, peak correlation, and points over peak for all targets. The workflow additionally demonstrates that when processing data containing multiple overlapping m/z scan windows without mass_range separation, peaks display a sawtooth profile due to empty spectrum filtering, and shows that tardisPeaks() accepts both file paths and MsExperiment objects as input for screening mode operations.

## Research questions

- How does the createTargetList() function filter and restructure input compound data based on polarity specification to produce a correctly formatted target data.frame?
- Does tardisPeaks() in screening mode successfully generate and save extracted ion chromatogram (EIC) plots for all 10 target compounds (5 internal standards + 5 endogenous metabolites) to the diagnostic QC output folder?
- What quantitative metrics and output tables does tardisPeaks() generate when run in peak detection mode (screening_mode=FALSE) on LC-MS data?
- Does the sawtooth artefact appear in extracted ion chromatogram (EIC) output when tardisPeaks() is run on LC-MS data with multiple overlapping m/z scan windows without proper mass_range separation?
- Do MsExperiment objects with annotated sampleData$type produce identical screening-mode EIC diagnostic outputs compared to file-path-based invocation of tardisPeaks()?

## Methods overview

Load targets file (xlsx or csv) into R environment Validate required columns: compound ID, name, m/z, RT (minutes), polarity Filter rows by polarity mode (positive or negative ionization) Select and standardize column order for downstream tardisPeaks integration Validation: Output data.frame contains all original targets (or filtered subset) with correct column names and data types; no missing values in required fields References: source article (DOI: 10.1021/acs.analchem.5c00567) Load 14 centroided .mzML LC-MS runs and target compound metadata (m/z, retention time, polarity) into TARDIS environment. Execute tardisPeaks() with screening_mode=TRUE to screen target visibility within m/z and retention time windows, applying automatic polarity filtering. Generate and save 10 extracted ion chromatogram (EIC) PNG plots with peak annotations to output/screening/Diagnostic_QCs_Batch_1/ folder. Validation: verify that exactly 10 PNG files are generated (one per target), each file exists in the specified output directory, and files are readable PNG images with visible chromatographic traces and peak annotations. References: source article (DOI: 10.1021/acs.analchem.5c00567) Load vignette LC-MS data in centroided .mzML format using Spectra package. Apply xcms retention-time correction algorithm to align targets 1577 and 1583 across runs. Execute tardisPeaks() with screening_mode=FALSE to perform targeted peak detection with automatic polarity filtering. Calculate area-under-curve (AUC), max intensity, signal-to-noise ratio (SNR), peak correlation (peak_cor), and points-over-peak for each target in each run. Aggregate per-run metrics into QC feature table tibble (average metrics per target across QC runs) and export individual metric tables (AUC, Max Intensity, SNR, peak_cor, pop) as CSV files. Save extracted ion chromatograms (EICs) to output directory for manual quality inspection. Validation: Verify that QC feature table tibble and all per-metric CSV files (AUC, Max Intensity, SNR, peak_cor, pop) are successfully written to the output directory with correct structure and non-empty content matching expected metric columns. References: source article (DOI: 10.1021/acs.analchem.5c00567) Load centroided mzML vignette files and parse as Spectra objects. Define target compound list with m/z, RT, and polarity annotations. Execute tardisPeaks() with multi-window mass_range but without scan-window separation to trigger sawtooth artefacts. Re-execute tardisPeaks() with correct mass_range argument routing to enable scan-window segregation. Generate and compare EIC plots from both runs to visualize artefact elimination. Validation: Confirm sawtooth oscillations present in first EIC set and absent in second set; verify AUC and peak-shape metrics improve with correct routing. References: source article (DOI: 10.1021/acs.analchem.5c00567) Load vignette mzML files into a Spectra object via the Spectra package. Prepare sample metadata with type labels and combine with Spectra to construct an MsExperiment object. Define a target list with compound identifiers, chemical names, m/z values, retention times, and ion polarity. Execute tardisPeaks() in screening mode (screening_mode=TRUE) using the MsExperiment object as lcmsData to check target visibility within expected m/z and RT windows. Extract and compare diagnostic EIC PNG files from MsExperiment-based invocation against reference EICs from file-path-based invocation to confirm functional equivalence. Validation: EIC PNG files produced by both invocation methods are identical in file content and visual representation, confirming correct MsExperiment integration. References: source article (DOI: 10.1021/acs.analchem.5c00567)

**Domain:** multi-omics

**Techniques:** lc-ms, feature-detection, chromatogram-alignment, quality-control, spectral-library-matching

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** TARDIS automatically calculates area under the peak, max intensity and various quality metrics for targeted chemical compounds in LC-MS data. _[grounded: TARDIS_system]_
- **(finding)** TARDIS uses an established retention time correction algorithm from the xcms package. _[grounded: TARDIS_system]_
- **(finding)** TARDIS loads MS data as Spectra objects for easy integration with other tools of the Rformassspectrometry initiative. _[grounded: TARDIS_system]_
- **(finding)** Input files for TARDIS need to be converted to the .mzML format. _[grounded: TARDIS_system]_
- **(finding)** Input files for TARDIS need to be centroided. _[grounded: TARDIS_system]_
- **(finding)** Polarity filtering is done within TARDIS, so no polarity subsetting has to be performed when converting the files. _[grounded: TARDIS_system]_
- **(finding)** A compound ID must be present for each compound in the target data.frame.
- **(finding)** A compound Name must be present for each compound in the target data.frame.
- **(finding)** Theoretical or measured m/z must be present for each compound in the target data.frame.
- **(finding)** Expected RT in minutes must be present for each compound in the target data.frame.
- **(finding)** A column indicating the polarity of the formed ion must be present for each compound in the target data.frame.
- **(finding)** An input file can be either .xlsx or .csv format for conversion to a target data.frame using createTargetList(). _[grounded: comp_createTargetList]_
- **(finding)** The vignette example has a total of 14 runs: two QC injections, followed by four sample injections, two QC injections, four sample injections and two QC injections.
- **(finding)** An MsExperiment object can be used as input for TARDIS instead of file paths. _[grounded: TARDIS_system]_
- **(finding)** The sampleData column in an MsExperiment object for TARDIS must be named 'type'. _[grounded: TARDIS_system]_
- **(finding)** If data contains multiple overlapping m/z scan windows, it is necessary to analyze these separately through the mass_range argument. _[grounded: cond_multiple_scan_windows]_
- **(finding)** If data contains multiple overlapping m/z scan windows and is not analyzed separately, peaks will have a sawtooth profile due to filtering of empty spectra within TARDIS. _[grounded: TARDIS_system]_
- **(finding)** Screening mode can be run in TARDIS using the argument screening_mode = TRUE in the tardisPeaks function. _[grounded: TARDIS_system]_
- **(finding)** EICs (Extracted Ion Chromatograms) from screening mode are saved in the output folder and can be inspected. _[grounded: comp_screening_mode]_
- **(finding)** Peak detection can be performed in all runs by setting screening_mode = FALSE in the tardisPeaks function. _[grounded: comp_tardisPeaks]_
- **(finding)** The results object from tardisPeaks is a list that contains a data.frame with the AUC of each target in each run. _[grounded: comp_tardisPeaks]_
- **(finding)** The results object from tardisPeaks contains a tibble with a feature table with the average metrics for each target in the QC runs. _[grounded: comp_tardisPeaks]_
- **(finding)** Results from tardisPeaks include tables with metrics: Max. Int., SNR, peak_cor and points over the peak. _[grounded: comp_tardisPeaks]_
- **(finding)** Results tables from tardisPeaks are saved into the output folder. _[grounded: comp_tardisPeaks]_
- **(finding)** The screening mode in the vignette example was limited to 10 targets: 5 internal standards and 5 endogenous metabolites. _[grounded: comp_screening_mode]_
- **(finding)** In the vignette example, target 1577 eluted towards the edge of the retention time window.
- **(finding)** In the vignette example, target 1583 eluted towards the edge of the retention time window.
- **(finding)** In the vignette example, the expected retention time for target 1577 was adjusted to 8.82 minutes.
- **(finding)** In the vignette example, the expected retention time for target 1583 was adjusted to 4 minutes.

## Sanctioned method substitutions
Using any of these instead of the source method is **not penalized**:
- MsExperiment object can be used as input instead of file paths

## Invariants (must not change)
Changing any of these **is** a failure regardless of openness:
- Data with multiple overlapping m/z scan windows must be analyzed separately through mass_range argument

## Steps

### Step `task_001`
- Title: Reconstruct the createTargetList filtering and formatting step for LC-MS target input files
- Task kind: `component_reconstruction`
- Task: Load a targets.xlsx or .csv file, apply polarity filtering, select required columns (compound ID, name, m/z, RT, polarity), and produce a correctly structured target data.frame for downstream peak integration by tardisPeaks.
- Inputs:
  - Targets file in .xlsx or .csv format containing compound ID, name, m/z, RT, and polarity columns
- Expected outputs:
  - Formatted target data.frame with polarity-filtered rows and standardized column structure
- Tools: xcms, R
- Landmark output files: targets_loaded.csv, targets_filtered.csv
- Primary expected artifact: `target_dataframe.rds`

### Step `task_002`
- Depends on: `task_000`
- Title: Reproduce the screening-mode Diagnostic EIC Plots for 10 selected targets across one batch
- Task kind: `reproduction`
- Task: Execute tardisPeaks() with screening_mode=TRUE on a 14-run LC-MS vignette dataset (10 targets: 5 internal standards + 5 endogenous compounds) to perform target visibility screening and generate 10 diagnostic extracted ion chromatogram (EIC) PNG plots saved to output/screening/Diagnostic_QCs_Batch_1/.
- Inputs:
  - 14 centroided .mzML LC-MS data files (vignette dataset)
  - Target list data.frame with compound ID, name, m/z, retention time, and polarity
- Expected outputs:
  - 10 extracted ion chromatogram (EIC) PNG plots (one per target compound) with peak annotations
- Tools: TARDIS, Spectra, xcms, R, MsExperiment, knitr
- Landmark output files: screening_results.csv, target_visibility_summary.txt, Diagnostic_QCs_Batch_1/*.png

### Step `task_003`
- Depends on: `task_001`
- Title: Reproduce the QC Feature Table and Metric CSV Output Files from full peak detection mode
- Task kind: `reproduction`
- Task: Run tardisPeaks() with screening_mode=FALSE on the vignette LC-MS dataset after retention-time adjustment for targets 1577 and 1583, and reproduce the output QC feature table tibble and per-metric CSV files (AUC, Max Intensity, SNR, peak_cor, pop) to the designated output directory.
- Inputs:
  - task_001.expected_outputs[0]: Formatted target data.frame with polarity-filtered rows and standardized column structure
  - Vignette LC-MS dataset in .mzML centroided format with compound target list specifying compound ID, name, m/z, expected RT (minutes), and polarity
- Expected outputs:
  - QC feature table tibble containing average metrics for each target in QC runs
  - CSV file with AUC values for each target in each run
  - CSV files with Max Intensity, SNR, peak_cor, and points over peak metrics
  - Extracted Ion Chromatograms (EICs) saved in the output folder
- Tools: Spectra, xcms, R, knitr, kableExtra
- Landmark output files: targets_1577_1583_rt_adjusted.RData, qc_feature_table.csv, auc_metrics.csv, max_intensity_metrics.csv, snr_metrics.csv, peak_cor_metrics.csv
- Primary expected artifact: `qc_feature_table.csv`

### Step `task_004`
- Depends on: `task_001`
- Title: Analyze the effect of multiple overlapping m/z scan windows on peak profile quality using the sawtooth diagnostic
- Task kind: `analysis`
- Task: Run tardisPeaks() on vignette mzML files with a multi-window mass_range configuration to demonstrate the sawtooth artefact that appears when scan-window separation is omitted, then re-run with correct mass_range routing to produce clean peak profiles and EIC plots.
- Inputs:
  - Centroided mzML vignette files
  - Target list data.frame with compound ID, name, m/z, RT, and polarity
- Expected outputs:
  - EIC plots with sawtooth artefact (incorrect mass_range routing)
  - EIC plots with clean peak profiles (correct mass_range routing)
  - Data.frame with AUC metrics for each target across both runs
- Tools: xcms, Spectra, R, knitr
- Landmark output files: eic_artefact_*.png, eic_clean_*.png, results_artefact.RDS, results_clean.RDS
- Primary expected artifact: `eic_comparison_report.html`

### Step `task_005`
- Depends on: `task_004`
- Title: Extend TARDIS to accept an MsExperiment object as input and reproduce the screening-mode EIC plots
- Task kind: `extension`
- Task: Construct an MsExperiment object from vignette mzML files with sample type labels, execute tardisPeaks() in screening mode using the MsExperiment object as lcmsData input, and verify that the resulting diagnostic EIC PNG files match those from file-path-based invocation.
- Inputs:
  - mzML files (centroided) corresponding to LC-MS runs for targeted analysis
  - Target list data frame with columns: compound ID, compound name, m/z, expected retention time (minutes), and polarity
  - Sample metadata including type labels (e.g., QC, sample) for each mzML file
- Expected outputs:
  - EIC PNG diagnostic figures saved to output folder for visual inspection of target peak detection in screening mode
  - Verification report confirming EIC PNG files from MsExperiment-based invocation match file-path-based reference invocation
- Tools: xcms, Spectra, MsExperiment, TARDIS, R, knitr
- Landmark output files: spectra_object.rds, msexperiment_object.rds, screening_mode_eics/*.png, reference_eics/*.png
- Primary expected artifact: `eic_equivalence_verification_report.txt`

## Final expected outputs

- `10 extracted ion chromatogram (EIC) PNG plots (one per target compound) with peak annotations` (type: file, tolerance: hash)
- `QC feature table tibble containing average metrics for each target in QC runs` (type: file, tolerance: hash)
- `CSV file with AUC values for each target in each run` (type: file, tolerance: hash)
- `CSV files with Max Intensity, SNR, peak_cor, and points over peak metrics` (type: file, tolerance: hash)
- `Extracted Ion Chromatograms (EICs) saved in the output folder` (type: file, tolerance: hash)
- `EIC PNG diagnostic figures saved to output folder for visual inspection of target peak detection in screening mode` (type: file, tolerance: hash)
- `Verification report confirming EIC PNG files from MsExperiment-based invocation match file-path-based reference invocation` (type: file, tolerance: hash)

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
  "workflow_id": "coll_tardis_workflow",
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
    "10 extracted ion chromatogram (EIC) PNG plots (one per target compound) with peak annotations": "<locator>",
    "QC feature table tibble containing average metrics for each target in QC runs": "<locator>",
    "CSV file with AUC values for each target in each run": "<locator>",
    "CSV files with Max Intensity, SNR, peak_cor, and points over peak metrics": "<locator>",
    "Extracted Ion Chromatograms (EICs) saved in the output folder": "<locator>",
    "EIC PNG diagnostic figures saved to output folder for visual inspection of target peak detection in screening mode": "<locator>",
    "Verification report confirming EIC PNG files from MsExperiment-based invocation match file-path-based reference invocation": "<locator>"
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
