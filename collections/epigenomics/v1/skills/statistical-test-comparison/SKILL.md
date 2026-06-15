---
name: statistical-test-comparison
description: Use when when you have run differential methylation analysis in methylKit and need to validate whether overdispersion correction (overdispersion='MN') produces appropriately stringent statistical tests.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3295
  - http://edamontology.org/topic_3674
  tools:
  - R
  - methylKit
  - Bismark
  - MethylDackel
derived_from:
- doi: 10.1186/gb-2012-13-10-r87
  title: methylkit
evidence_spans:
- packageVersion('methylKit')
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_methylkit
    doi: 10.1186/gb-2012-13-10-r87
    title: methylkit
  dedup_kept_from: coll_methylkit
schema_version: 0.2.0
---

# statistical-test-comparison

## Summary

Compare statistical test stringency and multiple-testing correction outcomes (q-value distributions, test type, variance adjustment) between corrected and uncorrected differential methylation analyses to verify that overdispersion correction produces more conservative significance thresholds.

## When to use

When you have run differential methylation analysis in methylKit and need to validate whether overdispersion correction (overdispersion='MN') produces appropriately stringent statistical tests. Apply this skill when comparing a corrected run (with overdispersion='MN' and test='Chisq') against a parallel uncorrected baseline (overdispersion=FALSE) to confirm the correction adjusts variance for excess dispersion and makes p-value/q-value thresholds more conservative.

## When NOT to use

- Input methylBase object has <3 replicates per group — Fisher's exact test (not logistic regression or F-test) will be used, and overdispersion correction assumptions may not hold.
- Samples have already been filtered to remove low-coverage bases or PCR bias artifacts — comparison may conflate the effects of coverage filtering with overdispersion correction.
- Goal is exploratory rather than hypothesis-testing — a single uncorrected run may suffice; side-by-side comparison adds computational burden without validation value.

## Inputs

- methylBase object (unified methylation data across samples and sites)
- methylKit R package with dataSim() simulation or imported bisulfite sequencing data

## Outputs

- q-value distribution from overdispersion='MN' corrected run
- q-value distribution from uncorrected (overdispersion=FALSE) baseline run
- comparative summary statistics (mean, median, range of q-values per method)
- count of significantly differential sites at fixed q-value threshold (e.g., q < 0.01) per method

## How to apply

Execute calculateDiffMeth() on a unified methylBase object twice: once with overdispersion='MN' and test='Chisq', and once with overdispersion=FALSE (or default uncorrected mode). Extract the q-value distributions from both runs and compare their central tendencies, ranges, and proportions of sites passing a common significance cutoff (e.g., q < 0.01). The overdispersion='MN' mode applies a scaling parameter φ = X²/(N−P) to adjust variance as φ·n_i·π̂_i·(1−π̂_i), and automatically switches to an F-test from Chi-square, which should result in higher (more stringent) q-values on average. Verify that the corrected method produces visibly elevated median and mean q-values and a smaller proportion of sites meeting a fixed q-value threshold compared to the uncorrected baseline.

## Related tools

- **methylKit** (R package providing calculateDiffMeth(), dataSim(), and methylBase objects for differential methylation analysis with tunable overdispersion correction) — https://github.com/al2na/methylKit
- **Bismark** (Bisulfite sequencing mapper and methylation caller; produces alignment files that feed into methylKit via methRead()) — https://github.com/FelixKrueger/Bismark
- **MethylDackel** (Alternative methylation metrics extractor from BAM/CRAM files; output can be converted to methylKit-compatible format) — https://github.com/dpryan79/MethylDackel

## Examples

```
# Generate simulated methylBase; compare overdispersion-corrected vs. uncorrected
library(methylKit)
mBase <- dataSim(replicates=6, sites=1000, treatment=c(1,1,1,0,0,0))
mDiff_corrected <- calculateDiffMeth(mBase, overdispersion='MN', test='Chisq')
mDiff_uncorrected <- calculateDiffMeth(mBase, overdispersion=FALSE, test='Chisq')
# Extract and compare q-value distributions
qvals_corr <- mDiff_corrected@data$qvalue
qvals_uncorr <- mDiff_uncorrected@data$qvalue
print(c(mean(qvals_corr), mean(qvals_uncorr)))  # Should show higher mean for corrected
```

## Evaluation signals

- Mean and median q-values from overdispersion='MN' run are visibly higher (more stringent) than uncorrected baseline, indicating variance inflation correction is active.
- Proportion of sites passing a fixed q-value threshold (e.g., q < 0.01) is smaller in the overdispersion='MN' run, confirming more conservative multiple-testing correction.
- Overdispersion='MN' run automatically uses F-test instead of Chi-square test, which can be verified by inspecting the internal test statistic column or by checking that the number of distinct q-value magnitudes differs from uncorrected output.
- Scaling parameter φ is >1 for the majority of sites, confirming that variance adjustment is being applied (φ represents excess variance relative to binomial expectation).
- Q-value rank order is largely preserved between corrected and uncorrected runs (i.e., top differentially methylated sites remain concordant), indicating the correction refines stringency without reversing relative significance.

## Limitations

- Overdispersion correction assumes that observed variance exceeds binomial expectations; if data are underdispersed or binomially distributed, the correction may over-penalize significance and yield false negatives.
- Comparison is most informative when sample sizes are ≥3 per group; with very small sample numbers, Fisher's exact test is used instead of logistic regression, and overdispersion correction is not applicable.
- The choice of q-value threshold (e.g., 0.01 vs. 0.05) affects the magnitude of difference observed between corrected and uncorrected runs; a threshold too permissive may obscure the correction's effect, while too stringent may yield too few differentially methylated sites for robust comparison.
- Simulated data from dataSim() may not fully capture the complexity of real bisulfite sequencing artifacts (e.g., C-to-T conversion bias, strand asymmetry), so validation on empirical data is recommended.

## Evidence

- [other] The calculateDiffMeth() function with overdispersion='MN' parameter calculates a scaling parameter φ = X²/(N-P) to adjust variance as φ·n_i·π̂_i·(1-π̂_i), which makes statistical tests more stringent by correcting for variance in excess of binomial expectations and automatically switches from Chisq to F-test.: "calculateDiffMeth() function with overdispersion='MN' parameter calculates a scaling parameter φ = X²/(N-P) to adjust variance as φ·n_i·π̂_i·(1−π̂_i), which makes statistical tests more stringent by"
- [intro] After q-value calculation, we can select the differentially methylated regions/bases based on q-value and percent methylation difference cutoffs.: "After q-value calculation, we can select the differentially methylated regions/bases based on q-value and percent methylation difference cutoffs"
- [intro] The calculateDiffMeth() function is the main function to calculate differential methylation. Depending on the sample size per each set it will either use Fisher's exact or logistic regression.: "The calculateDiffMeth() function is the main function to calculate differential methylation. Depending on the sample size per each set it will either use Fisher's exact or logistic regression"
- [intro] We start by reading in the methylation call data from bisulfite sequencing with methRead function. Reading in the data this way will return a methylRawList object.: "We start by reading in the methylation call data from bisulfite sequencing with methRead function. Reading in the data this way will return a methylRawList object"
- [readme] methylKit is an R package for DNA methylation analysis and annotation from high-throughput bisulfite sequencing.: "methylKit is an R package for DNA methylation analysis and annotation from high-throughput bisulfite sequencing"
