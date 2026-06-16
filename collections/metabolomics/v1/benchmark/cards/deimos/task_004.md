# SciTask Card: Reconstruct Isotopologue Detection on a Detected Feature Table

- Task ID: `task_004`
- Schema version: `0.18.0`
- Created at: `2026-06-16T07:39:32.715601+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_deimos/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-processing`, `benchmark-evaluation`
- GitHub: `pnnl/deimos`
- Input from: `task_002`

## Classification

- Task kind: `component_reconstruction`
- Article type: `software-tool`
- Primary domain: `metabolomics`
- Subdomains: `computational-metabolomics`, `untargeted-metabolomics`
- Techniques: `ion-mobility`, `feature-detection`, `chromatogram-alignment`, `mass-spectrometry-imaging`
- Keywords: `high-dimensional mass spectrometry` · `feature detection` · `feature alignment` · `collision cross section calibration` · `isotope detection` · `ms/ms spectral deconvolution` · `n-dimensional data analysis` · `untargeted metabolomics` · `multidimensional spectrometry`

## Research Question
Does the DEIMoS Snakemake workflow successfully execute end-to-end on the publicly deposited MassIVE user guide example dataset, completing all workflow rules and producing final HDF5 output artifacts?

## Connected Finding
DEIMoS functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution, with output comprising detected features aligned across study samples and characterized by mass, CCS, tandem mass spectra, and isotopic signature.

## Task Description
Execute the DEIMoS Snakemake workflow end-to-end on the MassIVE user-guide LC-IMS-MS/MS dataset (MSV000091746), using the provided YAML configuration and default workflow parameters, to produce aligned features characterized by mass, collision cross section, tandem mass spectra, and isotopic signature in HDF5 output files.

## Inputs
- task_002.expected_outputs[0]: Aligned feature table in HDF5 format containing matched features with mz, drift_time, retention_time, and intensity for all aligned features
- MassIVE user-guide LC-IMS-MS/MS dataset (MSV000091746) in mzML.gz format
- YAML configuration file specifying workflow parameters (e.g., config.yaml or workflows/default_config.yaml)

## Expected Outputs
- HDF5-formatted output files in output/ directory containing detected features aligned across study samples, characterized by mass, CCS, tandem mass spectra, and isotopic signature
- Snakemake DAG execution log confirming all workflow rules (peak detection, alignment, calibration, isotope detection, deconvolution) completed successfully

## Expected Output File

- `features.h5`

## Landmark Outputs

- `ms1_peaks.h5`
- `ms2_spectra.h5`
- `aligned_features.h5`
- `isotope_annotations.h5`
- `ccs_calibration_model.pkl`

## Tools
- DEIMoS
- Snakemake
- conda
- pip
- Python

## Skills
- mass-spectrometry-workflow-orchestration-snakemake
- lcims-msms-data-preprocessing-peak-detection
- multidimensional-feature-alignment-cross-dataset
- collision-cross-section-calibration-ccs
- tandem-mass-spectrum-deconvolution-isotope-annotation
- hdf5-output-validation-verification

## Workflow Description
1. Clone the DEIMoS repository from GitHub and activate the conda environment as specified in the installation documentation. 2. Download the MassIVE user-guide example dataset (MSV000091746) and place mzML.gz files in the input/ directory. 3. Prepare or modify the config.yaml file (or use workflows/default_config.yaml) to specify dataset-specific parameters for the workflow. 4. Invoke the DEIMoS CLI with the configuration file, specifying the number of cores and execution mode (local or cluster) as needed: deimos --config config.yaml --cores N. 5. Snakemake automatically detects input files, executes the complete rule DAG including peak detection, feature alignment, CCS calibration, isotope detection, and MS/MS deconvolution, and populates output/ with HDF5-formatted results. 6. Verify successful completion by confirming all output HDF5 files are present in output/ and contain expected datasets (ms1, ms2, features, isotopes) with non-zero row counts.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `figures/icon.png` | figure | False |
| `figures/logo.png` | figure | False |
| `figures/overview.png` | figure | False |
| `paper.md` | main_article | True |

## Data Deposits

