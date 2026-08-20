---
name: multiple-comparison-correction
description: Use when after running ANOVA or G-test statistical analysis across multiple
  biomolecules in an omics dataset (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - pmartR
  - R
  - Shiny
  license_tier: open
derived_from:
- doi: 10.1021/acs.jproteome.3c00512
  title: PMart
evidence_spans:
- Shiny GUI implementation of the pmartR R package.
- Shiny GUI implementation of the pmartR R package
- the bulk of the functionality of the package to be available to the user without
  the need for familiarity with R or the package itself
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.3c00512
  all_source_dois:
  - 10.1021/acs.jproteome.3c00512
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# multiple-comparison-correction

## Summary

Apply false discovery rate (FDR) correction to p-values produced by statistical tests (ANOVA, G-test) across multiple biomolecules and comparisons to control the proportion of false positives in high-dimensional omics biomarker discovery. This prevents inflated type-I error rates inherent when conducting hundreds or thousands of simultaneous hypothesis tests.

## When to use

After running ANOVA or G-test statistical analysis across multiple biomolecules in an omics dataset (e.g. proteomics or multi-omics), when you have raw p-values from each biomolecule-comparison pair and need to account for multiple testing to determine which biomarkers meet statistical significance thresholds for reporting.

## When NOT to use

- Single hypothesis test or univariate analysis where only one p-value is computed (multiple comparison correction is unnecessary).
- Already-corrected p-values provided by another tool or preprocessing step (applying FDR twice would be redundant and incorrect).
- Exploratory or hypothesis-generation analysis where type-I error control is not a priority (e.g., initial screening without formal statistical claims).

## Inputs

- Raw p-value vector from ANOVA or G-test across multiple biomolecules
- Raw p-values from multiple comparison groups within an omics dataset
- Test results object containing p-values for each biomolecule-contrast pair

## Outputs

- FDR-adjusted p-value vector (one adjusted p-value per biomolecule-contrast)
- Updated statistical test results table with both raw and adjusted p-values
- Downloadable results file containing adjusted p-values for biomarker reporting

## How to apply

Within the pmartR-shiny statistical analysis workflow, after configuring and executing an iMd-ANOVA or G-test, expose a user-selectable p-value adjustment parameter in the Shiny UI that allows choice between 'no correction' and 'FDR method'. When FDR is selected, integrate FDR adjustment logic into the test results processing pipeline to compute adjusted p-values alongside raw p-values. The adjusted p-values are then displayed in the results table and should be used for downstream biomarker selection and visualization. Validate correctness by confirming that FDR-corrected p-values are monotonically non-decreasing with raw p-values and that the adjusted value distribution reflects the expected relationship between raw and corrected significance.

## Related tools

- **pmartR** (R package backend that implements ANOVA and G-test statistical methods; provides or integrates FDR correction logic applied to multiple comparison results) — https://github.com/pmartR/pmartR
- **Shiny** (Web framework that exposes p-value adjustment parameter selection in the UI and renders adjusted p-values in interactive result tables for biomarker determination) — https://github.com/rstudio/shiny
- **R** (Statistical computing environment in which pmartR and Shiny execute FDR correction algorithms)

## Evaluation signals

- Adjusted p-values are greater than or equal to their corresponding raw p-values (monotonicity check).
- The distribution of adjusted p-values follows expected FDR control characteristics (e.g., fewer reject null at typical α=0.05 threshold compared to unadjusted).
- Adjusted p-values can be validated against reference FDR implementations (e.g., R's p.adjust() function with method='BH') for numerical correctness.
- Biomarker lists derived from adjusted p-values show reduced false discovery compared to lists derived from raw p-values when validated against orthogonal data or ground truth.
- Result tables display both raw and adjusted p-values side-by-side for transparency and allow users to download or filter results using either metric.

## Limitations

- FDR correction assumes independence or positive correlation among test statistics; violations (e.g. strong negative correlation) may yield over-conservative results.
- The method requires specification of the correction threshold (e.g., FDR < 0.05); this threshold is not data-adaptive and must be chosen a priori or validated post-hoc.
- Multiple biomolecules with missing or filtered-out values may reduce the effective sample size for FDR calculation; the article and README do not detail handling of incomplete results.
- Release notes do not specify which FDR variant (Benjamini-Hochberg, Benjamini-Yekutieli, or other) is implemented; users should verify against the pmartR documentation or source code.

## Evidence

- [other] The pmartR-shiny implementation provides statistical analysis capabilities including ANOVA and G-test methods for biomarker determination, with the February release adding p-value adjustment options for multiple comparisons and multiple biomolecules using FDR correction.: "p-value adjustment options for multiple comparisons and multiple biomolecules using FDR correction"
- [other] Add FDR correction option to the p-value adjustment interface, allowing users to select between no correction and FDR method for controlling false discovery across multiple biomolecules and comparisons.: "Add FDR correction option to the p-value adjustment interface, allowing users to select between no correction and FDR method"
- [other] Integrate the FDR adjustment logic into the test results processing pipeline such that adjusted p-values are computed and displayed alongside raw p-values.: "adjusted p-values are computed and displayed alongside raw p-values"
- [other] Update the Shiny UI to expose the p-value adjustment option as a user-selectable parameter when configuring and running iMd-ANOVA tests.: "Update the Shiny UI to expose the p-value adjustment option as a user-selectable parameter"
- [other] Validate that FDR-corrected p-values are correctly computed and match expected distributions across multiple test scenarios.: "FDR-corrected p-values are correctly computed and match expected distributions"
- [intro] Statistical analysis.  ANOVA, G-test, and combined analyses to determine biomarkers.: "ANOVA, G-test, and combined analyses to determine biomarkers"
