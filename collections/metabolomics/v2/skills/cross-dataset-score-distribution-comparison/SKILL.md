---
name: cross-dataset-score-distribution-comparison
description: 'Use when when you have applied multiple scoring functions (e.g., strain
  correlation and IOKR) to rank genomic-metabolomic (GCF-MF or BGC-spectrum) links
  and need to verify that: (1) standardisation produces zero mean and unit variance
  across all links;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3937
  edam_topics:
  - http://edamontology.org/topic_0203
  - http://edamontology.org/topic_3697
  - http://edamontology.org/topic_0080
  tools:
  - antiSMASH
  - BiG-SCAPE
  - MIBiG
  - GNPS
  - NPLinker
  - Paired Omics Data Platform (PoDP)
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1101/2024.10.11.617756
  title: NPLinker
- doi: 10.1371/journal.pcbi.1008920
  title: ''
evidence_spans:
- After downloading the strain assemblies and metabolomics data, the genomes were
  run through antiSMASH v5.0.0 for BGC detection
- and BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs
- BiG-SCAPE clusters the BGCs separately by product type
- antiSMASH to score the correspondence between the MIBiG entries and the detected
  BGCs
- the MIBiG database [32] has emerged as a central repository of characterised microbial
  BGCs
- this way, we built a set of known BGC-spectrum pairs. To avoid etabolites based
  on properties absent from an MS2 spectrum,
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

# cross-dataset-score-distribution-comparison

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Compute and compare mean, variance, and statistical significance of standardised genomic-metabolomic link scores (strain correlation and IOKR) across multiple datasets to validate score standardisation and assess complementarity of scoring functions. This skill detects whether standardisation successfully removes systematic bias and whether combined scores enrich for validated links.

## When to use

When you have applied multiple scoring functions (e.g., strain correlation and IOKR) to rank genomic-metabolomic (GCF-MF or BGC-spectrum) links and need to verify that: (1) standardisation produces zero mean and unit variance across all links; (2) standardised scores significantly enrich validated links relative to unvalidated ones; (3) complementary scoring functions improve ranking when combined. Apply this skill across at least 2–3 paired genomics–metabolomics datasets (e.g., from Paired Omics Data Platform) with known validated links to establish reproducibility and robustness.

## When NOT to use

- If you have only a single dataset with validated links; cross-dataset comparison requires at least 2 independent datasets to assess reproducibility.
- If raw scores have not been computed yet; this skill assumes raw scores, expected values, and variances are already in hand.
- If you lack a set of experimentally validated links for ground truth; without validated examples, enrichment tests cannot be performed.

## Inputs

- Raw strain correlation scores for all GCF-MF link pairs in a dataset
- Raw IOKR scores for all BGC-spectrum link pairs
- Expected value and variance of raw scores under null hypothesis (hypergeometric distribution)
- Set of experimentally validated GCF-MF or BGC-spectrum links (ground truth)
- Multiple paired genomics–metabolomics datasets (≥2, ideally from Paired Omics Data Platform)

## Outputs

- Standardised strain correlation score distribution (mean, variance, std dev)
- Standardised IOKR score distribution (mean, variance, std dev)
- P-values for enrichment of validated links in each standardised score
- Combined score (ℓp norm) and its enrichment p-value
- Cross-dataset comparison table showing consistency of score statistics and p-values

## How to apply

For each dataset, compute the raw score distribution (mean, variance) across all potential GCF-MF or BGC-spectrum pairs. Standardise each score as s* = (s − E[s]) / √Var[s] to yield zero mean and unit variance. Report standardised score statistics (mean, standard deviation) separately for all links and for the validated link subset. Perform statistical significance testing (e.g., hypergeometric test or Mann–Whitney U) to quantify enrichment of validated links in the standardised score distribution. Compare these statistics across datasets to confirm consistency and reproducibility. Finally, combine standardised scores using an ℓp norm (e.g., s_sum = sgn(s_corr)|s_corr|^p + sgn(s_IOKR)|s_IOKR|^p) and test whether the combined score shows greater enrichment (lower p-value) for validated links than either score alone.

## Related tools

