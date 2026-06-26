---
name: strain-correlation-hypergeometric-adjustment
description: Use when you have genomic clusters (GCFs) and metabolomic features (MFs)
  from paired microbial datasets, each with strain membership information, and you
  need to score potential links between them.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0602
  tools:
  - antiSMASH
  - BiG-SCAPE
  - NPLinker
  - GNPS
  - MIBiG
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1101/2024.10.11.617756
  title: NPLinker
- doi: 10.1371/journal.pcbi.1008920
  title: ''
evidence_spans:
- after downloading the strain assemblies and metabolomics data, the genomes were
  run through antiSMASH v5.0.0 for BGC detection
- genomes were run through antiSMASH v5.0.0 for BGC detection
- and BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs
- BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs
- NPLinker, a software framework to link genomic and metabolomic data
- NPLinker creates objects for spectra, MFs, BGCs and GCFs in the data set
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nplinker
    doi: 10.1101/2024.10.11.617756
    title: NPLinker
  dedup_kept_from: coll_nplinker
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

# strain-correlation-hypergeometric-adjustment

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Compute standardised strain correlation scores for genomic-metabolomic links by adjusting raw co-occurrence counts against a hypergeometric null distribution. This makes correlation scores comparable across datasets and significantly enriches for validated links by accounting for expected co-occurrence by chance.

## When to use

You have genomic clusters (GCFs) and metabolomic features (MFs) from paired microbial datasets, each with strain membership information, and you need to score potential links between them. Raw strain correlation counts are difficult to compare across datasets with different strain compositions and link densities. Use this skill when you want a standardised, statistically grounded score that accounts for the probability of observing co-occurrence by random chance alone.

## When NOT to use

- Input datasets lack strain-level metadata or genomes are not assigned to specific isolates/strains.
- You are comparing links within a single, homogeneous strain or environmental sample where strain variation is negligible.
- Raw co-occurrence counts are already heavily skewed by experimental design (e.g., targeted isolation of specific strains), making hypergeometric assumptions invalid.

## Inputs

- Genomic Cluster Family (GCF) strain membership lists
- Metabolomic Feature (MF) strain membership lists
- GCF-MF pair candidate set

## Outputs

- Raw strain correlation scores (σ_corr) per GCF-MF pair
- Standardised strain correlation scores (σ*_corr) per GCF-MF pair
- Expected value and variance parameters from hypergeometric null distribution

## How to apply

For each GCF-MF pair, compute the raw strain correlation score (number of strains in which both the GCF and MF are observed). Then standardise this score using the expected value and variance of the hypergeometric distribution under the null hypothesis of independent strain membership. The standardised score σ*_corr = (raw_count − expected_value) / sqrt(variance) makes scores directly comparable and enables pooling results across datasets with different strain counts. Filter or rank links by the standardised score to prioritise those with strain co-occurrence significantly exceeding chance expectation.

## Related tools

- **antiSMASH** (BGC detection and annotation from microbial genomes, source of GCF membership) — https://antismash.secondarymetabolites.org/
- **BiG-SCAPE** (BGC clustering into GCFs based on sequence homology) — https://github.com/BigSCAPE/BigSCAPE
- **NPLinker** (Framework for integrating and scoring genomic-metabolomic links, implements strain correlation and standardisation) — https://github.com/sdrogers/nplinker

## Evaluation signals

- Standardised correlation scores for validated links show significantly higher mean and median than scores for all hypothetical links (e.g., p < 0.001 by t-test or Mann–Whitney U).
- Standardised scores follow approximately normal distribution with mean ≈ 0 and variance ≈ 1 across the full link population.
- Links at the 90th percentile for standardised correlation show significantly enriched proportion of validated links compared to lower percentiles (Fisher exact test, p < 0.05).
- Standardised scores are comparable across datasets with different strain counts: no systematic bias in score magnitude across datasets.
- Joint filtering (both standardised correlation and orthogonal scoring method at 90th percentile) yields higher validated link enrichment than either method alone.

## Limitations

- Hypergeometric assumption requires that strain presence/absence is approximately independent across GCFs and MFs, which may not hold for closely related organisms or if strains are preferentially enriched for specific metabolomic phenotypes.
- Standardisation is sensitive to the total number of strains and link density; datasets with very few strains or very sparse GCF-MF co-occurrence may have unstable variance estimates.
- The method does not account for phylogenetic relatedness among strains; identical score standardisation is applied whether co-occurrence reflects true biosynthetic linkage or shared evolutionary history.

## Evidence

- [other] Compute raw and standardised strain correlation scores (σ_corr and σ*_corr) for each GCF-MF pair using hypergeometric null distribution with expected value and variance adjustment.: "Compute raw and standardised strain correlation scores (σ_corr and σ*_corr) for each GCF-MF pair using hypergeometric null distribution with expected value and variance adjustment."
- [abstract] GCF and spectrum pairs are then scored based upon their shared strains: "GCF and spectrum pairs are then scored based upon their shared strains"
- [other] Standardised correlation score mean for all links: -0.0060; for validated links: 3.6717 (p=6.8302 × 10−64): "Standardised correlation score mean for all links: -0.0060; for validated links: 3.6717 (p=6.8302 × 10−64)"
- [other] Both of the IOKR and standardised strain correlation scores are significantly enriched (p-value of 0.0139 and 2.483 × 10−11, respectively) for validated links: "both the IOKR and standardised strain correlation scores are significantly enriched (p-value of 0.0139 and 2.483 × 10−11, respectively) for validated links"
- [abstract] A standardised strain correlation score improves comparability across links: "A standardised strain correlation score improves comparability across links"
