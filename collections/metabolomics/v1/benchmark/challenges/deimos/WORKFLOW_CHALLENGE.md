# Workflow Challenge: `coll_deimos_workflow`


> DEIMoS is a Python API and command-line tool for high-dimensional mass spectrometry data analysis that performs feature detection, alignment, CCS calibration, isotope detection, and MS/MS deconvolution by simultaneously utilizing all data dimensions to improve detection sensitivity and reduce convolution artifacts.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 4-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

DEIMoS (Data Extraction for Integrated Multidimensional Spectrometry) operates on N-dimensional mass spectrometry data largely agnostic to acquisition instrumentation. The tool implements feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution, producing detected features aligned across study samples and characterized by mass, CCS, tandem mass spectra, and isotopic signature. Notably, algorithm implementations simultaneously utilize all dimensions of the input data to offer greater separation between features (improving detection sensitivity), increase alignment and feature matching confidence among datasets, and mitigate convolution artifacts in tandem mass spectra. The CCS calibration routine using the tunemix function achieves R-squared = 0.9999784552958121 for positive ion mode and R-squared = 0.9999784552958134 for negative ion mode. Reference-based alignment constructs a per-dimension model by putatively matching detected features against an in-study reference sample, minimizing residuals, and applying the fit transform. Isotope detection enumerates C13 isotopologue offsets by specifying an m/z delta of 1.003355 Da with up to 5 isotopic substitutions for singly charged species, constrained by m/z, drift time, and retention time tolerances, with final downselection using a maximum m/z error of 50 ppm.

## Research questions

- Does the DEIMoS tunemix calibration function produce collision cross section (CCS) calibration coefficients that achieve R-squared values ≥0.99997 when applied to positive and negative ion mode tune mix data?
- How does reference-based alignment in DEIMoS adjust feature coordinates across samples to account for instrument variation?
- How does DEIMoS enumerate isotopologue offsets for singly charged species, and what parameters define the m/z tolerance, drift time tolerance, retention time tolerance, and charge constraints used in this detection?
- Does the DEIMoS Snakemake workflow successfully execute end-to-end on the publicly deposited MassIVE user guide example dataset, completing all workflow rules and producing final HDF5 output artifacts?

## Methods overview

Load tunemix reference data (positive and negative ion modes) into DEIMoS using HDF5 file interface with ms1 key. Initialize CCS calibration objects specifying known tunemix CCS values and instrumental m/z–drift-time coordinates. Fit polynomial regression models to establish m/z–drift-time–CCS mapping for each ion mode independently. Extract R-squared coefficients from fitted models and verify they exceed 0.99997 threshold. Validation: Confirm that both positive and negative ion mode calibrations achieve R-squared ≥0.99997 as reported in the user guide. References: MSV000091746 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000091746) Load two feature tables in HDF5 format specifying multi-dimensional columns (mass, drift time, retention time, intensity). Apply reference-based alignment to match features across datasets using simultaneous N-dimensional similarity comparison. Export aligned features to HDF5 format with matched feature identities preserved. Validation: verify aligned output table contains features matched across both input datasets with dimensional consistency and no data loss. References: MSV000091746 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000091746) Load peak-picked HDF5 feature table with m/z, drift_time, retention_time, and intensity columns. Invoke deimos.isotopes module to enumerate C13 isotopologue mass offsets for charge +1 species by computing pairwise m/z differences and spatial concordance. Filter detected isotopic signatures to retain clusters with minimum 3 members. Annotate feature table rows with isotopologue identity labels (monoisotopic flag, member index, C13 count) and export to HDF5. Validation: Confirm output HDF5 file contains isotope annotation columns; verify all detected isotopic signatures satisfy ≥3-member threshold and mass offset consistency with theoretical C13 shift (1.003355 Da per substitution). References: MSV000091746 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000091746) Clone DEIMoS repository and create conda virtual environment with required dependencies. Download MassIVE user-guide dataset (MSV000091746) and place mzML.gz files in input/ directory. Prepare or modify YAML configuration file with workflow-specific parameters (default_config.yaml provided). Invoke DEIMoS CLI with config.yaml to execute Snakemake workflow, specifying core count and execution mode. Snakemake automatically orchestrates peak detection, feature alignment, CCS calibration, isotope detection, and MS/MS deconvolution, populating output/ with HDF5 files. Validation: confirm all output HDF5 files are present, contain expected datasets (ms1, ms2, features, isotopes), and have non-zero row counts indicating successful rule execution. References: MSV000091746 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000091746)

