---
name: mass-spectrometry-data-structure-interpretation
description: Use when you have converted multidimensional MS data (from Agilent .d, Bruker ion mobility .d, Thermo .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MZA
  - h5py
  - rhdf5
  - HDF5
  - OpenMS
  - R
  - arrow (R package)
  - pyarrow (Python library)
  - Rust mzPeak implementation
derived_from:
- doi: 10.1021/acs.jproteome.2c00313
  title: MZA
- doi: 10.1021/acs.jproteome.5c00435
  title: ''
evidence_spans:
- MZA is a stand-alone and self-contained command-line executable which converts multidimensional mass spectrometry (MS) data
- using generic HDF5 libraries available (e.g., h5py and rhdf5)
- There is also an R implementation in `R/`
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mza_cq
    doi: 10.1021/acs.jproteome.2c00313
    title: MZA
  - build: coll_mzpeak
    doi: 10.1021/acs.jproteome.5c00435
    title: mzpeak
  dedup_kept_from: coll_mza_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.2c00313
  all_source_dois:
  - 10.1021/acs.jproteome.2c00313
  - 10.1021/acs.jproteome.5c00435
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-data-structure-interpretation

## Summary

Interpret and navigate the hierarchical HDF5 structure of converted multidimensional mass spectrometry data (MZA format) to extract metadata, spectral arrays, and ion mobility calibration coefficients across programming languages. This skill enables reproducible access to complex LC–IM–MS datasets without vendor-specific tools.

## When to use

Apply this skill when you have converted multidimensional MS data (from Agilent .d, Bruker ion mobility .d, Thermo .raw, or mzML) into MZA format and need to programmatically retrieve spectra, metadata, ion mobility arrival times, or collision cross-section (CCS) calibration coefficients in Python (h5py) or R (rhdf5) without parsing vendor binary formats.

## When NOT to use

- Input is a raw vendor file (.raw, .d) that has not yet been converted to MZA format—use MZA converter executable first.
- You need to modify or write spectral data back to HDF5—MZA files are read-only access structures; conversion is one-directional.
- Data is already in a feature table, peak list, or mzML format where vendor-agnostic parsing via established libraries (e.g., pymzml, mzR) is already established.

## Inputs

- MZA-format HDF5 file (.mza extension)
- Scan identifiers (numeric, from Metadata table)
- File metadata table (HDF5 dataset containing row per spectrum)
- Optional: Partition index (MzaPath field) for sharded spectra

## Outputs

- Metadata table (rows: spectra; columns: scan number, MS level, retention time, ion mobility arrival time, activation type, precursor m/z, isolation window, TIC)
- 1D intensity arrays (per spectrum, zero-value omitted)
- 1D m/z arrays or m/z-bin index arrays (per spectrum)
- Full m/z array (shared across all spectra for ion mobility data)
- CCS calibration coefficients (if present: CCScalDT, CCScalTIMS, or CCScalSLIM)
- Serialized data structure report (JSON or text; optional)

## How to apply

Load the MZA HDF5 file using h5py (Python) or rhdf5 (R) and traverse the fixed hierarchical groups: Metadata (containing scan number, MS level, polarity, retention time, ion mobility frame, activation type, and precursor properties), Arrays_intensity and Arrays_mz (or Arrays_mzbin for ion mobility data, paired with Full_mz_array), and optional CCS calibration datasets (CCScalDT, CCScalSLIM, CCScalTIMS). For each spectrum identified by its Scan value in Metadata, retrieve the corresponding 1D intensity and m/z arrays from the appropriate group. For partitioned files (indicated by MzaPath ≠ empty string), append the partition index to the group name (e.g., Arrays_intensity1/630). Validate consistency by comparing the number of rows in Metadata against the union of dataset counts across intensity groups, and verify that intensity and m/z arrays have matching lengths per spectrum (after accounting for zero-value omission).

## Related tools

- **MZA** (Executable that converts proprietary multidimensional MS formats to MZA HDF5 structure for platform-agnostic access) — https://github.com/PNNL-m-q/mza/releases
- **h5py** (Python library for reading and traversing MZA HDF5 files and extracting metadata, arrays, and calibration coefficients)
- **rhdf5** (R package for reading and traversing MZA HDF5 files and extracting metadata, arrays, and calibration coefficients)
- **HDF5** (Underlying file format standard on which MZA data structure is based)

## Examples

```
import h5py
with h5py.File('sample.mza', 'r') as f:
    metadata = f['Metadata'][:]
    scan_630 = 630
    intensity = f['Arrays_intensity'][str(scan_630)][:]
    mz = f['Arrays_mz'][str(scan_630)][:]
    print(f'Scan {scan_630}: {len(intensity)} peaks, m/z range [{mz.min():.2f}, {mz.max():.2f}]')
```

## Evaluation signals

- Metadata table row count equals total number of datasets across all intensity groups (or across partitioned intensity groups if MzaPath > 0), accounting for zero-valued spectrum omission.
- For each spectrum, length(Arrays_intensity[Scan]) == length(Arrays_mz[Scan]) or length(Arrays_mzbin[Scan]).
- For ion mobility spectra, all unique mzbin values are valid indices into Full_mz_array (0 ≤ index < len(Full_mz_array)); IonMobilityBin == 0 denotes summed frame spectrum.
- Consistency check: same file read in Python (h5py) and R (rhdf5) yields identical Metadata table and matching intensity/m/z values per scan.
- CCS calibration datasets (if present) match expected coefficient counts: CCScalDT=[2], CCScalSLIM=[4], CCScalTIMS=[10].

## Limitations

- MZA executable runs on Windows natively; Unix/Linux requires Wine (tested on Ubuntu 22.04) or Docker container, adding setup complexity and potential compatibility issues.
- Partitioning by MzaPath is automatic for files with many spectra; querying partitioned spectra requires knowledge of the partition index from the Metadata table, which is not always obvious from Scan number alone.
- Zero-intensity values are omitted from Arrays_intensity and Arrays_mz, so the original full spectrum (with zeros) cannot be reconstructed without external baseline or noise model.
- Ion mobility CCS coefficients are only included if detected during conversion; absence does not indicate zero mobility—it indicates detection failure or acquisition without ion mobility.
- Input vendor formats supported are fixed (Agilent .d, Bruker IM .d, Thermo .raw, mzML); other formats must be converted to one of these before MZA conversion.

## Evidence

- [readme] The MZA file structure is simple: a metadata table and two groups with 1D arrays stored individually as HDF5 datasets per spectrum.: "The MZA file structure is simple: a metadata table and two groups with 1D arrays stored individually as HDF5 datasets per spectrum."
- [readme] Spectra are stored omitting zero-intensity values and as two jagged arrays, one in each corresponding group and named as the "Scan" value in the metadata table: Arrays_intensity (HDF5 group): contains 1D arrays with intensity values. Arrays_mz (HDF5 group): contains 1D arrays with mass-to-charge (m/z) values.: "Spectra are stored omitting zero-intensity values and as two jagged arrays, one in each corresponding group and named as the "Scan" value in the metadata table: Arrays_intensity (HDF5 group):"
- [readme] MZA files can be easily accessed from any programming language and operating system using generic HDF5 libraries available (e.g., h5py and rhdf5).: "MZA files can be easily accessed from any programming language and operating system using generic HDF5 libraries available (e.g., h5py and rhdf5)."
- [readme] For IM spectra the m/z dimension is stored as indexes (mzbins): Arrays_mzbin (HDF5 group): contains 1D arrays with indexes to Full_mz_array. Full_mz_array (HDF5 dataset): 1D array of full m/z values common for all spectra in the file.: "For IM spectra the m/z dimension is stored as indexes (mzbins): Arrays_mzbin (HDF5 group): contains 1D arrays with indexes to Full_mz_array. Full_mz_array (HDF5 dataset): 1D array of full m/z values"
- [readme] CCS calibration coefficients: These are included as an HDF5 dataset if detected during conversion to MZA: CCScalDT = [Tfix, Beta] for Agilent DT, CCScalSLIM = [C0, C1, C2, C3] for SLIM, CCScalTIMS = [C0, C1, C2, C3, C4, C5, C6, C7, C8, C9] for Bruker TimsTOF: "CCS calibration coefficients: These are included as an HDF5 dataset if detected during conversion to MZA"
- [readme] Partitions may be created for files with too many spectra. Having too many datasets within a single group can slow down data reading performance. HDF5 is more efficient when using multiple groups instead of storing many datasets within one group.: "Partitions may be created for files with too many spectra. Having too many datasets within a single group can slow down data reading performance. HDF5 is more efficient when using multiple groups"
- [readme] converts multidimensional mass spectrometry (MS) data from files in proprietary vendor formats to the MZA simple data structure based on the HDF5 format.: "converts multidimensional mass spectrometry (MS) data from files in proprietary vendor formats to the MZA simple data structure based on the HDF5 format."
