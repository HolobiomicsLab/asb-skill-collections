---
name: extracted-ion-chromatogram-processing
description: Use when you have Thermo Fisher Orbitrap .raw files and need to locate and quantify specific peptide precursor ions (e.g., iRT calibrants, synthetic standards, or putative identifications).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3673
  tools:
  - rawrr
  - RawFileReader
  - MsBackendRawFileReader
  - rawDiag
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# extracted-ion-chromatogram-processing

## Summary

Extract and process chromatographic traces for specific m/z values from Thermo Fisher Scientific raw files, enabling targeted detection and retention time annotation of peptide precursors. This skill bridges low-level binary data access with high-level peptide identification by isolating XIC signals at user-defined mass tolerance.

## When to use

You have Thermo Fisher Orbitrap .raw files and need to locate and quantify specific peptide precursor ions (e.g., iRT calibrants, synthetic standards, or putative identifications). Use this skill when retention time, intensity, or peak shape information for targeted m/z values is required for calibration, method development, or validation—particularly when working with small sets of known precursor masses (< 100) in complex proteomics runs.

## When NOT to use

- Input is already processed feature tables (mzML, mzXML, CSV peak lists) — use mass spectrometry format conversion tools instead.
- You need to extract and process all ions in the run (full MS1 or MS2 spectra) rather than targeted m/z values — use readSpectrum() or readIndex() for untargeted access.
- The raw file is not from Thermo Fisher Orbitrap instruments (e.g., Waters, AB Sciex, Bruker) — rawrr only supports .raw files from Thermo instruments and requires the RawFileReader .NET assembly.

## Inputs

- Thermo Fisher Scientific .raw file (binary Orbitrap data)
- Vector of precursor m/z values (numeric)
- Reference annotations (e.g., iRT scores, peptide identities)
- Mass tolerance in ppm (integer or numeric)
- Scan filter string (character; e.g., 'ms' for MS1)

## Outputs

- rawrrChromatogram object(s) containing intensity vs. retention time traces
- Fitted retention times (rtFittedAPEX) for each precursor m/z
- Linear regression model object(s) (class 'lm') relating RT to reference score
- R-squared statistic and residual diagnostics for RT linearity assessment
- Annotated data.frame with m/z, observed RT, reference score, and fit quality metrics

## How to apply

Load the raw file using rawrr::readFileHeader() to confirm instrument type and metadata. Prepare a vector of precursor m/z values and their associated reference masses (e.g., iRT scores). Call rawrr::readChromatogram() with the mass vector, setting type='xic', tol=10 (or your calibration tolerance in ppm), and filter='ms' to extract MS1-level ion chromatograms. The function returns rawrrChromatogram objects containing intensity profiles for each m/z trace. Fit Gaussian or polynomial curves to each trace to extract the retention time at maximum intensity (rtFittedAPEX). Annotate the fitted RTs with their corresponding reference scores and evaluate linearity via linear regression (lm(rtFittedAPEX ~ iRTscore)) to assess RT calibration quality. Use R-squared and residual diagnostics to validate that RT behavior is sufficiently linear (typically R² > 0.99 for calibrants).

## Related tools

- **rawrr** (R package wrapping RawFileReader; provides readChromatogram() function to extract ion chromatograms from .raw files and readFileHeader() for metadata validation) — https://github.com/fgcz/rawrr
- **RawFileReader** (Thermo Fisher Scientific .NET assembly underlying rawrr; performs low-level binary parsing and XIC extraction from Orbitrap .raw files) — https://github.com/thermofisherlsms/RawFileReader
- **MsBackendRawFileReader** (Bioconductor backend integrating rawrr with the Spectra package for standardized chromatogram and spectrum access in R) — https://github.com/cpanse/MsBackendRawFileReader
- **rawDiag** (R package for visualization and diagnostic analysis of LC-MS method parameters; complements rawrr for XIC quality assessment and instrument diagnostics) — https://github.com/fgcz/rawDiag

## Examples

```
C <- rawrr::readChromatogram(rawfile = '20181113_010_autoQC01.raw', mass = c(487.2567, 547.3087), tol = 10, type = 'xic', filter = 'ms'); rtFitted <- sapply(C, function(x) x$rt[which.max(x$intensity)]); fit <- lm(rtFitted ~ c(15.994, 28.971)); summary(fit)$r.squared
```

## Evaluation signals

- readChromatogram() successfully returns a rawrrChromatogram object with non-empty intensity and retention time vectors for each requested m/z.
- Fitted retention times (rtFittedAPEX) are reproducible and lie within the observed scan retention time range (no extrapolation beyond run boundaries).
- Linear regression R-squared for lm(rtFittedAPEX ~ iRTscore) is ≥ 0.99 or meets your calibration standard; residuals show no systematic trend.
- Mass tolerance (10 ppm) is validated by checking that observed m/z of extracted peaks match theoretical precursor m/z within the specified window.
- Peak shape diagnostics (e.g., fitted curve shape, goodness-of-fit) are consistent with expected chromatographic widths (typical LC peak width 10–30 s on Orbitrap).

## Limitations

- rawrr requires the Thermo Fisher RawFileReader .NET assembly and works on Windows, Linux, and macOS with .NET Framework or Mono; on Windows, the system decimal symbol must be configured as '.' for proper numeric parsing.
- XIC extraction is limited to MS1 (type='xic', filter='ms'); targeted MS/MS chromatogram extraction is not directly supported via readChromatogram().
- Performance degrades with very large m/z lists (> 1000 targets) or very narrow mass tolerances (< 1 ppm) due to increased I/O overhead.
- Retention time fitting accuracy depends on chromatographic peak quality; co-eluting precursors or low-intensity traces may yield unreliable rtFittedAPEX values.
- The skill assumes homogeneous retention time behavior across the run; non-linear RT drift or multi-segment calibration requires post-hoc segmentation and is not automated.

## Evidence

- [methods] Extract precursor m/z values and retention times for known iRT peptide standards using rawrr::readChromatogram() with mass tolerance 10 ppm and XIC filter.: "Extract precursor m/z values and retention times for known iRT peptide standards using rawrr::readChromatogram() with mass tolerance 10 ppm and XIC filter."
- [methods] Fit intensity traces stored in rawrrChromatogram objects to extract retention times at maximum intensity (rtFittedAPEX).: "Fit intensity traces stored in rawrrChromatogram objects to extract retention times at maximum intensity (rtFittedAPEX)."
- [results] The corresponding R-squared indicates that the RTs behave highly linear: "The corresponding R-squared indicates that the RTs behave highly linear"
- [results] we extract the RTs at the maximum of the fitted intensity traces stored in the rawrrChromatogram object and fit a linear model: "we extract the RTs at the maximum of the fitted intensity traces stored in the rawrrChromatogram object and fit a linear model"
- [intro] rawrr wraps the functionality of the RawFileReader .NET assembly: "rawrr wraps the functionality of the RawFileReader .NET assembly"
- [readme] Provides an alternative MsBackend to Spectra through the rawrr package. Ultimately this backend will allow direct access to spectral data logged in ThermoFischer Scientific .raw files: "Provides an alternative MsBackend to Spectra through the rawrr package. Ultimately this backend will allow direct access to spectral data logged in ThermoFischer Scientific .raw files"
