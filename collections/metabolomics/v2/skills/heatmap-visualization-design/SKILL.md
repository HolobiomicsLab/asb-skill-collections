---
name: heatmap-visualization-design
description: 'Use when after training a DeepMSProfiler model and generating per-sample
  predictions: when you need to display Pearson or Spearman correlation coefficients
  between individual metabolite signals and disease class labels in a matrix form
  suitable for publication or exploratory review of.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - seaborn
  - matplotlib
  - DeepMSProfiler
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
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

# heatmap-visualization-design

## Summary

Generate color-encoded correlation heatmaps that depict relationships between metabolite signals and disease classes from deep learning model outputs. This visualization enables rapid identification of disease-associated metabolite signatures in mass spectrometry data.

## When to use

After training a DeepMSProfiler model and generating per-sample predictions: when you need to display Pearson or Spearman correlation coefficients between individual metabolite signals and disease class labels in a matrix form suitable for publication or exploratory review of metabolite-disease associations.

## When NOT to use

- Input is raw, un-normalized LC-MS spectra (not model-processed feature signals).
- Disease labels are continuous rather than categorical (use scatter plots or 2D density plots instead).
- Sample size is <10 per disease class (correlation estimates become unstable and heatmap becomes sparse).

## Inputs

- Per-sample model outputs (sample predictions from trained DeepMSProfiler ensemble)
- Metabolite signal intensity matrix (features × samples)
- Disease class labels (categorical, one per sample)

## Outputs

- Correlation heatmap image (PNG/SVG format)
- Correlation matrix (NumPy .npy array; shape: num_diseases × num_metabolites)
- Heatmap metadata (colorbar scale, correlation range)

## How to apply

Load per-sample model outputs (metabolite signal intensities and disease predictions) from a trained DeepMSProfiler job directory. Compute correlation coefficients (Pearson or Spearman) between each metabolite feature and disease class labels across all samples. Construct a correlation matrix with metabolites as rows and diseases as columns, ensuring values are normalized for color mapping. Render the matrix using seaborn or matplotlib with a diverging colormap (e.g., coolwarm or RdBu) to encode both magnitude and direction of correlation; export as high-resolution PNG or SVG. The heatmap is typically generated as part of the feature extraction pipeline (`run_feature`) after model prediction completes.

## Related tools

- **seaborn** (Python library for rendering correlation heatmaps with customizable color palettes and annotations)
- **matplotlib** (Underlying plotting backend for heatmap image generation and export)
- **DeepMSProfiler** (Deep learning framework that generates model outputs and feature extraction pipeline; heatmap generation is invoked via run_feature() or -run_feature flag) — https://github.com/yjdeng9/DeepMSProfiler

## Examples

```
python showFeature.py
```

## Evaluation signals

- Heatmap shape matches expected dimensions (num_metabolites × num_diseases); verify via .npy file shape inspection.
- Correlation values are bounded in [-1, 1] or [0, 1] depending on coefficient type; no NaN or inf values in matrix.
- Rows (metabolites) and columns (diseases) are labeled and legible; color intensity visually corresponds to magnitude (darker = stronger correlation).
- High-correlation metabolites cluster visually and align with known biomarkers or prior metabolomic literature for the disease context.
- Heatmap output file size and DPI are appropriate for publication (≥300 DPI for PNG; vector format preferred for SVG).

## Limitations

- Correlation-based heatmaps assume linear relationships; nonlinear metabolite-disease associations may be masked.
- Pearson correlation is sensitive to outliers; Spearman is preferred for skewed metabolomics distributions but may reduce power with small sample sizes.
- Heatmap does not encode statistical significance (p-values); multiple-testing correction not applied by default in DeepMSProfiler.
- Feature ordering (row/column clustering) is not applied by default; manual reordering may be needed to reveal biological patterns.
- High-dimensional metabolite sets (>1000 features) produce unreadable heatmaps; filtering to top differentially correlated metabolites is recommended.

## Evidence

- [other] Compute correlation coefficients (e.g., Pearson or Spearman) between each metabolite signal and disease class labels for all samples.: "Compute correlation coefficients (e.g., Pearson or Spearman) between each metabolite signal and disease class labels for all samples."
- [other] Construct a correlation matrix with metabolites as rows and diseases as columns.: "Construct a correlation matrix with metabolites as rows and diseases as columns."
- [other] Generate heatmap visualization using a Python plotting library (e.g., matplotlib, seaborn), with rows representing metabolites, columns representing diseases, and cell colors encoding correlation magnitude and direction.: "Generate heatmap visualization using a Python plotting library (e.g., matplotlib, seaborn), with rows representing metabolites, columns representing diseases, and cell colors encoding correlation"
- [readme] Heatmaps depicting the correlation of different metabolite signals with diseases.: "Heatmaps depicting the correlation of different metabolite signals with diseases."
- [readme] After `run_feature` ,the heatmaps were saved in `../jobs/jobs007/feature_results/ensemble_RISE.npy`, so we can then show the feature heatmaps for different classes.: "After `run_feature` ,the heatmaps were saved in `../jobs/jobs007/feature_results/ensemble_RISE.npy`"
