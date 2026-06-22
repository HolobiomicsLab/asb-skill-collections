---
name: hypergeometric-distribution-probability-calculation
description: Use when when you have raw strain correlation scores computed across GCF–MF pairs of varying sizes (different numbers of strains in each set) and need to make those scores comparable.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_0749
  - http://edamontology.org/topic_3697
  - http://edamontology.org/topic_2885
  tools:
  - NumPy or SciPy
  - Python
  - NPLinker
derived_from:
- doi: 10.1101/2024.10.11.617756
  title: NPLinker
- doi: 10.1371/journal.pcbi.1008920
  title: ''
evidence_spans:
- follows the hypergeometric distribution as previously stated
- NPLinker, a Python module to accelerate and support the process of automatically linking GCFs
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nplinker_cq
    doi: 10.1101/2024.10.11.617756
    title: NPLinker
  dedup_kept_from: coll_nplinker_cq
schema_version: 0.2.0
---

# hypergeometric-distribution-probability-calculation

## Summary

Calculate the hypergeometric probability distribution and derived statistics (expected value and variance) to establish a null model for strain overlap between genomic and metabolomic feature sets. This enables standardization of raw correlation scores to make them comparable across GCF–MF links of different sizes.

## When to use

When you have raw strain correlation scores computed across GCF–MF pairs of varying sizes (different numbers of strains in each set) and need to make those scores comparable. The hypergeometric distribution models the null hypothesis that strain overlap is random given the population size N, GCF size g, MF size m, and observed overlap o. Apply this skill before standardizing raw scores, especially when links have heterogeneous set sizes that make raw scores non-comparable.

## When NOT to use

- The input already consists of standardized or z-scored correlation values; the hypergeometric calculation is redundant.
- All GCF–MF links have the same set sizes (g, m constant); raw score comparability is not the limiting issue and simpler standardization (e.g. z-score across all links) may suffice.
- Strain overlap does not follow random sampling assumptions (e.g., if strain presence is driven by strong ecological or evolutionary constraints that violate the hypergeometric null model).

## Inputs

- GCF strain-set membership (set G, size g)
- MF strain-set membership (set M, size m)
- Population size N (total strains in study)
- Observed strain overlap o for each GCF–MF link
- Raw strain correlation score σ_corr for each link

## Outputs

- Hypergeometric expected value E[σ_corr(M,G)] per link
- Hypergeometric variance Var[σ_corr(M,G)] per link
- Standardised correlation score s*_corr per link
- Table with columns: GCF ID, MF ID, raw score, expected value, variance, standardised score

## How to apply

For each GCF–MF link, compute the hypergeometric expected value E[σ_corr(M,G)] by summing over all possible overlap sizes k the product of (1) the raw correlation score σ_corr conditional on overlap k and (2) the hypergeometric probability p(o=k | N, g, m). Then compute the second moment E[σ_corr²] similarly to derive variance as Var[σ_corr(M,G)] = E[σ_corr²] − E[σ_corr]². The hypergeometric probability p(o=k) is calculated using the hypergeometric probability mass function with parameters: population size N (total strains), success states in population g (GCF strains), number of draws m (MF strains), and number of observed successes k (overlap). These statistics serve as the denominator and standardizer in the final formula s*_corr = (σ_corr − E[σ_corr]) / √Var[σ_corr], making score values directly comparable across links regardless of set size.

## Related tools

- **NumPy or SciPy** (Compute hypergeometric probability mass function, expected values, variances, and standardization operations)
- **NPLinker** (Framework integrating genomics and metabolomics data; applies this skill to standardize strain correlation scores before ranking GCF–MF links) — https://github.com/sdrogers/nplinker

## Examples

```
from scipy.stats import hypergeom; import numpy as np
N, g, m, o = 150, 20, 35, 5  # population, GCF size, MF size, overlap
probs = [hypergeom.pmf(k, N, g, m) for k in range(max(0, m+g-N), min(g, m)+1)]
expected = sum(score_given_overlap(k) * p for k, p in enumerate(probs))
variance = sum(score_given_overlap(k)**2 * p for k, p in enumerate(probs)) - expected**2
standardized = (raw_score - expected) / np.sqrt(variance)
```

## Evaluation signals

- Verify that E[σ_corr] and Var[σ_corr] are computed for every unique combination of (N, g, m); spot-check against manual hypergeometric PMF calculations.
- Check that standardised scores for all links (including non-validated ones) have mean ≈ 0 and variance ≈ 1 after standardization.
- Confirmed significant separation: validated links should have mean standardised score ~3.67 vs. all links mean ≈ -0.006, with p-value < 1e-10.
- Validate that hypergeometric parameters (N, g, m, k) are correctly extracted from strain-set membership; ensure no off-by-one errors in set size calculations.
- Output table schema check: verify all rows have numeric E[σ_corr], Var[σ_corr], and s*_corr; no NaNs, infinities, or negative variances.

## Limitations

- The hypergeometric model assumes strain overlap is purely random under the null hypothesis; if strain co-occurrence is driven by phylogeny, ecology, or experimental design, the null distribution may not hold, leading to miscalibrated standardised scores.
- Standardised scores still cannot distinguish between links with identical strain presence/absence patterns, even after hypergeometric standardization—a fundamental limitation of correlation-based approaches.
- The skill depends critically on correct identification of set membership (G, M) and population size (N); errors in strain assignment propagate directly into E[σ_corr] and Var[σ_corr].
- Very small sets (g, m, or overlap k near 1) may yield unstable variance estimates due to sparse hypergeometric support; in such cases, alternative regularization may be warranted.

## Evidence

- [other] The standardised strain correlation score is computed by subtracting the hypergeometric expected value E[σ_corr(M,G)] from the raw score and dividing by the variance Var[σ_corr(M,G)], where the expected value and variance are calculated based on the null hypothesis that strain overlap follows a hypergeometric distribution with population size N, GCF size g, MF size m, and overlap o.: "The standardised strain correlation score is computed by subtracting the hypergeometric expected value E[σ_corr(M,G)] from the raw score and dividing by the variance Var[σ_corr(M,G)], where the"
- [other] Calculate the hypergeometric expected value E[σ_corr(M, G)] by summing over all possible overlap sizes k, weighted by hypergeometric probability p(o=k). Calculate variance Var[σ_corr(M, G)] using the formula E[σ_corr²] − E[σ_corr]². Compute standardised score as s*_corr = (σ_corr − E[σ_corr]) / √Var[σ_corr] for each link.: "Calculate the hypergeometric expected value E[σ_corr(M, G)] by summing over all possible overlap sizes k, weighted by hypergeometric probability p(o=k). Calculate variance Var[σ_corr(M, G)] using the"
- [results] Standardising the score gives a mean score of -0.006 for all links, and 3.672 for validated links: "Standardising the score gives a mean score of -0.006 for all links, and 3.672 for validated links"
- [abstract] the most popular strain correlation score [17] has properties that make it impossible to reliably compare score values across links (even links from the same GCF or MF), severely limiting the scores: "the most popular strain correlation score has properties that make it impossible to reliably compare score values across links"
- [discussion] standardising the strain correlation score still suffers from the drawback inherent in correlation-based scoring, of not being able to distinguish between potential links showing the same pattern of strain presence or absence: "standardising the strain correlation score still suffers from the drawback inherent in correlation-based scoring, of not being able to distinguish between potential links showing the same pattern"
