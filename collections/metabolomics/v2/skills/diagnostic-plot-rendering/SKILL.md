---
name: diagnostic-plot-rendering
description: Use when when you have computed statistical or classification results (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3673
  - http://edamontology.org/topic_0203
  tools:
  - R Shiny
  - Docker
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

# diagnostic-plot-rendering

## Summary

Render publication-quality diagnostic and statistical plots (ROC curves, volcano plots, heatmaps, MA plots, survival curves) from omics or classification data using R Shiny, with metrics overlaid and output as PNG or PDF files suitable for manuscript inclusion.

## When to use

When you have computed statistical or classification results (e.g., true positive/false positive rates, log-fold-changes, p-values, survival data, correlation networks) and need to generate a polished, interactive or static visualization that communicates the result to a scientific audience. Specifically, when input data is a CSV containing pre-computed metrics (probabilities, fold-changes, p-values, group labels) and you want the plot to include overlaid statistics (AUC, effect sizes) and be exportable as a high-resolution figure.

## When NOT to use

- Input is raw, unprocessed sequencing data (FASTQ, BAM, or raw count matrices) — pre-compute statistics first using differential expression, quality control, or classification pipelines.
- You need custom statistical models not implemented in the Shiny modules (e.g., Bayesian ROC curves, non-standard survival estimators) — extend the module or use standalone R/Python scripts.
- The data is too large (>10⁶ rows) to render interactively in Shiny without performance degradation — use static plotting backends or aggregate/subsample first.

## Inputs

- CSV file with pre-computed metrics (e.g., roc_example.csv containing predicted probabilities and true labels; volcano_example.csv with fold-change and p-value columns; ma_example.csv with M and A values)
- Optional: group or metadata CSV (e.g., group_info.csv for heatmap color annotations)
- Classification or omics data with ground-truth labels or biological covariates

## Outputs

- Publication-quality PNG or PDF figure with overlaid statistical metrics (AUC, p-values, effect sizes)
- Interactive Shiny widget displaying the plot with brushing/hover interactivity (if rendered in Shiny environment)
- Plot object (R ggplot2 or base graphics) suitable for programmatic downstream use

## How to apply

Load the pre-computed metrics CSV file into the R Shiny application corresponding to your plot type (e.g., roc_example.csv for ROC analysis, volcano_example.csv for volcano plots, ma_example.csv for MA plots). The Shiny module ingests the CSV, applies the appropriate statistical computation (e.g., ROC: compute true positive rate and false positive rate across classification thresholds using R statistical libraries), calculates summary metrics (e.g., AUC for ROC; effect size or significance for volcano plots), and renders the plot with these metrics overlaid. Configure plot aesthetics (colors, labels, axis ranges) within the Shiny interface, then export the finalized figure as PNG or PDF. Correctness is judged by: (1) the plot renders without errors, (2) overlaid metrics match independent statistical validation, (3) the output file is readable and publication-quality, and (4) visual encodings (e.g., significance thresholds, effect-size regions) align with standard conventions in the literature.

## Related tools

- **R Shiny** (Interactive web framework for uploading CSVs, configuring plot parameters, computing statistics, and rendering/exporting diagnostic plots) — https://github.com/databio2022/GraphBio
- **Docker** (Container runtime for deploying the GraphBio Shiny application to a web server with reproducible R/system dependencies)

## Evaluation signals

- Plot renders without R errors or missing data glyphs and occupies the full plotting area.
- Overlaid statistics (e.g., AUC value on ROC curve, p-value thresholds on volcano plot) are numerically consistent with independent computation (e.g., pROC::auc() in R or sklearn.metrics.auc() in Python).
- Exported PNG/PDF file opens in standard image viewers and retains resolution ≥300 DPI (or equivalent vector quality for PDF).
- Axis labels, legends, and statistical annotations are readable and follow omics or biostatistics conventions (e.g., volcano plots use log₂ fold-change on x-axis, −log₁₀ p-value on y-axis).
- Interactive features (if Shiny-rendered) respond to user brush/click events without lag and update plots within <2 seconds.

## Limitations

- The Shiny modules assume input CSVs are correctly formatted with expected column names and data types — malformed CSVs will cause silent failures or incorrect plots. Pre-validation of input format is recommended.
- Performance is limited by browser rendering for large datasets (>100K rows); interactive Shiny plots may become sluggish without data aggregation or sampling.
- Statistical computations within the modules are fixed (e.g., ROC uses standard threshold sweeps, no custom loss functions); novel or non-standard statistical methods require module extension or standalone pipelines.
- The README does not specify version-specific reproducibility guarantees or long-term maintenance commitments for Docker images.

## Evidence

- [other] Load the ROC demo CSV (roc_example.csv) containing predicted probabilities and true labels.: "Load the ROC demo CSV (roc_example.csv) containing predicted probabilities and true labels"
- [other] Calculate the ROC curve by computing true positive rate and false positive rate across classification thresholds using R or Python statistical libraries.: "Calculate the ROC curve by computing true positive rate and false positive rate across classification thresholds using R or Python statistical libraries"
- [other] Compute the Area Under the Curve (AUC) metric from the ROC curve.: "Compute the Area Under the Curve (AUC) metric from the ROC curve"
- [other] Render the ROC curve as a publication-quality figure with AUC displayed on the plot and save as a PNG or PDF file.: "Render the ROC curve as a publication-quality figure with AUC displayed on the plot and save as a PNG or PDF file"
- [readme] GraphBio: a shiny web app to easily perform popular visualization analysis for omics data: "GraphBio: a shiny web app to easily perform popular visualization analysis for omics data"
- [readme] roc_example.csv for ROC curve: "roc_example.csv for ROC curve"
