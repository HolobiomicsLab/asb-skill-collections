# Workflow Challenge: `coll_pcpfm_workflow`


> The Python-Centric Pipeline for Metabolomics (PCPFM) is an end-to-end preprocessing framework that converts raw LC-MS data through feature extraction, quality control, normalization, and annotation to produce analysis-ready metabolomic feature tables and empirical compound annotations.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

PCPFM orchestrates a fixed sequence of metabolomics data processing steps: raw file conversion to mzML format, Asari-based feature extraction yielding full and preferred feature tables, blank masking by intensity ratio comparison, sample filtering by metadata or quality control results, TIC normalization using common features above a percentile threshold, missing value imputation as multiples of minimum per-feature values, optional pycombat-based batch correction for multi-batch experiments, and empirical compound construction via khipu with configurable mz/rt tolerances and adduct/isotope definitions. The pipeline outputs standardized feature tables and JSON-formatted empirical compounds ready for downstream statistical analysis, with intermediate results and quality control visualizations stored in a structured experiment directory.

## Research questions

- What are the sequential data processing steps that the PCPFM pipeline executes to transform raw LC-MS metabolomics data into normalized feature tables ready for statistical analysis?
- How does the blank_masking command filter features from a metabolomics feature table based on the intensity ratio between unknown samples and blank samples?
- How does the impute command replace zero and missing values in a metabolomics feature table using a minimum-value-based interpolation strategy?
- How does the build_empCpds command construct empirical compound groups from a feature table using khipu with configurable mz and retention time tolerances?
- Does batch correction via pycombat preserve the structural integrity (sample and feature count) of multi-batch metabolomics feature tables while reducing inter-batch variance?

## Methods overview

Parse and validate CSV metadata; create experiment directory structure and initialize experiment.json state object with sample metadata, file paths, and sample-type annotations. Convert Thermo .raw files to centroid mzML using ThermoRawFileParser; store converted files in experiment/converted_acquisitions subdirectory. Run Asari feature extraction on mzML files with inferred ionization mode, m/z tolerance (5 ppm), and retention-time tolerance (2 sec); generate 'full' and 'preferred' feature table monikers. Apply blank masking by comparing feature intensity ratios (study samples vs. blanks, default 3×) to remove likely contaminants and background ions; retain filtered feature table moniker. Drop unwanted samples (blanks, QC, outliers) via metadata field or QAQC filter criteria; generate trimmed feature table moniker. Normalize feature intensities using TIC of common features (default 90th percentile) with within-batch and between-batch correction if multiple batches present; apply normalization factors to all samples. Impute missing values using multiplicative floor (default 0.5× per-feature minimum) to handle zero or missing entries while respecting multiplicative error structure. Remove infrequent features below retention percentile (default 50%) to discard rare and potentially spurious features; generate filtered feature table moniker. Build empirical compounds from final feature table using khipu with adducts (z ≤ 3), isotope patterns (13C3), m/z tolerance (5 ppm), and retention-time tolerance (2 sec); assign pre-annotations (adduct class, isotope status) and generate empCpd.json. Validation: Verify feature table row count > 0, empCpd.json contains ≥1 compound objects with required keys (adducts, rt, mz, features), and experiment.json tracks all moniker transformations with no gaps in processing history. References: source article (DOI: 10.1371/journal.pcbi.1011912) Load feature table and metadata; parse sample types from the specified query field. Partition samples into blank and unknown groups based on the provided blank_value and sample_value. Calculate per-feature median/mean intensity within each group, excluding zeros. Compute intensity ratio (unknown/blank) for each feature. Apply threshold filter: retain features where ratio ≥ blank_intensity_ratio (default 3). Validation: Verify that dropped features are those with ratio < threshold and no data loss occurs for passing features. References: source article (DOI: 10.1371/journal.pcbi.1011912) Load the input feature table from disk using the provided table_moniker identifier. Compute the minimum non-zero intensity value for each feature across all samples, handling missing/zero values as absent. Apply the interpolation formula: imputation_value = interpolation_ratio × feature_minimum for each feature. Replace all zero and missing (NaN) values in the feature table with the calculated feature-specific imputation values. Save the imputed feature table to the experiment feature_tables directory under the new_moniker name. Validation: verify that all zero and missing values are replaced, all imputed values equal interpolation_ratio × feature_minimum, and the output table has identical dimensions to the input. References: source article (DOI: 10.1371/journal.pcbi.1011912) Load the preferred feature table with m/z, retention time, and intensity columns. Apply pairwise feature distance calculations (m/z in ppm, rt in seconds) to identify candidates for grouping within user-specified tolerances. Assign isotopologue and adduct labels based on theoretical mass differences and charge patterns, constrained by ionization mode and adduct list. Cluster features into empirical compound groups, recording the list of constituent feature IDs and median m/z and rt per group. Serialize groups to JSON with all required fields (list_of_features, mz, rt, adduct, isotope annotations) and validate structure. Validation: verify empCpd.json is well-formed JSON, contains ≥1 empirical compound group, and each group has non-empty list_of_features, numeric mz, and numeric rt fields. References: source article (DOI: 10.1371/journal.pcbi.1011912) Load interpolated feature table and metadata containing batch labels for each sample. Invoke pycombat-based batch correction via pcpfm batch_correct with --by_batch parameter set to the batch metadata field. Confirm output table preserves input sample and feature dimensions. Calculate median inter-batch variance for representative high-intensity features before and after correction, grouped by batch field. Validation: confirm corrected-table inter-batch variance is lower than uncorrected baseline, indicating successful batch effect attenuation without dimension loss. References: source article (DOI: 10.1371/journal.pcbi.1011912)

