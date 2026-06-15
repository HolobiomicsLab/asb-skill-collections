---
name: sample-metadata-preparation-and-assignment
description: Use when before constructing a DESeqDataSet from any count matrix (whether from tximport, HTSeq, featureCounts, or raw counts). You have sample identifiers (run IDs, file names, or row names) and must link them to condition labels (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0203
  tools:
  - tximport
  - DESeq2
  - Salmon
  - tximportData
  - readr
  - tximeta
derived_from:
- doi: 10.1186/s13059-014-0550-8
  title: deseq2
evidence_spans:
- txi <- tximport(files, type="salmon", tx2gene=tx2gene)
- The package DESeq2 provides methods to test for differential expression by use of negative binomial generalized linear models
- library("DESeq2") ddsTxi <- DESeqDataSetFromTximport(txi, colData = samples, design = ~ condition)
- files <- file.path(dir,"salmon", samples$run, "quant.sf.gz")
- library("tximportData") dir <- system.file("extdata", package="tximportData")
- library("readr") tx2gene <- read_csv(file.path(dir, "tx2gene.gencode.v27.csv"))
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/transcriptomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_deseq2
    doi: 10.1186/s13059-014-0550-8
    title: deseq2
  dedup_kept_from: coll_deseq2
schema_version: 0.2.0
---

# Sample Metadata Preparation and Assignment

## Summary

Construct a sample metadata table (colData) that maps sample identifiers to experimental conditions and covariates, then assign it as the column-level annotation for a DESeqDataSet. This is a prerequisite for differential expression testing, as DESeq2 uses metadata to define the design formula and contrast groups.

## When to use

Before constructing a DESeqDataSet from any count matrix (whether from tximport, HTSeq, featureCounts, or raw counts). You have sample identifiers (run IDs, file names, or row names) and must link them to condition labels (e.g., 'treated' vs 'untreated') and any batch or covariate information needed for the design formula.

## When NOT to use

- colData already exists and is correctly formatted — proceed directly to DESeqDataSet construction.
- Performing unsupervised analysis (e.g., clustering, PCA) on raw counts where condition is not yet known — metadata is not strictly required for exploratory analysis.
- Using an already-constructed DESeqDataSet from tximeta, which automatically includes full sample metadata — metadata assignment is already handled.

## Inputs

- Sample run/file identifiers (character vector or table)
- Condition labels per sample (character or factor)
- Optional batch/covariate annotations per sample (numeric or factor)

## Outputs

- colData object (DataFrame with sample row names and condition columns)
- DESeqDataSet with assigned column metadata

## How to apply

Create a data frame with sample identifiers as row names and experimental condition(s) as columns. Assign condition labels (e.g., 'A' and 'B', or 'treated' and 'untreated') explicitly to each sample; if performing differential expression, specify which level should be the reference by converting the condition column to a factor and setting factor levels with `factor(condition, levels=c('untreated','treated'))`. Include additional columns for batch, replicate ID, or other covariates that will appear in the design formula. Pass this metadata table to `DESeqDataSetFromMatrix()`, `DESeqDataSetFromTximport()`, or `DESeqDataSet()` via the `colData` parameter. Verify that row names in colData match column names in the count matrix and that all samples are represented.

## Related tools

- **DESeq2** (Accepts colData as input to DESeqDataSetFromMatrix(), DESeqDataSetFromTximport(), and DESeqDataSet() constructors; uses metadata to define design formula and specify contrasts) — https://github.com/thelovelab/DESeq2
- **tximport** (Produces a list that is paired with colData in DESeqDataSetFromTximport() to construct a DESeqDataSet)
- **tximeta** (Automatically generates a SummarizedExperiment with metadata; can be converted to DESeqDataSet using colData from the SE)

## Examples

```
samples <- data.frame(condition=c('A','B','A','B'), row.names=c('run1','run2','run3','run4')); samples$condition <- factor(samples$condition, levels=c('A','B')); dds <- DESeqDataSetFromTximport(txi, colData=samples, design=~condition)
```

## Evaluation signals

- colData row names match count matrix column names exactly (no reordering or misalignment).
- All rows in colData are represented (no missing samples); all columns in count matrix are represented in colData.
- Condition column is a factor with explicitly specified levels; reference level is listed first in `levels()` output.
- DESeqDataSet construction completes without error; `colData(dds)` returns the assigned metadata.
- Design formula (e.g., `~condition` or `~batch+condition`) uses column names that exist in colData; `model.matrix(design, colData)` produces a valid design matrix.

## Limitations

- Factor level ordering must be manually specified; the default alphabetical ordering may not reflect your intended reference level for contrast computation.
- Missing or mismatched sample identifiers between metadata and count matrix will cause silent column reordering or loss of data — always verify row/column alignment before DESeqDataSet construction.
- Complex experimental designs with many confounders or interactions require careful design formula specification; tximeta or external metadata curation tools may be preferable for large cohort studies.

## Evidence

- [other] Load the tximportData package and retrieve the sample metadata table, assigning condition labels (A and B) and setting run IDs as row names.: "retrieve the sample metadata table, assigning condition labels (A and B) and setting run IDs as row names"
- [other] Construct a DESeqDataSet from the tximport output using DESeqDataSetFromTximport(), specifying the sample metadata and design formula (~condition).: "DESeqDataSetFromTximport(txi, colData = samples, design = ~ condition)"
- [other] Set factor levels for reference comparison before DESeq analysis.: "dds$condition <- factor(dds$condition, levels = c("untreated","treated"))"
- [other] colData is passed to DESeqDataSet constructors; the design formula uses columns from colData.: "dds <- DESeqDataSetFromMatrix(countData = cts, colData = coldata, design= ~ batch + condition)"
