---
name: non-gap-filled-data-processing
description: Use when processing untargeted metabolomics LC-MS/MS and GC-MS data without gap-filling to maintain the integrity of detection patterns across samples, ensuring accurate analysis of shared metabolites in populations.
when_to_use_negative:
- Input is already gap-filled or imputed; re-filtering will propagate artifacts.
- Downstream analysis requires complete feature matrices with no missing values (e.g., certain multivariate methods that cannot tolerate NAs).
- Study design focuses on within-sample feature intensity relationships rather than cross-sample presence/absence patterns.
edam_operation: http://edamontology.org/operation_3695
edam_topics:
- http://edamontology.org/topic_3172
- http://edamontology.org/topic_0121
tools:
- name: MZmine
  role: Peak detection and feature table generation; applies minimum-peaks-in-a-row filtering in the absence of gap-filling
- name: R
  role: Population-level presence filtering; removes features not meeting per-population minimum sample thresholds
  repo: https://github.com/jhaffner09/core_metabolome_2021
- name: MSConvert
  role: Raw data conversion to mzXML format prior to MZmine processing
provenance:
  source_task_ids:
  - task_002
  source_papers:
  - doi: 10.1128/msystems.00710-22
    title: Untargeted Fecal Metabolomic Analyses across an Industrialization Gradient Reveal Shared Metabolites and Impact of Industrialization on Fecal Microbiome-Metabolome Interactions
schema_version: 0.2.0
derived_from:
- doi: 10.1128/msystems.00710-22
metadata:
  iri: https://w3id.org/holobiomicslab/asb-skill/non-gap-filled-data-processing@sha256:366dbaafa1379e4b51872fe3d03ca0455ab420477dfe86b85e4f90d05fd8821b
---

# non-gap-filled-data-processing

## Summary

Process untargeted LC-MS/MS metabolomic data without gap-filling to preserve the integrity of detection patterns across samples. This approach is critical when analyzing shared metabolites across populations where missing-value imputation could mask genuine absence or alter inter-sample comparison validity.

## When to use

When you have MZmine-processed feature tables from untargeted metabolomic studies and need to identify population-level shared metabolites while preserving the original detection patterns. Apply this skill when gap-filling is not appropriate for your downstream inference (e.g., presence/absence filtering, inter-population comparison of metabolite prevalence) or when you require explicit comparison of gap-filled vs. non-gap-filled results for methodological transparency.

## When NOT to use

- Input is already gap-filled or imputed; re-filtering will propagate artifacts.
- Downstream analysis requires complete feature matrices with no missing values (e.g., certain multivariate methods that cannot tolerate NAs).
- Study design focuses on within-sample feature intensity relationships rather than cross-sample presence/absence patterns.

## Inputs

- MZmine feature table (non-gap-filled, e.g., mzML or CSV format)
- Sample metadata (population assignments, sample counts per population)
- Filtering parameters (minimum-peaks-in-a-row threshold, per-population sample minimum)

## Outputs

- Filtered non-gap-filled feature table (e.g., 7,483 features)
- Feature presence matrix indexed by population
- Reproducibility report (feature count by filtering stage)

## How to apply

Load the non-gap-filled MZmine feature table (e.g., from MassIVE MSV000084794) and apply sequential filtering without gap-filling: (1) Apply MZmine's minimum-peaks-in-a-row filter (typically 6, representing half the sample count in a single population); (2) In R, remove features not found in at least 6 samples per population to enforce population-level presence; (3) Verify the final feature count matches expectations (e.g., 7,483 features for the reported workflow). The rationale is that non-gap-filled filtering explicitly captures which metabolites are genuinely detected across populations, avoiding the statistical artifacts introduced by imputation of missing values.

## Related tools

- **MZmine** (Peak detection and feature table generation; applies minimum-peaks-in-a-row filtering in the absence of gap-filling)
- **R** (Population-level presence filtering; removes features not meeting per-population minimum sample thresholds) — https://github.com/jhaffner09/core_metabolome_2021
- **MSConvert** (Raw data conversion to mzXML format prior to MZmine processing)

## Examples

```
# R script excerpt: Apply population-level presence filtering to non-gap-filled MZmine output
# Load feature table and filter to retain only features present in ≥6 samples per population
feature_table <- read.csv('mzmine_nongapfilled.csv', row.names=1)
population_assignments <- read.csv('sample_metadata.csv')
filtered_features <- feature_table[, apply(feature_table, 2, function(col) {
  all(tapply(col > 0, population_assignments$population, sum) >= 6)
})]
write.csv(filtered_features, 'filtered_nongapfilled_7483features.csv')
```

## Evaluation signals

- Final feature count matches reported value (e.g., 7,483 features after 6-minimum-peaks filtering + per-population presence check).
- All remaining features are present in at least the specified minimum number of samples in every population (6 samples in the reference workflow).
- Comparison of non-gap-filled and gap-filled results shows expected differences in feature counts; gap-filled typically yields more features due to imputation.
- Feature presence matrix contains no NaN or imputed values; only 0 (absent) or positive intensity values (detected).
- Reproducibility: R script successfully replicates filtering from the original MZmine table without manual intervention.

## Limitations

- Non-gap-filled filtering is more stringent and may discard low-abundance or sporadically detected metabolites that gap-filling would retain; this reduces feature count but increases confidence in cross-population comparisons.
- Minimum-peaks-in-a-row threshold must be calibrated to sample group sizes; fixed thresholds may be inappropriate for imbalanced study designs.
- Per-population presence filtering requires explicit population metadata; misspecified group assignments will produce incorrect feature lists.
- This approach does not impute missing values, so downstream analyses requiring complete matrices (e.g., certain clustering or dimensionality reduction methods) may require post-hoc handling of NAs.

## Evidence

- [methods] Three separate filtering workflows were done: 6 minimum peaks in a row (half the number of samples in a single population), 45 minimum peaks in a row (half our total samples), and 90 minimum peaks in: "Three separate filtering workflows were done: 6 minimum peaks in a row (half the number of samples in a single population)"
- [results] Further filtering by occurrences in each population highlighted 7,483 metabolite features in non-gap-filled data found in at least six samples in all populations: "Further filtering by occurrences in each population highlighted 7,483 metabolite features in non-gap-filled data found in at least six samples in all populations"
- [results] to ensure the greatest transparency, we present the analysis of both gap-filled and non-gap-filled data here: "to ensure the greatest transparency, we present the analysis of both gap-filled and non-gap-filled data here"
- [methods] For the six-sample filtering, additional processing was done in R (84) to remove any features that were not found in at least six samples from each population.: "For the six-sample filtering, additional processing was done in R to remove any features that were not found in at least six samples from each population"
- [methods] Instructions for recreating data analyses in R and Python are available as Jupyter Notebook (85) links at: https://github.com/jhaffner09/core_metabolome_2021.: "Instructions for recreating data analyses in R and Python are available as Jupyter Notebook links at: https://github.com/jhaffner09/core_metabolome_2021"
