# Workflow Challenge: `coll_ps2ms_workflow`


> PS²MS is a deep learning-based prediction system designed for detecting novel new psychoactive substances using mass spectrometry data.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 3-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

Reproduces 1 reported result: PS²MS is a deep learning-based prediction system designed for detecting novel new psychoactive substances using mass spectrometry data. Analyses 1 derived result: The PS2MS system is designed as a deep learning-based prediction system for detecting novel new psychoactive substances using mass spectrometry data. Reconstructs 1 described mechanism (described in the paper but not separately evaluated there): The paper describes PS2MS as a deep learning-based prediction system for detecting novel new psychoactive substances using mass spectrometry, which requires conversion of chemical structures into an encoded feature format.

## Research questions

- Can the PS²MS deep learning system successfully predict and identify new psychoactive substances from mass spectrometry data when applied to test inputs?
- How are SMILES representations of NPS chemical structures converted into the encoded feature format required as input for the PS2MS deep learning model?
- How do prediction confidence scores from the PS2MS deep learning model vary across structurally diverse or novel NPS analogues in the evaluation dataset?

## Methods overview

Load mass spectrometry spectral data from input files in standard formats (mzML/mzXML/MS2 or pre-processed matrices). Preprocess spectra through normalization and feature vectorization to match PS2MS input requirements. Load pre-trained deep learning model architecture and weights from the PS2MS repository. Execute forward inference pass on all preprocessed spectra to generate classification logits and probability scores. Assign NPS class labels based on maximum predicted probability and apply confidence filtering. Validation: Verify that prediction output format matches expected schema (spectrum_id, predicted_class, confidence_score columns) and that confidence scores are valid probabilities (0–1 range). References: source article (DOI: 10.1021/acs.analchem.3c05019) Parse SMILES strings and construct RDKit molecule objects with syntax validation. Extract molecular graph properties (atoms, bonds, connectivity) from validated structures. Compute structural and topological descriptors aligned with PS2MS input schema. Encode descriptor values into fixed-size numerical tensor format. Apply feature normalization (scaling/centering) using model training statistics. Validation: Confirm encoded matrix dimensions match PS2MS input layer specification (n_features) and no NaN or infinite values are present. References: source article (DOI: 10.1021/acs.analchem.3c05019) Load the PS2MS deep learning model and evaluation dataset from the public repository. Compute prediction confidence scores for all compounds in the evaluation set via forward inference. Calculate structural similarity of each compound to training set using molecular fingerprints and Tanimoto distance. Stratify compounds into structural novelty tiers based on similarity thresholds. Aggregate confidence statistics (mean, median, std, range) within each novelty stratum. Validation: Confirm that confidence scores are stratified by novelty category (lower confidence for more novel structures) and produce publication-ready summary statistics and visualizations. References: source article (DOI: 10.1021/acs.analchem.3c05019)

**Domain:** cheminformatics

**Techniques:** deep-learning, machine-learning, metabolite-identification, tandem-ms

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** PS²MS is a repository for an NYCU JHHLab NPS detection project. _[grounded: domain_nps]_
- **(finding)** PS²MS is a deep learning-based prediction system for detecting novel new psychoactive substances using mass spectrometry. _[grounded: tool_mass_spectrometry]_

## Steps

### Step `task_001`
- Title: Reproduce PS2MS deep learning model predictions for NPS detection from mass spectrometry data
- Task kind: `reproduction`
- Task: Run the PS2MS deep learning inference pipeline on mass spectrometry data to predict and classify new psychoactive substances (NPS). Produce structured NPS predictions with confidence scores matching the reported detection performance.
- Inputs:
  - Mass spectrometry data (raw spectra in mzML/mzXML/MS2 format or pre-processed feature matrix)
  - Pre-trained PS2MS deep learning model weights and architecture definition
- Expected outputs:
  - NPS classification predictions table with spectrum identifiers, predicted compound classes, and confidence scores per prediction
- Tools: PS2MS
- Landmark output files: preprocessed_spectra.pkl, model_outputs_raw.npy, nps_predictions.csv
- Primary expected artifact: `nps_predictions.csv`

### Step `task_002`
- Depends on: `task_001`
- Title: Reconstruct the SMILES-to-mass-spectrum feature encoding module within PS2MS
- Task kind: `component_reconstruction`
- Task: Convert candidate NPS chemical structures from SMILES notation into the encoded feature representation consumed by the PS2MS deep learning model. Produce a feature matrix suitable for direct input to the model's neural network layers.
- Inputs:
  - SMILES strings of candidate NPS compounds (plain text or CSV with SMILES column)
- Expected outputs:
  - Encoded feature matrix (NumPy array or HDF5 format) with shape [n_compounds, n_features] ready for PS2MS model input
- Tools: RDKit
- Landmark output files: smiles_validated.csv, molecular_graphs.pkl, feature_matrix_raw.npy
- Primary expected artifact: `encoded_features.h5`

### Step `task_003`
- Depends on: `task_002`
- Title: Analyze the relationship between predicted PS2MS scores and structural novelty of NPS compounds
- Task kind: `analysis`
- Task: Re-analyze PS2MS model prediction confidence scores across structurally diverse and novel NPS analogues from the paper's evaluation set to characterize how confidence varies with structural novelty.
- Inputs:
  - PS2MS trained model and evaluation dataset from jhhung/PS2MS GitHub repository
- Expected outputs:
  - Table of prediction confidence score statistics (mean, median, std, min, max, quartiles) stratified by structural novelty category
  - Visualization (box plot or violin plot) of confidence score distributions across structural novelty strata
- Tools: Python deep learning framework (PyTorch or TensorFlow), RDKit or similar cheminformatics library for molecular fingerprint computation, Matplotlib or Seaborn for visualization, Pandas for tabular data manipulation and aggregation
- Landmark output files: model_predictions.csv, structural_similarity_scores.csv, confidence_by_novelty_stratum.csv, confidence_distribution_plot.png
- Primary expected artifact: `confidence_score_analysis.csv`

## Final expected outputs

- `Table of prediction confidence score statistics (mean, median, std, min, max, quartiles) stratified by structural novelty category` (type: file, tolerance: hash)
- `Visualization (box plot or violin plot) of confidence score distributions across structural novelty strata` (type: file, tolerance: hash)

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
  "workflow_id": "coll_ps2ms_workflow",
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
    "Table of prediction confidence score statistics (mean, median, std, min, max, quartiles) stratified by structural novelty category": "<locator>",
    "Visualization (box plot or violin plot) of confidence score distributions across structural novelty strata": "<locator>"
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
