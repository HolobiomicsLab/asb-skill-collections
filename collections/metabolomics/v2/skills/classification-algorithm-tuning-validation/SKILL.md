---
name: classification-algorithm-tuning-validation
description: Use when you have labeled training data (e.g., pqm_development with 500 peaks and 89 samples) and need to select which of multiple classification algorithms (e.g., AdaBoost, Random Forest, SVM) and their hyperparameters (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
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

# classification-algorithm-tuning-validation

## Summary

Systematically tune and validate machine learning classifiers using k-fold cross-validation with repeated runs to identify optimal hyperparameter configurations and select the best-performing algorithm for peak-quality classification in LC-MS metabolomics data. This skill ensures reproducible model selection by comparing multiple algorithms and evaluation metrics across held-out folds.

## When to use

You have labeled training data (e.g., pqm_development with 500 peaks and 89 samples) and need to select which of multiple classification algorithms (e.g., AdaBoost, Random Forest, SVM) and their hyperparameters (e.g., nIter, method, mtry) will generalize best to unseen LC-MS peak-quality classification tasks. Use this skill when you must justify model choice based on cross-validated performance metrics (M4, M7, M11) rather than single-fold or full-data performance.

## When NOT to use

- You have an already-trained, published model and only need to apply it to new data (use getPredictions instead).
- Your dataset is very small (< 50 samples) such that k=5 folds leave too few training examples per fold to tune hyperparameters reliably.
- Your goal is exploratory data visualization or quality assessment of peak metrics themselves, not algorithm selection.

## Inputs

- labeled peak-quality training dataset (e.g., pqm_development: data frame with 500 peaks, 89 samples, binary quality labels)
- list of candidate classification algorithms (e.g., 'AdaBoost', 'RandomForest', 'SVM')
- hyperparameter grid or default space for each algorithm
- metric set specification (e.g., c('M4','M7','M11') for evaluation measures)

## Outputs

- trained model object (e.g., models$AdaBoost_M11) containing cross-validation fold results
- prediction data frame per model with hyperparameter columns and fold assignments
- evaluation measures table (sensitivity, specificity, balanced accuracy, etc.) averaged across folds and repetitions
- visualization plots (bar plots or CD plots) ranking algorithms by metric
- selected optimal hyperparameters and best-performing algorithm name

## How to apply

Call runCrossValidation() with parameters k=5 (or higher), repNum=10 (number of repetitions), rand.seed=512 (for reproducibility), models='all' (or a subset of algorithms), and metricSet specifying which evaluation measures to compute (e.g., c('M4','M7','M11') for sensitivity, specificity, balanced accuracy). This wrapper function trains each selected algorithm on k-1 folds and evaluates on the held-out fold, repeating the process repNum times with different random partitions. Extract the prediction data frame from each model's results (e.g., models$AdaBoost_M11$pred) to identify hyperparameter combinations tested during tuning. Use getEvaluationMeasures() and getBarPlots() or getCDPlots() to compare aggregate performance across all models and runs. Select the algorithm and hyperparameters corresponding to the best mean performance on the primary metric. The rationale is that repeated k-fold cross-validation reduces variance from a single train-test split and reveals whether hyperparameter differences (e.g., nIter=100 vs. nIter=150) produce consistent improvements across multiple data partitions.

## Related tools

- **caret** (R package underlying cross-validation and algorithm training; implements the wrapper interface for multiple classification algorithms with hyperparameter tuning)
- **MetaClean** (R package providing runCrossValidation(), getEvaluationMeasures(), getBarPlots(), and getCDPlots() wrapper functions for k-fold cross-validation tuning and comparison of 8 classification algorithms) — https://github.com/KelseyChetnik/MetaClean
- **R** (Programming environment in which MetaClean and caret functions execute)

## Examples

```
models <- runCrossValidation(trainData = pqm_development, k = 5, repNum = 10, rand.seed = 512, models = 'all', metricSet = c('M4', 'M7', 'M11'))
```

## Evaluation signals

- The returned models list contains a prediction data frame (models$AlgorithmName$pred) with non-empty hyperparameter columns (nIter, method, mtry, etc.) and fold/repetition identifiers; presence confirms tuning was applied.
- Evaluation measures are computed for each fold and repetition (repNum=10 runs × k=5 folds = 50 evaluations per algorithm); verify output contains mean ± SD (or similar aggregation) per algorithm and metric, not single-point scores.
- Bar plots or CD plots show statistically comparable rankings across algorithms; verify that selected algorithm has the highest mean rank on the primary metric (e.g., M11) with no misleading single-fold cherry-picking.
- Optimal hyperparameters (e.g., nIter=150, method='Adaboost.M1') can be extracted from the pred data frame by filtering for rows with best cross-validated performance; verify these differ meaningfully from default or prior literature values, validating that tuning discovered non-trivial settings.
- Random seed (rand.seed=512) is set and reported; reproducibility check: re-running with same seed and data should yield identical folds, predictions, and selected hyperparameters.

## Limitations

- Hyperparameter tuning is limited to the grid or space specified by the user; if the optimal settings lie outside this space, they will not be discovered.
- Cross-validation estimates generalization error but cannot guarantee performance on external validation sets; selected hyperparameters may overfit to the development set distribution.
- Computational cost increases linearly with repNum and number of algorithms; very large grids or many repetitions may be slow on large datasets.
- The article does not report absolute runtime or scalability thresholds; practitioners must validate that k, repNum, and grid size are feasible for their hardware.
- No mechanism described for handling missing peak-quality metrics; if input data contain NAs, they must be imputed or removed before calling runCrossValidation().

## Evidence

- [methods] The runCrossValidation function is a wrapper function that uses cross-validation to train a user-selected subset of the 8 available algorithms.: "The runCrossValidation function is a wrapper function that uses cross-validation to train a user-selected subset of the 8 available algorithms."
- [other] Load the trained models list returned by runCrossValidation() with parameters k=5, repNum=10, rand.seed=512, models='all', metricSet=c('M4','M7','M11') on pqm_development (500 peaks, 89 samples). Access the prediction data frame from models$AdaBoost_M11$pred.: "Load the trained models list returned by runCrossValidation() with parameters k=5, repNum=10, rand.seed=512, models='all', metricSet=c('M4','M7','M11') on pqm_development (500 peaks, 89 samples)."
- [methods] We use the getEvaluationMeasures function to do this.: "We use the getEvaluationMeasures function to do this."
- [methods] MetaClean provides a simple wrapper function to easily generate bar plot visualizations of the evaluation measures for each model. This is getBarPlots.: "MetaClean provides a simple wrapper function to easily generate bar plot visualizations of the evaluation measures for each model. This is getBarPlots."
- [readme] MetaClean utilizes 12 peak-quality metrics and 9 diverse machine learning algorithms to build a classifier to detect and flag low-quality peaks in untargeted metabolomics data.: "MetaClean utilizes 12 peak-quality metrics and 9 diverse machine learning algorithms to build a classifier to detect and flag low-quality peaks in untargeted metabolomics data."
