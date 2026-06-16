# Workflow Challenge: `coll_mol2ccs_workflow`


> This work reproduces the evaluation of graph neural networks for predicting collision cross section and analyzes feature importance to identify key structural drivers of GNN predictions.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 4-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

Reproduces 1 reported result: The paper evaluates the generalizability of graph neural networks for predicting collision cross section, as described in Engler et al. 2024. Analyses 1 derived result: The repository contains code and data for evaluating graph neural networks trained to predict collision cross section, enabling post-hoc attribution analysis to identify key structural drivers. Reconstructs 1 described mechanism (described in the paper but not separately evaluated there): The repository contains code for preprocessing raw SMILES strings from the CCS dataset into atom and bond feature tensors (graph objects) that serve as input to the graph neural network. Extends the paper in 1 task beyond its reported scope: The paper evaluates graph neural networks for predicting collision cross section, establishing a baseline for GNN-based approaches that can be extended with alternative architectures.

## Research questions

- Can graph neural network models trained for collision cross section prediction generalize effectively to held-out test data?
- Which molecular structural features are most important for driving graph neural network predictions of collision cross section?
- How are SMILES strings from the CCS dataset preprocessed and converted into graph tensor representations suitable for GNN input?
- How do alternative graph neural network architectures (e.g., GAT, MPNN) compare to the original GNN architecture in predicting collision cross section on the same dataset split?

## Methods overview

Load pre-trained GNN model checkpoint from enveda/ccs-prediction repository. Load and preprocess CCS dataset; partition into train/validation/test splits or load held-out test set. Execute GNN inference on test set to generate CCS predictions. Compute regression metrics (RMSE, MAE, R²) on predictions versus ground truth. Validation: reported metric values match paper-cited generalizability benchmarks within numerical precision tolerance. Load trained GNN model and test molecular graphs from repository Perform node and edge feature ablation by iterative masking and prediction delta measurement Compute gradient-based saliency via backpropagation through model Aggregate ablation and saliency scores across test set; normalize by feature frequency or molecular properties Rank features by total importance and produce ranked table and bar/heatmap visualization Validation: output table contains ≥10 ranked features with non-zero importance scores; visualization clearly labels top features and shows relative magnitudes Load raw SMILES strings from the CCS dataset repository. Canonicalize each SMILES string using RDKit to ensure structural uniqueness. Convert each canonical SMILES to a molecular graph representation. Extract atom-level features (atomic number, charge, hybridization, aromaticity) and bond-level features (type, aromaticity, stereochemistry). Construct node and edge feature tensors encoding molecular structure. Serialize all graph objects and associated metadata to a standard PyTorch or pickle format. Validation: confirm output file exists and contains graph tensors with shapes consistent with expected atom/bond dimensions. Clone enveda/ccs-prediction repository and load preprocessed CCS dataset with train/val/test splits. Implement alternative message-passing GNN (GAT or MPNN) with matching input/output dimensions. Train alternative architecture on training set using original hyperparameters and loss function. Evaluate both original and alternative models on test set, computing RMSE, MAE, accuracy, training time, and inference speed. Generate comparative performance table documenting results side-by-side. Validation: Ensure test-set RMSE and MAE values are computed consistently for both architectures and table is reproducible from stored model weights.

**Domain:** cheminformatics

**Techniques:** graph-neural-network, machine-learning, deep-learning, transfer-learning

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** This repository contains code and data described in detail in a paper by Engler et al., 2024.

## Steps

### Step `task_001`
- Title: Reproduce GNN generalizability evaluation for CCS prediction across molecular datasets
- Task kind: `reproduction`
- Task: Re-run trained GNN model(s) from the enveda/ccs-prediction repository on the CCS dataset to compute and reproduce reported generalizability metrics (RMSE, MAE, R²) on held-out test data.
- Inputs:
  - enveda/ccs-prediction repository (pre-trained model checkpoint and code)
  - CCS dataset (collision cross section molecular data with ground-truth labels)
- Expected outputs:
  - Generalizability metrics table (RMSE, MAE, R²) computed on held-out test data
  - Model predictions on test set (molecular identifiers and predicted vs. ground-truth CCS values)
- Tools: Graph Neural Network (GNN) framework (PyTorch Geometric or equivalent), enveda/ccs-prediction repository (model code and pre-trained weights)
- Landmark output files: model_checkpoint_loaded.log, test_set_predictions.csv, generalizability_metrics.json
- Primary expected artifact: `ccs_metrics_and_predictions.csv`

