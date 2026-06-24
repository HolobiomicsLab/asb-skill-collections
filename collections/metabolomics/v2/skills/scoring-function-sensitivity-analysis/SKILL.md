---
name: scoring-function-sensitivity-analysis
description: Use when you have two or more complementary scoring functions (e.g.,
  strain correlation and IOKR scores) that you wish to combine, and you need to determine
  which combination strategy and parameters maximize enrichment of known true links
  in a validation set.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_3520
  tools:
  - antiSMASH
  - Python (numpy, scipy.stats, pandas, matplotlib, seaborn)
  - NPLinker
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1101/2024.10.11.617756
  title: NPLinker
- doi: 10.1371/journal.pcbi.1008920
  title: ''
evidence_spans:
- after downloading the strain assemblies and metabolomics data, the genomes were
  run through antiSMASH v5.0.0 for BGC detection
- genomes were run through antiSMASH v5.0.0 for BGC detection
- NPLinker creates objects for spectra, MFs, BGCs and GCFs in the data set, maintaining
  the hierarchical relationship between them
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

# Scoring-function sensitivity analysis

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Systematically evaluate how parameter choices in scoring function combinations affect enrichment of validated links in BGC-metabolite predictions. This skill determines which combination function (e.g., ℓp-norm with varying exponents, weighted linear combinations, or alternative aggregation methods) best prioritizes true links across multiple datasets.

## When to use

You have two or more complementary scoring functions (e.g., strain correlation and IOKR scores) that you wish to combine, and you need to determine which combination strategy and parameters maximize enrichment of known true links in a validation set. This is especially relevant when individual scoring functions alone show moderate but different performance characteristics, and you suspect combining them could improve link ranking without ground truth guidance on the optimal weighting.

## When NOT to use

- You have only a single scoring function available and no complementary method to combine with it.
- Your validation set is too small (< 20 known true links per dataset) to support reliable enrichment statistics.
- You require real-time ranking and cannot afford the computational cost of evaluating multiple parameter combinations across large link spaces (millions of candidate pairs).

## Inputs