**Domain:** metabolomics

**Techniques:** ion-mobility, feature-detection, chromatogram-alignment, mass-spectrometry-imaging

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** DEIMoS is a Python application programming interface and command-line tool for high-dimensional mass spectrometry data analysis workflows. _[grounded: deimos_system]_
- **(finding)** DEIMoS functionality includes feature detection, feature alignment, collision cross section calibration, isotope detection, and MS/MS spectral deconvolution. _[grounded: deimos_system]_
- **(finding)** DEIMoS operates on N-dimensional data, largely agnostic to acquisition instrumentation. _[grounded: deimos_system]_
- **(finding)** Algorithm implementations in DEIMoS simultaneously utilize all dimensions to offer greater separation between features, thus improving detection sensitivity. _[grounded: deimos_system]_
- **(finding)** DEIMoS algorithm implementations increase alignment and feature matching confidence among datasets through simultaneous use of all dimensions. _[grounded: deimos_system]_
- **(finding)** DEIMoS algorithm implementations mitigate convolution artifacts in tandem mass spectra through simultaneous use of all dimensions. _[grounded: deimos_system]_
- **(finding)** DEIMoS version 1.6.2 is available at http://github.com/pnnl/deimos. _[grounded: deimos_system]_
- **(finding)** The CLI can process data from mzML through MS1 and MS2 peakpicking. _[grounded: fmt_mzml]_
- **(finding)** DEIMoS accepts mzML or mzML.gz file formats as inputs. _[grounded: deimos_system]_
- **(finding)** Example LC-IMS-MS/MS data are hosted on MassIVE because files are too large to host on GitHub.
- **(finding)** DEIMoS requires conda and anaconda to be updated before creating a virtual environment. _[grounded: deimos_system]_
- **(finding)** DEIMoS can be installed using pip with the command 'pip install -e .' _[grounded: deimos_system]_
- **(finding)** Alignment is the process by which feature coordinates across samples are adjusted to account for instrument variation such that matching features are aligned.
- **(finding)** DEIMoS implements reference-based alignment by constructing a model for each dimension of a sample by matching detected features against a reference sample. _[grounded: deimos_system]_
- **(finding)** Cross-sample alignment involves matching corresponding features across data sets within a user defined tolerance. _[grounded: method_cross_alignment]_
- **(finding)** DEIMoS achieved an r-squared value of 0.9999784552958134 in CCS calibration for positive ions. _[grounded: deimos_system]_
- **(finding)** DEIMoS achieved an r-squared value of 0.9999784552958121 in CCS calibration for negative ions using the tunemix function. _[grounded: deimos_system]_
- **(finding)** Isotope detection in DEIMoS enumerates m/z offsets corresponding to probable isotopic distance. _[grounded: deimos_system]_
- **(finding)** For C13 isotopologues detection in singly charged species, DEIMoS uses an m/z delta of 1.003355 Da. _[grounded: deimos_system]_
- **(finding)** For C13 isotopologues detection, DEIMoS uses a maximum number of isotopic substitutions of 5. _[grounded: deimos_system]_
- **(finding)** Isotope detection in DEIMoS partitioning should have an overlap of approximately 5.1 to include the range needed for complete isotopologue search with up to 5 substitutions. _[grounded: deimos_system]_
- **(finding)** DEIMoS loads frame, scan, m/z, and intensity from mzML files by default. _[grounded: deimos_system]_
- **(finding)** Conversion to mzML from several other formats can be performed using the ProteoWizard msconvert utility. _[grounded: tool_proteowizard]_
- **(finding)** MS2 extraction in DEIMoS uses non-m/z dimensions to assign fragments in data independent acquisition. _[grounded: deimos_system]_
- **(finding)** DEIMoS implements algorithmic deconvolution to disambiguate MS1 and MS2 features overlapping in non-m/z separation dimensions. _[grounded: deimos_system]_
- **(finding)** Feature detection is the process by which local maxima fulfilling certain criteria are located in signals acquired by analytical instruments.
- **(finding)** DEIMoS implements a peak detection method that leverages persistent homology. _[grounded: deimos_system]_
- **(finding)** The persistent homology peak detection method in DEIMoS runs faster than previous methods. _[grounded: deimos_system]_
- **(finding)** The persistent homology peak detection method in DEIMoS does not depend on any user-defined parameters. _[grounded: deimos_system]_
- **(finding)** DEIMoS was developed with support from Pacific Northwest National Laboratory operated by Battelle for the United States Department of Energy. _[grounded: deimos_system]_
- **(hypothesis)** DEIMoS is licensed under the BSD 3-Clause license. _[grounded: deimos_system]_
- **(finding)** Sean Colby is the development lead for DEIMoS. _[grounded: deimos_system]_
- **(finding)** Jessica Bade, Christine Chang, and Marjolein Oostrom are developers of DEIMoS. _[grounded: deimos_system]_
- **(finding)** Colby et al. published a 2022 paper on DEIMoS in Analytical Chemistry volume 94, issue 16. _[grounded: deimos_system]_
- **(finding)** The example data used in the user guide are available on MassIVE at task 749e436db868410383159b450b470eff.
- **(finding)** The entirety of the data used in the DEIMoS manuscript are available on MassIVE at task a407f040a3d3422d94b1dde95fc0178c. _[grounded: deimos_system]_

