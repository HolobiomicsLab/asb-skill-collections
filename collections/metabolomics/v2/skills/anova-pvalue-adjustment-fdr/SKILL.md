---
name: anova-pvalue-adjustment-fdr
description: Use when you have completed ANOVA or G-test statistical testing across
  multiple biomolecules in an omics dataset and need to account for multiple testing.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - pmartR
  - R
  - Shiny
  - PMart_ShinyApp
  license_tier: open
  provenance_tier: literature
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

# Apply False Discovery Rate (FDR) correction to ANOVA p-values for multiple comparisons

## Summary

FDR correction adjusts raw p-values from ANOVA tests to control the expected proportion of false discoveries when testing multiple biomolecules and comparisons simultaneously. This skill is essential in omics workflows where hundreds or thousands of statistical tests are performed in parallel, preventing inflation of Type I error rates across the entire analysis.

## When to use

Use this skill when you have completed ANOVA or G-test statistical testing across multiple biomolecules in an omics dataset and need to account for multiple testing. The skill is triggered specifically when the analysis involves testing many biomolecules (proteins, metabolites, transcripts, etc.) simultaneously and you want to control false discovery rate rather than family-wise error rate.

## When NOT to use

- When testing only a single biomolecule or performing a single comparison—multiple testing correction is unnecessary and may reduce power without benefit.
- When the analysis goal requires control of family-wise error rate (e.g., hypothesis-driven studies with a small, predefined set of comparisons) rather than false discovery rate—use Bonferroni or Holm correction instead.
- When p-values have already been corrected by an upstream analysis step or when using a combined analytical approach that internally accounts for multiplicity.

## Inputs

- Raw ANOVA or G-test p-values (one per biomolecule)
- Test results table with p-value column from iMd-ANOVA statistical analysis
- Number of biomolecules tested (or implicit from p-value vector length)
- FDR correction method selection parameter (e.g., 'none' or 'FDR')

## Outputs

- FDR-adjusted p-value column appended to test results table
- Results table with both raw and adjusted p-values side-by-side
- Biomarker list filtered by adjusted p-value threshold
- Visualization of raw vs. adjusted p-value distributions

## How to apply

After running ANOVA tests on each biomolecule in the pmartR-shiny interface, select the FDR correction option from the p-value adjustment menu in the statistical analysis configuration panel. The workflow computes adjusted p-values by applying FDR correction logic to the raw p-value distribution across all tested biomolecules and comparisons. This involves ranking p-values and applying the Benjamini-Hochberg procedure (or equivalent) to generate adjusted p-values that reflect the proportion of false discoveries. Display both raw and FDR-corrected p-values in the results table, allowing users to interpret significance at conventional thresholds (e.g., adjusted p < 0.05) while maintaining visibility of the original test statistics. Validate that adjusted p-values are monotonically increasing or equal when ordered by rank and that the total number of significant discoveries at a given FDR threshold matches expectations from the correction procedure.

## Related tools

- **pmartR** (R package implementing ANOVA, G-test, and combined statistical analyses with FDR adjustment options for biomarker determination in omics data) — https://github.com/pmartR/pmartR
- **Shiny** (Interactive web framework providing UI for selecting and executing FDR p-value adjustment options without requiring R proficiency) — https://github.com/rstudio/shiny
- **PMart_ShinyApp** (Shiny GUI wrapper around pmartR exposing FDR correction interface in statistical analysis workflow) — https://github.com/pmartR/PMart_ShinyApp

## Evaluation signals

- Adjusted p-values are monotonically non-decreasing when sorted by rank (or equal when tied), confirming correct FDR procedure application.
- Adjusted p-values are always ≥ corresponding raw p-values for each biomolecule (FDR correction never reduces p-values below the original test statistic).
- The proportion of discoveries at a given adjusted p-value threshold matches the expected FDR level (e.g., at adjusted p < 0.05, roughly ≤5% of discoveries are expected to be false).
- Both raw and adjusted p-value columns are present in output results table with matching row counts and biomolecule identifiers.
- Biomarker lists generated from adjusted p-values show expected reduction in the number of significant hits compared to raw p-values, reflecting multiple testing penalty.

## Limitations

- FDR correction assumes independence or positive correlation among tests; may be overly conservative when tests are negatively correlated, reducing power to detect true positives.
- The article provides no explicit detail on which specific FDR method is implemented (e.g., Benjamini-Hochberg, Benjamini-Yekutieli, or other variants), so practitioners should verify the specific procedure in the pmartR documentation.
- Release notes indicate FDR was added in February release but do not provide benchmark comparisons showing how FDR correction affects biomarker recovery or validation rates on real datasets.
- The skill applies to ANOVA and G-test results; applicability to combined or alternative statistical tests in the pmartR ecosystem is not explicitly discussed.

## Evidence

- [other] The pmartR-shiny implementation provides statistical analysis capabilities including ANOVA and G-test methods for biomarker determination, with the February release adding p-value adjustment options for multiple comparisons and multiple biomolecules using FDR correction.: "with the February release adding p-value adjustment options for multiple comparisons and multiple biomolecules using FDR correction"
- [other] What p-value adjustment methods are available in the iMd-ANOVA statistical analysis workflow to account for multiple comparisons and multiple biomolecules?: "What p-value adjustment methods are available in the iMd-ANOVA statistical analysis workflow to account for multiple comparisons and multiple biomolecules?"
- [other] Add FDR correction option to the p-value adjustment interface, allowing users to select between no correction and FDR method for controlling false discovery across multiple biomolecules and comparisons.: "Add FDR correction option to the p-value adjustment interface, allowing users to select between no correction and FDR method for controlling false discovery across multiple biomolecules and"
- [other] Integrate the FDR adjustment logic into the test results processing pipeline such that adjusted p-values are computed and displayed alongside raw p-values.: "Integrate the FDR adjustment logic into the test results processing pipeline such that adjusted p-values are computed and displayed alongside raw p-values."
- [readme] Statistical analysis.  ANOVA, G-test, and combined analyses to determine biomarkers.: "Statistical analysis.  ANOVA, G-test, and combined analyses to determine biomarkers."
