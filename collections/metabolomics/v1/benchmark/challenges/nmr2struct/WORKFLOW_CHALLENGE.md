# Workflow Challenge: `coll_nmr2struct_workflow`


> This benchmark reproduces an end-to-end multitask machine learning model that predicts molecular structure from 1D NMR spectra by integrating a convolutional neural network with a transformer architecture, and analyzes performance across different NMR input modalities.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 4-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

The paper introduces a multitask machine learning framework for rapid molecular structure elucidation from routine one-dimensional NMR spectra, addressing the combinatorial challenge of structure determination from limited spectroscopic data. The framework integrates a convolutional neural network with a transformer architecture designed to efficiently assemble molecular fragments into complete structures, automating a task traditionally performed manually by chemists. This benchmark reproduces the reported end-to-end structure prediction capability on molecules up to 19 heavy atoms and analyzes how performance varies when using ¹H NMR spectra alone, ¹³C NMR spectra alone, or combined 1D NMR inputs. The transformer fragment assembler mechanism is reconstructed as described in the paper to understand its role in the combinatorial assembly process. Additionally, the benchmark explores the framework's generalization beyond the demonstrated scope of 19 heavy atoms, establishing the known performance boundary of the original work.

## Research questions

- What are the exact structure recovery accuracy metrics achieved by the end-to-end NMR2Struct model on test molecules containing up to 19 heavy atoms?
- How does the transformer architecture assemble molecular fragments into candidate molecular structures?
- How do the individual contributions of ¹H NMR, ¹³C NMR, and their combination differ in accuracy for molecular structure elucidation using the multitask machine learning framework?
- Does the NMR2Struct model maintain accurate structure recovery performance when applied to molecules with more than 19 heavy atoms, or does accuracy degrade significantly beyond this training scope?

## Methods overview

Load and preprocess test set 1D NMR spectra (1H and/or 13C) for molecules with ≤19 heavy atoms. Encode spectra into feature vectors using the trained convolutional neural network encoder. Feed encoded features into the transformer fragment assembler to predict molecular fragments and connectivity graph. Perform multitask decoding to generate both molecular formula and connectivity predictions. Rank predicted structures and compute top-k exact structure recovery rates by comparing against ground-truth structures. Validation: Accuracy metrics (top-1, top-5 exact recovery rates) match or reproduce the paper's reported performance on the test set. Prepare fragment-structure ground truth pairs from the deposited dataset. Design and implement transformer encoder-decoder architecture to map fragment sets to assembled structures. Train the transformer on fragment-structure pairs using structure prediction loss. Evaluate assembly accuracy on held-out test pairs using exact-match and partial-correctness metrics. Validation: Achieve measurable fragment assembly accuracy on molecules up to 19 heavy atoms, with documented success/failure patterns by structural class. Load trained NMR2Struct model (CNN encoder + transformer decoder) and test set spectra–structure pairs. Partition test inputs into three modality conditions: 1H-only, 13C-only, and 1H+13C combined, preserving ground-truth labels. Run inference through CNN + transformer on each modality condition to generate structure predictions. Compute accuracy metrics (exact-match formula accuracy, connectivity matching) for each modality. Calculate individual contribution (per-modality accuracy) and joint contribution (combined accuracy minus single-modality baseline). Validation: accuracy values are compared side-by-side and reported in a structured table; synergy is confirmed by combined > max(1H, 13C) or reported as null if absent. Load the pretrained transformer + CNN NMR2Struct model from checkpoint Retrieve or construct a held-out test set of molecules with >19 heavy atoms from PubChem or equivalent database Obtain 1D ¹H and/or ¹³C NMR spectra for each out-of-scope molecule Generate ranked predictions of molecular formula and connectivity for each spectrum Compute top-1, top-3, and top-5 structure recovery accuracy on out-of-scope test set Compare out-of-scope accuracy to reported in-scope baseline (≤19 heavy atoms) and quantify absolute and relative degradation Validation: verify that reported accuracy metrics for in-scope and out-of-scope conditions are reproducible and documented, and that degradation is quantified against the published baseline

**Domain:** cheminformatics

