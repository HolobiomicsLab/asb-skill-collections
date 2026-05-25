---
name: transcript-abundance-estimation-counting
description: Use when metabolomics LC-MS GC-MS untargeted lipidomics to quantify mRNA abundance from RNA-seq read alignments by counting reads per annotated gene and normalizing for library composition bias.
when_to_use_negative:
- Input reads are unaligned or from unstranded libraries where strand information is unavailable — HTSeq mode=union with stranded=reverse will produce biased counts
- Gene annotations are incomplete or highly fragmented — HTSeq union mode will misassign reads to wrong features, inflating noise
- Sample sizes are very small (n < 2 per group) — TMM normalization requires sufficient library diversity to estimate composition bias reliably
edam_operation: http://edamontology.org/operation_3680
edam_topics:
- http://edamontology.org/topic_3170
- http://edamontology.org/topic_0203
tools:
- name: HTSeq
  role: Count reads overlapping annotated genes from BAM files in union mode with reverse strand orientation
- name: edgeR
  role: Apply TMM normalization via calcNormFactors() and calculate RPKM values via rpkm() function
- name: R
  role: Load count matrix and execute edgeR normalization and RPKM calculation
provenance:
  source_task_ids:
  - task_003
  source_papers:
  - doi: 10.1073/pnas
    title: Proceedings of the National Academy of Sciences
schema_version: 0.2.0
metadata:
  iri: https://w3id.org/holobiomicslab/asb-skill/transcript-abundance-estimation-counting@sha256:1da0e6c3e23226a8156a6a4b129c3ea2cb8c865fa46b6b19af744e8070eab33f
---

# transcript-abundance-estimation-counting

## Summary

Quantify mRNA abundance from RNA-seq read alignments by counting reads per annotated gene and normalizing for library composition bias. This skill bridges alignment and differential expression analysis, producing normalized expression matrices suitable for statistical testing.

## When to use

You have sorted BAM files from splice-aware alignment (e.g., HISAT2) of paired-end RNA-seq reads to a reference genome, annotated gene coordinates, and need to measure per-gene transcript abundance to detect expression changes across treatment conditions (e.g., baicalin supplementation vs. control).

## When NOT to use

- Input reads are unaligned or from unstranded libraries where strand information is unavailable — HTSeq mode=union with stranded=reverse will produce biased counts
- Gene annotations are incomplete or highly fragmented — HTSeq union mode will misassign reads to wrong features, inflating noise
- Sample sizes are very small (n < 2 per group) — TMM normalization requires sufficient library diversity to estimate composition bias reliably

## Inputs

- sorted BAM files from splice-aware read alignment (e.g., HISAT2 output)
- annotated gene feature file (GFF/GTF format)
- sample metadata specifying experimental conditions

## Outputs

- raw read count matrix (genes × samples)
- normalized expression matrix (RPKM values)
- normalization factors from TMM
- per-gene expression table for target genes across conditions

## How to apply

Count reads mapping to each annotated gene using HTSeq in union mode with reverse strand specification to avoid double-counting overlapping features. Load the resulting raw count matrix into R and apply trimmed mean of M-values (TMM) normalization via edgeR's calcNormFactors() to correct for library size and composition bias. Calculate RPKM (reads per kilobase per million mapped reads) using edgeR's rpkm() function to account for gene length and sequencing depth. Verify the normalization by confirming that median expression shifts are minimal across samples and that the distribution of log2-fold-changes is centered near zero. Extract expression values for target genes (e.g., LbUGT3) and tabulate normalized counts for comparison across conditions.

## Related tools

- **HTSeq** (Count reads overlapping annotated genes from BAM files in union mode with reverse strand orientation)
- **edgeR** (Apply TMM normalization via calcNormFactors() and calculate RPKM values via rpkm() function)
- **R** (Load count matrix and execute edgeR normalization and RPKM calculation)

## Examples

```
# Count reads from BAM to raw counts:
htseq-count -f bam -r pos -s reverse -m union baicalin_treated.bam genes.gtf > baicalin_counts.txt

# Normalize in R:
library(edgeR); counts <- read.table('baicalin_counts.txt'); dge <- DGEList(counts); dge <- calcNormFactors(dge, method='TMM'); rpkm_table <- rpkm(dge, gene.length=gene_widths)
```

## Evaluation signals

- Raw count distributions are non-negative integers with expected depth (millions of reads per sample); no negative or fractional values
- Normalization factors from calcNormFactors() are close to 1.0 (typically 0.8–1.2), indicating balanced library composition; factors far from 1 suggest severe composition bias not fully corrected
- RPKM values are positive real numbers; median RPKM across samples per gene should be similar, confirming composition correction
- Target gene (e.g., LbUGT3) shows expected fold-change magnitude (e.g., ≥ 2-fold) in supplemented vs. control condition, matching biological hypothesis
- MA plot (log2-fold-change vs. average log2 expression) is centered near y = 0 across the expression range, indicating successful normalization

## Limitations

- HTSeq union mode may introduce ambiguity when reads overlap multiple genes; consider using intersection-strict mode if gene annotation has extensive overlaps, at cost of discarding those reads
- TMM normalization assumes that most genes are not differentially expressed; if a treatment causes global expression shifts (e.g., > 50% of genes up-regulated), TMM may over-correct
- RPKM is susceptible to false positives for very short genes (< 300 bp) due to length normalization; consider alternative metrics (TPM, DESeq2 size factors) for short-gene studies
- Target enzyme prioritization may be difficult when multiple genes show high expression levels; RNAseq alone cannot resolve which enzyme is causative without functional validation

## Evidence

- [methods] Count reads using HTSeq approach and normalization: "Count reads mapping to annotated genes using HTSeq (mode=union, stranded=reverse) to produce raw count matrices."
- [methods] TMM normalization procedure in edgeR: "Load count data into R and apply edgeR normalization using trimmed mean of M-values (TMM) and calcNormFactors() to account for library size and composition bias."
- [methods] RPKM calculation and expression extraction: "Calculate RPKM (reads per kilobase per million mapped reads) values using edgeR's rpkm() function."
- [results] Verification of two-fold expression increase: "the expression level of LbUGT3 showed two-fold increase in the growth media containing 1"
- [results] Transcriptional profiling workflow context: "We conducted transcriptional profiling of eight L. brumalis UGTs in growth conditions without plant phenolics or with a flavonoid baicalin"
