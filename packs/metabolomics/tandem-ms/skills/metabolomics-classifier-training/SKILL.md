---
name: metabolomics-classifier-training
description: Use when you have a preprocessed metabolomics feature matrix (expression matrix with metabolite abundances as columns and samples as rows) with corresponding binary or multi-class sample labels, and you need to train and compare classifier performance to select the -performing model for disease.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0091
  tools:
  - Lilikoi v2.0
  - R
  - h2o
  techniques:
  - tandem-MS
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/gigascience/giaa162
  all_source_dois:
  - 10.1093/gigascience/giaa162
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomics-classifier-training

## Summary

Train and compare multiple machine learning and deep learning classifiers on preprocessed metabolomics feature matrices to discriminate sample phenotypes. This skill integrates traditional algorithms (SVM, RF, GBM, LDA, logistic regression) with h2o-based deep learning to enable multi-algorithm model selection and performance benchmarking on metabolomics classification tasks.

## When to use

Apply this skill when you have a preprocessed metabolomics feature matrix (expression matrix with metabolite abundances as columns and samples as rows) with corresponding binary or multi-class sample labels, and you need to train and compare classifier performance to select the best-performing model for disease classification or phenotype discrimination.

## When NOT to use

- Input is raw, unpreprocessed metabolomics data (e.g., still contains missing values, batch effects, or uninformative features) — apply preprocessing and feature selection before classifier training.
- Sample size is very small (n < 20) relative to feature count — use dimensionality reduction or pathway-aggregated features (e.g., PDSmatrix from lilikoi.PDSfun) before training.
- Labels are continuous (e.g., disease severity scores) rather than categorical — use prognosis prediction (lilikoi.prognosis with Cox-PH or Cox-nnet) instead.

## Inputs

- Preprocessed metabolomics feature matrix (samples × metabolites, numeric)
- Sample phenotype labels (binary or multi-class factor or character vector)
- Metabolomics data object from lilikoi.Loaddata() containing Metadata and dataSet

## Outputs

- Trained classifier model objects (Rpart, LDA, SVM, RF, GBM, PAM, LOG, DL) for each algorithm
- Performance metrics table (accuracy, sensitivity, specificity, AUC per classifier)
- Cross-validation results and model comparison summary
- Structured output files containing aggregated models and performance rankings

## How to apply

Load the preprocessed metabolomics feature matrix and corresponding sample labels into R. Initialize the Lilikoi v2.0 machine_learning module with classifier configuration flags (Rpart, LDA, SVM, RF, GBM, PAM, LOG, DL) and key hyperparameters: trainportion (default 0.8 for train/test split), cvnum (10-fold cross-validation), dlround (50 rounds for h2o deep learning), and nrun (10 iterations for repeated runs). Execute each enabled classifier sequentially, which trains models on the training partition and evaluates on held-out test data. Extract performance metrics (accuracy, sensitivity, specificity, AUC) for each method. Aggregate trained model objects and compile results into a structured comparison table to identify the classifier with the highest overall performance or best sensitivity/specificity trade-off for your phenotype of interest.

## Related tools

- **Lilikoi v2.0** (R package implementing machine_learning module with support for multiple classifiers (Rpart, LDA, SVM, RF, GBM, PAM, LOG) and h2o deep learning integration) — https://github.com/lanagarmire/lilikoi2
- **h2o** (Deep learning framework integrated into Lilikoi v2.0 for neural network-based classification with configurable rounds (dlround parameter))
- **R** (Programming environment for executing Lilikoi v2.0 machine learning pipeline)

## Examples

```
lilikoi.machine_learning(MLmatrix = Metadata, measurementLabels = Metadata$Label, significantPathways = 0, trainportion = 0.8, cvnum = 10, dlround = 50, nrun = 10, Rpart = TRUE, LDA = TRUE, SVM = TRUE, RF = TRUE, GBM = TRUE, PAM = FALSE, LOG = TRUE, DL = TRUE)
```

## Evaluation signals

- All enabled classifier models are trained and return valid model objects without errors.
- Cross-validation results show consistent performance across all cv folds (low variance in fold-wise accuracy/AUC indicates stable model).
- Performance metrics (accuracy, sensitivity, specificity, AUC) are within valid ranges [0, 1] and sum-of-class accuracies are consistent with overall accuracy.
- Test set performance (held-out partition) is comparable to cross-validation performance (within ~5–10%), indicating no severe overfitting.
- Deep learning model (DL) converges within dlround=50 iterations; inspect loss curves to confirm training stability.

## Limitations

- Default train/test split (trainportion=0.8) is fixed; no stratification mentioned — may lead to class imbalance in folds for imbalanced datasets.
- Deep learning hyperparameters (dlround=50, nrun=10) are hard-coded defaults; no guidance provided for tuning on small sample sizes (n < 100).
- No automatic feature scaling or normalization is documented as part of the classifier module; assumes input matrix is already appropriately normalized.
- Classifier comparison is based on cross-validation and held-out test metrics only; no statistical significance testing (e.g., McNemar test) is mentioned to compare classifier pairs.

## Evidence

- [readme] multiclassifier_support: "The Lilikoi v2.0 machine_learning module accepts an expression matrix and labels, supports multiple classifiers (Rpart, LDA, SVM, RF, GBM, PAM, LOG, and DL)"
- [readme] configurable_parameters: "and provides configurable parameters including trainportion (0.8), cvnum (10 folds), dlround (50 rounds for deep learning), and nrun (10 iterations)"
- [intro] deep_learning_method: "The new Lilikoi v2.0 R package has implemented a deep-learning method for classification, in addition to popular machine learning methods."
- [other] workflow_steps: "1. Load the preprocessed metabolomics feature matrix and corresponding sample labels into R. 2. Initialize the Lilikoi v2.0 machine learning classification module with the input matrix and classifier"
- [intro] h2o_integration: "The new Lilikoi v2.0 R package has implemented a deep-learning method for classification, in addition to popular machine learning methods."
