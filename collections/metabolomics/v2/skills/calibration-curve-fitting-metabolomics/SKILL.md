---
name: calibration-curve-fitting-metabolomics
description: Use when your experiment contains calibration-line samples with known
  spiked concentrations and you need to convert compound/internal-standard ratios
  into absolute concentrations for study samples (those with concentration = NA).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - mzQuality
  - SummarizedExperiment
  - mzQualityDashboard
  - R (lm, weighted.lm)
  license_tier: open
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

# calibration-curve-fitting-metabolomics

## Summary

Fit a weighted linear regression model to calibration-line samples with known concentrations, then apply the model to estimate absolute concentrations for study samples from their measured compound/internal-standard ratios. This skill enables quantitative metabolomics reporting when spiked calibration standards are available.

## When to use

Your experiment contains calibration-line samples with known spiked concentrations and you need to convert compound/internal-standard ratios into absolute concentrations for study samples (those with concentration = NA). Use this when metabolomics peak areas alone are insufficient and you require traceable quantification tied to external standards.

## When NOT to use

- No calibration samples with known concentrations are available in the experiment.
- The compound/internal-standard ratio shows no linear relationship with concentration (visual inspection or R² < 0.7 typically indicates poor model fit; fitting should be aborted or alternative approaches explored).
- Study samples have concentration values already assigned; fitting a new calibration curve will overwrite them.

## Inputs

- SummarizedExperiment object with assay data (peak areas/intensities), rowData (compound metadata), and colData (sample metadata including concentration column)
- Tab-delimited or Sciex OS text export with mandatory columns: compound, aliquot, assay type, internal standard assignment, and concentration (numeric for calibration samples, NA for study samples)

## Outputs

- SummarizedExperiment object with new assay 'concentration' (predicted absolute concentrations for all samples)
- SummarizedExperiment rowData enriched with R² value per compound quantifying model goodness-of-fit
- Concentration plot (scatter plot with fitted line and confidence interval)
- Tab-delimited export and Excel file (via createReports) containing colData with predicted concentrations

## How to apply

First, filter the SummarizedExperiment to retain only calibration samples by selecting rows where the concentration column contains known values (not NA). Calculate the compound/internal-standard ratio for each calibration sample by dividing the compound peak area by the internal-standard peak area. Fit a weighted linear regression model using R's lm() or weighted.lm() function, with ratio as the predictor and concentration as the response variable; weighting accounts for heteroscedasticity in the calibration data. Evaluate model fit by inspecting the R² value (higher is more reliable). Apply the fitted model to all study samples by predicting their concentrations from their measured ratios. Generate a concentration plot as a scatter plot showing calibration points, the fitted line with confidence bounds, and the projected sample concentrations, ideally within the calibration range. Samples projecting outside the calibration range should be flagged as extrapolations.

## Related tools

- **mzQuality** (Core R package that implements calibration-curve fitting via the doAnalysis wrapper function; integrates ratio calculation, model fitting, and concentration prediction into a single workflow for SummarizedExperiment objects.) — https://github.com/hankemeierlab/mzQuality
- **SummarizedExperiment** (Bioconductor container object that stores compound peak areas, sample metadata (including known concentrations), and predicted concentration assays; mzQuality internally uses this format for all calculations.) — https://bioconductor.org/packages/release/bioc/html/SummarizedExperiment.html
- **mzQualityDashboard** (Interactive Shiny application wrapping mzQuality for users without R programming experience; provides point-and-click access to calibration-curve fitting and concentration-plot visualization.) — https://github.com/hankemeierlab/mzQualityDashboard
- **R (lm, weighted.lm)** (Base and stats functions for fitting ordinary or weighted linear regression models; used to regress concentration on compound/internal-standard ratio.)

## Examples

```
exp <- doAnalysis(exp = exp); # generates concentration assay and R² in rowData if concentration column supplied in colData
```

## Evaluation signals

- R² value per compound is ≥ 0.7 (or higher threshold if specified) and reported in rowData; values < 0.7 indicate poor model fit.
- Calibration points cluster tightly around the fitted line; large vertical residuals suggest outlier calibration samples or measurement error.
- Study sample concentrations fall within the range of calibration concentrations (no extrapolation beyond calibration bounds); samples outside this range should be explicitly flagged.
- Predicted concentrations are positive and biologically plausible; negative or implausibly high values indicate model failure or data quality issues.
- Comparison of predicted concentrations across replicate study samples shows low coefficient of variation (typically < 20%), confirming reproducibility.

## Limitations

- Assumes a linear relationship between ratio and concentration; non-linear calibration curves are not addressed by this workflow.
- Requires calibration samples to span the full dynamic range of study samples; narrow calibration ranges lead to unreliable extrapolation.
- Outlier calibration samples (e.g., mis-injected standards or degraded compounds) can distort the fitted line; robust regression or manual outlier removal may be necessary.
- Internal standard selection and peak-area integration quality directly impact ratio calculation and downstream concentration estimates; poor internal standards compromise the entire workflow.
- The method assumes no batch effects or systematic drift between calibration and study sample acquisition; batch correction should be applied separately if needed.

## Evidence

- [other] Filter the experiment object to retain only calibration samples with known concentrations using the concentration column: "Filter the experiment object to retain only calibration samples with known concentrations using the concentration column."
- [other] Calculate the compound/internal-standard ratio for each calibration sample; fit a weighted linear regression model with ratio as predictor and concentration as response: "Calculate the compound/internal standard ratio for each calibration sample. 3. Fit a weighted linear regression model with ratio as predictor and concentration as response using R's lm or weighted-lm"
- [other] Apply the fitted model to all study samples to predict their absolute concentrations from their measured ratios: "Apply the fitted model to all study samples (those with concentration = NA) to predict their absolute concentrations from their measured ratios."
- [other] The Concentration Plot is a scatter plot with a linear model added, based on the calculated ratio and known concentration: "The Concentration Plot is a scatter plot with a linear model added, based on the calculated `ratio` and known `concentration`."
- [intro] by supplying calibration line samples and known concentrations for spiked compounds, mzQuality is able to calculate absolute concentrations: "by supplying calibration line samples and known concentrations for spiked compounds, mzQuality is able to calculate absolute concentrations"
- [readme] If known concentrations for calibration lines have been supplied, the doAnalysis function will also calculate the concentrations and the corresponding R2 value: "If known concentrations for calibration lines have been supplied, the `doAnalysis` function will also calculate the concentrations and the corresponding R2 value given the provided calibration lines."
