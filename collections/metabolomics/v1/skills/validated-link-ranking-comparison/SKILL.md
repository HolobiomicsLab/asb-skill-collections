---
name: validated-link-ranking-comparison
description: Use when when you have computed multiple independent scoring functions (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3697
  tools:
  - antiSMASH
  - Python (numpy, scipy.stats, pandas, matplotlib, seaborn)
  - NPLinker
  - scipy.stats
  - pandas
  - matplotlib / seaborn
derived_from:
- doi: 10.1371/journal.pcbi.1008920
  title: NPLinker
evidence_spans:
- after downloading the strain assemblies and metabolomics data, the genomes were run through antiSMASH v5.0.0 for BGC detection
- genomes were run through antiSMASH v5.0.0 for BGC detection
- NPLinker creates objects for spectra, MFs, BGCs and GCFs in the data set, maintaining the hierarchical relationship between them
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

# validated-link-ranking-comparison

## Summary

Systematically compare ranking performance of different BGC–metabolite scoring functions by measuring their ability to place experimentally validated links in top percentiles of predictions, then select the function(s) that statistically enrich for true positives. This skill bridges computational prediction with experimental ground truth to optimize link prioritization.

## When to use

When you have computed multiple independent scoring functions (e.g., strain correlation, IOKR, or other sequence/spectral features) for the same set of BGC–metabolite candidate pairs, and you possess a curated set of experimentally validated links (from MIBiG, manual curation, or other sources). Use this skill to decide which scoring function or combination thereof should be trusted for ranking predictions in new, unvalidated datasets.

## When NOT to use

- Input scoring functions are from a single strain or single dataset only (no independent validation cohort available).
- Validated links are absent, sparse (< 5% of total links), or unreliable (e.g., not manually curated or derived from weak homology).
- Scoring functions have not been standardized to a comparable scale (e.g., one is raw correlation, another is log-probability); standardization step must precede ranking comparison.

## Inputs

- Standardized strain correlation scores (s'_corr) for all GCF–MF pairs
- Standardized IOKR scores (s'_IOKR) for all GCF–MF pairs
- Validated link annotations (Boolean or set membership)
- Multi-dataset results (at least one independent validation cohort)

## Outputs

- Enrichment ratio (proportion of validated links in top percentile vs. baseline)
- Significance p-values (chi-square or Fisher exact test) for each scoring function
- Rank percentile distribution of validated links for each function
- Recommendation for best-performing scoring function or combination
- Visualization heatmaps/line plots indexed by function type and parameter

## How to apply

Load pre-computed scores for all hypothetical BGC–metabolite links alongside validated link annotations. For each scoring function (or parameterized variant, e.g., ℓp-norm with different p values), rank all links by score and compute the proportion of validated links in the 90th and 95th percentile tiers. Pool results across independent datasets (e.g., Crüsemann, Gross, Leão) and perform significance testing (chi-square or Fisher exact test) to identify which functions yield statistically significant enrichment (p < 0.05) relative to random or baseline functions. Visualize enrichment ratios and rank percentile improvements as heatmaps or line plots. Validate reproduction of known results (e.g., reported ℓ₁/₂-norm enrichment in supplementary tables) before finalizing the choice of scoring function.

## Related tools

- **NPLinker** (Framework for loading, standardizing, and combining BGC and metabolite scores; implements ℓp-norm and alternative combination functions) — https://github.com/sdrogers/nplinker
- **scipy.stats** (Performs chi-square and Fisher exact tests to assess statistical significance of enrichment ratios across datasets)
- **pandas** (Loads and manipulates score tables, validated link annotations, and facilitates per-dataset and pooled enrichment calculations)
- **matplotlib / seaborn** (Visualizes enrichment ratios and rank improvements as heatmaps and line plots indexed by parameter (p value, function type))

## Examples

```
import pandas as pd; from scipy.stats import chi2_contingency; scores_df = pd.read_csv('combined_scores.csv'); validated = pd.read_csv('validated_links.csv'); top_90pct = scores_df[scores_df['rank_percentile'] >= 90]; contingency = [[len(top_90pct[top_90pct['is_validated']]), len(top_90pct[~top_90pct['is_validated']])], [len(scores_df[scores_df['rank_percentile'] < 90][scores_df['is_validated']]), len(scores_df[scores_df['rank_percentile'] < 90][~scores_df['is_validated']])]]; chi2, p_val, dof, expected = chi2_contingency(contingency); print(f'Enrichment p-value: {p_val}')
```

## Evaluation signals

- Reproduced enrichment statistics match published supplementary tables (e.g., Table 4, Table D) for known scoring functions (ℓ₁/₂-norm, weighted linear, Chebyshev) within numerical tolerance.
- Pooled chi-square/Fisher exact p-values for at least one scoring function are < 0.05, indicating statistically significant enrichment of validated links above random baseline.
- Rank percentile distributions show validated links skewed toward higher percentiles (90th, 95th) compared to background distribution of all links; mean rank percentile for validated links > 80th percentile.
- Heatmaps or line plots show monotonic or unimodal trend (e.g., enrichment improving then plateauing with ℓp exponent), not flat or erratic variation, indicating stable function behavior across parameter ranges.
- Best-performing function achieves equal or superior enrichment ratio (validated links in top percentile) compared to individual scoring functions alone, confirming synergy from combination.

## Limitations

- Requires sufficient validated links per dataset (< 5% of total links may yield unstable estimates); insufficient test set size limits breakdown by product type or strain.
- Enrichment comparison is conditional on the quality and completeness of validated link annotations; missing true positives in the ground truth will bias rankings.
- Results generalize only to BGCs and metabolites within the training/validation dataset scope; applicability to novel product classes or strains with low MIBiG homology is restricted.
- Choice of percentile threshold (90th, 95th) and statistical test (chi-square vs. Fisher exact) can influence conclusions; sensitivity analysis on thresholds is recommended.
- Ranking comparison assumes independence of scoring functions; highly correlated functions will not reveal complementarity, and combining them may not improve enrichment.

## Evidence

- [other] For each (p, dataset) combination, rank all GCF-MF links by combined score and compute the proportion of validated links in the 90th and 95th percentile tiers.: "For each (p, dataset) combination, rank all GCF-MF links by combined score and compute the proportion of validated links in the 90th and 95th percentile tiers."
- [other] Pool results across the three datasets and perform significance testing (chi-square or Fisher exact test) to identify which combination functions yield statistically significant enrichment (p < 0.05) relative to using either score alone.: "Pool results across the three datasets and perform significance testing (chi-square or Fisher exact test) to identify which combination functions yield statistically significant enrichment (p < 0.05)"
- [other] The ℓ₁/₂-norm combination function assigned the best rank to validated links in 10 out of 15 cases, including three instances where it substantially outperformed either individual scoring function alone (e.g., retimycin A ranked at 253 vs. much higher individual ranks).: "The ℓ₁/₂-norm combination function assigned the best rank to validated links in 10 out of 15 cases, including three instances where it substantially outperformed either individual scoring function"
- [results] both the IOKR and standardised strain correlation scores are significantly enriched (p-value of 0.0139 and 2.483 × 10−11, respectively) for validated links: "both the IOKR and standardised strain correlation scores are significantly enriched (p-value of 0.0139 and 2.483 × 10−11, respectively) for validated links"
- [results] Standardised correlation score mean for all links: -0.0060; for validated links: 3.6717 (p=6.8302 × 10−64): "Standardised correlation score mean for all links: -0.0060; for validated links: 3.6717 (p=6.8302 × 10−64)"
- [abstract] We demonstrate that using multiple link-scoring functions together makes it easier to prioritise true links relative to others: "using multiple link-scoring functions together makes it easier to prioritise true links relative to others"
