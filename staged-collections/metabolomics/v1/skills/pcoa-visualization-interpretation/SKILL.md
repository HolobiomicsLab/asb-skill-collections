---
name: pcoa-visualization-interpretation
description: Use when analyzing metabolomics data through principal-coordinate analysis (PCoA) to visualize clustering patterns and compositional differences in high-dimensional LC-MS, GC-MS, or untargeted lipidomics feature abundance data.
when_to_use_negative:
- Feature abundance table has already been ordinated and visualized; re-running PCoA on the same data wastes computation.
- Categorical grouping variable is continuous (e.g., age, pH) rather than discrete; use regression-based or correlation-based ordination instead.
- Sample size is very small (n < 6 per group); ordination plots become unreliable and visual clustering patterns are meaningless.
edam_operation: http://edamontology.org/operation_3932
edam_topics:
- http://edamontology.org/topic_0121
- http://edamontology.org/topic_3520
tools:
- name: QIIME2
  role: Computes Canberra distance matrices and generates PCoA ordinations from metabolite feature tables
- name: EMPeror
  role: Visualizes PCoA ordinations interactively, supporting 2D/3D rendering and sample coloring by metadata variables
- name: PERMANOVA
  role: Tests statistical significance of group separation observed in PCoA; reports R² (variance explained by group) and P-value
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
    - outputs/audit_haffner_v2/skills/pcoa-visualization-interpretation/SKILL.md
    - outputs/audit_haffner_v2/skills/pcoa-visualization-interpretation/skill.md
    merged_at: '2026-05-25T07:33:56.351002+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/pcoa-visualization-interpretation@sha256:1242ede58a29af6e3100a5cc8db8f3e1a94335dce076a548404835806a63facc
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1128/msystems.00710-22
---

# PCoA visualization and interpretation

## Summary

Principal-coordinate analysis (PCoA) is an ordination technique that projects high-dimensional metabolite feature abundance data into a low-dimensional space to visualize clustering patterns and compositional differences among samples. It is essential for assessing whether sample groups (e.g., industrialization categories) exhibit distinct metabolomic profiles and for interpreting multivariate statistical significance.

## When to use

Apply this skill when you have a metabolite feature abundance table and wish to visualize and interpret whether categorical sample groupings (e.g., industrialization level, geographic origin, treatment) show distinct compositional separation in metabolome space. Use it prior to or alongside PERMANOVA testing to inspect whether the distance metric and grouping structure visually support statistical claims about metabolomic differentiation.

## When NOT to use

- Feature abundance table has already been ordinated and visualized; re-running PCoA on the same data wastes computation.
- Categorical grouping variable is continuous (e.g., age, pH) rather than discrete; use regression-based or correlation-based ordination instead.
- Sample size is very small (n < 6 per group); ordination plots become unreliable and visual clustering patterns are meaningless.

## Inputs

- Metabolite feature abundance table (rows=metabolite features, columns=samples; counts or intensities)
- Sample metadata table with categorical grouping variable (e.g., industrialization group assignment)
- Distance matrix computed from feature abundance (e.g., Canberra distance)

## Outputs

- PCoA ordination plot (2D or 3D scatterplot with samples colored by group)
- Principal coordinate axes and variance explained per axis
- Visual assessment of sample clustering and group separation
- Basis for interpreting PERMANOVA statistical results

## How to apply

Compute a distance matrix from the metabolite feature abundance table using an appropriate distance metric (e.g., Canberra distance for metabolomic data); the choice of metric affects which features drive separation. Apply PCoA decomposition to convert the distance matrix into principal coordinates, retaining the first two or three axes for visualization. Visualize the resulting ordination using EMPeror or similar software, coloring points by the categorical variable of interest (e.g., industrialization group: urban industrialized, rural industrialized, rural traditional, isolated traditional). Assess whether samples cluster by group, whether clusters are tight or dispersed, and whether any individual samples are outliers. Interpret the percent variance explained by each axis and cross-reference visual patterns with PERMANOVA results (R² and P-value) to judge whether group separation is statistically significant and biologically meaningful. Verify that the distance metric choice does not artificially drive spurious clustering.

## Related tools

- **QIIME2** (Computes Canberra distance matrices and generates PCoA ordinations from metabolite feature tables)
- **EMPeror** (Visualizes PCoA ordinations interactively, supporting 2D/3D rendering and sample coloring by metadata variables)
- **PERMANOVA** (Tests statistical significance of group separation observed in PCoA; reports R² (variance explained by group) and P-value)

## Evaluation signals

- PCoA plot shows visual clustering by industrialization group with minimal within-group scatter and clear between-group separation (or absence thereof, which is also informative)
- Principal coordinate axes together explain ≥50% of total variance (cumulative), indicating that the 2D/3D projection retains major patterns from the distance matrix
- PERMANOVA P-value is concordant with ordination visual pattern: significant P-value (P < 0.05) should correspond to distinct clusters; non-significant P should show overlapping groups
- Comparison of PCoA plots from gap-filled and non-gap-filled data show consistent clustering patterns and group separation, confirming that results are not artifacts of data preprocessing
- Outlier samples visible in the ordination plot can be explained by metadata (e.g., anomalous delay to freezing) or are flagged for quality review

## Limitations

- PCoA is a projection that necessarily loses information; patterns visible in 2D may not represent high-dimensional structure accurately, especially if variance is distributed across many axes.
- Choice of distance metric (e.g., Canberra vs. Bray-Curtis) influences which samples appear close or distant; different metrics can yield different apparent clustering patterns from the same data.
- Delay to initial freezing impacts overall fecal metabolome composition (PERMANOVA P = 0.001, R² = 0.04) and can confound interpretation if not controlled; such technical artifacts may obscure or amplify group signals.
- Visual interpretation of ordination plots is subjective; quantitative statistical tests (PERMANOVA) are required to support claims about group differences.
- Small sample sizes per group reduce the reliability of ordination patterns; clusters may reflect sampling noise rather than true biological differences.

## Evidence

- [results] populations exhibited similar metabolomes based on the degree of industrialization determined by principal-coordinate analysis (PCoA): "populations exhibited similar metabolomes based on the degree of industrialization determined by principal-coordinate analysis (PCoA)"
- [results] permutational multivariate analysis of variance [PERMANOVA] (38) P = 0.001, R2 = 0.140: "permutational multivariate analysis of variance [PERMANOVA] (38) P = 0.001, R2 = 0.140"
- [results] Delay to initial freezing did impact the overall fecal metabolome (PERMANOVA P = 0.001, R2 = 0.04; ANOVA P = 0.4563, eta2 = 6.32e-3), but these effects were overshadowed by the influence of: "Delay to initial freezing did impact the overall fecal metabolome (PERMANOVA P = 0.001, R2 = 0.04; ANOVA P = 0.4563, eta2 = 6.32e-3), but these effects were overshadowed by the influence of"
- [methods] Instructions for recreating data analyses in R and Python are available as Jupyter Notebook (85) links at: https://github.com/jhaffner09/core_metabolome_2021.: "Instructions for recreating data analyses in R and Python are available as Jupyter Notebook (85) links at: https://github.com/jhaffner09/core_metabolome_2021."
