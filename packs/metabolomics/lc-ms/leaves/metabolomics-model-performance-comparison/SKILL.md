---
name: metabolomics-model-performance-comparison
description: Use when you have trained multiple machine learning classifiers (e.g.,
  AdaBoost, SVM, Random Forest) on the same metabolomics peak-quality training set
  using k-fold cross-validation with repeated runs (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0091
  tools:
  - MetaClean
  - R
  - caret
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1007/s11306-020-01738-3
  title: MetaClean
- doi: 10.1186/1471-2105-15-s11-s5
  title: ''
evidence_spans:
- MetaClean is a package for building classifiers to identify low quality integrations
  in untargeted metabolomics data.
- '`MetaClean` provides 8 classification algorithms (implemented with the R package
  `caret`) for building a predictive model.'
- getEvalObj is called to extract the relevant data from the three objects provided
  by ther user and store them in an object of class evalObj
- It is an R package and can be easily incorporated
- MetaClean provides 8 classification algorithms (implemented with the R package caret)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaclean_cq
    doi: 10.1007/s11306-020-01738-3
    title: MetaClean
  dedup_kept_from: coll_metaclean_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1007/s11306-020-01738-3
  all_source_dois:
  - 10.1007/s11306-020-01738-3
  - 10.1186/1471-2105-15-s11-s5
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomics-model-performance-comparison

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Compare machine learning classifier performance across multiple algorithms and metric sets to identify the best-performing model for detecting low-quality peaks in untargeted LC-MS metabolomics data. This skill synthesizes evaluation measures (e.g., sensitivity, specificity, accuracy, balanced accuracy) computed via k-fold cross-validation to guide model selection before final training.

## When to use

You have trained multiple machine learning classifiers (e.g., AdaBoost, SVM, Random Forest) on the same metabolomics peak-quality training set using k-fold cross-validation with repeated runs (e.g., k=5, repNum=10), and you need to objectively rank them by performance to select which single model to train and deploy on held-out test data. Typical trigger: you have access to a list of trained models returned by runCrossValidation() with evaluation measures already computed, and you must decide which algorithm and metric set (M4, M7, M11) combination yields the best generalization.

## When NOT to use