- **NPLinker** (Framework for integrating genomic and metabolomic data and computing raw link scores (strain correlation and IOKR) across datasets) — https://github.com/sdrogers/nplinker
- **antiSMASH** (Detects biosynthetic gene clusters (BGCs) from microbial genomes; output used as input to strain correlation scoring)
- **BiG-SCAPE** (Clusters BGCs into Gene Cluster Families (GCFs); GCF membership defines strain correlation score computation)
- **GNPS** (Public repository of MS2 spectra and IOKR training data; metabolomic features scored against GCFs)
- **MIBiG** (Reference database of characterized BGCs; provides homology information for IOKR molecular fingerprint assignment)
- **Paired Omics Data Platform (PoDP)** (Source of paired genomics and metabolomics datasets with experimentally validated GCF-MF links (ground truth))

## Examples

```
# Load Crüsemann dataset (MSV000078836) with 120 strains and 8 validated links; compute raw strain correlation and IOKR scores; standardise each as (s - mean(s)) / sqrt(var(s)); report mean, variance, and p-value of enrichment for validated links; repeat for Leão (MSV000085018) and Gross (MSV000085038) datasets; compare cross-dataset reproducibility of standardised score statistics.
```

## Evaluation signals

- Standardised strain correlation score has mean ≈ 0 and variance ≈ 1 across all links in each dataset (e.g., mean −0.006, variance 1.0)
- Standardised scores for validated links are significantly shifted from all-link distribution (e.g., validated link mean 3.67 vs. all-link mean −0.006, p < 10−60)
- Standardisation dramatically improves p-value for validated link enrichment compared to raw scores (e.g., raw p = 0.0001 vs. standardised p = 6.8 × 10−64)
- Cross-dataset consistency: standardised score statistics (mean, variance, p-values for validated links) are reproducible across ≥2 independent datasets from PoDP
- Combined score (standardised strain correlation + standardised IOKR) shows further enrichment for validated links (e.g., combined p < individual p-values) when tested at 90th percentile threshold

## Limitations

- Standardisation assumes scores follow a known distribution (hypergeometric null); violations (e.g., heavy-tailed empirical distribution) may reduce validity of standardised comparisons across links.
- IOKR relies on MIBiG homology to assign molecular structures to BGCs, restricting its use to BGCs showing considerable homology to reference sequences and limiting applicability to novel chemistry.
- Strain correlation scoring cannot distinguish between potential links showing the same pattern of strain presence or absence, even after standardisation, reducing ability to prioritize among equally correlated alternatives.
- Kernel function and parameter selection for IOKR significantly affects score distribution and performance, but these choices are not fully characterized; different kernel/parameter combinations may yield different standardised distributions and cross-dataset comparisons.
- Limited ability to break down standardised score statistics and enrichment by product type due to insufficient test set size in individual datasets; meta-analysis across product classes requires larger consolidated datasets.

## Evidence

- [results] standardisation_yields_zero_mean_unit_variance: "Standardising the score gives a mean score of -0.006 for all links, and 3.672 for validated links"
- [results] standardisation_improves_enrichment_pvalue: "For the raw strain correlation score, the mean score is 83.514 for all links, and 14.667 for validated links (p=0.0001). Standardising the score gives a mean score of -0.006 for all links, and 3.672"
- [results] standardisation_formula: "Standardise the strain correlation score as s*_corr = (σ_corr − E[σ_corr]) / √Var[σ_corr] to yield zero mean and unit variance"
- [results] iokr_standardisation_same_approach: "For IOKR scores, compute the standardised IOKR score s*_IOKR = (σ_IOKR − E[σ_IOKR]) / √Var[σ_IOKR] using the same standardisation formula applied over the set of all potential links"
- [results] combined_score_enrichment: "Combined IOKR and standardised correlation scores show enrichment for validated links (p-value of 2.633 × 10−4 from IOKR and 0.0208 from standardised strain correlation)"
- [abstract] multiple_datasets_validation: "From this platform we concentrated on three data sets each with numerous validated links: MSV000078836, MSV000085018 and MSV000085038"
- [abstract] complementary_scores_hypothesis: "we introduce a method for combining their scores into a single scoring function for genomic and metabolomic links, which shows improved performance over either of the individual approaches"
- [abstract] standardisation_rationale: "the most popular strain correlation score has properties that make it impossible to reliably compare score values across links (even links from the same GCF or MF), severely limiting the scores"
