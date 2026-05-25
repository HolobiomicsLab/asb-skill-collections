---
name: gene-expression-quantification-rpkm-calculation
description: "Quantifies gene expression levels by normalizing RNA-seq read counts to RPKM (reads per kilobase per million mapped reads), accounting for library size and composition bias through TMM normalization. This skill bridges raw read-count matrices to interpretable expression fold-changes across experimental conditions."
when_to_use_negative: |
  - "Input count matrix is already log2-transformed or normalized to counts per million (CPM); re-normalizing will compound bias."
  - "Only single replicate per condition; statistical power is lost and fold-change estimates become unreliable."
  - "Gene length annotations are unavailable; RPKM requires exact per-gene length to normalize for transcript size."
edam_operation: "http://edamontology.org/operation_3565"
edam_topics: |
  - "http://edamontology.org/topic_3170"
  - "http://edamontology.org/topic_0769"
tools: |
  - name: "HTSeq"
  role: "counts aligned reads mapping to annotated genes in union mode (stranded=reverse) to produce raw count matrices that serve as input to RPKM normalization"
  - name: "edgeR"
  role: "applies TMM normalization via calcNormFactors() to account for library composition bias, then computes RPKM values via rpkm() function"
  - name: "R"
  role: "executes edgeR normalization and RPKM calculation workflows, loads count data, and tabulates normalized expression tables"
  - name: "HISAT2"
  role: "generates aligned BAM files that are subsequently counted by HTSeq; output files determine total mapped reads used in RPKM denominator"
provenance: |
  source_task_ids:
  - task_003
  source_papers:
  - doi: "10.1073/pnas"
  title: "Proceedings of the National Academy of Sciences"
schema_version: "0.2.0"
metadata:
  iri: https://w3id.org/holobiomicslab/asb-skill/gene-expression-quantification-rpkm-calculation@sha256:16bb88f515468e9ee8efab376590efb189849b989127e848fad691767c35eda8
---

# gene-expression-quantification-rpkm-calculation

## Summary

Quantifies gene expression levels by normalizing RNA-seq read counts to RPKM (reads per kilobase per million mapped reads), accounting for library size and composition bias through TMM normalization. This skill bridges raw read-count matrices to interpretable expression fold-changes across experimental conditions.

## When to use

You have aligned RNA-seq reads (BAM files) mapped to a reference genome, have generated raw gene-level read count matrices (e.g., from HTSeq), and need to normalize expression values to compare transcript abundance across treatment conditions (e.g., baicalin-supplemented vs. control cultures). Use this when a specific quantitative threshold (e.g., two-fold change) must be verified numerically.

## When NOT to use

- Input count matrix is already log2-transformed or normalized to counts per million (CPM); re-normalizing will compound bias.
- Only single replicate per condition; statistical power is lost and fold-change estimates become unreliable.
- Gene length annotations are unavailable; RPKM requires exact per-gene length to normalize for transcript size.

## Inputs

- raw gene-level read count matrix (e.g., HTSeq union-mode counts)
- gene length annotations (in kilobases)
- sample metadata (condition labels: baicalin-supplemented, control)

## Outputs

- RPKM-normalized expression table (genes × samples)
- fold-change values for target genes (e.g., LbUGT3)
- verification of expression threshold (e.g., two-fold increase)

## How to apply

Load raw read count matrices into R (or equivalent). Apply trimmed mean of M-values (TMM) normalization via edgeR's calcNormFactors() to correct for library size and composition bias. Calculate RPKM values using edgeR's rpkm() function, which normalizes by gene length (kilobases) and total mapped reads (millions). Extract expression values for target genes under each condition, compute the fold-change ratio, and tabulate the normalized expression table. This multi-step normalization ensures that apparent fold-changes reflect biological differences, not sequencing depth or transcript-size artifacts.

## Related tools

