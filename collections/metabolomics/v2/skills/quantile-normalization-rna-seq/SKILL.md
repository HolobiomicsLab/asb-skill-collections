---
name: quantile-normalization-rna-seq
description: Use when apply quantile normalization after filtering a Salmon-derived count matrix for low-abundance features using edgeR, and before batch-effect correction or differential expression analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0203
  tools:
  - limma
  - sva
  - ggplot2
  - ComplexHeatmap
  - edgeR
  - Nextflow
derived_from:
- doi: 10.1093/bioadv/vbae175
  title: MultiOmicsIntegrator
evidence_spans:
- 'Genes, miRNA, isoforms, proteins, lipids | Data preprocessing | R packages: edger, limma, sva'
- 'Genes, miRNA, isoforms, proteins, lipids | Data preprocessing | R packages: edger, limma, sva, ggplot2, ComplexHeatmap'
- 'R packages: DESeq2, edger, RankProd, ggplot2 ComplexHeatmap'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_multiomicsintegrator_cq
    doi: 10.1093/bioadv/vbae175
    title: MultiOmicsIntegrator
  dedup_kept_from: coll_multiomicsintegrator_cq
schema_version: 0.2.0
---

# quantile-normalization-rna-seq

## Summary

Quantile normalization is a distribution-based normalization method applied to filtered RNA-seq count matrices to remove technical variation across samples while preserving biological signal. It is a standard preprocessing step in multi-omics pipelines before differential expression analysis.

## When to use

Apply quantile normalization after filtering a Salmon-derived count matrix for low-abundance features using edgeR, and before batch-effect correction or differential expression analysis. Use this step when comparing expression levels across multiple RNA-seq samples and technical variation in library preparation or sequencing depth is suspected.

## When NOT to use

- Input count matrix has not been filtered for low-abundance features; apply filtering first to remove noise that distorts the reference distribution.
- Data is already normalized using a different method (e.g., TMM, DESeq2 median-of-ratios); applying quantile normalization after another normalization may introduce artifacts.
- Single-sample analysis or case studies where distributional alignment across samples is not relevant to the research question.

## Inputs

- Filtered count matrix from Salmon (RNA-seq gene/isoform/miRNA expression counts)
- Sample metadata/samplesheet (to identify sample associations if needed for distribution calculation)

## Outputs

- Quantile-normalized count matrix (RData format)
- Quantile-normalized count matrix (text format)

## How to apply

Load the filtered count matrix (post-filterByExp or post-cutoff filtering) into R and apply quantile normalization using the limma package. The method ranks expression values across samples and forces the empirical distribution of each sample to match a common reference distribution (typically the average of all sample distributions), ensuring that all samples have identical marginal distributions. This removes distributional differences while preserving the rank order of genes within each sample. Output the normalized matrix in both RData and text formats for downstream differential expression analysis or batch-effect correction.

## Related tools

- **limma** (Performs quantile normalization via R package functions on the filtered count matrix)
- **edgeR** (Upstream filtering (filterByExp) applied before quantile normalization to remove low-expression features)
- **Nextflow** (Workflow orchestration framework executing the preprocess_matrix subworkflow containing filtering, normalization, and batch-correction steps) — https://www.nextflow.io
- **sva** (Downstream batch-effect correction applied after quantile normalization using ComBat or SVA methods)

## Evaluation signals

- Verify that all samples have identical marginal distributions (e.g., box plots or density plots of log-normalized counts should be visually aligned after normalization).
- Confirm that the rank order of genes within each sample is preserved; gene A should remain higher-ranked than gene B if so before normalization.
- Check that the normalized matrix has no negative values and that the distribution of counts is continuous and smooth across the quantile range.
- Principal component analysis (PCA) or unsupervised clustering should reveal known batch structure or biological grouping; if collapsed unexpectedly, diagnose whether quantile normalization was too aggressive.
- Validate that downstream differential expression analysis (e.g., edgeR or DESeq2) detects expected biological signals; loss of known significant genes suggests over-normalization.

## Limitations

- Quantile normalization assumes that most genes are not differentially expressed across samples; severe imbalances in up/down-regulation can distort the reference distribution.
- The method is sensitive to outlier samples with extreme distributions; quality control and outlier detection should precede normalization.
- Quantile normalization may not be appropriate for sparse count data or very low-depth samples; minimum expression thresholds (via edgeR filterByExp) should be enforced first.
- After quantile normalization, counts lose their discrete integer nature and cannot be directly used with count-based statistical models; use normalized values only for visualization or as input to methods expecting continuous data.

## Evidence

- [methods] Apply quantile normalization to the filtered count matrix using the limma package.: "Apply quantile normalization to the filtered count matrix using the limma package."
- [other] The preprocess_matrix subworkflow supports filtering, normalization using calcNorm or quantile methods, and batch correction.: "The preprocess_matrix subworkflow supports three configurable preprocessing operations: filtering via filterByExp or cutoff values, normalization using calcNorm or quantile methods, and batch effect"
- [methods] Data preprocessing for omics data includes R packages: edger, limma, sva, ggplot2, ComplexHeatmap.: "Data preprocessing | Genes, miRNA, isoforms, proteins, lipids | Data preprocessing | R packages: edger, limma, sva, ggplot2, ComplexHeatmap"
- [other] Apply filterByExp filtering before normalization to retain features meeting minimum expression thresholds.: "Apply filterByExp filtering using edgeR to retain features meeting minimum expression thresholds as specified in params_genes.yml."
