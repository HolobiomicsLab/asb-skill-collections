---
name: classification-performance-metric-evaluation
description: Use when after training multiple classifiers (traditional ML and deep
  learning) on a preprocessed metabolomics feature matrix with labeled samples, and
  you need to quantify and compare their predictive performance to select the model
  or ensemble for downstream analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - Lilikoi v2.0
  - R
  - h2o
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1093/gigascience/giaa162
  title: Lilikoi V2.0
evidence_spans:
- The new Lilikoi v2.0 R package has implemented a deep-learning method for classification,
  in addition to popular machine learning methods.
- Lilikoi v2.0 is a modern, comprehensive package to enable metabolomics analysis
  in R programming environment.
- DL via h2o
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lilikoi_v2_0_cq
    doi: 10.1093/gigascience/giaa162
    title: Lilikoi V2.0
  dedup_kept_from: coll_lilikoi_v2_0_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/gigascience/giaa162
  all_source_dois:
  - 10.1093/gigascience/giaa162
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# classification-performance-metric-evaluation

## Summary

Aggregate and compare performance metrics (accuracy, sensitivity, specificity, AUC) across multiple trained machine learning and deep learning classifiers on metabolomics data. This skill validates classifier performance through multi-algorithm benchmarking and structured metric compilation.

## When to use

After training multiple classifiers (traditional ML and deep learning) on a preprocessed metabolomics feature matrix with labeled samples, and you need to quantify and compare their predictive performance to select the best model or ensemble for downstream analysis.

## When NOT to use

- Training data and test data have not been properly separated (e.g., metrics computed on training set only — causes overfitting bias).
- Only one classifier has been trained (no comparison or competitive evaluation is possible).
- Labels are missing or inconsistent across samples (cannot compute sensitivity/specificity or validate predictions).

## Inputs

- trained classifier objects (one per algorithm: Rpart, LDA, SVM, RF, GBM, PAM, LOG, DL)
- test/hold-out metabolomics feature matrix (rows=samples, columns=metabolites or pathway signatures)
- corresponding sample labels (binary or multi-class phenotype)
- cross-validation fold assignments (from cvnum parameter)

## Outputs

- performance metrics table (rows=algorithms, columns=accuracy, sensitivity, specificity, AUC)
- ranked classifier list (sorted by primary metric, e.g., AUC)
- per-classifier model objects and trained parameters
- structured output files containing aggregated results

## How to apply

Execute each trained classifier on held-out test data (held out via trainportion parameter, e.g., 0.8 train/0.2 test split) and cross-validation folds (cvnum, e.g., 10 folds). Extract per-classifier metrics: accuracy (overall correct predictions), sensitivity (true positive rate), specificity (true negative rate), and AUC (area under ROC curve). Aggregate these metrics into a structured comparison table across all methods (Rpart, LDA, SVM, RF, GBM, PAM, LOG, DL). Sort or rank by primary metric (e.g., AUC) to identify the highest-performing classifier. Store both model objects and the performance comparison table as structured outputs for reproducibility and visualization.

## Related tools

- **Lilikoi v2.0** (Integrates machine learning classifiers (Rpart, LDA, SVM, RF, GBM, PAM, LOG) and h2o deep learning; orchestrates training and metric extraction across all algorithms) — https://github.com/lanagarmire/lilikoi2
- **R** (Programming environment for executing classifier training and metric computation via Lilikoi v2.0)
- **h2o** (Deep learning framework integrated into Lilikoi v2.0 for training DL classifiers and extracting performance metrics)

## Examples

```
lilikoi.machine_learning(MLmatrix = Metadata, measurementLabels = Metadata$Label, significantPathways = 0, trainportion = 0.8, cvnum = 10, dlround=50, nrun=10, Rpart=TRUE, LDA=TRUE, SVM=TRUE, RF=TRUE, GBM=TRUE, PAM=FALSE, LOG=TRUE, DL=TRUE)
```

## Evaluation signals

- All trained classifiers have corresponding metric rows in the output table with no NaN or missing values for accuracy, sensitivity, specificity, AUC.
- Metrics are in valid ranges: accuracy, sensitivity, specificity, AUC ∈ [0, 1]; test set size matches (1 − trainportion) × total samples.
- Cross-validation results show consistency: standard deviation or confidence intervals on metrics are reasonable (not extreme variance suggesting data leakage or instability).
- Comparison table is sortable by metric and reproducible: same random seed produces identical metric values across runs.
- Deep learning (DL) classifier metrics are present, confirming h2o integration executed successfully alongside traditional ML methods.

## Limitations

- Metric comparison is meaningful only if all classifiers are trained on the same train/test split and cross-validation folds; inconsistent sampling invalidates comparison.
- Class imbalance in metabolomics phenotypes can inflate accuracy but deflate sensitivity/specificity; AUC is more robust but all four metrics should be inspected.
- Small sample sizes typical in metabolomics studies may lead to unstable metric estimates; cross-validation helps but does not eliminate variance.
- Deep learning (dlround=50 rounds, nrun=10 iterations) may require careful hyperparameter tuning; no automated optimization is described in the article.

## Evidence

- [other] supports multiple classifiers (Rpart, LDA, SVM, RF, GBM, PAM, LOG, and DL), and provides configurable parameters including trainportion (0.8), cvnum (10 folds), dlround (50 rounds for deep learning), and nrun (10 iterations): "The Lilikoi v2.0 machine_learning module accepts an expression matrix and labels, supports multiple classifiers (Rpart, LDA, SVM, RF, GBM, PAM, LOG, and DL), and provides configurable parameters"
- [other] extract performance metrics (accuracy, sensitivity, specificity, AUC) for each method. Compile results into structured output files containing model objects and performance comparison table.: "Aggregate trained classifier objects and extract performance metrics (accuracy, sensitivity, specificity, AUC) for each method. 6. Compile results into structured output files containing model"
- [readme] The new Lilikoi v2.0 R package has implemented a deep-learning method for classification, in addition to popular machine learning methods.: "The new Lilikoi v2 R package has implemented a deep-learning method for classification, in addition to popular machine learning methods."
- [readme] lilikoi.machine_learning function with multiple algorithm flags (Rpart, LDA, SVM, RF, GBM, PAM, LOG, DL) and cross-validation parameters: "lilikoi.machine_learning(MLmatrix = Metadata, measurementLabels = Metadata$Label, significantPathways = 0, trainportion = 0.8, cvnum = 10, dlround=50, nrun=10, Rpart=TRUE, LDA=TRUE, SVM=TRUE,"
