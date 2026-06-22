---
name: multiassayexperiment-object-manipulation
description: Use when when you have parsed metabolite measurements into a table (rows = metabolites, columns = samples) and have corresponding sample-level covariates (e.g., disease status, treatment group) and/or feature-level annotations (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - MetaboDiff
  - MultiAssayExperiment
  - SMPDB (Small Molecular Pathway Database)
derived_from:
- doi: 10.1093/bioinformatics/bty344
  title: MetaboDiff
- doi: 10.1158/0008-5472.can-14-1490
  title: ''
evidence_spans:
- The `MetaboDiff` R package requires R version 4.0.2 or higher.
- The `MetaboDiff` R package requires R version 4.0.2 or higher
- '`MetaboDiff` is available for all operating systems and can be installed via Github'
- met = knn_impute(met,cutoff=0.4)
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
---

# MultiAssayExperiment Object Manipulation

## Summary

Construction and management of MultiAssayExperiment objects that integrate assay matrices, sample metadata, and feature annotations into a unified data structure for downstream metabolomic analysis. This skill enables seamless coordination of heterogeneous data layers required for differential metabolomic workflows.

## When to use

When you have parsed metabolite measurements into a table (rows = metabolites, columns = samples) and have corresponding sample-level covariates (e.g., disease status, treatment group) and/or feature-level annotations (e.g., metabolite IDs, HMDB identifiers, pathway membership), and you need to perform integrated analysis (imputation, normalization, clustering, correlation network construction) that must track sample traits alongside metabolite data. This skill is essential before applying MetaboDiff workflow functions that expect a unified object.

## When NOT to use

- Input assay matrix already embedded in an existing MultiAssayExperiment or SummarizedExperiment object — use direct slot access or subset operations instead.
- Sample metadata and feature annotations are missing or cannot be reliably aligned to assay dimensions — postpone object creation until data QC and alignment are complete.
- Assay dimensions are inconsistent (e.g., colnames of assay matrix do not match rownames of colData) — validate and reconcile before calling `create_mae()`.

## Inputs

- Numeric matrix or data.frame: metabolite measurements (rows = metabolites, columns = samples)
- Data frame: rowData with feature annotations (e.g., metabolite IDs, names, identifiers)
- Data frame: colData with sample metadata (e.g., sample names, disease status, batch)
- Optional: Column indices for KEGG, HMDB, ChEBI identifiers to retrieve SMPDB annotations

## Outputs

- MultiAssayExperiment object with integrated assay, rowData, and colData slots
- Annotated MultiAssayExperiment with metabolite pathway/database identifiers (if SMPDB enrichment applied)

## How to apply

Use the MetaboDiff `create_mae()` function to merge three components: (1) a numeric assay matrix with metabolite measurements, (2) a data frame of rowData (feature annotations keyed to metabolite IDs), and (3) a data frame of colData (sample metadata keyed to sample identifiers). The function encapsulates these into a MultiAssayExperiment object that preserves row and column names and enables downstream functions to retrieve the correct assay, annotation, and phenotype layers by name. After object creation, optionally enrich rowData with external metabolite annotations via `get_SMPDBanno()` by providing column indices for KEGG, HMDB, or ChEBI identifiers. The resulting MAE object serves as the standard input for all subsequent MetaboDiff operations (imputation, normalization, visualization, statistical testing).

## Related tools

- **MetaboDiff** (Provides create_mae() function to construct and manipulate MultiAssayExperiment objects, and get_SMPDBanno() to enrich rowData with metabolite annotations) — https://github.com/andreasmock/MetaboDiff
- **MultiAssayExperiment** (Core Bioconductor package that defines the MAE class and methods for coordinated manipulation of assay, rowData, and colData layers)
- **SMPDB (Small Molecular Pathway Database)** (External database queried by get_SMPDBanno() to retrieve metabolite pathway and annotation metadata)

## Examples

```
met <- create_mae(assay_matrix, rowData=feature_annotations, colData=sample_metadata); met <- get_SMPDBanno(met, column_kegg_id=6, column_hmdb_id=7, column_chebi_id=NA)
```

## Evaluation signals

- Verify that the returned MAE object has non-null assay(), rowData(), and colData() slots with correct dimensions: nrow(rowData) == nrow(assay), ncol(assay) == nrow(colData).
- Check that rownames(assay) match rownames(rowData) and colnames(assay) match rownames(colData), confirming correct alignment.
- If SMPDB annotation was applied, confirm that rowData now contains columns for KEGG, HMDB, ChEBI identifiers (or the columns specified in the get_SMPDBanno() call).
- Verify that all downstream MetaboDiff functions (knn_impute, normalize_met, pca_plot, etc.) accept the MAE object without error and return modified MAE objects with same structure.
- Spot-check a subset of sample and metabolite identifiers in the MAE object against the original input tables to confirm no reordering or subsetting occurred unintentionally.

## Limitations

- MultiAssayExperiment object construction requires exact alignment of row and column names between assay matrix and metadata data frames; mismatched or missing identifiers will cause create_mae() to fail or produce a malformed object.
- SMPDB annotation enrichment (get_SMPDBanno) requires that metabolite identifiers (KEGG, HMDB, ChEBI) are already present in rowData; identifiers not found in SMPDB will result in NA values in the enriched columns.
- The MAE object does not automatically validate or correct for missing values, batch effects, or outliers in the assay matrix; these must be addressed by subsequent filtering and normalization steps.

## Evidence

- [methods] The function `create_mae` merges all objects into a so called `MultiAssayExperiment` object to simplify all downstream analysis.: "The function `create_mae` merges all objects into a so called `MultiAssayExperiment` object to simplify all downstream analysis."
- [methods] Metabolite annotation can be retrieved from the Small Molecular Pathway Database (SMPDB) if HMDB, KEGG or ChEBI ids are part of the rowData object: "Metabolite annotation can be retrieved from the Small Molecular Pathway Database (SMPDB) if HMDB, KEGG or ChEBI ids are part of the rowData object"
- [readme] The MetaboDiff packages aims to provide a low-level entry to differential metabolomic analysis with R by starting off with the table of metabolite measurements.: "The MetaboDiff packages aims to provide a low-level entry to differential metabolomic analysis with R by starting off with the table of metabolite measurements."
- [methods] met <- get_SMPDBanno(met, column_kegg_id=6, column_hmdb_id=7, column_chebi_id=NA): "met <- get_SMPDBanno(met, column_kegg_id=6, column_hmdb_id=7, column_chebi_id=NA)"
