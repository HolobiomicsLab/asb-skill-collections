---
name: classification-performance-visualization
description: Use when you have a CSV file with predicted probabilities and true binary
  labels from a classification model, and you need to evaluate classification performance
  across decision thresholds and communicate it via a standard diagnostic plot suitable
  for publication or presentation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_2269
  - http://edamontology.org/topic_0092
  tools:
  - R Shiny
  - Docker
  license_tier: open
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

# classification-performance-visualization

## Summary

Generate publication-quality ROC curve visualizations to assess binary classification model performance. This skill computes receiver operating characteristic curves from predicted probabilities and true labels, calculates the Area Under the Curve (AUC) metric, and renders the curve as a figure with AUC displayed.

## When to use

You have a CSV file with predicted probabilities and true binary labels from a classification model, and you need to evaluate classification performance across decision thresholds and communicate it via a standard diagnostic plot suitable for publication or presentation.

## When NOT to use

- Input is multiclass classification (not binary); use one-vs-rest decomposition or alternative metrics (e.g., macro/micro averaged ROC) instead.
- Predicted probabilities are not properly calibrated or are missing; imputation or recalibration required first.
- True labels are imbalanced and ROC is the only metric; supplement with precision–recall curves or F1 scores to account for class imbalance.

## Inputs

- CSV file containing predicted probabilities (numeric, 0–1 range) and true binary class labels (binary, 0/1 or equivalent)

## Outputs

- ROC curve plot (PNG or PDF) with axes labeled true positive rate (y-axis) and false positive rate (x-axis)
- Area Under the Curve (AUC) metric displayed on or reported with the plot
- Optionally: tabular ROC coordinates (threshold, TPR, FPR) for further analysis

## How to apply

Load the ROC demo CSV (roc_example.csv) containing predicted probabilities and true labels into R Shiny or a statistical environment. Calculate the ROC curve by computing true positive rate and false positive rate across classification thresholds using R or Python statistical libraries (e.g., sklearn.metrics.roc_curve in Python or pROC in R). Compute the Area Under the Curve (AUC) metric from the ROC curve. Render the ROC curve as a publication-quality figure with AUC displayed on the plot and save as a PNG or PDF file. The GraphBio Shiny application encapsulates this workflow, allowing interactive upload and visualization without manual scripting.

## Related tools

- **R Shiny** (Interactive web framework for uploading ROC CSV input, triggering ROC computation, and rendering the curve visualization in real time) — github.com/databio2022/GraphBio
- **Docker** (Containerization system for deploying GraphBio (including ROC module) as a standalone web service) — github.com/databio2022/GraphBio

## Examples

```
# In GraphBio R Shiny: upload roc_example.csv via the web interface, select the 'ROC curve' module, specify predicted probability and true label columns, click 'Generate', download the resulting ROC plot (PNG/PDF) with AUC displayed.
```

## Evaluation signals

- ROC curve is monotonically non-decreasing (true positive rate increases or stays constant as false positive rate increases).
- AUC value is between 0 and 1; AUC = 0.5 indicates random classifier performance; AUC = 1.0 indicates perfect separation.
- Visual inspection: curve passes through (0,0) and (1,1); lies above the diagonal line of random performance.
- Output file exists and is readable (PNG or PDF); plot title and axis labels are present and legible.
- Reproducibility: same input CSV yields identical AUC and curve coordinates across repeated runs.

## Limitations

- ROC curves are designed for binary classification; multiclass scenarios require aggregation (one-vs-rest) or alternative metrics.
- ROC curves do not account for class imbalance; a high AUC may hide poor performance on the minority class. Supplement with precision–recall curves or F1 scores when classes are severely imbalanced.
- Requires predicted probabilities (not just hard predictions); if only predicted classes are available, probabilistic output must be generated first.
- AUC assumes the cost of false positives and false negatives are equal; domain-specific thresholds may differ from the ROC optimum.

## Evidence

- [other] The ROC curve component consumes a CSV file (roc_example.csv) as input to perform ROC curve analysis and visualization.: "The ROC curve component consumes a CSV file (roc_example.csv) as input to perform ROC curve analysis and visualization."
- [other] Calculate the ROC curve by computing true positive rate and false positive rate across classification thresholds using R or Python statistical libraries.: "Calculate the ROC curve by computing true positive rate and false positive rate across classification thresholds using R or Python statistical libraries."
- [other] Compute the Area Under the Curve (AUC) metric from the ROC curve.: "Compute the Area Under the Curve (AUC) metric from the ROC curve."
- [other] Render the ROC curve as a publication-quality figure with AUC displayed on the plot and save as a PNG or PDF file.: "Render the ROC curve as a publication-quality figure with AUC displayed on the plot and save as a PNG or PDF file."
- [readme] GraphBio---A modular and scalable R Shiny dashboard: "GraphBio---A modular and scalable R Shiny dashboard"
- [readme] roc_example.csv for ROC curve: "roc_example.csv for ROC curve"
