---
name: raw-file-data-extraction-via-api
description: Use when you have a Thermo Fisher Scientific .raw file (e.g., Q Exactive
  HF, Orbitrap) and need to extract specific spectral scans, chromatographic traces,
  scan-level metadata, or file-level headers programmatically—e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - rawrr
  - RawFileReader
  - MsBackendRawFileReader
  - Spectra
  - rawDiag
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

# raw-file-data-extraction-via-api

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Extract spectral, chromatographic, and metadata records from proprietary Thermo Fisher Scientific Orbitrap .raw files using the rawrr R package's programmatic API, which wraps the RawFileReader .NET assembly. This skill enables modular, reproducible access to raw mass spectrometry data for quality control, method optimization, and end-to-end proteomics pipelines in R without relying on GUI software.

## When to use

You have a Thermo Fisher Scientific .raw file (e.g., Q Exactive HF, Orbitrap) and need to extract specific spectral scans, chromatographic traces, scan-level metadata, or file-level headers programmatically—e.g., to validate PRM cycle spacing, inspect scan indices for targeted acquisitions (fixed precursor m/z and HCD energy), or build a quality control report without using MaxQuant or Skyline. This is particularly valuable when you need to filter scans by acquisition type (e.g., 'FTMS + c NSI Full ms2') or compute inter-scan deltas to verify instrument method fidelity.

## When NOT to use

- Input file is not in Thermo Fisher Scientific .raw format (e.g., mzML, mzXML, NetCDF)—use ProteoWizard, pyteomics, or OpenMS instead.
- You only need high-level statistical analysis of already-processed peptide or protein abundance data—use MSstats, MSqRob, or MSnbase on feature tables rather than raw spectra.
- You require real-time streaming access to instrument data during acquisition, or need to write modified data back to .raw files—rawrr is read-only and post-acquisition.

## Inputs

- Thermo Fisher Scientific .raw file (binary format; e.g., 20181113_010_autoQC01.raw)
- scan type filter string (e.g., 'FTMS + c NSI Full ms2 487.2567@hcd27.00 [100.0000-1015.0000]')
- scan numbers or m/z values with tolerance (ppm or Da) for chromatogram extraction
- optional: acquisition filter pattern (e.g., 'ms' for MS1 scans)

## Outputs

- File header object with instrument metadata (scan count, retention time range, instrument model, etc.)
- Scan index data frame with scan number, scan type, retention time, precursor m/z, and collision energy
- Spectrum objects (list or data frame) containing m/z array, intensity array, and scan-level metadata for selected scans
- Chromatogram traces (intensity vs. retention time or scan number) for TIC or extracted ion chromatograms (XIC)
- Summary statistics (e.g., inter-scan delta values, PRM cycle validation pass/fail status)

## How to apply

Install the rawrr R package and its runtime dependencies (RawFileReader .NET assembly and Mono/.NET runtime). Call rawrr::readFileHeader() to retrieve metadata such as scan count, retention time range, and instrument configuration. Use rawrr::readIndex() to obtain a complete scan index table, then filter rows by scanType (e.g., matching 'FTMS + c NSI Full ms2 487.2567@hcd27.00') to isolate scans of interest. Extract scan numbers and compute differences between consecutive indices to validate cycle spacing (e.g., confirm delta = 22 for one complete PRM cycle). For individual spectra, call rawrr::readSpectrum() with selected scan numbers; for chromatograms, use rawrr::readChromatogram() with type='tic' for total ion current or type='xic' with mass tolerance and m/z range for extracted ion chromatograms. Validate results by confirming scan counts, checking that all delta values match the expected cycle length, and verifying that m/z and intensity ranges are physically plausible for the instrument and acquisition method.

## Related tools

