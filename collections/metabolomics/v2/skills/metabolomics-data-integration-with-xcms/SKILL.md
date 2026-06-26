---
name: metabolomics-data-integration-with-xcms
description: Use when you have untargeted LC-MS metabolomics data preprocessed with
  XCMS and need to filter out low-quality peak integrations that could introduce false
  positives or noise into metabolite quantification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
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

# metabolomics-data-integration-with-xcms

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Integrate peak-quality assessment into untargeted LC-MS metabolomics preprocessing pipelines by coupling XCMS chromatographic peak detection with MetaClean's machine learning classifier for flagging low-quality peaks. This skill enables quality control of extracted ion chromatograms (EICs) and peaks before downstream analysis.

## When to use

You have untargeted LC-MS metabolomics data preprocessed with XCMS and need to filter out low-quality peak integrations that could introduce false positives or noise into metabolite quantification. Apply this skill when you want to automatically detect and flag EICs with poor signal-to-noise, baseline drift, or integration artifacts before statistical analysis or annotation.

## When NOT to use

- Your LC-MS data has not yet been preprocessed with XCMS or an equivalent peak-detection tool; MetaClean operates on detected peaks, not raw spectra.
- You have only a small number of peaks (<100) or an unlabeled dataset with no ground truth for classifier training; MetaClean requires sufficient labeled data to train and validate robust models.
- You are working with targeted or data-independent acquisition (DIA) workflows where peak detection is not the primary quality bottleneck; MetaClean is designed for untargeted metabolomics EIC quality assessment.

## Inputs

- XCMS-preprocessed peak detection results (mzML or NetCDF format LC-MS data)
- Extracted ion chromatograms (EICs) with retention time, m/z, and intensity profiles
- Labeled peak-quality ground truth (for development/training set)
- MetaCleanData example data (pqm_development, pqm_test) or user-provided peak quality metrics matrix

## Outputs

- Trained MetaClean classifier model (e.g., AdaBoost_M11.model)
- Peak-quality predictions with pass/fail flags and confidence scores for each EIC
- Evaluation metrics (Pass_FScore, Fail_FScore, Accuracy, Precision, Recall) and model comparison plots (bar plots, CD plots)
- Filtered EIC list with low-quality peaks flagged or removed

## How to apply

Install MetaClean alongside your existing XCMS preprocessing pipeline. After XCMS peak detection, extract EICs and apply MetaClean's getPeakQualityMetrics function to compute 11–12 quality metrics (adapted from Zhang & Zhao 2014 and Eshghi et al. 2018) on each detected peak. Use runCrossValidation with k=5 folds and multiple repetitions to identify the best-performing machine learning algorithm (e.g., AdaBoost, RandomForest, or SVM) on a labeled development set using the M11 metric set. Once the best model is selected via statistical ranking (e.g., CD plots), train a final classifier using trainClassifier, then apply getPredictions to score test or production EICs and assign each peak a quality flag. Optionally filter by RSD % using rsdFilter before metric calculation to reduce computational burden.

## Related tools

