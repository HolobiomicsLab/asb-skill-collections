---
name: vendor-format-routing-dispatch
description: Use when you have a collection of raw mass spectrometry data files from multiple instrument vendors (Agilent, Bruker, Thermo) and/or mzML exports that need to be converted to a standardized, cross-platform format for downstream software development, AI research, or multi-vendor meta-analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MZA
  - HDF5
  - h5py
  - rhdf5
derived_from:
- doi: 10.1021/acs.jproteome.2c00313
  title: MZA
evidence_spans:
- MZA is a stand-alone and self-contained command-line executable which converts multidimensional mass spectrometry (MS) data
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mza_cq
    doi: 10.1021/acs.jproteome.2c00313
    title: MZA
  dedup_kept_from: coll_mza_cq
schema_version: 0.2.0
---

# vendor-format-routing-dispatch

## Summary

Route multidimensional mass spectrometry data files in proprietary vendor formats (Agilent '.d', Bruker ion mobility 'd', Thermo '.raw', mzML) to their corresponding MZA conversion handlers. This skill identifies the input format via file extension and signature inspection, then dispatches to the appropriate vendor-specific converter to standardize the data into HDF5-based MZA format.

## When to use

You have a collection of raw mass spectrometry data files from multiple instrument vendors (Agilent, Bruker, Thermo) and/or mzML exports that need to be converted to a standardized, cross-platform format for downstream software development, AI research, or multi-vendor meta-analysis. The input files are in their native proprietary formats and have not yet been converted to a common schema.

## When NOT to use

- Input data is already in .mza or standardized HDF5 format — routing is redundant.
- You require vendor-specific metadata or instrument parameters that MZA's simplified schema does not preserve.
- Input file format is not one of the four supported types (Agilent, Bruker IM, Thermo, mzML) — MZA will reject it or fail silently.

## Inputs

- Raw vendor MS data file or directory (Agilent '.d', Bruker ion mobility 'd', Thermo '.raw', or mzML)
- File extension string (e.g., '.d', '.raw', '.mzML') to disambiguate multi-format batches
- Optional intensity threshold (numeric; minimum intensity for signal inclusion)

## Outputs

- .mza file (HDF5-formatted standardized spectrum archive)
- Metadata table (CSV-exportable; one row per spectrum with scan, MS level, retention time, ion mobility, precursor m/z, activation type, etc.)
- Arrays_intensity HDF5 group (1D intensity arrays per spectrum)
- Arrays_mz or Arrays_mzbin HDF5 group (m/z values or ion-mobility bin indices per spectrum)

## How to apply

First, inspect the input file or directory to determine the vendor format by examining the file extension (.d, .raw, or mzML) and optionally validating the format signature. Map the detected format to its corresponding MZA conversion handler: Agilent '.d' (with or without ion mobility) → Agilent handler, Bruker ion mobility 'd' → Bruker handler, Thermo '.raw' → Thermo handler, mzML → mzML handler. Pass the identified file or directory path and the optional -intensityThreshold parameter (default behavior includes all signals; set a minimum intensity cutoff if noise filtering is required) to the MZA command-line executable. The executable will invoke the appropriate vendor-specific data access library (Mass Hunter for Agilent, TDF-SDK for Bruker, MSFileReader for Thermo, or the open mzML parser) and produce an output .mza file containing the spectrum metadata and intensity/m/z arrays stored in HDF5 groups.

## Related tools

- **MZA** (Command-line executable that performs format detection and dispatches each vendor file to its corresponding conversion handler, producing standardized HDF5 output) — https://github.com/PNNL-m-q/mza
- **HDF5** (Underlying storage format for the standardized .mza output files, enabling cross-platform and cross-language access)
- **h5py** (Python library for reading and accessing converted .mza HDF5 files)
- **rhdf5** (R package for reading and accessing converted .mza HDF5 files)

## Examples

```
mza -file test_data -extension .d -intensityThreshold 20
```

## Evaluation signals

- Output .mza file is created and contains valid HDF5 structure with Metadata, Arrays_intensity, and Arrays_mz/Arrays_mzbin groups.
- Metadata table row count matches the number of spectra in the original vendor file; all expected columns (Scan, MSLevel, RetentionTime, IonMobilityTime, etc.) are populated.
- Spectrum count and scan numbers in the metadata correspond to the vendor's native scan indexing; no scans are dropped or duplicated.
- If -intensityThreshold was set, all intensity values in Arrays_intensity groups exceed the specified threshold; signals below threshold are omitted.
- For ion-mobility data (Bruker, Agilent with IM), Arrays_mzbin and Full_mz_array are present; IonMobilityBin and IonMobilityTime columns are non-empty in metadata.

## Limitations

- MZA is a closed-source binary; vendor-specific format dependencies (Agilent Mass Hunter, Bruker TDF-SDK, Thermo MSFileReader) must be pre-installed and licensed separately.
- On Unix-like systems, MZA requires Wine (tested on Ubuntu 22.04.1 with Wine 6.0.3) or Docker; native Linux/macOS executables are not provided.
- The simplified MZA schema may not preserve all vendor-specific metadata fields (e.g., instrument configuration details, raw detector counts); users requiring complete provenance should retain original files.
- For files with very large numbers of spectra, MZA may partition the output into multiple HDF5 groups (e.g., Arrays_intensity/1, Arrays_intensity/2) to optimize read performance; users must handle partition indexes via the MzaPath column.
- CCS calibration coefficients are only included if detected during conversion; not all instrument types or vendor formats will have calibration data available.

## Evidence

- [other] Format identification and handler mapping: "Inspect the input file or directory extension and format signature to identify the vendor format (Agilent '.d', Bruker ion mobility 'd', Thermo '.raw', or mzML). Map the identified format to its"
- [readme] Supported vendor formats: "Input formats supported: * Agilent '.d' (with or without ion mobility) * Bruker ion mobility 'd' (with ion mobility) * Thermo '.raw' * mzML"
- [readme] MZA as command-line dispatcher: "MZA is a stand-alone and self-contained command-line executable which converts multidimensional mass spectrometry (MS) data from files in proprietary vendor formats to the MZA simple data structure"
- [readme] Intensity threshold parameter: "Optional: -intensityThreshold arg: The minimum intensity that must be exceeded for signals to be included in the output mza file."
- [readme] Output structure and standardization: "Once converted, MZA files can be easily accessed from any programming language and operating system using generic HDF5 libraries available (e.g., h5py and rhdf5)."
