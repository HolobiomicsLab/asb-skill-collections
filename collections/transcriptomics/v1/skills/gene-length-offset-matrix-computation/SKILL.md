---
name: gene-length-offset-matrix-computation
description: Use when you have transcript-level quantification (salmon, Sailfish, or kallisto output) summarized to gene level by tximport, and you observe or suspect differential isoform usage across your experimental conditions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0203
  tools:
  - tximport
  - DESeq2
  - salmon
  - Sailfish
  - kallisto
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

# gene-length-offset-matrix-computation

## Summary

Compute a transcript-length-derived offset matrix from tximport output to correct gene-level RNA-seq counts for differential isoform usage before differential expression analysis. This skill embeds length normalization into the statistical model to avoid biased inference when isoform composition varies across samples.

## When to use

You have transcript-level quantification (salmon, Sailfish, or kallisto output) summarized to gene level by tximport, and you observe or suspect differential isoform usage across your experimental conditions. The length matrix from tximport indicates sample-specific variation in average transcript length; use this skill to generate an offset that corrects gene-level count models for changes in effective gene length rather than true abundance changes.

## When NOT to use

- Input counts are from alignment-based methods (e.g., HTSeq, featureCounts) rather than pseudo-alignment (salmon/kallisto); these do not provide transcript-length estimates needed for offset construction.
- Analysis is at transcript level rather than gene level; use txOut=TRUE in tximport to retain transcript-level matrices instead.
- No evidence of isoform usage differences across samples or when isoform composition is assumed constant; offset correction may be unnecessary and may introduce noise if length variation is purely technical.

## Inputs

- tximport list object (txi) with gene-level counts, abundance, and length matrices
- sample table (colData) with sample identifiers and condition/group assignments

## Outputs

- DESeqDataSet object with embedded offset matrix derived from transcript-length estimates

## How to apply

Load the tximport list object (txi) produced by tximport() with type='salmon' (or equivalent), which contains gene-level counts, abundance, and length matrices. The length matrix represents average transcript length weighted by sample-specific transcript abundance estimates. Pass txi and a sample table (colData) to DESeq2::DESeqDataSetFromTximport, which automatically constructs and embeds the offset matrix from the length matrix into the resulting DESeqDataSet object. This offset matrix is then used internally during differential expression fitting (via DESeq()) to account for differential isoform usage. The rationale is that when isoform proportions differ across samples, the effective gene length changes; encoding this as an offset in the generalized linear model allows count differences to be attributed to true expression changes rather than compositional artifacts.

## Related tools

- **tximport** (Imports transcript-level estimates from pseudo-alignment quantifiers and aggregates to gene level, producing the length matrix used to compute the offset) — https://github.com/thelovelab/tximport
- **DESeq2** (DESeqDataSetFromTximport function accepts tximport output and automatically constructs and embeds the offset matrix into the DESeqDataSet for use in differential expression analysis)
- **salmon** (Upstream quantifier that produces transcript-level estimates (abundance and counts) ingested by tximport)
- **Sailfish** (Alternative upstream quantifier producing transcript-level estimates compatible with tximport)
- **kallisto** (Alternative upstream quantifier producing transcript-level estimates compatible with tximport)

## Examples

```
txi <- tximport(files, type='salmon', tx2gene=tx2gene); dds <- DESeqDataSetFromTximport(txi, colData=samples, design=~condition)
```

## Evaluation signals

- The offset matrix is present and accessible in the DESeqDataSet object (check assays(dds)['offset'] or modelMatrix(dds) metadata).
- Offset matrix dimensions match the gene-by-sample structure: genes (rows) × samples (columns).
- Offset values are non-zero and positive, reflecting log-scale normalization factors derived from length estimates.
- Differential expression results from DESeq(dds) show that genes with large length changes across conditions have adjusted fold changes closer to 1.0 compared to a model without offset, indicating correction for isoform-driven length shifts.
- The length matrix input used to construct the offset exhibits sample-wise variation (not constant across samples), confirming differential isoform usage is present.

## Limitations

- Offset computation assumes that transcript-length estimates from the quantifier are accurate and reflect true isoform composition; errors or bias in upstream quantification propagate to the offset.
- The method corrects for changes in effective gene length but does not separately estimate isoform-level expression; complementary transcript- or exon-level analysis may be needed to identify which isoforms drive the length changes.
- Requires that tximport was run with type specified correctly for the upstream quantifier; mismatched type can corrupt the length matrix.
- The README notes that 'we suggest that users not only perform gene-level analysis' — offset-based gene-level analysis should be complemented with transcript-level results to validate biological interpretation.

## Evidence

- [intro] tximport corrects for differential isoform usage: "this approach corrects for potential changes in gene length across samples (e.g. from differential isoform usage)"
- [intro] Length matrix used to generate offset for gene-level analysis: "The 'length' matrix can be used to generate an offset matrix for downstream gene-level differential analysis of count matrices"
- [readme] tximport produces length-derived matrices for offset construction: "Average transcript length, weighted by sample-specific transcript abundance estimates, is provided as a matrix which can be used as an offset for different expression of gene-level counts."
- [other] DESeqDataSetFromTximport embeds offset in DESeqDataSet: "DESeq2::DESeqDataSetFromTximport accepts a tximport list object (containing gene-level counts, abundance, and length matrices) and a sample table, and automatically constructs the appropriate offset"