- **XCMS** (Performs chromatographic peak detection and EIC extraction on raw LC-MS data; MetaClean integrates downstream to assess quality of XCMS-detected peaks.)
- **MetaClean** (Core tool for computing 11–12 peak-quality metrics and training/applying machine learning classifiers to detect low-quality peaks.) — https://github.com/KelseyChetnik/MetaClean
- **MetaCleanData** (Provides example development and test datasets for training and validating MetaClean classifiers.) — https://github.com/KelseyChetnik/MetaCleanData
- **caret** (R package underlying MetaClean's implementation of 8 classification algorithms (DecisionTree, LogisticRegression, NaiveBayes, RandomForest, SVM_Linear, AdaBoost, NeuralNetwork, ModelAveragedNeuralNetwork).)
- **R** (Programming environment for running MetaClean and generating evaluation visualizations.)

## Examples

```
runCrossValidation(pqm_development, k=5, repNum=10, rand.seed=453, algorithms=c('DecisionTree','LogisticRegression','NaiveBayes','RandomForest','SVM_Linear','AdaBoost','NeuralNetwork','ModelAveragedNeuralNetwork'), metricSet='M11')
```

## Evaluation signals

- Cross-validation fold results are reproducible: runCrossValidation with identical rand.seed, k, and repNum parameters produces identical model rankings and evaluation metrics across repeated runs.
- Statistical ranking via CD (Friedman-Demšar) plots shows clear differentiation among algorithms; the selected 'best' model has significantly lower average rank and confidence interval that does not overlap with lower-ranked competitors.
- Pass_FScore, Fail_FScore, and Accuracy metrics for the best-performing model on the held-out test set meet or exceed domain-specific thresholds (e.g., Fail_FScore ≥ 0.80 to reliably detect low-quality peaks).
- Predictions on new EICs are assigned confidence scores; predictions with high confidence (>0.9) on a validation set show >90% agreement with manual quality assessment or spike-in ground truth.
- Bar plots and CD plots generated by getBarPlots and getCDPlots show no visual anomalies (e.g., extreme outliers, missing algorithms, reversed metric scales) and confirm ranking consistency across evaluation measures.

## Limitations

- MetaClean uses 8 or 9 classification algorithms (source cards mention both counts); performance is sensitive to the choice of algorithm and metric set (e.g., M11), requiring cross-validation to select the best pair.
- The 11–12 peak-quality metrics are adapted from literature but may not capture all types of integration artifacts in user-specific LC-MS methods; metric relevance depends on ionization mode, chromatographic resolution, and sample complexity.
- MetaClean requires labeled training data (ground truth peak-quality annotations); de novo quality assessment without labeled data is not supported.
- No changelog or versioning documentation is available; reproducibility across MetaClean releases or dependencies (caret, R versions) is not guaranteed.
- The skill is demonstrated on small example datasets (MetaCleanData); scalability to large untargeted metabolomics cohorts (>10,000 peaks) is not explicitly validated.

## Evidence

- [readme] MetaClean utilizes 12 peak-quality metrics and 9 diverse machine learning algorithms to build a classifier to detect and flag low-quality peaks in untargeted metabolomics data.: "MetaClean utilizes 12 peak-quality metrics and 9 diverse machine learning algorithms to build a classifier to detect and flag low-quality peaks in untargeted metabolomics data"
- [intro] can be easily incorporated into existing untargeted LC-MS metabolomics pipelines that utilize the pre-processing software XCMS: "can be easily incorporated into existing untargeted LC-MS metabolomics pipelines that utilize the pre-processing software XCMS"
- [methods] The package is designed for use with the preprocessing package XCMS and can be easily integrated into existing untargeted metabolomics pipelines.: "The package is designed for use with the preprocessing package XCMS and can be easily integrated into existing untargeted metabolomics pipelines"
- [readme] The 12 peak-quality metrics used by MetaClean are adapted from the following publications: Zhang, W., & Zhao, P. X. (2014)… and Eshghi, S. T., Auger, P., & Mathews, W. R. (2018).: "The 12 peak-quality metrics used by MetaClean are adapted from the following publications… (2014)… and (2018)"
- [methods] MetaClean provides 8 classification algorithms (implemented with the R package caret): "MetaClean provides 8 classification algorithms (implemented with the R package caret)"
- [methods] runCrossValidation function is a wrapper function that uses cross-validation to train a user-selected subset of the 8 available algorithms.: "runCrossValidation function is a wrapper function that uses cross-validation to train a user-selected subset of the 8 available algorithms"
- [methods] MetaCleanData provides example data for development and test sets.: "MetaCleanData provides example data for development and test sets"
- [methods] getCDPlots… also provides a wrapper function to easily generate CD plots of the evaluation measures for each model.: "MetaClean also provides a wrapper function to easily generate CD plots of the evaluation measures for each model"
