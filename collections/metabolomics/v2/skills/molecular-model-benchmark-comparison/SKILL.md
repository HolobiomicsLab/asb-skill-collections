---
name: molecular-model-benchmark-comparison
description: Use when when you have (1) a candidate foundation model or pre-trained
  weights for natural products (e.g., NaFM), (2) one or more baseline models pre-trained
  on synthetic molecules (e.g., ChemBERTa, MolBERT), (3) a held-out test set from
  a downstream task (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0209
  tools:
  - NaFM
  - PyTorch Lightning
  - scikit-learn
  - train.py
  - inference.py
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1002/anie.202507483
  title: NA
evidence_spans: []
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

# molecular-model-benchmark-comparison

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Systematically evaluate a natural product foundation model (NaFM) against baseline models pre-trained on synthetic molecules on the same held-out test set, using unified metrics (accuracy, precision, recall, F1-score per taxonomy class) to quantify performance differences and demonstrate domain-specific advantages. This skill surfaces when assessing whether domain-specialized pre-training (natural products vs. synthetic chemistry) captures task-relevant structural and evolutionary patterns.

## When to use

When you have (1) a candidate foundation model or pre-trained weights for natural products (e.g., NaFM), (2) one or more baseline models pre-trained on synthetic molecules (e.g., ChemBERTa, MolBERT), (3) a held-out test set from a downstream task (e.g., taxonomy classification, bioactivity regression), and (4) the goal is to demonstrate that domain-specialized pre-training outperforms generic molecular representations. Use this skill specifically when the research question asks whether conventional synthetic-molecule pre-training is adequate for capturing natural synthesis patterns, evolutionary information, or scaffold-derived features.

## When NOT to use

- You only have a single model and no baselines to compare against; this skill requires ≥2 models on the same test set.
- Your test set or baseline weights are not available; fair benchmarking requires identical held-out data and reproducible model initialization.
- The downstream task is not on natural product data (e.g., pure synthetic chemistry benchmark); the skill's rationale is to demonstrate NaFM's advantage on natural product datasets where synthetic pre-training falls short.

## Inputs

- Pre-trained model checkpoint for candidate model (NaFM.ckpt or equivalent PyTorch Lightning .ckpt file)
- Pre-trained baseline model checkpoints (e.g., ChemBERTa, MolBERT weights or downloadable models)
- Downstream task dataset with SMILES and labels (e.g., CSV with 'SMILES' column and taxonomy class or bioactivity target); example: downstream_data/Ontology/raw/classification_data.csv
- Train/validation/test split indices or configuration
- Model architecture and hyperparameter configuration files (YAML, e.g., examples/Finetune.yml)

## Outputs

- Per-model evaluation metrics table (accuracy, precision, recall, F1-score for each taxonomy class or task target)
- Performance comparison summary (e.g., NaFM vs. each baseline with metric differences and statistical significance)
- Model-specific per-class or per-task breakdowns (CSV or DataFrame format)
- Predictions or embeddings from each model on the test set (for downstream error analysis)
- Visualizations (e.g., F1-score bar plots, confusion matrices, or heatmaps comparing models)

## How to apply

Load the pre-trained NaFM model weights from the official checkpoint (NaFM.ckpt) and each baseline model (e.g., ChemBERTa, MolBERT) into compatible inference environments. Split your downstream task dataset (e.g., Ontology for taxonomy classification) into train/validation/test sets, keeping test held-out. Fine-tune each model on the same training set with controlled hyperparameters (learning rate ~1.0e-4, batch size 256, early stopping patience 50) to ensure fair comparison. Evaluate all models on the identical held-out test set, computing accuracy, precision, recall, and F1-score for each taxonomy class or task target. Generate a summary comparison table showing metric differences, per-class breakdown, and report statistical significance (e.g., via paired t-tests or cross-validation fold variance). Document any performance gaps; gaps favoring NaFM on natural product datasets indicate that models pre-trained on synthetic molecules lack sufficient inductive bias for capturing natural synthesis patterns.

## Related tools

- **NaFM** (Pre-trained foundation model for natural products; candidate model being benchmarked) — https://github.com/TomAIDD/NaFM-Official
- **PyTorch Lightning** (Training and inference framework for loading checkpoints, fine-tuning, and evaluation)
- **scikit-learn** (Metrics computation (precision, recall, F1-score, confusion matrix) and statistical testing)
- **train.py** (Main training script for fine-tuning candidate and baseline models on downstream task) — https://github.com/TomAIDD/NaFM-Official
- **inference.py** (Inference script to generate model predictions and embeddings on held-out test set) — https://github.com/TomAIDD/NaFM-Official

## Examples

```
python train.py --task finetune --num-epochs 300 --emb-dim 1024 --dataset Ontology --dataset-root downstream_data/Ontology --pretrained-path NaFM.ckpt --lr 1.0e-4 --batch-size 256 --seed 0 && python inference.py --task classification --downstream-data downstream_data/Ontology/raw/classification_data.csv --checkpoint-path [finetuned_model_path]
```

## Evaluation signals

- All models evaluated on identical held-out test set (no train/val leakage); verify by cross-checking data splits and random seeds.
- Per-class metrics are reported for each model; compare F1-scores and check for statistical significance (e.g., paired t-test across folds, p < 0.05).
- NaFM metric values should exceed baseline metric values on natural product tasks (e.g., Ontology, Lotus, Bgc datasets); if NaFM F1 < baseline F1, the comparison is invalid or the hypothesis is rejected.
- Hyperparameters (learning rate, batch size, early stopping patience) are held constant across all models to isolate pre-training effects; verify config files match or are documented.
- Per-class breakdown reveals which taxonomy levels (Class, Superclass, Pathway) benefit most from NaFM's evolutionary and scaffold-aware pre-training; inspect confusion matrices for class-specific improvements.

## Limitations

- The evaluation scripts in test.py are lightweight demonstrations intended to illustrate basic inference workflow and input/output usage, not the exact production evaluation pipeline used to generate the benchmark results reported in the paper; adapt for production use.
- Minor downstream task parameter adjustment (learning rate, training epochs, early stopping patience) may be required depending on dataset and training environment; results on new datasets may require hyperparameter tuning.
- Benchmarking relies on fair checkpoint reproducibility and identical data splits; differences in random seed initialization, PyTorch/CUDA versions, or data preprocessing can affect comparisons.
- The skill compares across models but does not control for model size, number of parameters, or computational cost; a smaller baseline may underperform for reasons unrelated to pre-training domain.

## Evidence

- [intro] We first benchmark NaFM on taxonomy classification against models pre-trained on synthetic molecules, demonstrating their inadequacy for capturing natural synthesis patterns: "We first benchmark NaFM on taxonomy classification against models pre-trained on synthetic molecules, demonstrating their inadequacy for capturing natural synthesis patterns"
- [other] Models pre-trained on synthetic molecules demonstrate inadequacy for capturing natural synthesis patterns in taxonomy classification tasks: "Models pre-trained on synthetic molecules demonstrate inadequacy for capturing natural synthesis patterns in taxonomy classification tasks, as revealed through NaFM benchmarking"
- [other] Evaluate NaFM on the held-out test set, computing accuracy, precision, recall, and F1-score for each taxonomy class. Load baseline models pre-trained on synthetic molecules (e.g., ChemBERTa, MolBERT, or other standard molecular pre-training frameworks). Evaluate each baseline model on the same test set using identical metrics.: "Evaluate NaFM on the held-out test set, computing accuracy, precision, recall, and F1-score for each taxonomy class. Load baseline models pre-trained on synthetic molecules (e.g., ChemBERTa, MolBERT,"
- [readme] Note: The configs under examples/ are example settings used for running the provided tasks. Some downstream tasks may require minor adjustment of parameters such as learning rate, training epochs, or early stopping patience depending on the dataset and training environment.: "Some downstream tasks may require minor adjustment of parameters such as learning rate, training epochs, or early stopping patience depending on the dataset and training environment"
- [readme] In particular, test.py should be regarded as a minimal demonstration template rather than the exact production evaluation pipeline used to generate the benchmark results reported in the paper.: "In particular, test.py should be regarded as a minimal demonstration template rather than the exact production evaluation pipeline used to generate the benchmark results reported in the paper"
