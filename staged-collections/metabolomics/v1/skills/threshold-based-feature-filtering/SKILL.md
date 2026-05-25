---
name: threshold-based-feature-filtering
description: Use when metabolomics data is analyzed using LC-MS or GC-MS techniques to filter a ranked feature list by applying a quantitative threshold, retaining only features that meet a statistical or importance cutoff for downstream annotation and biological interpretation.
when_to_use_negative:
- Input feature list is already below ~500 features and does not require further reduction for annotation
- No ranking metric or statistical score has been computed; threshold-based filtering requires a quantitative score per feature
- Threshold value is arbitrary or chosen post-hoc from the data distribution (i.e., chosen after inspecting the data); use a pre-specified or cross-validated threshold instead
edam_operation: http://edamontology.org/operation_3695
edam_topics:
- http://edamontology.org/topic_0091
- http://edamontology.org/topic_3172
tools:
- name: random forest
  role: generates variable importance scores for each metabolite feature; thresholds are then applied to these importance values to identify differential features
- name: R programming language
  role: used for applying the variable importance threshold and subsetting the feature table in the analysis workflow
  repo: https://github.com/jhaffner09/core_metabolome_2021
provenance:
  source_task_ids:
  - task_003
  source_papers:
  - doi: 10.1128/msystems.00710-22
    title: Untargeted Fecal Metabolomic Analyses across an Industrialization Gradient Reveal Shared Metabolites and Impact of Industrialization on Fecal Microbiome-Metabolome Interactions
schema_version: 0.2.0
metadata:
  merge_audit:
    n_source_runs: 2
    source_files:
    - outputs/audit_haffner_v2/skills/threshold-based-feature-filtering/SKILL.md
    - outputs/audit_haffner_v2/skills/threshold-based-feature-filtering/skill.md
    merged_at: '2026-05-25T07:15:30.879945+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/threshold-based-feature-filtering@sha256:7d325abe7b5c60284c3d5bb80c7c1e43162e9855e68c1724ed9f4a96d3955e8d
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1128/msystems.00710-22
---

# threshold-based-feature-filtering

## Summary

Filter a ranked feature list (e.g., random-forest variable importance scores) by applying a quantitative threshold to retain only features meeting a statistical or importance cutoff. This skill is used to reduce high-dimensional metabolomic data to a smaller, interpretable set of differential features suitable for downstream annotation and biological interpretation.

## When to use

Apply this skill after computing feature-ranking metrics (e.g., random-forest variable importance, effect sizes, p-values) on a reduced feature set (e.g., top 1,000 most abundant metabolites), when the ranking output contains more features than can be practically annotated or interpreted, and when a biologically or statistically motivated threshold value is available to separate signal from noise.

## When NOT to use

- Input feature list is already below ~500 features and does not require further reduction for annotation
- No ranking metric or statistical score has been computed; threshold-based filtering requires a quantitative score per feature
- Threshold value is arbitrary or chosen post-hoc from the data distribution (i.e., chosen after inspecting the data); use a pre-specified or cross-validated threshold instead

## Inputs

- ranked metabolite feature table (e.g., top 1,000 most abundant features from preprocessed LC-MS/MS metabolomic data)
- variable importance scores or other ranking metric computed per feature (e.g., from random-forest classifier output)

## Outputs

- subset of differential metabolite features meeting the threshold criterion (e.g., 377 features with variable importance > 1.3)
- feature identifiers and their corresponding ranking metric values for the retained features

## How to apply

Extract the ranking metric (e.g., variable importance scores) for all features in the input set. Define a threshold value based on domain knowledge, statistical significance, or prior validation (in this case, variable importance > 1.3). Apply the threshold to the ranked metrics, retaining only features whose metric value exceeds the cutoff. This threshold-based subset is then used for annotation and biological follow-up. The rationale is that thresholding enforces a quantitative, reproducible boundary: features above the threshold are presumed to be truly differential with respect to the outcome (here, industrialization group), while those below are treated as background or noise.

## Related tools

- **random forest** (generates variable importance scores for each metabolite feature; thresholds are then applied to these importance values to identify differential features)
- **R programming language** (used for applying the variable importance threshold and subsetting the feature table in the analysis workflow) — https://github.com/jhaffner09/core_metabolome_2021

## Examples

```
# Pseudocode (R/Python hybrid from workflow context)
# Load preprocessed metabolite feature table and random-forest variable importance scores
# importance_scores <- rf_model$importance
# differential_features <- importance_scores[importance_scores > 1.3]
# export(differential_features, 'differential_metabolites_377.csv')
```

## Evaluation signals

- Threshold value is explicitly specified and reported (e.g., > 1.3) and matches the publication or analysis plan
- Output feature count is consistent with the expected cardinality (377 features retained from input set of 1,000)
- All features in the output satisfy the threshold criterion; spot-check: min(output metric values) >= threshold value
- Retained features show expected biological coherence (e.g., enriched metabolites align with known physiology of the outcome, here industrialization)
- Threshold choice is justified by prior work, cross-validation, or statistical rationale, not arbitrary selection

## Limitations

- Threshold value is specific to this dataset and random-forest model parameterization (tree count up to 200); different feature sets or models may require threshold re-optimization
- Random-forest variable importance is sensitive to feature correlation and multicollinearity; highly correlated features may share importance scores unpredictably
- Gap-filled and non-gap-filled variants of the feature table may yield different variable importance distributions; results should be reported for both to ensure robustness
- Threshold-based filtering discards potentially informative features just below the cutoff; biological significance may not align strictly with statistical importance ranking

## Evidence

- [results] random forest variable importance threshold application: "After applying a variable importance cutoff of >1.3 to subset the most differential metabolite features, 377 features remained"
- [results] random forest on top 1,000 abundant features: "we employed a random forest machine learning algorithm applied to the top 1,000 most abundant metabolite features"
- [results] gap-filled and non-gap-filled data analyzed separately: "to ensure the greatest transparency, we present the analysis of both gap-filled and non-gap-filled data here"
- [results] compound-level annotations of retained differential features: "A total of 163 (43.1%) metabolite features had compound-level annotations"
- [methods] repository housing reproducible analysis code: "Instructions for recreating data analyses in R and Python are available as Jupyter Notebook (85) links at: https://github.com/jhaffner09/core_metabolome_2021."
