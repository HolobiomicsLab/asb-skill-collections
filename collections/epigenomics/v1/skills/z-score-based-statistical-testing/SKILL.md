---
name: z-score-based-statistical-testing
description: Use when you have a sparse chromatin accessibility matrix (ATAC-seq or DNAse-seq counts per peak per sample), matched peak-annotation assignments (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0749
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_0621
  tools:
  - chromVAR
  - R
  - SummarizedExperiment
  - motifmatchr
  - BiocParallel
  - BSgenome.Hsapiens.UCSC.hg19
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

# z-score-based-statistical-testing

## Summary

Compute z-score deviations for genomic annotations (motifs, kmers) in sparse chromatin accessibility data, then apply statistical hypothesis testing and bootstrapped confidence intervals to rank annotations by variability and identify significant differential usage across sample groups or cell types.

## When to use

You have a sparse chromatin accessibility matrix (ATAC-seq or DNAse-seq counts per peak per sample), matched peak-annotation assignments (e.g., which peaks contain which transcription factor motifs from JASPAR), and you want to rank annotations by their association with variability in accessibility, or test whether annotation deviations differ significantly between two or more cell types or experimental conditions.

## When NOT to use

- Input is already a pre-computed feature-by-sample matrix (not raw counts with peak and annotation information)—use dimensionality reduction or clustering directly instead.
- You lack matched peak-to-annotation assignments (e.g., no motif positions or kmer matches); compute those first using motifmatchr.
- Your data is not sparse or depth-normalized (e.g., bulk RNA-seq with high counts); chromVAR is designed for sparse, count-based chromatin accessibility data.

## Inputs

- SummarizedExperiment with chromatin accessibility counts (rows = peaks, columns = samples/cells), GC-bias-corrected
- Peak-annotation match matrix (e.g., logical matrix from matchMotifs indicating which peaks contain which JASPAR motifs)
- Sample colData with grouping variable (e.g., Cell_Type with levels GM, H1)

## Outputs

- Variability scores and bootstrap confidence intervals per annotation, ranked by standard deviation of z-scores
- Visualization of rank-sorted annotations by variability (e.g., from plotVariability)
- Differential-deviation test results table (p-values, effect sizes, bias-corrected mean deviations per annotation per group)

## How to apply

Load the chromatin accessibility counts as a SummarizedExperiment with GC-bias correction applied. Match motifs or other annotations to peaks using motifmatchr. Call computeDeviations() to generate a deviation matrix (z-scores) where each cell/sample and annotation pair is scored by how much that annotation's peak accessibility deviates from the expected background, controlling for sequencing depth and GC content. Next, call computeVariability() to compute the standard deviation of z-scores across all samples for each annotation and generate bootstrap confidence intervals by resampling cells/samples; this ranks annotations by their variability score. For differential testing between groups (e.g., GM vs. H1 cell types), call differentialDeviations() which tests whether the bias-corrected mean deviations differ significantly between groups using the sample-level colData annotation. Export both the ranked variability table and the differential-deviation test results (p-values, effect sizes) as structured tables for downstream interpretation.

## Related tools

- **chromVAR** (Primary R package providing computeDeviations(), computeVariability(), differentialDeviations(), and plotVariability() functions for z-score deviation computation, variability ranking, and differential testing) — https://github.com/GreenleafLab/chromVAR
- **motifmatchr** (R package that matches JASPAR motifs (or other PWMs) to genomic peaks, producing the peak-annotation matrix fed into computeDeviations()) — https://github.com/GreenleafLab/motifmatchr
- **SummarizedExperiment** (Data container class for storing chromatin accessibility counts, peak annotations, and sample metadata (colData))
- **BiocParallel** (Enables parallelization of bootstrap resampling and hypothesis testing across annotations)
- **BSgenome.Hsapiens.UCSC.hg19** (Provides genome sequence for GC-bias computation in addGCBias() preprocessing step)
- **SnapATAC** (Downstream method that integrates chromVAR for motif analysis within single-cell ATAC-seq clustering and annotation workflows) — https://github.com/r3fang/SnapATAC

## Examples

```
library(chromVAR); data(example_counts, package = "chromVAR"); counts_filtered <- filterSamples(example_counts, min_depth = 1500, min_in_peaks = 0.15); motifs <- getJasparMotifs(); motif_ix <- matchMotifs(motifs, counts_filtered, genome = BSgenome.Hsapiens.UCSC.hg19); dev <- computeDeviations(object = counts_filtered, annotations = motif_ix); variability <- computeVariability(dev); diff_dev <- differentialDeviations(dev, "Cell_Type")
```

## Evaluation signals

- Verify that z-score deviations have mean ≈ 0 and standard deviation ≈ 1 across samples (by design, deviations are normalized); check for outliers that may indicate data quality issues.
- Confirm that bootstrap confidence intervals for variability scores contain the point estimate and have reasonable width (not zero, not implausibly wide).
- Verify that differentialDeviations() p-values are between 0 and 1, and that effect sizes are consistent in sign and magnitude with the observed mean deviations per group.
- Check that ranked variability table is sorted monotonically by variability score; spot-check top-ranked and bottom-ranked annotations for biological plausibility (e.g., known cell-type-specific TFs should appear in differential results for appropriate cell types).
- Ensure that the structured output tables have correct dimensions (annotations × 1 column for variability; annotations × group-specific columns for differential results) and no missing or infinite values.

## Limitations

- chromVAR clustering performance is outperformed by newer methods such as SnapATAC; this skill is better suited for motif annotation and variability ranking than for cell-type discovery itself.
- The method assumes sparse count data with sufficient depth (>1500 reads recommended per sample after filtering); samples below minimum depth must be filtered out a priori using filterSamples().
- Variability and differential-deviation inference depend on the quality of the peak-annotation matches (motifmatchr); weak or incorrect motif calls will propagate into noisy z-scores.
- Bootstrap confidence intervals and p-values assume exchangeable sampling of cells/samples; batch effects or technical confounders can inflate or deflate significance estimates and should be corrected before analysis.

## Evidence

- [other] chromVAR is designed to identify motifs or other genomic annotations associated with variability in chromatin accessibility between individual cells or samples: "chromVAR is designed to identify motifs or other genomic annotations associated with variability in chromatin accessibility between individual cells or samples, enabling ranking and differential"
- [other] computeVariability generates bootstrap confidence intervals and performs hypothesis tests: "Call computeVariability(dev) to compute standard deviation of z-scores across samples for each motif, generate bootstrap confidence intervals by resampling cells/samples, and perform hypothesis tests"
- [other] differentialDeviations tests for significant differences in deviations between cell types: "Call differentialDeviations(dev, "Cell_Type") to test for significant differences in bias-corrected deviations between GM and H1 cell groups using the colData cell-type annotation."
- [readme] chromVAR is an R package for sparse chromatin accessibility analysis: "chromVAR is an R package for the analysis of sparse chromatin accessibility data from single cell or bulk ATAC or DNAse-seq data."
- [readme] computeDeviations returns a SummarizedExperiment with assays of deviations: "The function `computeDeviations` returns a SummarizedExperiment with two "assays""
- [readme] Filtering samples and peaks improves downstream analysis: "it is advisable to filter out samples with insufficient reads using filterSamples"
