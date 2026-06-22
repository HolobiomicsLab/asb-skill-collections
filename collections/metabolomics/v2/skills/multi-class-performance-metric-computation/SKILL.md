---
name: multi-class-performance-metric-computation
description: Use when when evaluating a taxonomy classification model on held-out natural product data where multiple classes exist (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3324
  tools:
  - inference.py
  - scikit-learn classification_report
  - train.py with --task finetune
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# multi-class-performance-metric-computation

## Summary

Compute classification performance metrics (accuracy, precision, recall, F1-score) per taxonomy class to evaluate model performance on hierarchical natural product classification tasks. This skill enables comparative benchmarking across models by quantifying how well each class is predicted.

## When to use

When evaluating a taxonomy classification model on held-out natural product data where multiple classes exist (e.g., Class, Superclass, or Pathway levels in the Ontology dataset) and you need to assess whether performance varies systematically across classes, particularly to benchmark synthetic-molecule pre-trained models against NaFM.

## When NOT to use

- Input is already a pre-computed metric table or summary report — skip directly to comparison/visualization.
- Test set has severe class imbalance (>100:1) without stratification — macro-averaging will be misleading; use weighted metrics or class-balanced sampling instead.
- Predictions have not been generated yet — first run inference.py to obtain model predictions on the test set.

## Inputs

- finetuned model checkpoint (.ckpt file)
- held-out test set with SMILES and class labels (CSV with 'SMILES' column and class column)
- model architecture configuration (embedding dimension, feature dimension, number of layers, etc.)
- class hierarchy/mapping if using hierarchical taxonomy levels (Class, Superclass, Pathway)

## Outputs

- per-class accuracy, precision, recall, F1-score table (CSV or DataFrame)
- macro-averaged and weighted-averaged aggregate metrics
- confusion matrix (for visualization and error analysis)
- statistical significance test results (p-values, effect sizes)

## How to apply

Load the finetuned model checkpoint and the held-out test set split from your downstream dataset (e.g., downstream_data/Ontology/raw/classification_data.csv). Run inference on all test samples to obtain predicted class labels. For each taxonomy class, compute accuracy (fraction of correct predictions), precision (true positives / (true positives + false positives)), recall (true positives / (true positives + false negatives)), and F1-score (harmonic mean of precision and recall). Aggregate these metrics into a summary table indexed by class, then calculate summary statistics (macro-average, weighted-average) across classes. Use scikit-learn's classification_report or similar to ensure consistent computation. Compare baseline and NaFM metrics by computing per-class differences and applying statistical significance tests (e.g., McNemar's test) to determine whether NaFM's superior performance on specific classes is statistically justified.

## Related tools

- **inference.py** (Generate predicted class labels on test set for downstream metric computation) — https://github.com/TomAIDD/NaFM-Official
- **scikit-learn classification_report** (Compute precision, recall, F1-score, and support per class automatically)
- **train.py with --task finetune** (Finetuned model checkpoint generation on Ontology or other downstream datasets) — https://github.com/TomAIDD/NaFM-Official

## Examples

```
python inference.py --task classification --downstream-data downstream_data/Ontology --checkpoint-path finetuned_model.ckpt; then compute metrics using: from sklearn.metrics import classification_report; print(classification_report(y_test, y_pred, output_dict=True))
```

## Evaluation signals

- All per-class metrics (accuracy, precision, recall, F1-score) are in range [0, 1] and consistent with confusion matrix counts.
- Macro-averaged F1-score equals the mean of per-class F1-scores; weighted F1-score reflects class distribution in test set.
- Sum of support values across all classes equals total number of test samples; no class is missing or double-counted.
- For NaFM vs. synthetic pre-trained baseline comparison: NaFM shows statistically significant higher F1-score on at least 50% of taxonomy classes (p < 0.05 by McNemar's test), supporting the claim that synthetic models are inadequate for natural synthesis patterns.
- Class imbalance is documented (e.g., largest class has ≤ 10× samples of smallest class); if violated, weighted metrics and per-class confidence intervals are reported.

## Limitations

- Evaluation scripts (test.py) in the repository are minimal demonstration templates, not production-grade evaluation pipelines; they may not fully reproduce benchmark results reported in the paper.
- Macro-averaging treats all classes equally regardless of prevalence; weighted averaging is more appropriate for imbalanced datasets, but may obscure poor performance on rare classes.
- Statistical significance testing (e.g., McNemar's test) requires paired predictions from both NaFM and baseline on identical test samples; if train/test splits differ between models, comparisons are confounded.
- Hyperparameter sensitivity (learning rate, batch size, early stopping patience) can affect finetuned checkpoint performance; reported metrics depend on the configuration used (see examples/Finetune.yml for defaults).

## Evidence

- [other] Evaluate NaFM on the held-out test set, computing accuracy, precision, recall, and F1-score for each taxonomy class.: "Evaluate NaFM on the held-out test set, computing accuracy, precision, recall, and F1-score for each taxonomy class."
- [other] Compare NaFM performance against baselines and generate a summary table showing metric differences and statistical significance.: "Compare NaFM performance against baselines and generate a summary table showing metric differences and statistical significance."
- [intro] We first benchmark NaFM on taxonomy classification against models pre-trained on synthetic molecules, demonstrating their inadequacy for capturing natural synthesis patterns.: "We first benchmark NaFM on taxonomy classification against models pre-trained on synthetic molecules, demonstrating their inadequacy for capturing natural synthesis patterns."
- [readme] test.py should be regarded as a minimal demonstration template rather than the exact production evaluation pipeline used to generate the benchmark results reported in the paper.: "test.py should be regarded as a minimal demonstration template rather than the exact production evaluation pipeline used to generate the benchmark results reported in the paper."
- [readme] Supports hierarchical classification at Class, Superclass, and Pathway levels.: "Supports hierarchical classification at Class, Superclass, and Pathway levels."