**Domain:** metabolomics

**Techniques:** lc-ms, tandem-ms, feature-detection, database-annotation, spectral-library-matching, metabolite-identification

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** The Python-Centric Pipeline for Metabolomics is designed to take raw LC-MS metabolomics data and ready them for downstream statistical analysis.
- **(finding)** The pipeline can convert Thermo .raw files to mzML format using ThermoRawFileParser. _[grounded: COMP-THERMORAWFILEPARSER]_
- **(finding)** The pipeline can process mzML data to feature tables using Asari. _[grounded: COMP-ASARI]_
- **(finding)** The pipeline performs pre-annotation to group features to empirical compounds using khipu. _[grounded: COMP-KHIPU]_
- **(finding)** The pipeline can perform MS2 annotation using matchms with a custom database defaulting to MoNA. _[grounded: COMP-MATCHMS]_
- **(finding)** Asari supports a visual dashboard to explore and inspect individual features. _[grounded: COMP-ASARI]_
- **(finding)** The pipeline developers are working to add support for GC and other data types.
- **(finding)** To replicate the presented results, users need to run the download extras command.
- **(finding)** Mitchell et al. 2024 published a paper on common data models to streamline metabolomics processing and annotation in a Python pipeline.
- **(finding)** Li et al. 2023 published a paper on trackable and scalable LC-MS metabolomics data processing using asari in Nature Communications. _[grounded: COMP-ASARI]_
- **(finding)** There was an issue regarding sample names that do not match their mzML file names, which was fixed as of 2/28/24.
- **(finding)** The pipeline inputs should include raw files in .raw or .mzML format and a CSV file for metadata.
- **(finding)** The pipeline outputs are intended to be immediately usable for downstream analysis tools like MetaboAnalyst or common tools in R and Python. _[grounded: TOOL-METABOANALYST]_
- **(finding)** The preferred installation mechanism for PCPFM is pip. _[grounded: SYS-PCPFM]_
- **(finding)** The HMDB is not to be used for commercial purposes. _[grounded: DATASET-HMDB]_
- **(finding)** Annotation sources including the HMDB are free for public non-commercial use. _[grounded: DATASET-HMDB]_
- **(finding)** The download extras command can download LC-MS/MS databases from MoNA, a JMS-compliant version of the HMDB, and LMSD. _[grounded: DATASET-HMDB]_
- **(finding)** The preprocessing command can create a new CSV file using rules specified in a JSON preprocessing configuration file.
- **(finding)** The preprocessing configuration supports searching for substrings in specified fields to populate metadata values.
- **(finding)** If multiple preprocessing rules match, the specified values are concatenated using an underscore.
- **(finding)** The assemble command creates an experiment directory to store the project. _[grounded: COMP-EXPERIMENT]_
- **(finding)** The experiment object is used throughout processing and stores intermediates. _[grounded: COMP-EXPERIMENT]_
- **(finding)** Filters can be applied to include or exclude acquisitions based on metadata field values.
- **(finding)** The convert command converts .raw files to centroid .mzML files.
- **(finding)** The ThermoRawFileParser can be used on Mac with mono installed. _[grounded: COMP-THERMORAWFILEPARSER]_
- **(finding)** The asari command processes .mzML files into metabolomic feature tables. _[grounded: COMP-ASARI]_
- **(finding)** The asari command automatically infers the correct ionization mode for the experiment. _[grounded: COMP-ASARI]_
- **(finding)** After asari is run, two feature table monikers are generated: 'full' and 'preferred' for the full and preferred feature tables respectively. _[grounded: COMP-ASARI]_
- **(finding)** The QAQC command can generate PCA plots limited to two components.
- **(finding)** The QAQC command can generate t-SNE plots limited to two components.
- **(finding)** Blank masking removes features that are likely due to background ions and contaminants.
- **(finding)** Blank masking is achieved by comparing the intensity of a feature in study samples to those in blanks.
- **(finding)** The default blank_intensity_ratio is 3.
- **(finding)** Metadata values for drop sample commands are case sensitive.
- **(finding)** The default TIC normalization percentile is 0.90 (90%).
- **(finding)** The default feature retention percentile is 50% (0.50).
- **(finding)** The default imputation ratio is 0.5.
- **(finding)** Batch correction is performed using pycombat. _[grounded: COMP-PYCOMBAT]_
- **(finding)** Log transformation is performed using log2 by default.
- **(finding)** EmpCpds are groups of associated features, typically isotopes and adducts, that belong to the same tentative compound.
- **(finding)** By default, charges up to z=3 are used for EmpCpd construction. _[grounded: COMP-EMPCPD]_
- **(finding)** By default, m+13C3 isotopologues are considered for EmpCpd construction. _[grounded: COMP-EMPCPD]_
- **(finding)** For orbitrap LC data, a default 5 ppm tolerance and 2 second retention time tolerance is sufficient for EmpCpd construction. _[grounded: COMP-EMPCPD]_
- **(finding)** Level 4 annotations are not currently generated for singletons because their adducts cannot be inferred.
- **(finding)** MS1 Level 1b annotation compares feature retention time and m/z values to those of authentic standards libraries.
- **(finding)** MS2 mapping is performed by comparing precursor retention time and m/z to retention times and m/z values of features.
- **(finding)** The default m/z tolerance for MS2 to feature mapping is 5 ppm.
- **(finding)** The default retention time tolerance for MS2 mapping is 30 seconds.
- **(finding)** The MoNA database is used as the default for MS2 annotation if no custom database is provided. _[grounded: DATASET-MONA]_
- **(finding)** The generate_output command creates three output tables in the results subdirectory.
- **(finding)** The report command generates a PDF report in the output directory. _[grounded: COMP-REPORT]_
- **(finding)** The reset command destroys all user generated tables and EmpCpds but keeps the outputs from Asari intact. _[grounded: COMP-ASARI]_

