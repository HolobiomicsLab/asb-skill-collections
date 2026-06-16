# SciTask Card: Reproduce the Peak Matrix Shape from NeatMS Default Preprocessing Parameters

- Task ID: `task_001`
- Schema version: `0.18.0`
- Created at: `2026-06-16T07:11:40.529655+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_neatms/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-processing`, `benchmark-evaluation`
- GitHub: `bihealth/NeatMS`
- Quality: Score 4/5 — clean

## Classification

- Task kind: `reproduction`
- Article type: `software-tool`
- Primary domain: `metabolomics`
- Subdomains: `computational-metabolomics`, `artificial-intelligence`, `untargeted-metabolomics`
- Techniques: `machine-learning`, `deep-learning`, `feature-detection`, `metabolite-identification`, `dimensionality-reduction`
- Keywords: `untargeted lcms` · `signal labelling` · `peak filtering` · `false positive detection` · `neural network classification` · `ms1 peaks` · `metabolomics data processing`

## Research Question
Does applying NeatMS default preprocessing to example mzML and feature-table inputs produce a peak matrix with the documented result_matrix_shape dimensions?

## Connected Finding
NeatMS is an open source python package for untargeted LCMS signal labelling and filtering that enables automated filtering of false positive MS1 peaks reported by commonly used LCMS data processing pipelines.

## Task Description
Preprocess example mzML raw data and feature table using NeatMS default parameters to construct the peak matrix representation, verifying that the output matrix shape matches the documented architecture (2 dimensions × 120 points, with first/last 40 values representing signal margins and middle 40 values representing peak signal).

## Inputs
- Raw LC-MS data in mzML format from NeatMS example data (github.com/bihealth/NeatMS/data folder)
- Feature table in CSV format exported from mzMine or XCMS (github.com/bihealth/NeatMS/data/test_data folder)

## Expected Outputs
- Peak matrix arrays with shape (2, 120) per peak, where dimension 0 encodes signal intensity and dimension 1 encodes binary margin/peak classification
- Verification report confirming first and last 40 values represent signal margins (value 0) and middle 40 values represent peak signal (value 1)
- Batch split statistics (training, test, validation sample counts) matching 80:10:10 default split

## Expected Output File

- `peak_matrix_verification_report.txt`

## Landmark Outputs

- `experiment_object.pkl`
- `batch_training_arrays.npy`
- `batch_test_arrays.npy`
- `batch_validation_arrays.npy`
- `matrix_shape_validation.csv`

## Tools
- NeatMS
- Python
- NumPy
- pandas

## Skills
- lc-ms-data-preprocessing
- peak-matrix-construction
- mzml-feature-table-parsing
- neural-network-input-preparation
- batch-generation-and-validation

## Workflow Description
1. Create a NeatMS Experiment object by loading raw mzML files from the example data folder and the corresponding feature table (csv format) from the github repository, specifying the input format as 'mzmine'. 2. Instantiate a NN_handler (Neural Network Handler) object with the experiment and default batch-creation parameters (matrice_size=120, margin=1, min_scan_num=5). 3. Call create_batches() with default split ratios (80% training, 10% test, 10% validation) and normalise_class=False to generate peak matrix batches. 4. Inspect the resulting batch arrays to extract and verify the shape of the peak matrices (expected: 2 × 120 per peak) and confirm that the binary dimension correctly encodes margin (0) vs. peak (1) regions. 5. Validate that the first and last 40 values correspond to margin portions and the middle 40 values correspond to peak signal, matching the documented result_matrix_shape.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `figures/ADAP_threshold_all_vs_recall_training_500.png` | figure | False |
| `figures/ROC_recall_High_vs_all.png` | figure | False |
| `figures/Screenshot 2020-04-28 at 16.43.33.png` | figure | False |
| `figures/annotation_tool.png` | figure | False |
| `figures/recall_table.png` | figure | False |
| `paper.md` | main_article | True |

## Missing Information
- No changelog or version history provided
- Location and format of documented result_matrix_shape artifact not specified in provided text
- Expected peak matrix shape dimensions (rows, columns) and data type not documented in provided section

