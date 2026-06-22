---
name: score-standardisation-z-score-normalization
description: Use when when comparing raw link scores (strain correlation or IOKR) across different GCF-MF or BGC-spectrum pairs and you need to distinguish true positive links from background noise. Raw scores depend on overlap size and are incomparable across links with different cluster sizes;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3301
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3697
  tools:
  - antiSMASH
  - BiG-SCAPE
  - MIBiG
  - GNPS
  - NPLinker
derived_from:
- doi: 10.1101/2024.10.11.617756
  title: NPLinker
- doi: 10.1371/journal.pcbi.1008920
  title: ''
evidence_spans:
- After downloading the strain assemblies and metabolomics data, the genomes were run through antiSMASH v5.0.0 for BGC detection
- and BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs
- BiG-SCAPE clusters the BGCs separately by product type
- antiSMASH to score the correspondence between the MIBiG entries and the detected BGCs
- the MIBiG database [32] has emerged as a central repository of characterised microbial BGCs
- this way, we built a set of known BGC-spectrum pairs. To avoid etabolites based on properties absent from an MS2 spectrum,
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

# Score Standardisation (Z-Score Normalization)

## Summary

Transform raw scoring functions (strain correlation or IOKR) to zero mean and unit variance by subtracting the hypergeometric expected value and dividing by the standard deviation, enabling reliable cross-link comparison and statistical ranking. This standardisation resolves the inability of raw scores to distinguish links with identical strain/spectrum patterns.

## When to use

When comparing raw link scores (strain correlation or IOKR) across different GCF-MF or BGC-spectrum pairs and you need to distinguish true positive links from background noise. Raw scores depend on overlap size and are incomparable across links with different cluster sizes; standardisation is required when the raw score distribution differs substantially between links (e.g., mean 83.5 for all links vs. 14.7 for validated links) or when you observe that links with identical presence/absence patterns receive identical raw scores despite different biological relevance.

## When NOT to use

- When raw scores already have comparable distributions across all links (e.g., all derived from the same scoring function on uniformly-sized clusters); standardisation adds noise if variance is already unit or near-zero.
- When you cannot compute or do not have access to null model parameters (hypergeometric N, m, g, o); standardisation requires these to calculate expected value and variance.
- When the goal is to report absolute metabolite or genomic similarity rather than rank links; standardisation centers and rescales, losing absolute magnitude information.

## Inputs

- Raw strain correlation scores for all GCF-MF link pairs (numerical vector)
- Raw IOKR scores for all BGC-spectrum link pairs (numerical vector)
- Overlap statistics per link: population size N, cluster size (m or g), observed overlap count o
- Link validation labels (binary: validated vs. unvalidated)

## Outputs

- Standardised strain correlation scores (z-scores with mean ≈ 0, variance ≈ 1)
- Standardised IOKR scores (z-scores with mean ≈ 0, variance ≈ 1)
- Summary statistics: mean, variance, p-values for validated link enrichment
- Ranked link list sorted by standardised score

## How to apply

For each GCF-MF or BGC-spectrum link pair, compute the hypergeometric expected value E[score] and variance Var[score] under the null hypothesis of random strain or spectral overlap, using population size N (total strains or spectra), cluster size (m for metabolite families or g for gene clusters), and observed overlap count o. Apply the standardisation formula s* = (s_raw − E[s]) / √Var[s] to convert raw scores to z-scores with mean ≈ 0 and variance ≈ 1. For strain correlation, use the scoring rule: +10 (strain in both), −10 (strain in MF only), +1 (strain in neither), 0 (strain in GCF only). Apply the same standardisation approach to IOKR scores: s*_IOKR = (σ_IOKR − E[σ_IOKR]) / √Var[σ_IOKR]. Compute summary statistics (mean, variance, p-values from statistical tests) on the standardised scores across all links and separately for the validated link subset to verify that standardised validated links are significantly enriched (e.g., p < 0.01).

## Related tools

