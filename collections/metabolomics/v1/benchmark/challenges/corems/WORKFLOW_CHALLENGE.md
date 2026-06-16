# Workflow Challenge: `coll_corems_workflow`


> CoreMS is a comprehensive Python framework for mass spectrometry software development and data analysis that enables reproducible processing of FT-ICR MS and GC-MS data through modular pipelines including transient processing, noise thresholding, mass calibration, and molecular formula assignment.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

CoreMS demonstrates reproducible workflows for high-resolution mass spectrometry data processing, including complete FT-ICR MS molecular formula assignment via transient Fourier transformation, apodization, noise thresholding, and mass calibration against reference standards (SRFA.ref), as well as GC-MS compound identification through retention index calibration and spectral library matching. The framework provides configurable noise thresholding mechanisms spanning relative-abundance, signal-to-noise ratio, and log-normal distribution modes for peak detection. Mass calibration incorporates an iterative fallback strategy that progressively widens mass-error tolerances from ±1.0 to ±10 ppm when insufficient calibration points are found at stricter thresholds. Molecular formula searches operate in single-assignment (first-hit) and exhaustive modes, with results exportable to CSV and HDF5 formats; parameterization via MSParameters enables reproducible configuration of apodization methods, zero-fill counts, and search constraints across CHO, N, O, S, and halogen chemistries.

## Research questions

- Does the CoreMS FT-ICR data processing pipeline (Hanning apodization, log-based noise thresholding, MzDomainCalibration, and SearchMolecularFormulas) successfully assign molecular formulas to ESI_NEG_SRFA.d data with quantified mass error metrics?
- How does the calibration procedure handle cases where the initial narrow PPM window fails to find sufficient reference m/z matches?
- Does the CoreMS GC-MS processing pipeline successfully identify compounds from low-resolution mass spectrometry data using spectral library matching?
- How do the three noise thresholding methods implemented in CoreMS (log, signal_noise, and relative_abundance) differ in their selection criteria and how many peaks each retains from a given mass spectrum?
- How does the first_hit parameter in SearchMolecularFormulas affect the number of molecular formula assignments and their score distributions?

## Methods overview

Load FT-ICR raw data (ESI_NEG_SRFA.d) and calibration reference (SRFA.ref) into CoreMS factory. Apply Hanning window apodization with single zero-fill to time-domain transient. Remove noise via intensity thresholding on frequency-domain spectrum. Calibrate m/z axis using MzDomainCalibration against reference compounds in SRFA.ref. Search and assign molecular formulas using CHO elemental constraints; compute mass error and formula score for each assignment. Validation: Output CSV contains formula assignments with mass error values; all assigned formulas obey CHO elemental constraints and exhibit mass error consistent with FT-ICR instrumental resolution. Load mass spectrum from ESI_NEG_SRFA.d and reference m/z values from SRFA.ref using CoreMS data encapsulation. Perform initial reference m/z peak matching using a baseline PPM window (e.g., 5 ppm). Evaluate match count; if fewer than 5 points matched, expand PPM tolerance and rematch. Fit calibration polynomial (e.g., second-order) to matched points using least-squares regression. Compute residuals and export calibration coefficients with metadata to structured output record. Validation: Confirm that final calibration point count meets or exceeds 5; verify residual magnitude indicates acceptable fit quality for subsequent mass analysis. Load raw GC-MS chromatographic and spectral data from NetCDF format using ReadAndiNetCDF module. Calibrate retention times against alkane standards using GC_RI_Calibration to compute normalized retention indices. Extract low-resolution mass spectra and match each against PNNLMetV20191015.MSL library using LowResMassSpectralMatch with cosine similarity and retention-index scoring. Aggregate compound identifications with match scores and rank results by confidence. Validation: CSV output contains at least one identified compound per peak with spectral match score ≥0.7 and retention-index deviation ≤20 RI units, matching library entries in PNNLMetV20191015.MSL. Load mass spectrum from ESI_NEG_SRFA.d using CoreMS factory and MSParameters. Implement conditional dispatch that selects one of three mutually exclusive noise-threshold methods. Apply selected threshold method and count retained peaks per ionization mode. Serialize method name and peak counts as a structured CSV or JSON record. Validation: record contains method identifier and non-null peak count fields for each mode. Load calibrated mass spectrum from ESI_NEG_SRFA.d and reference file SRFA.ref into CoreMS framework. Execute SearchMolecularFormulas with parameter first_hit=True and collect all assigned formulas and their scores. Execute SearchMolecularFormulas with parameter first_hit=False and collect all assigned formulas and their scores. Calculate summary statistics (count, mean, median, standard deviation, minimum, maximum) for assignment scores in each mode. Tabulate and compare results side-by-side in a CSV summary table. Validation: Output file contains both modes' assignment counts and score statistics with no missing numeric fields.

