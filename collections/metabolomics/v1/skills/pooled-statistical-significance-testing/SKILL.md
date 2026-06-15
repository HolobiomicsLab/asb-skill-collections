---
name: pooled-statistical-significance-testing
description: Use when when you have validated link annotations from multiple independent datasets (≥2), individual scoring functions with per-dataset enrichment p-values, and you want to test whether a combined scoring strategy (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3372
  tools:
  - antiSMASH
  - BiG-SCAPE
  - NPLinker
  - GNPS
  - MIBiG
  - Python (numpy, scipy.stats, pandas, matplotlib, seaborn)
  - Python scipy.stats
derived_from:
- doi: 10.1371/journal.pcbi.1008920
  title: NPLinker
evidence_spans:
- after downloading the strain assemblies and metabolomics data, the genomes were run through antiSMASH v5.0.0 for BGC detection
- genomes were run through antiSMASH v5.0.0 for BGC detection
- and BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs
- BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs
- NPLinker, a software framework to link genomic and metabolomic data
- NPLinker creates objects for spectra, MFs, BGCs and GCFs in the data set
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

# pooled-statistical-significance-testing

## Summary

Combine validated link counts across multiple independent datasets and apply Fisher exact test or chi-square test to assess whether a combined ranking criterion (e.g. joint percentile threshold) yields statistically significant enrichment for true links compared to single-function baselines. This allows detection of complementarity effects that may be obscured in individual datasets.

## When to use

When you have validated link annotations from multiple independent datasets (≥2), individual scoring functions with per-dataset enrichment p-values, and you want to test whether a combined scoring strategy (e.g. ℓp-norm fusion, joint percentile filtering) shows significantly better enrichment than either function alone. Pooling is particularly valuable when single datasets lack statistical power or when the effect size is modest within each dataset but consistent across them.

## When NOT to use

- Input is from a single dataset only; use per-dataset significance tests instead (Fisher exact, Mann-Whitney U, or t-test depending on data structure).
- Datasets are not independent (e.g. overlapping sample composition, shared bias in validation labels); pooling may violate independence assumption and inflate type I error.
- You have no validated link annotations; enrichment testing requires ground truth labels to distinguish true from spurious predictions.

## Inputs

- per-dataset counts of validated links and total links in each scoring tier (all links, top percentile for function A, top percentile for function B, top percentile for both)
- list of dataset identifiers and their sizes
- individual p-values or effect sizes from each dataset (for comparison)

## Outputs

- pooled 2×2 or larger contingency table (rows: validated vs. non-validated; columns: scoring categories)
- Fisher exact test p-value or chi-square test statistic and p-value
- enrichment ratio (proportion validated in combined group vs. single-function group)
- conclusion of statistical significance (p < 0.05) and direction of enrichment

## How to apply

First, count the total number of validated links and non-validated links in each dataset that fall into each tested category (e.g. all links, top 90th percentile for function A alone, top 90th percentile for function B alone, top 90th percentile for both functions jointly). Pool these counts across all datasets by summing validated and non-validated link counts for each category. Then apply Fisher exact test (for 2×2 contingency tables) or chi-square test (for larger contingency tables) to compare the enrichment ratio (proportion of validated links) in the combined scoring group versus either single-function group. Record the resulting p-value and reject the null hypothesis of no difference if p < 0.05. Validation: confirm that pooled results reproduce the reported enrichments from the paper (e.g. p=2.633×10−4 for IOKR and p=0.0208 for standardised correlation when filtering at joint 90th percentile across three datasets).

## Related tools

- **Python scipy.stats** (Computes Fisher exact test and chi-square test statistics and p-values for contingency tables)
- **NPLinker** (Framework providing GCF-MF link scores (strain correlation, IOKR, combined) and integration with Paired Omics Data Platform for validated link retrieval) — https://github.com/sdrogers/nplinker

## Examples

```
from scipy.stats import fisher_exact; import pandas as pd; validated_joint = [50, 45, 40]; total_joint = [500, 480, 450]; validated_single_a = [35, 30, 25]; total_single_a = [600, 580, 560]; oddsratio, p_value = fisher_exact([[sum(validated_joint), sum(total_joint)-sum(validated_joint)], [sum(validated_single_a), sum(total_single_a)-sum(validated_single_a)]]); print(f'Pooled p-value: {p_value:.2e}')
```

## Evaluation signals

- Pooled p-value is ≤ single-dataset p-values (if effect is consistent) or lies between them (if datasets show heterogeneous effects); check monotonicity with respect to percentile threshold.
- Contingency table row sums (total validated, total non-validated) match the cumulative counts reported in paper tables (e.g. Table 2).
- Enrichment ratio for combined criterion exceeds enrichment ratio for either single function (e.g. combined group has higher proportion of validated links than either alone).
- P-value reproducibility: pooled p-value for the reported combination function (ℓ₁/₂-norm at 90th percentile) matches published values (p=2.633×10−4 for IOKR, p=0.0208 for standardised correlation).
- Sample sizes in each cell of the contingency table are reported; Fisher exact is appropriate for expected cell counts < 5, otherwise chi-square is preferred.

## Limitations

- Assumes independence of datasets; if samples or validation labels are shared or correlated across datasets, pooling inflates degrees of freedom and underestimates p-values.
- Power depends on total pool size; if individual datasets are small or validated link counts are sparse, pooled test may still lack power unless effect size is large.
- Does not account for heterogeneity in enrichment effect across datasets; if one dataset drives the signal while others show null or opposite effect, chi-square may mask this. Consider subgroup or sensitivity analyses.
- Requires curated validated link annotations; quality and completeness of ground truth (e.g. Paired Omics Data Platform BLAST matching threshold ≥10,000 cumulative score) directly impact enrichment estimates.
- Pooling assumes the combining function parameters (e.g. ℓp exponent, weights) are fixed before testing; testing multiple exponents across the same pooled data inflates type I error unless correction (e.g. Bonferroni) is applied.

## Evidence

- [other] Pool validated link counts across datasets and compute Fisher exact test p-values comparing enrichment of the joint top percentile group versus either single-function top percentile group.: "Pool validated link counts across datasets and compute Fisher exact test p-values comparing enrichment of the joint top percentile group versus either single-function top percentile group."
- [other] Links scoring above the 90th percentile for both standardised strain correlation and IOKR scores show significantly higher enrichment for validated links (p=2.633×10−4 from IOKR and p=0.0208 from standardised correlation) compared to either individual score alone.: "Links scoring above the 90th percentile for both standardised strain correlation and IOKR scores show significantly higher enrichment for validated links (p=2.633×10−4 from IOKR and p=0.0208 from"
- [other] Pool results across the three datasets and perform significance testing (chi-square or Fisher exact test) to identify which combination functions yield statistically significant enrichment (p < 0.05) relative to using either score alone.: "Pool results across the three datasets and perform significance testing (chi-square or Fisher exact test) to identify which combination functions yield statistically significant enrichment (p < 0.05)"
- [results] Table 2 shows the proportion of validated links among all possible GCF-MF links in the three data sets, both for all the potential links, and for the links scoring above the 90th percentile for raw: "Table 2 shows the proportion of validated links among all possible GCF-MF links in the three data sets, both for all the potential links, and for the links scoring above the 90th percentile"
- [discussion] By pairing the MIBiG and GNPS databases, and using the Paired omics Data Platform, we introduced data sets to test the efficiency of the scoring methods: "By pairing the MIBiG and GNPS databases, and using the Paired omics Data Platform, we introduced data sets to test the efficiency of the scoring methods"