## Steps

### Step `task_001`
- Title: Reconstruct the PCPFM fixed processing pipeline from raw mzML input to annotated feature table output
- Task kind: `component_reconstruction`
- Task: Implement the fixed PCPFM orchestration control loop that coordinates sequential metabolomics data processing: experiment assembly, LC-MS feature extraction via Asari, blank masking, sample dropping, normalization, missing-value imputation, and empirical compound construction. The system must maintain experiment state across all stages and output a feature table and empirical compound list ready for downstream annotation and statistical analysis.
- Inputs:
  - CSV metadata file with sample names, file paths, sample type classification, and batch identifiers
  - Raw LC-MS data files in Thermo .raw or mzML format
- Expected outputs:
  - Processed feature table (TSV/CSV) with normalized, imputed, and filtered metabolomic features ready for statistical analysis
  - Empirical compound JSON file representing putative metabolites grouped by isotopes and adducts with pre-annotation
  - Experiment state JSON file (experiment.json) tracking all processing steps, intermediate tables, and metadata
- Tools: Python, ThermoRawFileParser, Asari, khipu
- Landmark output files: converted_acquisitions/*.mzML, asari_results/preferred_Feature_table.tsv, feature_tables/*_blank_masked.tsv, feature_tables/*_normalized.tsv, feature_tables/*_imputed.tsv, annotations/empCpd.json
- Primary expected artifact: `preferred_feature_table.tsv`

### Step `task_002`
- Depends on: `task_001`
- Title: Implement the blank masking filter step in PCPFM and verify feature removal by intensity ratio
- Task kind: `component_reconstruction`
- Task: Apply blank-masking filter to a metabolomics feature table to remove features whose intensity in unknown samples does not exceed a configurable ratio threshold relative to blank samples. Output the filtered feature table with low-intensity background features removed.
- Inputs:
  - Feature table in TSV or CSV format with features as rows and samples as columns, indexed by feature identifier
  - Sample metadata CSV file with at minimum sample names and a categorical field (e.g., 'sample_type') designating blank vs. unknown samples
- Expected outputs:
  - Blank-masked feature table in TSV format with low-intensity background features removed, indexed by feature identifier and sample
- Tools: ThermoRawFileParser, Python
- Landmark output files: feature_intensity_comparison.csv, features_dropped_by_ratio.txt
- Primary expected artifact: `preferred_blank_masked.tsv`

### Step `task_003`
- Depends on: `task_001`
- Title: Implement the imputation filter step and verify output values equal interpolation_ratio times per-feature minimum
- Task kind: `component_reconstruction`
- Task: Apply the impute command to a feature table using a specified interpolation_ratio parameter, replacing all zero and missing values with the interpolation_ratio multiplied by the minimum non-zero value for each feature, and save the result to a named output table artifact.
- Inputs:
  - task_001.expected_outputs[0]: Processed feature table (TSV/CSV) with normalized, imputed, and filtered metabolomic features ready for statistical analysis
  - Feature table (identified by table_moniker parameter)
  - interpolation_ratio parameter (multiplier for minimum feature value)
- Expected outputs:
  - Imputed feature table saved with new_moniker in experiment feature_tables directory
- Tools: ThermoRawFileParser, Python
- Landmark output files: feature_table_original.tsv, feature_minima.json
- Primary expected artifact: `feature_table_imputed.tsv`

### Step `task_004`
- Depends on: `task_001`
- Title: Reconstruct the EmpCpd construction step and verify the empCpd.json output structure
- Task kind: `component_reconstruction`
- Task: Build empirical compounds (EmpCpds) from a preferred feature table using khipu with configurable m/z and retention time tolerances. Verify that the output JSON file is produced, is valid JSON, and contains the expected empirical compound group fields (list_of_features, m/z, rt).
- Inputs:
  - preferred feature table (TSV from asari processing)
  - ionization mode (positive or negative) inferred from experiment metadata
  - optional adduct configuration files (JSON) for positive and negative modes
- Expected outputs:
  - empCpd.json file containing empirical compound groups with fields: list_of_features, mz, rt, adduct annotations, and isotopologue assignments
  - experiment.json updated with empCpd moniker and metadata
- Tools: ThermoRawFileParser, khipu, Python
- Landmark output files: feature_clustering_assignments.log, empCpd.json
- Primary expected artifact: `empCpd.json`

### Step `task_005`
- Depends on: `task_002`
- Title: Extend PCPFM batch correction step to validate pycombat output retains sample count and reduces batch variance
- Task kind: `extension`
- Task: Apply batch correction to a multi-batch interpolated feature table using pycombat, then verify that the corrected table preserves sample and feature counts while reducing inter-batch variance for selected metabolite features.
- Inputs:
  - task_002.expected_outputs[0]: Blank-masked feature table in TSV format with low-intensity background features removed, indexed by feature identifier and sample
  - Interpolated feature table (.tsv) with missing values imputed to 0.5× minimum feature intensity
  - Sample metadata CSV with batch field indicating experimental batch or acquisition group for each sample
- Expected outputs:
  - Batch-corrected feature table (.tsv) with identical dimensions to input, feature intensities adjusted to remove systematic batch biases
  - Quantitative validation report containing: sample count, feature count, pre- and post-correction inter-batch variance estimates for ≥5 representative features
- Tools: ThermoRawFileParser, pycombat, Python
- Landmark output files: interpolated_input_table.tsv, pre_correction_batch_variance_summary.json, batch_corrected_feature_table.tsv, post_correction_batch_variance_summary.json, batch_correction_validation_report.txt
- Primary expected artifact: `batch_corrected_feature_table.tsv`

## Final expected outputs

- `Imputed feature table saved with new_moniker in experiment feature_tables directory` (type: file, tolerance: hash)
- `empCpd.json file containing empirical compound groups with fields: list_of_features, mz, rt, adduct annotations, and isotopologue assignments` (type: file, tolerance: hash)
- `experiment.json updated with empCpd moniker and metadata` (type: file, tolerance: hash)
- `Batch-corrected feature table (.tsv) with identical dimensions to input, feature intensities adjusted to remove systematic batch biases` (type: file, tolerance: hash)
- `Quantitative validation report containing: sample count, feature count, pre- and post-correction inter-batch variance estimates for ≥5 representative features` (type: file, tolerance: hash)

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
  "workflow_id": "coll_pcpfm_workflow",
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
    "Imputed feature table saved with new_moniker in experiment feature_tables directory": "<locator>",
    "empCpd.json file containing empirical compound groups with fields: list_of_features, mz, rt, adduct annotations, and isotopologue assignments": "<locator>",
    "experiment.json updated with empCpd moniker and metadata": "<locator>",
    "Batch-corrected feature table (.tsv) with identical dimensions to input, feature intensities adjusted to remove systematic batch biases": "<locator>",
    "Quantitative validation report containing: sample count, feature count, pre- and post-correction inter-batch variance estimates for \u22655 representative features": "<locator>"
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
