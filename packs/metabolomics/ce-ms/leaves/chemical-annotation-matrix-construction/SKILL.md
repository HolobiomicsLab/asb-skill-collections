---
name: chemical-annotation-matrix-construction
description: Use when you have selected a subset of public tandem MS files from ReDU/MassIVE that have been processed through GNPS spectral library matching, and you need to organize their chemical annotations into a matrix (rows = files, columns = annotated features) before performing PCA or other multivariate.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - ReDU
  - MassIVE
  - GNPS
  - scikit-learn
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chemical-annotation-matrix-construction

## Summary

Construct a feature-by-sample matrix from GNPS chemical annotations (m/z, retention time, spectral library matches) retrieved from a subset of ReDU/MassIVE files, handling missing values by imputation or removal to prepare data for unsupervised dimensionality reduction and visualization.

## When to use

You have selected a subset of public tandem MS files from ReDU/MassIVE that have been processed through GNPS spectral library matching, and you need to organize their chemical annotations into a matrix (rows = files, columns = annotated features) before performing PCA or other multivariate analysis to explore sample relationships and chemical annotation patterns across the cohort.

## When NOT to use

- Input files have not been processed through GNPS spectral library matching (raw MS2 spectra only, no annotations).
- Only unannotated m/z features are available (use raw feature tables from mass spectrometry preprocessing instead).
- You need to include multiple levels of annotation confidence (e.g., level 2 and level 3 GNPS annotations separately); this skill merges all available annotations without stratifying by confidence.

## Inputs

- Selected MassIVE file identifiers (MSV IDs)
- GNPS spectral library search results with compound identifications
- ReDU chemical annotation database query (per-file feature lists with m/z, RT, annotation ID)

## Outputs

- Feature-by-sample matrix (tab-separated text file or CSV: rows = files, columns = annotated chemical features)
- Metadata file mapping file identifiers to MassIVE IDs and sample attributes
- Matrix statistics (feature count, file count, sparsity, missing value report)

## How to apply

Query the ReDU database to retrieve GNPS chemical annotation results (spectral library matches with m/z, retention time, and compound identities) for each selected MassIVE file. Organize the annotations into a matrix where rows represent individual files and columns represent unique annotated chemical features. Handle missing values—where a file lacks an annotation for a feature—by either removing features below a frequency threshold or imputing with zero abundance. Validate matrix dimensions and consistency (e.g., no negative values, correct data types). The resulting matrix is then compatible with scikit-learn PCA and Emperor visualization import, enabling unsupervised exploration of chemical annotation structure across samples.

## Related tools

- **ReDU** (Query and retrieve GNPS-annotated chemical features from public MassIVE files for selected cohort) — https://github.com/mwang87/ReDU-MS2-GNPS
- **GNPS** (Perform spectral library matching to generate chemical annotations (m/z, retention time, compound identities) for each file's MS2 spectra) — https://github.com/CCMS-UCSD/GNPSDocumentation
- **MassIVE** (Public repository storing raw and processed tandem MS data files that serve as input to ReDU and GNPS)
- **scikit-learn** (Apply PCA to the constructed feature-by-sample matrix to compute principal component loadings and scores)

## Evaluation signals

- Matrix dimensions (rows = number of selected files, columns = number of unique annotated features) are consistent with input file count and annotation inventory.
- No negative or invalid values in the matrix; all entries are non-negative abundances or presence/absence flags.
- Sparsity metric (percentage of zero/missing entries) is documented and reasonable for the annotation scope.
- Metadata file row count matches matrix row count; all file identifiers are traceable to MassIVE IDs.
- Matrix imports successfully into scikit-learn and Emperor without format errors; PCA computes and produces valid PC scores.

## Limitations

- GNPS annotations are level 2 or 3 by the 2007 metabolomics standard initiative (putative or putatively characterized, not confirmed identifications), limiting biological interpretability.
- The same chemical may have multiple GNPS annotations due to slight variation in MS2 spectra (m/z or abundance differences), leading to feature duplication; deduplication strategy must be specified.
- Missing annotations for a file–feature pair can introduce bias if imputation method is not documented or if removal threshold is too aggressive (loss of rare features).
- Matrix construction does not account for batch effects, instrumental drift, or sample heterogeneity across files from different laboratories or collection dates.

## Evidence

- [methods] Query the ReDU database to retrieve chemical annotation matrices for selected MassIVE files, with rows as files and columns as annotated chemical features (m/z, retention time, GNPS annotations).: "Query the ReDU database to retrieve chemical annotation matrices for selected MassIVE files, with rows as files and columns as annotated chemical features (m/z, retention time, GNPS annotations)."
- [methods] Construct a feature-by-sample matrix from the annotation data, handling missing values by imputation or removal.: "Construct a feature-by-sample matrix from the annotation data, handling missing values by imputation or removal."
- [abstract] The same chemical can have multiple GNPS annotations. Slight variation in the MS2 spectra (*m/z* or abundance) cause the pattern to match different reference MS2 spectra for the same chemical: "The same chemical can have multiple GNPS annotations. Slight variation in the MS2 spectra cause patterns to match different reference spectra"
- [abstract] GNPS annotations via spectral reference matching are considered level 2 (putative annotation based on spectral library similarity) or level 3 (putatively characterized compound class): "GNPS annotations via spectral reference matching are considered level 2 (putative annotation based on spectral library similarity) or level 3"
- [readme] Download batch template for GNPS at ```https://redu.ucsd.edu/metabatchdump``` Run Batch Workflow for Spectral Library Search: "Download batch template for GNPS at https://redu.ucsd.edu/metabatchdump Run Batch Workflow for Spectral Library Search"
