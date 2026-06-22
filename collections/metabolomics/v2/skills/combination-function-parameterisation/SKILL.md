---
name: combination-function-parameterisation
description: Use when you have two or more independent, standardised scoring functions that rank the same set of candidate pairs (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0199
  - http://edamontology.org/topic_3407
  tools:
  - antiSMASH
  - Python (numpy, scipy.stats, pandas, matplotlib, seaborn)
  - NPLinker
derived_from:
- doi: 10.1101/2024.10.11.617756
  title: NPLinker
- doi: 10.1371/journal.pcbi.1008920
  title: ''
evidence_spans:
- after downloading the strain assemblies and metabolomics data, the genomes were run through antiSMASH v5.0.0 for BGC detection
- genomes were run through antiSMASH v5.0.0 for BGC detection
- NPLinker creates objects for spectra, MFs, BGCs and GCFs in the data set, maintaining the hierarchical relationship between them
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

# Combination-function parameterisation

## Summary

Systematically evaluate alternative mathematical combination functions and their parameters to optimally merge complementary scoring functions (e.g. ℓp-norm with varying exponent p) for ranking BGC-metabolite predictions. This skill identifies which combination strategy most enriches validated links in high-ranking tiers.

## When to use

You have two or more independent, standardised scoring functions that rank the same set of candidate pairs (e.g. BGC-metabolite links scored by strain correlation AND IOKR), and you want to determine whether combining them improves ranking of known true pairs, and which combination formula and parameters achieve the best enrichment of validated links in top percentile tiers.

## When NOT to use

- Scoring functions are not standardised to the same scale or distribution (e.g. one is raw count, other is z-score) — standardise first.
- You have only one scoring function — combination requires at least two independent inputs.
- Your goal is to build or train a new scoring function (this skill tunes parameter selection on existing, fixed functions, not learning or feature engineering).

## Inputs

- Standardised scoring matrices (one per scoring function) mapping candidate pairs to real-valued scores
- Validated pair annotations (binary ground-truth labels for which candidate pairs are true links)
- Multiple datasets or a pooled dataset to test robustness across cohorts

## Outputs

- Enrichment ratio heatmaps indexed by combination function type and parameter value
- Rank improvement plots (validated link percentile position) vs. parameter value
- Statistical test results (p-values, chi-square/Fisher exact statistics) comparing each combination strategy to individual scorers
- Ranked list of candidate pairs using the best-performing combination function and parameters

## How to apply

Load pre-computed standardised scores for both functions across all candidate pairs and validated link annotations. Compute combined scores using a parametrised combination formula (e.g. ℓp-norm with p ∈ [0.5, 3.0]) and alternative functions (weighted linear combinations with α ∈ [0, 1], Chebyshev distance, harmonic mean, geometric mean). For each (parameter, function) combination, rank all candidate pairs by combined score and measure the proportion of validated links in the 90th and 95th percentile tiers. Pool results across datasets and perform chi-square or Fisher exact test to identify which combination functions yield statistically significant enrichment (p < 0.05) relative to either score alone. Visualise enrichment ratios and rank improvements as heatmaps indexed by parameter value and function type, then validate that the best performer reproduces or exceeds reported benchmarks.

## Related tools

- **NPLinker** (Framework housing the scoring functions and link ranking pipeline to be optimised via combination-function parameterisation) — https://github.com/NPLinker/nplinker
- **Python (numpy, scipy.stats, pandas, matplotlib, seaborn)** (Numerical computation of combination functions, statistical significance testing, and visualisation of enrichment metrics across parameter ranges)

## Examples

```
s_combined = sgn(s_corr_norm) * np.abs(s_corr_norm)**p + sgn(s_IOKR_norm) * np.abs(s_IOKR_norm)**p; enrichment_ratio = chi2_contingency(validated_in_90th_percentile); results_df.plot(x='p_value', y='enrichment_ratio', kind='line', hue='function_type')
```

## Evaluation signals

- Enrichment ratio (proportion of validated links in 90th/95th percentile) for best combination function exceeds or equals the enrichment of either individual scoring function alone.
- Statistical test p-value for best combination function is < 0.05, indicating significant enrichment relative to random.
- Rank improvement for known validated links (percentile position in combined ranking) is documented; best function should demonstrate substantial uprank (e.g. rank 253 vs. much higher individual ranks, as exemplified in article).
- Reproducibility check: results for the reported best performer (ℓ₁/₂-norm) match or exceed figures in Table 4 and supplementary Table D from the article.
- Heatmap or line plot shows clear, interpretable trend in enrichment as parameter (e.g. p in ℓp-norm) varies, not random noise.

## Limitations

- Reliance on MIBiG homology for ground-truth validation limits applicability to BGCs with considerable homology to database entries; novel BGCs may lack validated link annotations.
- Results are sensitive to the choice of percentile tiers (90th vs. 95th) for measuring enrichment; different tiers may rank functions differently.
- Statistical power is reduced if the proportion of validated links in the candidate set is very low (sparse ground truth), making detection of subtle enrichment differences difficult.
- Combination function performance is data-dependent; parameter values optimised on one dataset (e.g. Crüsemann) may not transfer to another (e.g. Gross, Leão) if scoring distributions differ significantly.

## Evidence

- [other] For each (p, dataset) combination, rank all GCF-MF links by combined score and compute the proportion of validated links in the 90th and 95th percentile tiers.: "For each (p, dataset) combination, rank all GCF-MF links by combined score and compute the proportion of validated links in the 90th and 95th percentile tiers."
- [other] Test alternative combination functions (e.g. weighted linear combinations with α ∈ [0, 1], Chebyshev distance max(|s'_corr|, |s'_IOKR|), harmonic mean, geometric mean) and compute validated-link enrichment ratios for each.: "Test alternative combination functions (e.g. weighted linear combinations with α ∈ [0, 1], Chebyshev distance max(|s'_corr|, |s'_IOKR|), harmonic mean, geometric mean) and compute validated-link"
- [other] Pool results across the three datasets and perform significance testing (chi-square or Fisher exact test) to identify which combination functions yield statistically significant enrichment (p < 0.05) relative to using either score alone.: "Pool results across the three datasets and perform significance testing (chi-square or Fisher exact test) to identify which combination functions yield statistically significant enrichment (p < 0.05)"
- [other] The ℓ1/2-norm combination function assigned the best rank to validated links in 10 out of 15 cases, including three instances where it substantially outperformed either individual scoring function alone (e.g., retimycin A ranked at 253 vs. much higher individual ranks).: "The ℓ1/2-norm combination function assigned the best rank to validated links in 10 out of 15 cases, including three instances where it substantially outperformed either individual scoring function"
- [abstract] we demonstrate that they are in fact complementary, and show a way to combine them to improve their performance: "they are in fact complementary, and show a way to combine them to improve their performance"
- [other] Validation: confirm that results reproduce reported enrichment for ℓ₁/₂ (documented in Table 4 and Table D of supplementary text) and that the best-performing alternative function achieves equal or superior enrichment compared to the three functions reported in the paper.: "confirm that results reproduce reported enrichment for ℓ₁/₂ (documented in Table 4 and Table D of supplementary text) and that the best-performing alternative function achieves equal or superior"
