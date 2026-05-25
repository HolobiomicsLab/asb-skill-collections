---
name: metabolite-feature-table-distance-metric-computation
description: Use when computing pairwise distance metrics (Canberra) from a metabolite feature abundance matrix in the domain of metabolomics for ordination and statistical testing of metabolome composition differences across sample groups.
when_to_use_negative:
- Input is already a pre-computed distance or dissimilarity matrix—skip directly to ordination or PERMANOVA.
- Feature table contains gap-filled data and you require only non-gap-filled analysis (compute distance separately on non-gap-filled subset).
- Sample groups are nested or have hierarchical structure requiring mixed-model analysis rather than flat group assignment.
edam_operation: http://edamontology.org/operation_3279
edam_topics:
- http://edamontology.org/topic_0091
- http://edamontology.org/topic_3520
tools:
- name: QIIME2
  role: Compute Canberra distance matrix from metabolite feature abundance table; output serves as input to PCoA and PERMANOVA commands.
  repo: https://github.com/qiime2/qiime2
- name: EMPeror
  role: Visualize PCoA plots generated from the computed distance matrix to explore metabolome ordination space.
provenance:
  source_task_ids:
  - task_001
  source_papers:
  - doi: 10.1128/msystems.00710-22
    title: Untargeted Fecal Metabolomic Analyses across an Industrialization Gradient Reveal Shared Metabolites and Impact of Industrialization on Fecal Microbiome-Metabolome Interactions
schema_version: 0.2.0
metadata:
  merge_audit:
    n_source_runs: 2
    source_files:
    - outputs/audit_haffner_v2/skills/metabolite-feature-table-distance-metric-computation/SKILL.md
    - outputs/audit_haffner_v2/skills/metabolite-feature-table-distance-metric-computation/skill.md
    merged_at: '2026-05-25T07:04:57.473077+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/metabolite-feature-table-distance-metric-computation@sha256:beda4f1f86123bd66f9d54e5d2af3265de3168d37023fd51fbadff2176f9f56f
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1128/msystems.00710-22
---

# metabolite-feature-table-distance-metric-computation

## Summary

Compute pairwise distance metrics (Canberra) from a metabolite feature abundance matrix to enable ordination and statistical testing of metabolome composition differences across sample groups. This skill transforms raw feature abundances into a distance/dissimilarity matrix that quantifies metabolic differences between samples.

## When to use

When you have a filtered, normalized metabolite feature table (rows = metabolites/features, columns = samples; abundances in place) and need to test whether defined sample groups (e.g., industrialization level, treatment, phenotype) show significant differences in overall metabolome composition. Use this skill specifically when planning to perform PCoA ordination or PERMANOVA significance testing.

## When NOT to use

- Input is already a pre-computed distance or dissimilarity matrix—skip directly to ordination or PERMANOVA.
- Feature table contains gap-filled data and you require only non-gap-filled analysis (compute distance separately on non-gap-filled subset).
- Sample groups are nested or have hierarchical structure requiring mixed-model analysis rather than flat group assignment.

## Inputs

- Metabolite feature abundance table (biom or CSV format; rows=features, columns=samples, values=peak intensities or normalized abundances)
- Sample metadata mapping file (associating sample IDs with group labels, e.g., industrialization group)
- Feature presence/absence information if filtering by prevalence thresholds

## Outputs

- Distance matrix (symmetric, samples × samples, Canberra dissimilarity values between 0 and 1+)
- Distance matrix file in QIIME2-compatible format (e.g., DistanceMatrix artifact) for downstream PCoA and PERMANOVA

## How to apply

Load the non-gap-filled metabolite feature abundance matrix (filtered to presence in ≥6 samples per population or other threshold) as input. Specify Canberra distance as the distance metric—this metric is scale-invariant and suitable for sparse metabolomic data with many zeros. Invoke QIIME2's distance computation command on the feature table, which will output a symmetric distance matrix (samples × samples). Verify that the output matrix has no NaN or infinite values, is symmetric, and has zeros on the diagonal. This distance matrix is then used downstream in PCoA and PERMANOVA. The Canberra metric emphasizes rare features and penalizes zero-to-nonzero pairs, making it appropriate for detecting subtle metabolic differences across industrialization gradients.

## Related tools

- **QIIME2** (Compute Canberra distance matrix from metabolite feature abundance table; output serves as input to PCoA and PERMANOVA commands.) — https://github.com/qiime2/qiime2
- **EMPeror** (Visualize PCoA plots generated from the computed distance matrix to explore metabolome ordination space.)

## Examples

```
qiime diversity beta --i-table feature-table.qza --p-metric canberra --o-distance-matrix canberra-distance.qza
```

## Evaluation signals

- Distance matrix is symmetric: dist[i,j] == dist[j,i] for all sample pairs (i, j).
- Diagonal elements are zero: dist[i,i] == 0 for all samples.
- All distance values are non-negative and finite (no NaN or Inf).
- Distance values fall within expected range for Canberra metric: typically [0, 1] for normalized data, potentially higher for unnormalized abundances.
- PCoA ordination plot generated from the distance matrix shows visual separation along axes corresponding to sample group (e.g., industrialization level).
- PERMANOVA applied to the distance matrix yields R² and P-value consistent with stated findings (e.g., R² = 0.140, P = 0.001 for industrialization group).

## Limitations

- Canberra distance is sensitive to zero-inflation and can give high weights to rare features; sparse metabolomic data with many missing/zero values may produce uninformative ordination.
- Distance computation does not account for hierarchical or nested structure in samples; all groups are treated as independent.
- Output distance matrix is only as good as the input feature table: contamination, technical replicates, or uncontrolled batch effects in the abundance data will propagate into distance distortion.
- Delay to initial freezing of fecal samples was shown to impact overall metabolome (PERMANOVA P = 0.001, R² = 0.04), so preprocessing steps (e.g., sample storage time, freeze-thaw cycles) can confound distance-based inference.

## Evidence

- [methods] Canberra distance metric specification and QIIME2 usage: "Construct Canberra distance metrics from the feature abundance matrix using QIIME2"
- [results] Expected output: distance matrix for ordination: "populations exhibited similar metabolomes based on the degree of industrialization determined by principal-coordinate analysis (PCoA)"
- [results] PERMANOVA significance and effect size from distance-based analysis: "permutational multivariate analysis of variance [PERMANOVA] (38) P = 0.001, R2 = 0.140"
- [results] Input feature table filtering and non-gap-filled requirement: "Further filtering by occurrences in each population highlighted 7,483 metabolite features in non-gap-filled data found in at least six samples in all populations"
- [results] Preprocessing and sample handling impact on metabolomic distance inference: "Delay to initial freezing did impact the overall fecal metabolome (PERMANOVA P = 0.001, R2 = 0.04; ANOVA P = 0.4563, eta2 = 6.32e-3), but these effects were overshadowed by the influence of"