## Domain Knowledge
- The margin parameter controls the amount of surrounding signal (baseline) retained around the peak; margin=1 means the margin on both sides equals the peak width, resulting in a 3× the peak width total extraction window that is then interpolated to 120 points.
- The binary dimension (second axis of the 2×120 matrix) serves as an attention mask for the neural network, distinguishing margin regions (0) from true peak signal (1), helping the model learn to focus on peak features rather than baseline noise.
- The min_scan_num parameter (default 5) filters out low-quality peaks with fewer than 5 scans, as such sparse signals are unreliable for manual or automated classification and degrade model performance.
- The softmax output layer produces three class probabilities (High_quality, Low_quality, Noise) that sum to 1; downstream hyperparameter tuning uses a probability threshold to balance sensitivity vs. specificity.
- NeatMS applies dropout and kernel regularization within the convolutional architecture to prevent overfitting during transfer learning or full training, requiring careful monitoring of training vs. validation accuracy divergence.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] Does applying NeatMS default preprocessing to example mzML and feature-table inputs produce a peak matrix with the documented result_matrix_shape dimensions?: 'The source code and related materials (e.g. tutorials, example data, neural network model) are available at [https://github.com/bihealth/NeatMS](https://github.com/bihealth/NeatMS).'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] NeatMS is an open source python package for untargeted LCMS signal labelling and filtering that enables automated filtering of false positive MS1 peaks reported by commonly used LCMS data processing pipelines.: '**NeatMS** is an open source python package for untargeted LCMS signal labelling and filtering. **NeatMS** enables automated filtering of false positive MS<sup>1</sup> peaks reported by commonly used'
- `ev_003` from `agent2_synthesis` (agent2_traced): [other] Raw LC-MS data in mzML format from NeatMS example data (github.com/bihealth/NeatMS/data folder): 'Raw data files in mzML format'
- `ev_004` from `agent2_synthesis` (agent2_traced): [other] Feature table in CSV format exported from mzMine or XCMS (github.com/bihealth/NeatMS/data/test_data folder): 'One feature table file in .csv format'
- `ev_005` from `agent2_synthesis` (agent2_traced): [other] Peak matrix arrays with shape (2, 120) per peak, where dimension 0 encodes signal intensity and dimension 1 encodes binary margin/peak classification: 'The resulting matrix size for one peak is therefore (2, 120)'
- `ev_006` from `agent2_synthesis` (agent2_traced): [other] Verification report confirming first and last 40 values represent signal margins (value 0) and middle 40 values represent peak signal (value 1): 'the first and last 40 values of the peak will represent the margins (surrounding signal), the middle 40 values represent the peak itself'
- `ev_007` from `agent2_synthesis` (agent2_traced): [other] Batch split statistics (training, test, validation sample counts) matching 80:10:10 default split: 'By default, the split between training:test:validation batches is 80:10:10'
- `ev_008` from `agent2_synthesis` (agent2_traced): [other] NeatMS: 'NeatMS provides the necessary functions to do that, all we will have to do is create a `Neural network handler` object'
- `ev_009` from `agent2_synthesis` (agent2_traced): [other] Python: 'After installation, you should be able to import NeatMS'
- `ev_010` from `agent2_synthesis` (agent2_traced): [other] NumPy: 'import numpy as np'
- `ev_011` from `agent2_synthesis` (agent2_traced): [other] pandas: 'import pandas as pd'
- `ev_012` from `agent2_synthesis` (agent2_traced): [discussion] No changelog or version history provided: 'No changelog found.'
- `ev_013` from `agent2_synthesis` (agent2_traced): [discussion] Location and format of documented result_matrix_shape artifact not specified in provided text: 'No changelog found.'
- `ev_014` from `agent2_synthesis` (agent2_traced): [discussion] Expected peak matrix shape dimensions (rows, columns) and data type not documented in provided section: 'No changelog found.'

## Evaluation Strategy
### Direct Checks
- verify file exists in github:bihealth__NeatMS repository: example mzML input file
- verify file exists in github:bihealth__NeatMS repository: example feature-table input file
- script_runs: NeatMS default preprocessing applied to example inputs without errors
- verify output file format_is: peak matrix (array, table, or matrix format)
- verify peak matrix shape matches documented result_matrix_shape artifact — first 40 and last 40 values (robust to representation format)
- verify peak matrix binary dimension (rows vs. columns) matches documented result_matrix_shape — exact byte-for-byte or exact value comparison

### Expert Review
- peak matrix values and distributions are consistent with expected LC-MS preprocessing behavior (noise filtering, normalization if applied)
- first and last 40 row/column values are scientifically plausible given input mzML and feature-table characteristics

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Methodology Summary
1. Load raw mzML and feature table files into a NeatMS Experiment object using the standard import interface.
2. Create a NN_handler with default parameters (matrix_size=120, margin=1, min_scan_num=5) to instantiate the peak matrix construction pipeline.
3. Generate batch arrays by calling create_batches() with default 80:10:10 split ratios and no class normalization.
4. Extract and inspect the shape and binary encoding of the peak matrices to confirm (2, 120) dimensionality and margin/peak signal partitioning.
5. Validation: Confirm that peak matrices have shape (2, 120), binary dimension correctly encodes margin (0) and peak (1) regions with first/last 40 points and middle 40 points respectively, and batch counts match documented 80:10:10 split.

## Workflow Ports

**Inputs:**

- `raw_mzml_files` — Raw LC-MS data in mzML format
- `feature_table_csv` — Feature table in CSV format

**Outputs:**

- `peak_matrix_arrays` — Preprocessed peak matrices with shape (2, 120)
- `matrix_shape_verification` — Verification report of matrix dimensions and margin/peak encoding
- `batch_statistics` — Training/test/validation split statistics

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:bihealth__NeatMS`
- **Synthesized at:** 2026-06-16T07:21:35+00:00

## Extraction Quality
- Score: 4/5 — coherent, no placeholders, no flags.

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
