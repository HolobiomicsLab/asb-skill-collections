---
name: interactive-spectral-visualization-emperor
description: Use when when you have computed PCA coordinates from chemical annotation matrices (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - ReDU
  - Emperor
  - MassIVE
  - GNPS
  - scikit-learn
derived_from:
- doi: 10.1038/s41592-020-0916-7
  title: ReDU
- doi: 10.1186/2047-217x-2-16
  title: ''
evidence_spans:
- Validation of the ReDU sample information template using the drag-and-drop validator
- ReDU only interacts with MassIVE
- How do I find out more about the plotting options in Emperor?
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

# interactive-spectral-visualization-emperor

## Summary

Emperor is an interactive 3D/2D visualization tool for exploring high-dimensional spectral and chemical annotation data from mass spectrometry repositories. It enables researchers to dynamically explore sample relationships and chemical patterns through configurable PCA score plots with metadata-driven coloring and filtering.

## When to use

When you have computed PCA coordinates from chemical annotation matrices (e.g., from GNPS-annotated ReDU files with m/z, retention time, and spectral library matches) and need to interactively explore sample clustering, chemical annotation patterns, and relationships across a public mass spectrometry dataset without predefined class labels.

## When NOT to use

- Input is already a low-dimensional representation (≤2 dimensions) with no additional structure to explore interactively.
- Sample metadata is missing or sparse; Emperor's coloring and filtering capabilities require sufficient attribute coverage for meaningful exploration.
- Data is univariate or contains only a single chemical feature; Emperor is designed for high-dimensional multivariate data exploration.

## Inputs

- PCA principal component scores (sample coordinates along PC1, PC2, PC3, etc.) as text-delimited file
- PCA loadings (feature weights across principal components)
- Sample metadata mapping (MassIVE file IDs or sample identifiers to categorical/continuous attributes)
- Chemical annotation feature matrix (rows=MassIVE files, columns=annotated m/z, retention time, GNPS spectral matches)

## Outputs

- Interactive 3D or 2D PCA score plot (Emperor visualization state)
- Rendered plot image or interactive HTML/web artifact with configurable coloring and axes
- Saved visualization state (Emperor format) for reproducibility and sharing

## How to apply

After computing PCA scores and loadings from a feature-by-sample chemical annotation matrix using scikit-learn or equivalent unsupervised method, export the principal coordinate values (PC1, PC2, and other components) and associated sample metadata to a text-based format compatible with Emperor. Import the PCA scores and sample information (including attributes like organism, sample type, environment) into Emperor, then render the data as an interactive 3D or 2D score plot. Dynamically adjust visualization parameters—point size, color mapping by categorical or continuous metadata attributes, and axis selection—to identify sample clusters and outliers. The visualization preserves the full coordinate system, allowing users to rotate, zoom, and explore relationships interactively before exporting the final rendered plot or visualization state.

## Related tools

- **Emperor** (Interactive visualization engine; renders PCA score plots in 3D/2D with dynamic metadata-driven coloring, point size adjustment, and axis selection) — https://github.com/biocore/emperor
- **ReDU** (Chemical annotation database and file selector; provides curated spectral library matches (m/z, retention time, GNPS annotations) for selected MassIVE files as input to PCA) — https://github.com/mwang87/ReDU-MS2-GNPS
- **GNPS** (Spectral library matching platform; generates chemical annotations (level 2/3 by MSI standards) for mass spectra that populate the feature matrix for PCA) — https://github.com/CCMS-UCSD/GNPSDocumentation
- **MassIVE** (Public mass spectrometry data repository; source of raw and processed tandem MS files and their metadata (organism, sample type, environment) used in visualization)
- **scikit-learn** (Principal component analysis computation; computes PCA loadings and score coordinates in unsupervised manner before visualization)

## Evaluation signals

- PCA score plot renders without errors and all samples appear as distinct points in 3D or 2D coordinate space.
- Metadata-driven coloring is applied correctly: categorical attributes produce discrete color groups; continuous attributes produce smooth color gradients across the plot.
- Interactive controls (rotation, zoom, axis selection, point size adjustment) respond dynamically without lag or visualization artifacts.
- Exported visualization state can be re-imported into Emperor and reproduces the same coordinate layout and coloring scheme.
- Sample clustering patterns in the score plot reflect known biological or chemical groupings in the metadata (e.g., samples from same organism cluster together; samples with similar GNPS annotations co-locate).

## Limitations

- Emperor visualization quality depends on PCA convergence and the underlying feature matrix quality; sparse annotation matrices or poor imputation of missing values reduce interpretability.
- The same chemical can have multiple GNPS annotations due to slight MS2 spectral variation, potentially inflating the number of features and complicating PCA interpretation.
- GNPS annotations are level 2 or level 3 by the 2007 metabolomics standards initiative (putative annotation based on spectral library similarity or compound class), not confirmed identifications; visualization patterns should not be interpreted as definitive chemical characterization.
- Interactive 3D rendering performance may degrade with very large sample counts (>10,000 samples); 2D projections or data subsetting may be necessary.
- Visualization does not inherently identify statistically significant clusters or perform hypothesis testing; user must apply complementary multivariate statistics (PERMANOVA, post-hoc tests) to validate observed patterns.

## Evidence

- [other] PCA of selected ReDU files computes principal coordinate analysis values per sample and renders them via Emperor visualization, allowing users to explore chemical annotation patterns across a subset of public data.: "PCA of selected ReDU files computes principal coordinate analysis values per sample and renders them via Emperor visualization, allowing users to explore chemical annotation patterns across a subset"
- [other] Export PCA scores (sample coordinates along PC1, PC2, and other components) and loadings to a text-based format compatible with Emperor.: "Export PCA scores (sample coordinates along PC1, PC2, and other components) and loadings to a text-based format compatible with Emperor."
- [other] Import the PCA scores and sample metadata into Emperor and render an interactive 3D or 2D score plot with configurable coloring, point size, and axes selection options.: "Import the PCA scores and sample metadata into Emperor and render an interactive 3D or 2D score plot with configurable coloring, point size, and axes selection options."
- [abstract] The results are plotted using Emperor which provides interactive plotting capabilities to explore the data via a PCA score plot: "The results are plotted using Emperor which provides interactive plotting capabilities to explore the data via a PCA score plot"
- [readme] Emperor is a next-generation tool for the analysis and visualization of large microbial ecology datasets. Amongst its many features, Emperor provides a modern user interface that can be rapidly adjusted to your data analysis workflow.: "Emperor is a next-generation tool for the analysis and visualization of large microbial ecology datasets. Amongst its many features, Emperor provides a modern user interface that can be rapidly"
- [abstract] The same chemical can have multiple GNPS annotations. Slight variation in the MS2 spectra (*m/z* or abundance) cause the pattern to match different reference MS2 spectra for the same chemical: "Slight variation in the MS2 spectra cause the pattern to match different reference MS2 spectra for the same chemical"
- [abstract] GNPS annotations via spectral reference matching are considered level 2 (putative annotation based on spectral library similarity) or level 3 (putatively characterized compound class based on: "GNPS annotations via spectral reference matching are considered level 2 (putative annotation based on spectral library similarity)"
