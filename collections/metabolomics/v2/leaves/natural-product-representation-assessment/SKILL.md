---
name: natural-product-representation-assessment
description: Use when you have a natural product dataset with taxonomy labels (Class,
  Superclass, or Pathway), pre-trained molecular models (both natural-product-specialized
  and synthetic-molecule baselines), and a question about whether standard molecular
  representations are sufficient for natural product.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3372
  tools:
  - NaFM
  - PyTorch Lightning
  - scikit-learn
  - ChemBERTa / MolBERT
  license_tier: restricted
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

# natural-product-representation-assessment

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Benchmark a natural-product-aware molecular representation model (e.g., NaFM) against synthetic-molecule pre-trained baselines on taxonomy classification tasks to quantify whether conventional representations adequately capture natural synthesis patterns and evolutionary information. This skill surfaces representational gaps that justify domain-specific pre-training.

## When to use

You have a natural product dataset with taxonomy labels (Class, Superclass, or Pathway), pre-trained molecular models (both natural-product-specialized and synthetic-molecule baselines), and a question about whether standard molecular representations are sufficient for natural product tasks. Use this skill when you need empirical evidence that conventional representations fail to encode natural synthesis or evolutionary patterns.

## When NOT to use

- Input data lacks taxonomy labels or uses only regression targets; use regression benchmarking instead.
- Baseline models are already fine-tuned on natural products; this skill targets comparison of pre-trained representations, not task-adapted models.
- Goal is to optimize hyperparameters for a single model; this is a comparative assessment, not hyperparameter tuning.

## Inputs

- Pre-trained NaFM model checkpoint (NaFM.ckpt)
- Pre-trained synthetic-molecule baseline model weights (e.g., ChemBERTa, MolBERT)
- Ontology taxonomy classification dataset (CSV with SMILES and Class/Superclass/Pathway labels)
- Train/validation/test split indices or stratified split specification

## Outputs

- Accuracy, precision, recall, and F1-score per taxonomy class for NaFM
- Accuracy, precision, recall, and F1-score per taxonomy class for each baseline
- Summary comparison table showing metric differences between NaFM and baselines
- Statistical significance test results (e.g., p-values from paired t-tests or McNemar's test)
- Analysis report documenting representational gaps (e.g., which taxonomy classes show largest NaFM advantage)

## How to apply

Load the NaFM pre-trained weights from the official repository and the Ontology taxonomy classification dataset, splitting into train/validation/test sets. Evaluate NaFM on the held-out test set, computing accuracy, precision, recall, and F1-score for each taxonomy class. In parallel, load baseline models pre-trained on synthetic molecules (e.g., ChemBERTa, MolBERT) and evaluate each on the identical test set using identical metrics. Compare performance via a summary table highlighting metric differences and assess statistical significance. The rationale is that NaFM integrates contrastive learning with masked graph modeling to encode scaffold-derived evolutionary patterns and side-chain information, whereas synthetic-molecule models lack these inductive biases; a substantial performance gap at the taxonomy level reveals representation inadequacy for natural products.

## Related tools

- **NaFM** (Pre-trained natural-product foundation model encoding scaffold and evolutionary patterns; primary model under assessment) — https://github.com/TomAIDD/NaFM-Official
- **PyTorch Lightning** (Training and evaluation framework for model loading and inference)
- **scikit-learn** (Metric computation (accuracy, precision, recall, F1) and statistical significance testing)
- **ChemBERTa / MolBERT** (Synthetic-molecule baseline models for comparative evaluation)

## Examples

```
python train.py --task finetune --dataset Ontology --dataset-root downstream_data/Ontology --pretrained-path NaFM.ckpt --dataset-arg Class --num-epochs 300 --batch-size 256 --log-dir results/nafm_taxonomy && python inference.py --task classification --downstream-data downstream_data/Ontology/raw/classification_data.csv --checkpoint-path results/nafm_taxonomy
```

## Evaluation signals

- NaFM achieves higher average F1-score across all taxonomy classes compared to synthetic-molecule baselines.
- Precision and recall are balanced (no >10 pp gap) for NaFM, indicating it does not spuriously favor one class.
- Baseline models show systematic underperformance on classes with high structural diversity or scaffold novelty in natural products.
- Statistical significance test (paired t-test or McNemar's test) yields p < 0.05 for at least one metric, confirming the performance gap is not due to chance.
- Per-class analysis shows baseline failures correlate with natural-product-specific structural features (e.g., complex scaffolds, rare biosynthetic motifs).

## Limitations

- Evaluation scripts (test.py) are lightweight demonstration templates, not the exact production pipeline used to generate reported benchmark results; minor hyperparameter tuning may be required for your dataset.
- The Ontology dataset is one instantiation; results may not generalize to other taxonomy schemas or external natural product collections without re-benchmarking.
- Comparison is restricted to models for which compatible pre-trained weights are available; unmaintained or proprietary baselines cannot be easily included.
- The README notes that configs in examples/ are example settings; downstream tasks may require adjustment of learning rate, epochs, or early stopping patience depending on dataset and compute environment.

## Evidence

- [intro] We first benchmark NaFM on taxonomy classification against models pre-trained on synthetic molecules, demonstrating their inadequacy for capturing natural synthesis patterns.: "We first benchmark NaFM on taxonomy classification against models pre-trained on synthetic molecules, demonstrating their inadequacy for capturing natural synthesis patterns"
- [intro] Our method integrates contrastive learning with masked graph modeling, effectively encoding scaffold-derived evolutionary patterns alongside diverse side-chain information.: "Our method integrates contrastive learning with masked graph modeling, effectively encoding scaffold-derived evolutionary patterns alongside diverse side-chain information"
- [other] Evaluate NaFM on the held-out test set, computing accuracy, precision, recall, and F1-score for each taxonomy class.: "Evaluate NaFM on the held-out test set, computing accuracy, precision, recall, and F1-score for each taxonomy class"
- [intro] conventional molecular representation techniques are not well-suited to the unique structural and evolutionary features of natural products.: "conventional molecular representation techniques are not well-suited to the unique structural and evolutionary features of natural products"
- [intro] The proposed framework achieves state-of-the-art (SOTA) performance across a wide range of downstream tasks in natural product mining and drug discovery.: "The proposed framework achieves state-of-the-art (SOTA) performance across a wide range of downstream tasks in natural product mining and drug discovery"
- [readme] Supports hierarchical classification at **Class**, **Superclass**, and **Pathway** levels.: "Supports hierarchical classification at **Class**, **Superclass**, and **Pathway** levels"
- [readme] The repository includes lightweight demonstration scripts intended to illustrate the basic inference workflow and input/output usage of NaFM. In particular, ```test.py``` should be regarded as a minimal demonstration template rather than the exact production evaluation pipeline used to generate the benchmark results reported in the paper.: "test.py should be regarded as a minimal demonstration template rather than the exact production evaluation pipeline used to generate the benchmark results reported in the paper"
