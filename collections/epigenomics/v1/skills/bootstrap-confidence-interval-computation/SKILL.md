---
name: bootstrap-confidence-interval-computation
description: Use when when you have computed z-score deviations for genomic annotations (e.g., motifs) across multiple cells or samples and need to quantify uncertainty in their variability rankings before performing differential or comparative analyses.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3928
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_0654
  - http://edamontology.org/topic_3179
  tools:
  - chromVAR
  - R
  - SummarizedExperiment
  - BiocParallel
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

# bootstrap-confidence-interval-computation

## Summary

Compute bootstrap confidence intervals around variability metrics (e.g., standard deviations of z-scores) for genomic annotations by resampling cells or samples with replacement. This skill provides uncertainty quantification for ranking and hypothesis testing of motif variability across chromatin accessibility datasets.

## When to use

When you have computed z-score deviations for genomic annotations (e.g., motifs) across multiple cells or samples and need to quantify uncertainty in their variability rankings before performing differential or comparative analyses. Use this when sample size is small or variability estimates may be unstable.

## When NOT to use

- Input is already a pre-computed confidence interval table or posterior distribution — do not resample.
- Sample size is very large (n >> 1000) and asymptotic methods are more efficient.
- Variability is computed on aggregated bulk data with no cell/sample structure to resample.

## Inputs

- chromVARDeviations object (bias-corrected z-score deviations for annotations × samples)
- Variability metric (standard deviation of z-scores per annotation)
- Annotation labels (e.g., motif IDs)
- Sample/cell metadata (colData)

## Outputs

- Bootstrap confidence intervals (lower and upper bounds per annotation)
- Bootstrap replicate distributions (variability scores across resamples)
- Ranked annotations by variability with uncertainty bands

## How to apply

After computing variability scores (e.g., standard deviation of z-scores across samples for each motif), resample cells or samples with replacement multiple times (bootstrap replicates) to recompute the variability metric for each annotation in each replicate. Collect the distribution of bootstrap estimates and compute percentile-based confidence intervals (e.g., 2.5th and 97.5th percentiles for 95% CI). These intervals quantify the range of plausible variability values and support downstream hypothesis testing against a null variability threshold (e.g., 1.0 for normalized deviations).

## Related tools

- **chromVAR** (Core R package providing computeVariability() function to compute standard deviation of z-scores and bootstrap confidence intervals for motif variability) — https://github.com/GreenleafLab/chromVAR
- **SummarizedExperiment** (Data structure container for storing chromVARDeviations object with assays (z-scores) and colData (sample annotations))
- **BiocParallel** (Enables parallelized bootstrap resampling across multiple cores for computational efficiency)

## Examples

```
dev <- computeVariability(dev); variability <- dev@metadata$variability; ci_lower <- apply(dev@metadata$bootstrap_replicates, 1, quantile, 0.025); ci_upper <- apply(dev@metadata$bootstrap_replicates, 1, quantile, 0.975)
```

## Evaluation signals

- Bootstrap confidence intervals are non-empty and bounded (lower < upper) for all annotations
- Interval width decreases monotonically or stays stable as the number of bootstrap replicates increases (convergence)
- Annotations with higher point variability estimates have wider confidence intervals (proportional uncertainty)
- Null hypothesis significance (p-value) is consistent with whether confidence interval excludes null variability threshold (e.g., 1.0)
- Visual check: plotVariability() output shows confidence bands around ranked motifs; bands should not overlap implausibly for top-ranked vs. bottom-ranked annotations

## Limitations

- Bootstrap assumes samples/cells are exchangeable; violation (e.g., batch effects, pseudo-replicates) inflates or deflates intervals.
- Percentile-based confidence intervals can be biased for skewed distributions; bias-corrected methods (BCa) may be needed for small sample sizes.
- Computational cost scales with number of bootstrap replicates and annotation count; 1000+ replicates recommended but may be slow for >10,000 annotations.
- Does not account for spatial or temporal structure in the data; independent resampling assumes i.i.d. samples.

## Evidence

- [other] Variability computation with bootstrap: "Call computeVariability(dev) to compute standard deviation of z-scores across samples for each motif, generate bootstrap confidence intervals by resampling cells/samples"
- [readme] chromVAR package purpose: "chromVAR is an R package for the analysis of sparse chromatin accessibility data from single cell or bulk ATAC or DNAse-seq data"
- [other] Hypothesis testing context: "perform hypothesis tests against null variability of 1"
- [readme] Annotation identification: "aims to identify motifs or other genomic annotations associated with variability in chromatin accessibility between individual cells or samples"
