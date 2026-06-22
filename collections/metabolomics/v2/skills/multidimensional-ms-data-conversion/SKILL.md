---
name: multidimensional-ms-data-conversion
description: 'Use when you have acquired untargeted MS data with orthogonal separations (LC, ion mobility) and/or data-independent acquisition (DIA) from Thermo, Agilent, or Bruker instruments, and you need to: (1) store multidimensional spectra in a vendor-neutral, platform-agnostic format;'
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
  - Wine
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.2c00313
  all_source_dois:
  - 10.1021/acs.jproteome.2c00313
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# multidimensional-ms-data-conversion

## Summary

Convert multidimensional mass spectrometry data from proprietary vendor formats (Thermo .raw, Agilent .d, Bruker .d, mzML) to the MZA HDF5-based simple data structure, enabling cross-platform and cross-programming language access via generic HDF5 libraries.

## When to use

You have acquired untargeted MS data with orthogonal separations (LC, ion mobility) and/or data-independent acquisition (DIA) from Thermo, Agilent, or Bruker instruments, and you need to: (1) store multidimensional spectra in a vendor-neutral, platform-agnostic format; (2) enable downstream access from multiple programming languages and operating systems; or (3) prepare data for software development or AI research on complex MS datasets.

## When NOT to use

- Input file is already in mzML or MZA HDF5 format and does not require re-encoding.
- You need vendor-specific metadata or instrument parameters not mapped in the MZA simple data structure (e.g., raw detector voltage, RF values).
- The MS dataset is from an unsupported vendor or instrument type (MZA supports only Thermo, Agilent, Bruker, and mzML).
- You require the ability to edit or regenerate the raw spectral data; MZA conversion is destructive (zero-intensity values are omitted).

## Inputs

- Thermo .raw mass spectrometry file
- Agilent .d directory (with or without ion mobility)
- Bruker ion mobility .d directory
- mzML file
- Directory path containing multiple files of supported format

## Outputs

- MZA HDF5 file (.mza or .h5)
- Metadata table (HDF5 dataset) with spectrum properties
- Arrays_intensity HDF5 group (1D intensity arrays per scan)
- Arrays_mz HDF5 group (1D m/z arrays per scan)
- Arrays_mzbin HDF5 group (m/z indices for ion mobility spectra, if applicable)
- Full_mz_array HDF5 dataset (unified m/z values for IM data, if applicable)
- CCS calibration coefficients (HDF5 dataset, if detected)

## How to apply

Obtain the MZA command-line executable (mza.exe) from the PNNL-m-q/mza GitHub releases. Invoke MZA with the input vendor file (e.g., Thermo .raw, Agilent .d) and optional intensity threshold parameter to filter low-abundance signals. MZA converts the proprietary data to an HDF5 file containing a metadata table (scan properties: MS level, retention time, ion mobility arrival time, precursor m/z, activation type, etc.) and two or three jagged array groups (Arrays_intensity, Arrays_mz, and optionally Arrays_mzbin for ion mobility data). Verify output conformance by validating the HDF5 structure using h5py or rhdf5 libraries: confirm the presence of metadata dataset, intensity/m/z array groups, and correct mapping of scan numbers to arrays.

## Related tools

- **MZA** (Command-line executable that performs the vendor-format-to-HDF5 conversion of multidimensional MS data) — https://github.com/PNNL-m-q/mza/releases
- **h5py** (Python library for reading, validating, and accessing converted MZA HDF5 files)
- **rhdf5** (R package for reading, validating, and accessing converted MZA HDF5 files)
- **Wine** (Compatibility layer required to run MZA executable on Unix-like operating systems) — https://www.winehq.org
- **Docker** (Container system for deploying MZA with Wine on Unix-like systems without local Wine installation)

## Examples

```
mza -file test_data/LCMSMS_Lipids_POS.raw -intensityThreshold 20
```

## Evaluation signals

- Output HDF5 file is created and is readable by h5py or rhdf5 without errors.
- Metadata table contains expected columns (Scan, MzaPath, MSLevel, RetentionTime, IonMobilityTime, PrecursorMonoisotopicMz, Activation, etc.) and row count matches the number of spectra in the input file.
- Arrays_intensity and Arrays_mz (or Arrays_mzbin for IM data) groups exist and contain 1D datasets named after Scan values in the metadata table.
- For ion mobility data, Full_mz_array dataset is present and mzbins reference valid indices into this array.
- Sum or mean of intensity arrays per scan is greater than zero, and m/z values fall within the expected analytical range (typically 50–2000 m/z).
- If intensity threshold was specified, no intensity values in output arrays fall below the threshold (sparse representation validates signal filtering).
- CCS calibration coefficients dataset is present if input file contains calibration data (Agilent DT, SLIM, or Bruker TimsTOF).

## Limitations

- MZA omits zero-intensity values; sparse spectral representation cannot be inverted to recover the original density of the vendor data.
- On Unix-like systems, Wine compatibility layer (version 6.0.3 tested, wine-mono 7.3.0 tested) must be pre-installed; adds deployment complexity and potential performance overhead.
- Large files with many spectra may create partitions across multiple HDF5 groups to avoid performance degradation; practitioners must track MzaPath index to correctly access fragmented arrays.
- Vendor-specific metadata and parameters (e.g., detector voltage, RF frequencies, instrument tuning parameters) outside the MZA simple data structure schema are lost during conversion.
- Ion mobility dimension for IM spectra is indexed rather than stored as raw arrival times; lookup via Full_mz_array is required and may not preserve fine-grained m/z precision if binning was applied during acquisition.

## Evidence

- [readme] MZA is a stand-alone and self-contained command-line executable which converts multidimensional mass spectrometry (MS) data from files in proprietary vendor formats to the MZA simple data structure based on the HDF5 format.: "MZA is a stand-alone and self-contained command-line executable which converts multidimensional mass spectrometry (MS) data from files in proprietary vendor formats to the MZA simple data structure"
- [readme] Untargeted MS-based workflows incorporating orthogonal separations, such as liquid chromatography (LC) and ion mobility spectrometry (IM), and collecting extensive fragmentation data with data-independent acquisition (DIA) methods or alternative activation techniques, are providing heterogeneous and multidimensional information which allows deeper understanding in omics studies.: "Untargeted MS-based workflows incorporating orthogonal separations, such as liquid chromatography (LC) and ion mobility spectrometry (IM), and collecting extensive fragmentation data with"
- [readme] Once converted, MZA files can be easily accessed from any programming language and operating system using generic HDF5 libraries available (e.g., h5py and rhdf5).: "Once converted, MZA files can be easily accessed from any programming language and operating system using generic HDF5 libraries available (e.g., h5py and rhdf5)."
- [readme] The MZA file structure is simple: a metadata table and two groups with 1D arrays stored individually as HDF5 datasets per spectrum.: "The MZA file structure is simple: a metadata table and two groups with 1D arrays stored individually as HDF5 datasets per spectrum."
- [readme] Spectra are stored omitting zero-intensity values and as two jagged arrays, one in each corresponding group and named as the 'Scan' value in the metadata table: Arrays_intensity (HDF5 group): contains 1D arrays with intensity values. Arrays_mz (HDF5 group): contains 1D arrays with mass-to-charge (m/z) values.: "Spectra are stored omitting zero-intensity values and as two jagged arrays, one in each corresponding group and named as the 'Scan' value in the metadata table"
- [intro] Convert multidimensional mass spectrometry data from proprietary vendor formats to MZA simple data structure based on HDF5: "Convert multidimensional mass spectrometry data from proprietary vendor formats to MZA simple data structure based on HDF5"
