---
name: complementary-score-integration
description: Use when when you have scored a set of potential gene cluster family (GCF)–molecular feature (MF) links using two or more orthogonal methods (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3765
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - NPLinker
  - antiSMASH
  - BiG-SCAPE
  - MIBiG
  - GNPS
derived_from:
- doi: 10.1101/2024.10.11.617756
  title: NPLinker
- doi: 10.1371/journal.pcbi.1008920
  title: ''
evidence_spans:
- NPLinker creates objects for spectra, MFs, BGCs and GCFs in the data set, maintaining the hierarchical relationship between them
- Finally, we present NPLinker, a software framework to link genomic and metabolomic data
- After downloading the strain assemblies and metabolomics data, the genomes were run through antiSMASH v5.0.0 for BGC detection
- and BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs
- BiG-SCAPE clusters the BGCs separately by product type
- antiSMASH to score the correspondence between the MIBiG entries and the detected BGCs
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

# complementary-score-integration

## Summary

Combine multiple independent scoring functions (e.g., strain correlation and IOKR) into a unified ranking to identify high-confidence genomic-metabolomic links by exploiting their complementary strengths. This skill detects validated links that neither score alone would rank equally well, improving prioritization of true BGC-spectrum associations.

## When to use

When you have scored a set of potential gene cluster family (GCF)–molecular feature (MF) links using two or more orthogonal methods (e.g., presence/absence correlation patterns and machine-learned fingerprint similarity), and you want to prioritize links that rank highly on both rather than either alone. Use this skill when single-method ranking produces too many false positives or fails to capture links that multiple independent signals support.

## When NOT to use

- When you have only a single scoring method: dual-score integration requires at least two independent scoring approaches to extract complementarity.
- When one of your scores is strongly correlated with another: redundant scores do not provide independent evidence and may not improve prioritization.
- When validation data is too sparse (e.g., < 20 validated links total): statistical power to detect enrichment is insufficient for reliable p-value estimates.

## Inputs

- Preprocessed GCF-MF link scores from two or more independent scoring methods (e.g., standardised strain correlation scores and IOKR scores)
- Validation labels for a subset of links (known true BGC-spectrum pairs)
- Percentile thresholds for each score (e.g., 90th percentile)

## Outputs

- Combined ranking of GCF-MF links ordered by integrated score
- Partition of links into categories (dual-high, single-score high, below threshold)
- Enrichment statistics (proportions of validated links per category, Fisher exact test p-values)

## How to apply

Standardize each scoring function independently by subtracting its mean and dividing by variance, so scores become comparable across different scales and distributions. Identify links that exceed a joint threshold (e.g., 90th percentile) on both standardized scores. Combine standardized scores using a symmetric function (e.g., ℓ₁ norm with sign preservation: s_sum = sgn(s_corr)|s_corr| + sgn(s_IOKR)|s_IOKR|) to rank links by their dual-score strength. Validate the enrichment for known links by computing Fisher exact test p-values comparing the proportion of validated links in the dual-high category to single-score categories. Links scoring high on both standardized metrics show significantly higher enrichment (p < 0.001) for validated associations compared to links exceeding either score alone.

## Related tools

- **NPLinker** (Orchestrates the full genomic-metabolomic linking pipeline; scores GCF-MF links and integrates them for ranked output) — https://github.com/sdrogers/nplinker
- **antiSMASH** (Detects BGCs from microbial genomes; output fed into BiG-SCAPE for GCF clustering prior to scoring)
- **BiG-SCAPE** (Clusters BGCs into GCFs using homology; defines the genomic feature space over which strain correlation is computed)
- **GNPS** (Provides training spectra and molecular fingerprints for IOKR model; source of metabolomic features in the MF space)
- **MIBiG** (Reference database of characterized BGCs; used by IOKR to assign molecular structures and fingerprints for BGC-spectrum linking)

## Evaluation signals

- Dual-high links (≥90th percentile on both scores) show significantly enriched proportion of validated links (p < 0.05 by Fisher exact test) compared to single-score categories.
- Combined score ranking recovers known validated links at higher ranks (top-n accuracy) than either single score alone.
- The integrated score produces a monotonic relationship between score rank and validated-link proportion when links are binned by combined score quartiles or deciles.
- Cross-dataset consistency: enrichment pattern (p-values, proportions) is reproducible across independent datasets (Crüsemann, Gross, Leão).
- Standardization check: mean of standardized scores ≈ 0 and variance ≈ 1 for each method; no systematic bias introduced by centering and scaling.

## Limitations

- Strain correlation-based scoring cannot distinguish between links showing identical patterns of strain co-occurrence, even if their magnitudes differ; standardization mitigates but does not eliminate this ambiguity.
- IOKR scoring is restricted to BGCs with significant homology to MIBiG; novel or divergent BGC families without reference structures cannot be reliably scored via IOKR fingerprints.
- Performance depends critically on kernel choice and parameters in IOKR; insufficient characterization of how kernel selection affects combined-score performance limits generalization to new datasets.
- Percentile thresholds (e.g., 90th) are data-dependent and may not be optimal across datasets with different link distributions; manual threshold tuning may be required.

## Evidence

- [abstract] Strain correlation and IOKR scores are complementary: "we introduce a method for combining their scores into a single scoring function for genomic and metabolomic links, which shows improved performance over either of the individual approaches"
- [results] Joint threshold enrichment improves validated link detection: "the set of links scoring above the 90th percentile on both scores is significantly enriched compared to the set that exceed either of the individual scores (p-value of 2.633 × 10−4 and 0.0208"
- [results] Standardization formula and rationale: "Standardising the score gives a mean score of -0.006 for all links, and 3.672 for validated links, (p=6.8302 × 10−64)"
- [results] Combined scoring function definition: "Our combined scoring function is therefore s_sum = sgn(s_corr)|s_corr| + sgn(s_IOKR)|s_IOKR|"
- [abstract] Correlation score non-comparability motivates standardization: "the most popular strain correlation score has properties that make it impossible to reliably compare score values across links (even links from the same GCF or MF), severely limiting the scores"
- [results] Workflow step: partition links by dual-score membership: "Partition links into four categories: above 90th percentile for standardised correlation only, above 90th percentile for IOKR only, above 90th percentile for both scores, and below 90th percentile"
- [results] Statistical test for enrichment: "Pool data across all three datasets and compute Fisher exact test p-values comparing the proportion of validated links in the dual-score (both scores ≥90th percentile) category to each single-score"