| Kind | Accession | URL | Evidence |
|---|---|---|---|
| massive | `MSV000091746` | https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000091746 | 3d3422d94b1dde95fc0178c>`_ * Use ftp://massive.ucsd.edu/v01/MSV000091746 as the FTP Download Link (not the v07 folder shown in MassI |

## Missing Information
- No changelog documenting version history, bug fixes, or feature changes is available

## Domain Knowledge
- DEIMoS is instrument-agnostic and designed to operate on N-dimensional mass spectrometry data, utilizing all available dimensions (m/z, drift time, retention time, intensity) simultaneously for improved feature detection, alignment, and deconvolution.
- The Snakemake workflow automatically detects .mzML and .mzML.gz files in the input/ directory and produces HDF5-formatted output in output/, with the directory structure relative to the current working directory.
- The default workflow configuration provided in workflows/default_config.yaml may require modification to accommodate dataset-specific instrument parameters, ionization mode, and processing thresholds.
- Feature detection and alignment operate on all N dimensions to increase sensitivity and confidence in feature matching; MS/MS deconvolution benefits from multi-dimensional separation by reducing spectral convolution artifacts.
- Successful workflow completion requires no manual intervention after invocation; Snakemake manages rule dependencies, parallelization, and file routing based on the configuration and available computational resources.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] Does the DEIMoS Snakemake workflow successfully execute end-to-end on the publicly deposited MassIVE user guide example dataset, completing all workflow rules and producing final HDF5 output artifacts?: 'DEIMoS, or Data Extraction for Integrated Multidimensional Spectrometry, is a Python application programming interface and command-line tool for high-dimensional mass spectrometry (MS) data analysis'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] DEIMoS functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution, with output comprising detected features aligned across study samples and characterized by mass, CCS, tandem mass spectra, and isotopic signature.: 'Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution, with the output comprising detected'
- `ev_003` from `agent2_synthesis` (agent2_traced): [other] MassIVE user-guide LC-IMS-MS/MS dataset (MSV000091746) in mzML.gz format: 'Use ftp://massive.ucsd.edu/v01/MSV000091746 as the FTP Download Link'
- `ev_004` from `agent2_synthesis` (agent2_traced): [other] YAML configuration file specifying workflow parameters (e.g., config.yaml or workflows/default_config.yaml): 'A Snakemake configuration file in YAML format is required. DEIMoS will try to find config.yaml in the current directory, else a configuration file must be specified through the --config flag. A'
- `ev_005` from `agent2_synthesis` (agent2_traced): [other] HDF5-formatted output files in output/ directory containing detected features aligned across study samples, characterized by mass, CCS, tandem mass spectra, and isotopic signature: 'output comprising detected features aligned across study samples and characterized by mass, CCS, tandem mass spectra, and isotopic signature'
- `ev_006` from `agent2_synthesis` (agent2_traced): [other] Snakemake DAG execution log confirming all workflow rules (peak detection, alignment, calibration, isotope detection, deconvolution) completed successfully: 'The CLI is able to process data from mzML through MS1 and MS2 peakpicking.'
- `ev_007` from `agent2_synthesis` (agent2_traced): [other] DEIMoS: 'DEIMoS, or Data Extraction for Integrated Multidimensional Spectrometry, is a Python application programming interface and command-line tool'
- `ev_008` from `agent2_synthesis` (agent2_traced): [other] Snakemake: 'A Snakemake configuration file in YAML format is required.'
- `ev_009` from `agent2_synthesis` (agent2_traced): [other] conda: 'Use conda to create a virtual environment with required dependencies.'
- `ev_010` from `agent2_synthesis` (agent2_traced): [other] pip: 'Install DEIMoS using pip: pip install -e .'
- `ev_011` from `agent2_synthesis` (agent2_traced): [other] Python: 'is a Python application programming interface and command-line tool'
- `ev_012` from `agent2_synthesis` (agent2_traced): [discussion] No changelog documenting version history, bug fixes, or feature changes is available: '_No changelog found._'

## Evaluation Strategy
### Direct Checks
- verify file github:pnnl__deimos can be cloned from https://github.com/pnnl/deimos
- verify dataset MSV000091746 is accessible via ftp://massive.ucsd.edu/v01/MSV000091746
- verify Snakemake workflow execution completes without errors using provided YAML configuration
- verify all final HDF5 output artifacts exist (file_exists check on output .h5 files)
- verify output HDF5 files are valid HDF5 format using h5py or similar tool
- verify Snakemake reports successful completion of all workflow rules (script_runs with exit code 0)

### Expert Review
- confirm that HDF5 output structure and content are consistent with DEIMoS workflow specification
- validate that feature detection, alignment, and calibration steps produced chemically plausible results
- assess whether output datasets contain expected dimensional data (m/z, drift_time, retention_time, intensity) without corruption

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** medium

## Methodology Summary
1. Clone DEIMoS repository and create conda virtual environment with required dependencies.
2. Download MassIVE user-guide dataset (MSV000091746) and place mzML.gz files in input/ directory.
3. Prepare or modify YAML configuration file with workflow-specific parameters (default_config.yaml provided).
4. Invoke DEIMoS CLI with config.yaml to execute Snakemake workflow, specifying core count and execution mode.
5. Snakemake automatically orchestrates peak detection, feature alignment, CCS calibration, isotope detection, and MS/MS deconvolution, populating output/ with HDF5 files.
6. Validation: confirm all output HDF5 files are present, contain expected datasets (ms1, ms2, features, isotopes), and have non-zero row counts indicating successful rule execution.
7. References: MSV000091746 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000091746)

## Workflow Ports

**Inputs:**

- `mzml_dataset` — MassIVE user-guide mzML.gz files
- `config_yaml` — Snakemake YAML configuration file

**Outputs:**

- `hdf5_features` — HDF5 output files with aligned features and annotations
- `execution_log` — Snakemake workflow completion status

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:pnnl__deimos`
- **Synthesized at:** 2026-06-16T07:45:23+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
