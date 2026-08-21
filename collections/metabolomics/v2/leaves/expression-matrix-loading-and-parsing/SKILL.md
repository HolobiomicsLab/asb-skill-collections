---
name: expression-matrix-loading-and-parsing
description: Use when you have raw omics expression data in CSV format (rows=genes/features,
  columns=samples) and a separate group annotation file (sample IDs mapped to experimental
  groups or phenotypes), and you need to prepare them for heatmap or other omics visualizations
  in an R Shiny environment.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3761
  edam_topics:
  - http://edamontology.org/topic_0203
  - http://edamontology.org/topic_3673
  tools:
  - R Shiny
  license_tier: open
  provenance_tier: literature
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

# expression-matrix-loading-and-parsing

## Summary

Load and validate expression matrices (gene-by-sample count or intensity data) alongside group annotation metadata from CSV files, preparing them for downstream omics visualization. This skill ensures data structure compatibility and metadata alignment before rendering interactive visualizations.

## When to use

You have raw omics expression data in CSV format (rows=genes/features, columns=samples) and a separate group annotation file (sample IDs mapped to experimental groups or phenotypes), and you need to prepare them for heatmap or other omics visualizations in an R Shiny environment.

## When NOT to use

- Expression data is already in a processed feature table or data object (e.g., SummarizedExperiment, Seurat object); use data extraction instead.
- Group annotations are embedded as row/column names or attributes within the expression matrix; use metadata parsing directly.
- Input files are not CSV or are in a proprietary binary format (e.g., HDF5, Excel); use format conversion first.

## Inputs

- expression matrix CSV file (gene/feature × sample, numeric values)
- group annotation CSV file (sample IDs × group/phenotype labels)

## Outputs

- parsed and validated expression matrix (data frame or matrix object)
- parsed and validated group annotation metadata (data frame with sample-to-group mapping)
- aligned expression–annotation data structure ready for Shiny rendering

## How to apply

Load the expression matrix CSV (e.g., heatmap_test.csv) and group annotation CSV (e.g., group_info.csv) using R data I/O functions (read.csv or equivalent). Validate that the expression matrix has consistent numeric columns and that group annotation sample IDs match the expression matrix column names. Check for missing values, verify row and column counts, and ensure group labels are categorical and non-empty. Once validated, merge or align the group metadata with the expression matrix structure. Pass the validated, aligned data structures to the R Shiny rendering pipeline for visualization (e.g., clustering, color scaling, and annotation sidebar generation).

## Related tools

- **R Shiny** (Interactive web application framework for rendering validated expression matrix visualizations (heatmap, volcano plot, etc.) with real-time user interaction) — github.com/databio2022/GraphBio

## Evaluation signals

- Expression matrix dimensions match expected gene and sample counts; no row or column loss after parsing.
- Sample IDs in expression matrix column names are identical to sample IDs in group annotation file (100% match rate after validation).
- Group annotation labels are categorical, non-null, and assigned to every sample with no orphaned or duplicate entries.
- Numeric values in expression matrix are within expected range for the assay type (e.g., counts ≥ 0, log-normalized typically in range [−10, 10]).
- Heatmap rendering succeeds with row/column clustering and colored group sidebars generated correctly, confirming alignment of metadata.

## Limitations

- CSV parsing assumes standard formatting (comma-delimited, UTF-8 encoding); non-standard delimiters or encodings will fail silently or cause parsing errors.
- No built-in handling of missing or sparse data; NAs or empty cells may propagate through validation or cause clustering failures.
- Sample ID matching is case-sensitive and whitespace-sensitive; minor naming inconsistencies (e.g., 'Sample_1' vs 'Sample_1 ') will fail validation.
- Large expression matrices (>50,000 genes or >10,000 samples) may exceed memory or rendering performance constraints in R Shiny.
- Group annotations with very large numbers of groups or highly imbalanced group sizes may produce cluttered or visually uninformative annotations.

## Evidence

- [other] Load and validate inputs: "Load the expression matrix (heatmap_test.csv) and group annotation data (group_info.csv) using R data I/O functions."
- [other] Parse and validate structure: "Parse and validate the expression matrix structure and group labels for compatibility."
- [other] Input file formats: "The heatmap component consumes two CSV files: heatmap_test.csv (expression matrix) and group_info.csv (group annotations)"
- [readme] Example demo data: "heatmap_test.csv and group_info.csv for heatmap."
- [other] Integration with Shiny rendering: "Integrate group annotation metadata as heatmap annotations (e.g., colored sidebars or labels). Render the interactive heatmap within the R Shiny application interface."
