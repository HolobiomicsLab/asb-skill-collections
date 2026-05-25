---
name: multivariate-microbiome-analysis
description: Use when conducting multivariate analysis in metabolomics with techniques such as ordination (PCoA), permutation testing (PERMANOVA), and machine learning to assess population-level differences in microbial and metabolite composition based on categorical factors.
when_to_use_negative:
- Feature table is already filtered to a small set of pre-identified discriminant features; use univariate testing instead.
- Samples lack clear categorical grouping metadata or the grouping variable has too few replicates per group (typically <3 samples per group will yield unreliable permutation tests).
- Data are compositional with extreme sparsity (>99% zeros); consider rarefaction, centered log-ratio transformation, or compositional distance metrics before ordination.
edam_operation: http://edamontology.org/operation_3697
edam_topics:
- http://edamontology.org/topic_3172
- http://edamontology.org/topic_3174
tools:
- name: QIIME2
  role: Construct Canberra distance matrix from metabolite feature table and perform PERMANOVA on distance matrix with grouping variable
- name: EMPeror
  role: Visualize PCoA ordination plot from distance matrix, colored and faceted by categorical metadata
- name: PERMANOVA
  role: Test null hypothesis that industrialization group (or other categorical factor) explains no variance in metabolite or ASV composition; report R² and P-value
- name: random forest
  role: Identify differential features by ranking variable importance on top 1,000 most abundant features; apply importance cutoff (>1.3) to subset discriminant features
- name: mmvec (microbe-metabolite vectors)
  role: Learn neural network embeddings of co-occurrence between microbial ASVs and metabolite features; subset results to shared annotated metabolites and major predictive taxa
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
    - outputs/audit_haffner_v2/skills/multivariate-microbiome-analysis/SKILL.md
    - outputs/audit_haffner_v2/skills/multivariate-microbiome-analysis/skill.md
    merged_at: '2026-05-25T07:33:56.363963+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/multivariate-microbiome-analysis@sha256:df37a8af4046d901278ad808ecf2b6d6cb8b4ff42d2adb7d771fd934157e7f5c
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1128/msystems.00710-22
---

# multivariate-microbiome-analysis

## Summary

Multivariate analysis of microbiome and metabolomic data using ordination (PCoA), permutation testing (PERMANOVA), and machine learning to identify population-level differences in microbial and metabolite composition. This skill tests whether categorical factors (e.g., industrialization group, geographic origin) explain significant variance in community structure.

## When to use

Apply this skill when you have a feature abundance table (metabolite features, ASVs, or OTUs) paired with sample metadata containing categorical grouping variables (e.g., industrialization status, population, treatment), and you need to test whether group membership explains statistically significant variance in community composition. Use it as a first-pass exploratory and hypothesis-testing step before identifying individual discriminant features.

## When NOT to use

- Feature table is already filtered to a small set of pre-identified discriminant features; use univariate testing instead.
- Samples lack clear categorical grouping metadata or the grouping variable has too few replicates per group (typically <3 samples per group will yield unreliable permutation tests).
- Data are compositional with extreme sparsity (>99% zeros); consider rarefaction, centered log-ratio transformation, or compositional distance metrics before ordination.

## Inputs

- non-gap-filled or gap-filled feature abundance table (rows: features; columns: samples)
- sample metadata table with categorical grouping variable and covariates (age, sex, storage delay, etc.)
- distance matrix (Canberra, Euclidean, Bray-Curtis, UniFrac) or raw feature counts for distance calculation

## Outputs

- PCoA ordination plot (EMPeror visualization or equivalent) colored by grouping variable
- PERMANOVA results table with R², F-statistic, and P-value for each factor
- ANOVA results for univariate comparisons (effect sizes, eta²)
- subset of differential features (e.g., 377 features after variable importance >1.3 cutoff)

## How to apply

First, compute a distance matrix (e.g., Canberra distance for metabolomic features or UniFrac for microbial ASVs) from the normalized or non-gap-filled feature abundance table using a tool like QIIME2. Second, generate a principal-coordinate analysis (PCoA) plot from the distance matrix and visualize it using EMPeror or equivalent, coloring samples by the categorical variable of interest to inspect for visual clustering. Third, perform PERMANOVA on the distance matrix and metadata, specifying the grouping variable as the fixed effect; report the R² (proportion of variance explained) and permutation-based P-value (typically 999 permutations). Document confounders (e.g., age, sex, storage delay) by testing them as separate PERMANOVA terms and comparing effect sizes (R²) to identify whether the primary factor dominates. If PERMANOVA is significant, proceed to univariate filtering (e.g., variable importance cutoff >1.3 in random forest) to isolate differential features; verify results are consistent across gap-filled and non-gap-filled datasets.

