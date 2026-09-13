---
name: metabolite-feature-table-normalization
description: Use when you have selected a subset of ReDU public tandem MS files with
  GNPS chemical annotations (level 2 or 3 spectral library matches) and wish to explore
  sample relationships via principal component analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - ReDU
  - MassIVE
  - GNPS
  - scikit-learn
  - Emperor
  techniques:
  - CE-MS
  license_tier: restricted
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-feature-table-normalization

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Construct and normalize a feature-by-sample matrix from mass spectrometry chemical annotations (m/z, retention time, GNPS spectral library matches) to enable unsupervised dimensionality reduction and cross-sample comparison. This skill transforms sparse, multi-annotated MS/MS identifications into a dense analytical table suitable for PCA and interactive visualization.

## When to use

You have selected a subset of ReDU public tandem MS files with GNPS chemical annotations (level 2 or 3 spectral library matches) and wish to explore sample relationships via principal component analysis. Use this skill before PCA when raw annotation matrices contain missing values, duplicate annotations for the same chemical, or require feature aggregation across files.

## When NOT to use

- Input is already a processed feature table with normalized abundances or presence/absence encodings — skip normalization and proceed directly to PCA.
- Your goal is to perform supervised classification or targeted compound identification — normalization for dimensionality reduction is distinct from normalization for hypothesis testing or quantitative comparison.
- Sample metadata is incomplete or inconsistent across the selected file subset — validation and harmonization must precede feature table construction.

## Inputs

- ReDU database query results (chemical annotation matrices, rows = MassIVE files, columns = chemical features with m/z, retention time, GNPS spectral library identifiers)
- Sample metadata (associated with each MassIVE file ID)
- Raw MS/MS spectral data (for validation of annotation reproducibility)

## Outputs

- Normalized feature-by-sample matrix (text format: TSV or CSV)
- Feature metadata table (m/z, retention time, canonical GNPS annotation)
- Sample metadata table (linked to matrix rows)
- Summary statistics (feature sparsity, value distribution, transformation log)

## How to apply

Retrieve chemical annotation matrices for selected MassIVE files from the ReDU database, with rows as files and columns as annotated chemical features (m/z, retention time, GNPS spectral library identity). Handle missing values by imputation or removal to construct a complete feature-by-sample matrix. Account for the fact that the same chemical can have multiple GNPS annotations due to slight variation in MS2 spectra (m/z or abundance), either by merging duplicate annotations to a single canonical feature or by retaining all annotations and normalizing by annotation count. Apply standard feature normalization (e.g., log-transformation, abundance scaling) to reduce skewness and stabilize variance before PCA. Export the normalized matrix in a text-based format (e.g., comma- or tab-separated values) compatible with downstream PCA and Emperor visualization tools.

## Related tools

- **ReDU** (Query and retrieve chemical annotation matrices from public MassIVE tandem MS files; bridge between GNPS spectral library matches and raw MS data repository) — https://github.com/mwang87/ReDU-MS2-GNPS
- **GNPS** (Perform spectral library matching to generate level 2/3 chemical annotations (putative identifications) used to populate the feature matrix) — https://github.com/CCMS-UCSD/GNPSDocumentation
- **MassIVE** (Public mass spectrometry data repository; source of raw MS/MS files and their associated identifiers for ReDU queries)
- **scikit-learn** (Implement PCA and matrix transformations (imputation, scaling, log-transformation) on the normalized feature table)
- **Emperor** (Render and interactively explore the PCA score plot derived from the normalized feature matrix) — https://github.com/biocore/emperor

## Evaluation signals

- Feature matrix dimensions and sparsity match the query parameters (expected number of files and annotated chemicals); row and column counts are consistent with metadata.
- Missing value handling is documented: imputation method (e.g., zero-fill, mean) or removal thresholds are applied uniformly and recorded in a log.
- Duplicate GNPS annotations for the same chemical are reconciled or flagged; aggregation logic (e.g., sum, max, count) is transparent and reproducible.
- Normalized feature values fall within expected ranges after transformation (e.g., log-transformed abundances are non-negative; z-scores cluster around 0 with SD ≈ 1); no outliers or NaNs remain.
- PCA scores computed from the normalized matrix are stable (e.g., loadings and coordinates are reproducible under the same input subset) and visually interpretable in Emperor (3D/2D scatter plot renders without errors, sample clusters align with known sample attributes).

## Limitations

- The same chemical can have multiple GNPS annotations due to slight variation in MS2 spectra (m/z or abundance), complicating feature aggregation and introducing ambiguity in downstream analysis if not handled carefully.
- GNPS spectral library matches are level 2 or 3 identifications (putative annotations based on library similarity), not confirmed structure — normalization does not improve annotation certainty.
- Missing or incomplete sample metadata across the selected file subset may introduce bias or loss of information during feature-by-sample matrix construction.
- Normalization assumes that chemical abundance patterns are comparable across files; systematic technical variations (instrument platform, acquisition parameters, sample preparation) can violate this assumption and distort PCA.
- Large file subsets or highly complex annotation patterns may create computationally intensive matrices; performance and memory constraints may require further filtering or downsampling before PCA.

## Evidence

- [other] Query the ReDU database to retrieve chemical annotation matrices for selected MassIVE files, with rows as files and columns as annotated chemical features (m/z, retention time, GNPS annotations).: "Query the ReDU database to retrieve chemical annotation matrices for selected MassIVE files, with rows as files and columns as annotated chemical features (m/z, retention time, GNPS annotations)."
- [other] Construct a feature-by-sample matrix from the annotation data, handling missing values by imputation or removal.: "Construct a feature-by-sample matrix from the annotation data, handling missing values by imputation or removal."
- [abstract] The same chemical can have multiple GNPS annotations due to slight variation in MS2 spectra (*m/z* or abundance) cause the pattern to match different reference MS2 spectra for the same chemical: "The same chemical can have multiple GNPS annotations. Slight variation in the MS2 spectra (*m/z* or abundance) cause the pattern to match different reference MS2 spectra for the same chemical"
- [abstract] Chemical annotations originating from spectral library matching are considered level 2 or level 3 by the 2007 metabolomics standard initiative: "Chemical annotations originating from spectral library matching are considered level 2 or level 3 by the 2007 metabolomics standard initiative"
- [other] Apply PCA using scikit-learn or equivalent to compute principal component loadings and score coordinates in an unsupervised manner (no class labels).: "Apply PCA using scikit-learn or equivalent to compute principal component loadings and score coordinates in an unsupervised manner (no class labels)."
