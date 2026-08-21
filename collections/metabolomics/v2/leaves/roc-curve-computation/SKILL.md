---
name: roc-curve-computation
description: Use when you have paired columns of predicted probabilities (or decision
  scores) and true binary class labels, and need to assess classifier discrimination
  ability across all decision thresholds.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3391
  tools:
  - R Shiny
  - Docker
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.3389/fgene.2022.957317
  title: GraphBio
evidence_spans:
- GraphBio---A modular and scalable R Shiny dashboard
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_graphbio_cq
    doi: 10.3389/fgene.2022.957317
    title: GraphBio
  dedup_kept_from: coll_graphbio_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3389/fgene.2022.957317
  all_source_dois:
  - 10.3389/fgene.2022.957317
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# roc-curve-computation

## Summary

Compute and visualize receiver operating characteristic (ROC) curves from predicted probabilities and true binary labels, quantifying classifier performance across all classification thresholds via the Area Under the Curve (AUC) metric. This skill is essential for evaluating and comparing binary classification models in omics and biomedical contexts.

## When to use

Apply this skill when you have paired columns of predicted probabilities (or decision scores) and true binary class labels, and need to assess classifier discrimination ability across all decision thresholds. Common triggers include: post-hoc evaluation of a trained classifier, comparison of multiple models' performance, or publication-quality ROC visualization for methods papers.

## When NOT to use

- Input data are already aggregated metrics (sensitivity, specificity) rather than raw predictions and labels — use existing ROC coordinates directly instead.
- The classification task is multiclass (>2 classes) — use one-vs-rest ROC strategies or alternative metrics like macro-averaged AUC.
- Labels are continuous or soft probabilities rather than hard binary assignments — consider calibration or probability integral transform first.

## Inputs

- CSV file with columns: predicted probabilities (numeric, 0–1 range) and true labels (binary: 0/1 or similar)
- roc_example.csv (GraphBio demo format)

## Outputs

- ROC curve plot (PNG or PDF image file)
- AUC scalar value (numeric, 0–1 range)
- True positive rate and false positive rate coordinates (optional, for inspection)

## How to apply

Load a CSV file containing predicted probabilities and true binary labels (formatted as columns in roc_example.csv). Calculate the ROC curve by computing the true positive rate and false positive rate across a range of classification thresholds using R or Python statistical libraries (e.g., sklearn.metrics, pROC package). Compute the Area Under the Curve (AUC) statistic from the ROC coordinates as a single summary metric of classifier performance. Render the ROC curve as a publication-quality figure with AUC value prominently displayed on the plot, and export as PNG or PDF for integration into reports or manuscripts.

## Related tools

- **R Shiny** (Interactive web framework for deploying ROC curve computation and visualization as a modular dashboard component with CSV upload and rendering) — github.com/databio2022/GraphBio
- **Docker** (Container deployment mechanism for scaling GraphBio ROC analysis module across multiple users) — github.com/databio2022/GraphBio

## Evaluation signals

- AUC value is a scalar in the range [0, 1]; AUC ≥ 0.5 indicates non-random performance; AUC = 1.0 indicates perfect separation.
- ROC curve is monotonically non-decreasing, passes through (0,0) and (1,1), and lies on or above the diagonal y=x (random classifier baseline).
- Plot contains axis labels ('False Positive Rate', 'True Positive Rate'), a clear legend with AUC value, and is in publication-quality format (high DPI, readable fonts).
- Output file (PNG/PDF) is non-empty and can be opened in standard image viewers without corruption.
- Sensitivity/specificity values across reported thresholds sum to expected trade-off pattern (increasing sensitivity correlates with decreasing specificity).

## Limitations

- ROC curves and AUC assume binary classification; multiclass problems require one-vs-rest or micro/macro averaging strategies not covered by this single-curve skill.
- AUC is insensitive to class imbalance and threshold selection — highly skewed datasets may require precision-recall curves or threshold-aware metrics as supplementary evaluation.
- The skill does not address confidence intervals, statistical significance testing, or hypothesis testing across multiple classifiers; those require additional statistical inference.
- CSV input format and column naming are not explicitly validated in the GraphBio README; malformed or missing data columns may cause silent failures or rendering errors.

## Evidence

- [other] The ROC curve component consumes a CSV file (roc_example.csv) as input to perform ROC curve analysis and visualization.: "The ROC curve component consumes a CSV file (roc_example.csv) as input to perform ROC curve analysis and visualization."
- [other] Load the ROC demo CSV (roc_example.csv) containing predicted probabilities and true labels. Calculate the ROC curve by computing true positive rate and false positive rate across classification thresholds using R or Python statistical libraries. Compute the Area Under the Curve (AUC) metric from the ROC curve. Render the ROC curve as a publication-quality figure with AUC displayed on the plot and save as a PNG or PDF file.: "Calculate the ROC curve by computing true positive rate and false positive rate across classification thresholds using R or Python statistical libraries. Compute the Area Under the Curve (AUC) metric"
- [readme] GraphBio: a shiny web app to easily perform popular visualization analysis for omics data: "GraphBio: a shiny web app to easily perform popular visualization analysis for omics data"
- [readme] roc_example.csv for ROC curve: "roc_example.csv for ROC curve"
