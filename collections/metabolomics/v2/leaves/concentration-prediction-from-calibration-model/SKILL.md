---
name: concentration-prediction-from-calibration-model
description: Use when you have (1) a set of calibration samples with known spiked
  concentrations of target compounds, (2) measured compound/internal-standard ratios
  for both calibration and study samples, and (3) need to convert ratios to absolute
  concentrations for reporting.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3407
  tools:
  - R
  - mzQuality
  - SummarizedExperiment
  - R (base lm/weighted.lm)
  - mzQualityDashboard
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/jasms.5c00073
  title: mzquality
evidence_spans:
- library(mzQuality)
- knitr::rmarkdown, library(mzQuality)
- mzQuality requires a specific format for the input data.
- mzQuality requires a specific format for the input data
- The `buildExperiment` function will then take the data and create an experiment
  object that can be used for analysis.
- Internally, mzQuality uses Bioconductors' *SummarizedExperiment* object to store
  the data
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzquality_cq
    doi: 10.1021/jasms.5c00073
    title: mzquality
  dedup_kept_from: coll_mzquality_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.5c00073
  all_source_dois:
  - 10.1021/jasms.5c00073
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# concentration-prediction-from-calibration-model

## Summary

Fit a weighted linear regression model to calibration-line samples with known concentrations, then apply the fitted model to predict absolute concentrations for study samples from their measured compound/internal-standard ratios. This enables quantification of metabolites in untargeted metabolomics when authentic standards are available.

## When to use

Use this skill when you have (1) a set of calibration samples with known spiked concentrations of target compounds, (2) measured compound/internal-standard ratios for both calibration and study samples, and (3) need to convert ratios to absolute concentrations for reporting. This is typical after batch correction and internal standard normalization in LC-MS/MS metabolomics workflows.

## When NOT to use

- Calibration samples show non-linear relationship between ratio and concentration (fit polynomial or non-linear model instead)
- Concentration column is missing entirely or calibration samples are not flagged in metadata
- Study samples have measured ratios far outside the calibration range (extrapolation beyond empirical range is unreliable)

## Inputs

- SummarizedExperiment object with assay containing compound/internal-standard ratios
- colData column 'concentration' with known values for calibration samples (NA for study samples)
- rowData and colData metadata identifying sample types (calibration vs. study)

## Outputs

- SummarizedExperiment with added assay column containing predicted absolute concentrations for study samples
- Concentration plot (scatter plot with fitted linear model line, calibration points, and sample projections)
- Linear model object (slope, intercept, R² value, residuals)

## How to apply

Filter the SummarizedExperiment to retain only calibration samples (where concentration column is not NA). Calculate the compound/internal-standard ratio for each calibration sample. Fit a weighted linear regression model with ratio as predictor and known concentration as response using R's lm() or weighted-lm function (weights typically inversely proportional to variance). Visually inspect the calibration line for linearity and outliers. Apply the fitted model coefficients to all study samples (where concentration = NA) to predict their absolute concentrations from measured ratios. Generate a concentration plot overlay showing calibration points, the fitted line, and projected sample predictions; ideally all predictions fall within or near the calibration range.

## Related tools

- **mzQuality** (R package that implements calibration model fitting and concentration prediction via doAnalysis() and concentrationPlot() functions on SummarizedExperiment objects) — https://github.com/hankemeierlab/mzQuality
- **SummarizedExperiment** (Bioconductor container class storing assays (ratios), colData (sample metadata including concentrations), and rowData (compound metadata))
- **R (base lm/weighted.lm)** (Statistical function for fitting linear regression; mzQuality wraps this for weighted fitting by concentration)
- **mzQualityDashboard** (Interactive Shiny application frontend for visualizing calibration plots and inspecting concentration predictions without scripting) — https://github.com/hankemeierlab/mzQualityDashboard

## Examples

```
exp <- doAnalysis(exp = exp); concentrationPlot(exp, assay = "concentration")
```

## Evaluation signals

- R² value of the fitted model is ≥ 0.95, indicating strong linear fit of calibration samples
- Study sample predictions fall within or close to the concentration range spanned by calibration samples (no large extrapolations)
- Concentration plot visually shows calibration points, fitted line, and study sample projections all on the same axis without obvious outliers or gaps
- No NA or inf values in the output concentration assay for study samples (model was successfully applied)
- Residual plot of calibration samples shows random scatter around zero with no systematic bias

## Limitations

- Assumes a linear relationship between compound/IS ratio and absolute concentration; non-linear response (saturation, suppression) will reduce accuracy
- Predictions for study samples with ratios outside calibration range (extrapolation) are unreliable and should be flagged
- Requires sufficient and well-distributed calibration points; sparse or clustered calibration may yield poor model fit
- Weighted regression requires assumption about error variance; unequal weighting can bias estimates if variance model is misspecified
- Internal standard must be stable and not co-elute; if IS area varies unexpectedly, ratio and concentration estimates will be biased

## Evidence

- [other] The Concentration Plot is a scatter plot with a linear model added, based on the calculated `ratio` and known `concentration`. The measurements of the other samples are projected on this line, ideally within the range of the calibration line.: "The Concentration Plot is a scatter plot with a linear model added, based on the calculated `ratio` and known `concentration`. The measurements of the other samples are projected on this line,"
- [other] Filter the experiment object to retain only calibration samples with known concentrations using the concentration column. Calculate the compound/internal-standard ratio for each calibration sample. Fit a weighted linear regression model with ratio as predictor and concentration as response using R's lm or weighted-lm function.: "Filter the experiment object to retain only calibration samples with known concentrations using the concentration column. Calculate the compound/internal-standard ratio for each calibration sample."
- [intro] by supplying calibration line samples and known concentrations for spiked compounds, mzQuality is able to calculate absolute concentrations: "by supplying calibration line samples and known concentrations for spiked compounds, mzQuality is able to calculate absolute concentrations"
- [readme] If known concentrations for calibration lines have been supplied, the `doAnalysis` function will also calculate the concentrations and the corresponding R2 value given the provided calibration lines.: "If known concentrations for calibration lines have been supplied, the `doAnalysis` function will also calculate the concentrations and the corresponding R2 value given the provided calibration lines."
- [other] Apply the fitted model to all study samples (those with concentration = NA) to predict their absolute concentrations from their measured ratios.: "Apply the fitted model to all study samples (those with concentration = NA) to predict their absolute concentrations from their measured ratios."
