---
name: linear-regression-fitting-for-chromatography
description: Use when you have extracted retention times at peak maxima (rtFittedAPEX) from extracted-ion chromatograms (XICs) of known internal RT calibrants (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - rawrr
  - RawFileReader
  - R base lm()
  techniques:
  - LC-MS
derived_from:
- doi: 10.1101/2020.10.30.362533
  title: rawrr
- doi: 10.1021/acs.jproteome.0c00866
  title: ''
evidence_spans:
- rawrr::readSpectrum
- Our .NET 8.0 [@dotnet] precompiled wrapper methods are bundled, including the runtime, in the `r BiocStyle::Biocpkg('rawrr')` executable file
- The extracted information is written to a temporary location on the harddrive, read back into memory and parsed into `R` objects using RawFileReader API
- 'ThermoFisher.CommonCore dlls can be obtained through: https://github.com/thermofisherlsms/RawFileReader'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_rawrr
    doi: 10.1101/2020.10.30.362533
    title: rawrr
  dedup_kept_from: coll_rawrr
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2020.10.30.362533
  all_source_dois:
  - 10.1101/2020.10.30.362533
  - 10.1021/acs.jproteome.0c00866
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# linear-regression-fitting-for-chromatography

## Summary

Fit a linear regression model to retention time (RT) data extracted from liquid chromatography–mass spectrometry (LC-MS) runs using calibrant peptides (e.g., iRT standards) to quantify the linearity of RT behavior and validate chromatographic reproducibility. This skill produces an R-squared value that measures how well the fitted model explains variance in observed retention times.

## When to use

Apply this skill when you have extracted retention times at peak maxima (rtFittedAPEX) from extracted-ion chromatograms (XICs) of known internal RT calibrants (e.g., 11 iRT peptides with annotated iRTscore values), and you want to assess whether your LC-MS chromatographic system behaves predictably and linearly across the mass range. Use this as a quality-control step after raw data extraction and chromatogram fitting to validate instrumental performance.

## When NOT to use

- Input chromatograms contain fewer than 4–5 calibrant peptides; linear regression requires sufficient degrees of freedom and a wide dynamic range of iRTscore values to be statistically meaningful.
- Calibrant peptides show evidence of co-elution, peak overlap, or poor XIC signal-to-noise; the extracted rtFittedAPEX values will be biased and invalidate the model.
- The LC-MS system is known to operate in non-linear RT regions (e.g., very early or very late in the gradient), where a linear model is mechanistically inappropriate.

## Inputs

- rawrr::rawrrChromatogram object (extracted ion chromatograms for calibrant peptides)
- vector of observed retention times (rtFittedAPEX, in minutes)
- vector of reference iRT calibration scores (iRTscore, unitless or in relative RT units)

## Outputs

- linear regression model object (lm class in R)
- R-squared value (coefficient of determination, 0–1 range)
- fitted slope and intercept coefficients
- predicted retention times for validation set

## How to apply

Extract RT values at the maximum of intensity traces for all calibrant peptide XICs using rawrr::readChromatogram() with 10 ppm mass tolerance and 'xic' filter type. Fit an intercept-free or intercept-enabled linear model lm(rtFittedAPEX ~ iRTscore) using the observed RTs and their corresponding reference iRT scores. Report the R-squared value from the model summary: values > 0.99 indicate highly linear RT behavior characteristic of well-functioning Orbitrap systems. The fitted model slope and intercept can also be used to transform future observed RTs to predicted retention indices for target compound identification.

## Related tools

- **rawrr** (R package used to extract chromatogram data and read Thermo Orbitrap raw files; provides readChromatogram() and readFileHeader() functions to obtain RT values and instrument metadata) — https://github.com/fgcz/rawrr
- **RawFileReader** (.NET assembly wrapped by rawrr that provides low-level binary access to Thermo Scientific .raw file contents) — https://github.com/thermofisherlsms/RawFileReader
- **R base lm()** (Standard R function used to fit linear regression models to RT data and iRT calibration scores)

## Examples

```
C <- rawrr::readChromatogram(rawfile, mass = iRTmz, tol = 10, type = 'xic', filter = 'ms'); lm_fit <- lm(rtFittedAPEX ~ iRTscore, data = data.frame(rtFittedAPEX = observed_rts, iRTscore = irt_scores)); summary(lm_fit)$r.squared
```

## Evaluation signals

- R-squared value is ≥ 0.9999 (as reported in the article for iRT regression on well-functioning Q Exactive HF), indicating that the linear model explains >99.99% of variance in observed RTs.
- Residuals of the fitted model are normally distributed and homoscedastic (checked via plot(lm_object) diagnostics); systematic patterns in residuals suggest non-linearity or outliers.
- Fitted RTs computed from the model (predict(lm_object)) match observed rtFittedAPEX values with mean absolute error <0.5 min (or proportionally < 2% of gradient time).
- All 11 iRT calibrant peptides (or minimum of 5 peptides across wide iRTscore range) are included in the model fit; no calibrants are excluded as outliers without documented justification.

## Limitations

- The skill assumes that rtFittedAPEX values from chromatogram peak-fitting are accurate; poor peak shape or baseline noise will propagate error into the regression.
- Linear regression can mask localized non-linearity; RT behavior may be linear in one region (e.g., iRTscore 10–80) but non-linear at extremes. Inspect residuals and consider polynomial or spline fits if R-squared is unexpectedly low (<0.99).
- On Windows systems, the rawrr::readChromatogram() function requires the decimal symbol to be configured as '.' (period) in system locale settings; failure to do so causes data extraction errors.
- The skill is specific to Thermo Scientific Orbitrap .raw files (as wrapped by RawFileReader); adaptation to other instrument formats (Waters, Bruker, Sciex) would require different data-reading libraries.

## Evidence

- [other] construct a linear regression model lm(rtFittedAPEX ~ iRTscore) using annotated iRT reference scores and report R-squared value: "Fit intensity traces stored in rawrrChromatogram objects to extract retention times at maximum intensity (rtFittedAPEX). Construct a linear regression model lm(rtFittedAPEX ~ iRTscore) using"
- [other] Extract ion chromatograms using readChromatogram with 10 ppm tolerance: "Extract precursor m/z values and retention times for known iRT peptide standards using rawrr::readChromatogram() with mass tolerance 10 ppm and XIC filter."
- [other] R-squared of 0.9999 indicates highly linear RT behavior: "R-squared of 0.9999 for iRT regression indicating highly linear RT behavior"
- [other] Extract RTs at maximum of fitted intensity traces and fit linear model: "we extract the RTs at the maximum of the fitted intensity traces stored in the `rawrrChromatogram` object and fit a linear model"
- [readme] rawrr wraps RawFileReader .NET assembly functionality: "rawrr wraps the functionality of the RawFileReader .NET assembly"
