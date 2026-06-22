---
name: retention-time-index-calibration
description: Use when you have acquired a bottom-up proteomics LC-MS/MS run (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - RawFileReader
  - rawrr
  - MsBackendRawFileReader
  techniques:
  - LC-MS
derived_from:
- doi: 10.1101/2020.10.30.362533
  title: rawrr
- doi: 10.1021/acs.jproteome.0c00866
  title: ''
evidence_spans:
- Calling a wrapper method typically results in the execution of methods defined in the `RawFileReader` dynamic link library provided by Thermo Fisher Scientific.
- invoke compiled `C#` wrapper methods using a system call. Calling a wrapper method typically results in the execution of methods defined in the `RawFileReader` dynamic link library provided by Thermo
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_rawrr_2_cq
    doi: 10.1101/2020.10.30.362533
    title: rawrr
  dedup_kept_from: coll_rawrr_2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2020.10.30.362533
  all_source_dois:
  - 10.1101/2020.10.30.362533
  - 10.1021/acs.jproteome.0c00866
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# retention-time-index-calibration

## Summary

Calibrate observed LC retention times against internal retention time (iRT) standards by fitting a linear regression model to map MS scan retention times to iRT scores, enabling downstream RT-based peptide identification and method validation. This skill establishes a quantitative RT–iRT relationship for quality control and cross-run alignment in Orbitrap proteomics workflows.

## When to use

Apply this skill when you have acquired a bottom-up proteomics LC-MS/MS run (e.g., autoQC sample) containing iRT peptide standard mix injections and need to (1) validate that observed retention times behave linearly with known iRT reference values, (2) establish a RT calibration model for subsequent targeted or data-dependent workflows, or (3) diagnose LC gradient performance and peptide retention consistency. Typical trigger: presence of iRT peptide peaks in MS1 chromatograms with known Biognosys iRT scores and a run length of 10–100 min.

## When NOT to use

- Input does not include iRT peptide standards or reference iRT scores are unavailable — use alternative RT normalization methods (e.g., landmark peptide calibration, retention time prediction from sequence).
- MS run contains only MS2 data or MS1 scans lack chromatogram traces — readChromatogram() requires high-resolution intensity time series.
- Multiple distinct LC gradient profiles or non-linear flow conditions are present — linear regression assumption violates; use polynomial or spline-based calibration instead.
- Observed R² < 0.95 or residuals show systematic bias — indicates instrumental malfunction or column degradation; investigate LC system before proceeding with RT-dependent quantification.

## Inputs

- Thermo Fisher Scientific .raw file (Orbitrap instrument output)
- iRT peptide standard mix reference table (Biognosys iRT scores: LGGSSEPVTGLDAK, GAGSSEPVTGLDAK, VLEAQWESGYVER, TPVISITGSVSSNK, ADVTPADFSEVTSK, GTFIIDPGGVIQR, GTFIIDPAAVIQK, LFLQFGAQGSPHF, IYAPDSVEFSR, ADVTPADFSEVSK)
- MS1 scan index (output of readIndex())
- Chromatogram data for iRT peptides (output of readChromatogram())

## Outputs

- Linear regression model object (class 'lm') with fitted intercept and slope
- Intercept coefficient (a): predicted RT of reference peptide at iRT score = 0
- Slope coefficient (b): RT gradient (minutes per iRT unit)
- R-squared statistic quantifying linearity of RT–iRT relationship
- Residual standard error (measurement of model fit quality)
- Calibrated RT values for all iRT peptides (predicted vs. observed comparison)

## How to apply

First, read the raw file header and MS scan index using rawrr::readFileHeader() and rawrr::readIndex() to identify all MS1-level scans and their native retention times. Next, extract intensity chromatogram traces for iRT peptides using rawrr::readChromatogram(), which returns a rawrrChromatogramSet object; fit a spline or Gaussian to each chromatogram and identify the retention time at maximum intensity (rtFittedAPEX). Map each detected iRT peptide peak to its known Biognosys iRT score reference value. Then fit a linear regression model lm(rtFittedAPEX ~ iRTscore) to the matched pairs. Extract and inspect the fitted intercept (a) and slope (b): the intercept represents the predicted RT of the zero-iRT reference peptide GAGSSEPVTGLDAK, while the slope quantifies the RT gradient per iRT unit (typically ~1.5% buffer B per minute for standard 20 min gradients). Evaluate model fit quality via R² (expect R² > 0.99 for well-behaved LC systems); deviations suggest instrumental drift, column contamination, or gradient instability.

## Related tools

- **rawrr** (R package providing readSpectrum(), readChromatogram(), readFileHeader(), and readIndex() functions to extract MS scans, chromatogram intensity traces, file metadata, and scan indices from proprietary Thermo .raw files) — https://github.com/fgcz/rawrr
- **RawFileReader** (Vendor-supplied .NET assembly (C#) wrapped by rawrr; implements low-level access to binary .raw file structure and spectral metadata on Windows, Linux, and macOS) — https://github.com/thermofisherlsms/RawFileReader
- **MsBackendRawFileReader** (Bioconductor backend integrating rawrr with the Spectra package ecosystem for standardized on-disk access to Orbitrap spectral data and metadata) — https://github.com/cpanse/MsBackendRawFileReader

## Examples

```
library(rawrr); installRawrrExe(); raw_file <- '20181113_010_autoQC01.raw'; H <- readFileHeader(raw_file); idx <- readIndex(raw_file); ms1_scans <- subset(idx, msLevel == 1); chroms <- readChromatogram(raw_file, mass = c(391.2844, 437.2648, 556.2766, 641.3450, 702.3568, 727.3990, 789.4108, 805.4057, 748.3696, 804.4161)); model <- lm(rtFittedAPEX ~ iRTscore, data = iRT_matched_df); summary(model)
```

## Evaluation signals

- R² value ≥ 0.99 indicates highly linear retention time behavior consistent with well-functioning LC gradient; values 0.95–0.98 warrant investigation of LC performance; R² < 0.95 suggests instrumental miscalibration or column contamination.
- Residuals of the fitted linear model should be randomly distributed with no systematic trend (e.g., no U-shape or drift over iRT score range); Shapiro–Wilk test p-value > 0.05 supports normality assumption.
- Slope (b) should be close to expected 1.5% buffer B per minute for standard 20 min gradients; deviations > 20% indicate non-standard gradient profiles or flow rate instabilities.
- Intercept (a) should match the observed retention time of the zero-iRT reference peptide GAGSSEPVTGLDAK; systematic offsets > 0.5 min suggest column aging or equilibration issues.
- Visual inspection: scatter plot of observed rtFittedAPEX vs. iRT score should show tight clustering around the fitted regression line with no obvious outliers; any peptide > 3 residual standard errors from the line warrants verification of peak identity or exclusion as a measurement artifact.

## Limitations

- Linear regression assumes a linear RT–iRT relationship; non-linear chromatographic behavior (e.g., late-eluting hydrophobic peptides or early-eluting highly charged species) may violate this assumption and reduce model fit.
- Requires high-quality chromatogram peaks with well-defined maxima; co-eluting contaminants or low signal-to-noise ratios lead to incorrect rtFittedAPEX values and calibration drift.
- Biognosys iRT scores are empirical reference values obtained on specific instrument and LC configurations; transferability to different column chemistries, flow rates, or temperature protocols is limited.
- The skill applies only to Thermo Fisher Orbitrap instruments supported by RawFileReader; incompatible with other vendor formats (Waters .raw, Bruker .d, AB Sciex .wiff) without format conversion.
- Calibration model is specific to a single LC–MS run; temporal drift in RT over multiple runs requires re-calibration or use of run-to-run alignment methods.
- Missing or truncated chromatogram data (e.g., due to detector saturation or scan duty cycle constraints) can result in failed peak detection for one or more iRT peptides, leading to incomplete or biased model fitting.

## Evidence

- [other] What are the fitted intercept and slope coefficients of a linear regression model relating observed retention times to iRT scores for the iRT peptide standard mix in the autoQC01.raw file?: "What are the fitted intercept and slope coefficients of a linear regression model relating observed retention times to iRT scores for the iRT peptide standard mix in the autoQC01.raw file?"
- [other] The fitted iRT regression model shows highly linear retention time behavior (high R²), with the intercept (a) equal to the predicted RT of the iRT peptide GAGSSEPVTGLDAK (zero iRT score reference point) and the slope (b) equivalent to the gradient change rate of approximately 1.5% buffer B per minute during the 20 min LC gradient.: "The fitted iRT regression model shows highly linear retention time behavior (high R²), with the intercept (a) equal to the predicted RT of the iRT peptide GAGSSEPVTGLDAK (zero iRT score reference"
- [other] Extract retention times and scan numbers for MS1 scans using readSpectrum(). Read the intensity traces (chromatogram data) using readChromatogram() for the iRT peptides. Extract retention times at the maximum of the fitted intensity traces stored in the rawrrChromatogram object.: "Extract retention times at the maximum of the fitted intensity traces stored in the rawrrChromatogram object."
- [other] Fit a linear model lm(rtFittedAPEX ~ iRTscore) to the matched retention time and iRT score pairs. Extract and return the intercept and slope coefficients from the fitted model object.: "Fit a linear model lm(rtFittedAPEX ~ iRTscore) to the matched retention time and iRT score pairs."
- [intro] rawrr wraps the functionality of the RawFileReader .NET assembly: "rawrr wraps the functionality of the RawFileReader .NET assembly"
- [methods] R functions requesting access to data stored in binary raw files (reader family functions listed in Table 1) invoke compiled C# wrapper methods using a system call.: "R functions requesting access to data stored in binary raw files (reader family functions listed in Table 1) invoke compiled C# wrapper methods using a system call."
- [results] The corresponding R-squared indicates that the RTs behave highly linear: "The corresponding R-squared indicates that the RTs behave highly linear"
- [readme] rawrr provides access to proprietary Thermo Fisher Scientific Orbitrap instrument data as a stand-alone R package or serves as MsRawFileReaderBackend for the Bioconductor Spectra package.: "rawrr provides access to proprietary Thermo Fisher Scientific Orbitrap instrument data as a stand-alone R package"
