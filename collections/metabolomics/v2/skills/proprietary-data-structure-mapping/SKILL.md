---
name: proprietary-data-structure-mapping
description: Use when you have received raw mass spectrometry data in one of four proprietary vendor formats (Agilent '.d', Bruker ion mobility 'd', Thermo '.raw', or mzML) and need to convert it to a cross-platform, cross-language accessible format.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
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

# proprietary-data-structure-mapping

## Summary

Map vendor-specific mass spectrometry file formats (Agilent '.d', Bruker ion mobility 'd', Thermo '.raw', mzML) to their corresponding MZA conversion handlers by inspecting file extension and format signature. This skill enables routing of heterogeneous multidimensional MS data to appropriate conversion pipelines for standardization into HDF5-based MZA simple data structure.

## When to use

You have received raw mass spectrometry data in one of four proprietary vendor formats (Agilent '.d', Bruker ion mobility 'd', Thermo '.raw', or mzML) and need to convert it to a cross-platform, cross-language accessible format. This skill is required when your downstream analysis requires unified access to multidimensional MS data (LC, IM, and DIA fragmentation) regardless of vendor source.

## When NOT to use

- Input data is already in mzML or another open, non-proprietary format and your workflow already supports generic HDF5 libraries—use MZA only if unified access across vendor formats is the goal.
- You need vendor-specific metadata or activation types (e.g., CID, HCD, ETD, UVPD, EThcD) not supported by the MZA metadata schema.
- Your instrument produces ion mobility data from vendors not in the four supported formats (Agilent, Bruker, Thermo); MZA will not recognize the format.

## Inputs

- Raw vendor MS file (Agilent '.d' directory, Bruker ion mobility 'd', Thermo '.raw', or mzML file)
- File path or directory path (for batch conversion)
- File extension (when converting multiple files: .d, .raw, .mzML)
- Intensity threshold parameter (optional; numeric, minimum intensity to include in output)

## Outputs

- MZA file (HDF5-based structure with metadata table and jagged arrays)
- Handler reference (conversion pipeline identifier)
- Conversion parameters (set of parameters suitable for MZA command-line executable)

## How to apply

Inspect the input file or directory path and examine its file extension (.d, .raw, .mzML) and, if necessary, internal format signature to identify the vendor format. Map the identified format to its corresponding MZA conversion handler: Agilent '.d' (with or without ion mobility), Bruker ion mobility 'd' (with ion mobility), Thermo '.raw', or mzML. Apply optional parameters such as -intensityThreshold (default: include all signals; typical threshold 20 for noise rejection). Invoke the MZA command-line executable with the identified handler and conversion parameters. The routing decision is deterministic based on file extension; the rationale is that HDF5 generic libraries (h5py, rhdf5) can then uniformly access the converted multidimensional spectra across any programming language or operating system.

## Related tools

- **MZA** (Command-line executable that performs vendor format detection and routes each file to its corresponding conversion handler, outputting HDF5-based MZA simple data structure) — https://github.com/PNNL-m-q/mza
- **HDF5** (Underlying data storage format used by MZA to store converted multidimensional spectra and metadata in a standardized, cross-platform structure)
- **h5py** (Python library for reading and accessing MZA files after conversion; generic HDF5 interface independent of vendor format)
- **rhdf5** (R package for reading and accessing MZA files after conversion; generic HDF5 interface independent of vendor format)

## Examples

```
mza -file test_data -extension .d -intensityThreshold 20
```

## Evaluation signals

- File extension or format signature correctly identifies vendor (Agilent, Bruker, Thermo, or mzML); mismatch prevents handler routing.
- MZA executable successfully invokes the correct conversion handler without errors; routing to wrong handler causes format parsing failure.
- Output HDF5 file contains expected structure: metadata table with columns (Scan, MzaPath, MSLevel, Polarity, Activation, etc.) and jagged arrays (Arrays_intensity, Arrays_mz or Arrays_mzbin for IM data).
- Intensity values in output arrays meet or exceed the -intensityThreshold parameter; zero-intensity values are omitted as specified.
- For IM data, CCS calibration coefficients (if detected: CCScalDT, CCScalSLIM, CCScalTIMS) are present in output HDF5 dataset.

## Limitations

- MZA is a Windows executable; Unix-like systems require Wine compatibility layer (tested on Ubuntu 22.04.1) or Docker container, adding deployment overhead.
- Closed-source binary due to vendor library restrictions (Agilent Mass Hunter, Thermo MSFileReader, Bruker TDF-SDK); reproducibility and debugging are constrained.
- Input format support is limited to four vendor formats; data from other MS instruments cannot be routed through MZA.
- Large files with many spectra may be partitioned into multiple HDF5 groups to maintain read performance; MzaPath column indicates partition index, requiring awareness during downstream access.
- Software binary depends on proprietary vendor libraries; users must comply with license agreements of Agilent, Thermo Fisher, and Bruker libraries.

## Evidence

- [intro] MZA is a command-line executable that converts multidimensional mass spectrometry data from four proprietary vendor formats—Agilent '.d', Bruker ion mobility 'd', Thermo '.raw', and mzML—to the MZA simple data structure based on HDF5 format.: "MZA is a stand-alone and self-contained command-line executable which converts multidimensional mass spectrometry (MS) data from files in proprietary vendor formats to the MZA simple data structure"
- [other] Identify vendor format by inspecting file extension and format signature, then map to corresponding handler.: "Inspect the input file or directory extension and format signature to identify the vendor format (Agilent '.d', Bruker ion mobility 'd', Thermo '.raw', or mzML). 2. Map the identified format to its"
- [readme] Once converted, MZA files are accessed using generic HDF5 libraries independent of vendor format.: "Once converted, MZA files can be easily accessed from any programming language and operating system using generic HDF5 libraries available (e.g., h5py and rhdf5)."
- [readme] Four supported input formats listed explicitly in README.: "Input formats supported: * Agilent '.d' (with or without ion mobility) * Bruker ion mobility 'd' (with ion mobility) * Thermo '.raw' * mzML"
- [readme] Intensity threshold is an optional parameter for filtering signals in conversion.: "-intensityThreshold arg: The minimum intensity that must be exceeded for signals to be included in the output mza file."
- [readme] Example command showing vendor format routing by file extension.: "mza -file test_data\LowHigh_PC_160_180_frames1-10.d -intensityThreshold 20"
