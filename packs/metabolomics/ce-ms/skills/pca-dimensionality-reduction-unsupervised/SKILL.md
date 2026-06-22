---
name: pca-dimensionality-reduction-unsupervised
description: Use when you have a feature-by-sample matrix (rows = annotated chemical features such as m/z, retention time, GNPS spectral library matches;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3935
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
  tools:
  - ReDU
  - MassIVE
  - scikit-learn
  - Emperor
  - GNPS
  techniques:
  - CE-MS
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41592-020-0916-7
  all_source_dois:
  - 10.1038/s41592-020-0916-7
  - 10.1186/2047-217x-2-16
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# pca-dimensionality-reduction-unsupervised

## Summary

Unsupervised principal components analysis (PCA) of chemical annotation matrices from mass spectrometry data to compute principal coordinate scores and loadings, enabling low-dimensional visualization and interactive exploration of sample relationships without class labels. This skill is applied to metabolomics and natural products datasets where chemical feature patterns across samples must be discovered and visualized.

## When to use

Use this skill when you have a feature-by-sample matrix (rows = annotated chemical features such as m/z, retention time, GNPS spectral library matches; columns = mass spectrometry sample files) and need to explore and visualize high-dimensional chemical annotation patterns across a public or cohort dataset without predefined sample groupings. Typical triggers: (1) you have retrieved chemical annotation matrices for a selected subset of MassIVE files via ReDU; (2) you seek to discover latent patterns or clusters in sample chemical profiles; (3) you want to render an interactive 3D or 2D projection for hypothesis generation or outlier detection.

## When NOT to use

- Input matrix is already a low-dimensional representation (e.g. pre-computed PCA scores, t-SNE embedding, or UMAP projection).
- Feature matrix contains fewer samples than features and is severely rank-deficient; consider feature selection or regularized PCA first.
- Data contains strong batch effects or technical confounders that have not been corrected; perform batch normalization or removal before PCA to avoid artifactual dominant principal components.

## Inputs

- Feature-by-sample matrix of chemical annotations (rows = MassIVE files, columns = annotated m/z, retention time, GNPS spectral library matches)
- Sample metadata table (file identifiers, organism, sample type, collection attributes)
- Specification of handling strategy for missing annotation values (imputation method or removal threshold)

## Outputs

- PCA score matrix (sample coordinates along principal components PC1, PC2, PC3, …)
- PCA loadings matrix (feature contributions to each principal component)
- Interactive Emperor 3D/2D score plot (HTML or interactive object with configurable metadata coloring)
- Variance explained per principal component (scree plot data)

## How to apply

Construct a feature-by-sample matrix from chemical annotations (m/z, retention time, GNPS annotations as columns; individual MassIVE files as rows), handling missing values by imputation or removal according to the sparsity of your annotation dataset. Apply PCA using scikit-learn or an equivalent linear algebra library to compute principal component loadings and sample score coordinates in an unsupervised manner (no class labels or supervised constraints). Export the PCA scores (sample coordinates along PC1, PC2, and other components) and loadings to a text-based matrix format (e.g. tab-separated or comma-separated) compatible with Emperor. Import the PCA score matrix and associated sample metadata (organism, sample type, collection location, etc.) into Emperor via its Python API or web interface, then render an interactive 3D or 2D score plot with configurable coloring by metadata attributes, point size, and axes selection. Verify that variance explained by the leading principal components is sufficient (typically >70% in PC1+PC2+PC3 for metabolomics data) to justify the dimensionality reduction.

## Related tools

- **scikit-learn** (Computes unsupervised PCA decomposition (principal component loadings and sample scores from the feature matrix))
- **Emperor** (Imports PCA scores and metadata; renders interactive 3D/2D score plots with configurable coloring, point size, and axes selection for exploratory visualization of sample relationships) — https://github.com/biocore/emperor
- **ReDU** (Retrieves and aggregates chemical annotation matrices (from GNPS spectral library matching) for selected MassIVE files to populate the input feature-by-sample matrix) — https://github.com/mwang87/ReDU-MS2-GNPS
- **GNPS** (Performs spectral library matching and generates chemical annotations (m/z, retention time, reference matches) that populate the feature matrix) — https://github.com/CCMS-UCSD/GNPSDocumentation
- **MassIVE** (Public repository of mass spectrometry data files; serves as the data source from which ReDU retrieves chemical annotation matrices)

## Evaluation signals

- PCA scores and loadings matrices are exported in Emperor-compatible text format (tab-separated or comma-separated values with row and column labels).
- Interactive Emperor score plot renders without errors and displays sample points color-coded by at least one metadata attribute (e.g. organism, sample type).
- Variance explained by leading principal components (PC1 + PC2 + PC3) is ≥50%; if <50%, investigate whether feature preprocessing or scaling was adequate.
- PCA loadings show interpretable chemical features (m/z values, retention times, or GNPS match names) with non-zero contributions to PC1 and PC2; high-magnitude loadings should correspond to known or hypothesized discriminant chemical markers.
- Sample clusters or gradients visible in the score plot are concordant with known biological or sample collection metadata (e.g. samples from the same organism or environment cluster together).

## Limitations

- PCA assumes linear relationships among chemical features; non-linear manifold structures may not be captured and could require nonlinear methods (t-SNE, UMAP) as a complementary approach.
- The same chemical compound may have multiple GNPS spectral library matches due to slight variation in MS/MS spectra (m/z or abundance differences), leading to duplicate or redundant features in the annotation matrix; consider collapsing or deduplicating annotations by compound name before PCA.
- GNPS spectral library matching produces level 2 (putative annotation based on spectral library similarity) or level 3 (putatively characterized compound class) confidence annotations; identity may not be definitively confirmed, limiting biological interpretation of PCA loadings.
- Missing values in the annotation matrix (sparse features not detected in all samples) must be handled explicitly (imputation or removal); the choice of strategy can influence PCA results and should be justified or validated by sensitivity analysis.
- PCA is sensitive to feature scaling; standardization (z-score normalization) is recommended if features span different units or magnitudes (e.g. m/z vs. abundance vs. retention time).

## Evidence

- [other] PCA of selected ReDU files computes principal coordinate analysis values per sample and renders them via Emperor visualization, allowing users to explore chemical annotation patterns across a subset of public data.: "PCA of selected ReDU files computes principal coordinate analysis values per sample and renders them via Emperor visualization, allowing users to explore chemical annotation patterns across a subset"
- [other] Query the ReDU database to retrieve chemical annotation matrices for selected MassIVE files, with rows as files and columns as annotated chemical features (m/z, retention time, GNPS annotations). Construct a feature-by-sample matrix from the annotation data, handling missing values by imputation or removal.: "Query the ReDU database to retrieve chemical annotation matrices for selected MassIVE files, with rows as files and columns as annotated chemical features (m/z, retention time, GNPS annotations)."
- [other] Apply PCA using scikit-learn or equivalent to compute principal component loadings and score coordinates in an unsupervised manner (no class labels).: "Apply PCA using scikit-learn or equivalent to compute principal component loadings and score coordinates in an unsupervised manner (no class labels)."
- [other] Export PCA scores (sample coordinates along PC1, PC2, and other components) and loadings to a text-based format compatible with Emperor. Import the PCA scores and sample metadata into Emperor and render an interactive 3D or 2D score plot with configurable coloring, point size, and axes selection options.: "Export PCA scores (sample coordinates along PC1, PC2, and other components) and loadings to a text-based format compatible with Emperor. Import the PCA scores and sample metadata into Emperor and"
- [abstract] The results are plotted using Emperor which provides interactive plotting capabilities to explore the data via a PCA score plot: "The results are plotted using Emperor which provides interactive plotting capabilities to explore the data via a PCA score plot"
- [abstract] The same chemical can have multiple GNPS annotations. Slight variation in the MS2 spectra (*m/z* or abundance) cause the pattern to match different reference MS2 spectra for the same chemical: "The same chemical can have multiple GNPS annotations. Slight variation in the MS2 spectra (*m/z* or abundance) cause the pattern to match different reference MS2 spectra for the same chemical"
- [readme] Emperor is a next-generation tool for the analysis and visualization of large microbial ecology datasets. Amongst its many features, Emperor provides a modern user interface that can be rapidly adjusted to your data analysis workflow.: "Emperor is a next-generation tool for the analysis and visualization of large microbial ecology datasets. Amongst its many features, Emperor provides a modern user interface that can be rapidly"