## Related tools

- **QIIME2** (Construct Canberra distance matrix from metabolite feature table and perform PERMANOVA on distance matrix with grouping variable)
- **EMPeror** (Visualize PCoA ordination plot from distance matrix, colored and faceted by categorical metadata)
- **PERMANOVA** (Test null hypothesis that industrialization group (or other categorical factor) explains no variance in metabolite or ASV composition; report R² and P-value)
- **random forest** (Identify differential features by ranking variable importance on top 1,000 most abundant features; apply importance cutoff (>1.3) to subset discriminant features)
- **mmvec (microbe-metabolite vectors)** (Learn neural network embeddings of co-occurrence between microbial ASVs and metabolite features; subset results to shared annotated metabolites and major predictive taxa)

## Examples

```
qiime diversity beta --i-table feature-table.qza --p-metric canberra --o-distance-matrix canberra-dm.qza; qiime diversity pcoa --i-distance-matrix canberra-dm.qza --o-pcoa pcoa.qza; qiime diversity beta-group-significance --i-distance-matrix canberra-dm.qza --m-metadata-file sample-metadata.tsv --m-metadata-column industrialization_group --o-visualization permanova-results.qzv
```

## Evaluation signals

- PCoA plot shows clear visual separation of samples by the primary grouping variable (e.g., industrialization status) with minimal overlap; points in the same group cluster tightly.
- PERMANOVA P-value is ≤0.05 and R² is substantially larger (e.g., >0.10) than confounding factors (e.g., age, sex, storage delay); effect size hierarchy matches biological expectation.
- Differential features (subset by variable importance >1.3) show consistent direction of enrichment when compared across gap-filled and non-gap-filled datasets (i.e., same features upregulated in the same groups).
- ANOVA on univariate metabolite abundances (e.g., Kruskal-Wallis) for top differential features yields P-values consistent with the multivariate finding (e.g., P ≤ 0.01 for strong signals).
- Distance matrix metric (e.g., Canberra) is appropriate for the data type and matches the study's sampling design; verify metric choice is justified (e.g., Canberra for non-negative metabolite abundances).

## Limitations

- PERMANOVA assumes exchangeability of samples within groups and can yield inflated P-values if pseudoreplication or hierarchical structure (e.g., multiple samples per subject) is present; specify the correct design in the test.
- PCoA captures only the first few principal coordinates; rare or weak signals may be obscured. Visualize multiple PC axes (PC1 vs PC2, PC1 vs PC3) to assess robustness.
- Gap-filling (imputation of missing values) can artificially inflate similarity and inflate R² values; present results for both gap-filled and non-gap-filled data separately to assess sensitivity, as the authors did.
- Storage delay and sample handling (e.g., delay to freezing) can confound results by introducing technical variance comparable to biological signal; always test and report such covariates.
- The variable importance cutoff (e.g., >1.3) is arbitrary; sensitivity analysis (e.g., cutoffs 1.0–2.0) is recommended to verify that identified differential features are robust across thresholds.

## Evidence

- [results] populations exhibited similar metabolomes based on the degree of industrialization determined by principal-coordinate analysis (PCoA): "populations exhibited similar metabolomes based on the degree of industrialization determined by principal-coordinate analysis (PCoA"
- [results] permutational multivariate analysis of variance [PERMANOVA] (38) P = 0.001, R2 = 0.140: "permutational multivariate analysis of variance [PERMANOVA] (38) P = 0.001, R2 = 0.140"
- [results] industrialization had a stronger influence on metabolic similarity between populations than geographic origin, age, or sex: "industrialization had a stronger influence on metabolic similarity between populations than geographic origin, age, or sex (Fig. 1c; ANOVA industrialization group P = 0.046, effect size [partial"
- [methods] Construct Canberra distance metrics from the feature abundance matrix using QIIME2. Generate PCoA plots using the computed distance matrix and visualize using EMPeror.: "Construct Canberra distance metrics from the feature abundance matrix using QIIME2. Generate PCoA plots using the computed distance matrix and visualize using EMPeror. Execute PERMANOVA via QIIME2"
- [results] to ensure the greatest transparency, we present the analysis of both gap-filled and non-gap-filled data here: "to ensure the greatest transparency, we present the analysis of both gap-filled and non-gap-filled data here"
- [results] After applying a variable importance cutoff of >1.3 to subset the most differential metabolite features, 377 features remained: "After applying a variable importance cutoff of >1.3 to subset the most differential metabolite features, 377 features remained"
