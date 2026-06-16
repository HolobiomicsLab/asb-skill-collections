# Workflow Challenge: `coll_mistcf_workflow`


> MIST-CF ranks chemical formula and adduct assignments for unknown mass spectra in a de novo setting using a formula transformer neural network with an internal subformula assignment protocol and sinusoidal formula embeddings, without requiring spectrum databases or external fragmentation trees.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

MIST-CF extends the MIST framework for annotating MS1 precursor masses from MS/MS data by employing an internal chemical subformula assignment protocol as an alternative to SIRIUS fragmentation trees, enabling the formula transformer neural network to assign subformulas to peaks in a data-dependent fashion. The model incorporates sinusoidal formula embeddings, a technique developed in prior work (SCARF), as an advance to the chemical formula transformer architecture for improved representation of chemical formulas. MIST-CF considers multiple adduct types beyond [M+H]+ in positive mode ionization, ranking both chemical formula and adduct assignments using an end-to-end energy-based modeling approach without referencing any spectrum databases.

## Research questions

- How does MIST-CF's end-to-end energy-based formula transformer perform on ranking chemical formula and adduct assignments compared to SIRIUS-based approaches on benchmark MS/MS data?
- How does MIST-CF assign chemical subformulas to MS/MS fragment peaks without relying on SIRIUS fragmentation trees?
- What is the performance improvement in chemical formula ranking accuracy when MIST-CF incorporates support for multiple adduct types compared to restricting predictions to [M+H]+ only?
- How are sinusoidal formula embeddings implemented as a component of the MIST-CF chemical formula transformer architecture?
- Can the MIST-CF formula transformer architecture be extended to support negative-mode adducts, and what is the resulting top-k formula ranking accuracy on negative-mode MS/MS spectra?

## Methods overview

Load benchmark MS/MS dataset with ground-truth chemical formula annotations and precursor m/z values. Preprocess MS/MS spectra by normalizing intensities, filtering low-intensity noise, and extracting fragment m/z and intensity pairs. Execute MIST-CF formula transformer neural network on preprocessed spectra to generate energy-scored ranked lists of candidate chemical formulas and associated adduct assignments for each spectrum. Compute top-k accuracy metrics (top-1, top-3, top-k) by checking whether the ground-truth formula and adduct appear in the ranked prediction list. Run SIRIUS on the same benchmark dataset using internal chemical subformula assignment protocol and extract its ranked formula predictions. Compare MIST-CF and SIRIUS top-k accuracy scores to reproduce reported performance advantage. Validation: top-k accuracy for MIST-CF formula assignment must be reproducible and rank performance metrics must match or exceed reported baselines in the paper. References: source article (DOI: 10.1021/acs.jcim.3c01082) Load MS/MS test spectra with reference precursor masses and ground-truth subformula annotations. Apply MIST-CF internal subformula assignment (formula transformer neural network) to rank candidate subformulas for each fragment peak without invoking SIRIUS or external databases. Generate per-peak subformula predictions conditioned on precursor formula and observed m/z. Compute per-peak accuracy, exact-match rate per spectrum, and top-k ranking statistics. Validation: Accept predictions if per-peak accuracy and exact-match rates meet or exceed reported benchmark thresholds on the held-out set. References: source article (DOI: 10.1021/acs.jcim.3c01082) Load the published benchmark dataset with ground-truth MS/MS spectra, chemical formulas, and adduct assignments. Configure MIST-CF to restrict predictions to [M+H]+ only (disabling multi-adduct support) and run inference on all benchmark spectra. Configure MIST-CF to enable full multi-adduct support and run inference on the same spectra using energy-based ranking. Compute top-1 and top-k ranking accuracy for both modes (correct formula-adduct pair at rank 1 and within top-k). Calculate performance delta (multi-adduct accuracy minus [M+H]+-only accuracy) to quantify MULTI_ADDUCT_SUPPORT contribution. Validation: Report ranking accuracy metrics and delta with per-spectrum results; confirm multi-adduct and [M+H]+-only runs use identical spectral input and hyperparameters. References: source article (DOI: 10.1021/acs.jcim.3c01082) Load the MIST-CF sinusoidal formula embedding layer from the official repository. Prepare a representative set of chemical formulas for embedding. Compute embedding vectors by invoking the embedding layer forward pass on each formula. Verify embedding dimensionality matches the configured parameter. Verify all embedding values fall within the expected range [-1, 1]. Compare produced embeddings against reference outputs from the repository to confirm numerical reproducibility within tolerance. Validation: embeddings match reference outputs with L2 distance < 1e-6 and all values are in [-1, 1]. References: source article (DOI: 10.1021/acs.jcim.3c01082) Load negative-mode MS/MS spectra with annotated formulas from a public repository (MassIVE or MetaboLights). Preprocess and normalize spectra, filtering by quality thresholds. Extend MIST-CF's adduct layer to tokenize common negative-mode adducts ([M-H]−, [M+Cl]−, [M+FA]−). Fine-tune the formula transformer neural network on negative-mode training data, preserving sinusoidal embeddings. Evaluate on held-out negative-mode test set and compute top-k ranking accuracy. Validation: Report top-1, top-5, and top-10 formula ranking accuracy; success threshold is comparable or improved performance relative to positive-mode baseline. References: source article (DOI: 10.1021/acs.jcim.3c01082)