- **NPLinker** (Framework within which standardised strain correlation and IOKR scores are computed and combined; implements the standardisation formula and null model calculations) — https://github.com/sdrogers/nplinker
- **BiG-SCAPE** (Clusters BGCs into GCFs, providing the GCF size (g) and membership data needed to compute overlap counts and standardisation parameters for strain correlation scores)
- **antiSMASH** (Detects BGCs from genomes; BGC assignments to strains are used to compute raw strain correlation scores before standardisation)
- **GNPS** (Provides MS2 spectra and metabolite families; spectrum-to-MF assignments used to compute IOKR scores and standardisation parameters)

## Examples

```
s_standardized = (s_raw - E_hypergeometric) / sqrt(Var_hypergeometric); mean_all = np.mean(s_standardized); mean_validated = np.mean(s_standardized[validated_links]); pval = scipy.stats.mannwhitneyu(s_standardized[validated_links], s_standardized[~validated_links]).pvalue
```

## Evaluation signals

- Standardised scores have empirical mean ≈ 0.0 (e.g., −0.006 ± tolerance) and variance ≈ 1.0 across all links
- Validated links show significantly higher standardised scores than unvalidated links (p < 0.01, e.g., p = 6.8302 × 10−64 for strain correlation or p = 1.7968 × 10−9 for IOKR in the reference dataset)
- Standardised scores are more discriminative than raw scores: raw validated mean 14.667 vs. all links mean 83.514; standardised validated mean 3.672 vs. all links mean −0.006
- Standardised scores eliminate the 'identical pattern' problem: links with the same presence/absence pattern now receive different scores based on hypergeometric significance
- Combined standardised correlation and IOKR scores show enrichment at the 90th percentile (p ≤ 0.05) compared to individual scores

## Limitations

- Standardisation still cannot distinguish between links showing identical strain presence/absence patterns; the method assumes patterns differ in their hypergeometric significance, not their raw frequency.
- IOKR standardisation requires MIBiG homology to assign molecular structures to BGCs; restricted to BGCs with considerable sequence similarity, so standardised IOKR scores are not applicable to novel, uncharacterized BGCs.
- Hypergeometric model assumes random overlap under the null; violation of this assumption (e.g., if strains or spectra are phylogenetically or chemically clustered) will bias expected values and invalidate standardisation.
- Performance of standardised IOKR is not fully characterized by product type due to insufficient test set size for some BGC classes.
- Kernel function and parameter selection for IOKR significantly affect the input scores; poor kernel choice degrades IOKR before standardisation and may not be corrected by standardisation alone.

## Evidence

- [results] Standardising the strain correlation score as s*_corr = (σ_corr − E[σ_corr]) / √Var[σ_corr]: "Standardise the strain correlation score as s*_corr = (σ_corr − E[σ_corr]) / √Var[σ_corr] to yield zero mean and unit variance."
- [results] Raw correlation score statistics and standardised comparison: "For the raw strain correlation score, the mean score is 83.514 for all links, and 14.667 for validated links. Standardising the score gives a mean score of -0.006 for all links, and 3.672 for"
- [results] Standardisation applied to IOKR using same approach: "To make the IOKR score comparable to the standardised correlation score, we can standardise it in a similar manner: s*_IOKR = (σ_IOKR − E[σ_IOKR]) / Var[σ_IOKR]"
- [abstract] Problem solved by standardisation: inability to compare raw scores across links: "the most popular strain correlation score has properties that make it impossible to reliably compare score values across links (even links from the same GCF or MF)"
- [methods] Hypergeometric null model for computing expected value and variance: "calculate the hypergeometric expected value E[σ_corr(M,G)] and variance Var[σ_corr(M,G)] under the null hypothesis of random overlap, using population size N, MF size m, GCF size g, and overlap count"
- [results] Significant enrichment of validated links after standardisation: "both the IOKR and standardised strain correlation scores are significantly enriched (p-value of 0.0139 and 2.483 × 10−11, respectively)"
