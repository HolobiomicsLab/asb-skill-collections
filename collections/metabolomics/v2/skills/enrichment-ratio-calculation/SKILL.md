---
name: enrichment-ratio-calculation
description: Use when after generating combined or alternative scores for a set of BGC-metabolite (GCF-MF) link candidates, you need to evaluate whether a scoring function preferentially ranks true validated links higher than spurious ones.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0080
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3407
  tools:
  - antiSMASH
  - Python (numpy, scipy.stats, pandas, matplotlib, seaborn)
  - numpy
  - scipy.stats
  - pandas
  - matplotlib / seaborn
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

# enrichment-ratio-calculation

## Summary

Calculate the proportion of validated genomic-metabolomic links in ranked prediction tiers (e.g., 90th or 95th percentile) to quantify whether a scoring function enriches for true positive links relative to the background of all hypothetical links. This enables statistical comparison of alternative combination functions and identification of which parameters or function types yield significant enrichment.

## When to use

After generating combined or alternative scores for a set of BGC-metabolite (GCF-MF) link candidates, you need to evaluate whether a scoring function preferentially ranks true validated links higher than spurious ones. Specifically, when you have: (1) a population of all possible GCF-MF pairs with computed scores; (2) a set of annotated validated links within that population; and (3) a goal to compare multiple scoring functions or parameter choices (e.g., different ℓp-norm exponents) to identify which maximizes the proportion of true positives in high-scoring tiers.

## When NOT to use

- When validated link annotations are missing or sparse; enrichment statistics require sufficient labeled positive and negative examples to be meaningful.
- When comparing scoring functions on a single dataset without replication; pooling across multiple datasets (Crüsemann, Gross, Leão) is necessary for robust statistical testing (p < 0.05).
- When the goal is to rank individual links for a user-facing prediction tool; use the best-performing combination function directly rather than computing enrichment ratios for every candidate link.

## Inputs

- all GCF-MF link pairs with computed standardised scores (e.g., s'_corr, s'_IOKR, or combined s_sum)
- annotation file mapping GCF-MF pairs to validation status (validated vs. unvalidated)
- ranked link list sorted by scoring function output (descending)

## Outputs

- enrichment ratio table (function type × parameter × dataset) quantifying fold-enrichment for validated links
- proportion of validated links in 90th and 95th percentile tiers for each function and dataset
- p-value matrix from chi-square or Fisher exact test comparing enrichment across functions
- rank improvement metrics (e.g., percentile rank of validated links under each function)

## How to apply

For each scoring function and (parameter, dataset) combination: (1) rank all GCF-MF links by computed score in descending order; (2) define enrichment tiers at the 90th and 95th percentile thresholds (i.e., top 10% and top 5% of links by score); (3) count the number of validated links present in each tier and compute the proportion as (validated links in tier) / (total links in tier); (4) compute the enrichment ratio by dividing this proportion by the baseline proportion of validated links across all hypothetical links; (5) pool results across datasets and perform chi-square or Fisher exact test (p < 0.05) to test statistical significance of enrichment relative to using either individual score alone; (6) visualize enrichment ratios as heatmaps indexed by function type and parameter (e.g., p value for ℓp-norm), highlighting functions that achieve equal or superior enrichment compared to the baseline (ℓ₁/₂-norm reported in the paper).

## Related tools

- **numpy** (vectorized computation of proportions and ranking statistics across large link sets)
- **scipy.stats** (chi-square and Fisher exact test for significance testing of enrichment ratios across function types)
- **pandas** (tabular organization and aggregation of enrichment results by function, parameter, and dataset)
- **matplotlib / seaborn** (visualization of enrichment ratio heatmaps and rank improvement line plots indexed by p and function type)

## Examples

```
import pandas as pd; from scipy.stats import chi2_contingency; validated = df[df['is_validated']==True]; tier_90 = df[df['rank_percentile'] >= 90]; enrichment_ratio = (len(validated[validated['rank_percentile'] >= 90]) / len(tier_90)) / (len(validated) / len(df)); chi2, p_val, dof, expected = chi2_contingency(pd.crosstab(df['function_type'], df['is_validated'])); print(f'Enrichment ratio: {enrichment_ratio:.3f}, p-value: {p_val:.2e}')
```

## Evaluation signals

- Enrichment ratio for the ℓ₁/₂-norm baseline function reproduces Table 4 and Table D from supplementary text; if not, the calculation pipeline contains errors.
- All enrichment ratios are ≥ 1.0 (or ≤ 1.0 if negative enrichment); negative ratios indicate the scoring function ranks validated links lower than chance, signaling a poor function.
- P-values from chi-square/Fisher exact test are < 0.05 for functions identified as significantly enriched; p ≥ 0.05 indicates no statistical evidence of enrichment over individual scores alone.
- Validated links appearing in the enrichment tier have higher mean scores than unvalidated links; median or quartile distributions should show clear separation.
- The best-performing alternative function achieves enrichment equal to or exceeding the ℓ₁/₂-norm baseline; if all alternatives underperform, the baseline is confirmed as optimal.

## Limitations

- Enrichment statistics are sensitive to the choice of percentile threshold (90th vs. 95th); tiers are arbitrary and may mask fine-grained ranking performance differences.
- Pooling results across three datasets (Crüsemann, Gross, Leão) assumes homogeneous data properties; dataset-specific effects (e.g., strain representation, metabolite diversity) may not be detected.
- Chi-square and Fisher exact tests assume independence of tested links; true links from the same strain may be correlated, violating test assumptions.
- Validated link annotations are sparse relative to the total number of hypothetical links, leading to low absolute counts in enrichment tiers and reduced statistical power.

## Evidence

- [other] For each (p, dataset) combination, rank all GCF-MF links by combined score and compute the proportion of validated links in the 90th and 95th percentile tiers.: "For each (p, dataset) combination, rank all GCF-MF links by combined score and compute the proportion of validated links in the 90th and 95th percentile tiers."
- [other] Pool results across the three datasets and perform significance testing (chi-square or Fisher exact test) to identify which combination functions yield statistically significant enrichment (p < 0.05) relative to using either score alone.: "Pool results across the three datasets and perform significance testing (chi-square or Fisher exact test) to identify which combination functions yield statistically significant enrichment (p < 0.05)"
- [results] both the IOKR and standardised strain correlation scores are significantly enriched (p-value of 0.0139 and 2.483 × 10−11, respectively) for validated links: "both the IOKR and standardised strain correlation scores are significantly enriched (p-value of 0.0139 and 2.483 × 10−11, respectively) for validated links"
- [other] The ℓ1/2-norm combination function assigned the best rank to validated links in 10 out of 15 cases, including three instances where it substantially outperformed either individual scoring function alone: "The ℓ1/2-norm combination function assigned the best rank to validated links in 10 out of 15 cases, including three instances where it substantially outperformed either individual scoring function"
- [other] Visualise enrichment ratio and rank improvement (validated link rank percentile) as heatmaps and line plots indexed by p and function type.: "Visualise enrichment ratio and rank improvement (validated link rank percentile) as heatmaps and line plots indexed by p and function type."
