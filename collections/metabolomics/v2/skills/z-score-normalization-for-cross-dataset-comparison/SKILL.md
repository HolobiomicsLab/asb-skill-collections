---
name: z-score-normalization-for-cross-dataset-comparison
description: Use when you have multiple scoring functions (e.g., strain correlation or spectral similarity scores) computed over heterogeneous GCF-MF or BGC-spectrum link sets where raw scores cannot be directly compared due to differences in set sizes (GCF size g, MF size m, overlap o) or null-model.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0602
  tools:
  - NumPy or SciPy
  - Python
  - NumPy
  - SciPy
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2024.10.11.617756
  all_source_dois:
  - 10.1101/2024.10.11.617756
  - 10.1371/journal.pcbi.1008920
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# z-score-normalization-for-cross-dataset-comparison

## Summary

Transform raw scoring metrics (strain correlation, IOKR) into standardized z-scores by subtracting the null-model expected value and dividing by standard deviation, enabling direct comparison of link scores across GCF-MF pairs of different sizes and molecular families. This normalization resolves the inability of raw scores to distinguish validated links reliably when scores span different ranges.

## When to use

Apply this skill when you have multiple scoring functions (e.g., strain correlation or spectral similarity scores) computed over heterogeneous GCF-MF or BGC-spectrum link sets where raw scores cannot be directly compared due to differences in set sizes (GCF size g, MF size m, overlap o) or null-model distributions. Use it specifically when raw score means differ substantially between validated and non-validated link populations (e.g., raw mean 83.5 vs. 14.7), indicating that raw values conflate signal with background variation.

## When NOT to use

- Raw scores are already normally distributed or scale-free (e.g., percentile ranks, log odds); standardization may flatten or distort the signal.
- Link sets are homogeneous in size and all derived from the same null model; raw scores may already be comparable.
- You need interpretable effect sizes tied to biological mechanism rather than statistical deviation; z-scores obscure the magnitude of correlation or spectral similarity.

## Inputs

- GCF and MF strain-set membership data (sets G and M, population size N)
- Raw strain correlation scores or IOKR scores for each GCF-MF or BGC-spectrum link
- Four-term rule components: indicator for strain producing metabolite, strain having BGC, both, or neither

## Outputs

- Standardized score (z-score) for each link
- Table with columns: link ID, raw score, expected value E[s], variance Var[s], standardized score z
- Statistical summary: mean and standard deviation of z-scores for validated vs. all links, with p-values

## How to apply

For each link, compute the expected value E[s] and variance Var[s] of the raw score under the null hypothesis (hypergeometric distribution for strain overlap, or empirical distribution for IOKR). Then compute the standardized score as z = (s_raw − E[s]) / √Var[s]. For strain correlation, calculate E[σ_corr(M,G)] by summing the four-term rule score (+10, −10, +1, 0) weighted by hypergeometric probabilities over all possible overlaps k. For IOKR, standardize using the same formula applied to the empirical distribution of IOKR values. Output a table with raw score, expected value, variance, and z-score for each link. Validate that standardized scores for validated links cluster significantly above the mean (e.g., z > 3.67) with low p-value (< 0.001) compared to all links (z ≈ 0).

## Related tools

- **NumPy** (Vectorized computation of hypergeometric probabilities, expected values, and variances; element-wise z-score transformation)
- **SciPy** (scipy.stats.hypergeom for computing probability mass function and cumulative distribution; statistical testing (scipy.stats.ttest_ind for p-value computation))
- **NPLinker** (Framework that ingests raw strain correlation and IOKR scores and applies standardization prior to link ranking and combination) — https://github.com/sdrogers/nplinker

## Examples

```
import numpy as np
from scipy.stats import hypergeom
# Compute z-score for a GCF-MF link: raw_score=20, N=500, g=50, m=40, o=15
expected = sum(hypergeom.pmf(k, N, g, m) * score_func(k) for k in range(0, min(g,m)+1))
variance = sum(hypergeom.pmf(k, N, g, m) * score_func(k)**2 for k in range(0, min(g,m)+1)) - expected**2
z_score = (raw_score - expected) / np.sqrt(variance)
print(f'z_score: {z_score}')
```

## Evaluation signals

- Standardized scores for validated links have mean > 3.0 and p-value < 0.01 vs. all-link mean near 0.
- Raw score means differ substantially between validated and all-link populations (e.g., 14.7 vs. 83.5), while standardized means are separable (e.g., 3.67 vs. −0.006).
- Histogram of standardized scores shows bimodal or right-skewed distribution with validated links in the right tail, indicating signal separation.
- Variance is non-zero and finite for each link (no division by zero or infinite z-scores); no NaN or inf values in output.
- Combining standardized scores from multiple methods (e.g., IOKR + strain correlation via ℓ_p norm) yields higher statistical enrichment (lower p-value) than either raw score alone.

## Limitations

- Standardization still cannot distinguish between links that share identical strain presence/absence patterns but differ in other attributes (inherent drawback of correlation-based scoring).
- Hypergeometric null model assumes strain overlap is random; if true biology exhibits bias (e.g., co-occurrence), expected value and variance may be misspecified, leading to misleading z-scores.
- IOKR scores depend on MIBiG homology; BGCs with low homology will have poorly estimated null distributions, reducing standardization effectiveness.
- Small sample sizes in some GCF or MF subsets may yield unstable variance estimates; consider Bayesian shrinkage or pooled variance if subsets are sparse.

## Evidence

- [other] The standardised strain correlation score is computed by subtracting the hypergeometric expected value E[σ_corr(M,G)] from the raw score and dividing by the variance Var[σ_corr(M,G)]: "The standardised strain correlation score is computed by subtracting the hypergeometric expected value E[σ_corr(M,G)] from the raw score and dividing by the variance Var[σ_corr(M,G)]"
- [results] For the raw strain correlation score, the mean score is 83.514 for all links, and 14.667 for validated links (p=0.0001); standardising gives a mean of −0.006 for all links and 3.672 for validated links (p=6.8302 × 10−64): "For the raw strain correlation score, the mean score is 83.514 for all links, and 14.667 for validated links. Standardising the score gives a mean score of -0.006 for all links, and 3.672 for"
- [abstract] the most popular strain correlation score has properties that make it impossible to reliably compare score values across links (even links from the same GCF or MF), severely limiting the scores: "the most popular strain correlation score has properties that make it impossible to reliably compare score values across links (even links from the same GCF or MF)"
- [other] Calculate the hypergeometric expected value E[σ_corr(M, G)] by summing over all possible overlap sizes k, weighted by hypergeometric probability p(o=k): "Calculate the hypergeometric expected value E[σ_corr(M, G)] by summing over all possible overlap sizes k, weighted by hypergeometric probability p(o=k)"
- [results] To make the IOKR score comparable to the standardised correlation score, we can standardise it in a similar manner: "To make the IOKR score comparable to the standardised correlation score, we can standardise it in a similar manner"
- [results] the set of links scoring above the 90th percentile on both scores is significantly enriched compared to the set that exceed either of the individual scores: "the set of links scoring above the 90th percentile on both scores is significantly enriched compared to the set that exceed either of the individual scores"
