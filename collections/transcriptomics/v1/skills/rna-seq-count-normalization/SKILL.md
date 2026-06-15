---
name: rna-seq-count-normalization
description: Use when you have transcript-level abundance estimates and inferred counts from salmon/kallisto/Sailfish (with or without Gibbs/bootstrap replicates) that must be summarized to gene or transcript level, and you plan to use count-based differential expression tools (edgeR, DESeq2, limma-voom).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3218
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0099
  tools:
  - tximport
  - edgeR
  - DESeq2
  - limma-voom
  - salmon
  - tximeta
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

# rna-seq-count-normalization

## Summary

Normalize transcript- or gene-level count matrices derived from quantification tools (salmon, kallisto, Sailfish) by incorporating sample-specific length offsets and library size factors to account for differential isoform usage and sequencing depth before differential expression analysis. This skill bridges probabilistic quantification estimates with count-based statistical models in edgeR, DESeq2, or limma-voom.

## When to use

Apply this skill when you have transcript-level abundance estimates and inferred counts from salmon/kallisto/Sailfish (with or without Gibbs/bootstrap replicates) that must be summarized to gene or transcript level, and you plan to use count-based differential expression tools (edgeR, DESeq2, limma-voom). Normalization is mandatory when gene length varies across samples due to differential isoform usage, which violates the constant-length assumption of standard count-based models.

## When NOT to use

- Input is already an alignment-based count matrix (e.g., from featureCounts on BAM files); tximport is designed for pseudo-alignment or mapping-free quantifiers, not existing counts.
- Analysis goal is isoform-level (exon or splice-variant) differential expression; this skill handles gene or transcript level only.
- Quantification tool is not Salmon, Kallisto, or Sailfish (e.g., RSEM, eXpress); tximport does not natively support all quantifiers.

## Inputs

- Salmon/Kallisto/Sailfish quantification files (quant.sf or equivalent) with transcript-level abundance and counts
- Gibbs sample or bootstrap replicate files (optional, for inferential uncertainty quantification)
- tx2gene data.frame mapping transcript IDs to gene IDs (required for gene-level summarization; optional for transcript-level)

## Outputs

- DGEList object (edgeR) with normalized counts, offsets, and library size factors
- Alternatively: tximport list with count, abundance, and length matrices for manual offset construction
- Offset matrix (log-scale transcript length, weighted by sample-specific abundance)

## How to apply

First, import transcript-level quantification files using tximport with type='salmon' (or 'kallisto'/'sailfish') and specify txOut=TRUE for transcript-level or provide a tx2gene mapping for gene-level summarization. tximport returns a list containing count, abundance, and length matrices. For gene-level analysis, use the length matrix as an offset (log-scale) in your downstream model to adjust for transcript-length bias; edgeR::DGEListFromTximport automates this by accepting the tximport output and creating a DGEList with pre-computed offsets. For transcript-level analysis with inferential replicates (Gibbs samples), use divide=TRUE in DGEListFromTximport to estimate overdispersion from the replicate variability and produce variance-stabilized, divided counts. Verify that the resulting count matrix has no zero-length transcripts and that library size factors reflect total sequencing depth; inspect the offset or length matrix to confirm it captures sample-specific isoform composition.

## Related tools

- **tximport** (Imports transcript-level abundance, estimated counts and transcript lengths from pseudo-alignment quantifiers, then summarizes into normalized count, abundance, and length matrices for gene or transcript-level downstream analysis.) — https://github.com/thelovelab/tximport
- **edgeR** (Accepts tximport output via DGEListFromTximport to construct a DGEList with pre-computed offsets and library size normalization, enabling count-based differential expression analysis with proper length and depth correction.)
- **DESeq2** (Downstream differential expression tool compatible with tximport-normalized counts and length offsets for gene or transcript-level inference.)
- **limma-voom** (Downstream differential expression tool for count-based analysis using tximport-normalized counts and length offsets.)
- **salmon** (Upstream quantifier producing transcript-level abundance estimates, inferred counts, and (as of v1.3.9) Gibbs samples or bootstrap replicates that serve as input to tximport.)
- **tximeta** (Extension of tximport that provides the same normalization and summarization functionality plus automatic addition of genomic annotation metadata.)

## Examples

```
txi <- tximport(files=c('sample1.quant.sf', 'sample2.quant.sf'), type='salmon', tx2gene=tx2gene); dge <- edgeR::DGEListFromTximport(txi, group=c(1,2))
```

## Evaluation signals

- Inspect the resulting count matrix for absence of NA or infinite values; all transcript/gene lengths should be positive and finite.
- Verify that the offset matrix (or length matrix) reflects sample-specific variation in isoform composition; manually check that highly-expressed isoforms with variable usage produce non-uniform offsets across samples.
- Confirm library size factors in the DGEList sum to 1.0 (or similar norm) and match total counts per sample after length normalization.
- For inferential replicates (divide=TRUE): check that tagwise and common dispersion estimates are present and reasonable (typically 0.01–0.5 for RNA-seq); absence suggests insufficient replicate information.
- Cross-validate normalized counts against the original length matrix: gene-level counts should be lower for genes with shorter mean transcript length, all else equal.

## Limitations

- tximport assumes transcript quantification has been performed correctly by the upstream tool; garbage quantification input yields garbage counts and offsets.
- The length offset corrects for between-sample isoform shifts but does not account for within-isoform length variation (e.g., intron retention); exon-level or isoform-level analysis may be needed for fine-grained inference.
- Gibbs sample-based overdispersion estimation (divide=TRUE) requires multiple replicates per condition; sparse designs or single-replicate conditions may not provide stable dispersion estimates.
- Gene-level summarization via tx2gene loses transcript identity; transcript-level inference should be performed separately if isoform switching is of interest.

## Evidence

- [intro] approach corrects for potential changes in gene length across samples (e.g. from differential isoform usage): "this approach corrects for potential changes in gene length across samples (e.g. from differential isoform usage)"
- [readme] tximport functionality for importing and normalizing counts: "Imports transcript-level abundance, estimated counts and transcript lengths, and summarizes into matrices for use with downstream statistical analysis packages such as edgeR, DESeq2, limma-voom."
- [intro] length matrix use as offset for differential analysis: "The 'length' matrix can be used to generate an offset matrix for downstream gene-level differential analysis of count matrices"
- [readme] inferential replicates import capability: "tximport as of version 1.3.9 will import inferential replicates (Gibbs samples or bootstrap samples) from Salmon, Sailfish or kallisto."
- [other] DGEListFromTximport with divide parameter for divided counts: "DGEListFromTximport with divide=TRUE estimates count overdispersion from inferential replicates and produces divided counts suitable for transcript-level differential expression analysis"
