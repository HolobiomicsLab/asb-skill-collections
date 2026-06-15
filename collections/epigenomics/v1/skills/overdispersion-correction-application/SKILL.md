---
name: overdispersion-correction-application
description: Use when analyzing differential methylation from bisulfite sequencing data where you suspect overdispersion (variance exceeds binomial expectations), or when comparing uncorrected and corrected statistical tests to determine whether more stringent thresholds are justified by the data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3658
  edam_topics:
  - http://edamontology.org/topic_3295
  - http://edamontology.org/topic_0654
  - http://edamontology.org/topic_2269
  tools:
  - R
  - methylKit
  - Bismark
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

# overdispersion-correction-application

## Summary

Apply overdispersion correction in methylKit's calculateDiffMeth() function using the 'MN' (Methylation-specific Negative Binomial) parameter to adjust for variance in excess of binomial expectations, producing more stringent p-value and q-value distributions in differential methylation analysis. This skill is essential when methylation count data exhibit greater variance than expected under a binomial model, which is common in bisulfite sequencing due to biological and technical sources of variation.

## When to use

Apply this skill when analyzing differential methylation from bisulfite sequencing data where you suspect overdispersion (variance exceeds binomial expectations), or when comparing uncorrected and corrected statistical tests to determine whether more stringent thresholds are justified by the data. Use it specifically when working with methylBase objects from methylKit and seeking to adjust variance estimates as φ·n_i·π̂_i·(1-π̂_i), where φ = X²/(N-P) is the scaling parameter computed from Chi-square test residuals.

## When NOT to use

- When input data are already aggregated at regional or tiling-window level rather than single-base resolution; overdispersion correction is designed for individual base-pair methylation counts.
- When sample size is very small (< 3 replicates per group); the overdispersion parameter estimation becomes unstable with insufficient degrees of freedom.
- When the research question explicitly requires nominal p-values or when multiple-testing correction has already been applied at an earlier filtering stage (e.g., pre-filtering to high-variance sites).

## Inputs

- methylBase object (merged methylation data across samples at consistent genomic positions)
- Sample grouping/treatment assignment for differential methylation comparison

## Outputs

- Differential methylation results with variance-corrected test statistics and q-values
- Overdispersion scaling parameter φ (X²/(N-P))
- Q-value distribution (higher in corrected vs. uncorrected analyses)

## How to apply

Generate a simulated or real methylBase object using methylKit's methRead() and unite() functions to ensure consistent base coverage across samples. Execute calculateDiffMeth() on the methylBase object with overdispersion parameter set to 'MN' (Methylation-specific Negative Binomial) and test parameter set to 'Chisq'. The function automatically computes the overdispersion scaling parameter φ and recalculates variance-adjusted test statistics; notably, it switches from Chi-square to F-test when overdispersion correction is applied. Extract and compare q-value distributions from the corrected run (overdispersion='MN') against a parallel uncorrected run (overdispersion=FALSE or default) to verify that corrected tests produce higher average q-values, confirming more stringent multiple-testing correction.

## Related tools

- **methylKit** (R package providing calculateDiffMeth() function with overdispersion='MN' parameter and dataSim() for generating simulated methylBase objects) — https://github.com/al2na/methylKit
- **Bismark** (Upstream tool for bisulfite sequencing alignment and methylation calling whose output (cytosine methylation reports) can be read into methylKit via methRead()) — https://github.com/FelixKrueger/Bismark
- **R** (Execution environment for methylKit and statistical analysis)

## Examples

```
library(methylKit); meth <- dataSim(replicates=6, sites=1000); diff_corrected <- calculateDiffMeth(meth, overdispersion='MN', test='Chisq'); diff_uncorrected <- calculateDiffMeth(meth, overdispersion=FALSE, test='Chisq'); summary(diff_corrected@.Data$qvalue) # compare to summary(diff_uncorrected@.Data$qvalue)
```

## Evaluation signals

- Q-value distribution from overdispersion-corrected run (overdispersion='MN') is shifted toward higher values compared to uncorrected run (overdispersion=FALSE), indicating more stringent multiple-testing correction.
- Overdispersion scaling parameter φ is computed and reported; values φ > 1 indicate underdispersion was corrected, φ ≈ 1 indicates binomial assumptions were adequate.
- Test statistic type switches from Chi-square to F-test when overdispersion='MN' is applied, confirming that variance adjustment recalibrated the null distribution.
- Number of significantly differentially methylated bases/regions (at fixed q-value and percent-methylation-difference thresholds) is reduced in the corrected analysis compared to uncorrected, reflecting the more conservative thresholds.
- Comparison of raw test statistics (e.g., X² or F) between corrected and uncorrected runs shows expected increase in test statistic magnitude when variance is properly adjusted.

## Limitations

- Overdispersion correction requires sufficient replicates per group and genomic coverage to reliably estimate the scaling parameter φ; with very low coverage or few replicates, estimates become unstable.
- The 'MN' overdispersion model assumes a specific variance structure; if true variance deviates from φ·n_i·π̂_i·(1-π̂_i), the correction may be suboptimal or mask unmeasured sources of variation.
- Switching from Chi-square to F-test changes the null distribution; practitioners must ensure downstream software and interpretation protocols account for this change in test type and degrees of freedom.
- High average q-values from overdispersion correction can result in very few or no differentially methylated regions being reported, which may reflect overly conservative correction if overdispersion estimates are inflated by outliers or batch effects not removed beforehand.

## Evidence

- [other] calculateDiffMeth() function with overdispersion='MN' parameter calculates a scaling parameter φ = X²/(N-P) to adjust variance as φ·n_i·π̂_i·(1-π̂_i), which makes statistical tests more stringent: "calculateDiffMeth() function with overdispersion='MN' parameter calculates a scaling parameter φ = X²/(N-P) to adjust variance as φ·n_i·π̂_i·(1-π̂_i), which makes statistical tests more stringent by"
- [other] Overdispersion correction produces higher q-values in corrected vs. uncorrected runs: "Extract and compare the q-value distributions from the corrected run (overdispersion='MN') against a parallel uncorrected run (overdispersion=FALSE or default) to verify that the corrected method"
- [readme] methylKit is an R package for DNA methylation analysis from high-throughput bisulfite sequencing: "methylKit is an R package for DNA methylation analysis and annotation from high-throughput bisulfite sequencing. The package is designed to deal with sequencing data from RRBS and its variants, but"
- [intro] calculateDiffMeth() is the main function for differential methylation calculation: "The calculateDiffMeth() function is the main function to calculate differential methylation. Depending on the sample size per each set it will either use Fisher's exact or logistic regression"
- [other] dataSim() function generates simulated methylBase objects for testing: "Generate a simulated methylBase object using methylKit's dataSim() function with parameters set to 6 replicates and 1000 methylation sites."
