---
name: machine-learning-model-selection-and-comparison
description: Use when when you have a preprocessed metabolomics feature matrix with labeled samples and need to determine which classifier (traditional ML vs. deep learning) predicts the phenotype of interest.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - Lilikoi v2.0
  - R
  - h2o
derived_from:
- doi: 10.1093/gigascience/giaa162
  title: Lilikoi V2.0
evidence_spans:
- The new Lilikoi v2.0 R package has implemented a deep-learning method for classification, in addition to popular machine learning methods.
- Lilikoi v2.0 is a modern, comprehensive package to enable metabolomics analysis in R programming environment.
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
---

# machine-learning-model-selection-and-comparison

## Summary

Systematically train and evaluate multiple machine learning and deep learning classifiers on a preprocessed metabolomics feature matrix to identify the best-performing model for disease classification. This skill enables empirical comparison of algorithm performance across standardized cross-validation folds.

## When to use

When you have a preprocessed metabolomics feature matrix with labeled samples and need to determine which classifier (traditional ML vs. deep learning) best predicts the phenotype of interest. Apply this skill after feature selection or pathway aggregation, when you have a stable input matrix and require quantitative performance metrics (accuracy, sensitivity, specificity, AUC) to guide model selection for downstream prediction or clinical deployment.

## When NOT to use

- Input feature matrix is not yet aggregated or preprocessed (raw metabolite abundances without normalization or pathway transformation)
- Sample size is very small (< 20–30 samples) where cross-validation is unreliable; consider leave-one-out CV or nested CV instead
- Labels are missing or contain > 20% missingness; impute or exclude samples first

## Inputs

- Preprocessed metabolomics feature matrix (samples × features, normalized abundances or pathway scores)
- Sample labels/phenotype vector (binary or multiclass classification targets)
- Classifier configuration flags (boolean indicators for Rpart, LDA, SVM, RF, GBM, PAM, LOG, DL)
- Cross-validation and training parameters (trainportion, cvnum, dlround, nrun)

## Outputs

- Trained classifier objects (one per enabled algorithm)
- Performance metrics table (accuracy, sensitivity, specificity, AUC per classifier)
- Cross-validation fold predictions and probabilities
- Structured comparison output files suitable for visualization and reporting

## How to apply

Load the preprocessed feature matrix (e.g., pathway-derived scores or metabolite abundances) and corresponding sample labels into R. Initialize the Lilikoi v2.0 machine_learning module with configuration flags for desired classifiers (Rpart, LDA, SVM, RF, GBM, PAM, LOG, DL) and set key hyperparameters: trainportion (typically 0.8 for 80% training), cvnum (typically 10 for 10-fold cross-validation), dlround (50 rounds for deep learning iterations), and nrun (10 for multiple runs to assess stability). Execute all enabled classifiers in parallel on the same data splits to ensure fair comparison. Extract performance metrics (accuracy, sensitivity, specificity, AUC) from each trained model and aggregate into a structured comparison table. Select the best-performing classifier based on your primary metric (e.g., highest AUC or balanced sensitivity/specificity), then validate its generalization on a held-out test set.

## Related tools

- **Lilikoi v2.0** (R package that orchestrates multi-algorithm classification, integrates h2o for deep learning, manages cross-validation splits, and aggregates performance metrics) — https://github.com/lanagarmire/lilikoi2
- **h2o** (Deep learning backend invoked by Lilikoi for neural network–based classification (DL algorithm))
- **R** (Programming environment hosting Lilikoi v2.0 and supporting traditional ML classifiers (Rpart, LDA, SVM, RF, GBM, PAM, LOG))

## Examples

```
lilikoi.machine_learning(MLmatrix = Metadata, measurementLabels = Metadata$Label, significantPathways = 0, trainportion = 0.8, cvnum = 10, dlround=50, nrun=10, Rpart=TRUE, LDA=TRUE, SVM=TRUE, RF=TRUE, GBM=TRUE, PAM=FALSE, LOG=TRUE, DL=TRUE)
```

## Evaluation signals

- All enabled classifiers produce non-null performance metrics (no NaN or missing values in accuracy, AUC, sensitivity, specificity columns)
- Cross-validation fold assignments are consistent and non-overlapping (trainportion + test = 1.0; cvnum folds partition training data correctly)
- Performance metrics lie within valid ranges (0 ≤ accuracy, sensitivity, specificity, AUC ≤ 1.0)
- Deep learning (DL) model converges within dlround iterations without divergence (monitor loss trajectory); compare DL AUC to traditional classifiers to validate integration
- Comparison table rows correspond to nrun independent runs per classifier; verify stability by checking coefficient of variation (CV) of AUC across runs (CV < 10% suggests stable ranking)

## Limitations

- Deep learning performance depends heavily on sample size; Lilikoi DL may underperform on small cohorts (< 100 samples) relative to regularized traditional ML
- No built-in hyperparameter optimization; dlround, trainportion, and cvnum are fixed by user; extensive tuning requires external grid search
- Imbalanced class labels may inflate accuracy; prioritize sensitivity, specificity, and AUC when classes are skewed
- Cross-validation fold stratification is not explicitly documented in the README; class distribution may differ across folds if not stratified

## Evidence

- [other] Finding: Classifier support and parameters: "The Lilikoi v2.0 machine_learning module accepts an expression matrix and labels, supports multiple classifiers (Rpart, LDA, SVM, RF, GBM, PAM, LOG, and DL), and provides configurable parameters"
- [other] Workflow: Training and aggregation: "Execute traditional machine learning classifiers (e.g., support vector machines, random forests, logistic regression) as implemented in Lilikoi v2.0. Execute the deep learning classifier via h2o"
- [intro] Tool capability: Deep learning integration: "The new Lilikoi v2.0 R package has implemented a deep-learning method for classification, in addition to popular machine learning methods."
- [readme] Example invocation: lilikoi.machine_learning call: "lilikoi.machine_learning(MLmatrix = Metadata, measurementLabels = Metadata$Label, significantPathways = 0, trainportion = 0.8, cvnum = 10, dlround=50,nrun=10, Rpart=TRUE,"
