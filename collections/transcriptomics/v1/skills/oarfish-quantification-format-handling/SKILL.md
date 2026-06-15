---
name: oarfish-quantification-format-handling
description: Use when you have long-read RNA-seq samples quantified by oarfish (output as quant.gz files) and need to extract transcript-level or gene-level abundance, count, and length matrices for downstream statistical analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3198
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_3308
  tools:
  - tximport
  - DESeq2
  - edgeR
  - limma-voom
derived_from:
- doi: 10.12688/f1000research.7563.1
  title: tximport
evidence_spans:
- Imports transcript-level abundance, estimated counts and transcript lengths, and summarizes into matrices for use with downstream statistical analysis packages
- Importing transcript abundance with tximport
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/transcriptomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_tximport
    doi: 10.12688/f1000research.7563.1
    title: tximport
  dedup_kept_from: coll_tximport
schema_version: 0.2.0
---

# oarfish-quantification-format-handling

## Summary

Import and extract transcript-level abundance, count, and length matrices from oarfish long-read RNA-seq quantification files (quant.gz format) using tximport. This skill is essential when working with oarfish-quantified long-read data that must be integrated into downstream differential expression workflows.

## When to use

You have long-read RNA-seq samples quantified by oarfish (output as quant.gz files) and need to extract transcript-level or gene-level abundance, count, and length matrices for downstream statistical analysis. Use this skill when you want to preserve transcript-level information during import rather than immediately aggregating to gene level, or when you need length matrices to account for differential isoform usage across samples.

## When NOT to use

- Input files are already in gene-level count matrix format (use directly with DESeq2 or edgeR instead of re-importing)
- Quantification was performed with a different tool (salmon, sailfish, kallisto); use the appropriate type parameter instead
- You require inferential replicates (Gibbs or bootstrap samples); verify oarfish output includes these before attempting import

## Inputs

- oarfish quant.gz files (one per sample)
- sample metadata or design table (recommended for downstream use)
- tx2gene mapping data.frame (required if gene-level summarization is desired)

## Outputs

- abundance matrix (transcript or gene level, rows = features, columns = samples)
- counts matrix (estimated counts, same dimensions as abundance)
- length matrix (average transcript length weighted by sample-specific abundance)

## How to apply

Load oarfish quant.gz files using tximport with the type='oarfish' parameter to specify the quantification software. Set txOut=TRUE to retain transcript-level output matrices instead of gene-level summarization; omit or set txOut=FALSE if gene-level aggregation is desired. Extract the returned list object containing three matrices: 'abundance' (normalized transcript abundances), 'counts' (estimated transcript counts), and 'length' (transcript lengths weighted by sample-specific abundances). The length matrix can subsequently be used as an offset for downstream gene-level differential analysis to correct for potential changes in gene length arising from differential isoform usage. Verify that matrix dimensions match the number of samples and transcripts/genes, and check for consistency of row names (transcript or gene IDs) and column names (sample identifiers) across replicates.

## Related tools

- **tximport** (Primary import function; accepts type='oarfish' parameter and txOut flag to control output level and extract matrices) — github:thelovelab__tximport
- **DESeq2** (Downstream differential expression analysis using imported count matrices and length-based offsets)
- **edgeR** (Alternative downstream differential expression analysis using imported count matrices and length-based offsets)
- **limma-voom** (Alternative downstream differential expression analysis using imported count matrices and length-based offsets)

## Examples

```
txi <- tximport(files = c('sample1.quant.gz', 'sample2.quant.gz', 'sample3.quant.gz'), type = 'oarfish', txOut = TRUE)
```

## Evaluation signals

- Returned abundance, counts, and length matrices have consistent dimensions (same number of rows = features, same number of columns = samples)
- Row names match expected transcript or gene IDs from the quantification; column names match input sample identifiers
- Abundance values are in expected range (typically 0–1 or log-scale); counts are non-negative integers or near-integer estimates; length values are positive
- No missing (NA) or infinite values in returned matrices; all samples are represented
- Downstream differential analysis (DESeq2/edgeR/limma-voom) accepts the matrices without format errors and length offset can be incorporated

## Limitations

- tximport requires a tx2gene mapping only if gene-level summarization is desired; transcript-level output (txOut=TRUE) does not require this mapping
- The length matrix represents average transcript length weighted by abundance and may vary across samples due to differential isoform usage; this is intentional and supports correction for composition bias in downstream analysis
- No automatic metadata annotation is provided by tximport itself; for automatic addition of annotation metadata, use the tximeta package instead

## Evidence

- [other] transcript-level import with txOut parameter: "tximport with type='oarfish' and txOut=TRUE successfully imports transcript-level abundance, count, and length matrices from oarfish quant.gz files"
- [intro] length matrix for offset calculation: "Average transcript length, weighted by sample-specific transcript abundance estimates, is provided as a matrix which can be used as an offset for different expression of gene-level counts"
- [readme] tximport function purpose: "Imports transcript-level abundance, estimated counts and transcript lengths, and summarizes into matrices for use with downstream statistical analysis packages such as edgeR, DESeq2, limma-voom"
- [intro] type parameter specification: "The tximport package has a single function for importing transcript-level estimates. The type argument is used to specify what software was used for estimation"
- [intro] correction for differential isoform usage: "this approach corrects for potential changes in gene length across samples (e.g. from differential isoform usage)"
