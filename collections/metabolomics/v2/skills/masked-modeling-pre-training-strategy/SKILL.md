---
name: masked-modeling-pre-training-strategy
description: Use when when you have unlabeled molecular structure data (SMILES or
  molecular graphs) from natural products and need to learn task-agnostic representations
  that capture both evolutionary (scaffold-level) and structural (side-chain) information
  before finetuning on downstream classification or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3680
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0154
  tools:
  - Git
  - PyTorch
  - PyTorch Lightning
  - PyTorch Geometric (PyG)
  - NaFM Official Repository
  license_tier: restricted
derived_from:
- doi: 10.1002/anie.202507483
  title: NA
evidence_spans:
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1002/anie.202507483
  all_source_dois:
  - 10.1002/anie.202507483
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# masked-modeling-pre-training-strategy

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Masked graph modeling is a self-supervised pre-training objective that learns molecular representations by predicting masked nodes and edges in graph-structured molecules, complementing contrastive learning to encode scaffold-derived evolutionary patterns and side-chain structural diversity in natural products.

## When to use

When you have unlabeled molecular structure data (SMILES or molecular graphs) from natural products and need to learn task-agnostic representations that capture both evolutionary (scaffold-level) and structural (side-chain) information before finetuning on downstream classification or regression tasks. Particularly useful when supervised datasets for your specific task are small or unavailable.

## When NOT to use

- Input is already task-labeled (classification labels or regression targets available); use supervised finetuning directly instead.
- Molecules are not represented as graphs or SMILES (e.g., 3D conformer files without conversion); graph construction is a prerequisite.
- Pre-trained weights for natural products already exist and are appropriate for your domain; reuse them instead of retraining.

## Inputs

- SMILES strings (unlabeled molecules in CSV or pickle format)
- Molecular graph representations (node and edge tensors)
- Configuration file specifying embedding dimension, number of layers, masking ratio, and loss weights

## Outputs

- Pre-trained model checkpoint (.ckpt) with learned graph neural network weights
- Frozen molecular embeddings (1024-dim by default) for downstream task finetuning
- Training logs with masked prediction accuracy and contrastive loss curves

## How to apply

Convert your unlabeled SMILES data to a standardized pickle format (pretrain_smiles.pkl) by running the filter pipeline to remove salts and duplicates. Construct molecular graphs and apply random masking to nodes and edges. Jointly optimize two loss objectives: (1) masked node/edge prediction via graph neural network reconstruction, and (2) contrastive loss between augmented graph pairs. Train using the provided Pretrain.yml configuration with PyTorch Lightning, monitoring convergence via tensorboard. The dual objectives together ensure that scaffold-derived evolutionary patterns (captured by contrastive pairs) and side-chain diversity (reconstructed during masked prediction) are jointly encoded in the final embeddings.

## Related tools

- **PyTorch** (Deep learning framework for implementing masked graph neural networks and contrastive learning objectives)
- **PyTorch Lightning** (Training framework for managing pre-training loops, validation, and checkpoint saving across distributed hardware)
- **PyTorch Geometric (PyG)** (Graph neural network library for constructing graph datasets, applying masking operations, and defining message-passing layers)
- **NaFM Official Repository** (Reference implementation including graph construction, masking pipeline, contrastive and masked prediction loss functions, and training scripts) — github.com/TomAIDD/NaFM-Official

## Examples

```
python train.py --conf examples/Pretrain.yml
```

## Evaluation signals

- Masked prediction accuracy (fraction of correctly reconstructed nodes/edges) should increase monotonically during training and plateau at >70%.
- Contrastive learning loss (NT-Xent or equivalent) should decrease smoothly; divergence or plateauing at high values indicates misalignment between augmented pairs.
- Downstream task performance (e.g., taxonomy classification F1, bioactivity regression R²) on held-out finetuning data should exceed performance of models trained from scratch or models pre-trained on synthetic molecules (reported as baseline comparisons in the paper).
- Learned embeddings should cluster molecules by scaffold (evolutionary signal) and separate by side-chain modifications, verifiable via t-SNE or UMAP visualization of taxonomy labels.
- Model checkpoint should load without errors and produce consistent 1024-dim embeddings for the same SMILES input across runs.

## Limitations

- Pre-training requires substantial unlabeled natural product data (order of 10k+ molecules recommended); performance degrades with smaller datasets.
- Masking ratio and graph construction hyperparameters are data-dependent; configurations tuned on LOTUS/Ontology datasets may not transfer to external natural product collections.
- Contrastive learning assumes that augmented graph pairs (e.g., different masking patterns) preserve semantic similarity; this may not hold for chemically fragile scaffolds or side chains.
- Downstream task improvements over synthetic pre-training are most pronounced for taxonomy classification; virtual screening and bioactivity prediction gains are smaller and task-dependent.
- The paper notes evaluation scripts (test.py) are minimal demonstrations rather than production pipelines; users must validate on their specific downstream task and dataset.

## Evidence

- [intro] Our method integrates contrastive learning with masked graph modeling, effectively encoding scaffold-derived evolutionary patterns alongside diverse side-chain information: "Our method integrates contrastive learning with masked graph modeling, effectively encoding scaffold-derived evolutionary patterns alongside diverse side-chain information"
- [other] data loading → graph construction → feature embedding → contrastive loss computation and masked node/edge prediction → gradient updates: "data loading → graph construction → feature embedding → contrastive loss computation and masked node/edge prediction → gradient updates"
- [readme] First, convert your SMILES data to a `.csv` file and place it in `raw_data/raw`. Then run: cd NaFM/raw_data/raw python filter.py This will standardize SMILES, remove salt and duplicate atoms, and generate `pretrain_smiles.pkl`.: "convert your SMILES data to a `.csv` file and place it in `raw_data/raw`. Then run: cd NaFM/raw_data/raw python filter.py This will standardize SMILES, remove salt and duplicate atoms, and generate"
- [intro] We first benchmark NaFM on taxonomy classification against models pre-trained on synthetic molecules, demonstrating their inadequacy for capturing natural synthesis patterns: "benchmark NaFM on taxonomy classification against models pre-trained on synthetic molecules, demonstrating their inadequacy for capturing natural synthesis patterns"
- [intro] conventional molecular representation techniques are not well-suited to the unique structural and evolutionary features of natural products: "conventional molecular representation techniques are not well-suited to the unique structural and evolutionary features of natural products"
