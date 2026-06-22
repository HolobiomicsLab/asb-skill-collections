---
name: meta-analysis-effect-size-estimation
description: Use when when you have tabulated results (p-value, fold-change, study size N) from two or more independent metabolomics studies addressing the same research question and need a single meta-analytic estimate of effect size and statistical significance without access to raw data or variance estimates.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3807
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - amanida
  - webchem
derived_from:
- doi: 10.1093/bioinformatics/btab591
  title: Amanida
- doi: 10.3390/metabo13121167
  title: ''
evidence_spans:
- Amanida R package, which contains a collection of functions for computing a weighted meta-analysis in R
- This vignette illustrates `Amanida` R package, which contains a collection of functions for computing a weighted meta-analysis
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# meta-analysis-effect-size-estimation

## Summary

Combines p-values and fold-changes across multiple metabolomics studies using study-size-weighted statistical methods to produce unified effect size estimates and significance values. This skill enables cross-study comparison in metabolomics where raw data and standard deviations are unavailable.

## When to use

When you have tabulated results (p-value, fold-change, study size N) from two or more independent metabolomics studies addressing the same research question and need a single meta-analytic estimate of effect size and statistical significance without access to raw data or variance estimates.

## When NOT to use

- When raw individual-level data or study-level variance/standard error estimates are available—use traditional meta-analysis methods (e.g., inverse-variance weighting) instead.
- When studies report results only as trend direction (up/down) without quantitative p-values or fold-changes—use vote-counting (amanida_vote) as a qualitative alternative.
- When combining results from non-metabolomics fields (e.g., genomics, proteomics) that may report effect sizes in different scales or use different standardization conventions.

## Inputs

- Tabulated metabolomics results table (CSV, XLS, XLSX, or TXT format)
- Columns: compound identifier, p-value, fold-change (or log-fold-change), study sample size (N), bibliographic reference
- Two or more independent studies with overlapping compound measurements

## Outputs

- S4 object with @stat slot: meta-analysis results table (compound identifier, combined p-value, combined fold-change, trend direction, N_total)
- S4 object with @vote slot: vote-counting qualitative results (optional)
- Numerical estimates: meta-analytic p-value, meta-analytic log2(fold-change), total sample size

## How to apply

Load the multi-study dataset (identifier, p-value, fold-change, N per study) using amanida_read with mode='quan'. Apply weighted Fisher's method to combine p-values by assigning gamma-distributed weights proportional to each study's sample size N. Transform fold-changes using log2, then compute the study-size-weighted average of log2-transformed fold-changes. Execute compute_amanida to generate the @stat results table, which contains the combined p-value, combined fold-change (with direction: up-, down-, or no trend), and N_total (sum of all study sizes). Use standard cutoffs (p < 0.05 for significance, fold-change > 2 for biological meaningfulness) to interpret results.

## Related tools

- **amanida** (R package that performs weighted meta-analysis combining p-values via weighted Fisher's method and fold-changes via log2 transformation and study-size weighting) — https://github.com/mariallr/amanida
- **webchem** (R package used (optionally, via check_names) to harmonize compound identifiers to PubChem IDs before meta-analysis)
- **R** (Statistical computing environment in which amanida functions execute)

## Examples

```
library(amanida); coln = c("Compound Name", "P-value", "Fold-change", "N total", "References"); datafile <- amanida_read("studies.csv", mode = "quan", coln, separator=";"); amanida_result <- compute_amanida(datafile, comp.inf = FALSE); volcano_plot(amanida_result, cutoff = c(0.05, 2))
```

## Evaluation signals

- Verify that N_total equals the sum of all input study sample sizes.
- Confirm that combined fold-change direction (up/down/none) is consistent with the sign of the weighted average log2(fold-change).
- Check that combined p-value is ≤ the most significant (smallest) individual study p-value and ≥ the least significant (largest) individual study p-value.
- Ensure no missing or NA values in combined p-value and fold-change columns of @stat table; missing input data should have been skipped during amanida_read import.
- Volcano plot should display combined results without duplicate compound entries; coordinates should match combined p-value and log2(fold-change) from @stat table.

## Limitations

- Requires study sample size (N) for each compound in each study; missing N values are ignored, reducing effective weighting.
- Does not account for between-study heterogeneity (I² statistic not computed); high heterogeneity may inflate confidence in combined estimates.
- Negative fold-change values are automatically transformed to positive (1/value); users should verify this is appropriate for their data encoding.
- Method assumes fold-changes are reported on comparable scales across studies; unnormalized or batch-corrected values may introduce bias.
- Weighted Fisher's method is sensitive to the number of combined p-values; combination of many non-significant p-values can yield spurious significance if weights are large.

## Evidence

- [intro] Quantitative meta-analysis method: "P-value: weighted p-values combination, which is a variant of Fisher's method. A gamma distribution is used to assign non-integral weights proportional to study size to each p-value."
- [intro] Fold-change combination method: "Fold-change: [combined using] logarithmic transformation for average with weighting by number of participants."
- [intro] Output structure and contents: "In this step you will obtain an S4 object with two tables: adapted meta-analysis acces by `amanida_result@stat` [and] vote-counting acces by `amanida_results@vote`"
- [readme] Design rationale: non-integral weighting: "amanida performs weighted meta-analysis combining overall results based on statistical significance, relative change and study size without requiring standard deviation"
- [readme] Input requirements: "Dataset to analyse must include the following columns: identifier, p-value, fold-change, study size (N) and reference"
- [intro] Biological meaningfulness cutoff: "in case of fold-change we recommend values higher than 2, where it is considered to have biological meaningfulness"
- [readme] Vote-counting as qualitative complement: "Amanida also computes qualitative meta-analysis performing a vote-counting for compounds, including the option of only using identifier and trend labels"
