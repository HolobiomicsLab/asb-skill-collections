---
name: rawrr-spectral-data-retrieval
description: Use when you have Thermo Orbitrap .raw files and need to access raw spectral
  data (individual MS1 or MS2 scans, base-peak values, chromatogram traces, retention
  times, or scan-level metadata) for custom analysis, visualization, or integration
  into an R-based pipeline.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - rawrr
  - RawFileReader
  - R
  - MsBackendRawFileReader
  - Spectra
  - tartare
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1101/2020.10.30.362533
  title: rawrr
- doi: 10.1021/acs.jproteome.0c00866
  title: ''
evidence_spans:
- Our `.NET 8.0` [@dotnet] precompiled wrapper methods are bundled, including the
  runtime, in the `r BiocStyle::Biocpkg('rawrr')` executable file and shipped with
  the released `R` package.
- R` functions requesting access to data stored in binary raw files (reader family
  functions listed in Table 1) invoke compiled `C#` wrapper methods
- Calling a wrapper method typically results in the execution of methods defined in
  the `RawFileReader` dynamic link library provided by Thermo Fisher Scientific.
- invoke compiled `C#` wrapper methods using a system call. Calling a wrapper method
  typically results in the execution of methods defined in the `RawFileReader` dynamic
  link library provided by Thermo
- Our implementation consists of two language layers, the top `R` layer and the hidden
  `C#` layer.
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# rawrr-spectral-data-retrieval

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Programmatically extract spectral data (m/z, intensity, retention time, scan metadata) directly from Thermo Fisher Scientific Orbitrap .raw files using the rawrr R package, without requiring external file conversion. This enables modular end-to-end proteomics pipelines in R that operate on vendor-native binary data.

## When to use

You have Thermo Orbitrap .raw files and need to access raw spectral data (individual MS1 or MS2 scans, base-peak values, chromatogram traces, retention times, or scan-level metadata) for custom analysis, visualization, or integration into an R-based pipeline. Use this when external preprocessing tools (MaxQuant, Skyline) are not appropriate, or when you need programmatic access to scan-level details for quality control, method optimization, or modular downstream processing.

## When NOT to use

- Input data is already in an open exchange format (mzML, mzXML, NetCDF); use format-agnostic tools like MSnbase or Spectra instead.
- You only need high-level statistical analysis (e.g., differential abundance, pathway analysis); use MaxQuant → MSstats or MSqRob rather than low-level spectral access.
- Your .raw files are from non-Thermo instruments (e.g., Waters, Bruker, Agilent); rawrr only supports Orbitrap instruments and the RawFileReader API.

## Inputs

- Thermo Fisher Scientific Orbitrap .raw file (binary)
- Scan index data.frame (output from readIndex(); optional pre-filtered subset)
- Vector of scan numbers or MS level filter criteria

## Outputs

- rawrrSpectrum or rawrrSpectrumSet R object(s) containing m/z, intensity, retention time, scan metadata
- Tabular data (data.frame or CSV) with columns: scan_number, retention_time, base_peak_mz, base_peak_intensity, MS_level
- rawrrChromatogram object (if chromatogram data is extracted)

## How to apply

First, install the rawrr R package and its compiled executable wrapper (rawrr::installRawrrExe()), which wraps the vendor RawFileReader .NET assembly and manages inter-process communication via temporary file I/O. Load the .raw file path and call readIndex() to generate a scan-level data.frame that indexes all scans with their MS level, scan type, retention time, and other metadata. Subset this index by MS level (ms == 1 for precursor scans, ms == 2 for fragment scans) or scan type as needed. Then iterate over scan numbers of interest and call readSpectrum() on each to retrieve individual rawrrSpectrum objects; extract desired properties (m/z, intensity, base-peak) using accessor functions. Aggregate the results into a table and export. The rationale is that rawrr avoids lossy conversion to exchange formats (mzML) and preserves full access to vendor-specific metadata and high-resolution data.

## Related tools

