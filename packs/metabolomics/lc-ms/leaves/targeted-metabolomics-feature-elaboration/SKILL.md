---
name: targeted-metabolomics-feature-elaboration
description: Use when you have targeted metabolomics data with peak area intensities
  organized in rows (samples) × columns (compounds), accompanying sample metadata
  indicating which samples are blanks, calibration curve points, or QC samples with
  known concentration values, and a compound legend assigning.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3663
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - R
  - GetFeatistics
  - lme4
  - AER
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1515/jib-2025-0047
  title: GetFeatistics
evidence_spans:
- R (version ≥ 4.3.1)
- devtools::install_github("FrigerioGianfranco/GetFeatistics", dependencies = TRUE)
- The **GetFeatistics** (GF) package provides several functions useful for the elaboration
  of metabolomics data
- linear models with mixed effects (random and fixed), using the _lmer_ function from
  the lme4 package
- TOBIT linear models, using the _tobit_ function of the AER package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_getfeatistics_cq
    doi: 10.1515/jib-2025-0047
    title: GetFeatistics
  dedup_kept_from: coll_getfeatistics_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1515/jib-2025-0047
  all_source_dois:
  - 10.1515/jib-2025-0047
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# targeted-metabolomics-feature-elaboration

## Summary

Apply the GetFeatistics get_targeted_elaboration function to convert peak area intensity tables into quantified metabolite concentrations, accuracy metrics, and regression model summaries for targeted metabolomics datasets. Use this skill when you have calibration curves, quality control samples, and internal standard assignments and need to extract fitted concentration predictions with model diagnostics.

## When to use

You have targeted metabolomics data with peak area intensities organized in rows (samples) × columns (compounds), accompanying sample metadata indicating which samples are blanks, calibration curve points, or QC samples with known concentration values, and a compound legend assigning internal standards. You need to fit linear regression models per compound, back-calculate sample concentrations, and assess model fit quality (R², accuracy %, internal standard CV).

## When NOT to use

- Input is already a feature table from untargeted analysis (XCMS/MS-Dial output); use non-targeted QC filtering and statistical workflows instead.
- No internal standards are assigned or calibration curves are absent; the function requires paired calibration samples with known concentrations.
- Sample types are not clearly labeled (blank, curve, qc, unknown); the legend table must explicitly classify each sample to enable model fitting.

## Inputs

- Peak area intensity matrix (samples × compounds) with numeric intensities
- Sample legend table (sample ID, sample type {'blank'|'curve'|'qc'|'unknown'}, known concentration values)
- Compound metadata table (compound ID, assigned internal standard, units, weighting factors)

## Outputs

- Predicted sample concentrations table (sample ID, compound ID, calculated concentration, actual known concentration)
- Accuracy metrics per compound (R², mean absolute error, root mean square error)
- Internal standard relative standard deviation (CV%) for reproducibility assessment
- Regression model summaries (slope, intercept, R², p-value per compound)
- Fitted linear regression model objects (lm class, one per compound)

## How to apply

