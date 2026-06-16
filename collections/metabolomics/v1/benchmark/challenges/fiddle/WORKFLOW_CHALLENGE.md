# Workflow Challenge: `coll_fiddle_workflow`


> FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra. This repository provides the full research codebase for model training, evaluation, and paper reproduction.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

Reproduces 3 reported results: The provided document does not contain explicit reporting of dataset split counts (28,751 training and 3,195 test compounds) or details of the instrument allowlist fix methodology needed to verify this sub-task. The rescore model has been redesigned with a Siamese architecture in version 2.0.0, indicating a structural change to the model components that would affect encoder freezing and training behavior. The rescore model in FIDDLE v2.0.0 has been redesigned with a Siamese architecture, which is the operative inference architecture for the test. Reconstructs 2 described mechanisms (described in the paper but not separately evaluated there): The document does not provide explicit details about the prepare_augment_rescore.py script's operations, data augmentation procedures, or rescore training data generation mechanisms within the available text. The FIDDLE repository contains code for model training, evaluation, and paper reproduction, with full research codebase available for inspection of preprocessing steps including spectrum handling.

## Research questions

- Does applying the updated instrument allowlist fix (adding 'ftms' to gnps_orbitrap) to the dataset result in the reported training and test split counts of 28,751 and 3,195 compounds respectively?
- What data preparation operations does the prepare_augment_rescore.py script apply to TCN train and test sets before rescore model training?
- Does the rescore model training script freeze the TCN spectrum encoder and train only the FormulaEncoder and RescoreHead components?
- Does the FIDDLE v2.0.0 model with its redesigned Siamese rescore architecture successfully complete inference on GNPS caffeine spectra and produce scored molecular formula candidates?
- Is the precursor m/z value (env[:, 0]) consistently zeroed before spectrum encoding across the three main execution scripts in the FIDDLE codebase?

## Methods overview

Load raw GNPS spectral dataset with instrument metadata annotations. Update instrument allowlist configuration by adding 'ftms' to gnps_orbitrap category. Apply filtering logic to select compounds matching the updated allowlist. Execute train-test split using msfiddle preprocessing module with the corrected configuration. Extract training set size (target: 28,751) and test set size (target: 3,195) from split output. Validation: Verify training count equals 28,751 and test count equals 3,195 exactly; output passes if both counts match reported baseline. Load TCN train and test spectra with formula annotations. Cap the number of positive examples per molecular formula to enforce balance. Generate negative examples by pairing spectra within a precursor m/z window. Downsample combined positive and negative examples to 1:1 ratio. Validation: Output train and test sets conform to expected format and contain correct positive/negative counts and ratio. Load and freeze pre-trained TCN spectrum encoder to preserve learned spectral feature representations Initialize trainable FormulaEncoder and RescoreHead modules Train encoder and head modules using binary cross-entropy loss on annotated MS/MS spectra Monitor formula_acc (with H) on validation set after each epoch Save checkpoint only when validation formula_acc improves; serialize formula_encoder_state_dict and rescore_head_state_dict Validation: checkpoint is accepted when formula_acc (with H) on validation set reaches or exceeds reported baseline performance threshold Load the trained FIDDLE v2.0.0 model checkpoint from the zenodo deposit. Retrieve caffeine (C8H10N4O2) MS/MS spectra from the GNPS public library. Execute test_caffeine.py via the msfiddle Python API to perform inference on the spectra. Apply the Siamese rescore architecture to rank molecular formula candidates by prediction score. Validation: Output file exists, is a valid CSV or JSON, contains at least one scored formula candidate row, and inference script exits without error. Retrieve the three Python execution scripts (run_fiddle.py, train_rescore.py, test_caffeine.py) from the FIDDLE repository. Locate the preprocessing block in each script where the spectrum feature array (env) is prepared before TCN encoder input. Extract and document the exact code line(s) that set env[:, 0] to zero, including surrounding context and parameter names. Compare the implementation across all three scripts to verify that the zeroing operation is identical in index, operation type, and timing. Validation: Confirm that all three scripts implement env[:, 0] = 0 (or equivalent) consistently before TCN encoder invocation; report pass if all three match, fail if any divergence is found.

**Domain:** metabolomics

