---
name: raw-spectral-data-reading
description: Use when you have Thermo Orbitrap .raw files and need to extract specific spectral features (base-peak m/z, intensity values, chromatographic traces, scan-level metadata) for downstream statistical analysis or visualization in R. Use this skill when you want to avoid lossy format conversion (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3945
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - rawrr
  - R
  - RawFileReader
  - MsBackendRawFileReader
  - Spectra
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1101/2020.10.30.362533
  title: rawrr
- doi: 10.1021/acs.jproteome.0c00866
  title: ''
evidence_spans:
- The `rawrr` executable will run out of the box
- '`R` functions requesting access to data stored in binary raw files (reader family functions listed in Table 1) invoke compiled `C#` wrapper methods'
- Calling a wrapper method typically results in the execution of methods defined in the `RawFileReader` dynamic link library provided by Thermo Fisher Scientific
- methods defined in the `RawFileReader` dynamic link library provided by Thermo Fisher Scientific
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_rawrr_cq
    doi: 10.1101/2020.10.30.362533
    title: rawrr
  dedup_kept_from: coll_rawrr_cq
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

# raw-spectral-data-reading

## Summary

Direct programmatic access to spectral attributes (m/z, intensity, retention time, scan metadata) from proprietary Thermo Fisher Scientific .raw binary files without conversion to exchange formats. Enables modular end-to-end proteomics analysis pipelines in R by bridging the gap between instrument data and statistical analysis environments.

## When to use

You have Thermo Orbitrap .raw files and need to extract specific spectral features (base-peak m/z, intensity values, chromatographic traces, scan-level metadata) for downstream statistical analysis or visualization in R. Use this skill when you want to avoid lossy format conversion (e.g., to mzML) and require direct, programmatic access to binary spectral data with subsetting and filtering capabilities.

## When NOT to use

- Input data is already in an open exchange format (mzML, mzXML, netCDF). Use format-agnostic libraries like MSnbase or Spectra instead.
- You need cross-platform vendor-agnostic raw data reading (e.g., Waters, Bruker, Agilent). rawrr is Thermo-specific.
- Your workflow is already embedded in specialized tools (MaxQuant, Skyline) that handle raw file parsing internally.

## Inputs

- Thermo Fisher Scientific .raw file (binary Orbitrap instrument data)
- scan index (data.frame from readIndex())
- scan number(s) or scan range (integer vector)

## Outputs

- rawrrSpectrum objects (mass spectrum representations with m/z, intensity, metadata)
- rawrrChromatogramSet objects (mass chromatogram traces)
- data.frame with extracted spectral attributes (scan index, base-peak m/z, intensity, retention time)
- list object from readFileHeader() containing instrument and acquisition metadata

## How to apply

Install the rawrr executable using rawrr::installRawrrExe(), then read the file header with readFileHeader() to confirm file structure. Generate a scan index using readIndex() to retrieve all scans as a data frame. Filter the index to specific MS levels (e.g., ms_level==1 for MS1-only analysis) or scan types (e.g., FTMS Full ms for intact peptides). Iterate through filtered scan numbers, calling readSpectrum() on each to extract rawrrSpectrum objects. Extract desired spectral attributes using accessor functions and subsetting operators ($, [[) to obtain m/z and intensity vectors, then aggregate into tabular format (data.frame). Optionally use readChromatogram() for XIC/TIC traces and extract retention times at chromatogram peak maxima.

## Related tools

- **rawrr** (Core R package wrapping RawFileReader .NET assembly; provides reader family functions (readFileHeader, readIndex, readSpectrum, readChromatogram) and spectral data objects (rawrrSpectrum, rawrrChromatogramSet)) — https://github.com/fgcz/rawrr
- **RawFileReader** (Vendor-provided .NET assembly from Thermo Fisher Scientific; implements low-level binary .raw file parsing that rawrr wraps) — https://github.com/thermofisherlsms/RawFileReader
- **MsBackendRawFileReader** (Optional integration layer; serves as MsBackend for Bioconductor Spectra package to provide unified spectral data interface) — https://github.com/fgcz/MsBackendRawFileReader
- **Spectra** (Optional downstream integration; unified R interface for mass spectrometry spectral data with pluggable backends (including MsBackendRawFileReader)) — https://bioconductor.org/packages/Spectra/

## Examples

```
library(rawrr); rawrr::installRawrrExe(); idx <- readIndex('20181113_010_autoQC01.raw'); idx_ms1 <- subset(idx, ms_level==1); spec <- readSpectrum('20181113_010_autoQC01.raw', scan=idx_ms1$scan[1]); bp_mz <- spec$mz[which.max(spec$intensity)]; bp_int <- max(spec$intensity)
```

## Evaluation signals

- Returned rawrrSpectrum object contains non-empty m/z and intensity vectors with matching lengths
- Extracted base-peak m/z corresponds to the m/z position with maximum intensity in the spectrum
- Scan index filtering (e.g., ms_level==1) reduces total scan count as expected; all returned scans match the filter criterion
- Retention times extracted from chromatogram objects are monotonically increasing (if single LC run) and within instrument acquisition window (e.g., 0–55 min for example run)
- File header metadata (instrument type, number of scans, time range) matches raw file properties reported by vendor software

## Limitations

- Requires Windows, Linux, or macOS with .NET/Mono runtime; does not work on architectures without .NET Framework support
- rawrr uses file I/O to communicate with C# wrapper methods via system calls, which may introduce latency for large-scale batch processing of thousands of scans
- Binary .raw format is proprietary to Thermo Fisher Scientific; this skill cannot read Bruker, Waters, or Agilent raw files
- MsBackendRawFileReader integration with Bioconductor Spectra package is noted as 'WIP' (work-in-progress) in the repository status badge

## Evidence

- [intro] Direct access to spectral data and motivation: "rawrr utilizes a vendor-provided API named RawFileReader to access spectral data logged in proprietary Thermo Fisher Scientific raw files"
- [intro] Gap that rawrr fills in R proteomics ecosystem: "We strongly believe that a library providing raw data reading would finally close the gap and facilitate modular end-to-end analysis pipeline development in R"
- [methods] Core workflow: install, load, index, filter, iterate, extract: "R functions requesting access to data stored in binary raw files (reader family functions listed in Table 1) invoke compiled C# wrapper methods using a system call"
- [results] Practical readSpectrum and readIndex usage: "Individual scans or scan collections (sets) can be read by the function readSpectrum(). By using the readIndex() function a data.frame that indexes all scans found in a raw file is returned"
- [results] Spectral object representation and accessor methods: "rawrr provides accessor functions and subsetting operators ($, [[) to programmatically extract spectral attributes from rawrrSpectrum objects"
- [results] Filtering by MS level for targeted extraction: "using only MS1-level scans"
- [discussion] Advantage: no lossy format conversion: "provides direct access to spectral data stored in Thermo Fisher Scientific raw-formatted binary files, thereby eliminating the need for unfavorable conversion to exchange formats"
- [readme] MsBackendRawFileReader integration goal: "Provides an alternative MsBackend to Spectra through the rawrr package. Ultimately this backend will allow direct access to spectral data logged in ThermoFischer Scientific .raw files"
