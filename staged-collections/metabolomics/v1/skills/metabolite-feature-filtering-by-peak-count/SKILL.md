---
name: metabolite-feature-filtering-by-peak-count
description: Use when metabolomics applies a minimum-peaks-in-a-row threshold in MZmine to filter low-frequency metabolite features from untargeted LC-MS/MS data based on contiguous peak detection across multiple samples.
when_to_use_negative:
- Input data is already gap-filled—apply filtering before gap-filling, not after, to avoid artificially inflating peak counts.
- Study has only one or two samples per group—minimum-peaks-in-a-row filtering will be too stringent and may remove valid but rare metabolites.
- You are working with targeted metabolomics or known-compound datasets where every detected feature has been independently validated; this filter is designed for untargeted discovery to reduce false positives.
edam_operation: http://edamontology.org/operation_3695
edam_topics:
- http://edamontology.org/topic_0092
- http://edamontology.org/topic_3172
tools:
- name: MZmine
  role: Applies the minimum-peaks-in-a-row filter during feature detection on raw LC-MS/MS data
- name: R
  role: Post-processes MZmine output to apply population-level presence filtering (removal of features not found in ≥6 samples per population)
  repo: https://github.com/jhaffner09/core_metabolome_2021
provenance:
  source_task_ids:
  - task_002
  source_papers:
  - doi: 10.1128/msystems.00710-22
    title: Untargeted Fecal Metabolomic Analyses across an Industrialization Gradient Reveal Shared Metabolites and Impact of Industrialization on Fecal Microbiome-Metabolome Interactions
schema_version: 0.2.0
metadata:
  merge_audit:
    n_source_runs: 2
    source_files:
    - outputs/audit_haffner_v2/skills/metabolite-feature-filtering-by-peak-count/SKILL.md
    - outputs/audit_haffner_v2/skills/metabolite-feature-filtering-by-peak-count/skill.md
    merged_at: '2026-05-25T07:33:56.329155+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/metabolite-feature-filtering-by-peak-count@sha256:c69d25f18e0feb64445fa888e4f43c9d588cf1526fa2901cbd99880cc37af80d
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1128/msystems.00710-22
---

# metabolite-feature-filtering-by-peak-count

## Summary

Apply a minimum-peaks-in-a-row threshold in MZmine to remove low-frequency metabolite features from untargeted LC-MS/MS data, reducing noise and retaining only features with contiguous peak detection across multiple samples. This filtering is typically applied to non-gap-filled data before population-level presence filtering to identify a robust shared metabolome.

## When to use

When you have processed untargeted LC-MS/MS data (e.g., from MZmine feature detection) and need to reduce the feature space by eliminating sporadic or singleton peaks that are unlikely to represent true biological metabolites. Apply this filter when your study has multiple sample groups (populations) and you want to ensure features are detected consistently within at least one group—e.g., if a population has 12 samples, use a 6-minimum-peaks-in-a-row threshold (half the population size) to capture robust, recurring signals.

## When NOT to use

- Input data is already gap-filled—apply filtering before gap-filling, not after, to avoid artificially inflating peak counts.
- Study has only one or two samples per group—minimum-peaks-in-a-row filtering will be too stringent and may remove valid but rare metabolites.
- You are working with targeted metabolomics or known-compound datasets where every detected feature has been independently validated; this filter is designed for untargeted discovery to reduce false positives.

## Inputs

- MZmine-processed LC-MS/MS feature table (non-gap-filled, in feature_list or CSV format)
- Sample metadata indicating population/group assignment for each sample
- Integer threshold value: sample count per population (e.g., 12 samples → 6-minimum-peaks-in-a-row)

## Outputs

- Filtered metabolite feature table (reduced dimensionality, e.g., 7,483 features from ~20,000+)
- Feature count per filtering stage (optional: for QC reporting)
- Population-level feature presence matrix (presence/absence per population)

## How to apply

In MZmine, apply a minimum-peaks-in-a-row filter set to half the sample count of your smallest population cohort (e.g., 6 peaks in a row if a population has 12 samples). This threshold is applied during MZmine's feature detection workflow to non-gap-filled data, removing any detected feature that does not have at least that many contiguous peak detections. After filtering in MZmine, export the resulting feature table and apply a second-stage population-level presence filter in R (or similar): retain only features found in at least six samples from each of your study populations. This two-stage approach (within-run contiguity + population presence) balances sensitivity and specificity, removing transient noise while preserving population-level shared metabolites. The rationale is that a feature with 6+ consecutive peak detections is more likely a true metabolite than a singleton or doublet, and requiring presence across all populations ensures cross-population reproducibility.

## Related tools

- **MZmine** (Applies the minimum-peaks-in-a-row filter during feature detection on raw LC-MS/MS data)
- **R** (Post-processes MZmine output to apply population-level presence filtering (removal of features not found in ≥6 samples per population)) — https://github.com/jhaffner09/core_metabolome_2021

## Examples

```
# MZmine: apply 6-minimum-peaks-in-a-row filter during feature detection (GUI or batch mode)
# Then in R: filtered_features <- feature_table[rowSums(feature_table[, pop1_samples] > 0) >= 6 & rowSums(feature_table[, pop2_samples] > 0) >= 6 & ... , ]
```

## Evaluation signals

- Output feature count matches expected value (e.g., 7,483 features reported in paper after 6-minimum-peaks-in-a-row + population-level filtering).
- All retained features are present in at least the minimum-peaks-in-a-row count across at least one sample sequence.
- All retained features appear in ≥6 samples from each of the defined populations; features present in only 1–2 populations are absent.
- Feature table schema is preserved (same columns as input; row count reduced by ~60–75% depending on stringency).
- No features with missing values (NA or zero) in the population-presence matrix for any retained feature across all populations.

## Limitations

- Minimum-peaks-in-a-row threshold is population-specific and must be recalculated for studies with unequal group sizes; no single universal threshold applies.
- Filtering is sensitive to sample ordering in the input data; features at file boundaries may be incorrectly discarded if contiguity is enforced across file boundaries rather than within sample groups.
- Rare metabolites with true biological signal but low detection frequency (<50% of samples in any group) will be removed; use with caution in biomarker discovery studies.
- Gap-filling performed after filtering can artificially inflate apparent peak counts; analyses of both gap-filled and non-gap-filled data should be reported separately for transparency.

## Evidence

- [methods] Three separate filtering workflows were done: 6 minimum peaks in a row (half the number of samples in a single population), 45 minimum peaks in a row (half our total samples), and 90 minimum peaks in: "Three separate filtering workflows were done: 6 minimum peaks in a row (half the number of samples in a single population), 45 minimum peaks in a row (half our total samples), and 90 minimum peaks in"
- [results] Further filtering by occurrences in each population highlighted 7,483 metabolite features in non-gap-filled data found in at least six samples in all populations: "Further filtering by occurrences in each population highlighted 7,483 metabolite features in non-gap-filled data found in at least six samples in all populations"
- [methods] For the six-sample filtering, additional processing was done in R (84) to remove any features that were not found in at least six samples from each population.: "For the six-sample filtering, additional processing was done in R (84) to remove any features that were not found in at least six samples from each population."
- [results] to ensure the greatest transparency, we present the analysis of both gap-filled and non-gap-filled data here: "to ensure the greatest transparency, we present the analysis of both gap-filled and non-gap-filled data here"
- [methods] After each filtering step, gap-filling was performed using the previous parameters.: "After each filtering step, gap-filling was performed using the previous parameters."
