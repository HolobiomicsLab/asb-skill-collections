---
name: deep-learning-neural-network-optimization
description: Use when you have a preprocessed metabolomics expression matrix with labeled samples and need to compare deep learning performance against traditional classifiers (SVM, RF, GBM, LDA, LOG, Rpart, PAM), or when you need to build a prognosis model that incorporates non-linear interactions between.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_2275
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

# deep-learning-neural-network-optimization

## Summary

Train and optimize deep neural networks for metabolomics classification and prognosis prediction using the Lilikoi v2.0 h2o integration. This skill enables practitioners to configure and execute deep learning models as an alternative to traditional machine learning classifiers, with tunable hyperparameters for model rounds, cross-validation folds, and training/validation splits.

## When to use

Apply this skill when you have a preprocessed metabolomics expression matrix with labeled samples and need to compare deep learning performance against traditional classifiers (SVM, RF, GBM, LDA, LOG, Rpart, PAM), or when you need to build a prognosis model that incorporates non-linear interactions between metabolites and survival outcomes.

## When NOT to use

- Input data has fewer than ~100 samples; deep learning typically requires larger datasets than traditional methods and may overfit on small metabolomics cohorts.
- Preprocessed expression matrix has not undergone filtering or normalization; deep learning amplifies noise from raw feature matrices.
- Classification task is binary with highly separable classes; simpler methods (logistic regression, SVM) provide equivalent performance with faster training and interpretability.

## Inputs

- preprocessed metabolomics expression matrix (rows=metabolites, columns=samples)
- sample phenotype labels or classification vector
- event indicator vector (for prognosis models)
- time-to-event vector (for prognosis models)
- Lilikoi v2.0 configuration parameters (dlround, cvnum, trainportion, nrun)

## Outputs

- trained deep learning classifier object (h2o model)
- trained Cox-nnet prognosis model (if coxnnet=TRUE)
- performance metrics table (accuracy, sensitivity, specificity, AUC)
- C-index or concordance statistics (for prognosis)
- cross-validation fold predictions and probabilities

## How to apply

Load the preprocessed metabolomics feature matrix and corresponding sample labels (or event/time vectors for prognosis) into R. Initialize Lilikoi v2.0's machine_learning or prognosis module with the input data and set deep learning flags (DL=TRUE or coxnnet=TRUE). Configure key hyperparameters: dlround (default 50 rounds for deep learning iterations), cvnum (default 10 folds for cross-validation), trainportion (default 0.8 for train/test split), and nrun (default 10 iterations for ensemble stability). For prognosis, specify additional parameters including alpha (regularization strength), nfold (cross-validation folds), and method (quantile-based stratification). Execute the deep learning classifier via h2o backend and extract performance metrics (accuracy, sensitivity, specificity, AUC for classification; C-index for prognosis). Compare deep learning results against traditional classifiers in the aggregated performance table to determine if non-linear modeling provides clinically meaningful improvement.

## Related tools

- **Lilikoi v2.0** (R package wrapping h2o for deep learning classification and Cox-nnet prognosis on metabolomics data; provides machine_learning() and prognosis() modules) — github.com/lanagarmire/lilikoi2
- **h2o** (backend deep learning framework integrated into Lilikoi v2.0 for neural network training and optimization)
- **R** (scripting environment for Lilikoi v2.0 execution and result aggregation)

## Examples

```
lilikoi.machine_learning(MLmatrix = Metadata, measurementLabels = Metadata$Label, significantPathways = 0, trainportion = 0.8, cvnum = 10, dlround=50, nrun=10, DL=TRUE)
```

## Evaluation signals

- Deep learning model converges without divergence across dlround iterations (monitor h2o training loss curve).
- Cross-validation AUC and accuracy metrics are stable across cvnum folds (coefficient of variation < 10%).
- Deep learning performance metrics (AUC, sensitivity, specificity) are compared side-by-side with traditional classifiers in output table; improvement > 5% AUC indicates meaningful non-linear benefit.
- For prognosis: Cox-nnet C-index is higher than Cox-PH baseline; Kaplan-Meier curves stratified by predicted risk score show significant log-rank p-value (p < 0.05).
- Training and validation loss curves show no overfitting (validation loss does not diverge from training loss after convergence).

## Limitations

- Deep learning requires substantially more samples than metabolomics cohorts typically provide; 50 rounds with 10-fold CV may still overfit on small datasets (<200 samples).
- h2o integration is not explicitly documented in the README; users must have h2o package installed and Python path configured for some functions.
- Interpretability is reduced compared to traditional classifiers; no feature importance or coefficient estimates are provided for deep learning models, limiting biological insight.
- Cox-nnet prognosis module requires Python backend (reticulate) and may fail silently if Python paths are misconfigured.
- No hyperparameter tuning (e.g., layer depth, activation function, learning rate) is exposed in the Lilikoi API; only dlround and ensemble parameters are configurable.

## Evidence

- [other] classifier configuration and output format: "The Lilikoi v2.0 machine_learning module accepts an expression matrix and labels, supports multiple classifiers (Rpart, LDA, SVM, RF, GBM, PAM, LOG, and DL), and provides configurable parameters"
- [intro] deep learning integration in Lilikoi v2.0: "The new Lilikoi v2.0 R package has implemented a deep-learning method for classification, in addition to popular machine learning methods."
- [intro] prognosis module with Cox-nnet: "the most significant addition of prognosis prediction, implemented by Cox-PH model and the deep-learning based Cox-nnet model"
- [other] machine learning workflow steps: "Execute the deep learning classifier via h2o integration within Lilikoi v2.0 as an alternative classification approach. Aggregate trained classifier objects and extract performance metrics (accuracy,"
- [readme] example invocation syntax: "lilikoi.machine_learning(MLmatrix = Metadata, measurementLabels = Metadata$Label, significantPathways = 0, trainportion = 0.8, cvnum = 10, dlround=50, nrun=10, Rpart=TRUE, LDA=TRUE, SVM=TRUE,"
