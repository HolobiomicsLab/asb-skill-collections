---
name: multiclass-metabolite-comparison
description: Use when when you have a normalized metabolite abundance matrix with
  sample metadata assigning each sample to one of three or more distinct biological
  classes (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  tools:
  - margheRita
  - R
  - notame
  - MS-DIAL
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1101/2024.06.20.599545v1
  title: MargheRita
- doi: 10.1101/2024.06.20.599545
  title: ''
evidence_spans:
- The R package margheRita addresses the complete workflow for metabolomic profiling
  in untargeted studies based on liquid chromatography (LC) coupled with tandem mass
  spectrometry (MS/MS)
- The R package margheRita addresses the complete workflow for metabolomic profiling
- The R package margheRita addresses the complete workflow
- The R package margheRita
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_margherita_cq
    doi: 10.1101/2024.06.20.599545v1
    title: MargheRita
  dedup_kept_from: coll_margherita_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2024.06.20.599545v1
  all_source_dois:
  - 10.1101/2024.06.20.599545v1
  - 10.1101/2024.06.20.599545
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Multiclass metabolite comparison

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Perform univariate statistical testing (ANOVA) across three or more sample classes to identify metabolic features with statistically significant abundance differences, followed by multiple-hypothesis correction and feature filtering. This skill is essential for discovering class-discriminative metabolites in untargeted LC-MS/MS metabolomics studies.

## When to use

When you have a normalized metabolite abundance matrix with sample metadata assigning each sample to one of three or more distinct biological classes (e.g., disease phenotypes, treatment groups, or genetic backgrounds) and you wish to identify which metabolic features show significant differential abundance across those classes. Typical trigger: comparing three or more sample cohorts in a single dataset.

## When NOT to use

- Input is a single case-control pair (binary comparison) — use a univariate t-test or Wilcoxon rank-sum test instead of ANOVA.
- Sample classes are not independent or are nested (e.g., repeated measures within subjects) — use mixed-effects models or paired statistical tests.
- Input has fewer than ~3–5 samples per class — ANOVA will have low statistical power; consider descriptive or effect-size-based approaches instead.

## Inputs

- Normalized metabolite abundance matrix (e.g., Urine_RP_NEG_norm.txt, Urine_RP_POS_norm.txt from MS-DIAL output)
- Sample metadata with class assignments (minimum 3 classes; e.g., AA, DD, MM phenotypes)
- margheRita data object or compatible format (ExpressionSet, SummarizedExperiment, or notame metaboset)

## Outputs

- Table of significant metabolic features with Feature_ID, metabolite names, ANOVA F-statistics, p-values, q-values, and effect sizes
- Filtered feature set passing the q-value cutoff threshold
- Statistical summary (number of features tested, number significant, FDR correction details)

## How to apply

Load the normalized metabolite abundance table (e.g., Urine_RP_NEG_norm.txt format from MS-DIAL) with associated sample class labels (AA, DD, MM, or equivalent) into margheRita as a data object. Apply the univariate() function to compute ANOVA F-statistics and p-values for each metabolite feature across all class levels simultaneously. The function automatically applies Benjamini–Hochberg false discovery rate (FDR) correction to produce q-values. Use select_sign_features() to filter significant features based on a chosen q-value threshold (e.g., q < 0.05 or q < 0.1). Extract and tabulate results including Feature_ID, metabolite names, ANOVA statistics, raw p-values, adjusted q-values, and effect sizes. Verify that the number of significant features is reasonable given your sample size and effect magnitude.

## Related tools

- **margheRita** (R package implementing univariate() and select_sign_features() functions for ANOVA testing and FDR-corrected feature selection across multiple sample classes) — https://github.com/emosca-cnr/margheRita
- **notame** (Alternative R package for non-targeted LC-MS metabolomics preprocessing and statistical analysis; compatible via margheRita export functions (as.metaboset())) — https://github.com/hanhineva-lab/notame
- **R** (Statistical computing environment in which margheRita runs)
- **MS-DIAL** (Upstream peak-picking and feature detection tool; produces normalized abundance tables consumed by margheRita) — http://prime.psc.riken.jp/Metabolomics_Software/MS-DIAL/

## Examples

```
univariate(data = urine_data, class = "phenotype"); sig_features <- select_sign_features(univariate_result, q_cutoff = 0.05)
```

## Evaluation signals

- Verify that the number of features tested matches the row count of the input abundance matrix.
- Confirm that q-values are monotonically non-decreasing when sorted by p-value (required property of FDR correction).
- Check that the number of features passing the q-value threshold is consistent with the applied cutoff and the distribution of raw p-values.
- Inspect effect sizes (e.g., eta-squared) to ensure significant features have biologically meaningful magnitude differences, not just statistical significance.
- Validate that sample class assignments are correctly reflected in the feature grouping used for ANOVA (e.g., three groups for AA/DD/MM).

## Limitations

- ANOVA assumes normality of residuals within each class; violation can inflate false positives — consider non-parametric alternatives (Kruskal–Wallis) for heavily skewed data.
- Multiple testing correction (Benjamini–Hochberg FDR) controls the false discovery rate but may still produce false positives if the number of features is very large relative to sample size.
- ANOVA tests for any difference among classes but does not specify which classes differ; post-hoc pairwise tests (e.g., Tukey HSD) are needed to identify class-pair contrasts.
- Missing values must be handled before ANOVA; margheRita supports multiple imputation strategies, but the choice can influence results.
- Effect size interpretation depends on the biological context and instrument; no universal threshold for 'significant' effect magnitude exists.

## Evidence

- [other] univariate() function to compute ANOVA F-statistics and p-values across the three class levels for each metabolite feature: "Apply univariate() function to compute ANOVA F-statistics and p-values across the three class levels for each metabolite feature."
- [other] select_sign_features() to filter significant features based on q-value threshold (Benjamini–Hochberg FDR correction applied during univariate or select_sign_features step): "Use select_sign_features() to filter significant features based on q-value threshold (Benjamini–Hochberg FDR correction applied during univariate or select_sign_features step)."
- [other] Extract and tabulate the results including feature identifiers, ANOVA statistics, p-values, q-values, and effect sizes: "Extract and tabulate the results including feature identifiers, ANOVA statistics, p-values, q-values, and effect sizes."
- [readme] simplified execution of parametric and non-parametric statistical tests over a large number of features: "simplified execution of parametric and non-parametric statistical tests over a large number of features"
- [other] ANOVA testing across AA, DD, and MM class levels in the Urine dataset identified significant metabolic features, with results reported in a table including Feature_ID, metabolite names, and associated q-values for filtering at specified cutoffs: "ANOVA testing across AA, DD, and MM class levels in the Urine dataset identified significant metabolic features, with results reported in a table including Feature_ID, metabolite names, and"
