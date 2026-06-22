---
name: spectral-quality-assurance-proteomics
description: Use when when you have extracted a raw Orbitrap scan from a .raw file and need to verify that the instrument operated within expected parameters and that observed peptide fragment ions rise substantially above noise—i.
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
  - MsBackendRawFileReader
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

# Spectral Quality Assurance in Proteomics

## Summary

Validates Orbitrap mass spectrometry spectral data by confirming instrument metadata (resolving power, AGC injection time) and quantifying signal-to-noise ratios for fragment ions relative to baseline noise. Essential for ensuring high-quality peptide fragmentation spectra suitable for identification and quantification workflows.

## When to use

When you have extracted a raw Orbitrap scan from a .raw file and need to verify that the instrument operated within expected parameters and that observed peptide fragment ions rise substantially above noise—i.e., when assessing whether a spectrum meets minimum quality thresholds before downstream identification or quantification (e.g., scan 9594 in the MassIVE dataset MSV000086542).

## When NOT to use

- Input spectrum is already preprocessed into a feature table or peptide-spectrum match score; quality assurance requires raw m/z and intensity data.
- The .raw file format is not Thermo Orbitrap (e.g., mzML, mzXML, Bruker .d); rawrr is specific to ThermoFisher proprietary formats.
- Instrument metadata is unavailable or the spectrum is from an instrument without documented resolving power specifications (e.g., low-resolution ion trap with broad mass accuracy).

## Inputs

- Thermo Fisher Scientific .raw file (binary Orbitrap data file)
- scan number (integer, e.g., 9594)
- peptide sequence (string) or theoretical fragment m/z list (numeric array)

## Outputs

- rawrrSpectrum object (centroided m/z and intensity arrays, instrument metadata)
- instrument metadata dictionary (resolving power, AGC target, injection time in ms)
- fragment ion signal-to-noise ratios (numeric vector per ion)
- quality pass/fail classification (boolean or categorical)

## How to apply

First, extract the target scan using rawrr::readSpectrum() and parse the returned rawrrSpectrum object to retrieve instrument metadata including resolving power (e.g., 30,000 at 200 m/z), AGC target (e.g., 100,000 charges), and actual injection time (e.g., 2.8 ms). Cross-reference the injection time against the maximum allowed (e.g., 55 ms) to confirm AGC was not saturated. Next, extract m/z and intensity arrays from the centroided spectrum. Identify fragment ions (e.g., y-ions for a known peptide precursor) by matching observed m/z to theoretical values within tolerance. For each fragment, calculate the signal-to-noise ratio by comparing peak intensity to the local baseline noise floor. Reject the scan if any expected fragment falls below tens to hundreds of counts above noise, or if metadata (resolving power, AGC time) deviates significantly from instrument specifications. Accept the scan if all major fragments are several tens to hundreds of times above noise level.

## Related tools

