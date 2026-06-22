---
name: comparative-classifier-performance-assessment
description: Use when you have a labeled peak quality dataset (development set with ground-truth pass/fail labels), a defined set of peak-quality metrics (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3502
  edam_topics:
  - http://edamontology.org/topic_3394
  - http://edamontology.org/topic_0091
  tools:
  - MetaClean
  - R
  - caret
  - devtools
  - MetaCleanData
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
---

# Comparative Classifier Performance Assessment

## Summary

Systematically train and rank multiple machine learning algorithms on the same peak-quality assessment task using k-fold cross-validation with statistical ranking plots to identify the best-performing classifier. This skill applies when selecting among competing algorithms for peak quality classification in LC-MS metabolomics data.

## When to use

You have a labeled peak quality dataset (development set with ground-truth pass/fail labels), a defined set of peak-quality metrics (e.g., M11 metric set), and need to determine which of the 8–9 available machine learning algorithms (DecisionTree, LogisticRegression, NaiveBayes, RandomForest, SVM_Linear, AdaBoost, NeuralNetwork, ModelAveragedNeuralNetwork) will perform best before deploying a final classifier on test data. Use this skill when model selection must be reproducible across multiple repetitions (e.g., 10 repetitions × 5 folds) and when statistical ranking rather than a single run is required.

## When NOT to use

- Input data lacks ground-truth labels — runCrossValidation requires labeled training data, not unlabeled peak sets.
- You already have a pre-trained classifier validated on independent test data — do not re-rank algorithms; proceed to final model training instead.
- Sample size is very small (e.g., <50 labeled peaks total) — cross-validation with k=5 and repNum=10 may yield unreliable rankings due to high variance.

## Inputs

- pqm_development: labeled peak quality metrics matrix with ground-truth pass/fail labels
- metric set specification (e.g., 'M11')
- random seed (integer, for reproducibility)
- cross-validation parameters (k, repNum)

## Outputs

- cross-validation fold results: trained models and hyperparameters for each algorithm and fold
- evaluation measures table: Pass_FScore, Fail_FScore, Accuracy, Pass_Precision, Pass_Recall, Fail_Precision, Fail_Recall per model and round
- bar plots: visual comparison of mean scores across algorithms
- CD (Friedman-Demšar) plots and rank matrices: statistical ranking of algorithms
- best-performing algorithm identifier with mean scores

## How to apply

Execute runCrossValidation on the labeled peak quality metrics matrix (pqm_development) with specified parameters: k=5 folds, repNum=10 repetitions, a fixed random seed (e.g., 453), your chosen metric set (e.g., 'M11'), and the full subset of algorithms to compare. Apply getEvaluationMeasures to extract Pass_FScore, Fail_FScore, Accuracy, and other measures across all cross-validation rounds. Visualize results using getBarPlots to compare mean performance scores across models, then generate CD (Friedman-Demšar) plots with getCDPlots (compareBest=FALSE) to obtain statistical rankings that account for multiple comparisons. Rank models by mean evaluation scores and statistical significance; the algorithm with the highest mean score and lowest critical distance is the best performer for your metric set.

## Related tools

- **MetaClean** (R package providing runCrossValidation, getEvaluationMeasures, getBarPlots, and getCDPlots functions for multi-algorithm comparison and statistical ranking) — https://github.com/KelseyChetnik/MetaClean
- **caret** (underlying machine learning framework in R used by MetaClean to implement all 8 classification algorithms)
- **MetaCleanData** (R package providing example development and test peak-quality metrics matrices for reproducible cross-validation studies) — https://github.com/KelseyChetnik/MetaCleanData
- **R** (runtime environment and language for executing MetaClean functions)

## Examples

```
runCrossValidation(pqm_development, k=5, repNum=10, rand.seed=453, algorithms=c('DecisionTree','LogisticRegression','NaiveBayes','RandomForest','SVM_Linear','AdaBoost','NeuralNetwork','ModelAveragedNeuralNetwork'), metricSet='M11')
```

## Evaluation signals

- Cross-validation completes without errors for all k·repNum fold splits and all requested algorithms; no missing hyperparameter sets returned.
- Evaluation measures are computed for all folds and all algorithms; no NaN or infinite values in Pass_FScore, Fail_FScore, or Accuracy columns.
- Bar plots show non-overlapping or clearly distinct mean scores across at least 2–3 top-ranked algorithms, indicating discriminative ranking.
- CD plot rankings are consistent with mean scores: algorithm with highest mean Pass_FScore appears at lowest critical distance rank.
- Friedman statistical test p-value (if reported) is <0.05, indicating significant differences among algorithms; if p≥0.05, no algorithm is truly superior within the metric set.

## Limitations

- Results are specific to the chosen metric set (e.g., M11); algorithm rankings may differ for other metric sets (e.g., M1–M8 or custom subsets).
- Cross-validation performance does not guarantee generalization to truly independent test data; final validation on held-out pqm_test is required before deployment.
- MetaClean uses only 8 fixed algorithms (DecisionTree, LogisticRegression, NaiveBayes, RandomForest, SVM_Linear, AdaBoost, NeuralNetwork, ModelAveragedNeuralNetwork); custom or ensemble algorithms not in this set cannot be ranked using runCrossValidation.
- Hyperparameter tuning is performed by caret's internal defaults; systematic hyperparameter optimization is not described in the workflow and may affect algorithm rankings if different hyperparameters are chosen.

## Evidence

- [other] 5-fold cross-validation with 10 repetitions on M11 metric set using random seed 453: "running 5-fold cross-validation with 10 repetitions on the M11 metric set using MetaCleanData with random seed 453"
- [methods] runCrossValidation function wraps cross-validation training of user-selected algorithm subset: "The runCrossValidation function is a wrapper function that uses cross-validation to train a user-selected subset of the 8 available algorithms."
- [methods] getEvaluationMeasures extracts performance metrics per model across CV rounds: "We use the getEvaluationMeasures function to do this."
- [methods] getCDPlots generates statistical CD plots and rank matrices for algorithm comparison: "MetaClean also provides a wrapper function to easily generate CD plots of the evaluation measures for each model. This is getCDPlots"
- [other] AdaBoost identified as best algorithm by comparing mean scores and statistical rankings: "Identify AdaBoost as the best-performing algorithm by comparing mean evaluation scores and statistical rankings across all models."
- [readme] 9 diverse machine learning algorithms available for training and comparison: "MetaClean utilizes 12 peak-quality metrics and 9 diverse machine learning algorithms to build a classifier to detect and flag low-quality peaks in untargeted metabolomics data."
