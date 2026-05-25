---
name: population-level-feature-presence-filtering
description: Use when filtering a metabolite feature table in metabolomics using LC-MS or GC-MS techniques to retain only features present in a minimum number of samples within each population stratum.
when_to_use_negative:
- Input data are already gap-filled or imputed; population-level filtering is most effective on raw, unimputed feature matrices to avoid inflating apparent prevalence.
- Populations are severely imbalanced (e.g., one population has <6 samples); the threshold becomes meaningless or overly stringent.
- Analysis goal is to detect rare, population-specific metabolites; this filter deliberately removes such features in favor of shared signatures.
edam_operation: http://edamontology.org/operation_3695
edam_topics:
- http://edamontology.org/topic_0769
- http://edamontology.org/topic_3370
tools:
- name: MZmine
  role: Performs initial feature detection, alignment, and minimum-peaks-in-a-row filtering prior to population-level filtering
- name: R
  role: Implements population-level presence filtering by subsetting the feature table to retain features meeting the per-population sample count threshold
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
    - outputs/audit_haffner_v2/skills/population-level-feature-presence-filtering/SKILL.md
    - outputs/audit_haffner_v2/skills/population-level-feature-presence-filtering/skill.md
    merged_at: '2026-05-25T07:04:57.474865+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/population-level-feature-presence-filtering@sha256:e786956b3d2bd614db207ddbc8797355d28278d6199ffdebb280a0f47a5c1a6d
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1128/msystems.00710-22
---

# population-level-feature-presence-filtering

## Summary

Filter a metabolite feature table to retain only features present in a minimum number of samples within each population stratum, ensuring population-level prevalence of metabolic markers. This skill ensures that downstream comparative analyses focus on shared, robust metabolic signatures that are consistently detectable across the sampled populations.

## When to use

Apply this skill after initial MZmine feature detection and minimum-peaks-in-a-row filtering, when you have a multi-population cohort and want to identify a core set of metabolite features that are prevalent across all populations. Trigger this when: (1) your input is a non-gap-filled or gap-filled MZmine feature intensity table with sample × feature dimensions, (2) samples are stratified into discrete populations (e.g., by geography, industrialization, or treatment group), and (3) you want to reduce spurious or population-specific features to focus on shared metabolic signatures suitable for cross-population comparisons (e.g., PCoA, PERMANOVA).

## When NOT to use

- Input data are already gap-filled or imputed; population-level filtering is most effective on raw, unimputed feature matrices to avoid inflating apparent prevalence.
- Populations are severely imbalanced (e.g., one population has <6 samples); the threshold becomes meaningless or overly stringent.
- Analysis goal is to detect rare, population-specific metabolites; this filter deliberately removes such features in favor of shared signatures.

## Inputs

- MZmine-processed non-gap-filled feature intensity table (m/z × RT × sample)
- Population membership vector or grouping metadata (sample → population)
- Minimum sample count threshold per population (integer, typically 6 or ≥50% of population size)

## Outputs

- Filtered feature intensity table (subset of input, same dimensions but fewer columns)
- Feature count summary (e.g., '7,483 features found in ≥6 samples per population')
- Optional: feature presence matrix (samples × features, binary or count-based)

## How to apply

Load the MZmine-processed feature intensity table (rows = samples, columns = m/z-RT features). Apply a minimum-peaks-in-a-row threshold in MZmine (e.g., 6 peaks, equivalent to half the sample count of the smallest population) to remove features with sparse temporal or technical coherence. Then, in R or equivalent scripting language, iterate over each population stratum and count the number of samples in that population where each feature has a non-zero (detected) intensity. Retain only features present (intensity > 0) in at least N samples per population, where N is set a priori (commonly ≥6 samples or ≥50% of population size). This two-stage approach—technical coherence followed by population-level prevalence—yields a high-confidence feature set enriched for biologically meaningful, reproducible metabolite signatures. Verify output cardinality matches expected feature count (e.g., 7,483 features) and that all populations contribute qualifying features.

## Related tools

- **MZmine** (Performs initial feature detection, alignment, and minimum-peaks-in-a-row filtering prior to population-level filtering)
- **R** (Implements population-level presence filtering by subsetting the feature table to retain features meeting the per-population sample count threshold) — https://github.com/jhaffner09/core_metabolome_2021

## Examples

```
# R code: load feature table, apply population-level filtering
features <- read.csv('mzmine_features.csv', row.names=1)
population_map <- read.csv('sample_population.csv')
filtered <- features[, apply(features, 2, function(col) all(tapply(col > 0, population_map$pop, sum) >= 6))]
write.csv(filtered, 'filtered_7483_features.csv')
```

## Evaluation signals

- Output feature count matches the reported target (e.g., exactly 7,483 features if using 6-sample threshold on six populations).
- All retained features have non-zero intensity in at least the specified minimum number of samples in every population (schema check: no feature should have <N detections in any stratum).
- Feature presence is balanced across populations; no population is under-represented in the final set (inspect feature count distribution across groups).
- Downstream comparative analyses (e.g., PCoA, PERMANOVA) on the filtered table show coherent population clustering consistent with study hypothesis (e.g., industrialization gradient).
- Gap-filled and non-gap-filled variants produce similar but distinct counts, validating separation of analytical paths (expected: gap-filled slightly larger due to imputation).

## Limitations

- Threshold choice (e.g., 6 samples vs. 50% of population size) is somewhat arbitrary and may bias results toward or away from rare metabolites; sensitivity analysis recommended.
- Population-level filtering may discard real but low-prevalence metabolites that are biologically relevant (e.g., those enriched in subgroups within a population).
- If populations have unequal sample sizes, a fixed threshold (e.g., 6 samples) may be too stringent for small populations or too permissive for large ones; relative thresholds (e.g., 50% per population) are more robust.
- Filtering is sensitive to the definition of 'population' (geographic, clinical, or experimental); misclassification of sample strata invalidates the output.

## Evidence

- [results] Further filtering by occurrences in each population highlighted 7,483 metabolite features in non-gap-filled data found in at least six samples in all populations: "Further filtering by occurrences in each population highlighted 7,483 metabolite features in non-gap-filled data found in at least six samples in all populations"
- [methods] For the six-sample filtering, additional processing was done in R to remove any features that were not found in at least six samples from each population: "For the six-sample filtering, additional processing was done in R (84) to remove any features that were not found in at least six samples from each population."
- [methods] Six minimum peaks in a row (half the number of samples in a single population): "6 minimum peaks in a row (half the number of samples in a single population)"
- [results] to ensure the greatest transparency, we present the analysis of both gap-filled and non-gap-filled data here: "to ensure the greatest transparency, we present the analysis of both gap-filled and non-gap-filled data here"
