# Workflow Challenge: `coll_cmmrt_workflow`


> This benchmark reproduces machine learning methods for accurate retention time prediction in chromatography, including a heavily regularized deep neural network achieving 39.2±1.2 s mean absolute error and a Bayesian meta-learning approach for retention time projection between chromatographic methods using minimal calibration data.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

The paper presents methods for predicting retention times in chromatographic analysis using machine learning trained on 80,038 experimental RTs from the METLIN dataset. A heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging achieved mean absolute error of 39.2±1.2 s and median absolute error of 17.2 ± 0.9 s on the SMRT dataset. Analysis of different feature types—molecular descriptors, fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints), and combinations thereof—shows that fingerprints tend to perform better than descriptors alone. The paper proposes a Bayesian meta-learning approach that enables retention time projection between chromatographic methods using as few as 10 calibration molecules while maintaining competitive error rates relative to previous projection methods. The DNN and meta-learning components are intended for integration into a probabilistic metabolite annotation framework.

## Research questions

- What is the predictive performance of a heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging on retention time prediction using the METLIN SMRT dataset?
- Do fingerprints outperform molecular descriptors alone when training machine learning models for retention time prediction on the METLIN SMRT dataset?
- How does the Bayesian meta-learning approach enable retention time projection between different chromatographic methods using minimal calibration data?
- Can a Bayesian meta-learning approach achieve competitive retention time prediction error rates when calibrated with only 10 molecules across different chromatographic methods?
- How can DNN-predicted retention times be combined with meta-learned chromatographic projections to generate probabilistic likelihood scores for ranking candidate metabolite annotations?

## Methods overview

Load SMRT dataset (80,038 molecules with experimental retention times from METLIN). Generate 5,666 descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, Path) using alvaDesc. Construct feature matrices combining descriptors and fingerprints; split into train/validation/test sets. Train heavily regularized DNN with cosine annealing warm restarts scheduling and stochastic weight averaging. Evaluate on test set and compute mean absolute error and median absolute error with uncertainties. Validation: output MAE = 39.2±1.2 s and MdAE = 17.2±0.9 s matches reported values within reported standard deviations. References: source article (DOI: 10.1186/s13321-022-00613-8) Load SMRT dataset with 80,038 experimental retention times and molecular structures. Generate 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, Path) using alvaDesc. Train heavily regularized DNN with cosine annealing warm restarts and stochastic weight averaging on three feature conditions: descriptors-only, fingerprints-only, and combined. Evaluate each model using mean absolute error (MAE) and median absolute error (MdAE) on held-out test set. Validation: Confirm that fingerprints-only achieves lower MAE and MdAE than descriptors-only, and comparable or superior performance to combined features, matching reported findings of fingerprint superiority. References: source article (DOI: 10.1186/s13321-022-00613-8) Load the pre-trained DNN model trained on METLIN SMRT data with 80,038 experimental retention times Generate molecular fingerprints (MACCS166, Extended Connectivity, Path Fingerprints) for calibration and test molecules using alvaDesc Extract latent feature representations from the pre-trained DNN for calibration and test sets Fit a Bayesian meta-learning projection model using 10 calibration molecules to map external chromatographic RT space to DNN latent space Generate RT predictions for test set by projecting through learned mapping and DNN regression head Validation: calculate mean and median absolute errors on test predictions, confirming competitive error rates against base DNN benchmarks (MAE 39.2±1.2 s, MedAE 17.2±0.9 s) References: source article (DOI: 10.1186/s13321-022-00613-8) Load the METLIN SMRT dataset (80,038 experimental retention times with pre-computed molecular descriptors and fingerprints). Apply the Bayesian meta-learning projection model (cond_meta_learning_10mol) with 10 calibration molecules to project retention times across chromatographic methods. Calculate mean absolute error (MAE) and median absolute error (MdAE) between predicted and experimental retention times. Tabulate results with confidence intervals and compare against baseline projection approach metrics (MAE ~39.2±1.2 s, MdAE ~17.2±0.9 s). Validation: Verify that the Bayesian meta-learning approach achieves error rates competitive with (or better than) reported baseline projections while using only 10 calibration molecules, with MAE and MdAE within the confidence bounds reported for the original model. References: source article (DOI: 10.1186/s13321-022-00613-8) Generate molecular descriptors and fingerprints (MACCS166, Extended Connectivity, Path) for each candidate structure using alvaDesc. Apply trained DNN regression model to predict retention times and extract prediction uncertainty from model outputs. Use Bayesian meta-learning to project predicted RTs from reference chromatographic method to target method using calibration molecules (≥10). Convert projected RTs and uncertainties into normalized RT-based likelihood scores (probability density function). Rank candidates by RT likelihood score and output ranked list with scores. Validation: Confirm ranked list contains all input candidates, RT scores sum to or normalize appropriately, and no candidate has missing or NaN likelihood value. References: source article (DOI: 10.1186/s13321-022-00613-8)

