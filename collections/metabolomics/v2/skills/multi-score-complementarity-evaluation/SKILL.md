---
name: multi-score-complementarity-evaluation
description: Use when you have two or more independent scoring functions ranking the same set of candidate links (GCF-MF pairs, BGC-spectrum associations, etc.), and you want to determine whether they capture complementary information that justifies combining them.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0160
  - http://edamontology.org/topic_3172
  tools:
  - antiSMASH
  - BiG-SCAPE
  - NPLinker
  - GNPS
  - MIBiG
  - Paired Omics Data Platform
derived_from:
- doi: 10.1101/2024.10.11.617756
  title: NPLinker
- doi: 10.1371/journal.pcbi.1008920
  title: ''
evidence_spans:
- after downloading the strain assemblies and metabolomics data, the genomes were run through antiSMASH v5.0.0 for BGC detection
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
---

# multi-score-complementarity-evaluation

## Summary

Evaluate whether combining independent scoring functions for genomic-metabolomic links produces enrichment for validated links beyond either individual scorer alone, using joint percentile filtering and statistical significance testing. This skill determines whether two complementary ranking methods (e.g. strain correlation and IOKR) should be integrated into a single composite score.

## When to use

You have two or more independent scoring functions ranking the same set of candidate links (GCF-MF pairs, BGC-spectrum associations, etc.), and you want to determine whether they capture complementary information that justifies combining them. Specifically, when you have a curated set of validated links against which to benchmark, and you want to test whether the top percentile (e.g. 90th) of links scoring high on BOTH functions simultaneously shows significantly higher enrichment for validated links than either individual top percentile alone.

## When NOT to use

- You have only one scoring function or fewer than two independent rankers; complementarity requires at least two distinct scoring approaches.
- Your curated validation set is very small (<50 validated links) or unrepresentatively biased; statistical power and generalisability are compromised.
- The two scores are highly correlated (e.g. both derived from the same genomic features or both measuring strain overlap); redundant scorers will not improve enrichment.

## Inputs

- Set of candidate links between genomic clusters (GCFs) and metabolomic features (MFs) or BGCs and MS2 spectra
- Score matrix 1: raw or pre-standardised scores from first ranking function (e.g. raw strain correlation σ_corr)
- Score matrix 2: raw or pre-standardised scores from second ranking function (e.g. raw IOKR σ_IOKR)
- Curated set of validated links from reference database (e.g. Paired Omics Data Platform with antiSMASH BLAST matching cumulative score ≥10000)
- Expected value and variance parameters for each scorer over the full link population

## Outputs

- Standardised score matrices for each function (σ*_corr, σ*_IOKR, etc.)
- Enrichment proportions: percentage of validated links in top-percentile groups for each single function and joint criterion
- Fisher exact test p-values: comparison of joint enrichment vs. single-function enrichment
- Boolean decision: whether scores are complementary and justify integration

## How to apply

Standardise each scoring function independently using expected value and variance over all potential links, producing comparable z-scores (σ*_corr, σ*_IOKR, etc.). Filter the full link set at a high percentile threshold (e.g. 90th) for each scoring function separately and for the joint criterion (both functions above threshold). Count the proportion of validated links in each filtered group, then compute Fisher exact test p-values comparing the enrichment of the joint top percentile group versus each single-function top percentile group. If the joint group shows significantly higher enrichment (p < 0.05) than both individual methods, the scores are complementary; if only one shows improvement, consider whether the added complexity justifies integration. The rationale is that complementary scorers capture orthogonal link evidence (e.g. strain co-occurrence vs. molecular fingerprint similarity), so enforcing agreement on both reduces false positives more than either alone.

## Related tools

- **NPLinker** (Framework for linking genomic and metabolomic data; implements strain correlation and IOKR scoring functions and provides integrated evaluation workflow) — https://github.com/sdrogers/nplinker
- **antiSMASH** (Predicts BGCs from genome sequences; BGCs are clustered into GCFs and scored for links to metabolomic features)
- **BiG-SCAPE** (Clusters predicted BGCs into Gene Cluster Families (GCFs); output GCFs are the genomic side of candidate links)
- **GNPS** (Public database of MS2 spectra and spectral clusters; source of metabolomic features that are linked to genomic clusters)
- **MIBiG** (Reference database of characterized BGCs with structure annotations; used to validate BGC-structure-spectrum correspondences)
- **Paired Omics Data Platform** (Curated dataset of paired genomic and metabolomic data with validated BGC-spectrum links; gold standard for benchmarking)

## Evaluation signals

- Standardised scores should have mean ≈ 0 and variance ≈ 1 across the full link population; validate using summary statistics.
- Enrichment proportion (validated links / total links in percentile group) for joint filtering should be significantly higher than for either single scorer at the same percentile, with Fisher exact p < 0.05.
- Top-percentile link counts should be comparable across single-function groups; if one scorer is much more selective, it may dominate the joint criterion.
- Manual spot-check: examine 5–10 links in the joint top percentile and confirm that both scores are high (above the percentile threshold) for each.
- If combining into a composite score, verify that the combined ranking function (e.g. ℓp-norm with sign adjustment) produces a distribution that is sufficiently different from either parent scorer to justify the added complexity.

## Limitations

- Complementarity depends critically on validation set quality and size; small or biased reference sets may not reveal true complementarity or may produce spurious significance.
- High dependence on choice of percentile threshold (e.g. 90th); lower thresholds may show less enrichment, and optimal threshold should be tuned per dataset.
- Standardisation using expected value and variance assumes a well-behaved null distribution; heavily skewed scorers may require non-parametric standardisation.
- IOKR scores are restricted to BGCs with considerable homology to MIBiG; applicability is limited to genomes with characterised natural product biosynthesis.
- Strain correlation score requires high-quality strain membership information; incomplete or erroneous strain assignment will degrade this scorer and reduce apparent complementarity.

## Evidence

- [other] Links scoring above the 90th percentile for both standardised strain correlation and IOKR scores show significantly higher enrichment for validated links (p=2.633×10−4 from IOKR and p=0.0208 from standardised correlation) compared to either individual score alone.: "Links scoring above the 90th percentile for both standardised strain correlation and IOKR scores show significantly higher enrichment for validated links (p=2.633×10−4 from IOKR and p=0.0208 from"
- [abstract] We demonstrate that using multiple link-scoring functions together makes it easier to prioritise true links relative to others: "We demonstrate that using multiple link-scoring functions together makes it easier to prioritise true links relative to others"
- [abstract] Strain correlation and IOKR scores are complementary and combining them improves performance over either individual approach: "we demonstrate that they are in fact complementary, and show a way to combine them to improve their performance"
- [results] To make the IOKR score comparable to the standardised correlation score, we can standardise it in a similar manner to the strain correlation score.: "To make the IOKR score comparable to the standardised correlation score, we can standardise it in a similar manner to the strain correlation score."
- [results] Table 2 shows the proportion of validated links among all possible GCF-MF links in the three data sets, both for all the potential links, and for the links scoring above the 90th percentile for raw: "Table 2 shows the proportion of validated links among all possible GCF-MF links in the three data sets, both for all the potential links, and for the links scoring above the 90th percentile"
- [discussion] By pairing the MIBiG and GNPS databases, and using the Paired omics Data Platform, we introduced data sets to test the efficiency of the scoring methods: "By pairing the MIBiG and GNPS databases, and using the Paired omics Data Platform, we introduced data sets to test the efficiency of the scoring methods"
