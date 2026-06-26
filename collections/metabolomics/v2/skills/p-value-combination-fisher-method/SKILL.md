---
name: p-value-combination-fisher-method
description: Use when when you have tabulated p-values and study sample sizes (N)
  from multiple independent metabolomics studies measuring the same compounds or metabolites,
  and you need to compute a single meta-analytic p-value that reflects both statistical
  significance and study weight.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - R
  - amanida
  - webchem
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1093/bioinformatics/btab591
  title: Amanida
- doi: 10.3390/metabo13121167
  title: ''
evidence_spans:
- Amanida R package, which contains a collection of functions for computing a weighted
  meta-analysis in R
- This vignette illustrates `Amanida` R package, which contains a collection of functions
  for computing a weighted meta-analysis
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_amanida_cq
    doi: 10.1093/bioinformatics/btab591
    title: Amanida
  dedup_kept_from: coll_amanida_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btab591
  all_source_dois:
  - 10.1093/bioinformatics/btab591
  - 10.3390/metabo13121167
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# p-value-combination-fisher-method

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Combines statistical significance (p-values) from multiple metabolomics studies into a single meta-analytic p-value using a weighted variant of Fisher's method, where weights are gamma-distributed and proportional to study sample size. This enables aggregation of significance across studies without requiring raw data or standard deviations.

## When to use

When you have tabulated p-values and study sample sizes (N) from multiple independent metabolomics studies measuring the same compounds or metabolites, and you need to compute a single meta-analytic p-value that reflects both statistical significance and study weight. This is particularly useful when raw data or variance/standard deviation estimates are unavailable—a common situation in metabolomic meta-analysis.

## When NOT to use

- Input dataset already contains aggregated or pre-computed meta-analytic results (e.g., already a single combined p-value per compound across all studies).
- Study sizes (N) are unknown or unavailable; the weighting scheme requires explicit sample size for each study to be meaningful.
- Raw individual-level data or variance/standard deviation estimates are available; traditional parametric meta-analysis methods (e.g., inverse-variance weighting) may be more statistically efficient.
- Only qualitative trend data (up/down labels) and no p-values are present; use vote-counting (`amanida_vote`) instead.

## Inputs

- amanida data structure (S4 object) containing: compound identifier column, p-value column (numeric, 0–1 range), fold-change column (numeric), study size N column (positive integer), and reference column (study bibliographic identifier)

## Outputs

- amanida result object (S4 class) with @stat slot: data frame containing meta-analytic p-value per compound, trend direction (up-regulation, down-regulation, or no trend), combined log2(fold-change), and N_total (sum of sample sizes across contributing studies)

## How to apply

Load the input dataset (containing compound identifier, p-value, fold-change, and study size N columns) into an amanida data structure using `amanida_read()`. For each p-value in the dataset, assign a gamma-distributed weight proportional to the study's sample size (N); the weighted Fisher's method then combines these weighted p-values into a single meta-analytic result. Call `compute_amanida(datafile, comp.inf = FALSE)` to execute the combination and retrieve results via the @stat table slot, which reports trend direction and N_total (sum of all contributing study sizes). The rationale: larger studies receive higher weights via the gamma distribution, preventing small underpowered studies from dominating the meta-analytic signal, and Fisher's method tolerates the lack of standard deviation—a key limitation in metabolomic reporting.

## Related tools

- **amanida** (R package implementing weighted Fisher's method for p-value combination and hosting the compute_amanida function that executes the meta-analysis) — https://github.com/mariallr/amanida
- **R** (Statistical programming environment required to run amanida package functions)
- **webchem** (Optional R package used for compound ID harmonization (check_names function) prior to meta-analysis to ensure duplicate detection)

## Examples

```
amanida_result <- compute_amanida(datafile, comp.inf = FALSE); meta_pvalues <- amanida_result@stat
```

## Evaluation signals

- Output @stat table contains exactly one row per unique compound identifier present in the input dataset, with no duplicates or missing compounds.
- Meta-analytic p-values in @stat are numeric, bounded in [0, 1], and generally smaller (more significant) than the median or mean of the input p-values (reflecting increased power from aggregation).
- N_total for each compound equals the sum of all N values from the input studies contributing to that compound; spot-check by manually summing a subset of input rows.
- Trend direction is assigned consistently: positive combined log2(fold-change) corresponds to 'up-regulation', negative to 'down-regulation', absence of trend when log2(fold-change) is near zero.
- Compounds with larger or more concordant study sizes should have lower meta-analytic p-values (smaller gamma weights for outlier studies and more stable aggregation).

## Limitations

- Method requires p-values and study sizes to be reported for all compounds across all studies; missing data is ignored during import, which can reduce effective sample size and power for sparse compounds.
- Assumes independence between studies (no shared participant overlap); if studies use overlapping cohorts, p-values and weights may be biased upward.
- Fisher's method is sensitive to p-value distribution assumptions; if many p-values cluster near 0 or 1, the gamma-weighted combination may not capture effect heterogeneity as well as heterogeneity-aware methods (e.g., inverse-variance with tau²).
- No standard deviation or variance input means effect size estimates cannot be adjusted for precision; all weighting is based solely on sample size, not statistical uncertainty of fold-change estimates.
- Results reflect vote-counting consistency and weighted significance but do not estimate prediction intervals or between-study heterogeneity (I², tau²).

## Evidence

- [readme] P-value combination: Fisher's method weighted by number of participants on the study.: "P-value combination: Fisher's method weighted by number of participants on the study."
- [intro] A gamma distribution is used to assign non-integral weights proportional to study size to each p-value.: "A gamma distribution is used to assign non-integral weights proportional to study size to each p-value."
- [intro] When raw data is not available to perform a meta-analysis, there are different approaches that require the standard deviation for effect size estimate calculation and weighted methods: "When raw data is not available to perform a meta-analysis, there are different approaches that require the standard deviation for effect size estimate calculation and weighted methods"
- [intro] amanida performs weighted meta-analysis combining overall results based on statistical significance, relative change and study size without requiring standard deviation: "amanida performs weighted meta-analysis combining overall results based on statistical significance, relative change and study size without requiring standard deviation"
- [other] Execute compute_amanida function in R to generate the @stat results table, including trend direction (up-regulation, down-regulation, or no trend) and N_total (sum of study sizes across all contributing studies).: "Execute compute_amanida function in R to generate the @stat results table, including trend direction (up-regulation, down-regulation, or no trend) and N_total (sum of study sizes across all"
