---
name: hypergeometric-distribution-calculation
description: Use when when you have raw strain correlation scores (or similar overlap-based metrics) computed across genomic cluster family (GCF) and molecular family (MF) pairs of varying sizes, and you need to make those scores comparable across links with different GCF sizes (#G), MF sizes (#m), and.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0622
  tools:
  - antiSMASH
  - BiG-SCAPE
  - GNPS
  - MIBiG
  - NPLinker
derived_from:
- doi: 10.1371/journal.pcbi.1008920
  title: NPLinker
evidence_spans:
- after downloading the strain assemblies and metabolomics data, the genomes were run through antiSMASH v5.0.0 for BGC detection
- genomes were run through antiSMASH v5.0.0 for BGC detection
- and BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs
- BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs
- the metabolomics data, the genomes were run through antiSMASH v5.0.0 for BGC detection and BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs
- we use library MS2 spectra from the public, community-driven GNPS knowledge base [33] as a training set for the IOKR model
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nplinker
    doi: 10.1371/journal.pcbi.1008920
    title: NPLinker
  dedup_kept_from: coll_nplinker
schema_version: 0.2.0
---

# Hypergeometric Distribution Calculation

## Summary

Compute expected value and variance of strain correlation scores under a hypergeometric null model to standardize raw scores across GCF–MF links of different sizes. This enables fair comparison of genomic–metabolomic associations independent of set cardinalities.

## When to use

When you have raw strain correlation scores (or similar overlap-based metrics) computed across genomic cluster family (GCF) and molecular family (MF) pairs of varying sizes, and you need to make those scores comparable across links with different GCF sizes (#G), MF sizes (#m), and population sizes (#N). This is necessary when the raw score distribution is confounded by set size, making it difficult to distinguish true links from spurious high-scoring pairs that arise merely from large overlap counts.

## When NOT to use

- Raw overlap counts are already normalized or size-adjusted by another method (e.g., Jaccard or hypergeometric p-values already computed).
- The GCF and MF assignments are not independent or do not follow a random sampling model (e.g., if overlap is structured by phylogeny or functional constraint rather than chance).
- Population size #N is not well-defined or strains are not uniformly sampled (violates hypergeometric model assumptions).

## Inputs

- Raw strain correlation scores for all GCF–MF pairs
- GCF sizes (#G) for each pair
- MF sizes (#m) for each pair
- Observed overlap counts (#(G∩M)) for each pair
- Total population size (#N) — number of strains in the dataset

## Outputs

- Standardized correlation scores (s*_corr) for all GCF–MF links
- Expected values E[σ_corr(M,G)] per link
- Variances Var[σ_corr(M,G)] per link
- Distribution statistics (mean, std) for validated vs. all links

## How to apply

For each GCF–MF pair, compute the hypergeometric distribution over all possible overlap sizes k ∈ [0, min(#m, #G)], where p(overlap=k) follows hypergeometric(N, #m, #G). Calculate the expected value E[σ_corr(M,G)] and variance Var[σ_corr(M,G)] by marginalizing the raw correlation score σ_corr(M,G) over this distribution. Then standardize the observed raw score as s*_corr = (σ_corr(M,G) − E[σ_corr(M,G)]) / √Var[σ_corr(M,G)]. The hypergeometric model assumes a null hypothesis of random strain overlap: under this null, validated links should still cluster at high standardized scores (mean ≈ 3.67) while all links scatter near zero (mean ≈ −0.006), yielding large separation with p < 10^−60. This z-score transformation decouples the link score from the combinatorial bias inherent in comparing sets of different cardinalities.

## Related tools

- **antiSMASH** (BGC detection from microbial genomes; produces GCF assignments used to define set membership (#G))
- **BiG-SCAPE** (BGC clustering into GCFs; establishes which strains contribute to each GCF cardinality (#G))
- **GNPS** (Metabolomics spectrum database; defines MF membership and sizes (#m) via spectral clustering)
- **NPLinker** (Framework for computing and standardizing strain correlation scores; implements hypergeometric expectation and variance calculation) — https://github.com/sdrogers/nplinker
- **MIBiG** (Reference BGC database; provides validated GCF–MF links for evaluation)

## Evaluation signals

- Standardized scores for validated links have a significantly higher mean (target ≈ 3.67) and narrower range than all links (mean ≈ −0.006), with p-value < 10^−60 (e.g., t-test or Mann–Whitney U).
- Standardized scores have mean ≈ 0 and std ≈ 1 across all links (confirming z-score transformation).
- Raw and standardized score distributions show opposite trends: raw scores correlate with set size (larger #G and #m → higher raw scores); standardized scores are decoupled from cardinality.
- Validated links are significantly enriched (p < 10^−10) above the 90th percentile of standardized scores, whereas raw scores show no such enrichment.
- Histograms and boxplots comparing raw vs. standardized scores across multiple datasets (Crüsemann, Gross, Leão) show consistent separation patterns, confirming robustness of the hypergeometric model.

## Limitations

- The hypergeometric model assumes strains are sampled uniformly and independently; violations (e.g., phylogenetic clustering, functional constraints on overlap) invalidate the null distribution.
- Requires well-defined population size (#N); incomplete or biased strain inventories will distort expected values and variance.
- High computational cost for large datasets: calculating E and Var over the full support of the hypergeometric distribution for every GCF–MF pair can be slow; optimization via lookup tables or caching is recommended.
- Standardization by variance can be unstable or undefined for pairs with very small GCF or MF sizes, where variance is near zero; tail behavior may be unreliable.

## Evidence

- [other] For each GCF-MF pair, compute expected value E[σ_corr(M,G)] and variance Var[σ_corr(M,G)] using hypergeometric distribution over all possible overlap sizes k, where p(o=k) follows hypergeometric with parameters N, m, g, and overlap.: "For each GCF-MF pair, compute expected value E[σ_corr(M,G)] and variance Var[σ_corr(M,G)] using hypergeometric distribution over all possible overlap sizes k, where p(o=k) follows hypergeometric with"
- [other] The standardised correlation score achieves a mean of -0.0060 for all links and 3.6717 for validated links (p=6.8302 × 10−64), compared to the raw score's means of 83.5144 and 14.6667 respectively, demonstrating that standardisation successfully enables comparison across links with different GCF and MF sizes.: "The standardised correlation score achieves a mean of -0.0060 for all links and 3.6717 for validated links (p=6.8302 × 10−64), compared to the raw score's means of 83.5144 and 14.6667 respectively,"
- [other] Calculate standardised correlation score s*_corr = (σ_corr(M,G) - E[σ_corr(M,G)]) / √Var[σ_corr(M,G)] for all links.: "Calculate standardised correlation score s*_corr = (σ_corr(M,G) - E[σ_corr(M,G)]) / √Var[σ_corr(M,G)] for all links."
- [abstract] Based on standardising a commonly used score, we introduce a new, more effective score: "Based on standardising a commonly used score, we introduce a new, more effective score"
- [results] we examine the distribution of scores for validated links in relation to the scores for all hypothetical links: "we examine the distribution of scores for validated links in relation to the scores for all hypothetical links"