## Sanctioned method substitutions
Using any of these instead of the source method is **not penalized**:
- convolution-based approach for peak detection

## Steps

### Step `task_001`
- Title: Reproduce CCS Calibration R-squared Values for Positive and Negative Ion Modes
- Task kind: `reproduction`
- Task: Run the DEIMoS CCS calibration routine on tunemix example data for both positive and negative ion modes, fitting collision cross section values to produce calibration models with R-squared ≥0.99997.
- Inputs:
  - Tunemix reference data (positive ion mode, HDF5 format with ms1 key containing m/z, drift_time, and intensity columns)
  - Tunemix reference data (negative ion mode, HDF5 format with ms1 key containing m/z, drift_time, and intensity columns)
- Expected outputs:
  - Positive ion mode CCS calibration model with reported R-squared value ≥0.99997
  - Negative ion mode CCS calibration model with reported R-squared value ≥0.99997
- Tools: DEIMoS, Python, numpy
- Landmark output files: tunemix_pos_loaded.h5, tunemix_neg_loaded.h5, ccs_calibration_pos_model.pkl, ccs_calibration_neg_model.pkl
- Primary expected artifact: `ccs_calibration_report.txt`

### Step `task_002`
- Title: Reconstruct the Peak-Picking Processing Step on mzML Input Data
- Task kind: `component_reconstruction`
- Task: Align features across two HDF5 feature tables using deimos.alignment with reference-based alignment to produce a single merged feature table with matched features across datasets.
- Inputs:
  - First HDF5 feature table (e.g., example_alignment.h5 with key 'A')
  - Second HDF5 feature table (e.g., example_alignment.h5 with key 'B')
- Expected outputs:
  - Aligned feature table in HDF5 format containing matched features with mz, drift_time, retention_time, and intensity for all aligned features
