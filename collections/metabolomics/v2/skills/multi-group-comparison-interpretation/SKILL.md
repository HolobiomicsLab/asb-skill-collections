---
name: multi-group-comparison-interpretation
description: Use when after performing an ANOVA-style multi-group de_design() analysis
  on a LipidomicsExperiment object, when you need to determine whether a categorical
  sample variable (e.g., Cancer Stage, SampleType, Race) significantly associates
  with the lipid molecular profile.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - lipidr
  - limma
  - R
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.jproteome.0c00082
  title: lipidr
evidence_spans:
- Datasets can be easily downloaded and parsed into `LipidomicsExperiment` object
  using `lipidr` function `fetch_mw_study()`
- '`lipidr` allows users, to quickly explore public lipidomics experiments. `lipidr`
  provides an easy way to re-analyze and visualize these datasets.'
- This step of the workflow requires the `limma` package to be installed.
- Data Mining and Analysis of Lipidomics Datasets in R
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidr_cq
    doi: 10.1021/acs.jproteome.0c00082
    title: lipidr
  dedup_kept_from: coll_lipidr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.0c00082
  all_source_dois:
  - 10.1021/acs.jproteome.0c00082
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# multi-group-comparison-interpretation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Interpret ANOVA-style multi-group differential expression results in lipidomics by extracting and filtering significant molecules, then contextualizing findings within the biological sample grouping structure. This skill involves validating whether the grouping variable meaningfully stratifies the lipid molecular profile.

## When to use

After performing an ANOVA-style multi-group de_design() analysis on a LipidomicsExperiment object, when you need to determine whether a categorical sample variable (e.g., Cancer Stage, SampleType, Race) significantly associates with the lipid molecular profile. Specifically, use this skill when you have computed p-values and adjusted p-values across multiple lipid molecules and must decide whether the grouping variable has a true biological effect—or whether no significant molecules were identified, indicating the variable does not stratify the lipid profile.

## When NOT to use

- Input is already a pre-filtered list of known biomarkers—skip interpretation and proceed directly to validation or visualization.
- Sample size is very small (n < 3 per group) or groups are severely imbalanced—ANOVA power is low and non-significance may be a false negative.
- You have not yet performed quality control (QC) on the dataset—outlier samples or failed assays can inflate or deflate significance.

## Inputs

- de_design() results object (limma-fitted model with significant_molecules table)
- LipidomicsExperiment object (processed lipidomics data with sample annotations)
- Grouping variable metadata (e.g., Stage, SampleType, Race annotations)

## Outputs

- Filtered significant_molecules table (lipids with adjusted p-values above or below threshold)
- Count and summary statistics of significant vs. non-significant molecules
- Interpretation statement (e.g., 'no significant molecules identified', 'X molecules significantly associated')
- Volcano plot or effect-size visualization
- Contextualized finding linking univariate results to multivariate patterns

## How to apply

Extract the significant_molecules table from the de_design() results object, typically by filtering for adjusted p-value (padj) threshold—commonly p > 0.05 to identify non-significant associations or p < 0.05 for significant ones depending on your hypothesis direction. Count the number of lipid molecules meeting significance criteria and assess their biological relevance. Cross-reference findings with PCA or PCoA multivariate results to corroborate whether the grouping variable produces visible clustering; if ANOVA yields no significant molecules but PCA shows group separation, this may indicate weak univariate effects masked by multivariate patterns. Document the count and nature of significant molecules (e.g., lipid classes, chain-length patterns) and explicitly state whether the grouping variable meaningfully affects the lipid molecular profile. Use volcano plots or similar visualizations to inspect the distribution of p-values and effect sizes across all molecules.

## Related tools

- **lipidr** (Provides de_design() function for ANOVA-style multi-group differential expression and significant_molecules table extraction; integrates LipidomicsExperiment object representation) — https://github.com/ahmohamed/lipidr
- **limma** (Underlying statistical engine for ANOVA-style contrasts and p-value computation in de_design())
- **R** (Execution environment for lipidr workflow and statistical interpretation)

## Examples

```
multi_group <- de_design(d, ~ Stage); sig_lipids <- multi_group$significant_molecules; nrow(sig_lipids[sig_lipids$padj < 0.05, ])
```

## Evaluation signals

- Adjusted p-value distribution is reasonable (not uniformly zero or one); QQ-plot of raw p-values shows expected inflation at tail for non-significant molecules.
- Count of significant molecules is reported explicitly and matches the filtering threshold applied (e.g., 'no significant molecules identified at padj > 0.05').
- Interpretation is consistent with multivariate analysis (PCA/PCoA): if ANOVA finds no significant molecules, PCA should show minimal or no group separation; conversely, strong PCA clustering should correlate with ≥ some significant molecules in ANOVA.
- Volcano plot shows reasonable distribution of effect sizes and p-values; extreme outliers are visually identifiable and biologically plausible (e.g., lipid classes known to vary with disease stage).
- Findings statement includes explicit qualifier about magnitude of effect (e.g., 'small Race effect', 'no effect of Cancer Stage') grounded in molecule counts and/or effect-size ranges.

## Limitations

- ANOVA assumes equal variance across groups; if violated, p-values may be biased. Diagnostics (e.g., Levene's test) should be performed separately.
- Multiple-testing correction (e.g., Benjamini-Hochberg) controls false discovery rate but may still miss weak biological effects in small cohorts or high-dimensional datasets.
- Lack of significant molecules does not prove absence of biological association—it may reflect low univariate effect size, high noise, or insufficient sample size; multivariate or alternative statistical methods may reveal patterns.
- Interpretation depends on sample annotation quality and grouping variable definition; miscoded or mislabeled samples will yield spurious or misleading results.
- Results are specific to the lipids assayed and the measurement platform (e.g., Skyline MS/MS data); findings may not generalize to untargeted or alternative analytical methods.

## Evidence

- [intro] multi_group <- de_design(d, ~ Stage): "Perform multi-group differential expression analysis using ANOVA-style design"
- [other] Extract the significant_molecules table from the de_design results, filtering for lipids with adjusted p-value > 0.05 (non-significant).: "Extract the significant_molecules table from the de_design results, filtering for lipids with adjusted p-value > 0.05 (non-significant)"
- [other] Cancer stage does not appear to affect lipid molecules profiled in the experiment, as no significant molecules were identified in the ANOVA-style multi-group comparison using stage as the grouping variable.: "Cancer stage does not appear to affect lipid molecules profiled in the experiment, as no significant molecules were identified in the ANOVA-style multi-group comparison using stage as the grouping"
- [intro] Surprisingly, Cancer Stage does not appear to affect lipid molecules profiled in this experiment.: "Surprisingly, Cancer Stage does not appear to affect lipid molecules profiled in this experiment"
- [intro] In this case, we are seeing similar pattern as the two-group comparison, which indicates a small Race effect.: "In this case, we are seeing similar pattern as the two-group comparison, which indicates a small Race effect"
