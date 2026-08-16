---
name: machine-learning-model-training-with-cross-validation
description: Use when when you have a labeled peak quality matrix (with known pass/fail labels), need to objectively compare performance across multiple classification algorithms (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - MetaClean
  - R
  - caret
  - devtools
  - MetaCleanData
  techniques:
  - LC-MS
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

# machine-learning-model-training-with-cross-validation

## Summary

Train and compare multiple machine learning classifiers using k-fold cross-validation with repetitions to identify the best-performing algorithm for peak quality assessment in LC-MS metabolomics data. This skill applies statistical ranking and evaluation metrics to select a robust classifier from a candidate algorithm pool.

## When to use

When you have a labeled peak quality matrix (with known pass/fail labels), need to objectively compare performance across multiple classification algorithms (e.g., AdaBoost, Random Forest, SVM, Neural Networks), and want to avoid overfitting by using repeated k-fold cross-validation with a fixed random seed for reproducibility. Typical trigger: preparing to train a final single-model classifier for deployment on held-out test data.

## When NOT to use

- Input is a single small dataset without meaningful fold structure (e.g., <50 labeled examples) — cross-validation becomes unstable and statistical ranking loses power.
- The peak quality labels are highly imbalanced (e.g., >95% pass, <5% fail) without stratified sampling — fold-wise class distribution may vary too much, inflating variance in estimates.
- You have already trained and selected a single best model and are now applying it to test data — this skill is for model selection, not deployment or prediction.

## Inputs

- peak quality metrics matrix (pqm_development)
- metadata (sample annotations, EIC/peak associations)
- list of candidate machine learning algorithms
- metric set name (e.g., 'M11')
- cross-validation hyperparameters (k folds, repetitions, random seed)

## Outputs

- trained model objects for each algorithm and fold
- hyperparameter sets per model
- evaluation measure matrix (Pass_FScore, Fail_FScore, Accuracy, Precision, Recall per fold and algorithm)
- bar plot visualizations of mean evaluation scores
- Friedman-Demšar CD plot with algorithm rankings
- ranked comparison matrix (mean scores and statistical groups)

## How to apply

Load the peak quality metrics matrix (pqm_development) with labeled examples and call runCrossValidation with specified parameters: k folds (typically 5), repetition count (e.g., 10), a fixed random seed (e.g., 453), the metric set (e.g., 'M11'), and a list of candidate algorithms. Extract trained models and hyperparameters from the returned list structure. Apply getEvaluationMeasures to compute Pass_FScore, Fail_FScore, Accuracy, Precision, and Recall across all cross-validation rounds. Visualize mean scores using getBarPlots, then generate Friedman-Demšar CD plots via getCDPlots (with compareBest=FALSE) to statistically rank algorithms. Select the algorithm with the highest mean evaluation score and favorable statistical ranking. The rationale is that repeated cross-validation with statistical testing reduces variance in performance estimates and guards against selection bias caused by a single random train-test split.

## Related tools

- **MetaClean** (R package providing runCrossValidation, getEvaluationMeasures, getBarPlots, and getCDPlots wrapper functions to train candidate classifiers and rank them statistically) — https://github.com/KelseyChetnik/MetaClean
- **caret** (underlying R machine learning package that implements the 8 classification algorithms (DecisionTree, LogisticRegression, NaiveBayes, RandomForest, SVM_Linear, AdaBoost, NeuralNetwork, ModelAveragedNeuralNetwork) wrapped by MetaClean)
- **MetaCleanData** (R package providing example peak quality metrics matrices (pqm_development, pqm_test) for prototyping and validation) — https://github.com/KelseyChetnik/MetaCleanData
- **R** (programming environment for executing runCrossValidation, getEvaluationMeasures, and statistical ranking functions)

## Examples

```
runCrossValidation(pqm_development, k=5, repNum=10, rand.seed=453, algorithms=c('DecisionTree','LogisticRegression','NaiveBayes','RandomForest','SVM_Linear','AdaBoost','NeuralNetwork','ModelAveragedNeuralNetwork'), metricSet='M11')
```

## Evaluation signals

- Cross-validation execution completes without error and returns a list of lists containing trained models, hyperparameters, and fold-wise predictions for all algorithms and repetitions.
- Evaluation measure matrix is complete (no missing values) with one row per fold per repetition per algorithm, and all metrics (Pass_FScore, Fail_FScore, Accuracy, Precision, Recall) in valid numeric range [0, 1].
- Bar plots show non-overlapping or minimally overlapping confidence intervals for at least two algorithms, indicating differentiation in performance.
- CD plot displays statistically significant groups (e.g., Friedman-Demšar p < 0.05) with the selected best algorithm ranked in the top group and separated from lower-ranked competitors.
- Reproducibility check: re-running the same workflow with the same random seed (e.g., 453) and same fold count (e.g., 5) and repetition count (e.g., 10) on the same input matrix reproduces identical mean evaluation scores and algorithm rankings.

## Limitations

- MetaClean's default metric set is M11 (11 peak-quality metrics); choice of metric set can influence which algorithm ranks best, so results may not generalize to other metric sets (M1, M2, etc.) without re-running cross-validation.
- Cross-validation is computationally expensive with 5 folds × 10 repetitions × 8–9 algorithms; runtime scales with peak matrix size and algorithm complexity (e.g., Neural Networks slower than Decision Trees).
- Statistical ranking via Friedman-Demšar CD plots assumes independence of fold-wise scores, which may be violated if samples are highly correlated (e.g., technical replicates from the same run).
- Selected best algorithm is conditional on the training data distribution and metric set; performance may degrade on test data if test set has different quality characteristics or is enriched in rare peak types.
- No changelog or versioning available for MetaClean, so results may vary across package versions without explicit documentation of algorithmic changes.

## Evidence

- [methods] runCrossValidation function parameter specification: "The runCrossValidation function is a wrapper function that uses cross-validation to train a user-selected subset of the 8 available algorithms."
- [methods] evaluation measures computed after cross-validation: "We use the getEvaluationMeasures function to do this."
- [methods] statistical ranking via CD plots: "MetaClean also provides a wrapper function to easily generate CD plots of the evaluation measures for each model. This is getCDPlots"
- [readme] 9 diverse algorithms available in MetaClean: "MetaClean utilizes 12 peak-quality metrics and 9 diverse machine learning algorithms to build a classifier to detect and flag low-quality peaks in untargeted metabolomics data."
- [methods] repeated k-fold cross-validation workflow step: "Train Potential Classifiers"
