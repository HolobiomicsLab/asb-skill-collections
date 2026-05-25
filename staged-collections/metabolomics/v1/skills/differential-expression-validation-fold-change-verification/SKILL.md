---
name: differential-expression-validation-fold-change-verification
description: Validates predicted fold-change in gene expression by quantifying RNA-seq read counts, applying library-size normalization, and computing RPKM values to confirm that target genes meet expected expression thresholds under specific treatment conditions. This skill bridges transcriptional hypothesis and computational quantification, ensuring fold-change claims are grounded in normalized count data.
when_to_use_negative:
- Input is already a normalized expression matrix or TPM/FPKM values—skip to fold-change extraction rather than re-normalizing.
- RNA-seq reads have not been aligned to a reference genome or BAM files are unsorted/unvalidated—perform alignment and BAM curation first.
- The predicted fold-change threshold is not specified or hypothesis is exploratory (not confirmatory)—use differential expression testing (e.g., edgeR GLM, DESeq2) instead to identify significant genes without a prior fold-change target.
edam_operation: http://edamontology.org/operation_3565
edam_topics:
- http://edamontology.org/topic_3170
- http://edamontology.org/topic_0203
tools:
- name: HTSeq
  role: Counts reads mapped to annotated genes from sorted BAM files using union overlap mode and reverse strand orientation to produce raw count matrices.
- name: edgeR
  role: Applies TMM normalization via calcNormFactors() and computes RPKM values using the rpkm() function to normalize for library size, composition bias, and gene length.
- name: R
  role: Environment for loading count data, running edgeR normalization, computing fold-change ratios, and generating summary tables.
- name: HISAT2
  role: Splice-aware aligner used upstream to generate sorted BAM files from paired-end RNA-seq reads; required input for this skill.
provenance:
  source_task_ids:
  - task_003
  source_papers:
  - doi: 10.1073/pnas
    title: Proceedings of the National Academy of Sciences
schema_version: 0.2.0
metadata:
  iri: https://w3id.org/holobiomicslab/asb-skill/differential-expression-validation-fold-change-verification@sha256:146ae04bf1974544503455722c6c0ef4c1ff6bd636b5e527e7be8146f53080ca
---

# differential-expression-validation-fold-change-verification

## Summary

Validates predicted fold-change in gene expression by quantifying RNA-seq read counts, applying library-size normalization, and computing RPKM values to confirm that target genes meet expected expression thresholds under specific treatment conditions. This skill bridges transcriptional hypothesis and computational quantification, ensuring fold-change claims are grounded in normalized count data.

## When to use

When RNA-seq data has been aligned to a reference genome and you need to verify a quantitative hypothesis about expression magnitude (e.g., 'LbUGT3 expression increases two-fold under baicalin supplementation'). Apply this skill after read mapping is complete and you have BAM files stratified by experimental condition, but before downstream functional experiments on candidate genes.

## When NOT to use

- Input is already a normalized expression matrix or TPM/FPKM values—skip to fold-change extraction rather than re-normalizing.
- RNA-seq reads have not been aligned to a reference genome or BAM files are unsorted/unvalidated—perform alignment and BAM curation first.
- The predicted fold-change threshold is not specified or hypothesis is exploratory (not confirmatory)—use differential expression testing (e.g., edgeR GLM, DESeq2) instead to identify significant genes without a prior fold-change target.

## Inputs

- sorted BAM files aligned to reference genome (treatment and control conditions)
- annotated gene feature coordinates (GFF/GTF)
- sample metadata (condition labels, replicates)

## Outputs

- raw read count matrix (genes × samples)
- TMM-normalized library size factors
- RPKM expression matrix
- fold-change table (target gene, treatment vs. control)
- normalized expression summary table

## How to apply