- You have not yet trained multiple models or only a single algorithm candidate exists — use this skill only when comparing ≥2 distinct algorithms or metric sets.
- Cross-validation has not been completed; evaluation measures are not yet computed — defer this skill until runCrossValidation() and getEvaluationMeasures() outputs are available.
- Your goal is to tune hyperparameters within a single algorithm rather than select between algorithms — use grid search or Bayesian optimization (e.g., caret's tuneGrid parameter) before invoking this comparison skill.

## Inputs

- models list object returned by runCrossValidation() with k≥5, repNum≥10, and models='all' or subset thereof
- cross-validation prediction data frames (models$AlgorithmName$pred) containing fold-level performance
- development set (e.g., pqm_development: 500 peaks, 89 samples)
- peak-quality metric set options (M4, M7, M11 as computed by getPeakQualityMetrics())

## Outputs

- comparative performance ranking table (algorithm × metric set → mean/SD of sensitivity, specificity, accuracy, balanced accuracy, AUC)
- bar plots and critical-difference plots showing classifier rankings across evaluation measures
- selected best-performing model identifier (algorithm name + metric set + hyperparameters)
- decision rationale document (chosen model name, ranking position, performance scores, tie-breaker justification)

## How to apply

Extract the evaluation measures (sensitivity, specificity, accuracy, balanced accuracy, AUC) for each trained model from the cross-validation output using getEvaluationMeasures(). Visualize comparative performance across all models using getBarPlots() and getCDPlots() wrapper functions to identify patterns and statistical differences. Compute summary statistics (mean, SD, ranking) for each evaluation metric across the k×repNum folds. Select the model with the highest mean balanced accuracy or AUC (depending on class imbalance in your development set); if multiple models are competitive, apply a tiebreaker such as lowest variance across folds or preference for interpretability. Document the chosen model's algorithm name, metric set, and hyperparameters (e.g., nIter, method for AdaBoost), then proceed to trainClassifier() with those exact parameters on the full development set.

## Related tools

- **caret** (R package implementing 8 classification algorithms and providing cross-validation training wrapper (runCrossValidation) and evaluation measure computation (getEvaluationMeasures))
- **MetaClean** (R package providing getEvaluationMeasures(), getBarPlots(), getCDPlots(), and trainClassifier() functions to compute, visualize, and operationalize comparative model performance) — https://github.com/KelseyChetnik/MetaClean
- **R** (Runtime environment for executing cross-validation workflows and comparative analysis)

## Examples

```
models <- runCrossValidation(trainData=pqm_development, k=5, repNum=10, rand.seed=512, models='all', metricSet=c('M4','M7','M11')); eval_measures <- getEvaluationMeasures(models); getBarPlots(eval_measures); getBarPlots(eval_measures, plotType='CD'); best_model_idx <- which.max(eval_measures$balanced_accuracy_mean); selected <- names(models)[best_model_idx]; hyperparameters <- models[[selected]]$pred[1, c('nIter', 'method')]; final_model <- trainClassifier(trainData=pqm_development, model=sub('_.*', '', selected), metricSet=sub('.*_', '', selected), hyperparameters=hyperparameters)
```

## Evaluation signals

- Evaluation measures output from getEvaluationMeasures() contains non-null, numeric sensitivity, specificity, accuracy, balanced accuracy, and AUC values for each algorithm and fold combination.
- Bar plots and CD plots render without errors, showing all trained algorithms ranked by at least one evaluation metric; visual inspection confirms no algorithm is dominated (worse) across all metrics.
- Selected model's mean balanced accuracy or AUC ranks in top 1–3 among all candidates; SD across folds is ≤0.10 (indicating stable cross-validation performance).
- Hyperparameters documented for the selected model match a row in the cross-validation prediction data frame (e.g., nIter=150 and method='Adaboost.M1' for AdaBoost_M11).
- Downstream trainClassifier() call using the selected model and hyperparameters succeeds without error, and the final model achieves comparable or better performance on the held-out test set (getPredicitons output) relative to cross-validation estimates.

## Limitations

- Comparison quality depends on cross-validation fold count (k) and repetitions (repNum); small k or repNum may yield unstable performance estimates with high variance, weakening discriminability between models.
- Evaluation metric choice (accuracy vs. balanced accuracy vs. AUC) affects ranking, especially when class imbalance exists in the development set; no single metric is universally optimal; practitioners should select metric(s) aligned with their application (e.g., AUC preferred for imbalanced data).
- The 9 algorithms implemented in MetaClean may not include specialized metabolomics models or domain-specific adaptations; comparison is limited to algorithms available in caret.
- Hyperparameter tuning is not explicitly included in this skill's scope; the workflow assumes cross-validation was already run with fixed or default hyperparameters; grid search must precede this comparison if hyperparameter sensitivity is suspected.
- No changelog or versioning found in the repository, so reproducibility across MetaClean versions or R package updates is not guaranteed.

## Evidence

- [intro] MetaClean utilizes 12 peak-quality metrics and 9 diverse machine learning algorithms to build a classifier to detect and flag low-quality peaks in untargeted metabolomics data: "MetaClean utilizes 12 peak-quality metrics and 9 diverse machine learning algorithms to build a classifier to detect and flag low-quality peaks in untargeted metabolomics data"
- [methods] The runCrossValidation function is a wrapper function that uses cross-validation to train a user-selected subset of the 8 available algorithms.: "The runCrossValidation function is a wrapper function that uses cross-validation to train a user-selected subset of the 8 available algorithms."
- [methods] We use the getEvaluationMeasures function to do this.: "We use the getEvaluationMeasures function to compute evaluation measures for each model."
- [methods] MetaClean provides a simple wrapper function to easily generate bar plot visualizations of the evaluation measures for each model. This is getBarPlots: "MetaClean provides a simple wrapper function to easily generate bar plot visualizations of the evaluation measures for each model. This is getBarPlots"
- [methods] MetaClean also provides a wrapper function to easily generate CD plots of the evaluation measures for each model. This is getCDPlots: "MetaClean also provides a wrapper function to easily generate CD plots of the evaluation measures for each model. This is getCDPlots"
- [methods] Compare Classifiers and Select Best Performing: "Compare Classifiers and Select Best Performing"
- [methods] metaclean_model <- trainClassifier(trainData = pqm_development, model = "AdaBoost", metricSet = "M11", hyperparameters = hyperparameters): "metaclean_model <- trainClassifier(trainData = pqm_development, model = "AdaBoost", metricSet = "M11", hyperparameters = hyperparameters)"
- [readme] It is an R package and can be easily incorporated into existing untargeted LC-MS metabolomics pipelines that utilize the pre-processing software XCMS.: "It is an R package and can be easily incorporated into existing untargeted LC-MS metabolomics pipelines that utilize the pre-processing software XCMS."
