---
name: multivariate-ordination-interpretation
description: Use when you have a collection of tandem MS/MS samples (stored in MassIVE) with GNPS spectral library annotations (m/z, retention time, compound identity), and you want to explore whether samples cluster by shared chemical features without predefined class labels.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3520
  tools:
  - ReDU
  - MassIVE
  - GNPS
  - Emperor
  - scikit-learn
derived_from:
- doi: 10.1038/s41592-020-0916-7
  title: ReDU
- doi: 10.1186/2047-217x-2-16
  title: ''
evidence_spans:
- Validation of the ReDU sample information template using the drag-and-drop validator
- ReDU only interacts with MassIVE
- data uploaded to MassIVE as a public dataset
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_redu_cq
    doi: 10.1038/s41592-020-0916-7
    title: ReDU
  dedup_kept_from: coll_redu_cq
schema_version: 0.2.0
---

# multivariate-ordination-interpretation

## Summary

Compute unsupervised principal components analysis (PCA) on chemical annotation matrices derived from mass spectrometry data, then render and interactively explore the resulting ordination plots to identify sample relationships and chemical annotation patterns across a cohort.

## When to use

You have a collection of tandem MS/MS samples (stored in MassIVE) with GNPS spectral library annotations (m/z, retention time, compound identity), and you want to explore whether samples cluster by shared chemical features without predefined class labels. Use this skill when you need to reduce high-dimensional chemical annotation space to 2–3 principal components for visual pattern discovery and interactive sample navigation.

## When NOT to use

- Input is already reduced to <5 dimensions or lacks sufficient feature diversity (PCA adds minimal interpretive value).
- Samples have strong a priori class structure that requires supervised methods (e.g., Linear Discriminant Analysis or Partial Least Squares-DA) for classification accuracy rather than exploratory ordination.
- Chemical annotation data are predominantly missing or below a minimum detection threshold across most samples (feature matrix too sparse for robust covariance estimation).

## Inputs

- ReDU chemical annotation matrix (rows=files, columns=annotated features with m/z, retention time, GNPS identifiers)
- MassIVE dataset identifiers (e.g., MSV* accessions)
- Sample metadata table (e.g., organism, sample type, treatment)

## Outputs

- PCA score matrix (samples × principal components)
- PCA loading matrix (features × principal components)
- Emperor-compatible ordination plot (interactive 3D/2D visualization)
- Saved visualization state and exported raster/vector plot

## How to apply

First, query the ReDU database to retrieve chemical annotation matrices for your selected MassIVE files, with rows representing files and columns representing annotated features (m/z, retention time, GNPS compound annotations). Construct a feature-by-sample matrix, handling missing values by imputation or removal as appropriate for your dataset. Apply unsupervised PCA using scikit-learn or equivalent to compute principal component loadings and sample coordinates. Export PCA scores (sample coordinates along PC1, PC2, and other components) and loadings to a text-based format compatible with Emperor. Import the scores and sample metadata into Emperor and render an interactive 3D or 2D score plot with configurable coloring by sample attributes, point size, and dynamic axes selection. This approach allows pattern discovery without class labels and enables hypothesis generation about which chemical features drive separation along principal components.

## Related tools

- **ReDU** (Query and retrieve chemical annotation matrices for selected MassIVE files; provides the data source for PCA) — https://github.com/mwang87/ReDU-MS2-GNPS
- **GNPS** (Perform spectral library matching to generate chemical annotations (level 2/3 identifications) that populate the feature matrix) — https://github.com/CCMS-UCSD/GNPSDocumentation
- **MassIVE** (Public repository storing raw tandem MS data; ReDU bridges to MassIVE to access MS2 spectra and sample metadata)
- **Emperor** (Interactive visualization and exploration of PCA scores; supports 3D/2D ordination plots with configurable coloring, point size, and axes) — https://github.com/biocore/emperor
- **scikit-learn** (Compute unsupervised PCA decomposition (loadings and scores) from the chemical annotation feature matrix)

## Evaluation signals

- PCA explains ≥60–70% of total variance in the first 2–3 principal components (check scree plot); if <50%, features may be too noisy or uncorrelated.
- Score plot exhibits visually distinct clusters or gradients that align with known sample properties (organism, habitat, sample type) or reveal unexpected sample relationships.
- Loading plot shows that the top features (highest absolute loadings on PC1/PC2) are chemically or biologically sensible (e.g., expected metabolites for the sample source).
- Emperor renders without missing data artifacts; all samples and metadata are present in the interactive plot; color/size legends are interpretable.
- Repeat PCA with subsets of samples or features; dominant patterns should remain stable (robustness check against feature selection or sample composition artifacts).

## Limitations

- PCA assumes linear relationships among features; nonlinear manifold structures may be misrepresented in low-dimensional projections.
- Chemical annotations from spectral library matching are considered level 2 or 3 by the 2007 metabolomics standard initiative and may be ambiguous; the same chemical can have multiple GNPS annotations due to slight variation in MS2 spectra (m/z or abundance).
- Missing or imputed values in the annotation matrix can bias covariance estimation and loadings; users must document imputation strategy.
- Interactive exploration in Emperor is exploratory; observed clusters are not validated by statistical testing and may reflect technical batch effects or confounding variables rather than biological signal.
- Scaling of features (e.g., by variance or l2-norm) affects which features dominate principal components; choice must be justified based on whether you wish to weight rare or abundant metabolites equally.

## Evidence

- [other] PCA of selected ReDU files computes principal coordinate analysis values per sample and renders them via Emperor visualization, allowing users to explore chemical annotation patterns across a subset of public data.: "PCA of selected ReDU files computes principal coordinate analysis values per sample and renders them via Emperor visualization, allowing users to explore chemical annotation patterns across a subset"
- [other] Query the ReDU database to retrieve chemical annotation matrices for selected MassIVE files, with rows as files and columns as annotated chemical features (m/z, retention time, GNPS annotations).: "Query the ReDU database to retrieve chemical annotation matrices for selected MassIVE files, with rows as files and columns as annotated chemical features (m/z, retention time, GNPS annotations)"
- [other] Apply PCA using scikit-learn or equivalent to compute principal component loadings and score coordinates in an unsupervised manner (no class labels).: "Apply PCA using scikit-learn or equivalent to compute principal component loadings and score coordinates in an unsupervised manner (no class labels)"
- [other] Import the PCA scores and sample metadata into Emperor and render an interactive 3D or 2D score plot with configurable coloring, point size, and axes selection options.: "Import the PCA scores and sample metadata into Emperor and render an interactive 3D or 2D score plot with configurable coloring, point size, and axes selection options"
- [abstract] The results are plotted using Emperor which provides interactive plotting capabilities to explore the data via a PCA score plot: "The results are plotted using Emperor which provides interactive plotting capabilities to explore the data via a PCA score plot"
- [abstract] Chemical annotation is performed in GNPS by comparing MS2 spectra: "Chemical annotation is performed in GNPS by comparing MS2 spectra"
- [abstract] GNPS annotations via spectral reference matching are considered level 2 (putative annotation based on spectral library similarity) or level 3 (putatively characterized compound class based on: "GNPS annotations via spectral reference matching are considered level 2 (putative annotation based on spectral library similarity) or level 3 (putatively characterized compound class based on"
- [abstract] The same chemical can have multiple GNPS annotations. Slight variation in the MS2 spectra (*m/z* or abundance) cause the pattern to match different reference MS2 spectra for the same chemical: "The same chemical can have multiple GNPS annotations. Slight variation in the MS2 spectra (m/z or abundance) cause the pattern to match different reference MS2 spectra"