- **rawrr** (R package providing direct access to Orbitrap .raw file data; invokes readSpectrum() to extract scan data and instrument metadata via the RawFileReader C# wrapper) — https://github.com/fgcz/rawrr
- **RawFileReader** (.NET assembly wrapping Thermo Fisher Scientific proprietary APIs; underlying engine for rawrr's spectrum and metadata extraction) — https://github.com/thermofisherlsms/RawFileReader
- **rawDiag** (Companion R package for LC-MS method optimization and diagnostic visualization of raw file metadata and QC metrics; complements rawrr for quality assessment workflows) — https://github.com/fgcz/rawDiag
- **MsBackendRawFileReader** (Bioconductor-compatible backend for the Spectra package; integrates rawrr into modular end-to-end analysis pipelines for on-disk access to Orbitrap data) — https://github.com/cpanse/MsBackendRawFileReader

## Examples

```
S <- rawrr::readSpectrum(rawfile = '20181113_010_autoQC01.raw', scan = 9594); S[[1]]$centroid.mZ; S[[1]]$centroid.intensity; S[[1]]$`MS order`; S[[1]]$`Orbitrap Resolution`
```

## Evaluation signals

- Instrument metadata (resolving power, AGC target, injection time) match the expected values documented for the instrument and are consistent with the file header.
- Actual AGC injection time does not exceed the maximum allowed time (e.g., < 55 ms for a Q Exactive HF); verify that actual collection time is a reasonable fraction of the maximum (e.g., 2.8 ms ≈ 5% of 55 ms).
- All expected fragment ions (y-ions, b-ions) for the known peptide precursor are present in the m/z array within mass tolerance (typically ≤ 5 ppm for high-resolution Orbitrap).
- Signal-to-noise ratios for all major fragments exceed a minimum threshold (tens to hundreds of counts above local baseline noise); no dominant fragments fall below this threshold.
- Centroiding was applied to the spectrum (confirmed via spectrum type in filter metadata, e.g., 'FTMS + c NSI'), and the intensity array contains distinct peaks rather than continuous profile data.

## Limitations

- rawrr requires the RawFileReader .NET assembly and a .NET runtime (mono, .NET Core, or .NET Framework); Windows systems require decimal symbol configuration as '.' for proper data extraction.
- The RawFileReader API is proprietary to Thermo Fisher Scientific; rawrr cannot read non-Orbitrap formats (Bruker, Waters, etc.).
- Noise floor estimation relies on local baseline calculation, which may be unreliable in spectra with very high dynamic range or dense precursor ion regions; alternative noise models may be needed for extreme cases.
- The skill assesses individual scan quality but does not account for retention time drift, method suitability, or chromatographic peak shape; integration into a full QC workflow (e.g., rawDiag) is recommended.
- MsBackendRawFileReader backend for Spectra integration was in work-in-progress status at the time of article publication; full production-ready interoperability may require newer package versions.

## Evidence

- [other] Scan 9594 was successfully extracted using rawrr::readSpectrum, confirming resolving power of 30,000 at 200 m/z and AGC injection time of 2.8 ms (~5% of maximum 55 ms); all y-ion signals for LGGNEQVTR++ peptide are several tens to hundreds of times above the noise level, demonstrating high spectral quality.: "Scan 9594 was successfully extracted using rawrr::readSpectrum, confirming resolving power of 30,000 at 200 m/z and AGC injection time of 2.8 ms (~5% of maximum 55 ms); all y-ion signals for"
- [methods] The example file `20181113_010_autoQC01.raw` used throughout this manuscript contains Fourier-transformed Orbitrap spectra (FTMS) recorded on a Thermo Fisher Scientific Q Exactive HF: "The example file `20181113_010_autoQC01.raw` used throughout this manuscript contains Fourier-transformed Orbitrap spectra (FTMS) recorded on a Thermo Fisher Scientific Q Exactive HF"
- [methods] Specifically, `R` functions requesting access to data stored in binary raw files (reader family functions listed in Table 1) invoke compiled `C#` wrapper methods using a system call: "`R` functions requesting access to data stored in binary raw files invoke compiled `C#` wrapper methods using a system call"
- [results] the C-trap managed to collect the defined 100,000 charges within 2.8 ms, corresponding to only ~`r format((2.8/55)*100, digits = 1)`% of the maximum injection time of 55 ms: "the C-trap managed to collect the defined 100,000 charges within 2.8 ms, corresponding to only ~5.1% of the maximum injection time of 55 ms"
- [results] In total, the API provides `r length(S[[1]])` data items for this particular scan: "the API provides 119 data items for the scanned spectrum"
- [readme] rawrr wraps the functionality of the RawFileReader .NET assembly: "rawrr wraps the functionality of the RawFileReader .NET assembly"
- [intro] A gap exists in R ecosystem for modular end-to-end analysis pipelines that can directly read raw mass spectrometry data: "a library providing raw data reading would finally close the gap and facilitate modular end-to-end analysis pipeline development in R"
- [discussion] On Windows, the decimal symbol has to be configured as a '.'!: "On Windows, the decimal symbol has to be configured as a '.'"
