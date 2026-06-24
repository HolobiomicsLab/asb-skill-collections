---
name: metabolite-disease-correlation-computation
description: 'Use when after training a DeepMSProfiler deep learning model and generating
  per-sample predictions and metabolite signal intensities, use this skill when you
  need to: (1) identify which metabolites are most strongly associated with each disease
  class, (2) generate publication-ready visualizations.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - Python (matplotlib, seaborn)
  - DeepMSProfiler
  - SciPy / NumPy
  license_tier: restricted
derived_from:
- doi: 10.1038/s41467-024-51433-3
  title: DeepMSProfiler
evidence_spans: []
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

# metabolite-disease-correlation-computation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Compute correlation coefficients between individual metabolite signal intensities and disease class labels across all samples, then construct and visualize a correlation matrix as a heatmap to reveal disease-associated metabolic signatures. This skill transforms raw model outputs into interpretable disease-metabolite associations.

## When to use

After training a DeepMSProfiler deep learning model and generating per-sample predictions and metabolite signal intensities, use this skill when you need to: (1) identify which metabolites are most strongly associated with each disease class, (2) generate publication-ready visualizations of metabolite-disease relationships, or (3) validate that learned features correspond to biologically meaningful metabolic differences between disease groups.

## When NOT to use

- Input metabolite data is already aggregated by disease group (correlation computation requires per-sample intensities and labels, not group means).
- Disease labels are continuous (e.g., disease severity score) rather than categorical; consider regression or rank correlation instead.
- Metabolite intensities contain missing values or extreme outliers that have not been preprocessed; imputation or normalization should precede correlation.

## Inputs

- Per-sample model predictions (class labels for each sample)
- Per-sample metabolite signal intensities (~341 metabolites × N samples)
- Disease class labels for all samples (categorical: e.g., 'health', 'nodule', 'cancer')

## Outputs

- Correlation matrix (metabolites × diseases, numeric values in [-1, 1])
- Heatmap visualization (high-resolution image file)
- Feature results array (.npy format) containing heatmap for ensemble models

## How to apply

Load the per-sample model outputs (sample predictions and metabolite signal intensities) from the trained DeepMSProfiler model. Compute correlation coefficients (Pearson or Spearman) between each of the ~341 metabolite signals and disease class labels (encoded numerically) across all samples. Construct a 2D correlation matrix with metabolites as rows and disease classes as columns. Generate a heatmap visualization using Python libraries (matplotlib/seaborn) with color intensity encoding correlation magnitude and direction (typically diverging colormap: negative = blue, zero = white, positive = red). Export the heatmap as a high-resolution image file (PNG/SVG).

## Related tools

- **Python (matplotlib, seaborn)** (Generate heatmap visualization from correlation matrix)
- **DeepMSProfiler** (Source tool that trains model and outputs per-sample metabolite intensities and predictions used as input to this correlation workflow) — https://github.com/yjdeng9/DeepMSProfiler
- **SciPy / NumPy** (Compute Pearson or Spearman correlation coefficients between metabolite signals and disease labels)

## Examples

```
python showFeature.py
```

## Evaluation signals

- Correlation matrix shape matches expectations: [~341 metabolites × number of disease classes], with all values in [-1, 1].
- Heatmap visual inspection: metabolites with known disease associations should show strong correlations (|r| > 0.5) in expected disease columns; background should appear neutral (near-white for correlation ≈ 0).
- No NaN or inf values in correlation matrix; all cells contain valid numeric correlation coefficients.
- Heatmap color scale is correctly oriented (red = positive correlation, blue = negative correlation, white ≈ 0) and labeled with metabolite and disease identifiers.
- Exported image file has sufficient resolution (≥300 DPI) and is readable for publication.

## Limitations

- Correlation magnitude does not imply causation or biological relevance; statistically significant correlations may reflect technical artifacts or confounding.
- Pearson correlation assumes linear relationships; non-linear metabolite-disease associations will be underestimated.
- Disease class imbalance in the training set can bias correlations toward overrepresented classes.
- Raw metabolite signal intensities may contain batch effects, normalization biases, or instrument drift not accounted for in correlation; preprocessing quality affects result interpretation.

## Evidence

- [other] Compute correlation coefficients (e.g., Pearson or Spearman) between each metabolite signal and disease class labels for all samples.: "Compute correlation coefficients (e.g., Pearson or Spearman) between each metabolite signal and disease class labels for all samples."
- [other] Construct a correlation matrix with metabolites as rows and diseases as columns.: "Construct a correlation matrix with metabolites as rows and diseases as columns."
- [other] Generate heatmap visualization using a Python plotting library (e.g., matplotlib, seaborn), with rows representing metabolites, columns representing diseases, and cell colors encoding correlation magnitude and direction.: "Generate heatmap visualization using a Python plotting library (e.g., matplotlib, seaborn), with rows representing metabolites, columns representing diseases, and cell colors encoding correlation"
- [readme] It takes raw metabolomics data from different disease groups as input and provides three main outputs: 1. Sample disease type labels. 2. Heatmaps depicting the correlation of different metabolite signals with diseases.: "It takes raw metabolomics data from different disease groups as input and provides three main outputs: 1. Sample disease type labels. 2. Heatmaps depicting the correlation of different metabolite"
- [readme] After `run_feature` ,the heatmaps were saved in `../jobs/jobs007/feature_results/ensemble_RISE.npy`: "the heatmaps were saved in `../jobs/jobs007/feature_results/ensemble_RISE.npy`"