**Domain:** cheminformatics

**Techniques:** tandem-ms, machine-learning, in-silico-fragmentation, deep-learning, metabolite-identification

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** MIST-CF is an extension of MIST for annotating MS1 precursor masses from MS/MS data in a de novo setting. _[grounded: MIST_CF_SYSTEM]_
- **(finding)** MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach. _[grounded: MIST_CF_SYSTEM]_
- **(finding)** MIST-CF does not reference any spectrum databases in its approach. _[grounded: MIST_CF_SYSTEM]_
- **(finding)** MIST-CF adopts a formula transformer neural network architecture. _[grounded: MIST_CF_SYSTEM]_
- **(finding)** MIST-CF learns in a data dependent fashion instead of computing fragmentation trees. _[grounded: MIST_CF_SYSTEM]_
- **(finding)** MIST-CF utilizes an internal chemical subformula assignment protocol rather than SIRIUS fragmentation trees. _[grounded: MIST_CF_SYSTEM]_
- **(finding)** MIST-CF considers multiple adduct types beyond [M+H]+ in positive mode. _[grounded: MIST_CF_SYSTEM]_
- **(finding)** MIST-CF utilizes sinusoidal formula embeddings as developed in the prior work SCARF. _[grounded: MIST_CF_SYSTEM]_

## Sanctioned method substitutions
Using any of these instead of the source method is **not penalized**:
- SIRIUS fragmentation trees can be replaced with internal chemical subformula assignment protocol

## Invariants (must not change)
Changing any of these **is** a failure regardless of openness:
- MIST-CF operates only in positive mode

## Steps

### Step `task_001`
- Title: Reproduce MIST-CF formula and adduct ranking performance versus SIRIUS baseline
- Task kind: `reproduction`
- Task: Run MIST-CF's end-to-end energy-based formula transformer on a benchmark MS/MS dataset to rank chemical formula and adduct assignments. Reproduce reported top-k accuracy metrics and comparison against SIRIUS baseline.
- Inputs:
  - Benchmark MS/MS dataset with unknown spectra and ground-truth chemical formula annotations
- Expected outputs:
  - Top-k accuracy scores (top-1, top-3, top-k) for MIST-CF chemical formula and adduct assignments
  - Comparative ranking performance table: MIST-CF vs SIRIUS baseline metrics
  - Ranked candidate formula predictions with confidence scores for benchmark dataset
- Tools: MIST, MIST-CF, SIRIUS, SCARF
- Landmark output files: preprocessed_benchmark_spectra.mzML, mist_cf_ranked_candidates.csv, sirius_ranked_candidates.csv, top_k_accuracy_comparison.csv, ranking_performance_plot.png
- Primary expected artifact: `mist_cf_benchmark_results.csv`

### Step `task_002`
- Depends on: `task_001`
- Title: Reconstruct the internal chemical subformula assignment protocol replacing SIRIUS fragmentation trees
- Task kind: `component_reconstruction`
- Task: Implement the internal subformula assignment component of MIST-CF that assigns chemical subformulas to MS/MS fragment peaks without invoking SIRIUS fragmentation trees. Evaluate the per-peak subformula label predictions on a held-out test set of spectra and report accuracy metrics.
- Inputs:
  - MS/MS spectra with annotated MS1 precursor masses and ground-truth subformula labels for held-out test set
- Expected outputs:
  - Per-peak subformula predictions as a structured table (peak m/z, predicted subformula, rank, confidence score)
  - Evaluation metrics table including per-peak accuracy, exact-match rate per spectrum, and top-k ranking statistics
- Tools: MIST, MIST-CF, SCARF
- Landmark output files: parsed_test_spectra.json, subformula_predictions_ranked.csv, evaluation_metrics.json
- Primary expected artifact: `subformula_predictions.csv`

### Step `task_003`
- Depends on: `task_001`
- Title: Analyze the impact of multi-adduct support on formula ranking accuracy
- Task kind: `analysis`
- Task: Evaluate MIST-CF formula-ranking accuracy on a published benchmark dataset comparing [M+H]+ only predictions versus multi-adduct predictions, quantifying the contribution of the MULTI_ADDUCT_SUPPORT component to ranking performance.
- Inputs:
  - Published benchmark dataset with MS/MS spectra, ground-truth chemical formulas, and adduct annotations
- Expected outputs:
  - CSV or JSON table with per-spectrum ranking accuracy results for [M+H]+-only and multi-adduct modes
  - Numerical comparison report quantifying the performance contribution of MULTI_ADDUCT_SUPPORT (delta in top-1 and top-k accuracy)
