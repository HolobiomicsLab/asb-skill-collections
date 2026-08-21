---
name: multiassay-data-structure-construction
description: 'Use when you have three separate data components from a metabolomics
  assay: (1) a matrix of metabolite measurements (assay) with samples as columns and
  metabolites as rows, (2) a table of metabolite annotations (rowData, e.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3906
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - MetaboDiff
  - R
  - MultiAssayExperiment
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1093/bioinformatics/bty344
  title: MetaboDiff
- doi: 10.1158/0008-5472.can-14-1490
  title: ''
evidence_spans:
- '`MetaboDiff` is available for all operating systems and can be installed via Github'
- met = knn_impute(met,cutoff=0.4)
- The `MetaboDiff` R package requires R version 4.0.2 or higher.
- The `MetaboDiff` R package requires R version 4.0.2 or higher
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metabodiff_cq
    doi: 10.1093/bioinformatics/bty344
    title: MetaboDiff
  dedup_kept_from: coll_metabodiff_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/bty344
  all_source_dois:
  - 10.1093/bioinformatics/bty344
  - 10.1158/0008-5472.can-14-1490
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# MultiAssayExperiment Data Structure Construction

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Merge heterogeneous metabolomic assay data (metabolite measurements, metabolite annotations, and sample metadata) into a unified MultiAssayExperiment object to enable standardized downstream analysis in R. This skill is essential for preparing metabolite tables with associated metadata for quality control, normalization, and differential analysis workflows.

## When to use

You have three separate data components from a metabolomics assay: (1) a matrix of metabolite measurements (assay) with samples as columns and metabolites as rows, (2) a table of metabolite annotations (rowData, e.g., HMDB, KEGG, or ChEBI identifiers and pathway information), and (3) a table of sample-level metadata (colData, e.g., case/control status, batch information, patient identifiers). Use this skill before any quality control, imputation, or normalization step to unify these components into a single container that tracks relationships between assay measurements and their associated annotations.

## When NOT to use

- Data is already in a unified container (SummarizedExperiment, ExpressionSet, or existing MultiAssayExperiment) — use accessor functions directly instead.
- Assay measurements and metadata are from different organisms or non-aligned samples — verify row and column dimensions match before calling create_mae().
- Metabolite identifiers are missing or unmapped — while create_mae() will still construct the MAE, downstream annotation retrieval via get_SMPDBanno() will fail without valid KEGG/HMDB/ChEBI IDs in rowData.

## Inputs

- assay matrix: numeric matrix with metabolites in rows, samples in columns (e.g., from Metabolon or similar vendor)
- rowData table: data.frame or tibble with one row per metabolite, columns containing HMDB/KEGG/ChEBI identifiers and pathway annotations
- colData table: data.frame or tibble with one row per sample, columns containing group assignments (e.g., tumor/normal), batch, patient ID, or other sample-level covariates

## Outputs

- MultiAssayExperiment object: a unified container with assay data accessible via assay(), metabolite annotations via rowData(), and sample metadata via colData()

## How to apply

Load the MetaboDiff R package and call the `create_mae()` function, passing the assay matrix, rowData annotation table, and colData sample metadata as arguments. The assay should have metabolites in rows and samples in columns; rowData should have one row per metabolite with columns containing external identifiers (HMDB ID, KEGG ID, ChEBI ID) and functional annotations; colData should have one row per sample with columns for group membership (e.g., tumor_normal), batch, or other covariates. The function will merge all three objects into a single MultiAssayExperiment container, which standardizes access to measurements and metadata throughout the analysis pipeline. Verify successful construction by checking that the resulting MAE object has the correct dimensions (number of metabolites, number of samples) and that slot accessors (assay(), rowData(), colData()) retrieve the expected data structures.

## Related tools

- **MetaboDiff** (R package providing the create_mae() function to construct MultiAssayExperiment objects from metabolite assay, annotation, and metadata tables) — https://github.com/andreasmock/MetaboDiff
- **MultiAssayExperiment** (Bioconductor class that standardizes storage and access of assay measurements linked to feature annotations and sample metadata)
- **R** (Programming environment required to run MetaboDiff (version 4.0.2 or higher))

## Examples

```
met <- create_mae(assay, rowData, colData)
```

## Evaluation signals

- The resulting MAE object reports correct dimensions: nrow(mae) equals the number of metabolites, ncol(mae) equals the number of samples.
- assay(mae) returns the metabolite measurement matrix with metabolites in rows and samples in columns.
- rowData(mae) returns the metabolite annotation table with one row per metabolite and columns for HMDB/KEGG/ChEBI identifiers.
- colData(mae) returns the sample metadata table with one row per sample and columns for group assignments and covariates.
- Subsequent visualization functions (na_heatmap, pca_plot) correctly identify and display group_factor columns from colData without errors.

## Limitations

- create_mae() does not perform validation of row/column alignment — if assay rows do not correspond to rowData rows or assay columns do not correspond to colData rows, the MAE will be constructed but will cause errors in downstream operations.
- Metabolite identifiers (HMDB, KEGG, ChEBI) are not automatically validated or retrieved during MAE construction — missing or malformed IDs will not raise errors until get_SMPDBanno() is called.
- The function is a low-level merge operation and does not handle missing data, duplicated identifiers, or metadata inconsistencies — data cleaning should precede MAE construction.

## Evidence

- [methods] create_mae function merges assay, rowData, and colData: "The function `create_mae` merges all objects into a so called `MultiAssayExperiment` object to simplify all downstream analysis."
- [intro] MetaboDiff entry point uses MultiAssayExperiment object: "The MetaboDiff packages aims to provide a low-level entry to differential metabolomic analysis with R by starting off with the table of metabolite measurements."
- [methods] MultiAssayExperiment merges assay, rowData, colData: "Load the MetaboDiff package and the met_example dataset containing assay (metabolite measurements), rowData (metabolite annotations), and colData (sample metadata)."
- [methods] create_mae is a required preprocessing step: "Create a MultiAssayExperiment object by calling create_mae(assay, rowData, colData) to merge the three data components."
