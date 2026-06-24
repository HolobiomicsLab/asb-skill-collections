---
name: statistical-test-configuration
description: Use when after data transformation, normalization, and filtering are
  complete, and you have assigned experimental groups (main effects, covariates, pairing
  structure).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0085
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

# statistical-test-configuration

## Summary

Configure and execute statistical tests (ANOVA, G-test) on multi-omics data within the pmartR-Shiny framework, with optional p-value adjustment for multiple comparisons using FDR correction. This skill enables users to specify test parameters, select adjustment methods, and produce both raw and adjusted p-values for biomarker discovery across multiple biomolecules.

## When to use

After data transformation, normalization, and filtering are complete, and you have assigned experimental groups (main effects, covariates, pairing structure). Use this skill when you need to test for statistical differences across biomolecules (proteins, peptides, metabolites) between treatment groups and require FDR-corrected p-values to control false discovery rate across the set of tested biomolecules.

## When NOT to use

- Data have not been normalized and filtered—apply normalization and filtering first to ensure valid test assumptions.
- No clear experimental group structure exists or group assignments have not been configured in the application.
- Input is already a statistical results table with pre-computed p-values (this skill is for generating, not re-processing, test results).
- Testing requires methods beyond ANOVA and G-test (e.g., non-parametric rank-based tests, survival analysis).

## Inputs

- normalized omics expression matrix (log2-transformed, samples × biomolecules)
- sample metadata with group assignments (main effects, covariates, pair identifiers)
- biomolecule metadata (gene/protein/metabolite identifiers, annotations)
- group configuration object specifying test design and pairing structure

## Outputs

- statistical test results table with raw p-values per biomolecule
- FDR-adjusted p-values per biomolecule
- test statistics (F-statistic for ANOVA, G-statistic for G-test) per biomolecule
- visualization-ready data frame for plotting (e.g., volcano plots, p-value distributions)

## How to apply

Within the pmartR-Shiny statistical analysis module, configure the test by: (1) selecting the statistical method (ANOVA for continuous normally-distributed data or G-test for count data); (2) specifying the group variable(s) and pairing structure from the group assignment metadata; (3) selecting p-value adjustment method—choose 'FDR' to apply false discovery rate correction across all biomolecules, or 'none' for raw p-values only; (4) execute the test pipeline, which computes test statistics and p-values for each biomolecule independently, then applies the selected adjustment method to control the false discovery rate; (5) validate that adjusted p-values are monotonically non-decreasing (adjusted p-value ≥ raw p-value) and fall within [0, 1]. The FDR-corrected values enable direct filtering of significant biomarkers at a chosen false discovery threshold (e.g., adjusted p < 0.05).

## Related tools

- **pmartR** (R package providing the underlying statistical test implementations (ANOVA, G-test) and p-value adjustment logic for multiple comparison correction) — https://github.com/pmartR/pmartR
- **Shiny** (Web framework exposing pmartR statistical functionality as interactive UI for test configuration, parameter selection, and result visualization without requiring R expertise) — https://shiny.posit.co
- **R** (Host language for all statistical computation, FDR correction algorithms, and p-value adjustment calculations)

## Evaluation signals

- Adjusted p-values are greater than or equal to their corresponding raw p-values (monotonicity check: adjusted_p ≥ raw_p for all biomolecules).
- All p-values (raw and adjusted) fall within the valid range [0, 1].
- FDR-adjusted p-values follow the expected distribution when compared to the raw p-value distribution (adjusted values shift rightward, reducing false positives).
- Test statistics and degrees of freedom are consistent with the specified test design (number of groups, pairing structure, sample size per group).
- Results are reproducible: re-running the test with identical configuration and data produces identical p-values and adjusted p-values.

## Limitations

- ANOVA assumes normally-distributed residuals and homogeneity of variance; severe violations may produce invalid p-values. Consider diagnostic plots before interpretation.
- FDR correction controls false discovery rate but may be conservative with small sample sizes or very sparse biomolecule sets; consider the trade-off between sensitivity and specificity.
- The skill does not implement post-hoc pairwise comparisons; only omnibus test p-values (one per biomolecule) are produced. Multi-group studies require manual follow-up testing.
- Missing values must be handled by prior filtering or imputation; the test configuration does not impute missing data.
- The Shiny interface currently supports only ANOVA and G-test; other statistical methods (Kruskal–Wallis, survival, logistic regression) require direct pmartR package usage or custom script development.

## Evidence

- [intro] Statistical analysis. ANOVA, G-test, and combined analyses to determine biomarkers.: "Statistical analysis.  ANOVA, G-test, and combined analyses to determine biomarkers."
- [other] FDR correction option added in February release for multiple comparisons and biomolecules.: "February release adding p-value adjustment options for multiple comparisons and multiple biomolecules using FDR correction."
- [other] Adjusted p-values are computed and displayed alongside raw p-values in the test results.: "Integrate the FDR adjustment logic into the test results processing pipeline such that adjusted p-values are computed and displayed alongside raw p-values."
- [other] FDR-corrected p-values must be validated for correct computation and expected distributions.: "Validate that FDR-corrected p-values are correctly computed and match expected distributions across multiple test scenarios."
- [other] Shiny UI exposes p-value adjustment as a user-selectable parameter for test configuration.: "Update the Shiny UI to expose the p-value adjustment option as a user-selectable parameter when configuring and running iMd-ANOVA tests."
- [readme] Group assignment step specifies main effects, covariates, and pairing structure before statistical analysis.: "Group assignment (main effects, covariates, pairing structure)"