**Domain:** metabolomics

**Techniques:** feature-detection, metabolite-identification, database-annotation, quality-control, spectral-library-matching

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** CoreMS is a comprehensive mass spectrometry framework for software development and data analysis of small molecules analysis. _[grounded: SYS-001]_
- **(finding)** Data handling and software development for modern mass spectrometry is an interdisciplinary endeavor requiring skills in computational science and a deep understanding of MS.
- **(finding)** Contributors must create an issue proposing a fix or expanded functionality before contributing.
- **(finding)** Contributors can fork the CoreMS repository or make a branch if part of the development team. _[grounded: SYS-001]_
- **(finding)** CoreMS follows the NumPy documentation style guide. _[grounded: SYS-001]_
- **(finding)** Documentation in CoreMS is rendered using the pdoc package. _[grounded: SYS-001]_
- **(finding)** CoreMS uses semantic versioning with major, minor, and patch version numbers. _[grounded: SYS-001]_
- **(finding)** Major version is incremented when making incompatible API changes.
- **(finding)** Minor version is incremented when adding new features in a backwards-compatible manner.
- **(finding)** Patch version is incremented for backwards-compatible bug fixes.
- **(finding)** Unit tests must be added or updated to cover changes made in merge requests.
- **(finding)** Documentation must be updated and rerendered to reflect any new features or changes in CoreMS. _[grounded: SYS-001]_
- **(finding)** The CI/CD pipeline must pass before merging into the master branch.
- **(finding)** Relevant issues or pull requests should be referenced in merge requests.
- **(finding)** Contributing to CoreMS means agreeing that contributions will be licensed as described in the LICENSE file. _[grounded: SYS-001]_
- **(finding)** CoreMS has sibling projects including EnviroMS and MetaMS. _[grounded: SYS-001]_

## Steps

### Step `task_001`
- Title: Reproduce FT-ICR transient processing and molecular formula assignment for ESI_NEG_SRFA
- Task kind: `reproduction`
- Task: Execute the complete FT-ICR data processing pipeline on ESI_NEG_SRFA.d raw data: apply Hanning apodization with one zero-fill, perform noise thresholding, calibrate mass domain against SRFA.ref reference, and assign molecular formulas with CHO constraints. Output a CSV table of assigned formulas with mass error and score fields.
- Inputs:
  - ESI_NEG_SRFA.d raw FT-ICR mass spectrometry data file
  - SRFA.ref calibration reference file for mass calibration
- Expected outputs:
  - CSV table of assigned molecular formulas with mass error and score fields
- Tools: Docker, CoreMS, pandas, numpy
- Landmark output files: processed_spectrum_mz_intensity.csv, calibration_residuals.csv, assigned_molecular_formulas.csv
- Primary expected artifact: `assigned_molecular_formulas.csv`

### Step `task_002`
- Depends on: `task_001`
- Title: Reconstruct the MzDomainCalibration fallback PPM-widening step for sparse reference lists
- Task kind: `component_reconstruction`
- Task: Implement a conditional fallback mechanism for mass spectrum calibration that expands the PPM tolerance window when fewer than 5 reference m/z values are matched against SRFA.ref. Output a structured record reporting the number of calibration points found and the final calibration coefficients with residuals.
- Inputs:
  - Mass spectrum data file ESI_NEG_SRFA.d
  - Reference m/z calibration file SRFA.ref