- **RawFileReader** (Vendor-provided .NET assembly that implements low-level binary .raw file parsing; wrapped by rawrr via C# interop and system calls) — https://github.com/thermofisherlsms/RawFileReader
- **rawrr** (R package that wraps RawFileReader, provides high-level accessor functions (readIndex, readSpectrum, readChromatogram, readFileHeader), and manages temporary file I/O for data exchange) — https://github.com/fgcz/rawrr
- **MsBackendRawFileReader** (Bioconductor backend that integrates rawrr with the Spectra package, enabling on-disk spectral data access via standardized MsBackend interface) — https://github.com/cpanse/MsBackendRawFileReader
- **Spectra** (Bioconductor package providing unified S4 classes and methods for spectral data; can use MsBackendRawFileReader to read from .raw files) — https://bioconductor.org/packages/Spectra/
- **tartare** (Bioconductor ExperimentData package providing test .raw files for rawrr development and validation)

## Examples

```
rawrr::installRawrrExe(); idx <- rawrr::readIndex(rawrr::sampleFilePath()); ms1_idx <- subset(idx, ms == 1); sp <- rawrr::readSpectrum(rawrr::sampleFilePath(), scan=ms1_idx$scan[1]); bp_mz <- sp@mz[which.max(sp@intensity)]; bp_int <- max(sp@intensity)
```

## Evaluation signals

- Scan index data.frame contains expected number of rows (one per scan) with non-null columns: ms (1 or 2), rt (retention time in minutes), and scanType; verify row count matches instrument log.
- readSpectrum() returns valid rawrrSpectrum objects with m/z and intensity vectors of equal length; check object structure using str() or summary().
- Base-peak extraction yields m/z and intensity pairs where intensity > 0 and m/z is within instrument mass range (e.g., 100–2000 m/z for typical proteomics); spot-check against raw vendor software or alternative parsers.
- Aggregate table has no missing values for filtered scans; retention times increase monotonically across scan sequence; CSV writes successfully with correct delimiter and encoding.
- Extracted chromatogram data (if used) shows expected retention time distribution and peak shapes consistent with LC method parameters (e.g., peak width, gradient length).

## Limitations

- rawrr is Windows/Linux/macOS compatible only on systems with .NET runtime installed; requires explicit executable installation via rawrr::installRawrrExe().
- Inter-process communication via temporary file I/O can incur I/O overhead for very large numbers of scans; batch processing recommended over single-scan iteration in performance-critical pipelines.
- rawrr provides access to Orbitrap instruments only (Thermo Fisher Scientific); not compatible with Waters, Bruker, Agilent, or other vendor raw formats.
- Future alignment with R for Mass Spectrometry initiative (exchangeable backends) is planned but not yet fully implemented, limiting long-term stability guarantees.
- Big computational proteomics capabilities in R are still being developed; current rawrr is suitable for method optimization and quality control but not yet optimized for large-scale repository-scale reanalysis.

## Evidence

- [other] rawrr provides readIndex() to generate a scan index data.frame, readSpectrum() to read spectral data, and accessor functions to programmatically extract scan properties: "rawrr provides readIndex() to generate a scan index data.frame, readSpectrum() to read spectral data, and accessor functions to programmatically extract scan properties"
- [methods] R functions requesting access to data stored in binary raw files invoke compiled C# wrapper methods using a system call. Extracted information is written to a temporary location on harddrive, read back into memory and parsed into R objects: "R functions requesting access to data stored in binary raw files (reader family functions listed in Table 1) invoke compiled C# wrapper methods using a system call. [...] In order to return extracted"
- [results] By using the readIndex() function a data.frame that indexes all scans found in a raw file is returned: "By using the `readIndex()` function a `data.frame` that indexes all scans found in a raw file is returned"
- [results] Individual scans or scan collections (sets) can be read by the function readSpectrum(): "Individual scans or scan collections (sets) can be read by the function `readSpectrum()`"
- [intro] A library providing raw data reading would finally close the gap and facilitate modular end-to-end analysis pipeline development in R: "We strongly believe that a library providing raw data reading would finally close the gap and facilitate modular end-to-end analysis pipeline development in R"
- [readme] rawrr wraps the functionality of the RawFileReader .NET assembly. Provides access to proprietary Thermo Fisher Scientific Orbitrap instrument data: "The package provides access to proprietary Thermo Fisher Scientific Orbitrap instrument data as a stand-alone R package or serves as MsRawFileReaderBackend for the Bioconductor Spectra package. rawrr"
- [results] using only MS1-level scans: "Filter MS scans using ms filter; using only MS1-level scans"