- Standardized strain correlation scores (s'_corr) for all GCF-MF links
- Standardized IOKR scores (s'_IOKR) for all GCF-MF links
- Validated link annotations (binary ground truth labels)
- Multiple datasets with paired genomics and metabolomics (e.g., Crüsemann, Gross, Leão)

## Outputs

- Enrichment ratio heatmaps indexed by parameter (p, α) and function type
- Line plots showing validated-link rank percentile vs. parameter value
- Statistical test results (p-values, chi-square/Fisher exact test statistics)
- Ranked list of validated links using best-performing combination function
- Performance comparison table (top-n accuracy, AUC, enrichment p-values)

## How to apply

Load standardized scores for all candidate GCF-MF or BGC-metabolite links, together with validated link annotations. Compute combined scores across a range of function families and parameters (e.g., ℓp-norm exponents p ∈ [0.5, 3.0], weighted linear combinations α ∈ [0, 1], or Chebyshev/harmonic/geometric means). For each combination, rank all links by combined score and compute the proportion of validated links in high-percentile tiers (e.g., 90th, 95th percentile). Pool results across datasets and apply chi-square or Fisher exact tests to identify statistically significant enrichment (p < 0.05) relative to using either score alone. Visualize enrichment ratios and rank improvements as heatmaps and line plots indexed by parameter and function type, then confirm reproducibility of published results (e.g., ℓ₁/₂-norm performance reported in supplementary tables).

## Related tools

- **NPLinker** (Framework for computing and combining strain correlation and IOKR scores for BGC-metabolite linking) — https://github.com/sdrogers/nplinker
- **antiSMASH** (BGC detection from microbial genomes prior to linking with metabolites)
- **Python (numpy, scipy.stats, pandas, matplotlib, seaborn)** (Numerical computation, statistical testing (chi-square, Fisher exact), and visualization of enrichment heatmaps and sensitivity curves)

## Examples

```
# Compute combined ℓp-norm scores for p in [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency
s_combined = np.sign(s_corr) * np.abs(s_corr)**p + np.sign(s_iokr) * np.abs(s_iokr)**p
ranks = np.argsort(-s_combined)
enrichment_90pctl = np.sum(validated_links[ranks[:int(0.1*len(ranks))]]) / np.sum(validated_links)
pval = chi2_contingency(pd.crosstab(ranks < int(0.1*len(ranks)), validated_links))[1]
```

## Evaluation signals

- Enrichment p-values for best combination function are statistically significant (p < 0.05) and substantially lower than for either individual scoring function alone.
- Validated links show a higher mean combined score than non-validated links, with effect size measurable via standardized difference (e.g., Cohen's d or Mann–Whitney U test).
- Reproducibility check: published results for ℓ₁/₂-norm (Table 4, supplementary Table D) match recomputed enrichment ratios and rank percentiles within acceptable numerical tolerance (< 1% difference).
- Best-performing combination function achieves equal or superior enrichment compared to all three functions reported in the original paper (ℓ₁/₂, weighted linear, Chebyshev).
- Sensitivity curve is smooth across parameter range with a clear local maximum, indicating a well-defined optimum rather than noise or overfitting to a single dataset.

## Limitations

- Optimization is restricted to BGCs with considerable homology to MIBiG entries; novel BGCs or those with only distant relatives will be absent from the training set, limiting IOKR applicability.
- Performance is highly dependent on the choice of molecular fingerprints and kernels used on MS2 spectra; alternative fingerprints or kernels may substantially alter which combination function performs best.
- Test set size may be insufficient to break down performance by BGC product type, so generalization across distinct product classes (PKS, NRPS, etc.) is not guaranteed.
- Results are validated only on three paired omics datasets (Crüsemann, Gross, Leão); transferability to other microbial sources or metabolomics platforms is untested.

## Evidence

- [other] For each dataset, compute combined scores using the ℓ_p-norm formula s_sum = sgn(s'_corr)|s'_corr|^p + sgn(s'_IOKR)|s'_IOKR|^p across a range of p values: "For each dataset, compute combined scores using the ℓ_p-norm formula s_sum = sgn(s'_corr)|s'_corr|^p + sgn(s'_IOKR)|s'_IOKR|^p across a range of p values (0.5 to 3.0 in 0.1 increments, plus"
- [other] For each (p, dataset) combination, rank all GCF-MF links by combined score and compute the proportion of validated links in the 90th and 95th percentile tiers.: "For each (p, dataset) combination, rank all GCF-MF links by combined score and compute the proportion of validated links in the 90th and 95th percentile tiers."
- [other] Pool results across the three datasets and perform significance testing (chi-square or Fisher exact test) to identify which combination functions yield statistically significant enrichment (p < 0.05): "Pool results across the three datasets and perform significance testing (chi-square or Fisher exact test) to identify which combination functions yield statistically significant enrichment (p < 0.05)"
- [other] The ℓ1/2-norm combination function assigned the best rank to validated links in 10 out of 15 cases, including three instances where it substantially outperformed either individual scoring function alone: "The ℓ1/2-norm combination function assigned the best rank to validated links in 10 out of 15 cases, including three instances where it substantially outperformed either individual scoring function"
- [abstract] Using multiple link-scoring functions together makes it easier to prioritise true links relative to others: "We demonstrate that using multiple link-scoring functions together makes it easier to prioritise true links relative to others"
- [abstract] Strain correlation and IOKR scores are complementary and combining them improves performance over either individual approach: "we demonstrate that they are in fact complementary, and show a way to combine them to improve their performance"
- [other] Visualise enrichment ratio and rank improvement (validated link rank percentile) as heatmaps and line plots indexed by p and function type: "Visualise enrichment ratio and rank improvement (validated link rank percentile) as heatmaps and line plots indexed by p and function type."
- [discussion] IOKR is also highly dependent on the choice of both kernel function and molecular fingerprints: "IOKR is also highly dependent on the choice of both kernel function and molecular fingerprints"
