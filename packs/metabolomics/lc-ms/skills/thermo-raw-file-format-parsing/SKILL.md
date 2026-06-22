---
name: thermo-raw-file-format-parsing
description: Use when you have acquired multidimensional mass spectrometry data (MS1, MS/MS, or data-independent acquisition) from a Thermo instrument saved in the proprietary '.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - MZA
  - h5py
  - rhdf5
  - Wine
  - Docker
  techniques:
  - LC-MS
  - ion-mobility-MS
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

# thermo-raw-file-format-parsing

## Summary

Convert proprietary Thermo '.raw' mass spectrometry data files into the MZA HDF5-based simple data structure, enabling cross-platform and cross-programming language access to multidimensional MS data via generic HDF5 libraries.

## When to use

You have acquired multidimensional mass spectrometry data (MS1, MS/MS, or data-independent acquisition) from a Thermo instrument saved in the proprietary '.raw' format, and you need to access it programmatically from any programming language or operating system without vendor-specific software dependencies, or you are integrating heterogeneous MS data from multiple instrument vendors into a unified HDF5-based archive.

## When NOT to use

- Input file is already in mzML or HDF5 format; use native parsers or alternative conversion tools instead.
- You require preservation of all zero-intensity m/z values or raw binary metadata not exposed in the MZA schema; MZA omits zeros and abstracts vendor-specific fields.
- You are working on a non-Windows system without Docker or Wine pre-installed; MZA is a Windows executable and requires compatibility layer setup on Unix-like systems.

## Inputs

- Thermo '.raw' file (proprietary binary mass spectrometry data file)
- Optional intensity threshold value (numeric, units: instrument-dependent intensity)

## Outputs

- MZA file (HDF5-based simple data structure with metadata table and two jagged array groups)
- Metadata table (CSV-like HDF5 dataset with columns: Scan, MzaPath, MSLevel, Polarity, Activation, CollisionEnergy, RetentionTime, PrecursorScan, PrecursorMonoisotopicMz, PrecursorCharge, IsolationWindowTargetMz, IsolationWindowLowerOffset, IsolationWindowUpperOffset, TIC, SpectrumTitle, IonMobilityFrame, IonMobilityBin, IonMobilityTime)

## How to apply

Download the latest mza.exe executable from the PNNL-m-q/mza GitHub releases page. Invoke MZA from the command line with the '-file' parameter pointing to your Thermo '.raw' input file; optionally apply an '-intensityThreshold' parameter to exclude low-intensity signals (e.g., -intensityThreshold 20) that may introduce noise. MZA will convert the proprietary vendor format to the MZA simple data structure: a metadata table describing spectrum properties (scan number, MS level, retention time, precursor m/z, activation type, etc.) and two HDF5 groups (Arrays_intensity and Arrays_mz) storing 1D arrays per spectrum, with zero-intensity values omitted. Verify the output '.mza' file conforms to the MZA schema by loading it with h5py (Python) or rhdf5 (R) and inspecting the metadata table structure and dataset hierarchy.

## Related tools

- **MZA** (Command-line executable that performs the conversion from Thermo '.raw' vendor format to MZA HDF5 simple data structure) — https://github.com/PNNL-m-q/mza
- **h5py** (Python library for reading, validating, and accessing MZA output HDF5 files programmatically)
- **rhdf5** (R package for reading, validating, and accessing MZA output HDF5 files programmatically)
- **Wine** (Compatibility layer required to run MZA executable on Unix-like operating systems (Ubuntu, macOS)) — https://www.winehq.org
- **Docker** (Optional containerization method to run MZA on Unix-like systems without manual Wine installation)

## Examples

```
mza -file sample_data/LCMSMS_Lipids_POS.raw -intensityThreshold 20
```

## Evaluation signals

- Output file is created with '.mza' extension and is a valid HDF5 file readable by h5py or rhdf5 without errors.
- Metadata table HDF5 dataset is present and contains all expected columns (Scan, MSLevel, RetentionTime, PrecursorMonoisotopicMz, etc.) with correct data types and no null entries for required fields.
- Arrays_intensity and Arrays_mz groups exist and contain 1D datasets named after Scan values from the metadata table; all datasets have matching lengths (m/z and intensity paired).
- No zero-intensity values are present in the Arrays_intensity datasets (confirming MZA's zero-omission behavior).
- Spectrum count in metadata table matches the number of datasets in Arrays_intensity and Arrays_mz groups; file size is smaller than the original '.raw' file due to zero-omission and format compression.

## Limitations

- MZA is a closed-source Windows binary executable; Unix-like users must use Wine (tested on Ubuntu 22.04.1, Wine 6.0.3) or Docker to run it, adding dependency complexity.
- MZA omits zero-intensity m/z values in output, which is appropriate for sparse MS spectra but may lose information if full m/z ranges or baseline values are required for downstream analysis.
- Vendor-specific metadata and raw binary structures not mapped to the MZA schema are discarded during conversion; only standardized spectrum properties (scan number, retention time, precursor m/z, activation type, collision energy) are preserved.
- Performance may degrade for files with very large numbers of spectra; MZA creates multiple HDF5 groups (partitions) to avoid storing too many datasets in a single group, but this partitioning is opaque to the user and requires awareness of the MzaPath column to access arrays correctly.
- The '-intensityThreshold' parameter filters globally across all spectra; there is no per-scan or per-MS-level threshold control, which may inappropriately remove weak but real signals in some regions of the data.

## Evidence

- [readme] Thermo '.raw' support confirmed: "Input formats supported: * Agilent '.d' (with or without ion mobility) * Bruker ion mobility 'd' (with ion mobility) * Thermo '.raw' * mzML"
- [readme] MZA HDF5 output structure definition: "The MZA file structure is simple: a metadata table and two groups with 1D arrays stored individually as HDF5 datasets per spectrum. * Metadata (HDF5 dataset): each row in the metadata table (see csv"
- [readme] Zero-omission behavior: "Spectra are stored omitting zero-intensity values and as two jagged arrays, one in each corresponding group and named as the "Scan" value in the metadata table"
- [readme] Cross-platform and cross-programming-language access: "Once converted, MZA files can be easily accessed from any programming language and operating system using generic HDF5 libraries available (e.g., h5py and rhdf5)."
- [readme] Intensity threshold parameter use: "Optional: -intensityThreshold arg: The minimum intensity that must be exceeded for signals to be included in the output mza file."
- [readme] Windows invocation example: "Convert a single '.d' file: mza -file test_data\LowHigh_PC_160_180_frames1-10.d -intensityThreshold 20"
- [readme] Multidimensional MS context: "Untargeted MS-based workflows incorporating orthogonal separations, such as liquid chromatography (LC) and ion mobility spectrometry (IM), and collecting extensive fragmentation data with"
- [readme] Vendor library dependencies: "By using MZA, you agree to comply with the restrictions imposed on you by the license agreements of the software libraries on which it depends: * Agilent Technologies Mass Hunter Data Access"