**Techniques:** molecular-networking, gnps-workflow, spectral-library-matching, database-annotation, metabolite-identification

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra. _[grounded: FIDDLE_system]_
- **(finding)** FIDDLE research was published in Nature Communications in 2025. _[grounded: FIDDLE_system]_
- **(finding)** A CLI and Python API for FIDDLE is available as msfiddle. _[grounded: FIDDLE_system]_
- **(finding)** The rescore model was redesigned with a Siamese architecture in version 2.0.0.
- **(finding)** Version 2.0.0 was released on 2026-03-23.
- **(finding)** An inference script for caffeine (C8H10N4O2) GNPS spectra was added in version 2.0.0. _[grounded: compound_caffeine]_
- **(finding)** An end-to-end retraining script for both Orbitrap and Q-TOF was added in version 2.0.0. _[grounded: compound_caffeine]_
- **(finding)** The train_rescore.py trainer freezes the TCN spectrum encoder and trains FormulaEncoder and RescoreHead with BCE loss. _[grounded: TCN_encoder]_
- **(finding)** The FormulaEncoder converts atom-count vectors to 512-dimensional L2-normalised embeddings. _[grounded: formula_encoder]_
- **(finding)** The RescoreHead performs element-wise product of spectrum and formula embeddings to produce a scalar logit. _[grounded: rescore_head]_
- **(finding)** An environment configuration file for macOS ARM64 (Apple Silicon) setup was added in version 2.0.0.
- **(finding)** Docstrings were added across multiple modules in version 2.0.0.
- **(finding)** FDRNet-based reranking was replaced with the Siamese rescore architecture. _[grounded: siamese_rescore_arch]_
- **(finding)** Output CSV columns were renamed from FDR (k) to Rescore (k).
- **(finding)** Precursor m/z is zeroed before the spectrum encoder to prevent the model from learning a mass-based frequency prior.
- **(finding)** The FDRNet class was removed from model_tcn.py. _[grounded: fdrnet]_
- **(finding)** The ftms instrument was added to the gnps_orbitrap instrument allowlist.
- **(finding)** The Orbitrap dataset was expanded to 28,751 training compounds.
- **(finding)** The Orbitrap dataset was expanded to 3,195 test compounds.
- **(finding)** The refine_atom_type function is now extended with atoms present in the predicted formula before calling formula_refinement.
- **(finding)** The refinement search space at training time now matches inference.
- **(finding)** Result export loading in train_tcn_gpus_cl.py was fixed to load from resume_path instead of checkpoint_path.
- **(finding)** Embeddings are L2-normalized before contrastive loss in train_tcn_gpus_cl.py.
- **(finding)** Gradient clipping with max_norm=1.0 was added to train_tcn_gpus_cl.py.
- **(finding)** Division by zero in H/C ratio target was fixed using y[:, 0].clamp(min=1) in train_tcn_gpus_cl.py.
- **(finding)** Checkpoints are saved only when formula_acc (with H) improves.
- **(finding)** Multi-scale feature collection now uses isinstance(layer, TemporalBlock) instead of i % 2 == 0. _[grounded: temporal_block]_
- **(finding)** Version 1.1.0 was released on 2025-08-20.
- **(finding)** Ablation study scripts were added for systematic evaluation of model components.
- **(finding)** A chimeric spectra experiment was added to evaluate robustness to co-eluting compounds.
- **(finding)** A noised spectra experiment was added to evaluate robustness to spectral noise.
- **(finding)** A demo training and evaluation script was added in version 1.1.0.
- **(finding)** Version 1.0.0 was released on 2024-11-26.
- **(finding)** Version 1.0.0 represented the initial FIDDLE release. _[grounded: FIDDLE_system]_
- **(finding)** FIDDLE source code is available on GitHub. _[grounded: FIDDLE_system]_
- **(finding)** The repository is licensed under Apache 2.0.
- **(finding)** FIDDLE has a Zenodo record with DOI 10.5281/zenodo.19181279. _[grounded: FIDDLE_system]_
- **(finding)** The prepare_augment_rescore.py script caps positives per formula using the --pos_cap parameter. _[grounded: tool_prepare_augment_rescore]_
- **(finding)** The prepare_augment_rescore.py script generates cross-spectrum negatives within a precursor m/z window specified by --tolerance in ppm. _[grounded: tool_prepare_augment_rescore]_
- **(finding)** The prepare_augment_rescore.py script downsamples to 1:1 positive:negative ratio. _[grounded: tool_prepare_augment_rescore]_
- **(finding)** Formula refinement in prepare_augment_rescore.py is parallelised via multiprocessing.Pool. _[grounded: tool_prepare_augment_rescore]_

## Steps

### Step `task_001`
- Title: Reproduce the Orbitrap dataset expansion to 28,751 training / 3,195 test compounds
- Task kind: `reproduction`
- Task: Apply the instrument allowlist fix (adding 'ftms' to gnps_orbitrap) to the FIDDLE dataset preprocessing pipeline and verify that the resulting training/test split produces exactly 28,751 training and 3,195 test compounds.
- Inputs:
  - Raw GNPS public library spectral dataset and compound metadata
  - Original instrument allowlist configuration (before 'ftms' addition)
- Expected outputs:
  - Training set compound count: 28,751
  - Test set compound count: 3,195
  - Verification report confirming dataset split matches reported counts
