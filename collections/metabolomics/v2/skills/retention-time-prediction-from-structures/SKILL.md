---
name: retention-time-prediction-from-structures
description: Use when you have molecular structures (SMILES or SDF format) for which
  you need to predict retention time in liquid chromatography, especially when your
  target dataset contains fewer than ~500 annotated examples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3791
  edam_topics:
  - http://edamontology.org/topic_3174
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3336
  tools:
  - PyTorch
  - DGL
  - RDKit
  - retention_time_gnn
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.3c03177
  title: retention_time_gnn
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_retention_time_gnn_cq
    doi: 10.1021/acs.analchem.3c03177
    title: retention_time_gnn
  dedup_kept_from: coll_retention_time_gnn_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c03177
  all_source_dois:
  - 10.1021/acs.analchem.3c03177
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# retention-time-prediction-from-structures

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Use a pre-trained graph neural network (GNN) to predict liquid chromatography retention times from molecular structures, enabling rapid screening on small training datasets without retraining from scratch. This approach leverages transfer learning to generalize across different chromatographic methods and chemical libraries.

## When to use

You have molecular structures (SMILES or SDF format) for which you need to predict retention time in liquid chromatography, especially when your target dataset contains fewer than ~500 annotated examples. The skill is most valuable when you want to avoid the data collection burden of training a GNN from scratch, or when you are working across different chromatographic platforms (e.g., METLIN-SMRT to PredRet or MoNA databases).

## When NOT to use

- Your molecules are outside the structural diversity of the pre-training set (METLIN small molecules); performance degrades significantly for very large or exotic chemical scaffolds not represented in METLIN.
- You have a large fully-annotated retention time dataset (> 5000 samples) — training a model from scratch may be more efficient and better calibrated than transfer learning.
- Your chromatographic method is substantially different from those in METLIN, PredRet, or MoNA (e.g., supercritical fluid chromatography or gel filtration); transfer learning may not capture method-specific behavior.

## Inputs

- Molecular structures (SMILES strings or SDF files)
- Pre-trained GNN model checkpoint
- Optional: small annotated retention time dataset for transfer learning (< 500 samples recommended)
- Chromatographic platform identifier (e.g., 'FEM_long' for PredRet database)
- RDKit molecule objects or graph tensors (nodes, edges, atom features)

## Outputs

- Predicted retention time values (continuous numeric)
- Model checkpoint after transfer learning (PyTorch .pt or .pth file)
- Predictions file (CSV or JSON with molecule ID and predicted retention time)
- Molecular embeddings from GNN encoder (optional, for downstream analysis)

## How to apply

Obtain pre-trained GNN model weights from the seokhokang/retention_time_gnn repository and the retention time reference dataset (METLIN-SMRT, PredRet, or MoNA). Convert molecular structures to graph representations (nodes as atom types and features, edges as bonds) using RDKit and DGL. Load the pre-trained encoder to generate molecular embeddings, then optionally fine-tune the prediction head on your target chromatographic platform using run_transfer.py. The GNN processes the full molecular graph topology end-to-end rather than hand-crafted molecular descriptors, allowing it to learn chemical patterns relevant to retention from the pre-training phase. Evaluate predictions on a held-out test set using standard regression metrics (e.g., root mean squared error, mean absolute error).

## Related tools

- **PyTorch** (Deep learning framework for GNN model architecture, forward pass, and gradient-based transfer learning)
- **DGL** (Graph neural network library for constructing and processing molecular graph representations)
- **RDKit** (Chemistry toolkit for converting SMILES/SDF to molecular graphs and extracting atom features)
- **retention_time_gnn** (Reference implementation providing pre-trained model weights, data loading utilities, and training scripts) — https://github.com/seokhokang/retention_time_gnn

## Examples

```
python run_transfer.py -t FEM_long
```

## Evaluation signals

- Predicted retention times fall within the observed range of the target dataset (sanity check for extrapolation).
- Root mean squared error (RMSE) or mean absolute error (MAE) on a held-out test set is within 10–20% of the training RMSE, indicating no severe overfitting.
- Predictions are invariant to the order of input molecules (reproducibility check).
- Molecular embeddings from the encoder show clustering by chemical class or retention range (qualitative validation via t-SNE or UMAP).
- Transfer learning on the target platform achieves lower error than applying the pre-trained model without fine-tuning, confirming benefit of adaptation.

## Limitations

- Performance depends on structural similarity between molecules in the pre-training set (METLIN-SMRT) and your target dataset; large domain shifts reduce accuracy.
- The model requires valid molecular graphs (valence-correct SMILES or SDF); invalid structures will fail at the graph preprocessing step.
- Transfer learning with very small target datasets (< 50 samples) may overfit or provide unstable predictions; cross-validation is recommended.
- Retention time is affected by chromatographic hardware, temperature, and solvent composition; the GNN learns only chemical structure—method-specific factors must be controlled experimentally.
- The pre-trained model was optimized for small molecules in the METLIN library; performance on metabolites, natural products, or large polymers is not characterized.

## Evidence

- [other] The implementation is a PyTorch-based graph neural network model designed to predict retention time by learning from small training datasets through pre-trained GNN components.: "PyTorch-based graph neural network model designed to predict retention time by learning from small training datasets through pre-trained GNN components"
- [other] Forward pass through the GNN encoder layers to generate molecular embeddings. Pass embeddings through the prediction head to generate retention time predictions.: "Forward pass through the GNN encoder layers to generate molecular embeddings. Pass embeddings through the prediction head to generate retention time predictions."
- [readme] Pytorch implementation of the model described in the paper Retention Time Prediction by Learning from Small Training Dataset with Pre-Trained Graph Neural Network: "Pytorch implementation of the model described in the paper [Retention Time Prediction by Learning from Small Training Dataset with Pre-Trained Graph Neural Network]"
- [readme] The METLIN-SMRT dataset can be downloaded; The target datasets from PredRet database and MoNA database can be downloaded.: "The METLIN_small_molecule_dataset_for_machine_learning-based_retention_time_prediction; target datasets from PredRet database; target datasets from MoNA database"
- [readme] python run_pretrain.py; python run_transfer.py -t FEM_long: "python run_transfer.py -t FEM_long"
- [readme] Dependencies: Python, Pytorch, DGL, RDKit: "Dependencies: Python, Pytorch, DGL, RDKit"
