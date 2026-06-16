# Workflow Challenge: `coll_deepion_workflow`


> DeepION is a deep learning model that learns low-dimensional representations of ion images for mass spectrometry imaging through contrastive learning, with specialized augmentation strategies for co-localized ions (COL mode) and isotope ions (ISO mode).

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 3-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

DeepION comprises four modules for processing ion images in mass spectrometry imaging. The Data Augmentation module applies mode-specific transformations: COL mode uses color jitter, filtering, Poisson noise, and random missing value, while ISO mode adds an intensity-dependent missing value process. Two augmented images from the same source are propagated through a pair of parameter-shared ResNet18-based encoders to produce 512-dimensional representation vectors. The Projection and Prediction modules then process these vectors to avoid solution collapse while optimizing for maximum similarity between augmentations of the same ion image through contrastive loss.

## Research questions

- What are the specific augmentation operations applied in the COL and ISO modes of the DeepION data augmentation pipeline T, and how do they differ?
- How does the Encoder module in DeepION process two augmented ion images through shared-weight ResNet18 encoders to produce 512-dimensional representation vectors?
- How do the Projection and Prediction modules operate on 512-dimensional encoder outputs to prevent representation collapse during contrastive learning of ion images?

## Methods overview

Load the original ion image as input Apply COL mode augmentation sequence: color jitter → filtering → Poisson noise → random missing value, producing two independent augmented samples Apply ISO mode augmentation sequence: execute all COL mode operations, then apply intensity-dependent missing value targeting high or low intensity pixels, producing two independent augmented samples Validation: verify that each mode produces exactly two augmented images with no pixel value clipping or NaN artifacts; confirm intensity-dependent missing value in ISO mode correlates with input intensity distribution Define ResNet18 architecture with input compatibility for ion images and 512-dimensional output layer Instantiate shared-weight encoder module using single ResNet18 instance for both augmented images Configure parameter sharing constraints to ensure identical weights across encoder branches Implement bidirectional forward pass accepting two augmented images and outputting paired representation vectors Validation: Verify output tensor shapes match expected dimensions (batch_size × 512) and confirm parameter identity between branches Load 512-dimensional encoder outputs from paired ResNet18 networks processing augmented ion image pairs. Pass encoder outputs through a learnable Projection module to map to a contrastive learning space. Pass projected vectors through a learnable Prediction module to introduce asymmetry and prevent solution collapse. Compute contrastive loss (e.g., NT-Xent or SimCLR loss) between predictions of augmented pairs, maximizing similarity within pairs and minimizing across pairs. Optimize Projection and Prediction module parameters via backpropagation while maintaining encoder representations. Validation: contrastive loss converges to a stable minimum and learned representations preserve ion-image-specific structure (verified by downstream clustering or classification performance on COL/ISO modes).

**Domain:** bioinformatics

**Techniques:** deep-learning

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** DeepION is a deep learning-based low-dimensional representation model of ion images for mass spectrometry imaging. _[grounded: deepion_system]_
- **(finding)** DeepION has two modes denoted as COL and ISO. _[grounded: deepion_system]_
- **(finding)** The COL mode is designed for regular co-localized ions from different molecules. _[grounded: mode_col]_
- **(finding)** The ISO mode is designed for isotope ions from a same molecule. _[grounded: mode_iso]_
- **(finding)** Lei Guo is the developer of DeepION from the Laboratory of Biomedical Network at Xiamen University of China. _[grounded: deepion_system]_
- **(finding)** DeepION consists of four modules. _[grounded: deepion_system]_
- **(finding)** The Data Augmentation module generates two augmented images from the original ion image. _[grounded: module_data_augmentation]_
- **(finding)** The T_COL augmentation includes color jitter, filtering, Poisson noise, and random missing value. _[grounded: mode_col]_
- **(finding)** The T_ISO augmentation introduces an additional process of intensity-dependent missing value in ISO mode. _[grounded: mode_iso]_
- **(finding)** The Encoder module uses a pair of ResNet18-based encoders with shared parameters. _[grounded: module_encoder]_
- **(finding)** The Encoder module outputs two 512-dimensional representation vectors. _[grounded: module_encoder]_
- **(finding)** The Projection and Prediction modules are used to avoid collapsing solutions during optimization. _[grounded: module_projection]_
- **(finding)** The optimization process aims to maximize the similarity between two augmentations from the same image.
- **(finding)** A contrastive loss is employed in DeepION. _[grounded: deepion_system]_

## Steps

### Step `task_001`
- Title: Reconstruct the Data Augmentation Module for COL and ISO Modes
- Task kind: `component_reconstruction`
- Task: Implement data augmentation pipeline T to generate two augmented ion images per input image: apply color jitter, filtering, Poisson noise, and random missing value for COL mode; add intensity-dependent missing value for ISO mode. Output two augmented image pairs per input under each mode.
- Inputs:
  - Original ion image from mass spectrometry imaging
- Expected outputs:
  - Two augmented ion images from COL mode augmentation pipeline
  - Two augmented ion images from ISO mode augmentation pipeline
- Tools: ResNet18, Color jitter augmentation, Filtering augmentation, Poisson noise augmentation, Random missing value augmentation, Intensity-dependent missing value augmentation
- Landmark output files: col_augmented_image_1.npy, col_augmented_image_2.npy, iso_augmented_image_1.npy, iso_augmented_image_2.npy

### Step `task_002`
- Depends on: `task_001`
- Title: Reconstruct the ResNet18-Based Encoder Module Producing 512-D Representation Vectors
- Task kind: `component_reconstruction`
- Task: Implement a shared-weight ResNet18 encoder pair that accepts two augmented ion images and outputs two 512-dimensional representation vectors for the DeepION contrastive learning framework.
- Inputs:
  - Ion image dataset with augmented image pairs (from Data Augmentation module)
- Expected outputs:
  - Two 512-dimensional representation vectors per input pair
- Tools: ResNet18
- Landmark output files: encoder_model.pt, sample_representation_vectors.npy, output_shape_verification.txt

### Step `task_003`
- Depends on: `task_002`
- Title: Reconstruct the Projection and Prediction Modules with Contrastive Loss
- Task kind: `component_reconstruction`
- Task: Implement the Projection and Prediction modules to process 512-dimensional encoder outputs and apply contrastive loss to maximize similarity between augmentations of the same ion image, preventing collapse of learned representations.
- Inputs:
  - 512-dimensional representation vectors from paired ResNet18 encoders
  - Original ion images and their augmented versions (from Data Augmentation module)
- Expected outputs:
  - Trained Projection module weights and biases
  - Trained Prediction module weights and biases
  - Contrastive loss values per batch or epoch
  - Final learned representations for ion images after contrastive training
- Tools: ResNet18
- Landmark output files: projection_module_weights.pth, prediction_module_weights.pth, contrastive_loss_per_epoch.csv, learned_embeddings.npy
- Primary expected artifact: `contrastive_loss_training.csv`

## Final expected outputs

- `Trained Projection module weights and biases` (type: file, tolerance: hash)
- `Trained Prediction module weights and biases` (type: file, tolerance: hash)
- `Contrastive loss values per batch or epoch` (type: file, tolerance: hash)
- `Final learned representations for ion images after contrastive training` (type: file, tolerance: hash)

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

- **Composition modularity:** flat

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
  "workflow_id": "coll_deepion_workflow",
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
    "Trained Projection module weights and biases": "<locator>",
    "Trained Prediction module weights and biases": "<locator>",
    "Contrastive loss values per batch or epoch": "<locator>",
    "Final learned representations for ion images after contrastive training": "<locator>"
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
