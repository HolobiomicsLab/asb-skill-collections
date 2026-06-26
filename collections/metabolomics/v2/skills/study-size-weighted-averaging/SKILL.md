---
name: study-size-weighted-averaging
description: Use when you have metabolomics results from multiple independent studies
  (each with a fold-change, p-value, and sample size N) and need to produce a single
  quantitative meta-analysis fold-change estimate.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  tools:
  - R
  - amanida
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

# study-size-weighted-averaging

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Combine effect sizes (fold-changes) across multiple metabolomics studies by applying log2 transformation and computing a weighted average where weights are proportional to each study's sample size (N). This produces a single pooled fold-change estimate that reflects both the magnitude of change and the statistical power of each contributing study.

## When to use

You have metabolomics results from multiple independent studies (each with a fold-change, p-value, and sample size N) and need to produce a single quantitative meta-analysis fold-change estimate. Use this skill when raw data and standard deviations are unavailable but relative change (fold-change) and study sample sizes are known, as is typical in published metabolomics comparisons.

## When NOT to use

- Standard deviations or confidence intervals are available for each study—use conventional meta-analysis effect-size methods instead.
- Data are already individual-level (raw metabolite abundances), not summarized study-level results.
- You are performing qualitative vote-counting analysis; use that skill independently for trend consensus without fold-change pooling.

## Inputs

- amanida data structure (S4 object) containing: identifier (metabolite name), fold-change (numeric, typically > 0), study size N (integer sample count), and p-value columns from multiple studies

## Outputs

- compute_amanida @stat table containing pooled fold-change estimate, trend direction (up-regulation / down-regulation / no trend), and N_total (sum of study sizes)

## How to apply

First, log2-transform each study's fold-change value to symmetrize the scale (so a 2-fold increase and 2-fold decrease are equidistant from zero). Then compute a weighted average where each transformed fold-change is multiplied by its study size N and divided by the sum of all N values. The rationale is that larger studies provide more precise estimates and should contribute proportionally more to the pooled result. This weighting ensures the meta-analysis fold-change reflects the combined evidence, not an unweighted arithmetic mean. The result is stored in the @stat table of the compute_amanida output object and reports both the pooled fold-change and the direction of regulation (up/down/no trend).

## Related tools

- **amanida** (Executes study-size-weighted fold-change averaging via compute_amanida() function; stores results in @stat table) — https://github.com/mariallr/amanida
- **R** (Host language for amanida package and log2 transformation operations)

## Examples

```
amanida_result <- compute_amanida(datafile, comp.inf = F); pooled_fc <- amanida_result@stat
```

## Evaluation signals

- Verify @stat table contains non-zero pooled fold-change values with direction labels (up/down/no trend) and N_total equals sum of input study sizes.
- Check that log2-transformed fold-changes are symmetric around zero (e.g., 2-fold up and 0.5-fold down both have absolute magnitude ~1 on log2 scale).
- Confirm volcano plot shows pooled log2(fold-change) on x-axis aligned with combined p-value significance on y-axis.
- Validate that studies with larger N values have greater influence on the pooled fold-change estimate by sensitivity analysis (removing large-N studies shifts result meaningfully).
- Ensure N_total in output matches manual sum of input study sizes across all rows.

## Limitations

- Negative fold-change values are transformed to positive (1/value) before processing; true directional information may be lost if input data mix up/down regulation inconsistently.
- Fold-changes < 2 are not recommended for biological interpretation; pooled estimates below this threshold should be treated as non-significant even if statistically combined.
- Assumes fold-changes are already normalized and comparable across studies; batch effects or different quantification platforms may bias the pooled estimate.
- No uncertainty (confidence interval) is reported for the pooled fold-change; only point estimate and direction are provided.

## Evidence

- [intro] log2_transformation_and_weighting: "Fold-change: logarithmic transformation for average with weighting by number of participants"
- [readme] compute_amanida_output_structure: "In this step you will obtain an S4 object with two tables: adapted meta-analysis acces by `amanida_result@stat` and vote-counting acces by `amanida_results@vote`"
- [other] stat_table_contents: "producing meta-analysis results accessible via the @stat table containing trend direction and N_total (sum of study sizes)"
- [intro] study_size_proportional_weighting: "P-value: weighted p-values combination, which is a variant of Fisher's method. A gamma distribution is used to assign non-integral weights proportional to study size to each p-value. Fold-change:"
- [readme] input_data_requirements: "Dataset to analyse must include the following columns: identifier, p-value, fold-change, study size (N) and reference"
