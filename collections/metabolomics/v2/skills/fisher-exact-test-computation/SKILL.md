---
name: fisher-exact-test-computation
description: Use when you have partitioned genomic-metabolomic links into discrete categories (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3316
  - http://edamontology.org/topic_0091
  tools:
  - NPLinker
  - antiSMASH
  - BiG-SCAPE
  - MIBiG
  - GNPS
  - Python scipy.stats.fisher_exact or R stats::fisher.test
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# fisher-exact-test-computation

## Summary

Compute Fisher exact test p-values to statistically compare the proportion of validated links across categorized link sets, determining whether dual-score enrichment (links exceeding multiple scoring thresholds) is significantly different from single-score enrichment. This enables rigorous hypothesis testing of complementary scoring approach performance.

## When to use

You have partitioned genomic-metabolomic links into discrete categories (e.g., above 90th percentile for score A only, score B only, both scores, or neither) and need to test whether the proportion of validated links differs significantly between categories—particularly when comparing a dual-threshold (combined) category against single-threshold or baseline categories.

## When NOT to use

- Input is continuous score data rather than categorical counts—use rank-based tests (Mann–Whitney U) or regression instead.
- Sample sizes are very large (>1000 per cell) and expected frequencies are all >5; a χ² test may be more efficient.
- You seek to rank individual links rather than compare category proportions—use threshold-filtering or scoring directly.

## Inputs

- Partitioned link categories with counts: {validated_in_category, total_in_category} per category
- Link categorization scheme: e.g., [both_scores_≥90th_percentile, score_A_only_≥90th_percentile, score_B_only_≥90th_percentile, both_scores_<90th_percentile]
- Pooled or per-dataset contingency tables

## Outputs

- Fisher exact test p-values comparing dual-score category to single-score categories
- Proportions of validated links per category
- Statistical comparison table (e.g., Table 2 format: proportions and p-values across datasets and pooled analysis)

## How to apply

For each link category, compute the proportion of validated links (number of validated links in category / total links in category). Pool data across datasets (e.g., Crüsemann, Gross, Leão) to increase statistical power. Use Fisher exact test to compare the proportion of validated links in the dual-score category (links scoring ≥90th percentile on both standardised strain correlation AND IOKR) against each single-score category. Report two-tailed p-values; significance is typically assessed at α = 0.05. The rationale is that Fisher exact test is appropriate for small sample sizes and categorical (2×2 contingency table) data, making it ideal for validating whether combining independent scoring functions genuinely enriches for true links relative to using either score alone.

## Related tools

- **NPLinker** (Framework that generates partitioned GCF-MF link categories and scores (strain correlation, IOKR) on which Fisher test is applied) — https://github.com/sdrogers/nplinker
- **Python scipy.stats.fisher_exact or R stats::fisher.test** (Computes Fisher exact test p-values and contingency statistics)

## Examples

```
from scipy.stats import fisher_exact; contingency = [[validated_dual, non_validated_dual], [validated_single, non_validated_single]]; oddsratio, pvalue = fisher_exact(contingency, alternative='two-sided'); print(f'Fisher p-value: {pvalue}')
```

## Evaluation signals

- P-values for dual-score category vs. single-score categories are computed correctly from 2×2 contingency tables (validated/non-validated × in_category/not_in_category).
- Proportions are calculated correctly: validated_in_category / total_in_category for each category, matching Table 2 reported values.
- P-values from pooled analysis match or corroborate per-dataset p-values; pooling should yield smaller p-values if effect is consistent.
- Dual-score p-value is significantly smaller than single-score p-values, demonstrating enrichment; reported p-values are 2.633 × 10⁻⁴ (IOKR) and 0.0208 (standardised strain correlation) in the article.
- Results are reproducible across all three datasets (Crüsemann, Gross, Leão) and tabulated in comparable structure to reported findings.

## Limitations

- Fisher exact test requires categorical data (counts); if scores are continuous, thresholding introduces information loss and the choice of threshold (e.g., 90th percentile) affects statistical power and conclusions.
- Test assumes independence of observations; if links share underlying biological structure (e.g., same BGC or metabolite cluster), multiple testing correction may be needed.
- Small sample sizes in individual link categories can reduce power; pooling across datasets helps but may mask dataset-specific effects.
- Fisher exact test is one-tailed by default in some implementations; two-tailed p-values must be explicitly requested or computed to avoid underestimating significance.

## Evidence

- [results] Links scoring above the 90th percentile on both standardised strain correlation and IOKR scores are significantly enriched for validated links (p-value 2.633 × 10−4 from IOKR and 0.0208 from standardised strain correlation): "the set of links scoring above the 90th percentile on both scores is significantly enriched compared to the set that exceed either of the individual scores (p-value of 2.633 × 10−4 and 0.0208"
- [other] For each category, compute the proportion of validated links (number of validated links in category / total links in category). Pool data across all three datasets and compute Fisher exact test p-values.: "For each category, compute the proportion of validated links (number of validated links in category / total links in category). 5. Pool data across all three datasets and compute Fisher exact test"
- [other] Tabulate results showing proportions and p-values for all three datasets and pooled analysis, matching the structure and values reported in Table 2.: "Tabulate results showing proportions and p-values for all three datasets and pooled analysis, matching the structure and values reported in Table 2"
- [other] Fisher exact test p-values comparing the proportion of validated links in the dual-score (both scores ≥90th percentile) category to each single-score category.: "compute Fisher exact test p-values comparing the proportion of validated links in the dual-score (both scores ≥90th percentile) category to each single-score category"
- [other] Partition links into four categories: above 90th percentile for standardised correlation only, above 90th percentile for IOKR only, above 90th percentile for both scores, and below 90th percentile for both.: "Partition links into four categories: above 90th percentile for standardised correlation only, above 90th percentile for IOKR only, above 90th percentile for both scores, and below 90th percentile"
