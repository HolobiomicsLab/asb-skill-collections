---
name: permanova-beta-diversity-testing
description: Use when analyzing metabolomics data with PERMANOVA to test if a categorical variable explains significant variance in metabolome composition based on a distance matrix.
when_to_use_negative:
- Distance matrix has not yet been computed from the feature table — compute distance first.
- Grouping variable is continuous (e.g., age in years) rather than categorical — use Mantel test or distance-based linear regression instead.
- Sample size is very small (n < 4 per group) — permutation test power is limited and results may be unreliable.
edam_operation: http://edamontology.org/operation_3799
edam_topics:
- http://edamontology.org/topic_0091
- http://edamontology.org/topic_3520
tools:
- name: QIIME2
  role: Computes Canberra distance matrix from feature table and executes PERMANOVA with permutation testing and effect size calculation
- name: EMPeror
  role: Visualizes PCoA ordinations derived from the distance matrix to show metabolome clustering by group
- name: principal-coordinate analysis (PCoA)
  role: Ordination method applied to the distance matrix to generate low-dimensional visualization prior to or alongside PERMANOVA statistical testing
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
    - outputs/audit_haffner_v2/skills/permanova-beta-diversity-testing/SKILL.md
    - outputs/audit_haffner_v2/skills/permanova-beta-diversity-testing/skill.md
    merged_at: '2026-05-25T06:57:01.498885+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/permanova-beta-diversity-testing@sha256:85446bc795c46f0007ecc7f5a73a86c95a4a51fda255189878d583c53bae8e95
derived_from:
- doi: 10.1128/msystems.00710-22
---

# permanova-beta-diversity-testing

## Summary

PERMANOVA tests whether a categorical variable (e.g., industrialization group) explains statistically significant variance in metabolome composition by permuting group assignments across a distance matrix. This skill assesses beta-diversity structure and effect size when exploring how sample metadata drives metabolite feature abundance patterns.

## When to use

When you have a distance matrix computed from metabolite feature abundances (e.g., Canberra distance) and a categorical grouping variable (industrialization group, geographic origin, disease state), and you want to test whether that grouping explains significant multivariate compositional variance and quantify effect size (R²). Do NOT use this skill before computing a distance metric or if groups are continuous.

## When NOT to use

- Distance matrix has not yet been computed from the feature table — compute distance first.
- Grouping variable is continuous (e.g., age in years) rather than categorical — use Mantel test or distance-based linear regression instead.
- Sample size is very small (n < 4 per group) — permutation test power is limited and results may be unreliable.

## Inputs

- Canberra distance matrix computed from metabolite feature abundance table
- Sample metadata table with categorical grouping variable (e.g., industrialization group: urban industrialized, rural industrialized, rural traditional, isolated traditional)

## Outputs

- PERMANOVA result object with R² (proportion of variance explained), P-value, and test statistic
- Summary table reporting R², P-value, and significance annotation for the grouping variable

## How to apply

Compute a Canberra distance matrix from the non-gap-filled metabolite feature table using QIIME2 (or equivalent). Run PERMANOVA via QIIME2 with the categorical variable (e.g., industrialization group) as the predictor. PERMANOVA permutes group labels across the distance matrix and calculates the proportion of variance explained (R²) and empirical P-value under the null hypothesis that group explains no variance. Interpret P < 0.05 as statistically significant association. Report both R² (effect size; here 0.140 for industrialization) and P-value (here 0.001). Note that effect sizes may be modest even when P-values are significant due to multiple confounders (age, sex, freeze delay); use ANOVA on individual features as a complementary univariate test.

## Related tools

- **QIIME2** (Computes Canberra distance matrix from feature table and executes PERMANOVA with permutation testing and effect size calculation)
- **EMPeror** (Visualizes PCoA ordinations derived from the distance matrix to show metabolome clustering by group)
- **principal-coordinate analysis (PCoA)** (Ordination method applied to the distance matrix to generate low-dimensional visualization prior to or alongside PERMANOVA statistical testing)

## Examples

```
qiime diversity beta-group-significance --i-distance-matrix canberra_distance_matrix.qza --m-metadata-file sample_metadata.txt --m-metadata-column industrialization_group --o-visualization permanova_result.qzv
```

## Evaluation signals

- P-value is computed via permutation (typically ≥ 999 permutations); verify that the number of permutations is sufficient (usually reported in output).
- R² value is between 0 and 1 and represents the proportion of total variance explained by the grouping variable; compare to univariate effect sizes (e.g., partial eta-squared from ANOVA) to assess consistency.
- Significant P-value (P < 0.05) should be paired with meaningful R² (e.g., R² ≥ 0.05); small R² even with P < 0.05 indicates weak biological effect due to large sample size.
- PERMANOVA results should be robust across different distance metrics (e.g., Canberra, Bray-Curtis) if the signal is strong; verify robustness by re-running with an alternative metric.
- PCoA biplot or ordination plot should visually show separation of groups along principal coordinates; clusters should align with significant grouping variables identified by PERMANOVA.

## Limitations

- PERMANOVA assumes homogeneity of multivariate dispersions; use a betadispersion test (QIIME2 beta-group-significance) to verify that groups do not differ only in spread rather than location.
- Effect size (R²) can be modest (0.04–0.14) even for statistically significant associations in observational data with confounders; interpret in context of biological relevance and cofactor ANOVA tests.
- Delay to initial freezing impacted metabolome variance (PERMANOVA P = 0.001, R² = 0.04), but biological variables (industrialization) overshadowed this effect; always report and control for technical metadata.
- Multiple testing of different grouping variables (age, sex, geography) can inflate Type I error; report Bonferroni-corrected or FDR-adjusted P-values when testing multiple hypotheses.
- PERMANOVA does not identify which individual features drive the grouping; combine with univariate feature-level tests (Kruskal-Wallis, random forest) to identify discriminatory metabolites.

## Evidence

- [results] permutational multivariate analysis of variance [PERMANOVA] (38) P = 0.001, R2 = 0.140: "permutational multivariate analysis of variance [PERMANOVA] (38) P = 0.001, R2 = 0.140"
- [results] populations exhibited similar metabolomes based on the degree of industrialization determined by principal-coordinate analysis (PCoA): "populations exhibited similar metabolomes based on the degree of industrialization determined by principal-coordinate analysis (PCoA)"
- [results] Delay to initial freezing did impact the overall fecal metabolome (PERMANOVA P = 0.001, R2 = 0.04; ANOVA P = 0.4563, eta2 = 6.32e-3), but these effects were overshadowed by the influence of: "Delay to initial freezing did impact the overall fecal metabolome (PERMANOVA P = 0.001, R2 = 0.04; ANOVA P = 0.4563, eta2 = 6.32e-3), but these effects were overshadowed by the influence of"
- [results] industrialization had a stronger influence on metabolic similarity between populations than geographic origin, age, or sex (Fig. 1c; ANOVA industrialization group P = 0.046, effect size [partial: "industrialization had a stronger influence on metabolic similarity between populations than geographic origin, age, or sex"
- [methods] Instructions for recreating data analyses in R and Python are available as Jupyter Notebook (85) links at: https://github.com/jhaffner09/core_metabolome_2021.: "Instructions for recreating data analyses in R and Python are available as Jupyter Notebook (85) links at: https://github.com/jhaffner09/core_metabolome_2021."
