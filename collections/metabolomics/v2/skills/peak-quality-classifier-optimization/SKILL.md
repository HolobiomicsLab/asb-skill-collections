---
name: peak-quality-classifier-optimization
description: Use when after calculating 12 peak-quality metrics on a development set of extracted ion chromatograms (EICs) and labeled peaks, when you need to select both the classification algorithm and its optimal hyperparameters before training a final model on held-out test data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
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
---

# Peak-Quality Classifier Optimization

## Summary

Optimize machine learning classifier hyperparameters for detecting low-quality chromatographic peaks in LC-MS metabolomics data using k-fold cross-validation and comparative evaluation metrics. This skill identifies the best-performing algorithm configuration (e.g., AdaBoost with nIter=150, method='Adaboost.M1') by training multiple classifiers on development data and ranking them by performance across diverse quality metrics.

## When to use

After calculating 12 peak-quality metrics on a development set of extracted ion chromatograms (EICs) and labeled peaks, when you need to select both the best classification algorithm and its optimal hyperparameters before training a final model on held-out test data. Typical trigger: you have a candidate set of 8+ machine learning algorithms and want data-driven evidence to choose one algorithm and its parameter configuration rather than relying on defaults.

## When NOT to use

- Input is a pre-trained, published classifier model with fixed hyperparameters — skip optimization and go directly to getPredictions() on test data.
- Development set is <100 peaks or heavily imbalanced (>>90% one class) — cross-validation results will be unreliable; collect more balanced labeled data first.
- You only have a test set with no held-out development set — hyperparameter tuning on test data causes overfitting; partition labeled data into development and test before applying this skill.

## Inputs

- Peak-quality metrics matrix (pqm_development): 500+ peaks × 89 samples with 12 calculated quality metrics (RSD, signal-to-noise, shape symmetry, etc.)
- Binary labels or quality annotations for development peaks
- List of candidate classification algorithms (subset or all 8 available in caret)

## Outputs

- Cross-validation results object (models$<algorithm>$pred) containing predictions and hyperparameter combinations for each fold/repetition
- Evaluation measures data frame (M4, M7, M11, etc.) for each model–hyperparameter pair
- Optimized hyperparameter values and algorithm name (e.g., AdaBoost with nIter=150, method='Adaboost.M1')
- Visualization plots (bar plots, CD plots) comparing classifier performance

## How to apply

Call runCrossValidation() with k=5 folds, repNum=10 repetitions, rand.seed=512, and a subset of models (e.g., models='all' to try AdaBoost, Random Forest, SVM, etc.) on the development peak-quality matrix (pqm_development). Extract the pred data frame from each trained model to access hyperparameter combinations and their cross-validation performance. Calculate evaluation measures (e.g., M4, M7, M11 representing sensitivity, specificity, and F-score) using getEvaluationMeasures() for each model–hyperparameter pair. Visualize comparative rankings with getBarPlots() or getCDPlots() to identify the algorithm and hyperparameters yielding the highest performance across your chosen metric set. Record the optimized configuration (e.g., nIter and method for AdaBoost) and validate it corresponds to the best-performing classifier before invoking trainClassifier() with those fixed hyperparameters on the full development set.

## Related tools

- **MetaClean** (R package hosting the runCrossValidation(), getEvaluationMeasures(), getBarPlots(), getCDPlots(), and trainClassifier() functions for classifier optimization and evaluation) — https://github.com/KelseyChetnik/MetaClean
- **caret** (Underlying R package providing the 8 classification algorithms (including AdaBoost, Random Forest, SVM, etc.) and cross-validation framework used by MetaClean)
- **R** (Programming environment for executing MetaClean functions and manipulating cross-validation results)

## Examples

```
models <- runCrossValidation(trainData = pqm_development, k = 5, repNum = 10, rand.seed = 512, models = 'all', metricSet = c('M4','M7','M11')); eval_measures <- getEvaluationMeasures(models); getBarPlots(eval_measures); optimized_model <- trainClassifier(trainData = pqm_development, model = 'AdaBoost', metricSet = 'M11', hyperparameters = list(nIter = 150, method = 'Adaboost.M1'))
```

## Evaluation signals

- Cross-validation repetitions (repNum=10) converge on the same or highly similar best hyperparameters; high variance across repetitions suggests unstable optimization.
- Evaluation measures (sensitivity M4, specificity M7, F-score M11) for the selected algorithm exceed baseline or threshold values (e.g., F-score > 0.80); compare against published benchmarks if available.
- Optimized hyperparameters differ meaningfully from algorithm defaults; if optimized nIter, method, or other tuned parameters match library defaults, re-check cross-validation configuration (seed, folds, metric set).
- Performance on held-out test set (obtained via getPredictions() with optimized hyperparameters) remains within ±5–10% of cross-validation performance; larger gaps indicate overfitting or distribution shift.
- Bar plots / CD plots show the selected algorithm as statistically distinct (non-overlapping confidence intervals) from runner-up classifiers across the metric set.

## Limitations

- Cross-validation results depend critically on the composition and balance of the development set; sparse or skewed class distributions can produce unreliable rankings.
- Optimization uses only the 12 pre-defined peak-quality metrics (RSD, S/N, shape symmetry, etc.); novel or domain-specific metrics not in the MetaClean metric set are not considered.
- The skill assumes independence between peak samples; if peaks within the same sample or batch are highly correlated, cross-validation folds may leak information between training and validation sets.
- Hyperparameter space explored is limited to algorithm-specific tuning grids in caret; custom or application-specific hyperparameter ranges beyond caret defaults cannot be searched with runCrossValidation().

## Evidence

- [methods] Cross-validation setup and hyperparameter extraction: "Load the trained models list returned by runCrossValidation() with parameters k=5, repNum=10, rand.seed=512, models='all', metricSet=c('M4','M7','M11') on pqm_development (500 peaks, 89 samples). 2."
- [methods] Evaluation measures computation: "The runCrossValidation function is a wrapper function that uses cross-validation to train a user-selected subset of the 8 available algorithms."
- [methods] Comparative visualization: "MetaClean provides a simple wrapper function to easily generate bar plot visualizations of the evaluation measures for each model. This is getBarPlots"
- [methods] Classifier training with optimized hyperparameters: "metaclean_model <- trainClassifier(trainData = pqm_development, model = "AdaBoost", metricSet = "M11", hyperparameters = hyperparameters)"
- [readme] Algorithm diversity and metric foundation: "MetaClean utilizes 12 peak-quality metrics and 9 diverse machine learning algorithms to build a classifier to detect and flag low-quality peaks in untargeted metabolomics data."