- Tools: DEIMoS, Python, deimos
- Landmark output files: feature_table_a_loaded.csv, feature_table_b_loaded.csv, alignment_report.txt
- Primary expected artifact: `aligned_features.h5`

### Step `task_003`
- Depends on: `task_002`
- Title: Reconstruct Feature Alignment Across Two Sample Datasets Using Reference-based Alignment
- Task kind: `component_reconstruction`
- Task: Apply DEIMoS isotope detection to a peak-picked HDF5 feature table to identify C13 isotopologue offsets for singly charged species and produce an annotated output table labeling detected isotopologues.
- Inputs:
  - Peak-picked feature table in HDF5 format (deimos-formatted) containing m/z, drift_time, retention_time, and intensity columns
- Expected outputs:
  - Annotated feature table (HDF5) with isotopologue labels including monoisotopic designation, isotope membership count, and C13 mass offsets
- Tools: deimos, Python
- Landmark output files: isotope_clusters.csv, isotope_validation_report.txt
- Primary expected artifact: `features_with_isotopes.h5`

### Step `task_004`
- Depends on: `task_002`
- Title: Reconstruct Isotopologue Detection on a Detected Feature Table
- Task kind: `component_reconstruction`
- Task: Execute the DEIMoS Snakemake workflow end-to-end on the MassIVE user-guide LC-IMS-MS/MS dataset (MSV000091746), using the provided YAML configuration and default workflow parameters, to produce aligned features characterized by mass, collision cross section, tandem mass spectra, and isotopic signature in HDF5 output files.
- Inputs:
  - task_002.expected_outputs[0]: Aligned feature table in HDF5 format containing matched features with mz, drift_time, retention_time, and intensity for all aligned features
  - MassIVE user-guide LC-IMS-MS/MS dataset (MSV000091746) in mzML.gz format
  - YAML configuration file specifying workflow parameters (e.g., config.yaml or workflows/default_config.yaml)
- Expected outputs:
  - HDF5-formatted output files in output/ directory containing detected features aligned across study samples, characterized by mass, CCS, tandem mass spectra, and isotopic signature
  - Snakemake DAG execution log confirming all workflow rules (peak detection, alignment, calibration, isotope detection, deconvolution) completed successfully
- Tools: DEIMoS, Snakemake, conda, pip, Python
- Landmark output files: ms1_peaks.h5, ms2_spectra.h5, aligned_features.h5, isotope_annotations.h5, ccs_calibration_model.pkl
- Primary expected artifact: `features.h5`

## Final expected outputs

- `Positive ion mode CCS calibration model with reported R-squared value ≥0.99997` (type: file, tolerance: hash)
- `Negative ion mode CCS calibration model with reported R-squared value ≥0.99997` (type: file, tolerance: hash)
- `Annotated feature table (HDF5) with isotopologue labels including monoisotopic designation, isotope membership count, and C13 mass offsets` (type: file, tolerance: hash)
- `HDF5-formatted output files in output/ directory containing detected features aligned across study samples, characterized by mass, CCS, tandem mass spectra, and isotopic signature` (type: file, tolerance: hash)
- `Snakemake DAG execution log confirming all workflow rules (peak detection, alignment, calibration, isotope detection, deconvolution) completed successfully` (type: file, tolerance: hash)

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
  "workflow_id": "coll_deimos_workflow",
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
    "Positive ion mode CCS calibration model with reported R-squared value \u22650.99997": "<locator>",
    "Negative ion mode CCS calibration model with reported R-squared value \u22650.99997": "<locator>",
    "Annotated feature table (HDF5) with isotopologue labels including monoisotopic designation, isotope membership count, and C13 mass offsets": "<locator>",
    "HDF5-formatted output files in output/ directory containing detected features aligned across study samples, characterized by mass, CCS, tandem mass spectra, and isotopic signature": "<locator>",
    "Snakemake DAG execution log confirming all workflow rules (peak detection, alignment, calibration, isotope detection, deconvolution) completed successfully": "<locator>"
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
