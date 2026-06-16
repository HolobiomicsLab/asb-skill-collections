# Evaluation Strategy

## Direct Checks

- file_exists: verify that the IBD (External) dataset files or metadata are present in the MiMeNet repository (YDaiLab/MiMeNet) or accessible via the cited cohort accessions (LifeLines-DEEP or equivalent)
- file_format_is: verify that prediction outputs (correlation scores or result table) from external validation are in a standard tabular format (CSV, TSV, or Excel)
- value_in_range: verify that reported Spearman correlation coefficients for external validation predictions fall within the valid range [-1.0, 1.0]
- output_matches_reference: retrieve the reported external validation correlation metrics from Figure 2 or Table 2 (or cited supplementary figure) and confirm that reproduced values match the published reference values within rounding tolerance (robust to minor floating-point precision)
- script_runs: verify that the MiMeNet codebase (from https://github.com/YDaiLab/MiMeNet) contains a reproducible script or workflow for training on IBD (PRISM) full dataset and evaluating on IBD (External) cohorts without errors

## Expert Review

- Validate that the model trained on IBD (PRISM) full dataset (121 IBD samples) does not leak information from the held-out IBD (External) samples (43 IBD + 20 control subjects); confirm data provenance and exclusivity of training/test splits
- Assess whether the reported external validation correlation coefficients are biologically plausible and consistent with the cross-validation results reported in the abstract and main text
- Review the exact composition and preprocessing steps applied to the two external cohorts (LifeLines-DEEP and the second cohort) to confirm they match the methodology described in the Methods section
- Evaluate whether the choice of Spearman correlation as the evaluation metric is appropriate for the reported metabolite abundance distributions and whether any alternative metrics should be reported for comparison