**Domain:** metabolomics

**Techniques:** retention-time-prediction, machine-learning, metabolite-identification, database-annotation, deep-learning

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** The CMM-RT code implements methods for accurate prediction of Retention Times for a given Chromatographic Method using machine learning. _[grounded: system_cmmrt]_
- **(finding)** State-of-the-art machine learning regressors were trained using 80,038 experimental RTs from the METLIN small molecule dataset. _[grounded: dataset_smrt]_
- **(finding)** Both retained and unretained molecules were considered in the training dataset.
- **(finding)** 5,666 molecular descriptors were generated with the alvaDesc software. _[grounded: tool_alvadesc]_
- **(finding)** 2,214 fingerprints were generated with the alvaDesc software. _[grounded: tool_alvadesc]_
- **(finding)** The fingerprints used were MACCS166, Extended Connectivity, and Path Fingerprints. _[grounded: component_maccs166]_
- **(finding)** Models were trained using only the descriptors, only the fingerprints, and both types of features simultaneously.
- **(finding)** Fingerprints tend to perform better than descriptors or combined features for retention time prediction.
- **(finding)** A heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging achieved mean absolute error of 39.2±1.2 s. _[grounded: metric_mae_mean]_
- **(finding)** A heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging achieved median absolute error of 17.2 ± 0.9 s. _[grounded: metric_mae_median]_
- **(finding)** A novel Bayesian meta-learning approach is proposed for RT projection between CMs.
- **(finding)** The Bayesian meta-learning approach requires as few as 10 molecules for RT projection between chromatographic methods.
- **(finding)** The meta-learning approach obtains competitive error rates compared with previous approaches.
- **(finding)** The proposed DNN and meta-learned projections can be integrated into metabolite annotation workflows.

## Steps

### Step `task_001`
- Title: Reproduce DNN mean and median absolute error on SMRT dataset
- Task kind: `reproduction`
- Task: Train a heavily regularized deep neural network with cosine annealing warm restarts and stochastic weight averaging on the SMRT dataset using molecular descriptors and fingerprints to predict retention time, and reproduce the reported mean absolute error of 39.2±1.2 s and median absolute error of 17.2±0.9 s.
- Inputs:
  - SMRT dataset with 80,038 experimental retention times and molecular structures from METLIN small molecule dataset
- Expected outputs:
  - Trained DNN model checkpoint and retention time predictions on test set
  - Performance metrics: mean absolute error of 39.2±1.2 s and median absolute error of 17.2±0.9 s
- Tools: alvaDesc
- Landmark output files: descriptors_fingerprints.npz, train_val_test_split.json, dnn_model_checkpoint.h5, predictions_metrics.csv
- Primary expected artifact: `dnn_model_predictions.csv`

### Step `task_002`
- Title: Analyze fingerprints-only vs descriptors-only vs combined feature sets on SMRT retention time prediction
- Task kind: `analysis`
- Task: Train and compare three machine learning models (descriptors-only, fingerprints-only, and combined) on the SMRT dataset using alvaDesc-generated features to verify that fingerprints outperform descriptors for retention time prediction.
- Inputs:
  - SMRT dataset with 80,038 experimental retention times and molecular structures
- Expected outputs:
  - Model performance comparison table with mean and median absolute errors for descriptors-only, fingerprints-only, and combined feature models
  - Trained regression model weights and architecture specification
- Tools: alvaDesc
- Landmark output files: descriptors.csv, fingerprints.csv, combined_features.csv, descriptors_model_metrics.json, fingerprints_model_metrics.json, combined_model_metrics.json
- Primary expected artifact: `performance_comparison.csv`

### Step `task_003`
- Depends on: `task_001`
- Title: Reconstruct the Bayesian meta-learning RT projection module
- Task kind: `component_reconstruction`
- Task: Implement a Bayesian meta-learning projection mechanism that maps retention times from an external chromatographic method onto the SMRT-trained DNN's latent space using as few as 10 calibration molecules, and generate projected RT predictions for a held-out test set.
- Inputs:
  - Pre-trained DNN model checkpoint trained on METLIN SMRT dataset (80,038 experimental retention times)
  - Calibration set: 10 molecules with measured retention times from external chromatographic method and corresponding structures
  - Held-out test set: molecules with experimental retention times from external chromatographic method and structures