**Techniques:** nmr, deep-learning, machine-learning, transformer-model

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** Rapid determination of molecular structures can greatly accelerate workflows across many chemical disciplines.
- **(finding)** Elucidating structure using only one-dimensional NMR spectra remains an extremely challenging problem because of the combinatorial explosion of the number of possible molecules as the number of constituent atoms is increased.
- **(finding)** A multitask machine learning framework can predict molecular structure (formula and connectivity) from 1D ¹H and/or ¹³C NMR spectra. _[grounded: MultitaskLearningFramework]_
- **(finding)** A transformer architecture can be constructed to efficiently solve the task of assembling large numbers of molecular fragments into molecular structures.
- **(finding)** The framework demonstrates effectiveness on molecules with up to 19 heavy (non-hydrogen) atoms.

**Speculative claims (excluded from scoring):**
- **(finding)** For molecules with up to 19 heavy atoms, there are trillions of possible structures.

## Steps

### Step `task_001`
- Title: Reproduce end-to-end structure prediction accuracy on molecules up to 19 heavy atoms from 1D NMR spectra
- Task kind: `reproduction`
- Task: Run the NMR2Struct pipeline (CNN spectra encoder + transformer fragment assembler) on the test set of molecules with up to 19 heavy atoms and reproduce the reported top-k exact structure recovery accuracy metrics.
- Inputs:
  - Test set NMR spectra (1D 1H and/or 13C) for molecules with up to 19 heavy atoms
  - Ground-truth molecular structures (formula and connectivity) for test set molecules
- Expected outputs:
  - Top-k exact structure recovery accuracy metrics (e.g., top-1, top-5 accuracy rates)
  - Predicted molecular structures (formula and connectivity) for test set compounds
- Tools: convolutional neural network, transformer architecture
- Landmark output files: encoded_spectra.pkl, predicted_candidates.csv, top_k_accuracy.json
- Primary expected artifact: `structure_recovery_metrics.json`

### Step `task_002`
- Depends on: `task_001`
- Title: Reconstruct the Transformer Fragment Assembler for combinatorial fragment-to-structure assembly
- Task kind: `component_reconstruction`
- Task: Reconstruct and evaluate a transformer-based fragment assembly module that assembles molecular fragments into candidate structures. Validate assembly accuracy on fragment-structure pairs derived from the deposited dataset.
- Inputs:
  - Deposited dataset containing molecular structures and fragmentation patterns
- Expected outputs:
  - Trained transformer fragment assembly model weights and configuration
  - Fragment assembly accuracy metrics (exact match rate, partial correctness scores)
  - Test set predictions and evaluation report
- Tools: transformer architecture
- Landmark output files: fragment_structure_pairs.json, model_checkpoint.pt, train_test_split.json, assembly_predictions.csv
- Primary expected artifact: `fragment_assembly_evaluation.csv`

### Step `task_003`
- Depends on: `task_001`
- Title: Analyze the effect of using only 1H NMR vs. only 13C NMR vs. combined 1D NMR inputs on structure prediction performance
- Task kind: `analysis`
- Task: Using the trained NMR2Struct multitask model on its test set, evaluate structure elucidation accuracy separately for 1H-only, 13C-only, and 1H+13C combined input modalities to quantify the individual and synergistic contributions of each spectrum type to prediction performance.
- Inputs:
  - Trained NMR2Struct model (transformer + CNN architecture checkpoint)
  - Test set: molecular structures with paired 1H and 13C NMR spectra
- Expected outputs:
  - Accuracy comparison table (modality × accuracy metrics) for 1H-only, 13C-only, and combined conditions
  - Quantified individual and joint contribution scores (e.g., absolute accuracy per modality and synergy gain)
- Tools: transformer architecture, convolutional neural network
- Landmark output files: 1h_predictions.json, 13c_predictions.json, combined_predictions.json, accuracy_per_modality.csv
- Primary expected artifact: `modality_accuracy_comparison.csv`

