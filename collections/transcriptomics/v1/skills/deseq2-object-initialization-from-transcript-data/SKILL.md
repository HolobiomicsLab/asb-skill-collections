---
name: deseq2-object-initialization-from-transcript-data
description: Use when you have transcript-level abundance, count, and length estimates (from salmon, Sailfish, or kallisto via tximport) and want to perform gene-level differential expression analysis in DESeq2 using the 'original counts and offset' method, which accounts for changes in effective gene length.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3258
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3308
  tools:
  - tximport
  - DESeq2
  - salmon
  - tximeta
derived_from:
- doi: 10.12688/f1000research.7563.1
  title: tximport
evidence_spans:
- Imports transcript-level abundance, estimated counts and transcript lengths, and summarizes into matrices for use with downstream statistical analysis packages
- Importing transcript abundance with tximport
- use with downstream statistical analysis packages such as edgeR, DESeq2, limma-voom
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

# DESeq2 Object Initialization from Transcript Data

## Summary

Construct a DESeqDataSet from transcript-level quantification (via tximport) with an embedded offset matrix that corrects for differential isoform usage at the gene level. This skill bridges transcript-level abundance estimates to gene-level differential expression analysis while preserving length-derived offsets.

## When to use

You have transcript-level abundance, count, and length estimates (from salmon, Sailfish, or kallisto via tximport) and want to perform gene-level differential expression analysis in DESeq2 using the 'original counts and offset' method, which accounts for changes in effective gene length across samples due to differential isoform usage.

## When NOT to use

- Input is already a count matrix with no transcript-length or isoform-usage information — use standard DESeqDataSetFromMatrix instead.
- You intend to perform transcript-level differential expression analysis — use tximport with txOut=TRUE to generate transcript-level matrices and analyze directly.
- Transcript quantification tool output is not from salmon, Sailfish, or kallisto — tximport does not support all quantifiers.

## Inputs

- tximport list object (containing gene-level counts, abundance, and length matrices)
- sample table / colData (data.frame with sample identifiers and condition/group assignments)

## Outputs

- DESeqDataSet object with embedded offset matrix derived from transcript-length estimates

## How to apply

Import transcript-level estimates using tximport with a tx2gene mapping to generate gene-level matrices (abundance, counts, and length). Create a sample table (colData) with sample identifiers and experimental group assignments. Pass the tximport list object and sample table to DESeq2::DESeqDataSetFromTximport, which automatically constructs an offset matrix from the length matrix to correct for differential isoform usage. Verify that the resulting DESeqDataSet object contains the offset matrix in the correct slot and has the expected dimensions (genes × samples for counts and offset). This approach avoids discarding multi-mapped reads and improves sensitivity by leveraging transcript-level estimates rather than gene-level alignment.

## Related tools

- **tximport** (Imports transcript-level abundance, estimated counts, and transcript lengths from salmon/Sailfish/kallisto; summarizes into gene-level matrices for downstream analysis) — https://github.com/thelovelab/tximport
- **DESeq2** (Constructs DESeqDataSet from tximport output and performs gene-level differential expression analysis using offset-corrected counts)
- **salmon** (Quantifies transcript-level abundance and estimated counts; output imported by tximport)
- **tximeta** (Extends tximport with automatic addition of annotation metadata to the tximport list object)

## Examples

```
txi <- tximport(files, type='salmon', tx2gene=tx2gene); dds <- DESeq2::DESeqDataSetFromTximport(txi, colData, design=~condition)
```

## Evaluation signals

- The returned DESeqDataSet object contains a non-null offset matrix in the assays slot with dimensions matching the count matrix (genes × samples).
- Offset matrix values reflect transcript-length-weighted abundance estimates and vary across samples consistent with differential isoform usage.
- DESeqDataSet colData matches the input sample table in row order and column content.
- Gene-level count matrix dimensions match the number of unique gene IDs in the tx2gene mapping.
- Downstream DESeq2 analysis (DESeq function) executes without error and uses the embedded offset in the generalized linear model fit.

## Limitations

- The offset matrix is only as accurate as the transcript-length estimates from the quantifier; misspecified or poorly estimated lengths can bias correction.
- This approach assumes that differences in isoform usage are the primary source of gene-length variation; other sources of bias (e.g. GC content, library prep effects) are not corrected.
- The skill does not handle cases where tx2gene mapping is incomplete or contains many unmapped transcripts; careful validation of the tx2gene data.frame is required beforehand.
- Offset-based correction is appropriate for gene-level summary of transcript counts, but the article emphasizes that gene-level analysis should be complemented with transcript- or exon-level analysis for complete understanding.

## Evidence

- [other] DESeq2::DESeqDataSetFromTximport accepts a tximport list object and sample table and automatically constructs the appropriate offset matrix from transcript-length estimates.: "DESeq2::DESeqDataSetFromTximport accepts a tximport list object (containing gene-level counts, abundance, and length matrices) and a sample table, and automatically constructs the appropriate offset"
- [intro] The length matrix from tximport can be used to generate an offset matrix for downstream gene-level differential analysis.: "The 'length' matrix can be used to generate an offset matrix for downstream gene-level differential analysis of count matrices"
- [intro] tximport corrects for potential changes in gene length across samples from differential isoform usage.: "this approach corrects for potential changes in gene length across samples (e.g. from differential isoform usage)"
- [intro] tximport generates gene-level matrices of abundance, counts, and length by summarizing transcript-level information.: "A simple list with matrices, 'abundance', 'counts', and 'length', is returned, where the transcript level information is summarized to the gene-level"
- [readme] README states tximport summarizes transcript-level estimates into matrices for use with downstream packages like DESeq2, with length matrix available as offset.: "Average transcript length, weighted by sample-specific transcript abundance estimates, is provided as a matrix which can be used as an offset for different expression of gene-level counts."
