---
name: simulation-based-validation
description: Use when when you need to verify that a statistical correction (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3295
  - http://edamontology.org/topic_3673
  tools:
  - R
  - methylKit
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

# simulation-based-validation

## Summary

Generate synthetic methylation data using dataSim() to benchmark and validate statistical methods such as overdispersion-corrected differential methylation analysis. This skill enables controlled testing of analysis parameters and their effects on stringency and accuracy before applying methods to real data.

## When to use

When you need to verify that a statistical correction (e.g., overdispersion adjustment in calculateDiffMeth with overdispersion='MN') produces expected changes in test stringency, or when you want to validate that a new analysis workflow produces correct q-value distributions and variance adjustments under known ground-truth conditions.

## When NOT to use

- When you have sufficient real experimental replicates and real biological effect sizes — simulation is no substitute for validation on actual data with true biological variance.
- When your primary goal is differential methylation discovery on real samples — simulation-based validation is a method-vetting step, not a substitute for direct analysis.
- When computational resources are severely constrained and you must prioritize analysis speed over methodological validation.

## Inputs

- methylKit dataSim() parameters (number of replicates, number of methylation sites)
- methylBase object (simulated or real methylation data with coverage and methylation percentage columns)

## Outputs

- methylDiff object with q-values and test statistics from uncorrected run
- methylDiff object with q-values and test statistics from corrected run (overdispersion='MN')
- q-value distribution comparison (mean, median, and percentile values)

## How to apply

Use methylKit's dataSim() function to generate a synthetic methylBase object with controlled parameters (e.g., 6 replicates and 1000 methylation sites). Run calculateDiffMeth() on this object twice: once with your method of interest (e.g., overdispersion='MN' with test='Chisq') and once with a baseline uncorrected configuration (overdispersion=FALSE or default). Extract and compare the resulting q-value distributions between runs to verify that the corrected method produces higher average q-values (more stringent multiple-testing correction) and that the variance adjustment factor φ = X²/(N-P) is correctly applied, confirming the expected shift from Chi-square to F-test behavior.

## Related tools

- **methylKit** (Core R package providing dataSim() function for synthetic methylation data generation and calculateDiffMeth() for differential methylation analysis with overdispersion correction) — https://github.com/al2na/methylKit
- **R** (Runtime environment for executing methylKit functions and statistical comparisons)

## Examples

```
library(methylKit); sim <- dataSim(replicates=6, sites=1000); diff_corrected <- calculateDiffMeth(sim, overdispersion='MN', test='Chisq'); diff_uncorrected <- calculateDiffMeth(sim, overdispersion=FALSE, test='Chisq'); mean(diff_corrected@data$qvalue); mean(diff_uncorrected@data$qvalue)
```

## Evaluation signals

- Mean q-value from overdispersion-corrected run (overdispersion='MN') is higher than uncorrected baseline, confirming more stringent multiple-testing correction
- Statistical test automatically switches from Chi-square (uncorrected) to F-test (corrected with overdispersion='MN'), verifiable via test statistic type in methylDiff object
- Variance scaling factor φ = X²/(N-P) is applied only in the corrected run, evidenced by larger denominator in test statistic calculation
- Q-value distribution shift is consistent across the full range of methylation percentages (not an artifact of a few extreme sites)
- Simulated data with known effect sizes confirms that corrected method maintains or improves specificity while adjusting for overdispersion relative to binomial expectations

## Limitations

- Simulated data from dataSim() may not capture all real-world sources of variance and batch effects present in actual bisulfite-seq experiments.
- Validation on simulation alone does not guarantee equivalent performance on real data with complex sample heterogeneity, sequencing errors, or technical biases.
- The overdispersion='MN' correction assumes methylation-specific negative binomial distribution; if your data violates this assumption, validation results may not transfer to real analysis.

## Evidence

- [other] Generate a simulated methylBase object using methylKit's dataSim() function with parameters set to 6 replicates and 1000 methylation sites.: "Generate a simulated methylBase object using methylKit's dataSim() function with parameters set to 6 replicates and 1000 methylation sites."
- [other] Extract and compare the q-value distributions from the corrected run (overdispersion='MN') against a parallel uncorrected run (overdispersion=FALSE or default) to verify that the corrected method produces higher average q-values: "Extract and compare the q-value distributions from the corrected run (overdispersion='MN') against a parallel uncorrected run (overdispersion=FALSE or default) to verify that the corrected method"
- [other] The calculateDiffMeth() function with overdispersion='MN' parameter calculates a scaling parameter φ = X²/(N-P) to adjust variance as φ·n_i·π̂_i·(1-π̂_i), which makes statistical tests more stringent by correcting for variance in excess of binomial expectations and automatically switches from Chisq to F-test.: "The calculateDiffMeth() function with overdispersion='MN' parameter calculates a scaling parameter φ = X²/(N-P) to adjust variance as φ·n_i·π̂_i·(1-π̂_i), which makes statistical tests more stringent"
- [readme] methylKit is an R package for DNA methylation analysis and annotation from high-throughput bisulfite sequencing: "methylKit is an R package for DNA methylation analysis and annotation from high-throughput bisulfite sequencing."
