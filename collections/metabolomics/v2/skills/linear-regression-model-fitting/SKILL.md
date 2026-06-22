---
name: linear-regression-model-fitting
description: Use when when you have a targeted metabolomics dataset with known concentration values for calibration ('curve') and quality control ('qc') samples, peak area intensities for those samples, and you need to establish and validate a concentration-prediction model before applying it to unknown samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_0121
  tools:
  - R
  - GetFeatistics
  - lme4
  - AER
  - R base
  - Python 3
  - networkx
  - mass2chem
  - khipu
  - RawFileReader
  - rawrr
  - R base stats package (lm function)
derived_from:
- doi: 10.1515/jib-2025-0047
  title: GetFeatistics
- doi: 10.1021/acs.analchem.2c05810
  title: ''
- doi: 10.1101/2020.10.30.362533
  title: ''
- doi: 10.1021/acs.jproteome.0c00866
  title: ''
evidence_spans:
- R (version ≥ 4.3.1)
- devtools::install_github("FrigerioGianfranco/GetFeatistics", dependencies = TRUE)
- The **GetFeatistics** (GF) package provides several functions useful for the elaboration of metabolomics data
- linear models with mixed effects (random and fixed), using the _lmer_ function from the lme4 package
- TOBIT linear models, using the _tobit_ function of the AER package
- Khipu is developed as an open source Python 3 package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_getfeatistics_cq
    doi: 10.1515/jib-2025-0047
    title: GetFeatistics
  - build: coll_khipu_cq
    doi: 10.1021/acs.analchem.2c05810
    title: khipu
  - build: coll_rawrr_2_cq
    doi: 10.1101/2020.10.30.362533
    title: rawrr
  dedup_kept_from: coll_getfeatistics_cq
schema_version: 0.2.0
---

# linear-regression-model-fitting

## Summary

Fit linear regression models to targeted metabolomics calibration data to estimate compound concentrations from peak area intensities. This skill produces fitted models with slope, intercept, and R² coefficients that quantify the relationship between known standard concentrations and observed intensities.

## When to use

When you have a targeted metabolomics dataset with known concentration values for calibration ('curve') and quality control ('qc') samples, peak area intensities for those samples, and you need to establish and validate a concentration-prediction model before applying it to unknown samples.

## When NOT to use

- Input data are already normalized concentrations rather than raw peak areas.
- Sample legend lacks known concentration values for calibration samples ('curve' type).
- The relationship between intensity and concentration is non-linear or exhibits significant curvature that violates linearity assumption.

## Inputs

- Peak area intensities table (data frame: samples × compounds)
- Sample legend/metadata (data frame: sample ID, type classification, known concentration values)
- Compound legend with internal standard assignments (data frame: compound ID, internal standard match, units)

## Outputs

- Fitted linear regression models (one per compound)
- Regression coefficients (slope, intercept, R² per compound)
- Predicted concentrations for all samples (including 'unknown' type)
- Accuracy metrics (R², MAE, or equivalent for fitted curve and QC points)
- Internal standard relative standard deviation (CV%) across samples

## How to apply

Call get_targeted_elaboration with three input data frames: (1) peak area intensities table (samples in rows, compounds in columns), (2) sample legend with type classifications ('blank', 'curve', 'qc', 'unknown') and known concentration values for 'curve' and 'qc' samples, and (3) optional compound metadata table. The function fits linear models relating intensity to known concentration using the 'curve' samples, then evaluates model accuracy (R², MAE) on both 'curve' and 'qc' calibration points. Extract results_concentrations (predicted vs. actual values), results_accuracy (accuracy %), and summary_regression_models (slope, intercept, R² per compound). Three modeling strategies are available: fixed-effects linear models (lm), linear mixed-effects models with random intercepts (lmer), and TOBIT censored regression (tobit) for handling below-detection-limit values.

## Related tools

- **GetFeatistics** (R package implementing get_targeted_elaboration function for fitting regression models to targeted metabolomics data) — https://github.com/FrigerioGianfranco/GetFeatistics
- **lme4** (Provides lmer function for fitting linear models with random and fixed effects)
- **AER** (Provides tobit function for fitting censored (TOBIT) linear models)
- **R base** (Provides lm function for fitting standard fixed-effects linear models)

## Examples

```
library(GetFeatistics); result <- get_targeted_elaboration(df_example_targeted, df_example_targeted_legend, df_example_targeted_compounds_legend); summary_models <- result$summary_regression_models; predicted_conc <- result$results_concentrations
```

## Evaluation signals

- Returned regression_models list contains one fitted model object per compound with valid coefficients (slope, intercept).
- R² values in summary_regression_models are in valid range [0, 1] and reflect model fit quality on 'curve' samples.
- Predicted concentrations in results_concentrations align with actual known values for 'curve' and 'qc' samples (accuracy % > acceptable threshold).
- Internal standard CV% (cv_internal_standards) is consistent across replicates, indicating stable ionization normalization.
- Model predictions on 'unknown' samples are biochemically plausible (e.g., within expected metabolite concentration range for the biological matrix).

## Limitations

- Linear models assume a linear intensity–concentration relationship; non-linear or biphasic dose responses will produce poor fit and unreliable predictions.
- Accuracy depends critically on the number and distribution of 'curve' calibration points; sparse or unbalanced calibration ranges reduce model reliability.
- TOBIT and mixed-effects models require adequate sample replication and may be unstable with very small datasets or sparse internal standard measurements.
- No changelog is available in the package repository, limiting traceability of model fitting algorithm changes across versions.

## Evidence

- [other] get_targeted_elaboration returns a list containing: results_concentrations (calculated concentrations), results_accuracy (accuracy % for curve and QC points), cv_internal_standards (relative standard deviation of internal standard intensities), compound_legend (input metadata), summary_regression_models (slope, intercept, R² values), and regression_models (fitted linear regression models).: "get_targeted_elaboration returns a list containing: results_concentrations (calculated concentrations), results_accuracy (accuracy % for curve and QC points)...summary_regression_models (slope,"
- [other] Call the get_targeted_elaboration function with these three data frames as inputs: df_example_targeted (peak area intensities with samples in rows and compounds in columns), df_example_targeted_legend (sample classifications and known concentration values), and df_example_targeted_compounds_legend (internal standard assignments and compound metadata).: "Call the get_targeted_elaboration function with these three data frames as inputs...df_example_targeted (peak area intensities with samples in rows and compounds in columns),"
- [intro] The first should contain the intensities of peak area. Samples in rows, analysed compounds in columns. The second column should contain the following: 'blank', 'curve', 'qc', or 'unknown'. The third column should have the actual known values for 'curve' and 'qc' samples.: "The first should contain the intensities of peak area. Samples in rows, analysed compounds in columns...the second column should contain the following: "blank", "curve", "qc", or "unknown". the third"
- [intro] Linear models (with fixed effects), using the lm function; linear models with mixed effects (random and fixed), using the lmer function from the lme4 package; TOBIT linear models, using the tobit function of the AER package.: "linear models (with fixed effects), using the _lm_ function...linear models with mixed effects (random and fixed), using the _lmer_ function from the lme4 package...TOBIT linear models, using the"
- [discussion] No changelog found in the package repository.: "_No changelog found._"
- [readme] Just type: library(GetFeatistics). Then, an example of workflow is provided in the following picture. Check also the vignette guiding you through the workflow step by step.: "Just type: library(GetFeatistics). Then, an example of workflow is provided"
