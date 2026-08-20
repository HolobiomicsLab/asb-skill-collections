---
name: foundation-model-prediction-generation
description: Use when you have a pre-trained foundation model checkpoint (e.g., NaFM.ckpt)
  and new molecules represented as SMILES strings or a CSV file, and you need to generate
  predictions (e.g., bioactivity scores, taxonomy class, screening rankings) or embeddings
  for downstream analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3474
  - http://edamontology.org/topic_3407
  tools:
  - PyTorch
  - Git
  - PyTorch Lightning
  - inference.py
  - scikit-learn
  license_tier: restricted
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

# foundation-model-prediction-generation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Use a pre-trained foundation model to generate molecular embeddings and predictions on downstream tasks (classification, regression, or virtual screening) by loading pre-trained weights and running inference on new molecular data. This skill leverages learned evolutionary and structural patterns to produce bioactivity predictions or molecular representations without task-specific retraining.

## When to use

You have a pre-trained foundation model checkpoint (e.g., NaFM.ckpt) and new molecules represented as SMILES strings or a CSV file, and you need to generate predictions (e.g., bioactivity scores, taxonomy class, screening rankings) or embeddings for downstream analysis. Particularly useful when your molecules are natural products or derivatives thereof, and existing synthetic-molecule models underperform.

## When NOT to use

- Input molecules are highly synthetic (e.g., combinatorial libraries or fully synthetic compounds) — foundation models pre-trained on synthetic molecules may be more suitable.
- Pre-trained weights are not available or incompatible with your PyTorch/CUDA version.
- You need to adapt the model to a novel task not covered in the pre-training objective (e.g., a task requiring task-specific architectural changes) — fine-tuning would be more appropriate.

## Inputs

- Pre-trained model checkpoint file (PyTorch Lightning .ckpt)
- Molecular data as CSV file with 'SMILES' column
- Task specification (classification, regression, or virtual screening)
- Model configuration (embedding dimension, number of layers, dropout ratio)

## Outputs

- Predictions CSV file with SMILES, predicted labels/scores, and confidence values
- Molecular embeddings (optional, for downstream analysis)
- Ranking or retrieval metrics for virtual screening tasks

## How to apply

Load the pre-trained model checkpoint using the inference script, prepare your input data as a CSV file with a 'SMILES' column, specify the task type (classification or regression), and run the inference.py script with the checkpoint path and data location. The model will encode each molecule into learned representations capturing scaffold-derived evolutionary patterns and side-chain information, then apply the task-specific head (classifier or regressor) to produce outputs. Save predictions to a results file and validate that output schema matches expected format (class labels or numeric scores with confidence ranges).

## Related tools

- **PyTorch** (Deep learning framework for loading and executing the pre-trained model graph)
- **PyTorch Lightning** (Checkpoint management and inference orchestration for the NaFM model)
- **inference.py** (Primary inference script for generating predictions on new molecular data) — https://github.com/TomAIDD/NaFM-Official
- **scikit-learn** (Compute evaluation metrics (e.g., ranking accuracy, retrieval scores) on predictions)

## Examples

```
python inference.py --task classification --downstream-data downstream_data/Ontology/raw/classification_data.csv --checkpoint-path NaFM.ckpt
```

## Evaluation signals

- Output CSV contains all input SMILES with corresponding predictions and no null/NaN values in prediction columns.
- Prediction scores are within the expected range (class indices for classification, numeric values for regression, 0–1 for probabilities).
- For classification tasks, predicted class labels match the ontology or dataset schema (e.g., valid taxonomy classes, pathway codes).
- For virtual screening, ranking metrics (e.g., hit rate, area under curve on ranked retrieval) match or exceed baseline performance reported in the paper (SOTA on downstream benchmarks).
- Model inference time per molecule is consistent with batch processing efficiency (no sudden crashes or GPU memory errors).

## Limitations

- The provided inference scripts (test.py and inference.py) are demonstration templates rather than production pipelines — parameter tuning (learning rate, batch size, early stopping patience) may be required for novel datasets.
- Pre-trained weights encode patterns from natural product training corpora; performance on highly synthetic or non-drug-like molecules is not guaranteed.
- Virtual screening results depend on dataset composition and domain alignment; external or proprietary screening libraries may require retraining or fine-tuning.
- Model evaluation is sensitive to SMILES standardization and salt/duplicate removal; inconsistent preprocessing can degrade prediction quality.

## Evidence

- [readme] For inference on new molecules (CSV with a "SMILES" column): python inference.py --task classification --downstream-data [data location] --checkpoint-path [your finetuned model path]: "For inference on new molecules (CSV with a "SMILES" column)"
- [intro] The proposed framework achieves state-of-the-art (SOTA) performance across a wide range of downstream tasks in natural product mining and drug discovery: "The proposed framework achieves state-of-the-art (SOTA) performance across a wide range of downstream tasks in natural product mining and drug discovery"
- [intro] Our method integrates contrastive learning with masked graph modeling, effectively encoding scaffold-derived evolutionary patterns alongside diverse side-chain information: "Our method integrates contrastive learning with masked graph modeling, effectively encoding scaffold-derived evolutionary patterns alongside diverse side-chain information"
- [intro] NaFM reveals a strong capacity for learning evolutionary information: "NaFM reveals a strong capacity for learning evolutionary information"
- [readme] Results will be saved to NaFM/predictions.csv: "Results will be saved to NaFM/predictions.csv"
