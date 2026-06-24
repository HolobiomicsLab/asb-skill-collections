---
name: statistical-model-ranking-and-selection
description: Use when you have trained multiple machine learning algorithms (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3306
  tools:
  - MetaClean
  - R
  - caret
  - devtools
  license_tier: restricted
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
- devtools::install_github("KelseyChetnik/MetaCleanData")
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

# statistical-model-ranking-and-selection

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Rank and select the best-performing machine learning classifier from a candidate set using cross-validation, evaluation metrics (F-score, precision, recall, accuracy), and statistical comparison plots (Friedman-Demšar CD plots). This skill identifies the optimal algorithm for a specific downstream task (e.g., peak quality classification) by comparing mean performance scores and statistical significance across all folds and repetitions.

## When to use

You have trained multiple machine learning algorithms (e.g., DecisionTree, LogisticRegression, NaiveBayes, RandomForest, SVM, AdaBoost, NeuralNetwork) on the same labeled dataset using k-fold cross-validation with multiple repetitions, and you need to select a single best model for deployment or further tuning. Typical trigger: you have cross-validation results for ≥3 algorithms and need to decide which to train as the final classifier.

## When NOT to use

- Only one algorithm has been trained; statistical ranking requires ≥2 candidate models.
- Cross-validation has not been completed; this skill operates on already-trained CV results, not raw data.
- You have only a single train-test split (not repeated cross-validation); statistical comparison via CD plots requires variance estimates across multiple folds.

## Inputs

- cross-validation results: list of trained models, hyperparameters, and predictions from runCrossValidation()
- peak quality metrics matrix (pqm_development) with k=5 folds and repNum=10 repetitions
- metric set specification (e.g., 'M11')
- algorithm specification (list of ≥2 candidate algorithms)

## Outputs

- evaluation measures data frame: Pass_FScore, Fail_FScore, Accuracy, Pass_Precision, Pass_Recall, Fail_Precision, Fail_Recall per algorithm and fold
- bar plots visualizing mean evaluation measures (Pass_FScore, Fail_FScore, Accuracy) by algorithm
- Friedman-Demšar CD plots showing statistical rankings and significance groups
- rank matrix identifying best-performing algorithm and confidence in selection
- selected algorithm name (e.g., 'AdaBoost') to pass to trainClassifier() for final model training

## How to apply

After running cross-validation across all candidate algorithms, calculate evaluation measures (Pass_FScore, Fail_FScore, Accuracy, precision, recall) for each model across all folds and repetitions using getEvaluationMeasures(). Visualize performance using getBarPlots() to identify candidate leaders. Then generate statistical ranking plots using getCDPlots() with the Friedman-Demšar test (with compareBest=FALSE) to rank models within the metric set and assess whether performance differences are statistically significant. Compare mean evaluation scores and statistical rankings to identify the best-performing algorithm, which becomes the basis for training the final classifier. This approach accounts for variance across cross-validation rounds rather than relying on a single train-test split.

## Related tools

- **MetaClean** (Provides runCrossValidation(), getEvaluationMeasures(), getBarPlots(), getCDPlots() wrapper functions to execute cross-validation, compute evaluation metrics, and generate statistical ranking visualizations.) — https://github.com/KelseyChetnik/MetaClean
- **caret** (Underlying R package implementing the 8 machine learning algorithms (DecisionTree, LogisticRegression, NaiveBayes, RandomForest, SVM_Linear, AdaBoost, NeuralNetwork, ModelAveragedNeuralNetwork) trained and compared within MetaClean's cross-validation framework.)
- **R** (Statistical computing environment in which MetaClean, caret, and CD plot generation (Friedman-Demšar test) are executed.)

## Examples

```
# Compute evaluation measures for all cross-validated models
eval_measures <- getEvaluationMeasures(cv_results)

# Visualize Pass_FScore, Fail_FScore, Accuracy by algorithm
getBarPlots(eval_measures, measures = c('Pass_FScore', 'Fail_FScore', 'Accuracy'))

# Generate Friedman-Demšar CD plots and rank models
getCDPlots(eval_measures, compareBest = FALSE)

# Extract best algorithm from rank matrix
best_algo <- names(which.min(colMeans(rank_matrix)))
```

## Evaluation signals

- Evaluation measures (Pass_FScore, Fail_FScore, Accuracy) are computed for every model across all k folds and all repetitions; no fold or algorithm is missing.
- Bar plots show non-zero, bounded values (F-scores and accuracy in [0,1]); extreme or NaN values indicate failed cross-validation.
- CD plots render statistical groupings (critical difference intervals) such that algorithms within the same group are not significantly different (α=0.05 typically); algorithms outside are ranked as significantly better or worse.
- Rank matrix displays all algorithms with average rank scores; best algorithm has the lowest mean rank and is positioned at the left edge of the CD plot.
- Selected algorithm name matches one of the candidate algorithms passed to runCrossValidation(); verify the selection is consistent with both bar plot and CD plot rankings.

## Limitations

- Statistical power depends on the number of folds and repetitions; 5 folds with 10 repetitions (50 total evaluations per algorithm) provides moderate power but may miss subtle differences in small datasets.
- CD plots assume exchangeable cross-validation rounds and do not account for temporal or data dependency structure; if folds are not independent, ranking may be biased.
- Metric set selection ('M11', etc.) is fixed before cross-validation; comparison is valid only within one metric set, not across different feature sets.
- Final model selection based on training-set cross-validation performance may not generalize to an independent test set; post-selection validation on a held-out test set is recommended but not included in this skill.

## Evidence

- [methods] Apply getEvaluationMeasures to calculate Pass_FScore, Pass_Precision, Pass_Recall, Fail_FScore, Fail_Precision, Fail_Recall, and Accuracy across all cross-validation rounds and models.: "Apply getEvaluationMeasures to calculate Pass_FScore, Pass_Precision, Pass_Recall, Fail_FScore, Fail_Precision, Fail_Recall, and Accuracy across all cross-validation rounds and models."
- [methods] Visualize evaluation measures using getBarPlots (Pass_FScore, Fail_FScore, Accuracy) to assess model performance.: "Visualize evaluation measures using getBarPlots (Pass_FScore, Fail_FScore, Accuracy) to assess model performance."
- [methods] Generate CD (Friedman-Demšar) plots and rank matrices using getCDPlots with compareBest=FALSE to statistically rank models within the M11 metric set.: "Generate CD (Friedman-Demšar) plots and rank matrices using getCDPlots with compareBest=FALSE to statistically rank models within the M11 metric set."
- [methods] Identify AdaBoost as the best-performing algorithm by comparing mean evaluation scores and statistical rankings across all models.: "Identify AdaBoost as the best-performing algorithm by comparing mean evaluation scores and statistical rankings across all models."
- [readme] MetaClean utilizes 12 peak-quality metrics and 9 diverse machine learning algorithms to build a classifier to detect and flag low-quality peaks in untargeted metabolomics data: "MetaClean utilizes 12 peak-quality metrics and 9 diverse machine learning algorithms to build a classifier to detect and flag low-quality peaks in untargeted metabolomics data"