### Step `task_004`
- Depends on: `task_001`
- Title: Extend NMR2Struct structure prediction to molecules beyond 19 heavy atoms
- Task kind: `extension`
- Task: Apply a pretrained NMR2Struct model to a held-out test set of molecules with >19 heavy atoms from a public chemical database (PubChem or equivalent), and quantify the degradation in top-k structure recovery accuracy relative to the in-scope (≤19 heavy atom) baseline condition.
- Inputs:
  - Pretrained or fine-tuned NMR2Struct model checkpoint (transformer + CNN weights)
  - Held-out test set of molecules exceeding 19 heavy atoms from PubChem or equivalent public chemical database
  - 1D ¹H and/or ¹³C NMR spectra for out-of-scope molecules (experimental or simulated)
  - In-scope baseline accuracy metrics (top-k structure recovery for molecules ≤19 heavy atoms)
- Expected outputs:
  - Top-1, top-3, and top-5 structure recovery accuracy scores for out-of-scope molecules (>19 heavy atoms)
  - Comparative accuracy degradation table (out-of-scope vs. in-scope baseline, absolute and relative loss)
  - Summary report documenting failure modes, error distribution, and molecular size/complexity thresholds at which model performance drops significantly
- Tools: transformer architecture, convolutional neural network
- Landmark output files: oos_predictions.json, oos_top_k_accuracy.csv, degradation_baseline_comparison.csv, failure_mode_analysis.txt
- Primary expected artifact: `oos_accuracy_degradation_report.csv`

## Final expected outputs

- `Trained transformer fragment assembly model weights and configuration` (type: file, tolerance: hash)
- `Fragment assembly accuracy metrics (exact match rate, partial correctness scores)` (type: file, tolerance: hash)
- `Test set predictions and evaluation report` (type: file, tolerance: hash)
- `Accuracy comparison table (modality × accuracy metrics) for 1H-only, 13C-only, and combined conditions` (type: file, tolerance: hash)
- `Quantified individual and joint contribution scores (e.g., absolute accuracy per modality and synergy gain)` (type: file, tolerance: hash)
- `Top-1, top-3, and top-5 structure recovery accuracy scores for out-of-scope molecules (>19 heavy atoms)` (type: file, tolerance: hash)
- `Comparative accuracy degradation table (out-of-scope vs. in-scope baseline, absolute and relative loss)` (type: file, tolerance: hash)
- `Summary report documenting failure modes, error distribution, and molecular size/complexity thresholds at which model performance drops significantly` (type: file, tolerance: hash)

## How your attempt will be scored

ASB defines seven rubrics in `workflow_rubric.py` (STEP_ORDERING, INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT, TOOL_SELECTION, EFFICIENCY, CLAIM_VALIDATION, ADVERSARIAL_TRAP_AVOIDANCE). Which of them bind for *this* challenge depends on the tier and openness below.

### Tier evaluation profile

**Evaluator:** automated — filesystem presence + type-port resolution; END_TO_END_OUTPUT with declared per-output tolerance.
**Binding rubrics:** STEP_ORDERING, END_TO_END_OUTPUT (typed/tolerance), TOOL_SELECTION, CLAIM_VALIDATION.

### Openness stance

**Openness: closed — reproduction-first.** The deterministic rubrics above bind. A different method is acceptable ONLY if it appears under *Sanctioned method substitutions*; outputs are compared with the declared tolerance. Different is wrong here only when it departs from the sanctioned set or breaks an invariant.

## Workflow characterisation

_Suter et al. 2025 (DOI 10.1016/j.future.2025.107974)._

- **Coupling:** tight

- **Composition modularity:** hierarchical

- **Abstraction level:** intermediate

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
  "workflow_id": "coll_nmr2struct_workflow",
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
    "Trained transformer fragment assembly model weights and configuration": "<locator>",
    "Fragment assembly accuracy metrics (exact match rate, partial correctness scores)": "<locator>",
    "Test set predictions and evaluation report": "<locator>",
    "Accuracy comparison table (modality \u00d7 accuracy metrics) for 1H-only, 13C-only, and combined conditions": "<locator>",
    "Quantified individual and joint contribution scores (e.g., absolute accuracy per modality and synergy gain)": "<locator>",
    "Top-1, top-3, and top-5 structure recovery accuracy scores for out-of-scope molecules (>19 heavy atoms)": "<locator>",
    "Comparative accuracy degradation table (out-of-scope vs. in-scope baseline, absolute and relative loss)": "<locator>",
    "Summary report documenting failure modes, error distribution, and molecular size/complexity thresholds at which model performance drops significantly": "<locator>"
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