- **HTSeq** (counts aligned reads mapping to annotated genes in union mode (stranded=reverse) to produce raw count matrices that serve as input to RPKM normalization)
- **edgeR** (applies TMM normalization via calcNormFactors() to account for library composition bias, then computes RPKM values via rpkm() function)
- **R** (executes edgeR normalization and RPKM calculation workflows, loads count data, and tabulates normalized expression tables)
- **HISAT2** (generates aligned BAM files that are subsequently counted by HTSeq; output files determine total mapped reads used in RPKM denominator)

## Examples

```
library(edgeR); counts <- read.table('htseq_counts.txt', row.names=1); dge <- DGEList(counts=counts, group=c('control','control','baicalin','baicalin')); dge <- calcNormFactors(dge, method='TMM'); rpkm_vals <- rpkm(dge, gene.length=geneLengths); write.table(rpkm_vals, 'LbUGT3_RPKM_normalized.txt')
```

## Evaluation signals

- Fold-change for target gene (LbUGT3) matches expected threshold (e.g., exactly 2.0 or within 5–10% confidence interval); verify baicalin-supplemented RPKM ÷ control RPKM = 2.0.
- TMM normalization factors are in expected range (typically 0.8–1.2 per library); extreme values (>1.5 or <0.5) indicate severe composition bias.
- RPKM values are non-negative and finite for all genes; presence of NaN or negative values indicates missing gene lengths or count matrix corruption.
- Tabulated expression table has consistent structure: one row per gene, one column per sample, values in RPKM units; spot-check 2–3 housekeeping genes for reasonable values (typically 5–100 RPKM).
- Total mapped reads per sample (from BAM file headers or samtools idxstats) are consistent with denominator used in RPKM calculation; discrepancies indicate mismatched alignment or counting steps.

## Limitations

- RPKM assumes all reads within a gene are equitably distributed; highly expressed exons may skew per-gene averages, especially for alternatively spliced transcripts.
- Requires accurate gene length annotations; error in annotation (e.g., missing exons, intron inclusion) directly propagates to RPKM error.
- TMM normalization is sensitive to presence of highly differentially expressed genes (>10-fold changes); if many genes show extreme fold-changes, TMM may under-correct.
- Target enzyme prioritization difficult when multiple genes show high expression levels simultaneously, limiting power of fold-change alone to identify causal genes.
- RPKM alone does not provide statistical significance; differential expression testing (e.g., edgeR GLM) is needed to assign p-values to fold-changes.

## Evidence

- [other] Load count data into R and apply edgeR normalization using trimmed mean of M-values (TMM) and calcNormFactors() to account for library size and composition bias.: "Load count data into R and apply edgeR normalization using trimmed mean of M-values (TMM) and calcNormFactors() to account for library size and composition bias."
- [other] Calculate RPKM (reads per kilobase per million mapped reads) values using edgeR's rpkm() function.: "Calculate RPKM (reads per kilobase per million mapped reads) values using edgeR's rpkm() function."
- [results] RNAseq analysis revealed that LbUGT3 expression increased two-fold when L. brumalis was supplemented with baicalin (compound 1) compared to cultures without plant phenolics, as quantified by RPKM (reads per kilobase per million mapped reads).: "RNAseq analysis revealed that LbUGT3 expression increased two-fold when L. brumalis was supplemented with baicalin (compound 1) compared to cultures without plant phenolics, as quantified by RPKM"
- [results] the expression level of LbUGT3 showed two-fold increase in the growth media containing 1: "the expression level of LbUGT3 showed two-fold increase in the growth media containing 1"
- [other] Extract and tabulate LbUGT3 expression values for baicalin-supplemented and control conditions, verify two-fold expression increase, and save normalized expression table.: "Extract and tabulate LbUGT3 expression values for baicalin-supplemented and control conditions, verify two-fold expression increase, and save normalized expression table."
- [discussion] The RNAseq analysis provided us with a clue for target prioritization, but it will not be helpful when multiple genes show high level of expression or target enzyme is a housekeeping one: "The RNAseq analysis provided us with a clue for target prioritization, but it will not be helpful when multiple genes show high level of expression or target enzyme is a housekeeping one"
