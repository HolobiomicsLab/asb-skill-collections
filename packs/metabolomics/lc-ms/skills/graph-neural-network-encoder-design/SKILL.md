---
name: graph-neural-network-encoder-design
description: Use when when you need to compare spectrum prediction models fairly across different encoder architectures (GNN vs. FFN vs. Transformer), and you require equivalent settings (same covariates, identical hyperparameter sweeps) to isolate the effect of the encoder design.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0821
  - http://edamontology.org/topic_3372
  tools:
  - PubChem
  - coleygroup/ms-pred
  - PyTorch Geometric
  techniques:
  - LC-MS
derived_from:
- doi: 10.1038/s42256-024-00816-8
  title: ICEBERG
evidence_spans:
- By inputting the chemical formula and your experimental spectrum, the WebUI will rank it against all candidates from PubChem.
- the WebUI will rank it against all candidates from PubChem
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_iceberg_cq
    doi: 10.1038/s42256-024-00816-8
    title: ICEBERG
  dedup_kept_from: coll_iceberg_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s42256-024-00816-8
  all_source_dois:
  - 10.1038/s42256-024-00816-8
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# graph-neural-network-encoder-design

## Summary

Design and train a graph neural network (GNN) encoder to learn molecular representations from chemical graph structures for end-to-end spectrum prediction. This skill enables fair baseline comparison of GNN-based molecular encoders against alternative architectures (FFN, Transformer) under equivalent hyperparameter and covariate settings.

## When to use

When you need to compare spectrum prediction models fairly across different encoder architectures (GNN vs. FFN vs. Transformer), and you require equivalent settings (same covariates, identical hyperparameter sweeps) to isolate the effect of the encoder design. Use this skill specifically when reconstructing NEIMS baseline variants or building contrastive encoder experiments on mass spectrometry datasets with annotated chemical structures.

## When NOT to use

- Input molecules lack structural/graph annotations or are represented only as chemical formulas (use SCARF or FFN baseline instead).
- You require predictions at chemical formula level rather than molecular fragment level (SCARF is more suitable).
- Computational budget is severely limited and you cannot afford the overhead of GNN message-passing (FFN encoders are faster).

## Inputs

- Molecular dataset with SMILES strings or chemical structures (from PubChem or NIST'20)
- Experimental tandem mass spectra (.mgf, .hdf5, or .SDF format)
- Dataset splits (train/val/test) with collision energy annotations
- Hyperparameter configuration (batch_size, learning_rate, num_layers, hidden_dim)
- Molecular graph representation (atoms as nodes, bonds as edges)

## Outputs

- Trained GNN encoder model weights (.pt or .ckpt file)
- Predicted spectra or fragment ion intensities on test set
- Evaluation metrics (top-1/top-k retrieval accuracy, cosine similarity scores)
- Model comparison table (GNN vs. FFN encoder on same dataset/hyperparams)

## How to apply

Load molecular chemical structures from PubChem or NIST'20 as SMILES strings and convert them into graph representations (nodes=atoms, edges=bonds). Design a GNN encoder (e.g., message-passing or graph convolutional layers) to embed these molecular graphs into fixed-dimensional vectors. Train the GNN encoder end-to-end on the spectrum prediction task using the same dataset split, batch size, learning rate schedule, and hyperparameter ranges as the FFN baseline. Evaluate on held-out test spectra using established metrics (e.g., top-k retrieval accuracy, spectral similarity cosine score) and compare against the FFN-encoder variant to isolate encoder architecture effects. Save trained model weights, prediction outputs, and comparison metrics to enable reproducible ablation studies.

## Related tools

- **PubChem** (Source of molecular structures and chemical formula data for graph construction)
- **coleygroup/ms-pred** (Reference implementation repository containing NEIMS GNN/FFN encoder variants and equivalent-settings comparison framework) — https://github.com/coleygroup/ms-pred
- **PyTorch Geometric** (Library for GNN layer implementations (message-passing, graph convolutions))

## Examples

```
python src/ms_pred/models/train_neims.py --model_type=gnn --dataset=nist20 --batch_size=32 --num_layers=3 --hidden_dim=256 --lr=0.001 --split=split_1_rnd1
```

## Evaluation signals

- GNN encoder produces fixed-dimensional molecular embeddings matching the input graph structure (nodes = atoms, edges = bonds).
- Training loss (e.g., cross-entropy or MSE on spectrum prediction) converges on both training and validation sets without divergence.
- Test-set metrics (top-k retrieval accuracy, cosine similarity) are reproducible across seeds and match reported baseline values within statistical confidence intervals.
- GNN encoder performance is comparable to or outperforms FFN baseline when both use identical hyperparameters, dataset splits, and covariates (equivalent-settings condition).
- Model weights and prediction outputs can be loaded and re-evaluated without retraining, confirming serialization integrity.

## Limitations

- GNN training requires molecules with well-formed SMILES and explicit atom/bond annotations; malformed or ambiguous structures will degrade encoder learning.
- GNN scalability is constrained by graph size and batch size; NIST'20 training on a single GPU (24GB RAM) may require batch_size reduction below the hyperparameter sweep baseline.
- Equivalent-settings comparison assumes all models use identical covariates and splits; any deviation (e.g., different data augmentation, train/val/test ratio) invalidates fair comparison.
- GNN encoder performance is sensitive to initialization and random seeds; results reported in the literature use multiple random seeds (3 seeds mentioned in README) to compute confidence intervals.

## Evidence

- [other] NEIMS baseline is implemented with both FFN and GNN encoder variants as part of an equivalent-settings comparison framework where all models use the same covariates and hyperparameter sweeps.: "NEIMS baseline is implemented with both FFN and GNN encoder variants as part of an equivalent-settings comparison framework where all models use the same covariates and hyperparameter sweeps."
- [other] Construct a graph neural network (GNN) encoder to learn molecular representations from chemical graphs.: "Construct a graph neural network (GNN) encoder to learn molecular representations from chemical graphs."
- [other] Train the GNN encoder end-to-end on the spectrum prediction task using the dataset split and hyperparameters specified for the baseline comparison.: "Train the GNN encoder end-to-end on the spectrum prediction task using the dataset split and hyperparameters specified for the baseline comparison."
- [other] Evaluate the trained GNN-encoder NEIMS model on the held-out test set, computing prediction accuracy and comparison metrics against ms-pred reference results.: "Evaluate the trained GNN-encoder NEIMS model on the held-out test set, computing prediction accuracy and comparison metrics against ms-pred reference results."
- [intro] ICEBERG predicts spectra at the level of molecular fragments, whereas SCARF predicts spectra at the level of chemical formula.: "ICEBERG predicts spectra at the level of molecular fragments, whereas SCARF predicts spectra at the level of chemical formula."
- [readme] You need two GPUs with at least 24GB RAM to train ICEBERG. If you are trying to train the model on a smaller GPU, try cutting down the batch size and skipping the contrastive finetuning step.: "You need two GPUs with at least 24GB RAM to train ICEBERG. If you are trying to train the model on a smaller GPU, try cutting down the batch size and skipping the contrastive finetuning step."
- [readme] we implement a number of baselines and alternative models using equivalent settings across models (i.e., same covariates, hyperparameter sweeps for each, etc.): "we implement a number of baselines and alternative models using equivalent settings across models (i.e., same covariates, hyperparameter sweeps for each, etc.)"
- [other] Load the molecular dataset and chemical structures from PubChem with associated experimental mass spectra.: "Load the molecular dataset and chemical structures from PubChem with associated experimental mass spectra."