- Expected outputs:
  - Structured record containing calibration point count, final calibration coefficients, and residuals
- Tools: Docker, CoreMS, pandas, numpy
- Landmark output files: matched_peaks_initial.csv, matched_peaks_expanded.csv
- Primary expected artifact: `calibration_record.json`

### Step `task_003`
- Title: Reproduce GC-MS compound identification pipeline using PNNLMetV20191015 reference library
- Task kind: `reproduction`
- Task: Execute the GC-MS processing pipeline against the PNNLMetV20191015.MSL spectral library to identify compounds from raw GC-MS data. Output a CSV table containing identified compounds with retention-index scores and spectral match scores.
- Inputs:
  - Raw GC-MS data file in NetCDF (Agilent .d) or equivalent format
  - PNNLMetV20191015.MSL spectral library (NIST-format MS library with retention indices)
- Expected outputs:
  - CSV table of identified compounds with columns: compound name, CAS number, retention index, spectral match score, match rank, and peak integration metrics
- Tools: Docker, CoreMS, pandas, numpy
- Landmark output files: raw_spectra_extracted.csv, retention_indices_calibrated.csv, spectral_matches_ranked.csv
- Primary expected artifact: `identified_compounds.csv`

### Step `task_004`
- Depends on: `task_001`
- Title: Reconstruct the noise threshold method dispatch for relative-abundance, signal-noise, and log modes
- Task kind: `component_reconstruction`
- Task: Implement a dispatch mechanism that applies three mutually exclusive noise-threshold conditions to a loaded mass spectrum and output a structured record (JSON or CSV row) documenting the selected method name and the number of peaks retained for each ionization mode.
- Inputs:
  - Mass spectrum data file (ESI_NEG_SRFA.d)
- Expected outputs:
  - Structured record (JSON or CSV row) containing selected noise-threshold method name and peak count per ionization mode
- Tools: Docker, CoreMS, pandas, numpy
- Landmark output files: spectrum_loaded.json, peaks_before_threshold.csv, peaks_after_threshold.csv
- Primary expected artifact: `threshold_dispatch_result.csv`

### Step `task_005`
- Depends on: `task_001`
- Title: Analyze the effect of first-hit versus all-hits search on molecular formula assignment counts for SRFA
- Task kind: `analysis`
- Task: Apply SearchMolecularFormulas to a calibrated mass spectrum from DS-001 under two configuration modes (first_hit=True and first_hit=False) and compare the number and score distribution of assigned formulas. Output a summary table with assignment counts and score statistics for each mode.
- Inputs:
  - Calibrated mass spectrum dataset ESI_NEG_SRFA.d
  - Reference file SRFA.ref for spectrum calibration
- Expected outputs:
  - Summary table with assignment counts and score statistics for first_hit=True and first_hit=False modes
- Tools: Docker, CoreMS, pandas, numpy, matplotlib
- Landmark output files: spectrum_loaded.txt, assignments_first_hit_true.csv, assignments_first_hit_false.csv
- Primary expected artifact: `formula_assignment_comparison.csv`

## Final expected outputs

- `Structured record containing calibration point count, final calibration coefficients, and residuals` (type: file, tolerance: hash)
- `CSV table of identified compounds with columns: compound name, CAS number, retention index, spectral match score, match rank, and peak integration metrics` (type: file, tolerance: hash)
- `Structured record (JSON or CSV row) containing selected noise-threshold method name and peak count per ionization mode` (type: file, tolerance: hash)
- `Summary table with assignment counts and score statistics for first_hit=True and first_hit=False modes` (type: file, tolerance: hash)

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

- **Composition modularity:** hierarchical

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
  "workflow_id": "coll_corems_workflow",
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
    "Structured record containing calibration point count, final calibration coefficients, and residuals": "<locator>",
    "CSV table of identified compounds with columns: compound name, CAS number, retention index, spectral match score, match rank, and peak integration metrics": "<locator>",
    "Structured record (JSON or CSV row) containing selected noise-threshold method name and peak count per ionization mode": "<locator>",
    "Summary table with assignment counts and score statistics for first_hit=True and first_hit=False modes": "<locator>"
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