Load three data frames into R: (1) df_example_targeted with peak area intensities (samples × compounds), (2) df_example_targeted_legend with sample type classifications ('blank', 'curve', 'qc', 'unknown') and known concentration values for curve and QC samples, and (3) df_example_targeted_compounds_legend with internal standard assignments and compound metadata. Call get_targeted_elaboration(intensity_data, sample_legend, compound_legend) and extract the returned list. Validate that the output contains: results_concentrations (predicted and actual concentration values), results_accuracy (R² and mean absolute error for each compound's regression model), cv_internal_standards (relative standard deviation of internal standard peak areas as a reproducibility check), summary_regression_models (slope, intercept, R² per compound), and regression_models (fitted lm objects). Check that all expected compounds appear in concentration and accuracy tables, and that internal standard CV values are within acceptable reproducibility thresholds (typically <20–30%).

## Related tools

- **GetFeatistics** (R package providing get_targeted_elaboration function for concentration back-calculation, regression model fitting, and accuracy assessment of targeted metabolomics data) — https://github.com/FrigerioGianfranco/GetFeatistics
- **R** (Execution environment; version ≥ 4.3.1 required)
- **lme4** (Optional: used internally by GetFeatistics for advanced linear models with mixed effects (random and fixed) if extended model fitting is needed)
- **AER** (Optional: used internally by GetFeatistics for TOBIT censored regression models when dealing with detection limits)

## Examples

```
library(GetFeatistics); result <- get_targeted_elaboration(df_example_targeted, df_example_targeted_legend, df_example_targeted_compounds_legend); concentrations <- result$results_concentrations; accuracy <- result$results_accuracy; models_summary <- result$summary_regression_models
```

## Evaluation signals

- Output list contains all six expected keys: results_concentrations, results_accuracy, cv_internal_standards, compound_legend, summary_regression_models, regression_models.
- results_concentrations table has no missing values (NA) for calibration curve and QC samples; predicted concentrations match actual known values within the model's residual standard error.
- results_accuracy R² values are > 0.95 for well-behaved compounds; compounds with R² < 0.90 warrant investigation of outliers or instrumental drift.
- cv_internal_standards is < 20–30% (method-dependent threshold); higher CV indicates instrumental variation or sample preparation issues.
- Predicted concentration ranges for 'unknown' samples are within the validated calibration curve range; extrapolated predictions beyond curve bounds are flagged or excluded.

## Limitations

- Function assumes linear relationship between peak area intensity and concentration; nonlinear calibration curves require manual model substitution.
- Requires at least 3–5 calibration points per compound for stable regression; sparse or unevenly spaced calibration data may yield poor model fit.
- Internal standard intensity outliers (e.g., from sample preparation error) propagate into CV calculations; pre-filtering outliers is recommended.
- No built-in handling of matrix effects or ion suppression; if peak area intensity is confounded by sample composition, additional normalization may be needed before calling the function.
- Output does not include confidence intervals or prediction intervals around predicted concentrations; users must extract and compute these from the returned regression_models objects if required.

## Evidence

- [full_text] get_targeted_elaboration returns a list containing: results_concentrations (calculated concentrations), results_accuracy (accuracy % for curve and QC points), cv_internal_standards (relative standard deviation of internal standard intensities), compound_legend (input metadata), summary_regression_models (slope, intercept, R² values), and regression_models (fitted linear regression models).: "get_targeted_elaboration returns a list containing: results_concentrations (calculated concentrations), results_accuracy (accuracy % for curve and QC points), cv_internal_standards (relative standard"
- [full_text] Load the three example data frames from the GetFeatistics package: df_example_targeted (peak area intensities with samples in rows and compounds in columns), df_example_targeted_legend (sample classifications and known concentration values), and df_example_targeted_compounds_legend (internal standard assignments and compound metadata).: "Load the three example data frames from the GetFeatistics package: df_example_targeted (peak area intensities with samples in rows and compounds in columns), df_example_targeted_legend (sample"
- [intro] The first should contain the intensities of peak area. Samples in rows, analysed compounds in columns: "The first should contain the intensities of peak area. Samples in rows, analysed compounds in columns"
- [intro] the second column should contain the following: "blank", "curve", "qc", or "unknown". the third column should have the actual known values for "curve" and "qc" samples: "the second column should contain the following: "blank", "curve", "qc", or "unknown". the third column should have the actual known values for "curve" and "qc" samples"
- [intro] a third table is useful especially if you work with internal standards...in the second column, the matched internal standard (or NA if there isn't an internal standard for that molecule): "a third table is useful especially if you work with internal standards...in the second column, the matched internal standard (or NA if there isn't an internal standard for that molecule)"
- [readme] devtools::install_github("FrigerioGianfranco/GetFeatistics", dependencies = TRUE): "devtools::install_github("FrigerioGianfranco/GetFeatistics", dependencies = TRUE)"
- [intro] linear models with mixed effects (random and fixed), using the _lmer_ function from the lme4 package: "linear models with mixed effects (random and fixed), using the _lmer_ function from the lme4 package"
- [intro] TOBIT linear models, using the _tobit_ function of the AER package: "TOBIT linear models, using the _tobit_ function of the AER package"
