---
name: feature-table-reproducibility-validation
description: Use when validating a metabolomics feature table by applying LC-MS or GC-MS techniques to ensure it matches expected cardinality after sequential filtering steps.
when_to_use_negative:
- Input data is already gap-filled; apply reproducibility validation separately to non-gap-filled data to isolate the effect of gap-filling.
- Population structure differs from the six-population design; thresholds (6 peaks, 6 samples per population) must be recalibrated.
- Feature table has already been subset by other criteria (e.g., variable importance cutoff > 1.3, compound-level annotation); validate at the raw-filtering stage, not post-hoc.
edam_operation: http://edamontology.org/operation_3695
edam_topics:
- http://edamontology.org/topic_0091
- http://edamontology.org/topic_3172
tools:
- name: MZmine
  role: Performs initial peak detection, alignment, and feature table construction; outputs feature table to which minimum-peaks-in-a-row filtering is applied
- name: R
  role: Implements population-level feature presence filtering to remove features not found in at least N samples (e.g., 6) from each population; counts final feature cardinality
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
    - outputs/audit_haffner_v2/skills/feature-table-reproducibility-validation/SKILL.md
    - outputs/audit_haffner_v2/skills/feature-table-reproducibility-validation/skill.md
    merged_at: '2026-05-25T07:04:57.486619+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/feature-table-reproducibility-validation@sha256:6f0ebbd5da4ccb310a43b07617bcf351be7246437b966ef413bab3c48c252fea
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1128/msystems.00710-22
---

# feature-table-reproducibility-validation

## Summary

Validates that a metabolomic feature table has been correctly filtered and processed by verifying it matches expected cardinality (e.g., 7,483 features) after applying sequential filtering steps (minimum-peaks-in-a-row thresholds and population-level presence filtering). This skill ensures reproducibility of feature selection decisions across non-gap-filled and gap-filled datasets.

## When to use

Use this skill when you have applied filtering workflows (minimum-peaks-in-a-row thresholds followed by population-level presence filtering) to MZmine-processed metabolomic data and need to verify that the resulting feature table matches the expected feature count (e.g., 7,483 features in non-gap-filled data). Apply it as a checkpoint after filtering to confirm the pipeline produced the reported output cardinality.

## When NOT to use

- Input data is already gap-filled; apply reproducibility validation separately to non-gap-filled data to isolate the effect of gap-filling.
- Population structure differs from the six-population design; thresholds (6 peaks, 6 samples per population) must be recalibrated.
- Feature table has already been subset by other criteria (e.g., variable importance cutoff > 1.3, compound-level annotation); validate at the raw-filtering stage, not post-hoc.

## Inputs

- MZmine-processed non-gap-filled metabolomic feature table (mzXML or equivalent format)
- Sample-to-population assignment mapping (six populations with ~12 samples each)
- Filter thresholds: minimum-peaks-in-a-row (integer, e.g., 6) and minimum samples per population (integer, e.g., 6)

## Outputs

- Filtered feature table containing only features meeting both minimum-peaks-in-a-row and population-level presence thresholds
- Feature count verification report (observed count vs. expected count, e.g., 7,483)

## How to apply

Load the non-gap-filled MZmine feature table and apply a 6-minimum-peaks-in-a-row filter (corresponding to half the number of samples in a single population). Then, using R or equivalent scripting, remove any features not found in at least six samples from each of the six populations. Count the resulting features and compare against the expected value (7,483 for this study). If counts match exactly, the filtering was applied correctly. The rationale is that this two-stage filter—peak continuity followed by cross-population presence—ensures features are robust across the study design and not driven by single-population artifacts.

## Related tools

- **MZmine** (Performs initial peak detection, alignment, and feature table construction; outputs feature table to which minimum-peaks-in-a-row filtering is applied)
- **R** (Implements population-level feature presence filtering to remove features not found in at least N samples (e.g., 6) from each population; counts final feature cardinality) — https://github.com/jhaffner09/core_metabolome_2021

## Examples

```
# Load non-gap-filled MZmine feature table; apply R filter: features_filtered <- features[rowSums(features > 0) >= 6 & apply(features, 1, function(x) all(tapply(x > 0, population_map, sum) >= 6)), ]; nrow(features_filtered) == 7483
```

## Evaluation signals

- Feature count after filtering equals expected value (7,483 for non-gap-filled data in this study).
- Every retained feature is present in at least 6 samples in each of the 6 populations (cross-validate via group-wise feature abundance summaries).
- Every retained feature passes the 6-minimum-peaks-in-a-row threshold (inspect peak-occurrence patterns in the MZmine output or processed data).
- No features are duplicated or lost in the filtering pipeline (row count before and after are additive, with no unexplained gaps).
- Comparison between non-gap-filled and gap-filled versions shows expected cardinality differences (non-gap-filled: 7,483; gap-filled should differ predictably based on gap-filling logic).

## Limitations

- Thresholds (6 minimum-peaks-in-a-row, 6 samples per population) are specific to this study design (12 samples per population); they must be adjusted proportionally if sample counts or population structure changes.
- This validation only confirms reproducibility of the filtering step, not the biological validity of the features; downstream validation (annotation, statistical significance) is required.
- Gap-filling introduces uncertainty; non-gap-filled data is more conservative and recommended for transparency, but the study analyzed both separately.

## Evidence

- [results] Further filtering by occurrences in each population highlighted 7,483 metabolite features in non-gap-filled data found in at least six samples in all populations: "Further filtering by occurrences in each population highlighted 7,483 metabolite features in non-gap-filled data found in at least six samples in all populations"
- [methods] Three separate filtering workflows were done: 6 minimum peaks in a row (half the number of samples in a single population): "Three separate filtering workflows were done: 6 minimum peaks in a row (half the number of samples in a single population)"
- [methods] For the six-sample filtering, additional processing was done in R (84) to remove any features that were not found in at least six samples from each population.: "For the six-sample filtering, additional processing was done in R (84) to remove any features that were not found in at least six samples from each population."
- [results] to ensure the greatest transparency, we present the analysis of both gap-filled and non-gap-filled data here: "to ensure the greatest transparency, we present the analysis of both gap-filled and non-gap-filled data here"
- [methods] Instructions for recreating data analyses in R and Python are available as Jupyter Notebook (85) links at: https://github.com/jhaffner09/core_metabolome_2021.: "Instructions for recreating data analyses in R and Python are available as Jupyter Notebook (85) links at: https://github.com/jhaffner09/core_metabolome_2021."