- Tools: MIST, MIST-CF
- Landmark output files: mist_cf_predictions_[M+H]_only.json, mist_cf_predictions_multi_adduct.json, ranking_accuracy_metrics.csv
- Primary expected artifact: `adduct_ablation_comparison.csv`

### Step `task_004`
- Depends on: `task_001`
- Title: Reconstruct sinusoidal formula embeddings from the SCARF component within MIST-CF
- Task kind: `component_reconstruction`
- Task: Implement the sinusoidal formula embedding layer as used in MIST-CF and verify that embedding vectors produced for a set of chemical formulas match expected numerical properties (dimensionality, value range, reproducibility) against reference outputs from the MIST-CF repository.
- Inputs:
  - MIST-CF repository (samgoldman97/mist-cf) containing sinusoidal formula embedding implementation
  - Representative set of chemical formulas for embedding verification (e.g., C6H12O6, C3H7NO2, C8H10N4O2)
- Expected outputs:
  - Embedding vectors for each input chemical formula with shape (num_formulas, embedding_dimension)
  - Validation report confirming dimensionality, value range, and reproducibility against reference outputs
- Tools: MIST, SCARF, MIST-CF
- Landmark output files: embedding_vectors.csv, validation_metrics.json, reproducibility_check.log
- Primary expected artifact: `embedding_validation_report.json`

### Step `task_005`
- Depends on: `task_001`
- Title: Extend MIST-CF multi-adduct support to negative ionisation mode
- Task kind: `extension`
- Task: Extend MIST-CF's MULTI_ADDUCT_SUPPORT to handle negative-mode adducts (e.g., [M-H]−) by fine-tuning the formula transformer on negative-mode MS/MS spectra from a public dataset, and report top-k formula ranking accuracy metrics.
- Inputs:
  - Negative-mode MS/MS spectra with annotated molecular formulas and adduct assignments from a public dataset (MassIVE or MetaboLights)
  - Pretrained MIST-CF model checkpoint with positive-mode formula transformer weights
- Expected outputs:
  - Fine-tuned MIST-CF model checkpoint with negative-mode adduct support
  - Top-k formula ranking accuracy metrics (top-1, top-5, top-10) on negative-mode test set, reported as accuracy_metrics.csv
- Tools: MIST, SCARF
- Landmark output files: negative_mode_spectrum_preprocessing_log.txt, adduct_tokenization_config.json, finetuned_model_checkpoint.pt, test_set_predictions.csv, accuracy_metrics.csv
- Primary expected artifact: `accuracy_metrics.csv`

## Final expected outputs

- `Per-peak subformula predictions as a structured table (peak m/z, predicted subformula, rank, confidence score)` (type: file, tolerance: hash)
- `Evaluation metrics table including per-peak accuracy, exact-match rate per spectrum, and top-k ranking statistics` (type: file, tolerance: hash)
- `CSV or JSON table with per-spectrum ranking accuracy results for [M+H]+-only and multi-adduct modes` (type: file, tolerance: hash)
- `Numerical comparison report quantifying the performance contribution of MULTI_ADDUCT_SUPPORT (delta in top-1 and top-k accuracy)` (type: file, tolerance: hash)
- `Embedding vectors for each input chemical formula with shape (num_formulas, embedding_dimension)` (type: file, tolerance: hash)
- `Validation report confirming dimensionality, value range, and reproducibility against reference outputs` (type: file, tolerance: hash)
- `Fine-tuned MIST-CF model checkpoint with negative-mode adduct support` (type: file, tolerance: hash)
- `Top-k formula ranking accuracy metrics (top-1, top-5, top-10) on negative-mode test set, reported as accuracy_metrics.csv` (type: file, tolerance: hash)

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
  "workflow_id": "coll_mistcf_workflow",
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
    "Per-peak subformula predictions as a structured table (peak m/z, predicted subformula, rank, confidence score)": "<locator>",
    "Evaluation metrics table including per-peak accuracy, exact-match rate per spectrum, and top-k ranking statistics": "<locator>",
    "CSV or JSON table with per-spectrum ranking accuracy results for [M+H]+-only and multi-adduct modes": "<locator>",
    "Numerical comparison report quantifying the performance contribution of MULTI_ADDUCT_SUPPORT (delta in top-1 and top-k accuracy)": "<locator>",
    "Embedding vectors for each input chemical formula with shape (num_formulas, embedding_dimension)": "<locator>",
    "Validation report confirming dimensionality, value range, and reproducibility against reference outputs": "<locator>",
    "Fine-tuned MIST-CF model checkpoint with negative-mode adduct support": "<locator>",
    "Top-k formula ranking accuracy metrics (top-1, top-5, top-10) on negative-mode test set, reported as accuracy_metrics.csv": "<locator>"
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
