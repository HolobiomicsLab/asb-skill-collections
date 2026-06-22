---
name: statistical-significance-testing-p-value-calculation
description: Use when after standardizing link scores (strain correlation and IOKR) across all potential GCF-MF pairs in a metabologenomics dataset, perform significance testing to determine whether validated links show statistically distinguishable score distributions from the background.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3325
  - http://edamontology.org/topic_3518
  - http://edamontology.org/topic_0092
  tools:
  - antiSMASH
  - BiG-SCAPE
  - MIBiG
  - GNPS
  - NPLinker
  techniques:
  - LC-MS
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

# statistical-significance-testing-p-value-calculation

## Summary

Compute p-values and significance tests to quantify whether observed differences in link-scoring distributions (e.g., mean standardised scores for validated vs. random links) are unlikely under the null hypothesis of random association. This skill enables ranking and filtering of GCF-MF links by statistical strength.

## When to use

After standardizing link scores (strain correlation and IOKR) across all potential GCF-MF pairs in a metabologenomics dataset, perform significance testing to determine whether validated links show statistically distinguishable score distributions from the background. Apply this when comparing mean or median scores between validated link subsets and all-link populations, or when filtering links by score percentile and need to confirm enrichment.

## When NOT to use

- Input is already a pre-filtered or pre-ranked link set with no access to the full background distribution (p-values require population-level statistics).
- No validated ground-truth labels are available; significance testing requires a known subset of true links for comparison.
- Score distributions are highly non-normal and sample sizes are very small (<5 validated links); classical parametric tests may be unreliable.

## Inputs

- standardised strain correlation scores for all GCF-MF link pairs
- standardised IOKR scores for all GCF-MF link pairs
- binary labels or ground-truth set of validated GCF-MF links
- link metadata (GCF identifier, MF identifier, score values)
- optional: score percentile threshold (e.g., 90th percentile)

## Outputs

- p-values for pairwise score comparisons (validated vs. all links)
- mean and variance of scores stratified by link validation status
- significance test results with test statistic and effect size
- enrichment p-value for filtered link subsets
- ranked or prioritized link list annotated with significance labels

## How to apply

For each scoring function (standardised strain correlation and IOKR), compute the mean score for the validated link subset and the full link population. Apply a statistical test (e.g., t-test, Mann–Whitney U, or permutation test) to generate a p-value quantifying the probability of observing the observed difference under random overlap. Report the p-value alongside effect size (mean difference). When filtering links above the 90th percentile by score, apply a hypergeometric or contingency-table test to assess whether the proportion of validated links in the filtered set exceeds the background rate, reporting the enrichment p-value. Use these p-values to prioritize scoring functions and combined scores that show the strongest statistical separation (lower p-values indicate stronger signal).

## Related tools

- **NPLinker** (Framework that integrates genomic and metabolomic scoring functions and reports p-values for link enrichment validation) — https://github.com/sdrogers/nplinker
- **BiG-SCAPE** (Clusters BGCs into GCFs; output is necessary to compute strain correlation scores used in significance testing)
- **antiSMASH** (Detects BGCs from genomes; required upstream to define the GCF entities scored in link significance tests)
- **GNPS** (Provides MS/MS spectral data and metabolite identifications; used to train IOKR scoring model and define validated MF-spectrum pairs)

## Evaluation signals

- p-values for validated link subset are much smaller (e.g., p < 0.001) than for background all-link population, indicating strong statistical separation of true from random links.
- Mean standardised score for validated links is >2 standard deviations from the mean of all links (e.g., validated mean 3.67, all-link mean −0.006 as reported).
- When links are filtered above the 90th percentile, the proportion of validated links in the filtered subset significantly exceeds the background rate (enrichment p-value < 0.05).
- Combined or multi-score filtering (both IOKR and standardised correlation >90th percentile) yields lower p-values than either score alone, confirming complementarity.
- Statistical test assumptions are met: if using parametric tests, verify normality of score distributions; if non-normal, confirm use of non-parametric alternatives (e.g., Mann–Whitney U) or report effect sizes alongside p-values.

## Limitations

- Standardised strain correlation score still suffers from inability to distinguish between links showing identical strain presence/absence patterns, limiting the biological interpretability of marginal p-value differences.
- IOKR scoring relies on MIBiG homology; validated link sets used for significance testing are biased toward BGCs with known close homologs, potentially inflating p-values for novel or divergent BGCs.
- P-value computation assumes independence of link pairs; in reality, GCFs and MFs are nested structures, so multiple links per GCF or MF may violate independence assumptions and inflate significance.
- Sample size of validated links is often small (e.g., 8 validated links in Crüsemann dataset); statistical power is limited, and p-values may be unstable or driven by outliers.

## Evidence

- [other] The standardised strain correlation score has a mean of -0.0060 and variance of 1 across all links (compared to raw score mean of 83.5144), with standardised scores for validated links reaching 3.6717 (p=6.8302 × 10−64).: "The standardised strain correlation score has a mean of -0.0060 and variance of 1 across all links (compared to raw score mean of 83.5144), with standardised scores for validated links reaching"
- [results] For the raw strain correlation score, the mean score is 83.514 for all links, and 14.667 for validated links: "For the raw strain correlation score, the mean score is 83.514 for all links, and 14.667 for validated links"
- [results] Standardising the score gives a mean score of -0.006 for all links, and 3.672 for validated links: "Standardising the score gives a mean score of -0.006 for all links, and 3.672 for validated links"
- [results] the set of links scoring above the 90th percentile on both scores is significantly enriched compared to the set that exceed either of the individual scores (p-value of 2.633 × 10−4 and 0.0208: "the set of links scoring above the 90th percentile on both scores is significantly enriched compared to the set that exceed either of the individual scores (p-value of 2.633 × 10−4 and 0.0208"
- [results] both the IOKR and standardised strain correlation scores are significantly enriched (p-value of 0.0139 and 2.483 × 10−11, respectively): "both the IOKR and standardised strain correlation scores are significantly enriched (p-value of 0.0139 and 2.483 × 10−11, respectively)"
- [other] For each link, calculate the hypergeometric expected value E[σ_corr(M,G)] and variance Var[σ_corr(M,G)] under the null hypothesis of random overlap, using population size N, MF size m, GCF size g, and overlap count o.: "For each link, calculate the hypergeometric expected value E[σ_corr(M,G)] and variance Var[σ_corr(M,G)] under the null hypothesis of random overlap"
