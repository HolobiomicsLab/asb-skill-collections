---
name: python-scientific-visualization
description: Use when you have per-sample model predictions and metabolite signal
  intensities from a trained deep learning model (e.g., DeepMSProfiler) and need to
  visualize which metabolites correlate most strongly with specific disease phenotypes.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - Python matplotlib
  - Python seaborn
  - Python numpy
  - DeepMSProfiler
  license_tier: open
derived_from:
- doi: 10.1038/s41467-024-51433-3
  title: DeepMSProfiler
evidence_spans:
- code style-pep8
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_deepmsprofiler_cq
    doi: 10.1038/s41467-024-51433-3
    title: DeepMSProfiler
  dedup_kept_from: coll_deepmsprofiler_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-024-51433-3
  all_source_dois:
  - 10.1038/s41467-024-51433-3
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Reconstruct generation of metabolite-disease correlation heatmaps

## Summary

Generate publication-quality heatmap visualizations that depict correlations between metabolite signal intensities and disease class labels from deep learning model outputs. This skill transforms numerical correlation matrices into color-encoded 2D grids suitable for identifying disease-associated metabolite signatures.

## When to use

You have per-sample model predictions and metabolite signal intensities from a trained deep learning model (e.g., DeepMSProfiler) and need to visualize which metabolites correlate most strongly with specific disease phenotypes. Use this when exploratory analysis of metabolite-disease associations is the goal and you want to communicate patterns across multiple metabolites and disease groups simultaneously.

## When NOT to use

- Input is already a pre-computed correlation matrix from an external tool — use directly without recomputing correlations.
- Disease phenotype is continuous rather than categorical — consider regression-based scatter plots or 2D scatter matrices instead.
- Sample size is <10 per disease group — correlation estimates will be unstable; consider alternative visualizations or aggregation strategies.

## Inputs

- Per-sample model output predictions (numpy array or pandas DataFrame)
- Metabolite signal intensity matrix (samples × metabolites)
- Disease class labels (sample × 1 categorical vector)
- Sample identifiers (optional, for row/column annotation)

## Outputs

- Correlation matrix (metabolites × diseases, numeric)
- Heatmap visualization (PNG/SVG image file)
- Heatmap array in serializable format (e.g., .npy file)

## How to apply

Load per-sample model outputs (sample predictions and metabolite signal intensities) from the trained model. Compute correlation coefficients (Pearson or Spearman) between each metabolite signal intensity and disease class labels across all samples. Construct a correlation matrix with metabolites as rows and diseases as columns, ensuring both dimensions are labeled. Use Python visualization libraries (matplotlib or seaborn) to render the matrix as a heatmap, with cell colors encoding both magnitude and direction of correlation (e.g., blue for negative, red for positive). Export as a high-resolution image file (PNG or SVG) for publication.

## Related tools

- **Python matplotlib** (Core plotting library for rendering heatmap visualization with customizable colormap, axis labels, and figure formatting)
- **Python seaborn** (Statistical visualization library providing high-level heatmap function with clustering and annotation options)
- **Python numpy** (Numerical computation of correlation coefficients (Pearson/Spearman) and matrix construction)
- **DeepMSProfiler** (Upstream deep learning model that generates per-sample predictions and metabolite signal intensities used as inputs) — https://github.com/yjdeng9/DeepMSProfiler

## Examples

```
from DeepMSProfiler import *; run_feature(job_dir='DeepMSProfiler/example/out/jobs007'); show_feature(job_dir='DeepMSProfiler/example/out/jobs007', mode='ensemble')
```

## Evaluation signals

- Heatmap dimensions match input: rows = number of unique metabolites, columns = number of unique disease classes.
- Correlation values are bounded in [-1, 1] for Pearson or [-1, 1] for Spearman; check for NaN or infinite values.
- Color scale is bidirectional (e.g., diverging blue-white-red) and symmetric around zero to preserve interpretation of positive vs. negative correlations.
- Row and column labels are legible and correspond to metabolite and disease identifiers in the input data; no missing or misaligned labels.
- Output image resolution is ≥300 dpi and saved in a lossless or high-quality format (PNG/SVG) suitable for publication.

## Limitations

- Pearson correlation assumes linear relationships; metabolite-disease associations may be nonlinear and not be captured.
- Correlation magnitude is sensitive to outliers and skewed distributions; preprocessing (log-transformation, outlier removal) is often required but not automated.
- Multiple hypothesis testing across many metabolites inflates false discovery rate; no built-in p-value correction or multiple testing control is mentioned in the README.
- Heatmap interpretation depends on adequate sample size per disease group; small sample sizes lead to unstable correlation estimates.
- Missing data (NaN values) in metabolite intensities or disease labels will cause correlation computation to fail unless explicitly handled.

## Evidence

- [other] Compute correlation coefficients (e.g., Pearson or Spearman) between each metabolite signal and disease class labels for all samples.: "Compute correlation coefficients (e.g., Pearson or Spearman) between each metabolite signal and disease class labels for all samples."
- [other] Construct a correlation matrix with metabolites as rows and diseases as columns.: "Construct a correlation matrix with metabolites as rows and diseases as columns."
- [other] Generate heatmap visualization using a Python plotting library (e.g., matplotlib, seaborn), with rows representing metabolites, columns representing diseases, and cell colors encoding correlation magnitude and direction.: "Generate heatmap visualization using a Python plotting library (e.g., matplotlib, seaborn), with rows representing metabolites, columns representing diseases, and cell colors encoding correlation"
- [readme] Heatmaps depicting the correlation of different metabolite signals with diseases.: "Heatmaps depicting the correlation of different metabolite signals with diseases."
- [readme] It takes raw metabolomics data from different disease groups as input and provides three main outputs: 1. Sample disease type labels. 2. Heatmaps depicting the correlation of different metabolite: "It takes raw metabolomics data from different disease groups as input and provides three main outputs: 1. Sample disease type labels. 2. Heatmaps depicting the correlation of different metabolite"
