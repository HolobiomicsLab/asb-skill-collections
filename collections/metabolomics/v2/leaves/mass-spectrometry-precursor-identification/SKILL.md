---
name: mass-spectrometry-precursor-identification
description: Use when when you need to locate and extract quantitative retention time
  and intensity data for known peptide standards (e.g., iRT peptides) from a Thermo
  .raw file to validate LC-MS retention time linearity, assess method reproducibility,
  or establish retention time calibration curves.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - rawrr
  - RawFileReader
  - Spectra
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

# Mass Spectrometry Precursor Identification

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Identify and extract precursor m/z values and retention times for peptide standards from Thermo Orbitrap raw files using extracted ion chromatograms (XIC) with tight mass tolerance. This skill enables validation of LC-MS method linearity and peptide behavior through comparison of experimental retention times against known reference standards.

## When to use

When you need to locate and extract quantitative retention time and intensity data for known peptide standards (e.g., iRT peptides) from a Thermo .raw file to validate LC-MS retention time linearity, assess method reproducibility, or establish retention time calibration curves. Apply this skill when standard peptides are available with known m/z values and reference retention time scores (iRTscore).

## When NOT to use

- Input is already a processed feature table or aligned retention time matrix — use this skill only when working directly with raw binary .raw files that require chromatogram extraction.
- Working with non-Thermo instrument formats (e.g., Bruker .d, Waters .raw, mzML) — rawrr and RawFileReader are specific to Thermo Orbitrap instruments.
- No known peptide standards or reference retention time scores are available — the skill requires ground truth m/z and iRT scores to construct the validation regression.

## Inputs

- Thermo Fisher Scientific .raw file (e.g., 20181113_010_autoQC01.raw from Orbitrap Q Exactive HF)
- List of precursor m/z values for peptide standards
- Reference retention time scores or iRT scores for standards
- Mass tolerance parameter (typically 10 ppm)
- MS-level filter specification (e.g., 'ms' for MS1 scans)

## Outputs

- Extracted ion chromatogram (XIC) objects (rawrrChromatogram)
- Fitted retention times at maximum intensity (rtFittedAPEX) for each precursor
- Linear regression model object with R-squared value
- Quantified R-squared metric indicating retention time linearity

## How to apply

First, obtain the target precursor m/z values and reference retention time scores (e.g., iRTscore) for your peptide standards. Load the raw file using rawrr::readFileHeader() to confirm instrument configuration (e.g., Q Exactive HF, Orbitrap). Extract extracted ion chromatograms (XIC) for each precursor using rawrr::readChromatogram() with type='xic', specifying the precursor mass list, a tight mass tolerance (e.g., 10 ppm), and filter='ms' to isolate MS1-level precursor signals. Fit the intensity traces stored in the returned rawrrChromatogram objects to identify the retention time at maximum intensity (rtFittedAPEX) for each peptide. Finally, construct a linear regression model (e.g., lm(rtFittedAPEX ~ iRTscore)) to evaluate the linearity of retention time behavior across standards; an R-squared value near 1.0 (e.g., 0.9999) indicates highly linear RT behavior and validates method performance.

## Related tools

