---
name: multi-criterion-score-combination-and-ranking
description: Use when you have generated hypothetical links (e.g., GCF–MF pairs) and computed multiple independent scoring functions on them (e.g., strain co-occurrence, IOKR structural fingerprint matching), but individual scores show incomplete discrimination power.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3673
  - http://edamontology.org/topic_0091
  tools:
  - antiSMASH
  - BiG-SCAPE
  - NPLinker
  - GNPS
  - MIBiG
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

# multi-criterion-score-combination-and-ranking

## Summary

Combine multiple independent scoring functions (strain correlation, structural similarity) using standardized ℓ₁/₂-norm aggregation to rank hypothetical links between genomic and metabolomic entities. This skill improves discrimination of true links by leveraging complementary scoring signals that separately may miss important associations.

## When to use

You have generated hypothetical links (e.g., GCF–MF pairs) and computed multiple independent scoring functions on them (e.g., strain co-occurrence, IOKR structural fingerprint matching), but individual scores show incomplete discrimination power. Combine scores when you need to rank links for validation prioritization or when validation data shows that high-scoring links in one metric alone miss validated pairs that score highly in another metric.

## When NOT to use

- Only one scoring function is available; combination requires at least two independent scoring functions to be meaningful.
- Scores are already highly correlated (r > 0.8); standardization and combination of redundant signals will not improve discrimination.
- Your validation set is too small (<50 validated links) to reliably estimate enrichment significance; ranking without validated enrichment testing is unreliable for prioritization.

## Inputs

- hypothetical links (e.g., GCF–MF pairs with entity IDs and strain associations)
- raw strain correlation scores for all links
- raw IOKR scores for all links (or any second scoring function)
- set of validated/true links for enrichment testing (optional but recommended for validation)

## Outputs

- standardized strain correlation scores (z-normalized per link)
- standardized IOKR scores (z-normalized per link)
- combined scores (aggregated ℓ₁/₂-norm values)
- ranked link table with all scores and metadata (sortable, filterable columns)
- enrichment statistics for high-scoring link sets (if validation set provided)

## How to apply

First, standardize each scoring function independently by computing the mean and variance across all hypothetical links, then z-normalize: s*_i = (s_i − E[s_i]) / √Var[s_i]. For strain correlation, this is computed as the hypergeometric expected value and variance of raw correlation scores. For IOKR (or other structural scores), standardize identically over the full candidate set. Next, apply the combined scoring function s_combined = sgn(s*_corr)|s*_corr|^(1/2) + sgn(s*_IOKR)|s*_IOKR|^(1/2), which uses the ℓ₁/₂-norm with sign adjustment to preserve directionality and weight each standardized score nonlinearly. Rank all links by combined score in descending order and export as a sortable table. Validate by comparing the enrichment of validated links in the joint 90th percentile for both standardized scores; significant enrichment (p < 0.05) relative to either score alone indicates successful combination.

## Related tools

- **NPLinker** (Framework for constructing hypothetical links, computing standardized scores, and exporting ranked link tables with filtering and visualization) — https://github.com/sdrogers/nplinker
- **BiG-SCAPE** (Clusters BGCs into GCFs prior to link generation; output (GCF assignments) feeds into link construction)
- **GNPS** (Source of metabolomic spectra and molecular family (MF) annotations; provides MF entities for link pairing with GCFs)
- **MIBiG** (Source of BGC structural homology annotations and molecular fingerprints used to compute IOKR scores)

## Evaluation signals

- Standardized scores should have mean ≈ 0 and variance ≈ 1 across all links (z-score properties)
- Validated links should show significantly higher combined score distributions than random/all links (p < 0.05 by Mann–Whitney U or equivalent)
- Links in the joint 90th percentile for both standardized strain correlation AND IOKR should show enrichment of validated links significantly higher than either metric alone (validated enrichment p < 0.05)
- Ranked table should be sortable by each component score and combined score without data loss or rank inversions
- Combined scores should show improved top-n accuracy (proportion of true links in top-n ranked candidates) compared to either individual score

## Limitations

- Standardization assumes the score distributions are stable across the full candidate set; if candidate sets are highly heterogeneous (e.g., different product types, different strain counts), standardization may obscure true differences.
- IOKR scores depend critically on MIBiG homology threshold (cumulative BLAST score ≥10,000); links to novel BGCs without MIBiG matches cannot be scored, restricting applicability.
- ℓ₁/₂-norm combination is not theoretically justified for all score pairs; kernel function and molecular fingerprint choices significantly affect IOKR score quality, which in turn affects combined score reliability.
- Rank stability depends on the quality of input scores; if one scoring function is uninformative or biased, it may degrade combined scores despite standardization.
- Validation set must contain true positive links from the same strains and data sources to avoid bias in enrichment testing.

## Evidence

- [full_text] standardised scores using expected value and variance over the set of all potential links: s*_IOKR = (s_IOKR − E[s_IOKR]) / √Var[s_IOKR]: "standardised scores using expected value and variance over the set of all potential links: s*_IOKR = (s_IOKR − E[s_IOKR]) / √Var[s_IOKR]"
- [full_text] Combine standardised scores using ℓ₁/₂-norm with sign adjustment: s_combined = sgn(s*_corr)|s*_corr|^(1/2) + sgn(s*_IOKR)|s*_IOKR|^(1/2): "Combine standardised scores using ℓ₁/₂-norm with sign adjustment: s_combined = sgn(s*_corr)|s*_corr|^(1/2) + sgn(s*_IOKR)|s*_IOKR|^(1/2)"
- [abstract] using multiple link-scoring functions together makes it easier to prioritise true links relative to others: "using multiple link-scoring functions together makes it easier to prioritise true links relative to others"
- [abstract] they are in fact complementary, and show a way to combine them to improve their performance: "they are in fact complementary, and show a way to combine them to improve their performance"
- [full_text] links scoring in the joint 90th percentile for both standardised strain correlation and IOKR show significantly higher enrichment of validated links (p < 0.05) compared to either score alone: "links scoring in the joint 90th percentile for both standardised strain correlation and IOKR show significantly higher enrichment of validated links (p < 0.05) compared to either score alone"
- [full_text] Rank all hypothetical links by combined score and export as filterable table with sortable columns for each scoring function: "Rank all hypothetical links by combined score and export as filterable table with sortable columns for each scoring function"
- [results] both the IOKR and standardised strain correlation scores are significantly enriched (p-value of 0.0139 and 2.483 × 10−11, respectively) for validated links: "both the IOKR and standardised strain correlation scores are significantly enriched (p-value of 0.0139 and 2.483 × 10−11, respectively) for validated links"
