---
name: vendor-proprietary-format-interoperability
description: Use when you have mass spectrometry raw data in a proprietary vendor format (Thermo .raw, Agilent .d with or without ion mobility, Bruker ion mobility .d, or mzML) and need to enable reproducible, language-agnostic access to multidimensional spectra (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MZA
  - h5py
  - rhdf5
  - Wine (Unix/Linux)
  - Docker
derived_from:
- doi: 10.1021/acs.jproteome.2c00313
  title: MZA
evidence_spans:
- MZA is a stand-alone and self-contained command-line executable which converts multidimensional mass spectrometry (MS) data
- using generic HDF5 libraries available (e.g., h5py and rhdf5)
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

# vendor-proprietary-format-interoperability

## Summary

Convert multidimensional mass spectrometry data from proprietary vendor formats (Thermo .raw, Agilent .d, Bruker .d, mzML) into a standardized HDF5-based MZA simple data structure, enabling cross-platform and cross-programming-language access via generic HDF5 libraries.

## When to use

You have mass spectrometry raw data in a proprietary vendor format (Thermo .raw, Agilent .d with or without ion mobility, Bruker ion mobility .d, or mzML) and need to enable reproducible, language-agnostic access to multidimensional spectra (e.g., LC–IM–MS/MS data with extensive fragmentation metadata) for software development or artificial intelligence workflows. This is especially critical when downstream analysis requires access from multiple programming languages or operating systems.

## When NOT to use

- Input data is already in open, standardized formats (mzML, netCDF) accessible via existing parsers—MZA conversion adds no value.
- The proprietary vendor format is not among those supported (Thermo .raw, Agilent .d, Bruker .d, mzML); use vendor-specific APIs or alternative converters.
- Downstream analysis requires direct access to vendor-specific metadata or calibration parameters not preserved in the MZA schema (consult vendor documentation).

## Inputs

- Thermo .raw files
- Agilent .d directories (with or without ion mobility)
- Bruker ion mobility .d directories
- mzML files
- Directory paths containing multiple vendor files (with -extension parameter)

## Outputs

- .mza HDF5 files with metadata table and spectrum arrays
- Metadata CSV table (rows=spectra; columns=scan, MSLevel, Polarity, Activation, RetentionTime, IonMobilityTime, PrecursorMonoisotopicMz, TIC, etc.)
- Arrays_intensity HDF5 group (1D intensity arrays per spectrum)
- Arrays_mz HDF5 group (1D m/z arrays per spectrum) or Arrays_mzbin + Full_mz_array for ion mobility data
- CCS calibration coefficient datasets (if detected: CCScalDT, CCScalSLIM, CCScalTIMS)

## How to apply

Obtain the MZA command-line executable (mza.exe) from the PNNL-m-q/mza GitHub releases. Invoke MZA with the input vendor file path and specify optional parameters such as -intensityThreshold (minimum intensity for signal inclusion, e.g., 20) to filter noise; this threshold directly affects output file size and downstream signal-to-noise ratio. MZA converts the proprietary data into a hierarchical HDF5 structure: a metadata table (one row per spectrum, with columns for scan number, MS level, activation type, retention time, ion mobility arrival time, precursor m/z, collision energy, and isolation window parameters) and two or more groups (Arrays_intensity and Arrays_mz for standard MS; Arrays_mzbin, Full_mz_array, and calibration coefficient datasets for ion mobility data). Verify the output .mza file conforms to schema by inspecting the metadata table structure and validating that all spectra have matching intensity and m/z array dimensions using h5py or rhdf5.

## Related tools

- **MZA** (Stand-alone command-line executable that performs the vendor format to HDF5 conversion; accepts proprietary MS files and emits .mza files with standardized HDF5 structure.) — https://github.com/PNNL-m-q/mza
- **h5py** (Python library for reading and validating the HDF5 output structure, metadata table, and spectrum arrays post-conversion.)
- **rhdf5** (R package for reading and validating the HDF5 output structure, metadata table, and spectrum arrays post-conversion.)
- **Wine (Unix/Linux)** (Compatibility layer required to run the MZA Windows executable (mza.exe) on Unix-like operating systems.) — https://www.winehq.org
- **Docker** (Container runtime for executing MZA on Unix-like systems without native Wine installation; Dockerfile provided in repository.) — https://github.com/PNNL-m-q/mza

## Examples

```
mza -file test_data/LCMSMS_Lipids_POS.raw -intensityThreshold 20
```

## Evaluation signals

- Output .mza file exists and is valid HDF5 format (readable by h5py.File() or h5::H5File without errors).
- Metadata table contains expected columns (Scan, MSLevel, Polarity, Activation, RetentionTime, PrecursorMonoisotopicMz, IonMobilityTime, TIC) and number of rows equals number of spectra in input.
- Each spectrum record in metadata has corresponding 1D intensity and m/z (or mzbin) datasets in the appropriate HDF5 group, with non-zero array lengths.
- For ion mobility data: Full_mz_array is present and its length matches the maximum index in all Arrays_mzbin datasets; CCS calibration coefficients (CCScalDT, CCScalSLIM, or CCScalTIMS) are present if input file contains ion mobility calibration metadata.
- No intensity values fall below the specified -intensityThreshold parameter in the output arrays (noise filtering applied correctly).

## Limitations

- MZA is a closed-source binary (vendor libraries restrict source code distribution); troubleshooting depends on vendor library versions and Windows-only native support.
- On Unix-like systems, MZA requires Wine or Docker; Wine compatibility layer may introduce platform-specific performance variability.
- Conversion of very large vendor files may create .mza files with too many datasets in a single HDF5 group, triggering automatic partitioning (MzaPath field) and requiring users to adjust array access logic.
- Vendor-specific metadata not mapped to the MZA schema (e.g., instrument model, sample barcode, custom vendor fields) is not preserved in the output.
- Ion mobility data from Agilent DT, Bruker TIMS, or SLIM are stored as index arrays (mzbins) referencing Full_mz_array; direct m/z per ion mobility bin must be reconstructed post-conversion.

## Evidence

- [readme] converts multidimensional mass spectrometry (MS) data from files in proprietary vendor formats to the MZA simple data structure based on the HDF5 format: "converts multidimensional mass spectrometry (MS) data from files in proprietary vendor formats to the MZA simple data structure based on the HDF5 format"
- [readme] Once converted, MZA files can be easily accessed from any programming language and operating system using generic HDF5 libraries available (e.g., h5py and rhdf5).: "Once converted, MZA files can be easily accessed from any programming language and operating system using generic HDF5 libraries available (e.g., h5py and rhdf5)."
- [readme] Untargeted MS-based workflows incorporating orthogonal separations, such as liquid chromatography (LC) and ion mobility spectrometry (IM), and collecting extensive fragmentation data with data-independent acquisition (DIA) methods or alternative activation techniques, are providing heterogeneous and multidimensional information: "Untargeted MS-based workflows incorporating orthogonal separations, such as liquid chromatography (LC) and ion mobility spectrometry (IM), and collecting extensive fragmentation data"
- [readme] The MZA file structure is simple: a metadata table and two groups with 1D arrays stored individually as HDF5 datasets per spectrum.: "The MZA file structure is simple: a metadata table and two groups with 1D arrays stored individually as HDF5 datasets per spectrum."
- [readme] Spectra are stored omitting zero-intensity values and as two jagged arrays, one in each corresponding group and named as the 'Scan' value in the metadata table: Arrays_intensity (HDF5 group): contains 1D arrays with intensity values. Arrays_mz (HDF5 group): contains 1D arrays with mass-to-charge (m/z) values.: "Spectra are stored omitting zero-intensity values and as two jagged arrays, one in each corresponding group and named as the 'Scan' value in the metadata table: Arrays_intensity (HDF5 group):"
- [readme] For IM spectra the m/z dimension is stored as indexes (mzbins): Arrays_mzbin (HDF5 group): contains 1D arrays with indexes to Full_mz_array.: "For IM spectra the m/z dimension is stored as indexes (mzbins): Arrays_mzbin (HDF5 group): contains 1D arrays with indexes to Full_mz_array."
- [readme] CCS calibration coefficients: These are included as an HDF5 dataset if detected during conversion to MZA. CCScalDT = [Tfix, Beta] for Agilent DT; CCScalSLIM = [C0, C1, C2, C3] for SLIM; CCScalTIMS = [C0, C1, C2, C3, C4, C5, C6, C7, C8, C9] for Bruker TimsTOF: "CCS calibration coefficients: These are included as an HDF5 dataset if detected during conversion to MZA"
- [readme] -intensityThreshold arg: The minimum intensity that must be exceeded for signals to be included in the output mza file.: "-intensityThreshold arg: The minimum intensity that must be exceeded for signals to be included in the output mza file."