- **rawrr** (Primary R package for reading Thermo Orbitrap .raw file chromatogram data and extracting precursor ion intensities and retention times via readChromatogram() and readFileHeader() functions) — https://github.com/fgcz/rawrr
- **RawFileReader** (Underlying .NET assembly (C# wrapper) that rawrr invokes via system calls to access binary Thermo .raw file structure) — https://github.com/thermofisherlsms/RawFileReader
- **Spectra** (Optional Bioconductor backend via MsBackendRawFileReader for high-level spectral data access and manipulation in R) — https://bioconductor.org/packages/Spectra/
- **MsBackendRawFileReader** (Bioconductor-compatible backend that bridges rawrr functionality into the Spectra package ecosystem for standardized spectral accessor functions) — https://github.com/cpanse/MsBackendRawFileReader

## Examples

```
C <- rawrr::readChromatogram(rawfile, mass = c(450.21, 481.24, 502.26), tol = 10, type = "xic", filter = "ms"); rtFittedAPEX <- sapply(C, function(x) x$mz[which.max(x$intensity)]); fit <- lm(rtFittedAPEX ~ iRTscore); summary(fit)$r.squared
```

## Evaluation signals

- Extracted retention times (rtFittedAPEX) for all precursor standards are successfully returned from the rawrrChromatogram object and match the expected peptide elution window in the LC method.
- Linear regression R-squared value is ≥ 0.99 or higher, confirming highly linear retention time behavior across the standard peptides; values significantly lower (e.g., < 0.95) indicate potential instrument drift, calibration failure, or incorrect precursor identification.
- Fitted retention times exhibit low residual error and no systematic deviation across the iRTscore range, indicating unbiased and stable retention time prediction.
- All expected peptide standards (e.g., 11 iRT peptides) are detected and extracted without missing peaks; absence or very low intensity for any standard suggests chromatographic or ionization problems.
- Mass accuracy of extracted precursor m/z values remains within the specified tolerance (e.g., 10 ppm); larger deviations indicate potential mass calibration drift or incorrect filter specification.

## Limitations

- rawrr and RawFileReader are exclusive to Thermo Fisher Scientific Orbitrap instruments; other mass spectrometer formats (Bruker, Waters, AB Sciex) require alternative reading libraries.
- Windows systems require explicit decimal symbol configuration as '.' for proper data extraction via the RawFileReader .NET assembly; this platform dependency may complicate automated workflows across OS.
- The skill depends on access to compiled C# RawFileReader assemblies; availability and licensing of these binaries may restrict deployment in some environments.
- Performance and accuracy of retention time fitting depend on adequate XIC signal intensity and peak shape; low-abundance precursors or poor chromatographic resolution may lead to unreliable rtFittedAPEX estimates.
- The linear regression model assumes a simple linear relationship between iRTscore and observed RT; non-linear retention time behavior or systematic drift across the gradient may not be captured by this univariate approach.

## Evidence

- [other] Extract precursor m/z values and retention times for known iRT peptide standards using rawrr::readChromatogram() with mass tolerance 10 ppm and XIC filter.: "Extract precursor m/z values and retention times for known iRT peptide standards using rawrr::readChromatogram() with mass tolerance 10 ppm and XIC filter."
- [other] Fit intensity traces stored in rawrrChromatogram objects to extract retention times at maximum intensity (rtFittedAPEX).: "Fit intensity traces stored in rawrrChromatogram objects to extract retention times at maximum intensity (rtFittedAPEX)."
- [other] Construct a linear regression model lm(rtFittedAPEX ~ iRTscore) using annotated iRT reference scores and report R-squared value.: "Construct a linear regression model lm(rtFittedAPEX ~ iRTscore) using annotated iRT reference scores and report R-squared value."
- [methods] The example file `20181113_010_autoQC01.raw` used throughout this manuscript contains Fourier-transformed Orbitrap spectra (FTMS) recorded on a Thermo Fisher Scientific Q Exactive HF: "The example file `20181113_010_autoQC01.raw` used throughout this manuscript contains Fourier-transformed Orbitrap spectra (FTMS) recorded on a Thermo Fisher Scientific Q Exactive HF"
- [methods] R functions requesting access to data stored in binary raw files (reader family functions listed in Table 1) invoke compiled `C#` wrapper methods using a system call: "R functions requesting access to data stored in binary raw files (reader family functions listed in Table 1) invoke compiled `C#` wrapper methods using a system call"
- [results] we extract the RTs at the maximum of the fitted intensity traces stored in the `rawrrChromatogram` object and fit a linear model: "we extract the RTs at the maximum of the fitted intensity traces stored in the `rawrrChromatogram` object and fit a linear model"
- [results] The corresponding R-squared indicates that the RTs behave highly linear: "The corresponding R-squared indicates that the RTs behave highly linear"
- [readme] rawrr wraps the functionality of the RawFileReader .NET assembly: "rawrr wraps the functionality of the RawFileReader .NET assembly"
- [discussion] On Windows, the decimal symbol has to be configured as a '.'!: "On Windows, the decimal symbol has to be configured as a '.'!"