- **rawrr** (Core R package providing high-level functions (readFileHeader, readIndex, readSpectrum, readChromatogram) to invoke RawFileReader .NET methods and parse results into R objects) — https://github.com/fgcz/rawrr
- **RawFileReader** (.NET assembly (C# DLLs from ThermoFisher.CommonCore) that performs low-level binary parsing of Thermo .raw files; wrapped by rawrr) — https://github.com/thermofisherlsms/RawFileReader
- **MsBackendRawFileReader** (Optional Bioconductor backend that integrates rawrr with the Spectra package for unified high-level spectral data access) — https://github.com/cpanse/MsBackendRawFileReader
- **Spectra** (Bioconductor package providing a modular interface for spectral data; can use rawrr as a backend for direct .raw file access) — https://bioconductor.org/packages/Spectra/
- **rawDiag** (R package for LC-MS method optimization and quality control; uses rawrr for fast multiplatform reading and ggplot2 for visualization) — https://github.com/fgcz/rawDiag

## Examples

```
rawrr::readIndex(rawfile = '20181113_010_autoQC01.raw') |> subset(scanType == 'FTMS + c NSI Full ms2 487.2567@hcd27.00 [100.0000-1015.0000]') |> (function(x) { diff(x$scan) })()
```

## Evaluation signals

- File header retrieval succeeds without errors and reports plausible values (e.g., scan count > 0, retention time range covers the run duration, instrument model matches expected hardware).
- Scan index table is complete and filterable: all rows have non-null scanType, scan number, and retention time; filter for a specific precursor m/z and HCD energy yields at least one row.
- For PRM validation: computed inter-scan deltas (difference between consecutive scan numbers in the filtered index) are uniform and match the expected cycle length (e.g., all deltas = 22 scans); count of PRM scans is consistent with the run time and cycle time.
- Spectrum extraction returns non-empty m/z and intensity arrays with expected length (typically 102–2,000 peaks depending on mass range); precursor m/z ± 0.01 Da matches the filter specification.
- Chromatogram data shows monotonically increasing retention times and non-negative intensities; XIC at the expected m/z (within stated tolerance) exhibits a peak at the retention time of the target peptide.

## Limitations

- rawrr requires the .NET runtime (Mono on Linux/macOS, .NET Framework or .NET Core on Windows) to be pre-installed; .raw file reading is not supported in pure R and relies on system calls to compiled RawFileReader assemblies.
- On Windows systems, the decimal symbol must be configured as '.' (period), not ',' (comma), for proper numeric data extraction; failures may occur silently if locale settings are incorrect.
- rawrr is read-only; it cannot write or modify .raw files. To convert or export data, you must parse the extracted objects and write to a text or standard format (e.g., mzML via ProteoWizard).
- Access to proprietary Thermo Fisher Scientific data formats depends on the version and availability of RawFileReader assemblies; older .raw file formats or future instrument models may not be fully supported.
- API provides 119 data items per scan, but not all items are populated for all scan types; e.g., MS1 scans lack precursor m/z, and low-abundance spectra may have no intensity values above noise threshold.

## Evidence

- [readme] The package provides access to proprietary Thermo Fisher Scientific Orbitrap instrument data as a stand-alone R package or serves as MsRawFileReaderBackend for the Bioconductor Spectra package: "The package provides access to proprietary Thermo Fisher Scientific Orbitrap instrument data as a stand-alone R package or serves as MsRawFileReaderBackend for the Bioconductor Spectra package"
- [readme] rawrr wraps the functionality of the RawFileReader .NET assembly: "rawrr wraps the functionality of the RawFileReader .NET assembly"
- [methods] Specifically, `R` functions requesting access to data stored in binary raw files (reader family functions listed in Table 1) invoke compiled `C#` wrapper methods using a system call: "R functions requesting access to data stored in binary raw files invoke compiled C# wrapper methods using a system call"
- [methods] In order to return extracted data back to the `R` layer we use file I/O. More specifically, the extracted information is written to a temporary location on the harddrive, read back into memory and parsed into R objects: "extracted information is written to a temporary location, read back into memory and parsed into R objects"
- [methods] The example file `20181113_010_autoQC01.raw` used throughout this manuscript contains Fourier-transformed Orbitrap spectra (FTMS) recorded on a Thermo Fisher Scientific Q Exactive HF: "example file contains Fourier-transformed Orbitrap spectra (FTMS) recorded on a Thermo Fisher Scientific Q Exactive HF"
- [other] Call rawrr::readIndex() on the 20181113_010_autoQC01.raw file to retrieve the complete scan index table: "Call rawrr::readIndex() on the raw file to retrieve the complete scan index table"
- [other] Filter the index data frame to retain only rows where scanType matches the PRM acquisition method pattern (e.g., 'FTMS + c NSI Full ms2' with a fixed precursor m/z and HCD energy): "Filter the index data frame to retain only rows where scanType matches the PRM acquisition method pattern (e.g., 'FTMS + c NSI Full ms2' with a fixed precursor m/z and HCD energy)"
- [other] Extract the scan numbers from the filtered rows and compute the difference between consecutive scan indices: "Extract the scan numbers from the filtered rows and compute the difference between consecutive scan indices"
- [results] The corresponding R markdown file is part of the rawrr package and demonstrates readFileHeader, readSpectrum, readChromatogram, and readIndex workflows: "rawrr::readIndex(rawfile = rawfile) |> subset(scanType == ...)"
- [intro] We strongly believe that a library providing raw data reading would finally close the gap and facilitate modular end-to-end analysis pipeline development in R: "a library providing raw data reading would facilitate modular end-to-end analysis pipeline development in R"
- [discussion] On Windows, the decimal symbol has to be configured as a '.'!: "On Windows, the decimal symbol has to be configured as a '.'"
- [results] In total, the API provides 119 data items for this particular scan: "the API provides 119 data items for this particular scan"
