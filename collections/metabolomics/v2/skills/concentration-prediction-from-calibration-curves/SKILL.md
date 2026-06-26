---
name: concentration-prediction-from-calibration-curves
description: Use when when you have a targeted metabolomics peak area intensity table
  with samples classified into calibration curve standards (with known concentration
  values), quality control (QC) samples, blanks, and unknowns, and you need to convert
  raw peak intensities into predicted concentrations for.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3172
  tools:
  - R
  - GetFeatistics
  - lme4
  - AER
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

# concentration-prediction-from-calibration-curves

## Summary

Predict unknown sample concentrations by fitting linear regression models to calibration curve samples (with known concentrations) and applying the fitted models to unknown samples. This skill quantifies targeted metabolomics features using peak area intensities and internal standard normalization.

## When to use

When you have a targeted metabolomics peak area intensity table with samples classified into calibration curve standards (with known concentration values), quality control (QC) samples, blanks, and unknowns, and you need to convert raw peak intensities into predicted concentrations for unknown samples using the calibration curve relationship.

## When NOT to use

- Input data lacks calibration curve samples with known concentration values (cannot fit a model without standards).
- Peak intensities are already normalized and concentrations are already predicted (workflow already completed).
- Sample classifications are missing or cannot distinguish 'curve' (calibration) from 'unknown' samples.

## Inputs

- df_example_targeted (peak area intensities table: samples × compounds)
- df_example_targeted_legend (sample classifications and known concentration values)
- df_example_targeted_compounds_legend (internal standard assignments and metadata)

## Outputs

- results_concentrations (predicted concentrations for unknown samples and actual values for standards)
- results_accuracy (accuracy metrics: R², MAE for curve and QC points)
- summary_regression_models (slope, intercept, R² for each compound)
- regression_models (fitted linear regression model objects per compound)
- cv_internal_standards (relative standard deviation of internal standard intensities)

## How to apply

Load three data frames: (1) peak area intensities with samples in rows and compounds in columns, (2) sample legend with type classifications ('blank', 'curve', 'qc', 'unknown') and known concentration values for 'curve' and 'qc' samples, and (3) optional compound metadata specifying internal standard assignments. Call get_targeted_elaboration() with these three inputs. The function fits linear regression models (with or without mixed effects and optional TOBIT censored regression) separately for each compound using 'curve' samples, then applies the fitted slope and intercept to predict concentrations for 'unknown' samples. Calculate accuracy metrics (R², MAE) on curve-fitted points and QC samples to validate model performance. Extract the results_concentrations table (predicted and actual values), accuracy scores, and regression model summaries (coefficients, statistics) from the returned list object.

## Related tools

- **GetFeatistics** (Provides get_targeted_elaboration() function to fit regression models and predict concentrations from calibration curves) — https://github.com/FrigerioGianfranco/GetFeatistics
- **lme4** (Supplies lmer() for fitting linear models with mixed effects (random intercept) as alternative to fixed-effect regression)
- **AER** (Provides tobit() function for TOBIT censored regression models when dealing with detection limits)
- **R** (Base statistical environment (version ≥ 4.3.1) for executing the entire workflow)

## Examples

```
library(GetFeatistics); result <- get_targeted_elaboration(df_example_targeted, df_example_targeted_legend, df_example_targeted_compounds_legend); concentrations <- result$results_concentrations; accuracy <- result$results_accuracy
```

## Evaluation signals

- Regression model R² values for calibration curve samples are >0.95 (indicates good fit of the calibration relationship)
- Predicted concentrations for QC samples fall within acceptable accuracy range (e.g., mean absolute error <10% of known QC values)
- Coefficient of variation (CV) of internal standard intensities is <20%, indicating stable normalization
- All expected elements present in returned list: concentrations table, accuracy scores, and model summaries with coefficients and statistics
- Predicted unknown sample concentrations fall within biologically plausible ranges and are reasonable relative to the concentration range spanned by the calibration curve

## Limitations

- Requires sufficient calibration curve points (typically ≥3 points) to reliably estimate linear regression parameters; sparse or poorly distributed standards degrade prediction accuracy.
- Assumes linear relationship between peak intensity and concentration; non-linear curves require alternative models (polynomial regression, spline fitting).
- Performance depends on internal standard availability and stability; if internal standards are absent or show high CV (>20%), predicted concentrations may be unreliable.
- TOBIT regression for censored data (below detection limit) requires proper specification of detection threshold; misspecification can bias concentration estimates.
- Mixed-effects models (lmer) assume random intercept structure; complex study designs with multiple random effects may require manual model specification.

## Evidence

- [other] get_targeted_elaboration returns a list containing: results_concentrations (calculated concentrations), results_accuracy (accuracy % for curve and QC points), cv_internal_standards (relative standard deviation of internal standard intensities), compound_legend (input metadata), summary_regression_models (slope, intercept, R² values), and regression_models (fitted linear regression models).: "get_targeted_elaboration returns a list containing: results_concentrations (calculated concentrations), results_accuracy (accuracy % for curve and QC points), cv_internal_standards (relative standard"
- [other] Load the three example data frames from the GetFeatistics package: df_example_targeted (peak area intensities with samples in rows and compounds in columns), df_example_targeted_legend (sample classifications and known concentration values), and df_example_targeted_compounds_legend (internal standard assignments and compound metadata).: "Load the three example data frames from the GetFeatistics package: df_example_targeted (peak area intensities with samples in rows and compounds in columns), df_example_targeted_legend (sample"
- [intro] The first should contain the intensities of peak area. Samples in rows, analysed compounds in columns: "The first should contain the intensities of peak area. Samples in rows, analysed compounds in columns"
- [intro] the second column should contain the following: "blank", "curve", "qc", or "unknown". the third column should have the actual known values for "curve" and "qc" samples: "the second column should contain the following: "blank", "curve", "qc", or "unknown". the third column should have the actual known values for "curve" and "qc" samples"
- [intro] linear models (with fixed effects), using the _lm_ function...linear models with mixed effects (random and fixed), using the _lmer_ function...TOBIT linear models, using the _tobit_ function: "linear models (with fixed effects), using the _lm_ function...linear models with mixed effects (random and fixed), using the _lmer_ function...TOBIT linear models, using the _tobit_ function"
- [intro] a third table is useful especially if you work with internal standards...in the second column, the matched internal standard (or NA if there isn't an internal standard for that molecule): "a third table is useful especially if you work with internal standards...in the second column, the matched internal standard (or NA if there isn't an internal standard)"