### Step `task_002`
- Depends on: `task_001`
- Title: Analyze feature importance and molecular descriptor contributions to GNN CCS predictions
- Task kind: `analysis`
- Task: Perform post-hoc attribution analysis on trained graph neural network models to identify and rank the molecular structural features (nodes, edges, atom/bond properties) that drive CCS predictions. Produce a ranked feature-importance table or visualization.
- Inputs:
  - Trained GNN model checkpoint and molecular graph dataset from enveda/ccs-prediction repository
  - Input molecular graphs (node features, edge features, connectivity) for test molecules
  - Ground-truth or reference CCS values for evaluation
- Expected outputs:
  - Ranked feature-importance table (CSV or TSV) listing node/edge features sorted by ablation or saliency score
  - Feature-importance visualization (bar plot or heatmap) showing relative contribution of top structural features to CCS prediction
- Tools: PyTorch or TensorFlow, RDKit
- Landmark output files: ablation_scores.csv, gradient_saliency_maps.npz, feature_importance_table.csv, feature_importance_plot.png
- Primary expected artifact: `feature_importance_table.csv`

### Step `task_003`
- Depends on: `task_001`
- Title: Reconstruct the molecular graph construction step that converts SMILES to GNN input tensors
- Task kind: `component_reconstruction`
- Task: Reconstruct the data-preprocessing pipeline that converts raw SMILES strings from the CCS dataset into atom/bond feature tensors (graph objects) suitable for GNN consumption. Output a serialized graph dataset file in standard format (.pt or .pkl).
- Inputs:
  - Raw SMILES strings from CCS dataset (enveda/ccs-prediction repository)
- Expected outputs:
  - Serialized graph dataset file containing atom/bond feature tensors and molecular graphs in PyTorch or pickle format
- Tools: manual expert review
- Landmark output files: canonical_smiles.csv, molecular_graphs.pkl, atom_features.npy, bond_features.npy
- Primary expected artifact: `graph_dataset.pt`

### Step `task_004`
- Depends on: `task_003`
- Title: Extend CCS prediction by substituting an alternative GNN architecture and comparing held-out performance
- Task kind: `extension`
- Task: Replace the original GNN architecture in the enveda/ccs-prediction codebase with an alternative message-passing variant (GAT or MPNN) and re-evaluate on the same CCS dataset split to produce a comparative performance table.
- Inputs:
  - enveda/ccs-prediction repository containing original GNN model code, preprocessed molecular graph data, and CCS ground-truth labels
  - Training, validation, and test dataset splits with molecular structures and corresponding CCS values
- Expected outputs:
  - Comparative performance table (CSV or JSON) with metrics (RMSE, MAE, accuracy, training time, inference speed) for both original and alternative GNN architectures
  - Trained alternative GNN model weights and architecture definition file
  - Predictions on test set from both architectures for downstream comparison
- Tools: PyTorch Geometric (PyG), PyTorch
- Landmark output files: alt_gnn_architecture.py, training_log_alternative.txt, test_predictions_original.csv, test_predictions_alternative.csv, model_weights_alternative.pt
- Primary expected artifact: `ccs_gnn_comparison_table.csv`

## Final expected outputs

- `Ranked feature-importance table (CSV or TSV) listing node/edge features sorted by ablation or saliency score` (type: file, tolerance: hash)
- `Feature-importance visualization (bar plot or heatmap) showing relative contribution of top structural features to CCS prediction` (type: file, tolerance: hash)
- `Comparative performance table (CSV or JSON) with metrics (RMSE, MAE, accuracy, training time, inference speed) for both original and alternative GNN architectures` (type: file, tolerance: hash)
- `Trained alternative GNN model weights and architecture definition file` (type: file, tolerance: hash)
- `Predictions on test set from both architectures for downstream comparison` (type: file, tolerance: hash)

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
  "workflow_id": "coll_mol2ccs_workflow",
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
    "Ranked feature-importance table (CSV or TSV) listing node/edge features sorted by ablation or saliency score": "<locator>",
    "Feature-importance visualization (bar plot or heatmap) showing relative contribution of top structural features to CCS prediction": "<locator>",
    "Comparative performance table (CSV or JSON) with metrics (RMSE, MAE, accuracy, training time, inference speed) for both original and alternative GNN architectures": "<locator>",
    "Trained alternative GNN model weights and architecture definition file": "<locator>",
    "Predictions on test set from both architectures for downstream comparison": "<locator>"
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
