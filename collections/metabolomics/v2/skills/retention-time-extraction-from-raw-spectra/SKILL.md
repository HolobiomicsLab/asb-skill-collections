---
name: retention-time-extraction-from-raw-spectra
description: Use when when you have Thermo Orbitrap .raw files containing known reference
  peptides (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - rawrr
  - RawFileReader
  - MsBackendRawFileReader
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1101/2020.10.30.362533
  title: rawrr
- doi: 10.1021/acs.jproteome.0c00866
  title: ''
evidence_spans:
- rawrr::readSpectrum
- Our .NET 8.0 [@dotnet] precompiled wrapper methods are bundled, including the runtime,
  in the `r BiocStyle::Biocpkg('rawrr')` executable file
- The extracted information is written to a temporary location on the harddrive, read
  back into memory and parsed into `R` objects using RawFileReader API
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

# retention-time-extraction-from-raw-spectra

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Extract and validate retention time measurements from Thermo Fisher Scientific Orbitrap raw files by reading chromatographic data, fitting intensity traces to identify apex retention times, and evaluating linearity through regression modeling. This skill bridges proprietary binary .raw file formats to quantitative RT calibration and quality control in bottom-up proteomics.

## When to use

When you have Thermo Orbitrap .raw files containing known reference peptides (e.g., iRT standards) and need to (1) verify instrument retention time stability and linearity, (2) extract precise RT values at peak apex for calibration curves, or (3) validate LC-MS method performance by comparing observed vs. expected RT behavior. Typical trigger: QC workflows requiring reproducibility metrics, or iRT-based retention time alignment across runs.

## When NOT to use

- Non-Thermo instruments (e.g., Bruker, AB Sciex, Waters Synapt): rawrr wraps RawFileReader, which reads only Thermo .raw files; alternative tools (ProteoWizard, ThermoRawFileParser) or formats (mzML, mzXML) are required.
- Raw files from instruments without iRT or stable reference standards: the skill depends on annotated reference peptides with known RT scores; uncharacterized samples cannot be evaluated.
- Already-processed RT data (e.g., peak lists, mzML with centroids): this skill requires direct access to binary scan metadata and intensity traces; use this skill upstream of feature detection, not downstream.

## Inputs

- Thermo Fisher Scientific .raw file (binary Orbitrap format)
- Reference peptide metadata (m/z values, iRT scores, or other known RT scale)
- Mass tolerance window (ppm) for XIC extraction
- Scan filter specification (e.g., 'ms' for MS1-level data)

## Outputs

- Extracted ion chromatogram (rawrrChromatogram object with intensity vs. time)
- Retention time at apex for each reference peptide (rtFittedAPEX)
- Linear regression model object (lm class) with coefficients and R-squared
- R-squared value quantifying RT linearity (unitless, 0–1 scale)
- Fitted RT values and residuals for quality assessment

## How to apply

Load the binary .raw file using rawrr::readFileHeader() to confirm instrument metadata and scan parameters. Extract extracted ion chromatograms (XIC) for known reference peptide precursor m/z values using rawrr::readChromatogram() with type='xic', filter='ms' (for MS1-level scans), and a mass tolerance window (e.g. 10 ppm). For each XIC, fit a curve to the intensity trace to locate the retention time at maximum intensity (rtFittedAPEX). Construct a linear regression model lm(rtFittedAPEX ~ iRTscore) using annotated iRT reference scores, then report and interpret the R-squared value; R² > 0.99 indicates highly linear RT behavior suitable for downstream RT calibration. Document the fitted model coefficients and residuals as quality metrics.

## Related tools

- **rawrr** (R package providing direct read access to Thermo .raw file binary data; supplies readFileHeader(), readChromatogram(), and readSpectrum() functions for metadata and intensity trace extraction) — https://github.com/fgcz/rawrr
- **RawFileReader** (.NET assembly (C#) wrapping proprietary Thermo Scientific APIs; underlying dependency invoked by rawrr via system calls to extract chromatographic and spectral data) — https://github.com/thermofisherlsms/RawFileReader
- **MsBackendRawFileReader** (Optional Bioconductor backend enabling rawrr integration with Spectra package for standardized accessor functions and on-disk data handling) — https://github.com/cpanse/MsBackendRawFileReader

## Examples

```
C <- rawrr::readChromatogram(rawfile = '20181113_010_autoQC01.raw', mass = c(463.2671, 437.2808, 437.2655), tol = 10, type = 'xic', filter = 'ms'); fit <- lm(rtFittedAPEX ~ iRTscore, data = data.frame(rtFittedAPEX = c(...), iRTscore = c(-24.92, -14.15, 19.79))); summary(fit)$r.squared
```

## Evaluation signals

- R-squared value for lm(rtFittedAPEX ~ iRTscore) ≥ 0.99 indicates highly linear RT behavior; lower values (e.g., R² < 0.98) suggest instrumental drift or data quality issues requiring investigation.
- Residuals from the fitted regression model should be approximately normally distributed with mean near zero and constant variance; large or systematic deviations indicate non-linear RT behavior or outlier reference peptides.
- For each iRT peptide, rtFittedAPEX should fall within ±0.2 min of the expected retention time predicted by the regression model; deviations > 0.5 min suggest chromatographic problems or m/z calibration drift.
- XIC peak shape should be symmetric and unimodal; asymmetric or multi-modal intensity traces indicate co-eluting species or baseline issues that compromise apex-fitting accuracy.
- Comparison across multiple runs or time points: R² values should remain stable (variation < 0.001); systematic decline in R² over time signals instrument maintenance need or column degradation.

## Limitations

- Windows decimal symbol configuration: on Windows systems, the decimal symbol must be set to '.' (full stop) for proper data extraction; regional locale settings using ',' (comma) will cause parsing failures.
- Chromatogram resolution and fitting algorithm sensitivity: apex fitting depends on adequate intensity sampling density and curve-fitting quality; low-resolution or noisy XIC traces may yield unreliable rtFittedAPEX values, especially for co-eluting peptides.
- RawFileReader .NET dependency: rawrr invokes compiled C# methods via system calls, requiring Mono (.NET runtime) on Linux/macOS; Windows users may encounter additional complexity managing ThermoFisher.CommonCore DLL versions.
- Reference peptide annotation requirement: accurate iRT scores or other RT standards are mandatory; mislabeled or contaminated reference materials will corrupt the regression model and produce misleading R² values.
- Scope limited to Thermo Orbitrap instruments: readFileHeader() confirms Q Exactive HF and related Orbitrap platforms; no support for other vendors (Bruker, Waters, AB Sciex) without external conversion to mzML or mzXML.

## Evidence

- [methods] Extract and validate retention times from Orbitrap .raw files: "Extract precursor m/z values and retention times for known iRT peptide standards using rawrr::readChromatogram() with mass tolerance 10 ppm and XIC filter."
- [results] Fit intensity traces to apex for RT extraction: "we extract the RTs at the maximum of the fitted intensity traces stored in the `rawrrChromatogram` object and fit a linear model"
- [results] R-squared as linearity metric: "The corresponding R-squared indicates that the RTs behave highly linear"
- [intro] rawrr wraps RawFileReader for .raw file access: "rawrr wraps the functionality of the RawFileReader .NET assembly"
- [discussion] Windows decimal symbol configuration requirement: "On Windows, the decimal symbol has to be configured as a '.'!"
- [methods] iRT peptide standard reference: "The file is part of the MassIVE dataset [MSV000086542]"
