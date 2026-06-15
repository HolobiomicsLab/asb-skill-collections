---
name: differential-chromatin-accessibility-analysis-between-cell-types
description: Use when you have pre-processed chromatin accessibility data (ATAC-seq or DNAse-seq) with chromVAR deviations already computed for individual cells or bulk samples across multiple cell types or conditions, and you need to identify which transcription factor motifs exhibit significant differential.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3945
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_0749
  tools:
  - chromVAR
  - R
  - SummarizedExperiment
  - motifmatchr
  - BiocParallel
  - SnapATAC
derived_from:
- doi: 10.1038/nmeth.4401
  title: chromvar
evidence_spans:
- chromVAR is an R package for the analysis of sparse chromatin accessibility
- computeVariability(dev)
- An R package for the analysis of sparse chromatin accessibility
- library(chromVAR)
- library(SummarizedExperiment)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_chromvar
    doi: 10.1038/nmeth.4401
    title: chromvar
  dedup_kept_from: coll_chromvar
schema_version: 0.2.0
---

# differential-chromatin-accessibility-analysis-between-cell-types

## Summary

Identify transcription factor motifs showing statistically significant differences in chromatin accessibility bias between distinct cell populations (e.g., GM vs. H1 cell lines) using chromVAR's differential-deviation framework. This skill enables ranking motifs by their variability in accessibility and detecting cell-type-specific regulatory patterns.

## When to use

You have pre-processed chromatin accessibility data (ATAC-seq or DNAse-seq) with chromVAR deviations already computed for individual cells or bulk samples across multiple cell types or conditions, and you need to identify which transcription factor motifs exhibit significant differential bias or usage patterns between those populations.

## When NOT to use

- Input is raw BAM files or peak counts: must first apply filterSamples, filterPeaks, addGCBias, and computeDeviations to obtain a valid chromVARDeviations object.
- Cell-type or grouping annotation is absent or misaligned in colData: differentialDeviations requires a valid categorical grouping variable in the SummarizedExperiment colData.
- You are performing unsupervised clustering of cells: chromVAR's primary strength for clustering is k-mers + PCA; SnapATAC outperforms chromVAR for clustering tasks according to benchmarks.

## Inputs

- chromVARDeviations object with z-score deviations for motifs across samples
- colData annotation specifying cell-type or condition grouping for each sample
- JASPAR motif matches (from matchMotifs step)

## Outputs

- variability scores (standard deviation of z-scores) with bootstrap confidence intervals per motif
- differential-deviation test statistics (p-values, effect sizes, bias-corrected deviation estimates) per motif between cell types
- Ranked motif lists sorted by variability or differential significance
- Visualization plots (rank-sorted variability profiles and differential-deviation heatmaps)

## How to apply

Start with a pre-computed chromVARDeviations object (dev) derived from filtered counts and matched JASPAR motifs. First, call computeVariability(dev) to generate per-motif standard deviation of z-scores across samples and bootstrap confidence intervals to establish baseline variability. Then call differentialDeviations(dev, grouping_column) where grouping_column specifies the cell-type annotation in colData (e.g., 'Cell_Type' with values 'GM' and 'H1') to perform hypothesis tests of bias-corrected deviations between groups. The function generates p-values and effect sizes per motif; apply a multiple-testing correction threshold (e.g., adjusted p < 0.05) to prioritize significant hits. Export ranked variability scores and differential-deviation test results as structured tables for downstream interpretation and visualization.

## Related tools

- **chromVAR** (Core R package that computes deviations and performs differential-deviation testing between cell-type groups) — https://github.com/GreenleafLab/chromVAR
- **motifmatchr** (Matches JASPAR motifs to peaks prior to deviation computation) — https://github.com/GreenleafLab/motifmatchr
- **SummarizedExperiment** (Container class for storing counts, colData (cell-type annotations), and chromVAR results)
- **BiocParallel** (Enables parallelized computation of deviations and differential tests across multiple cores)
- **SnapATAC** (Alternative method for single-cell ATAC-seq analysis; integrates chromVAR for motif annotation in clustered cells) — https://github.com/r3fang/SnapATAC

## Examples

```
dev <- computeDeviations(object = counts_filtered, annotations = motif_ix); variability <- computeVariability(dev); diff_dev <- differentialDeviations(dev, "Cell_Type")
```

## Evaluation signals

- Variability scores (standard deviations) are computed for all motifs and rank-sorted; bootstrap confidence intervals show non-zero width, indicating statistical uncertainty is quantified.
- Differential-deviation p-values are computed between all specified cell-type pairs, with multiple-testing correction applied (e.g., FDR or Bonferroni); no NAs or Inf values in test statistics.
- Effect sizes (bias-corrected deviation differences) are reported per motif and show expected direction and magnitude (typically in z-score units or log-odds scale).
- Motifs with adjusted p-value < 0.05 (or user-specified threshold) are reliably identified and can be validated against known cell-type-specific transcription factors.
- Visualization plots (e.g., rank-sorted variability scatter plots, heatmaps of differential deviations) display expected patterns: high-variability motifs clustered at the extremes, cell-type-specific motifs showing distinct color patterns between groups.

## Limitations

- chromVAR assumes chromatin accessibility is driven primarily by transcription factor binding; does not account for other regulatory mechanisms (e.g., nucleosome positioning, chromatin looping).
- Performance degrades with very sparse data; filterSamples and filterPeaks are required to remove low-coverage samples and non-overlapping peak artifacts, which may remove biologically relevant signal in rare cell types.
- Clustering-based applications of chromVAR are outperformed by newer methods such as SnapATAC; the differential-deviation framework is better suited for annotation and ranking than for unsupervised discovery.
- Bootstrap confidence intervals require sufficient resampling iterations; default parameters may underestimate uncertainty if cell counts per type are very low (<10 cells).
- No changelog available; version compatibility and parameter stability across releases are not formally documented.

## Evidence

- [other] differentialDeviations function and use case: "Call differentialDeviations(dev, "Cell_Type") to test for significant differences in bias-corrected deviations between GM and H1 cell groups using the colData cell-type annotation."
- [other] variability computation and ranking: "Call computeVariability(dev) to compute standard deviation of z-scores across samples for each motif, generate bootstrap confidence intervals by resampling cells/samples, and perform hypothesis tests"
- [other] output exports: "Export ranked variability results and differential-deviation test results (p-values, effect sizes per motif) as structured tables."
- [readme] core chromVAR purpose: "chromVAR is designed to identify motifs or other genomic annotations associated with variability in chromatin accessibility between individual cells or samples"
- [readme] clustering performance caveat: "newer methods such as SnapATAC outperform chromVAR for the clustering tasks evaluated in the paper"
