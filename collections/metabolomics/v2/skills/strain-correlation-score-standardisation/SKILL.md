---
name: strain-correlation-score-standardisation
description: Use when you have computed raw strain correlation scores (based on shared
  strain membership) between genomic and metabolomic objects of heterogeneous sizes,
  and you need to compare link quality fairly across pairs with different numbers
  of strains.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0080
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - antiSMASH
  - BiG-SCAPE
  - GNPS
  - MIBiG
  - NPLinker
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
- the metabolomics data, the genomes were run through antiSMASH v5.0.0 for BGC detection
  and BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs
- we use library MS2 spectra from the public, community-driven GNPS knowledge base
  [33] as a training set for the IOKR model
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

# strain-correlation-score-standardisation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Standardise raw strain correlation scores between gene cluster families (GCFs) and molecular families (MFs) by z-normalizing them against their hypergeometric expectation and variance, enabling fair comparison across links with different GCF and MF sizes. This converts size-biased raw scores into a uniform null distribution where validated links show significantly elevated z-scores.

## When to use

Apply this skill when you have computed raw strain correlation scores (based on shared strain membership) between genomic and metabolomic objects of heterogeneous sizes, and you need to compare link quality fairly across pairs with different numbers of strains. Use it before filtering or ranking hypothetical GCF–MF links in a paired omics analysis, especially if raw score distributions show strong size bias (e.g., large GCFs and MFs inflating scores regardless of true co-occurrence).

## When NOT to use

- Input is already a standardised or z-normalised score (e.g. from a prior analysis) — applying this skill again will double-normalise and destroy interpretability.
- GCF or MF objects lack strain membership annotations or the dataset contains only a single strain — hypergeometric model requires multi-strain populations to compute meaningful expected values and variance.
- Raw score is computed using a non-discrete sampling model (e.g. continuous probability kernel or similarity metric) — hypergeometric standardisation assumes discrete combinatorial sampling and will not reflect the true null distribution.

## Inputs

- raw strain correlation scores for GCF–MF pairs
- GCF sizes (number of strains in each cluster)
- MF sizes (number of strains in each family)
- overlap counts (number of shared strains per pair)
- population size (total number of strains in dataset)

## Outputs

- standardised strain correlation z-scores (s*_corr) for all GCF–MF pairs
- expected value and variance tables for hypergeometric distributions
- comparative score distributions (validated links vs. all links)
- t-test p-values and effect sizes demonstrating improved separation

## How to apply

For each GCF–MF pair, extract the GCF size (#G), MF size (#m), overlap size (#(G∩M)), and population size (#N). Compute the expected value E[σ_corr(M,G)] and variance Var[σ_corr(M,G)] of the raw strain correlation score under the hypergeometric distribution over all possible overlap sizes k, where p(o=k) follows the hypergeometric with parameters N, m, g, and the observed overlap. Calculate the standardised z-score as s*_corr = (σ_corr(M,G) − E[σ_corr(M,G)]) / √Var[σ_corr(M,G)]. Verify standardisation improves discrimination between validated and all-links populations by comparing effect size (mean difference and p-value from t-test); validated links should show a mean z-score near +3.67 while all links cluster near 0, with p < 10^−10.

## Related tools

- **NPLinker** (orchestrates loading of GCF and MF objects, maintains strain annotations, and wraps standardised correlation scoring into its link-ranking pipeline) — https://github.com/sdrogers/nplinker
- **BiG-SCAPE** (clusters antiSMASH BGCs into GCFs, enabling GCF-level strain membership aggregation)
- **GNPS** (provides spectral clustering output (molecular families) with strain annotations for MF membership)
- **antiSMASH** (detects BGCs in microbial genomes, providing the genomic input to BiG-SCAPE clustering)

## Examples

```
from nplinker.scoring import compute_strain_correlation; s_corr = compute_strain_correlation(gcf, mf); expected_val, variance = hypergeometric_moments(N, m, g, overlap); s_standardised = (s_corr - expected_val) / sqrt(variance)
```

## Evaluation signals

- Mean standardised score for all links is near 0 (e.g. −0.0060) and for validated links is significantly elevated (e.g. +3.6717); asymmetry indicates successful size-bias removal.
- T-test p-value comparing validated and all-links populations is < 10^−10 (e.g. p = 6.83 × 10^−64 in the article), indicating strong separation; raw score p-values are typically much weaker (e.g. p = 0.0001) and non-significant after multiple-testing correction.
- Standardised score distributions show minimal skew and approximately symmetric spread around the mean for all-links population, consistent with a standard normal distribution.
- Histograms and boxplots comparing raw vs. standardised scores show that validated links occupy the upper tail of the standardised distribution while distributed across the middle range of raw scores.
- Hypergeometric expected value and variance calculations are internally consistent: for any pair, E[σ_corr] should fall within the range of possible overlap values, and variance should be positive and finite.

## Limitations

- Requires complete strain membership metadata for all GCFs and MFs; missing or sparse strain annotations will bias the hypergeometric expectation and produce unreliable z-scores.
- Hypergeometric model assumes all strains are equally likely to be sampled and that co-occurrence is governed purely by random chance under population mixing; violations (e.g. evolutionary relatedness, ecological co-isolation) will make z-scores over- or under-estimate true significance.
- Standardisation is specific to the dataset in which it is computed; transferring z-scores to a new dataset with different strain distributions, GCF compositions, or MF sizes will invalidate the hypergeometric parameters and produce non-comparable scores.
- Z-score interpretation assumes large sample size and approximately normal null distribution; with very small GCFs, MFs, or populations, the hypergeometric distribution may be skewed and z-scores may not calibrate correctly.
- Standardisation alone does not improve link validation sensitivity; it only removes size bias and improves comparability — true positive discovery still depends on sufficient strain co-occurrence signal and appropriate downstream filtering thresholds.

## Evidence

- [results] raw strain correlation score distribution is heavily size-biased (larger GCFs and MFs inflating scores): "raw score's means of 83.5144 and 14.6667 respectively, demonstrating that standardisation successfully enables comparison across links with different GCF and MF sizes"
- [results] hypergeometric model and z-normalisation procedure for standardisation: "For each GCF-MF pair, compute expected value E[σ_corr(M,G)] and variance Var[σ_corr(M,G)] using hypergeometric distribution over all possible overlap sizes k, where p(o=k) follows hypergeometric with"
- [results] standardised score formula and effect of standardisation on validated link discrimination: "Calculate standardised correlation score s*_corr = (σ_corr(M,G) - E[σ_corr(M,G)]) / √Var[σ_corr(M,G)] for all links. The standardised correlation score achieves a mean of -0.0060 for all links and"
- [abstract] purpose of standardisation in the broader NPLinker framework: "Based on standardising a commonly used score, we introduce a new, more effective score"
- [results] practical workflow for computing standardised scores on real microbial datasets: "Load raw strain correlation scores for all GCF-MF pairs in each dataset (Crüsemann, Gross, Leão), extracting GCF sizes (#G), MF sizes (#m), overlap sizes (#(G∩M)), and population size (#N)"
- [results] validation approach comparing standardised and raw score distributions: "Generate distributions (histograms and boxplots) comparing raw versus standardised scores for validated links versus all links across the three datasets"