Count aligned reads per gene using HTSeq in union mode with reverse strand orientation to produce raw count matrices for all samples. Load count data into R and apply edgeR's trimmed mean of M-values (TMM) normalization via calcNormFactors() to account for library size and composition bias. Compute RPKM (reads per kilobase per million mapped reads) values using edgeR's rpkm() function, which normalizes for both gene length and sequencing depth. Extract RPKM values for the target gene (e.g., LbUGT3) across treatment (baicalin-supplemented) and control (no plant phenolics) conditions. Calculate the fold-change ratio as RPKM(treatment) / RPKM(control) and verify it matches the predicted threshold (e.g., ≥2.0-fold). Tabulate and save normalized expression values alongside fold-change metrics to document the verification.

## Related tools

- **HTSeq** (Counts reads mapped to annotated genes from sorted BAM files using union overlap mode and reverse strand orientation to produce raw count matrices.)
- **edgeR** (Applies TMM normalization via calcNormFactors() and computes RPKM values using the rpkm() function to normalize for library size, composition bias, and gene length.)
- **R** (Environment for loading count data, running edgeR normalization, computing fold-change ratios, and generating summary tables.)
- **HISAT2** (Splice-aware aligner used upstream to generate sorted BAM files from paired-end RNA-seq reads; required input for this skill.)

## Examples

```
# Load count matrix and apply TMM normalization
library(edgeR)
counts <- read.table('htseq_counts.txt', row.names=1)
groups <- factor(c(rep('control', 3), rep('baicalin', 3)))
dge <- DGEList(counts=counts, group=groups)
dge <- calcNormFactors(dge, method='TMM')
rpkm_values <- rpkm(dge, gene.length=gene_lengths)
write.table(rpkm_values[grep('LbUGT3', rownames(rpkm_values)), ], file='LbUGT3_rpkm.txt', sep='\t')
```

## Evaluation signals

- Raw count matrix has no negative or non-integer values; dimensions match number of genes and samples.
- TMM normalization factors are close to 1.0 for samples with similar library composition; values deviate for compositionally biased samples, indicating successful bias correction.
- RPKM values are positive and in the expected range (typically 0.1–10,000 for expressed genes); zero or near-zero RPKM indicates unexpressed genes.
- Fold-change ratio for target gene (treatment RPKM / control RPKM) meets or exceeds the predicted threshold (e.g., ≥2.0-fold); if below threshold, hypothesis is not supported and warrants re-examination of alignment quality or biological reproducibility.
- Normalized expression table is complete with no missing values for target genes and can be cross-referenced against raw counts to verify consistency of normalization.

## Limitations

- RPKM normalization assumes that most genes are not differentially expressed; if treatment induces widespread expression changes, TMM factors may be biased and fold-change estimates less reliable.
- Fold-change verification requires replicate samples per condition to assess reproducibility; single samples per condition cannot distinguish true expression differences from technical noise.
- RPKM is sensitive to gene length annotation errors; incorrect or missing exon coordinates in the reference GTF will produce misleading expression estimates.
- Target gene prioritization by fold-change alone may be insufficient when multiple genes show similarly high expression levels or when the true functional gene is a constitutively expressed housekeeping gene.

## Evidence

- [methods] HTSeq counting with union mode and reverse strand: "Count reads mapping to annotated genes using HTSeq (mode=union, stranded=reverse) to produce raw count matrices."
- [methods] edgeR TMM normalization and RPKM computation: "Load count data into R and apply edgeR normalization using trimmed mean of M-values (TMM) and calcNormFactors() to account for library size and composition bias. Calculate RPKM (reads per kilobase"
- [methods] Extraction and verification of two-fold fold-change: "Extract and tabulate LbUGT3 expression values for baicalin-supplemented and control conditions, verify two-fold expression increase, and save normalized expression table."
- [results] Finding of LbUGT3 two-fold expression increase: "RNAseq analysis revealed that LbUGT3 expression increased two-fold when L. brumalis was supplemented with baicalin (compound 1) compared to cultures without plant phenolics, as quantified by RPKM"
- [other] Research question motivating fold-change verification: "Does LbUGT3 expression increase two-fold in L. brumalis cultured with baicalin compared to control conditions, and can this be quantified through RNA-seq read mapping, counting, and normalization"
