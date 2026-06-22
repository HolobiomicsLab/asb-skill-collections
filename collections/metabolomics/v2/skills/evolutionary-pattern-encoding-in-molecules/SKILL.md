---
name: evolutionary-pattern-encoding-in-molecules
description: Use when when building or fine-tuning a molecular representation model intended for natural product mining, taxonomy classification, or bioactivity prediction, and you have access to natural product SMILES data with scaffold and side-chain structural annotations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0009
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3307
  - http://edamontology.org/topic_3344
  tools:
  - Git
  - PyTorch
  - PyTorch Geometric (PyG)
  - PyTorch Lightning
  - RDKit or equivalent chemoinformatics library
  - NaFM-Official repository
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# evolutionary-pattern-encoding-in-molecules

## Summary

A pre-training strategy that encodes scaffold-derived evolutionary patterns and side-chain structural diversity in natural product molecules using dual objectives: contrastive learning and masked graph modeling. This approach enables foundation models to capture biosynthetic lineage information absent in synthetic molecule datasets.

## When to use

When building or fine-tuning a molecular representation model intended for natural product mining, taxonomy classification, or bioactivity prediction, and you have access to natural product SMILES data with scaffold and side-chain structural annotations. Use this skill specifically when conventional synthetic molecule pre-training has demonstrated inadequacy for your downstream task (e.g., poor performance on taxonomy classification or gene-level biosynthetic pattern recognition).

## When NOT to use

- Input consists entirely of synthetic molecules or molecules without known biosynthetic lineage—use standard molecular pre-training (e.g., on ChEMBL) instead.
- Downstream task does not require evolutionary or biosynthetic pattern understanding (e.g., purely chemical property prediction unrelated to natural product origin).
- SMILES data lack consistent quality or scaffold annotations—pre-training will not reliably encode evolutionary signals.

## Inputs

- SMILES strings (CSV file with 'SMILES' column)
- Natural product molecular structures with associated taxonomic or biosynthetic metadata
- Scaffold annotations or extractable sub-structures encoding evolutionary relationships

## Outputs

- Pre-trained model checkpoint (`.ckpt` file) with learned molecular representations
- Embedding vectors (dimension typically 1024) capturing scaffold-derived evolutionary patterns and side-chain information
- Validation metrics on taxonomy classification (Class/Superclass/Pathway accuracy)
- Gene and microbial-level interpretability analysis showing evolutionary information retention

## How to apply

Parse natural product SMILES from a CSV file and standardize them using SMILES filtering (removing salts, duplicates, and invalid structures) to produce a .pkl file. Construct molecular graphs and extract scaffold structures to represent evolutionary lineages. Implement a dual pre-training loss combining: (1) contrastive learning that groups molecules by evolutionary similarity (using cosine similarity with temperature parameter, e.g., τ=0.2), and (2) masked graph modeling that predicts masked nodes/edges in the molecular graph. Jointly optimize both objectives during training, alternating gradient updates through the GNN layers. Validate that the learned representations show high accuracy on taxonomy classification tasks (Class/Superclass/Pathway levels) and demonstrate interpretable gene and microbial-level patterns before applying to downstream tasks.

## Related tools

- **PyTorch** (Deep learning framework for implementing GNN layers, contrastive loss, and masked graph modeling objectives)
- **PyTorch Geometric (PyG)** (Graph neural network and geometric deep learning primitives for molecular graph construction and node/edge operations)
- **PyTorch Lightning** (Training loop management, distributed training orchestration, and checkpoint/logging handling for pre-training)
- **RDKit or equivalent chemoinformatics library** (SMILES standardization, salt removal, duplicate detection, and scaffold extraction for pre-training data preparation)
- **NaFM-Official repository** (Reference implementation of the dual pre-training framework, model architecture, and training configuration examples) — github.com/TomAIDD/NaFM-Official

## Examples

```
python train.py --conf examples/Pretrain.yml
```

## Evaluation signals

- Pre-trained model achieves >85% accuracy on natural product taxonomy classification (Class/Superclass/Pathway levels) when fine-tuned with limited labeled data, significantly outperforming models pre-trained on synthetic molecules on the same task.
- Learned representations show statistically significant clustering by gene family or microbial taxon when projected to 2D (t-SNE/UMAP), indicating evolutionary patterns were encoded.
- Contrastive loss converges to <0.1 and masked graph modeling loss reaches acceptable reconstruction accuracy (>80% node prediction accuracy) during pre-training, indicating stable dual-objective learning.
- Transfer learning performance on downstream bioactivity regression (e.g., predicting compound activity) shows >10% improvement in RMSE or R² compared to random initialization or synthetic molecule pre-training baseline.
- Scaffold-level analysis reveals that molecules sharing evolutionary lineage (same biosynthetic pathway or gene cluster origin) have cosine similarity >0.7 in the learned embedding space.

## Limitations

- Pre-training requires access to large, high-quality natural product SMILES datasets with consistent scaffold annotations; limited or noisy data will not reliably encode evolutionary patterns.
- Contrastive learning sensitivity to temperature parameter (τ) and batch size may require hyperparameter tuning for different natural product datasets; the paper demonstrates τ=0.2 but does not provide generalization rules.
- Masked graph modeling assumes graph connectivity and node/edge features are meaningful proxies for evolutionary information; this may fail if scaffold extraction is incomplete or side-chain diversity is low.
- Downstream task performance depends critically on fine-tuning hyperparameters (learning rate, early stopping patience, dropout); the paper recommends parameter adjustment 'depending on the dataset and training environment' without prescriptive guidance.
- Interpretability of learned patterns relies on post-hoc analysis (gene/microbial level clustering); the model does not explicitly output biological reasoning for predictions.

## Evidence

- [intro] Our method integrates contrastive learning with masked graph modeling, effectively encoding scaffold-derived evolutionary patterns alongside diverse side-chain information: "Our method integrates contrastive learning with masked graph modeling, effectively encoding scaffold-derived evolutionary patterns alongside diverse side-chain information"
- [intro] conventional molecular representation techniques are not well-suited to the unique structural and evolutionary features of natural products: "conventional molecular representation techniques are not well-suited to the unique structural and evolutionary features of natural products"
- [intro] We first benchmark NaFM on taxonomy classification against models pre-trained on synthetic molecules, demonstrating their inadequacy for capturing natural synthesis patterns: "We first benchmark NaFM on taxonomy classification against models pre-trained on synthetic molecules, demonstrating their inadequacy for capturing natural synthesis patterns"
- [intro] Through detailed analysis at both gene and microbial levels, NaFM reveals a strong capacity for learning evolutionary information: "Through detailed analysis at both gene and microbial levels, NaFM reveals a strong capacity for learning evolutionary information"
- [readme] python train.py --conf examples/Pretrain.yml: "python train.py --conf examples/Pretrain.yml"
- [readme] First, convert your SMILES data to a `.csv` file and place it in `raw_data/raw`. Then run: cd NaFM/raw_data/raw python filter.py: "convert your SMILES data to a `.csv` file and place it in `raw_data/raw`. Then run: cd NaFM/raw_data/raw python filter.py"
- [readme] This will standardize SMILES, remove salt and duplicate atoms, and generate `pretrain_smiles.pkl`: "This will standardize SMILES, remove salt and duplicate atoms, and generate `pretrain_smiles.pkl`"
