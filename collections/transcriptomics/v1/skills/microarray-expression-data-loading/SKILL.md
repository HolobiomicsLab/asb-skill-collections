---
name: microarray-expression-data-loading
description: Use when you have raw or normalized microarray expression matrices stored in public repositories (GEO accessions) along with sample metadata, and you need to load both into R as structured objects (expression matrix and phenotype data frame) to construct a design matrix and fit linear models for.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3518
  - http://edamontology.org/topic_0089
  tools:
  - limma
  - R
  - GEOquery
derived_from:
- doi: 10.1186/gb-2014-15-2-r29
  title: limmavoom
- doi: 10.1093/nar/gkv007
  title: ''
evidence_spans:
- Limma is an R package for the analysis of gene expression data, especially the use of linear models for analysing designed experiments
- Limma is an R package for the analysis of gene expression data, especially the use of linear models for analysing designed experiments and the assessment of differential expression
- Limma is an R package for the analysis of gene expression data
- Limma is an R package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/transcriptomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_limmavoom
    doi: 10.1186/gb-2014-15-2-r29
    title: limmavoom
  dedup_kept_from: coll_limmavoom
schema_version: 0.2.0
---

# microarray-expression-data-loading

## Summary

Loading and structuring microarray expression data and associated phenotype metadata from public repositories (e.g., GEO) into R memory for downstream linear modeling and differential expression analysis. This is the essential first step before applying limma's lmFit function to designed experiments.

## When to use

You have raw or normalized microarray expression matrices stored in public repositories (GEO accessions) along with sample metadata, and you need to load both into R as structured objects (expression matrix and phenotype data frame) to construct a design matrix and fit linear models for differential expression.

## When NOT to use

- Expression data are already loaded and validated in memory as a structured object.
- Working with RNA-seq count matrices (which require different normalization strategies than microarray intensity data).
- Data are already in a pre-processed, batch-corrected feature table from a prior analysis pipeline.

## Inputs

- GEO accession identifier (string)
- Public microarray dataset URL or local file path
- Phenotype/sample metadata table (CSV, TSV, or embedded in GEO record)

## Outputs

- Expression matrix (numeric matrix or ExpressionSet object; genes/probes × samples)
- Phenotype data frame (samples × experimental covariates)
- Combined eSet or MicroarrayExpressionSet object

## How to apply

Retrieve microarray expression data and phenotype metadata from a public GEO accession using appropriate R data-loading functions (e.g., GEOquery::getGEO or similar repository interfaces). Parse the expression matrix so that rows represent gene probes and columns represent sample replicates, and load the phenotype metadata as a data frame with rows matching sample order. Verify that sample identifiers in the expression matrix column names correspond exactly to row names in the phenotype data frame. This ensures that the design matrix constructed in the next step correctly maps experimental conditions to expression measurements.

## Related tools

- **limma** (Primary R package for fitting linear models to microarray expression after data loading; receives the loaded expression matrix and design matrix.) — https://github.com/bioc/limma
- **GEOquery** (R package for retrieving microarray and metadata directly from GEO accessions.)
- **R** (Programming environment for executing data loading, validation, and downstream analysis.)

## Evaluation signals

- Expression matrix dimensions match expected probe count and sample count; no missing values in critical rows/columns.
- Sample identifiers in expression matrix column names match exactly (by name and order) with row names in phenotype data frame.
- Expression values fall within expected intensity range for the microarray platform (e.g., log2 scale, 0–16 for Affymetrix; 0–65535 for two-color arrays).
- Phenotype data frame includes all required experimental grouping variables (e.g., treatment, control status) without NAs in key columns.
- No sample replicates are duplicated or missing; metadata row count equals expression matrix column count.

## Limitations

- GEO records may contain incomplete or ambiguous phenotype metadata; manual curation or cross-reference with the original publication may be required.
- Microarray platforms vary widely (Affymetrix, Illumina, two-color cDNA, etc.); platform-specific probe mapping and intensity normalization strategies must be applied before or immediately after loading.
- Public repositories may enforce access restrictions or rate limits on bulk downloads; script timeouts or authentication may be necessary.
- Batch effects introduced during sample collection, array manufacturing, or data acquisition are not resolved by loading alone; post-loading normalization and batch correction (limma::removeBatchEffect or similar) are typically required before statistical modeling.

## Evidence

- [other] Load microarray expression data and phenotype metadata from a public GEO accession using appropriate R data-loading functions.: "Load microarray expression data and phenotype metadata from a public GEO accession using appropriate R data-loading functions."
- [other] Limma is an R package for the analysis of gene expression data, especially the use of linear models for analysing designed experiments: "Limma is an R package for the analysis of gene expression data, especially the use of linear models for analysing designed experiments"
- [other] The linear model and differential expression functions apply to a wide variety of gene expression technologies including microarrays: "The linear model and differential expression functions apply to a wide variety of gene expression technologies including microarrays"
