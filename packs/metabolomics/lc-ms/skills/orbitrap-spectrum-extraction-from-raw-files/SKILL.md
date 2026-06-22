---
name: orbitrap-spectrum-extraction-from-raw-files
description: Use when you have a Thermo Fisher Orbitrap .raw file and need to retrieve a specific scan's spectral data (m/z and intensity arrays), validate instrument parameters (resolving power, AGC injection time), or assess signal-to-noise characteristics of fragment ions for a known precursor peptide (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - rawrr
  - RawFileReader
  - MsBackendRawFileReader
  - ProteoWizard
  - ThermoRawFileParser
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

# orbitrap-spectrum-extraction-from-raw-files

## Summary

Extract individual MS/MS spectra from Thermo Fisher Scientific Orbitrap .raw files with full instrument metadata (resolving power, AGC target, injection time) and centroided m/z–intensity arrays. This skill enables reproducible access to raw spectral data and quality assessment of peptide fragmentation in bottom-up proteomics workflows.

## When to use

You have a Thermo Fisher Orbitrap .raw file and need to retrieve a specific scan's spectral data (m/z and intensity arrays), validate instrument parameters (resolving power, AGC injection time), or assess signal-to-noise characteristics of fragment ions for a known precursor peptide (e.g., after peptide identification from a database search or from a targeted parallel reaction monitoring experiment).

## When NOT to use

- Input is not a Thermo Fisher Orbitrap .raw file (use ProteoWizard or ThermoRawFileParser for vendor-agnostic conversion to mzML/mzXML first).
- You need statistical or comparative analysis of preprocessed spectra across many samples; use higher-level tools like MSstats or MSnbase instead.
- Windows system without decimal symbol configured as '.' — rawrr will fail to parse numeric data correctly.

## Inputs

- Thermo Fisher Scientific .raw file (e.g., 20181113_010_autoQC01.raw)
- Scan number (integer)
- Known peptide sequence (optional, for fragment ion validation)

## Outputs

- rawrrSpectrum object with centroided m/z and intensity arrays
- Instrument metadata: resolving power (e.g., 30,000 at 200 m/z), AGC target (e.g., 100,000 charges), injection time (e.g., 2.8 ms)
- Fragment ion signal-to-noise ratios
- Spectral quality assessment (boolean: high-quality if major ions >> noise)

## How to apply

Invoke rawrr::readSpectrum() with the path to the .raw file and the target scan number to extract the raw spectrum object via the RawFileReader C# wrapper and API. Parse the returned rawrrSpectrum object to retrieve instrument metadata (resolving power at reference m/z, AGC target in charges, and injection time in milliseconds) from the spectrum header. Extract the centroided m/z and intensity arrays from the spectrum data. For quality assessment, identify fragment ion peaks (e.g., y-ions for a peptide precursor) by matching observed m/z to theoretical values, then calculate signal-to-noise ratio by comparing each peak intensity to the local baseline noise level. Confirm that all major fragment ions exceed tens to hundreds of counts above noise floor, indicating high spectral quality suitable for quantitative proteomics or spectral matching.

## Related tools

- **rawrr** (R package wrapping RawFileReader API; main interface for spectrum extraction and metadata retrieval from .raw files) — https://github.com/fgcz/rawrr
- **RawFileReader** (Thermo Fisher Scientific .NET assembly providing low-level read access to binary .raw file structure via C# wrapper methods invoked by rawrr) — https://github.com/thermofisherlsms/RawFileReader
- **MsBackendRawFileReader** (Alternative MsBackend for Bioconductor Spectra package; integrates rawrr for on-disk spectral data access in Spectra ecosystem) — https://github.com/cpanse/MsBackendRawFileReader
- **ProteoWizard** (Vendor-agnostic alternative for reading .raw files and converting to open formats (mzML); use if rawrr is unavailable or non-Windows platform support needed)
- **ThermoRawFileParser** (Java-based alternative for reading Thermo .raw files on non-Windows platforms; produces mzML output for downstream analysis) — https://github.com/compomics/ThermoRawFileParser

## Examples

```
S <- rawrr::readSpectrum(rawfile = "20181113_010_autoQC01.raw", scan = 9594); str(S[[1]])
```

## Evaluation signals

- rawrrSpectrum object returned without parsing errors; object contains 119+ metadata items including resolving power, AGC target, and injection time fields.
- Instrument metadata values match expected hardware specifications: e.g., resolving power ≥ 30,000 at 200 m/z for Orbitrap, AGC injection time ≤ 55 ms (max).
- Centroided m/z array has expected length (e.g., 50–200 fragment peaks for a doubly-charged peptide) and intensity array is non-empty with positive values.
- Fragment ion m/z values (e.g., y-ions for LGGNEQVTR++) match theoretical values within instrument mass accuracy (typically ≤ 5 ppm for Orbitrap).
- Signal-to-noise ratio for major fragment ions is ≥ 10:1 (tens to hundreds of counts above baseline); no obvious spectral contamination or baseline elevation.

## Limitations

- rawrr is Windows-native; Linux and macOS users may require Mono or Docker, or should use ThermoRawFileParser / ProteoWizard instead.
- Decimal symbol must be configured as '.' on Windows systems, otherwise numeric data parsing will fail silently.
- Only Thermo Fisher Scientific Orbitrap .raw files are supported; other vendor formats (Bruker, Waters, ABB) require alternative tools.
- MsBackendRawFileReader backend for Spectra is still in development (WIP status); use direct rawrr functions for production workflows.
- The skill retrieves individual scans; to extract ion chromatograms or perform multi-scan operations, use readChromatogram() or readIndex() functions separately.

## Evidence

- [other] Scan 9594 was successfully extracted using rawrr::readSpectrum, confirming resolving power of 30,000 at 200 m/z and AGC injection time of 2.8 ms: "Scan 9594 was successfully extracted using rawrr::readSpectrum, confirming resolving power of 30,000 at 200 m/z and AGC injection time of 2.8 ms"
- [intro] rawrr wraps the functionality of the RawFileReader .NET assembly, enabling spectrum extraction via C# wrapper methods: "rawrr wraps the functionality of the RawFileReader .NET assembly"
- [methods] invoke compiled C# wrapper methods using a system call to access binary raw file data: "R functions requesting access to data stored in binary raw files invoke compiled C# wrapper methods using a system call"
- [methods] extracted information is written to temporary location, read back into memory and parsed into R objects: "the extracted information is written to a temporary location on the harddrive, read back into memory and"
- [methods] All spectra were written to file after applying centroiding and lock mass correction: "All spectra were written to file after applying centroiding (c) and lock mass correction"
- [results] 119 data items provided by the API for each scanned spectrum: "the API provides 119 data items for this particular scan"
- [other] all y-ion signals for LGGNEQVTR++ peptide are several tens to hundreds of times above the noise level: "all y-ion signals for LGGNEQVTR++ peptide are several tens to hundreds of times above the noise level"
- [readme] The package provides access to proprietary Thermo Fisher Scientific Orbitrap instrument data as a stand-alone R package: "The package provides access to proprietary Thermo Fisher Scientific Orbitrap instrument data as a stand-alone R package"
- [discussion] On Windows, the decimal symbol has to be configured as a '.': "On Windows, the decimal symbol has to be configured as a '.'"
