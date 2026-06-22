---
name: strain-correlation-score-computation
description: Use when when you have paired genomics and metabolomics data from multiple strains (e.g., from Paired Omics Data Platform), have clustered BGCs into GCFs and detected molecular features, and need to score all potential GCF–MF links to prioritise true biosynthetic relationships.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3762
  edam_topics:
  - http://edamontology.org/topic_0622
  - http://edamontology.org/topic_0199
  - http://edamontology.org/topic_3361
  tools:
  - antiSMASH
  - BiG-SCAPE
  - MIBiG
  - GNPS
  - NumPy or SciPy
  - Python
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

# strain-correlation-score-computation

## Summary

Compute raw and standardised strain correlation scores to rank genomic–metabolomic links by quantifying strain overlap between gene cluster families (GCFs) and molecular features (MFs). Standardisation via hypergeometric null model enables fair comparison across links of different sizes.

## When to use

When you have paired genomics and metabolomics data from multiple strains (e.g., from Paired Omics Data Platform), have clustered BGCs into GCFs and detected molecular features, and need to score all potential GCF–MF links to prioritise true biosynthetic relationships. Use this skill to overcome the inability of raw correlation scores to be compared across links of different GCF or MF sizes.

## When NOT to use

- Input already consists of standardised or normalised scores—avoid double-standardisation.
- Dataset contains only a single strain or GCF, making overlap statistics undefined.
- GCF or MF membership data is incomplete or missing for >5% of strain annotations—hypergeometric calculations will be unreliable.

## Inputs

- GCF membership data (set of strains per GCF)
- MF membership data (set of strains per MF)
- Population size N (total number of strains in dataset)
- Raw strain correlation scores for all GCF–MF pairs

## Outputs

- Standardised strain correlation scores (s*_corr) for all GCF–MF pairs
- Hypergeometric expected values E[σ_corr(M,G)] per pair
- Hypergeometric variances Var[σ_corr(M,G)] per pair
- Summary statistics (mean, variance, p-values) of standardised scores across all links and validated link subset

## How to apply

For each GCF–MF pair: (1) compute the raw strain correlation score σ_corr(M,G) by applying the four-term rule: +10 if a strain produces the metabolite AND has the BGC, −10 if the strain produces metabolite but lacks BGC, +1 if the strain neither produces nor has BGC, 0 otherwise. (2) Calculate the hypergeometric expected value E[σ_corr(M,G)] and variance Var[σ_corr(M,G)] under the null hypothesis of random strain overlap, using population size N, MF size m, GCF size g, and observed overlap count o. (3) Standardise each score as s*_corr = (σ_corr − E[σ_corr]) / √Var[σ_corr] to achieve zero mean and unit variance across all links. This transformation makes scores comparable regardless of GCF or MF size, yielding standardised scores with mean ≈ −0.006 for background links and markedly higher values (e.g. 3.6717) for validated links.

## Related tools

- **antiSMASH** (BGC detection from microbial genomes; outputs clustered BGCs that feed into GCF membership) — https://antismash.secondarymetabolites.org/
- **BiG-SCAPE** (Clusters detected BGCs into Gene Cluster Families (GCFs); provides GCF membership required for scoring) — https://github.com/medema/BiG-SCAPE
- **NPLinker** (Framework that accepts antiSMASH/BiG-SCAPE outputs and integrates strain correlation scoring) — https://github.com/sdrogers/nplinker
- **NumPy or SciPy** (Computational backend for hypergeometric probability calculations and standardisation arithmetic)

## Evaluation signals

- Standardised score mean across all links is ≈ −0.006 (zero-centred) and variance ≈ 1 (unit variance).
- Validated links show standardised scores significantly higher than background (e.g. mean 3.6717 vs. −0.006, p < 1e−60).
- Raw scores cannot be compared directly across links of different sizes; standardised scores can.
- Hypergeometric expected values and variances are computed without error for all GCF–MF pairs; no division-by-zero or NaN values.
- Combined standardised correlation and IOKR scores enrich for validated links at the 90th percentile (p < 0.003).

## Limitations

- Standardised strain correlation score still cannot distinguish between potential links showing identical patterns of strain presence or absence; complementary scoring methods (e.g. IOKR) are needed to break such ties.
- Hypergeometric model assumes strain overlap is random and independent; strongly non-random population structure or ecological constraints may violate this assumption.
- Score is sensitive to missing or misannotated strain membership data; incomplete genome assemblies or metabolomics coverage will bias expected values and variances.

## Evidence

- [abstract] the most popular strain correlation score [17] has properties that make it impossible to reliably compare score values across links (even links from the same GCF or MF), severely limiting the scores: "the most popular strain correlation score has properties that make it impossible to reliably compare score values across links"
- [other] the raw strain correlation score σ_corr(M,G) for all potential GCF-MF link pairs using the standard rule: +10 (strain in both), −10 (strain in MF only), +1 (strain in neither), 0 (strain in GCF only): "compute the raw strain correlation score σ_corr(M,G) for all potential GCF-MF link pairs using the standard rule: +10 (strain in both), −10 (strain in MF only), +1 (strain in neither), 0 (strain in"
- [other] For each link, calculate the hypergeometric expected value E[σ_corr(M,G)] and variance Var[σ_corr(M,G)] under the null hypothesis of random overlap, using population size N, MF size m, GCF size g, and overlap count o: "calculate the hypergeometric expected value E[σ_corr(M,G)] and variance Var[σ_corr(M,G)] under the null hypothesis of random overlap, using population size N, MF size m, GCF size g, and overlap count"
- [other] Standardise the strain correlation score as s*_corr = (σ_corr − E[σ_corr]) / √Var[σ_corr] to yield zero mean and unit variance: "Standardise the strain correlation score as s*_corr = (σ_corr − E[σ_corr]) / √Var[σ_corr] to yield zero mean and unit variance"
- [other] The standardised strain correlation score has a mean of -0.0060 and variance of 1 across all links (compared to raw score mean of 83.5144), with standardised scores for validated links reaching 3.6717 (p=6.8302 × 10−64): "The standardised strain correlation score has a mean of -0.0060 and variance of 1 across all links, with standardised scores for validated links reaching 3.6717 (p=6.8302 × 10−64)"
- [discussion] standardising the strain correlation score still suffers from the drawback inherent in correlation-based scoring, of not being able to distinguish between potential links showing the same pattern of: "standardising the strain correlation score still suffers from the drawback inherent in correlation-based scoring, of not being able to distinguish between potential links showing the same pattern of"
