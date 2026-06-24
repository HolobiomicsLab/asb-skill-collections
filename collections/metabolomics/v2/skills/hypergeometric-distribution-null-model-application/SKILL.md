---
name: hypergeometric-distribution-null-model-application
description: Use when when you have raw strain correlation scores computed across
  multiple GCF–MF link pairs from a metabologenomics dataset and need to compare score
  magnitudes across different links.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0080
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_3697
  tools:
  - antiSMASH
  - BiG-SCAPE
  - MIBiG
  - GNPS
  - NPLinker
  license_tier: restricted
derived_from:
- doi: 10.1101/2024.10.11.617756
  title: NPLinker
- doi: 10.1371/journal.pcbi.1008920
  title: ''
evidence_spans:
- After downloading the strain assemblies and metabolomics data, the genomes were
  run through antiSMASH v5.0.0 for BGC detection
- and BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs
- BiG-SCAPE clusters the BGCs separately by product type
- antiSMASH to score the correspondence between the MIBiG entries and the detected
  BGCs
- the MIBiG database [32] has emerged as a central repository of characterised microbial
  BGCs
- this way, we built a set of known BGC-spectrum pairs. To avoid etabolites based
  on properties absent from an MS2 spectrum,
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# hypergeometric-distribution-null-model-application

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Apply a hypergeometric null model to compute expected value and variance of strain overlap between Gene Cluster Families (GCFs) and Molecular Features (MFs), enabling standardization of raw correlation scores to zero mean and unit variance for cross-link comparability. This skill transforms non-comparable raw scores into statistically normalized scores that reliably distinguish validated genomic–metabolomic links from false positives.

## When to use

When you have raw strain correlation scores computed across multiple GCF–MF link pairs from a metabologenomics dataset and need to compare score magnitudes across different links. Raw scores are incomparable because identical strain overlap patterns yield identical scores regardless of link quality; hypergeometric standardization resolves this by accounting for the null expectation of random strain co-occurrence, making validated links statistically distinguishable (mean 3.6717 vs. background mean -0.0060).

## When NOT to use

- Input is already a normalized or standardized score (e.g., z-scores, log-odds from another null model).
- Strain metadata is missing or incomplete (cannot compute population size, GCF/MF sizes, or overlap counts).
- The correlation scoring rule differs from the cited scheme (+10/−10/+1/0); the hypergeometric model is specific to this overlap matrix interpretation.

## Inputs

- strain presence/absence matrix for all GCFs and MFs (rows=strains, columns=clusters/features; binary)
- raw strain correlation scores σ_corr(M,G) for all potential GCF–MF link pairs
- link metadata: GCF size (g), MF size (m), overlap count (o), total strains (N)

## Outputs

- standardized strain correlation scores s*_corr with zero mean and unit variance
- per-link hypergeometric expected values E[σ_corr] and variances Var[σ_corr]
- summary statistics: mean and variance of standardized scores across all links and validated link subset
- p-values from statistical enrichment tests (e.g., validated vs. background)

## How to apply

For each GCF–MF pair, compute the raw strain correlation score σ_corr(M,G) using the standard scoring rule: +10 (strain in both GCF and MF), −10 (strain in MF only), +1 (strain in neither), 0 (strain in GCF only). Then calculate the hypergeometric expected value E[σ_corr(M,G)] and variance Var[σ_corr(M,G)] under the null hypothesis that strain presence/absence is random, using population size N (total strains), MF size m (strains in molecular feature), GCF size g (strains in gene cluster family), and observed overlap count o. Standardize each score as s*_corr = (σ_corr − E[σ_corr]) / √Var[σ_corr], yielding zero-mean unit-variance scores. Validated links should cluster at z-scores ≥3.67 (p<10⁻⁶⁴) while background links center near zero, enabling threshold-based link prioritization.

## Related tools

- **NPLinker** (Framework that implements strain correlation scoring and integrates hypergeometric standardization into GCF–MF link ranking) — https://github.com/sdrogers/nplinker
- **BiG-SCAPE** (Clusters antiSMASH-detected BGCs into GCFs, providing input GCF definitions and sizes for hypergeometric calculation)
- **antiSMASH** (Detects biosynthetic gene clusters from strain genomes, establishing the set of strains per GCF)

## Examples

```
from scipy.stats import hypergeom; N=120; m=8; g=15; o=3; raw_score=42; exp_val = hypergeom.mean(m, N, g); var_val = hypergeom.var(m, N, g); z_score = (raw_score - exp_val) / (var_val**0.5); print(f'Standardized score: {z_score:.4f}')
```

## Evaluation signals

- Standardized scores have empirical mean ≈ −0.006 and standard deviation ≈ 1.0 across all links (zero-mean unit-variance property verified).
- Validated links show mean standardized score ≥ 3.67 with p-value < 10⁻⁶⁴ (Mann–Whitney U or equivalent test against background distribution).
- Raw and standardized score distributions are visually distinct: raw scores cluster around 83.5 with poor separation; standardized scores show clear bimodal or right-skewed pattern with validated links in the tail.
- Hypergeometric E[σ_corr] and Var[σ_corr] satisfy mathematical consistency: variance is positive for all links and increases with GCF/MF sizes.
- Standardization correctly maps identical raw scores from different link pairs to identical z-scores only if GCF/MF size and overlap are identical (confirming size-normalized comparability).

## Limitations

- Standardized correlation scores still cannot distinguish between links with identical strain overlap patterns, even after normalization—a fundamental limitation of correlation-based scoring that requires complementary scoring functions (e.g., IOKR) for full disambiguation.
- Hypergeometric model assumes random strain co-occurrence; ecological or evolutionary dependencies among strains will bias expected values and reduce statistical power.
- Calculation requires complete metadata (N, m, g, o) for all links; missing or sparse strains invalidate the population assumptions.
- The standardization does not account for multiple-testing burden when ranking many links; downstream filtering (e.g., 90th percentile threshold) or Bonferroni correction may be needed depending on analysis goals.

## Evidence

- [other] hypergeometric expected value and variance calculation: "calculate the hypergeometric expected value E[σ_corr(M,G)] and variance Var[σ_corr(M,G)] under the null hypothesis of random overlap, using population size N, MF size m, GCF size g, and overlap count"
- [other] standardization formula: "Standardise the strain correlation score as s*_corr = (σ_corr − E[σ_corr]) / √Var[σ_corr] to yield zero mean and unit variance"
- [results] raw vs. standardized score statistics and p-value: "For the raw strain correlation score, the mean score is 83.514 for all links, and 14.667 for validated links. Standardising the score gives a mean score of -0.006 for all links, and 3.672 for"
- [other] scoring rule for raw correlation: "using the standard rule: +10 (strain in both), −10 (strain in MF only), +1 (strain in neither), 0 (strain in GCF only)"
- [abstract] problem motivation: raw score incomparability: "the most popular strain correlation score has properties that make it impossible to reliably compare score values across links (even links from the same GCF or MF), severely limiting the scores"
- [results] standardization enables cross-link comparison: "Standardising the score gives a mean score of -0.006 for all links, and 3.672 for validated links"
