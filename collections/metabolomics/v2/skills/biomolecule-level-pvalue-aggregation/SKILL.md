---
name: biomolecule-level-pvalue-aggregation
description: Use when after running iMd-ANOVA or G-test statistical analysis on normalized omics expression data with multiple biomolecules and group comparisons.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - pmartR
  - R
  - Shiny
  - PMart_ShinyApp
derived_from:
- doi: 10.1021/acs.jproteome.3c00512
  title: PMart
evidence_spans:
- Shiny GUI implementation of the pmartR R package.
- Shiny GUI implementation of the pmartR R package
- the bulk of the functionality of the package to be available to the user without the need for familiarity with R or the package itself
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pmart_cq
    doi: 10.1021/acs.jproteome.3c00512
    title: PMart
  dedup_kept_from: coll_pmart_cq
schema_version: 0.2.0
---

# biomolecule-level-pvalue-aggregation

## Summary

Apply False Discovery Rate (FDR) correction to p-values from statistical tests (ANOVA, G-test) across multiple biomolecules and comparisons to control the false discovery rate in omics biomarker identification. This skill converts raw test p-values into adjusted p-values suitable for multiple-testing inference at the biomolecule level.

## When to use

After running iMd-ANOVA or G-test statistical analysis on normalized omics expression data with multiple biomolecules and group comparisons. Use this skill when the number of hypothesis tests (one per biomolecule × contrast pair) exceeds ~10 and you need to bound the expected proportion of false positives among rejected hypotheses rather than control per-test Type I error.

## When NOT to use

- Single biomolecule analysis or very few simultaneous tests (< 5), where individual p-value thresholds are adequate
- When the study design requires per-comparison error rate control (e.g., planned orthogonal contrasts) rather than false discovery rate control
- If raw p-values have already been corrected by another method upstream (e.g., Bonferroni in the test itself)

## Inputs

- Raw p-values from iMd-ANOVA or G-test (one per biomolecule and contrast)
- Number of tests / biomolecules in the analysis
- User-selected significance level (α, typically 0.05)

## Outputs

- Adjusted p-values (FDR-corrected) for each biomolecule test
- Ranked list of biomolecules ordered by adjusted p-value
- Biomarker candidates selected at the chosen adjusted p-value threshold

## How to apply

Within the pmartR-Shiny statistical analysis workflow, after computing raw p-values from ANOVA or G-test results: (1) select the FDR correction option in the p-value adjustment interface instead of 'no correction'; (2) the Benjamini–Hochberg FDR procedure is applied to the set of raw p-values, sorting them and computing adjusted p-values such that the expected false discovery rate across all biomolecules remains below the chosen α threshold (typically 0.05); (3) adjusted p-values are computed and displayed alongside raw p-values in the test results; (4) biomolecules are then ranked and selected for biomarker determination using the adjusted p-value cutoff. FDR control is justified when multiple biomolecules are tested simultaneously and you can tolerate a small expected proportion of false positives in exchange for increased power.

## Related tools

- **pmartR** (R package providing ANOVA and G-test statistical test implementations and p-value computation for omics data; backend for FDR correction workflow) — https://github.com/pmartR/pmartR
- **Shiny** (GUI framework exposing pmartR statistical analysis capabilities and p-value adjustment options as user-selectable parameters) — https://shiny.posit.co
- **PMart_ShinyApp** (Web application implementing the iMd-ANOVA workflow with integrated FDR correction option in the statistical analysis tab) — https://github.com/pmartR/PMart_ShinyApp

## Evaluation signals

- Adjusted p-values are monotonically increasing when sorted in ascending order (non-decreasing property of FDR correction)
- Adjusted p-values are ≥ corresponding raw p-values for each biomolecule
- The number of rejected hypotheses at the adjusted p-value cutoff is ≤ the number at the raw p-value cutoff
- For a chosen α threshold, the expected proportion of false positives among rejected biomolecules is ≤ α
- Adjusted p-values correctly match output from standard R implementations (e.g., `p.adjust(..., method='BH')`) for the same raw p-value input

## Limitations

- FDR correction assumes independence or positive correlation among biomolecule tests; if tests are highly negatively correlated, the method may be conservative
- FDR control bounds the *expected* false discovery rate over many replicate experiments, not a fixed bound for a single experiment
- Sample size and effect size directly affect power; FDR correction does not recover statistical power lost to small sample size or weak signals
- The pmartR-Shiny implementation (as of the February release described) supports FDR but does not expose other p-value adjustment methods (e.g., Bonferroni, Holm); users requiring alternative corrections must export results and post-process outside the interface

## Evidence

- [other] The February release adding p-value adjustment options for multiple comparisons and multiple biomolecules using FDR correction.: "the February release adding p-value adjustment options for multiple comparisons and multiple biomolecules using FDR correction"
- [other] Add FDR correction option to the p-value adjustment interface, allowing users to select between no correction and FDR method.: "Add FDR correction option to the p-value adjustment interface, allowing users to select between no correction and FDR method for controlling false discovery across multiple biomolecules and"
- [other] Integrate the FDR adjustment logic into the test results processing pipeline such that adjusted p-values are computed and displayed.: "Integrate the FDR adjustment logic into the test results processing pipeline such that adjusted p-values are computed and displayed alongside raw p-values"
- [readme] Statistical analysis including ANOVA and G-test methods for biomarker determination.: "Statistical analysis.  ANOVA, G-test, and combined analyses to determine biomarkers"
- [readme] The Shiny GUI implementation makes functionality available without requiring R familiarity.: "The aim is for the bulk of the functionality of the package to be available to the user without the need for familiarity with R or the package itself"
