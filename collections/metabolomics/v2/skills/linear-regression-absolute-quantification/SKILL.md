---
name: linear-regression-absolute-quantification
description: Use when you have a set of calibration samples (spiked compounds) with known concentrations, measured compound and internal-standard peak areas, and you need to convert compound/internal-standard ratios from study samples into absolute concentrations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3662
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - mzQuality
  - SummarizedExperiment
  - R lm/weighted.lm
  - mzQualityDashboard
derived_from:
- doi: 10.1021/jasms.5c00073
  title: mzquality
evidence_spans:
- library(mzQuality)
- knitr::rmarkdown, library(mzQuality)
- mzQuality requires a specific format for the input data.
- mzQuality requires a specific format for the input data
- The `buildExperiment` function will then take the data and create an experiment object that can be used for analysis.
- Internally, mzQuality uses Bioconductors' *SummarizedExperiment* object to store the data
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
---

# linear-regression-absolute-quantification

## Summary

Fit a weighted linear regression model to calibration-line samples with known concentrations, then use the fitted model to predict absolute concentrations for study samples from their measured compound/internal-standard ratios. This enables absolute quantification of metabolites in untargeted metabolomics workflows.

## When to use

Apply this skill when you have a set of calibration samples (spiked compounds) with known concentrations, measured compound and internal-standard peak areas, and you need to convert compound/internal-standard ratios from study samples into absolute concentrations. The calibration samples must span a relevant concentration range that brackets the expected study sample concentrations.

## When NOT to use

- Study samples lack corresponding internal-standard measurements or peak areas are zero/missing.
- Calibration line contains fewer than 3 reliable points or spans an insufficient concentration range for the unknowns.
- Study sample ratios fall far outside the range of calibration-line ratios (extrapolation beyond model validity).

## Inputs

- SummarizedExperiment object with compound peak areas, internal-standard peak areas, and a concentration column (with values for calibration samples, NA for study samples)
- Tab-delimited text file with calibration sample metadata including concentration values
- Calculated compound/internal-standard ratios for all samples

## Outputs

- Predicted absolute concentrations for all study samples
- Fitted linear regression model (coefficients, R² value)
- Concentration plot (scatter plot showing calibration points, fitted line, and predicted sample concentrations)
- Updated SummarizedExperiment object with concentration predictions and R² in assay and rowData slots

## How to apply

First, filter the experiment object to retain only calibration samples (those with non-missing concentration values in the concentration column). Calculate the compound/internal-standard ratio for each calibration sample from their measured peak areas. Fit a weighted linear regression model with the ratio as the predictor variable and the known concentration as the response variable using R's `lm()` or `weighted.lm()` function (weighting by measurement precision or area values reduces influence of outliers). Apply the fitted model coefficients to all study samples (those with concentration = NA) to generate predicted concentrations from their measured ratios. The workflow should also compute and report the R² value of the calibration line as a quality metric for the fitted model. Ideally, predicted study sample concentrations should fall within or near the range spanned by the calibration line; predictions far outside this range indicate extrapolation and reduced reliability.

## Related tools

- **mzQuality** (R package that implements the complete workflow: reads experiment data into SummarizedExperiment objects, calculates compound/internal-standard ratios, fits weighted linear models to calibration samples, predicts concentrations for study samples, and generates concentration plots) — https://github.com/hankemeierlab/mzQuality
- **SummarizedExperiment** (Bioconductor container object that stores assays (peak areas, ratios, concentrations), rowData (compound metadata), and colData (sample metadata including concentration labels and type)) — https://bioconductor.org/packages/release/bioc/html/SummarizedExperiment.html
- **R lm/weighted.lm** (Base R and stats functions used to fit the linear regression model with optional weights)
- **mzQualityDashboard** (Shiny application frontend that provides interactive visualization and parameter control for the concentration plot and model fitting workflow without requiring R programming) — https://github.com/hankemeierlab/mzQualityDashboard

## Examples

```
exp <- doAnalysis(exp = exp); concentrationPlot(exp)
```

## Evaluation signals

- R² value of the fitted calibration line should be ≥ 0.90 (or user-defined threshold) to indicate a strong linear relationship.
- Residuals of calibration samples should be approximately normally distributed and homoscedastic (constant variance) when plotted against fitted values.
- Predicted concentrations for study samples should fall within or near the concentration range of the calibration line; predictions requiring large extrapolation warrant flagging.
- Concentration plot should show calibration points scattered around the fitted line with study sample predictions projected onto or near the line.
- The fitted model coefficients (slope and intercept) should be positive (or match expected stoichiometry) and remain stable across repeated analyses of the same calibration samples.

## Limitations

- Requires calibration samples with accurately known concentrations; mislabeled or contaminated calibration samples will produce invalid models.
- Linear regression assumes a linear relationship between ratio and concentration; non-linear or saturation effects at high concentrations may violate this assumption.
- Predictions outside the calibration concentration range are unreliable and should not be reported without explicit uncertainty intervals.
- The method depends on the stability and accuracy of internal-standard peak area measurements; poor IS performance compromises ratio-based quantification.
- Weighted regression requires careful choice of weights; inappropriate weighting can introduce bias or over-fit noise.

## Evidence

- [other] Calibration line filtering and ratio calculation: "Filter the experiment object to retain only calibration samples with known concentrations using the concentration column. Calculate the compound/internal-standard ratio for each calibration sample."
- [other] Linear regression fitting step: "Fit a weighted linear regression model with ratio as predictor and concentration as response using R's lm or weighted-lm function."
- [other] Prediction and visualization: "Apply the fitted model to all study samples (those with concentration = NA) to predict their absolute concentrations from their measured ratios. Generate a concentration plot showing calibration"
- [intro] mzQuality absolute concentration calculation capability: "by supplying calibration line samples and known concentrations for spiked compounds, mzQuality is able to calculate absolute concentrations"
- [intro] Concentration plot interpretation: "The Concentration Plot is a scatter plot with a linear model added, based on the calculated `ratio` and known `concentration`. The measurements of the other samples are projected on this line,"
- [readme] doAnalysis workflow includes concentration calculation: "If known concentrations for calibration lines have been supplied, the `doAnalysis` function will also calculate the concentrations and the corresponding R2 value given the provided calibration lines."