- Expected outputs:
  - Projected RT predictions for test set molecules (CSV table with molecule identifiers, predicted RTs, reference RTs)
  - Performance metrics: mean absolute error and median absolute error comparing predicted vs. reference RTs
  - Fitted Bayesian meta-learning projection model (serialized model object)
- Tools: alvaDesc
- Landmark output files: calibration_fingerprints.csv, test_fingerprints.csv, calibration_latent_features.npy, test_latent_features.npy, projection_model.pkl, test_set_predictions.csv
- Primary expected artifact: `projected_rt_predictions.csv`

### Step `task_004`
- Depends on: `task_003`
- Title: Reproduce meta-learning projection competitive error rates with 10-molecule calibration sets
- Task kind: `reproduction`
- Task: Using the Bayesian meta-learning projection approach (cond_meta_learning_10mol), reproduce the competitive error rates achieved with only 10 calibration molecules and compare against reported baseline projection methods. Output a results table with error metrics and method comparisons.
- Inputs:
  - task_003.expected_outputs[0]: Projected RT predictions for test set molecules (CSV table with molecule identifiers, predicted RTs, reference RTs)
  - METLIN small molecule dataset (SMRT) with 80,038 experimental retention times and molecular features
  - Pre-trained Bayesian meta-learning model (cond_meta_learning_10mol) or access to training code from constantino-garcia/cmmrt repository
- Expected outputs:
  - Results table with error metrics (MAE, MdAE, and confidence intervals) comparing Bayesian meta-learning projection with 10 calibration molecules against baseline projection approaches
- Tools: alvaDesc
- Landmark output files: predictions_10mol_calibration.csv, baseline_projection_results.csv, error_metrics_summary.txt
- Primary expected artifact: `meta_learning_error_comparison.csv`

### Step `task_005`
- Depends on: `task_003`
- Title: Extend DNN+meta-learned projections integration for probabilistic metabolite annotation scoring
- Task kind: `extension`
- Task: Combine DNN-predicted retention times with meta-learned chromatographic projections to generate RT-based likelihood scores for candidate metabolite annotations. Produce a ranked candidate list with RT probability scores for a query spectrum.
- Inputs:
  - Query spectrum (m/z, intensity pairs) and neutral mass of unknown metabolite
  - Candidate metabolite structures (SMILES or InChI) from reference database (e.g., METLIN)
  - Trained DNN regression model (checkpoint) for retention time prediction
  - Bayesian meta-learning model for RT projection between chromatographic methods
  - Calibration molecules (≥10) with known RTs in both reference and target chromatographic methods
- Expected outputs:
  - Ranked candidate list with RT probability scores (CSV or TSV table: candidate_id, molecular_formula, predicted_rt, rt_score, rank)
- Tools: alvaDesc
- Landmark output files: candidate_fingerprints.csv, predicted_rts.csv, projected_rts.csv, rt_likelihood_scores.csv
- Primary expected artifact: `ranked_candidates_rt_scores.csv`

## Final expected outputs

- `Model performance comparison table with mean and median absolute errors for descriptors-only, fingerprints-only, and combined feature models` (type: file, tolerance: hash)
- `Trained regression model weights and architecture specification` (type: file, tolerance: hash)
- `Results table with error metrics (MAE, MdAE, and confidence intervals) comparing Bayesian meta-learning projection with 10 calibration molecules against baseline projection approaches` (type: file, tolerance: hash)
- `Ranked candidate list with RT probability scores (CSV or TSV table: candidate_id, molecular_formula, predicted_rt, rt_score, rank)` (type: file, tolerance: hash)

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
  "workflow_id": "coll_cmmrt_workflow",
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
    "Model performance comparison table with mean and median absolute errors for descriptors-only, fingerprints-only, and combined feature models": "<locator>",
    "Trained regression model weights and architecture specification": "<locator>",
    "Results table with error metrics (MAE, MdAE, and confidence intervals) comparing Bayesian meta-learning projection with 10 calibration molecules against baseline projection approaches": "<locator>",
    "Ranked candidate list with RT probability scores (CSV or TSV table: candidate_id, molecular_formula, predicted_rt, rt_score, rank)": "<locator>"
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
