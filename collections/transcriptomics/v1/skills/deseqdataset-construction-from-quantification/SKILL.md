---
name: deseqdataset-construction-from-quantification
description: Use when you have transcript-level quantification files (quant.sf, kallisto abundance.h5, or RSEM output) from one or more RNA-seq samples and need to construct a count matrix for differential expression analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3170
  tools:
  - tximport
  - DESeq2
  - Salmon
  - tximportData
  - readr
  - kallisto
  - RSEM
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

# DESeqDataSet Construction from Quantification

## Summary

Convert transcript-level quantification files (from Salmon, kallisto, or RSEM) into a DESeqDataSet object suitable for differential expression testing. This skill bridges quantification tools and DESeq2 by aggregating transcript abundance to gene level and wrapping the result in a metadata-aware R object.

## When to use

You have transcript-level quantification files (quant.sf, kallisto abundance.h5, or RSEM output) from one or more RNA-seq samples and need to construct a count matrix for differential expression analysis. Use this when you want un-normalized estimated gene-level counts paired with sample metadata and a statistical design formula.

## When NOT to use

- You already have a gene-level count matrix from HTSeq, featureCounts, or similar; use DESeqDataSetFromMatrix() instead.
- You have quantification data imported via tximeta (which produces a SummarizedExperiment); construct DESeqDataSet directly from the SummarizedExperiment with design formula.
- Your input files are alignment BAM files rather than quantification files; use featureCounts or HTSeq to produce counts first.

## Inputs

- transcript-level quantification files (Salmon quant.sf.gz, kallisto abundance.h5, or RSEM .genes.results)
- tx2gene mapping table (data frame with columns: transcript ID, gene ID)
- sample metadata table (data frame with sample names as row names, columns for condition/covariates)

## Outputs

- DESeqDataSet object with count matrix, sample metadata (colData), and design formula
- assay matrix containing un-normalized estimated gene-level counts

## How to apply

First, load quantification file paths and sample metadata (with condition labels and run identifiers), then construct or load a tx2gene mapping table linking transcript IDs to gene IDs. Pass quantification files and the mapping to tximport() with type='salmon' (or 'kallisto'/'rsem') to aggregate transcript abundance estimates to gene level, producing a list containing estimated counts, lengths, and offsets. Finally, construct a DESeqDataSet using DESeqDataSetFromTximport(), specifying the tximport list, sample metadata table (colData), and design formula (e.g., ~condition). Verify the result by examining the assay matrix to confirm values are un-normalized integer estimates without library-size scaling.

## Related tools

- **tximport** (Imports transcript abundance quantifications and aggregates to gene level using tx2gene mapping)
- **DESeq2** (Provides DESeqDataSetFromTximport() constructor and differential expression testing framework) — https://github.com/thelovelab/DESeq2
- **Salmon** (Upstream quantification tool producing transcript-level abundance estimates (quant.sf files))
- **kallisto** (Alternative upstream quantification tool producing transcript abundance estimates)
- **RSEM** (Alternative upstream quantification tool producing transcript abundance estimates)
- **tximportData** (Provides example Salmon quantification files and tx2gene mapping for tutorial workflows)

## Examples

```
txi <- tximport(files, type="salmon", tx2gene=tx2gene); ddsTxi <- DESeqDataSetFromTximport(txi, colData = samples, design = ~ condition)
```

## Evaluation signals

- The resulting DESeqDataSet contains a count assay with integer (or quasi-integer) values without library-size normalization or log transformation.
- Row names of the count matrix match gene IDs from the tx2gene mapping; dimensions are (genes × samples).
- colData(dds) contains all sample metadata columns and matches the order of quantification files.
- The design formula is correctly stored and includes condition or covariate variables present in colData.
- Calling assay(dds) reveals un-scaled estimated counts aggregated across all transcripts per gene.

## Limitations

- tximport produces estimated counts based on transcript-level abundance; these are not raw read counts and should not be treated as such downstream.
- The tx2gene mapping must be accurate and complete; missing or duplicate mappings will result in missing genes or gene aggregation errors.
- Design formula must reference columns in the sample metadata table; misnamed variables will cause construction or analysis to fail.
- Pre-filtering of low-count genes is recommended after DESeqDataSet construction to reduce memory use and improve statistical power, but is not performed automatically.

## Evidence

- [other] tximport ingests transcript-level quantification files and produces a list object that contains un-normalized counts aggregated to the gene level, which serves as input to DESeqDataSetFromTximport for constructing a DESeqDataSet.: "tximport ingests transcript-level quantification files and produces a list object that contains un-normalized counts aggregated to the gene level, which serves as input to DESeqDataSetFromTximport"
- [other] you could import the data with *tximport*, which produces a list, and then you can use `DESeqDataSetFromTximport()`: "you could import the data with *tximport*, which produces a list, and then you can use `DESeqDataSetFromTximport()`"
- [other] If you have performed transcript quantification (with *Salmon*, *kallisto*, *RSEM*, etc.) you could import the data with *tximport*: "If you have performed transcript quantification (with *Salmon*, *kallisto*, *RSEM*, etc.) you could import the data with *tximport*"
- [other] ddsTxi <- DESeqDataSetFromTximport(txi, colData = samples, design = ~ condition): "ddsTxi <- DESeqDataSetFromTximport(txi, colData = samples, design = ~ condition)"
- [other] txi <- tximport(files, type="salmon", tx2gene=tx2gene): "txi <- tximport(files, type="salmon", tx2gene=tx2gene)"
