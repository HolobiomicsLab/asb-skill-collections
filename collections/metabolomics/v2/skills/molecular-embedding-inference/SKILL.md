---
name: molecular-embedding-inference
description: Use when you have a set of molecules (as SMILES strings in CSV format) and a pre-trained NaFM checkpoint, and you need to generate embeddings or predictions for virtual screening, bioactivity regression, or compound ranking tasks.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3336
  - http://edamontology.org/topic_0091
  tools:
  - PyTorch
  - Git
  - PyTorch Geometric (PyG)
  - NaFM inference.py
derived_from:
- doi: 10.1002/anie.202507483
  title: NA
evidence_spans:
- github.com/TomAIDD/NaFM-Official
- Fork the repository
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nafm_cq
    doi: 10.1002/anie.202507483
    title: NA
  dedup_kept_from: coll_nafm_cq
schema_version: 0.2.0
---

# molecular-embedding-inference

## Summary

Generate molecular embeddings and predictions for small molecules using a pre-trained foundation model (NaFM), producing fixed-dimensional vector representations that encode structural and evolutionary features of natural products. Use this to obtain meaningful molecular representations for downstream tasks like virtual screening, bioactivity prediction, or compound ranking without retraining.

## When to use

You have a set of molecules (as SMILES strings in CSV format) and a pre-trained NaFM checkpoint, and you need to generate embeddings or predictions for virtual screening, bioactivity regression, or compound ranking tasks. This skill is appropriate when the input molecules are natural products or synthetically-derived compounds that benefit from representations learned on natural product evolutionary patterns, and when you want to avoid supervised retraining on limited downstream task data.

## When NOT to use

- Input SMILES are already validated and canonicalized elsewhere — the inference pipeline performs its own SMILES standardization and may duplicate effort
- You require task-specific performance optimization — inference uses a frozen pre-trained model; finetuning is needed to adapt to new downstream tasks
- Input molecules are outside the natural product or drug-discovery domain — NaFM is specifically pre-trained on natural products and may underperform on purely synthetic chemical spaces

## Inputs

- Pre-trained model checkpoint (NaFM.ckpt)
- CSV file with 'SMILES' column containing molecule structures
- Configuration file or command-line parameters specifying task type, model hyperparameters, and output paths

## Outputs

- predictions.csv file containing model outputs (class predictions + probabilities for classification, regression scores for bioactivity)
- Molecular embeddings (1024-dimensional vectors per molecule) optionally saved or logged during inference

## How to apply

Load the pre-trained NaFM model weights from the checkpoint file (NaFM.ckpt), prepare input data as a CSV with a 'SMILES' column, then run the inference script specifying the task type (classification or regression) and checkpoint path. The inference pipeline will standardize SMILES, convert them to molecular graphs, pass them through the pre-trained encoder to produce embeddings or task-specific predictions, and save results to predictions.csv. Key parameters include the embedding dimension (default 1024), number of GNN layers (default 6), and dropout ratio (0.15 for classification, 0.1 for regression), which should match the checkpoint's training configuration. Validation involves comparing the output embedding dimensionality against expected values and checking that predictions fall within reasonable ranges for the task (e.g., classification probabilities in [0,1], regression values consistent with the training data distribution).

## Related tools

- **PyTorch** (Deep learning framework for loading pre-trained model weights and executing forward passes through the neural network encoder)
- **PyTorch Geometric (PyG)** (Graph neural network library used to represent molecules as molecular graphs and apply graph convolution layers during embedding inference) — https://github.com/pyg-team/pytorch_geometric
- **NaFM inference.py** (Official script for running inference on new molecules; handles SMILES parsing, graph construction, model loading, and output serialization) — github.com/TomAIDD/NaFM-Official

## Examples

```
python inference.py --task classification --downstream-data downstream_data/Ontology/raw/classification_data.csv --checkpoint-path NaFM.ckpt
```

## Evaluation signals

- Output predictions.csv contains one row per input molecule with correct column names (e.g., 'SMILES', 'prediction', 'probability' for classification; 'SMILES', 'score' for regression)
- Embedding vectors have shape (n_molecules, 1024) and values are finite (no NaN or Inf); embedding statistics should be centered near zero with typical L2 norms in the range [10–50] based on natural product feature distributions
- Classification predictions are valid probability distributions (sum to 1.0 per row, values in [0, 1]); regression predictions fall within or near the training data range observed in downstream_data/Regression
- Model successfully loads from checkpoint without errors; a quick inference on 1–10 test SMILES completes in <1 second per molecule on a CPU and <100ms on GPU
- Consistency check: re-running inference on the same input batch produces identical embeddings (deterministic behavior when seed is fixed)

## Limitations

- Inference uses a frozen encoder; performance is limited by the pre-training objective. For novel downstream tasks with task-specific data, finetuning the model head (or full model) typically outperforms pure inference embeddings.
- SMILES standardization in the inference pipeline may fail on unusual or non-standard SMILES; molecules with valence errors or unconventional notation should be validated and cleaned before input.
- The pre-trained model encodes scaffold-derived evolutionary patterns specific to natural products; inference on purely synthetic molecules (without natural product ancestry) may not capture relevant features as effectively as on the in-distribution natural product space.
- Inference assumes GPU availability for acceptable throughput; CPU inference on large compound libraries (>100k molecules) can be slow. Batch size tuning may be required to fit memory constraints.

## Evidence

- [readme] For inference on new molecules (CSV with a "SMILES" column): python inference.py --task classification --downstream-data [data location] --checkpoint-path [your finetuned model path]: "For inference on new molecules (CSV with a "SMILES" column): python inference.py --task classification --downstream-data [data location] --checkpoint-path [your finetuned model path]"
- [methods] Run the inference script on the screening compounds to generate molecular embeddings and predictions.: "Run the inference script on the screening compounds to generate molecular embeddings and predictions."
- [abstract] Our method integrates contrastive learning with masked graph modeling, effectively encoding scaffold-derived evolutionary patterns alongside diverse side-chain information.: "Our method integrates contrastive learning with masked graph modeling, effectively encoding scaffold-derived evolutionary patterns alongside diverse side-chain information."
- [abstract] The proposed framework achieves state-of-the-art (SOTA) performance across a wide range of downstream tasks in natural product mining and drug discovery.: "The proposed framework achieves state-of-the-art (SOTA) performance across a wide range of downstream tasks in natural product mining and drug discovery."
- [readme] Results will be saved to NaFM/predictions.csv.: "Results will be saved to NaFM/predictions.csv."
