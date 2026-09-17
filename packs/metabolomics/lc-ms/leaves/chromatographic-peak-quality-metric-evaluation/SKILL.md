---
name: chromatographic-peak-quality-metric-evaluation
description: Use when when processing untargeted LC-MS metabolomics data with XCMS
  and need to identify low-quality peak integrations that may introduce noise or bias
  into subsequent compound identification and quantification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3957
  tools:
  - MetaClean
  - R
  - caret
  - devtools
  - XCMS
  - MetaCleanData
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

# chromatographic-peak-quality-metric-evaluation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Systematic evaluation of extracted ion chromatogram (EIC) and peak quality in LC-MS metabolomics data using 12 standardized peak-quality metrics and machine learning classification to detect and flag low-quality peaks before downstream analysis.

## When to use

When processing untargeted LC-MS metabolomics data with XCMS and need to identify low-quality peak integrations that may introduce noise or bias into subsequent compound identification and quantification. Apply this skill after XCMS preprocessing when EICs and peak tables are available but before statistical analysis or metabolite annotation.

## When NOT to use

- Input data are already curated or manually validated for peak quality; this skill is designed for automated detection of low-quality peaks in large-scale datasets.
- EIC and peak integration data are not available from XCMS or equivalent preprocessing; the skill requires structured peak boundaries and mass spectral signals as input.
- The analysis goal is peak detection or alignment rather than quality assessment; use XCMS directly for those tasks.

## Inputs

- EIC (extracted ion chromatogram) data objects from XCMS preprocessing
- Mass spectrometry signal matrices
- Peak integration results (retention time, peak area, boundary definitions)
- Peak quality metrics matrix (pqm_development, pqm_test) with labeled quality status (Pass/Fail)
- MetaCleanData example dataset or user-supplied LC-MS metabolomics data

## Outputs

- Peak quality metrics matrix with 12 calculated metrics per EIC
- Cross-validation evaluation measures (Pass_FScore, Fail_FScore, Accuracy, Precision, Recall) for each algorithm and fold
- Bar plot visualizations comparing classifier performance
- CD (Friedman-Demšar) plots and statistical rank matrices
- Trained classifier model (best-performing algorithm with optimized hyperparameters)
- Peak quality predictions on test data (Pass/Fail classifications per peak)

## How to apply

Load the EIC data, mass spectrometry signals, and peak integration results into MetaClean's evaluation object using getEvalObj(). Calculate all 12 peak-quality metrics (e.g., peak area, signal-to-noise ratio, baseline stability, peak shape symmetry) on each extracted ion chromatogram using getPeakQualityMetrics(). Optionally filter EICs by relative standard deviation (RSD %) using rsdFilter() to remove highly variable features. Train multiple machine learning classifiers (DecisionTree, LogisticRegression, NaiveBayes, RandomForest, SVM_Linear, AdaBoost, NeuralNetwork, ModelAveragedNeuralNetwork) using runCrossValidation() with k-fold cross-validation and multiple repetitions to compare performance on the peak quality metric matrix. Calculate evaluation measures (Pass_FScore, Fail_FScore, Accuracy, Precision, Recall) across all models and visualize using getBarPlots() and getCDPlots() with statistical ranking (Friedman-Demšar tests). Select the best-performing classifier based on mean evaluation scores and statistical significance rankings. Train the final classifier on the complete development dataset and apply it to flag low-quality peaks in test data.

## Related tools

- **MetaClean** (Primary framework for calculating 12 peak-quality metrics and training/comparing machine learning classifiers to detect low-quality peaks) — https://github.com/KelseyChetnik/MetaClean
- **XCMS** (Upstream peak detection and integration software; MetaClean is designed for integration into XCMS-based metabolomics pipelines to post-process and validate peak quality)
- **caret** (R machine learning framework underlying MetaClean's implementation of 8 classification algorithms)
- **MetaCleanData** (Example dataset repository providing development and test sets for reproducible cross-validation and model benchmarking) — https://github.com/KelseyChetnik/MetaCleanData
- **R** (Computing environment and language for executing MetaClean functions and statistical analysis)

## Examples

```
runCrossValidation(pqm_development, k=5, repNum=10, rand.seed=453, algorithms=c('AdaBoost','RandomForest','SVM_Linear','NeuralNetwork'), metricSet='M11')
```

## Evaluation signals

- Cross-validation evaluation measures (Pass_FScore, Fail_FScore, Accuracy) are calculated and reported for all trained models; expect Pass_FScore and Fail_FScore values between 0 and 1, with Accuracy reflecting balanced performance on both quality classes.
- CD (Friedman-Demšar) plots show statistically significant differences in classifier performance; the selected best model should be ranked #1 or #2 with no other models in its equivalence group.
- Bar plot visualizations reveal consistent ranking of classifiers across cross-validation folds, indicating stable model selection; high variance across folds signals potential overfitting or insufficient training data.
- Predictions on held-out test data are binary (Pass/Fail) for each EIC and match the expected ratio of high-quality to low-quality peaks based on manual inspection or domain knowledge (when available).
- Hyperparameter sets extracted from the trained models match the ranges defined in the cross-validation setup; model reproducibility is confirmed by retraining with the same seed (rand.seed=453) and obtaining identical evaluation scores.

## Limitations

- MetaClean uses 12 peak-quality metrics adapted from prior publications; metric relevance depends on the LC-MS method, ionization mode, and metabolite classes analyzed. Metrics may not generalize across different chromatographic or mass spectrometry protocols.
- Cross-validation performance is contingent on the quality and representativeness of labeled training data (pqm_development); datasets with extreme class imbalance or limited true low-quality examples may bias classifier selection.
- The choice of metric set (M11, M12, etc.) affects model performance; the article does not provide guidance on metric set selection for different metabolomics experiments.
- No changelog is available in the repository, limiting reproducibility across package versions and historical comparisons.

## Evidence

- [readme] MetaClean utilizes 12 peak-quality metrics and 9 diverse machine learning algorithms to build a classifier to detect and flag low-quality peaks in untargeted metabolomics data: "MetaClean utilizes 12 peak-quality metrics and 9 diverse machine learning algorithms to build a classifier to detect and flag low-quality peaks in untargeted metabolomics data"
- [readme] can be easily incorporated into existing untargeted LC-MS metabolomics pipelines that utilize the pre-processing software XCMS: "can be easily incorporated into existing untargeted LC-MS metabolomics pipelines that utilize the pre-processing software XCMS"
- [methods] The runCrossValidation function is a wrapper function that uses cross-validation to train a user-selected subset of the 8 available algorithms.: "The runCrossValidation function is a wrapper function that uses cross-validation to train a user-selected subset of the 8 available algorithms"
- [methods] MetaClean provides a simple wrapper function to easily generate bar plot visualizations of the evaluation measures for each model. This is getBarPlots: "MetaClean provides a simple wrapper function to easily generate bar plot visualizations of the evaluation measures for each model. This is getBarPlots"
- [methods] MetaClean also provides a wrapper function to easily generate CD plots of the evaluation measures for each model. This is getCDPlots: "MetaClean also provides a wrapper function to easily generate CD plots of the evaluation measures for each model. This is getCDPlots"
- [methods] The function getPeakQualityMetrics uses the evalObj objects to calculate each of the 11 peak quality metrics.: "The function getPeakQualityMetrics uses the evalObj objects to calculate each of the 11 peak quality metrics"