- Tools: msfiddle
- Landmark output files: filtered_dataset.csv, training_set_compounds.csv, test_set_compounds.csv, split_counts.json
- Primary expected artifact: `dataset_split_verification.txt`

### Step `task_002`
- Depends on: `task_001`
- Title: Reconstruct the Siamese rescore data augmentation step via prepare_augment_rescore.py
- Task kind: `component_reconstruction`
- Task: Run prepare_augment_rescore.py on TCN train and test sets to generate augmented rescore training data with capped positives per formula, cross-spectrum negatives within precursor m/z window, and 1:1 positive:negative downsampling. Output augmented training and test sets ready for model training.
- Inputs:
  - TCN training dataset (spectra and formula annotations)
  - TCN test dataset (spectra and formula annotations)
- Expected outputs:
  - Augmented rescore training set with capped positives, cross-spectrum negatives, and 1:1 ratio
  - Augmented rescore test set with capped positives, cross-spectrum negatives, and 1:1 ratio
- Tools: msfiddle
- Landmark output files: train_capped_positives.csv, test_capped_positives.csv, train_with_negatives.csv, test_with_negatives.csv, augmented_train_balanced.csv, augmented_test_balanced.csv

### Step `task_003`
- Depends on: `task_001`
- Title: Reproduce the Siamese rescore model training with train_rescore.py
- Task kind: `reproduction`
- Task: Execute train_rescore.py to train the FormulaEncoder and RescoreHead modules with frozen TCN spectrum encoder using binary cross-entropy loss. Verify that model checkpoints are saved only when formula accuracy (including hydrogen atoms) improves, and confirm output contains formula_encoder_state_dict and rescore_head_state_dict.
- Inputs:
  - task_001.expected_outputs[0]: Training set compound count: 28,751
  - Pre-trained TCN spectrum encoder checkpoint
  - Training dataset with MS/MS spectra and molecular formula annotations
  - Validation dataset for formula accuracy monitoring
- Expected outputs:
  - Best model checkpoint containing formula_encoder_state_dict and rescore_head_state_dict
  - Training log recording formula_acc (with H) and loss metrics per epoch
- Tools: msfiddle
- Landmark output files: training_log.csv, validation_metrics_per_epoch.csv, best_rescore_checkpoint.pt
- Primary expected artifact: `best_rescore_checkpoint.pt`

### Step `task_004`
- Depends on: `task_003`
- Title: Reproduce caffeine inference via test_caffeine.py on GNPS spectra
- Task kind: `reproduction`
- Task: Run the FIDDLE v2.0.0 inference script (test_caffeine.py) against caffeine (C8H10N4O2) spectra from the GNPS public library using the trained model checkpoint, and verify that the script completes successfully and produces a structured output file (CSV or equivalent) containing scored molecular formula candidates.
- Inputs:
  - Trained FIDDLE v2.0.0 model checkpoint (from zenodo.org/record/19181279)
  - Caffeine (C8H10N4O2) MS/MS spectra from GNPS public library
  - test_caffeine.py inference script
- Expected outputs:
  - Structured output file (CSV or JSON) with scored molecular formula candidates for caffeine, ranked by prediction score
- Tools: msfiddle
- Landmark output files: model_checkpoint.pt, gnps_caffeine_spectra.mgf, caffeine_predictions.csv
- Primary expected artifact: `caffeine_predictions.csv`

### Step `task_005`
- Depends on: `task_002`
- Title: Reconstruct the precursor m/z zeroing mechanism in the spectrum encoder to prevent mass-based prior learning
- Task kind: `component_reconstruction`
- Task: Verify that the precursor m/z value (env[:, 0]) is consistently zeroed before TCN encoder input across all three FIDDLE execution scripts (run_fiddle.py, train_rescore.py, and test_caffeine.py). Produce a verification report documenting the zeroing implementation in each script.
- Inputs:
  - run_fiddle.py source code from FIDDLE repository
  - train_rescore.py source code from FIDDLE repository
  - test_caffeine.py source code from FIDDLE repository
- Expected outputs:
  - Preprocessing verification report documenting precursor m/z zeroing across all three scripts
- Tools: msfiddle
- Landmark output files: run_fiddle_preprocessing_check.txt, train_rescore_preprocessing_check.txt, test_caffeine_preprocessing_check.txt
- Primary expected artifact: `preprocessing_verification_report.txt`

## Final expected outputs

- `Structured output file (CSV or JSON) with scored molecular formula candidates for caffeine, ranked by prediction score` (type: file, tolerance: hash)
- `Preprocessing verification report documenting precursor m/z zeroing across all three scripts` (type: file, tolerance: hash)

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
  "workflow_id": "coll_fiddle_workflow",
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
    "Structured output file (CSV or JSON) with scored molecular formula candidates for caffeine, ranked by prediction score": "<locator>",
    "Preprocessing verification report documenting precursor m/z zeroing across all three scripts": "<locator>"
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
