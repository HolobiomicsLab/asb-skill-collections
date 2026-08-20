---
name: instrumental-parameter-validation-mass-spectrometry
description: Use when when you have obtained a raw Orbitrap mass spectrometry file
  and need to verify that the instrument was configured as claimed in the methods
  section or dataset documentation—especially before investing in peptide fragmentation
  analysis, spectrum library matching, or quantitative proteomics.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - rawrr
  - RawFileReader
  - rawDiag
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

# instrumental-parameter-validation-mass-spectrometry

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Validate that raw mass spectrometry data were acquired with reported instrument parameters (resolving power, AGC injection time, scan type) and confirm spectral quality metrics (signal-to-noise ratios for fragment ions). This skill ensures that downstream analysis assumptions about data provenance and quality are justified before peptide identification or quantification.

## When to use

When you have obtained a raw Orbitrap mass spectrometry file and need to verify that the instrument was configured as claimed in the methods section or dataset documentation—especially before investing in peptide fragmentation analysis, spectrum library matching, or quantitative proteomics. Apply this skill when a research question depends on knowing whether resolving power, AGC target, injection time, or centroiding parameters meet expected thresholds.

## When NOT to use

- Input is already a processed feature table or peptide identification matrix; use this skill on raw binary files only.
- You only have access to mzML, mzXML, or other open-format conversions of the raw file—rawrr requires the original proprietary .raw file to extract full instrument metadata.
- The research question does not depend on instrument configuration (e.g., pure bioinformatics re-analysis of already-published identifications).

## Inputs

- Thermo Fisher Scientific .raw file (binary Orbitrap data)
- Target scan number (integer)
- Precursor peptide sequence (string)
- Expected instrument parameters (resolving power, AGC target, injection time thresholds)

## Outputs

- Validated instrument metadata object (resolving power, AGC target, realized injection time)
- Centroided m/z and intensity arrays for the scan
- Signal-to-noise ratio table for observed fragment ions
- Quality assessment report (pass/fail, S/N summary statistics)

## How to apply

Load the raw file using rawrr::readFileHeader() to extract instrument metadata (resolving power at 200 m/z, AGC target, maximum injection time). Then use rawrr::readSpectrum() with the target scan number to retrieve the actual spectrum and parse the returned rawrrSpectrum object for the realized AGC injection time and scan filter string. Compare realized values (e.g., 2.8 ms actual injection time vs. 55 ms maximum) to the reported or expected parameters. For each major fragment ion (y-ions, b-ions), calculate the signal-to-noise ratio by comparing the peak intensity to the local baseline noise floor. Verify that all expected fragment ions are several tens to hundreds of counts above noise; if S/N is marginal (< 10:1 for major ions), flag the spectrum as lower-quality and consider excluding it from downstream analysis or downweighting its contribution.

## Related tools

- **rawrr** (R package providing direct API access to Orbitrap .raw file headers, spectra, and chromatograms via RawFileReader .NET wrapper) — https://github.com/fgcz/rawrr
- **RawFileReader** (.NET assembly (C#) that parses proprietary Thermo Fisher binary .raw format and exposes metadata, scan filters, and spectral data) — https://github.com/thermofisherlsms/RawFileReader
- **rawDiag** (Companion R package for quality control visualization and diagnostic assessment of LC-MS method parameters and raw data health) — https://github.com/fgcz/rawDiag

## Examples

```
S <- rawrr::readSpectrum(rawfile = '20181113_010_autoQC01.raw', scan = 9594); H <- rawrr::readFileHeader(rawfile = '20181113_010_autoQC01.raw'); print(paste('Resolving Power:', S[[1]]$`Resolving Power`, 'AGC Time (ms):', S[[1]]$`AGC injection time`))
```

## Evaluation signals

- Realized AGC injection time (e.g., 2.8 ms) is correctly parsed and matches the value reported in the raw file header and in secondary documentation.
- Resolving power value (e.g., 30,000 at 200 m/z) from readSpectrum() metadata matches the instrument configuration stated in the methods.
- All theoretically expected y-ion and/or b-ion fragments for the precursor peptide (LGGNEQVTR/2 in example) are detected with S/N ≥ 10:1; absence of major ions or S/N < 3:1 flags poor-quality spectra.
- Scan filter string (e.g., 'FTMS + c NSI Full ms2 487.2567@hcd27.00') correctly identifies scan type, centroiding status, collision energy, and mass range.
- Total ion current (TIC) or base peak intensity is consistent with expected peptide abundance; extreme outliers (very low intensity, saturation artifacts) warrant manual review.

## Limitations

- rawrr and RawFileReader require Windows, Linux, or macOS with .NET 5+ runtime; the compiled C# wrapper may have platform-specific behavior or require decimal symbol configuration (must be '.' on Windows).
- The skill validates instrument *metadata* and spectral quality but does not validate peptide-spectrum match scores, retention time calibration, or database search results; it is a prerequisite check, not a full quality pipeline.
- Access to the full rawrrSpectrum object (119 data items) may be overkill for this task; practitioners should focus on resolving power, AGC time, scan filter, and m/z/intensity arrays rather than all available fields.
- If the raw file has been pre-processed (centroiding applied, lock-mass correction applied) during acquisition, the validation can only confirm what was written to disk; it cannot assess quality of the original uncorrected signal.

## Evidence

- [other] Scan 9594 was successfully extracted using rawrr::readSpectrum, confirming resolving power of 30,000 at 200 m/z and AGC injection time of 2.8 ms (~5% of maximum 55 ms); all y-ion signals for LGGNEQVTR++ peptide are several tens to hundreds of times above the noise level, demonstrating high spectral quality.: "all y-ion signals for LGGNEQVTR++ peptide are several tens to hundreds of times above the noise level, demonstrating high spectral quality"
- [other] Invoke rawrr::readSpectrum with scan=9594 to extract spectral data via the compiled C# wrapper and RawFileReader API. Parse the returned rawrrSpectrum object to retrieve instrument metadata including resolving power, AGC target, and injection time.: "Invoke rawrr::readSpectrum with scan=9594 to extract spectral data via the compiled C# wrapper and RawFileReader API"
- [results] the C-trap managed to collect the defined 100,000 charges within 2.8 ms, corresponding to only ~5.1% of the maximum injection time of 55 ms: "the C-trap managed to collect the defined 100,000 charges within 2.8 ms, corresponding to only ~5.1% of the maximum injection time of 55 ms"
- [methods] Specifically, `R` functions requesting access to data stored in binary raw files (reader family functions listed in Table 1) invoke compiled `C#` wrapper methods using a system call: "functions requesting access to data stored in binary raw files invoke compiled `C#` wrapper methods using a system call"
- [readme] rawrr wraps the functionality of the RawFileReader .NET assembly.: "rawrr wraps the functionality of the RawFileReader .NET assembly"
- [readme] The package provides access to proprietary Thermo Fisher Scientific Orbitrap instrument data as a stand-alone R package or serves as MsRawFileReaderBackend for the Bioconductor Spectra package.: "The package provides access to proprietary Thermo Fisher Scientific Orbitrap instrument data as a stand-alone R package"
