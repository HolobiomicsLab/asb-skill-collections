---
name: count-matrix-statistical-modeling
description: Use when after count matrix preprocessing (normalization, batch correction, low-count filtering) when you have a feature-by-sample count matrix and phenotype metadata, and you need to identify differentially expressed genes, miRNAs, isoforms, or other features across treatment groups or conditions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3223
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0203
  - http://edamontology.org/topic_2269
  tools:
  - DESeq2
  - RankProd
  - ggplot2
  - ComplexHeatmap
  - edgeR
derived_from:
- doi: 10.1093/bioadv/vbae175
  title: MultiOmicsIntegrator
evidence_spans:
- 'Differential expression analyss | R packages: DESeq2, edger, RankProd'
- '### DESeq2 [deseq](../modules/local/deseq2)'
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

# count-matrix-statistical-modeling

## Summary

Select and execute a statistical differential expression algorithm (edgeR, DESeq2, or RankProduct) on preprocessed RNA-seq count matrices to quantify feature-level fold-changes, test statistics, and adjusted p-values across sample groups. This skill dispatches the chosen algorithm based on user configuration and enforces samplesheet column conventions specific to each method.

## When to use

After count matrix preprocessing (normalization, batch correction, low-count filtering) when you have a feature-by-sample count matrix and phenotype metadata, and you need to identify differentially expressed genes, miRNAs, isoforms, or other features across treatment groups or conditions. Apply this skill when you must choose between edgeR (flexible contrasts), DESeq2 (strict column naming), or RankProduct (ranked non-parametric) based on your study design and assumptions.

## When NOT to use

- Input count matrix has already been subjected to differential expression analysis; reapplying will produce redundant or conflicting results.
- Sample metadata lacks required grouping columns ('condition', 'batch', or 'cl') for the chosen algorithm; metadata must be reconciled first.
- Count matrix contains continuous (normalized) values rather than integer counts; edgeR and DESeq2 assume count-level data and will produce invalid results on log-transformed or FPKM inputs.

## Inputs

- Preprocessed count matrix (genes × samples, integer-valued)
- Samplesheet/phenotype metadata file with sample identifiers and grouping columns
- params_genes.yml configuration file with alg_genes parameter
- Feature annotation table (gene symbols, biotypes, or lipid/protein identifiers)

## Outputs

- Differential expression results table (feature ID, log2 fold-change, test statistic, raw p-value, adjusted p-value)
- Volcano plot (ggplot2)
- MA plot (mean-average plot, ggplot2)
- P-value distribution histogram
- Heatmap of top significant features (ComplexHeatmap)

## How to apply

Parse the alg_genes parameter from params_genes.yml (default 'edger') to select the statistical algorithm. Load the preprocessed count matrix and samplesheet, then validate that required metadata columns match the chosen algorithm: edgeR uses 'condition' for grouping and accepts custom formula/contrasts; DESeq2 requires columns named exactly 'condition' and 'batch'; RankProduct requires a 'cl' column coded as 0 (control) or 1 (treatment). Execute the selected R package (DESeq2, edgeR, or RankProd) on the count matrix using the sample group assignments. Generate a results table with feature identifiers, fold-changes, test statistics (log2FC, LFC SE, or rank statistics depending on algorithm), raw p-values, and adjusted p-values (Benjamini-Hochberg correction). Create diagnostic plots (volcano plot, MA plot, p-value distribution histogram) using ggplot2 and ComplexHeatmap to assess overall significance distribution and identify potential artifacts.

## Related tools

- **edgeR** (R package for negative-binomial statistical model fitting; supports custom contrasts and flexible formula specification for differential expression testing)
- **DESeq2** (R package for negative-binomial generalized linear model fitting with strict samplesheet column naming requirements ('condition', 'batch') for group and batch effect specification)
- **RankProd** (R package for rank-product non-parametric differential expression testing; requires binary 'cl' column (0/1 control/treatment coding))
- **ggplot2** (R package for generating volcano, MA, and p-value distribution diagnostic plots)
- **ComplexHeatmap** (R package for rendering annotated heatmaps of top differentially expressed features with sample and feature metadata)

## Evaluation signals

- Results table contains exactly one row per input feature with non-null fold-change, test statistic, p-value, and adjusted p-value columns; no rows are missing or duplicated.
- Adjusted p-values (FDR or BH correction) are monotonically non-decreasing when sorted by raw p-value; adjusted p-value ≥ raw p-value for all features.
- Volcano plot shows features with |log2FC| > threshold and -log10(p-value) > threshold in upper quadrants; MA plot shows asymmetric variance as a function of mean abundance, consistent with count-level noise.
- P-value distribution histogram is approximately uniform under the null (flat distribution for non-DE features) with a spike near zero for significant DE features; distribution does not show heavy left-skew suggesting p-value computation errors.
- Top differentially expressed features identified by each algorithm (e.g., FDR < 0.05, |log2FC| > 1) are biologically plausible and validated against samplesheet grouping; no features show contradictory fold-changes across replicates within the same condition.

## Limitations

- edgeR, DESeq2, and RankProduct assume that replicates within a group follow similar distributional assumptions; violations (e.g., outlier samples, batch effects not captured in metadata) can inflate or deflate test statistics.
- DESeq2 and edgeR require a minimum count threshold per feature to avoid numeric instability; features with very low counts across all samples may be filtered out automatically or produce unreliable estimates.
- RankProduct loses information by ranking counts rather than modeling counts directly; it is less powerful than model-based methods (edgeR, DESeq2) when effect sizes are small relative to variance.
- All three algorithms assume independence of samples; longitudinal or repeated-measures designs require specialized model formulas or blocking strategies not fully documented in the pipeline.
- The pipeline does not automatically check for confounders or hidden batch effects in count data; users must verify that samplesheet metadata (condition, batch, cl columns) fully capture known experimental factors.

## Evidence

- [other] The pipeline implements dispatched differential expression analysis where users specify the algorithm via the alg_genes parameter in params_genes.yml (defaulting to 'edger'): "Parse the alg_genes parameter from params_genes.yml (default 'edger') to select the differential expression algorithm."
- [other] Each algorithm requires specific samplesheet column conventions: edgeR uses 'condition' for grouping and accepts custom formula/contrasts; DESeq2 requires columns named exactly 'condition' and 'batch'; RankProduct requires a 'cl' column with 0 for controls and 1 for treatments: "edgeR uses 'condition' for grouping and accepts custom formula/contrasts; DESeq2 requires columns named exactly 'condition' and 'batch'; RankProduct requires a 'cl' column with 0 for controls and 1"
- [other] Generate a results table containing feature identifiers, fold-changes, test statistics, raw p-values, and adjusted p-values: "Generate a results table containing feature identifiers, fold-changes, test statistics, raw p-values, and adjusted p-values."
- [other] Create diagnostic plots using ggplot2 and ComplexHeatmap: "Create diagnostic plots (volcano plot, MA plot, p-value distribution) using ggplot2 and ComplexHeatmap."
- [readme] The pipeline is built using Nextflow version 23.04.2.5870 and uses Docker/Singularity containers for reproducibility: "The pipeline is built using [Nextflow](https://www.nextflow.io) version 23.04.2.5870 (IMPORTANT), a workflow tool to run tasks across multiple compute infrastructures"
