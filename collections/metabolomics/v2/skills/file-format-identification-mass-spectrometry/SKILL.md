---
name: file-format-identification-mass-spectrometry
description: Use when you have raw MS data files from one or more instrument vendors (Agilent, Bruker, Thermo Fisher, or mzML-formatted) and need to convert them to a vendor-agnostic HDF5-based storage format for downstream software development, machine learning, or cross-platform data access.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3365
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

# file-format-identification-mass-spectrometry

## Summary

Identify proprietary mass spectrometry vendor file formats (Agilent '.d', Bruker ion mobility 'd', Thermo '.raw', mzML) by inspecting file extension and format signature, then route each to its corresponding MZA conversion handler. This skill is essential for preprocessing heterogeneous multidimensional MS data before standardization to HDF5-based MZA format.

## When to use

You have raw MS data files from one or more instrument vendors (Agilent, Bruker, Thermo Fisher, or mzML-formatted) and need to convert them to a vendor-agnostic HDF5-based storage format for downstream software development, machine learning, or cross-platform data access. Trigger: receipt of unmapped vendor-proprietary MS files; goal is standardization to MZA format.

## When NOT to use

- Input MS data is already in MZA (HDF5) format or another standardized format (e.g., NetCDF, mzXML) not listed as supported by MZA.
- Vendor library dependencies (Agilent Mass Hunter, Thermo MSFileReader, Bruker TDF-SDK) are not installed or not compatible with your operating system.
- You need to preserve proprietary metadata or vendor-specific peak-picking algorithms; MZA performs its own feature extraction and stores only standardized metadata columns.

## Inputs

- Agilent vendor MS data directory (.d, optionally with ion mobility)
- Bruker vendor MS data directory (ion mobility 'd' format)
- Thermo vendor MS data file (.raw format)
- mzML-formatted mass spectrometry data file
- File path or directory path (string)

## Outputs

- MZA file (HDF5-based standardized format)
- Metadata table (HDF5 dataset with spectrum properties: Scan, MSLevel, RetentionTime, IonMobilityBin, etc.)
- Arrays_intensity group (1D intensity arrays per spectrum)
- Arrays_mz group (1D m/z arrays per spectrum)
- Arrays_mzbin group (for ion mobility data: m/z bin indexes)
- Full_mz_array dataset (for ion mobility data: shared m/z values)

## How to apply

Inspect the input file or directory path extension (.d, .raw, or .mzML) and examine the file's format signature bytes to unambiguously identify the vendor format. Map the identified format to its corresponding MZA conversion handler: Agilent '.d' (with or without ion mobility) → Agilent handler; Bruker ion mobility 'd' → Bruker handler; Thermo '.raw' → Thermo handler; mzML → mzML handler. Pass the file path and optional intensityThreshold parameter (default or user-specified minimum intensity to include signals) to the MZA command-line executable. Verify successful conversion by checking that the output .mza file is created and contains the HDF5 metadata table and Arrays_intensity/Arrays_mz (or Arrays_mzbin for ion mobility data) groups.

## Related tools

- **MZA** (Command-line executable that ingests identified vendor format, routes to handler, and produces standardized HDF5 output) — https://github.com/PNNL-m-q/mza
- **HDF5** (Underlying data structure and storage format for converted MZA files)
- **h5py** (Python library for reading and writing MZA (HDF5) files after conversion)
- **rhdf5** (R package for reading and writing MZA (HDF5) files after conversion)

## Examples

```
mza -file test_data/LCMSMS_Lipids_POS.raw -intensityThreshold 20
```

## Evaluation signals

- Output .mza file exists and is valid HDF5 format (readable by h5py or rhdf5 without errors).
- Metadata table contains expected columns (Scan, MSLevel, RetentionTime, etc.) and row count matches number of spectra in input.
- Arrays_intensity and Arrays_mz (or Arrays_mzbin for IM data) groups are populated with non-empty 1D datasets named by Scan value.
- All intensity values in output are ≥ intensityThreshold parameter (if specified); zero-intensity values are omitted.
- For ion mobility data: IonMobilityBin, IonMobilityTime, and Full_mz_array are correctly populated; IonMobilityBin=0 represents summed spectrum.

## Limitations

- MZA is a closed-source Windows binary; Unix/Linux users must run via Wine or Docker container, which may introduce performance overhead.
- File identification relies on extension and format signature; files with incorrect extensions or corrupted headers may fail routing or produce cryptic errors.
- Vendor library dependencies (Agilent Mass Hunter Data Access, Thermo MSFileReader, Bruker TDF-SDK) are proprietary and subject to vendor licensing restrictions; redistribution of MZA binary is limited.
- Ion mobility collisional cross-section (CCS) calibration coefficients are included only if detected during conversion; absent or non-standard calibrations are not auto-generated.
- Very large MS files may cause HDF5 performance degradation if too many spectra are stored in a single group; MZA automatically partitions into multiple groups, but this requires awareness when accessing data programmatically.

## Evidence

- [other] Inspect the input file or directory extension and format signature to identify the vendor format (Agilent '.d', Bruker ion mobility 'd', Thermo '.raw', or mzML).: "Inspect the input file or directory extension and format signature to identify the vendor format (Agilent '.d', Bruker ion mobility 'd', Thermo '.raw', or mzML)."
- [readme] MZA is a stand-alone and self-contained command-line executable which converts multidimensional mass spectrometry (MS) data from files in proprietary vendor formats to the MZA simple data structure based on the HDF5 format.: "MZA is a stand-alone and self-contained command-line executable which converts multidimensional mass spectrometry (MS) data from files in proprietary vendor formats to the MZA simple data structure"
- [other] Map the identified format to its corresponding MZA conversion handler. Return the handler reference and conversion parameters for routing to the MZA command-line executable.: "Map the identified format to its corresponding MZA conversion handler. Return the handler reference and conversion parameters for routing to the MZA command-line executable."
- [readme] Input formats supported: Agilent '.d' (with or without ion mobility), Bruker ion mobility 'd' (with ion mobility), Thermo '.raw', mzML: "Input formats supported: Agilent '.d' (with or without ion mobility), Bruker ion mobility 'd' (with ion mobility), Thermo '.raw', mzML"
- [readme] For IM spectra the m/z dimension is stored as indexes (mzbins): Arrays_mzbin (HDF5 group): contains 1D arrays with indexes to Full_mz_array. Full_mz_array (HDF5 dataset): 1D array of full m/z values common for all spectra in the file.: "For IM spectra the m/z dimension is stored as indexes (mzbins): Arrays_mzbin (HDF5 group): contains 1D arrays with indexes to Full_mz_array."
- [readme] Optional: -intensityThreshold arg: The minimum intensity that must be exceeded for signals to be included in the output mza file.: "Optional: -intensityThreshold arg: The minimum intensity that must be exceeded for signals to be included in the output mza file."
