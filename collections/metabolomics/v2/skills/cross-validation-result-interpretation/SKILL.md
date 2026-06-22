---
name: cross-validation-result-interpretation
description: Use when after running k-fold repeated cross-validation on a development set (via runCrossValidation with parameters k, repNum, and a subset of algorithms) and you need to select which trained classifier and hyperparameter combination to deploy.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3674
  tools:
  - MetaClean
  - R
  - caret
derived_from:
- doi: 10.1007/s11306-020-01738-3
  title: MetaClean
- doi: 10.1186/1471-2105-15-s11-s5
  title: ''
evidence_spans:
- MetaClean is a package for building classifiers to identify low quality integrations in untargeted metabolomics data.
- '`MetaClean` provides 8 classification algorithms (implemented with the R package `caret`) for building a predictive model.'
- getEvalObj is called to extract the relevant data from the three objects provided by ther user and store them in an object of class evalObj
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

# cross-validation-result-interpretation

## Summary

Extract optimized hyperparameter values and evaluation metrics from cross-validation output to identify and validate the best-performing machine learning classifier configuration. This skill bridges model training and final classifier deployment by systematically comparing held-out predictions and performance measures across folds and repetitions.

## When to use

After running k-fold repeated cross-validation on a development set (via runCrossValidation with parameters k, repNum, and a subset of algorithms) and you need to select which trained classifier and hyperparameter combination to deploy. Specifically, when you have prediction data frames and evaluation measures from multiple candidate models and must identify which one achieves the best trade-off on your chosen metric(s) before training the final classifier.

## When NOT to use

- You have not yet run cross-validation — use runCrossValidation() first to generate models and predictions.
- Your development set is too small or imbalanced to yield stable cross-validation results — consider data augmentation or stratified sampling before interpretation.
- You are interpreting results from a single train/test split rather than k-fold repeated cross-validation — this skill requires multiple folds and repetitions to validate hyperparameter stability.

## Inputs

- Cross-validation model list (output of runCrossValidation with models='all')
- Prediction data frame from models$[AlgorithmName]$pred (with hyperparameter and held-out prediction columns)
- Evaluation measures object (output of getEvaluationMeasures)
- Development set (500 peaks, 89 samples in example)

## Outputs

- Selected hyperparameter values (e.g., nIter, method) for best-performing configuration
- Ranked list of models by evaluation metric (sensitivity, specificity, accuracy, etc.)
- Visualization of evaluation measures (bar plots or CD plots)
- Best-performing algorithm name and configuration specification for final classifier training

## How to apply

Load the cross-validation results returned by runCrossValidation(k=5, repNum=10, rand.seed=512, models='all', metricSet=c('M4','M7','M11')) on the development set. For each candidate algorithm (e.g., AdaBoost_M11), access the prediction data frame via models$[AlgorithmName]$pred and extract the hyperparameter columns (nIter, method, etc.) to identify all unique combinations tested. Generate evaluation measures using getEvaluationMeasures() to obtain performance statistics (e.g., sensitivity, specificity, accuracy) for each configuration. Visualize or rank the results by your primary metric using getBarPlots() or getCDPlots() to identify the configuration with optimal performance. Cross-reference the hyperparameters of the top-ranked configuration with the prediction accuracy on held-out folds to confirm consistency. Document the selected hyperparameter set (e.g., nIter=150, method='Adaboost.M1') for use in the final classifier training step.

## Related tools

- **caret** (R package used internally by runCrossValidation and trainClassifier for model training and cross-validation orchestration)
- **MetaClean** (Parent package providing runCrossValidation, getEvaluationMeasures, getBarPlots, getCDPlots functions for cross-validation workflow) — https://github.com/KelseyChetnik/MetaClean
- **R** (Environment for executing cross-validation result extraction and interpretation functions)

## Examples

```
models <- runCrossValidation(trainData = pqm_development, k = 5, repNum = 10, rand.seed = 512, models = 'all', metricSet = c('M4', 'M7', 'M11')); eval_measures <- getEvaluationMeasures(models); getBarPlots(eval_measures)
```

## Evaluation signals

- Extracted hyperparameter combinations are non-empty and match the cardinality of the parameter grid specified in runCrossValidation (e.g., if testing 2 nIter values × 3 methods, expect 6 unique rows per algorithm).
- Evaluation measures computed via getEvaluationMeasures have non-null values for all selected metrics (M4, M7, M11) across all model configurations.
- The selected best-performing hyperparameter configuration shows consistent rank (same or top 2) across at least 80% of the 10 repetitions, indicating stable cross-validation performance.
- Comparison of best model's held-out prediction accuracy on the development set matches the reported evaluation metric values within a small tolerance (e.g., ±0.02), confirming internal consistency.
- Bar plots or CD plots generated by getBarPlots/getCDPlots visually confirm that the selected configuration is the top-ranked model on the primary evaluation metric.

## Limitations

- The task card notes that 'Unable to provide - the provided section text does not contain reported hyperparameter values or cross-validation results for AdaBoost model tuning,' suggesting the original article may not fully document hyperparameter ranges or final values; practitioners must consult the MetaClean package vignette or source code to infer default or tested ranges.
- Cross-validation results are sensitive to random seed and fold structure; identical hyperparameter selections across different seeds or fold strategies are not guaranteed, so results should be validated on held-out test sets before deployment.
- Evaluation measure interpretation depends on dataset-specific class balance and metric choice (e.g., accuracy may mislead on imbalanced data); practitioners should align metric selection with their quality-control goals (sensitivity vs. specificity trade-off for peak filtering).

## Evidence

- [other] Load the trained models list returned by runCrossValidation() with parameters k=5, repNum=10, rand.seed=512, models='all', metricSet=c('M4','M7','M11'): "Load the trained models list returned by runCrossValidation() with parameters k=5, repNum=10, rand.seed=512, models='all', metricSet=c('M4','M7','M11') on pqm_development (500 peaks, 89 samples)."
- [other] Access the prediction data frame and extract hyperparameters from models$AdaBoost_M11$pred: "Access the prediction data frame from models$AdaBoost_M11$pred. 3. Extract the unique hyperparameter combinations (nIter and method columns) from the pred data frame."
- [other] Identify optimized hyperparameters and validate against evaluation measures: "Identify and record the optimized hyperparameters determined during cross-validation (nIter=150, method='Adaboost.M1' per the example). 5. Validate that these hyperparameters correspond to the"
- [methods] MetaClean provides wrapper functions for generating comparative visualizations: "MetaClean provides a simple wrapper function to easily generate bar plot visualizations of the evaluation measures for each model. This is getBarPlots"
- [methods] Use getEvaluationMeasures to compare classifiers and select best performing: "We use the getEvaluationMeasures function to do this. … Compare Classifiers and Select Best Performing"
