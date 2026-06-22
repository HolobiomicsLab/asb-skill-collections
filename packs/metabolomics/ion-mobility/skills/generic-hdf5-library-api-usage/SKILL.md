---
name: generic-hdf5-library-api-usage
description: Use when when you have converted multidimensional MS data to MZA HDF5 format and need to programmatically read spectra, metadata, and ion mobility or mass-to-charge arrays in Python or R without vendor-specific dependencies.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - MZA
  - h5py
  - rhdf5
  - HDF5
  - hdf5plugin
  - NumPy
  techniques:
  - ion-mobility-MS
derived_from:
- doi: 10.1021/acs.jproteome.2c00313
  title: MZA
evidence_spans:
- MZA is a stand-alone and self-contained command-line executable which converts multidimensional mass spectrometry (MS) data
- using generic HDF5 libraries available (e.g., h5py and rhdf5)
- the MZA simple data structure based on the HDF5 format
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# generic-hdf5-library-api-usage

## Summary

Access and traverse multidimensional mass spectrometry data stored in HDF5 format using language-agnostic libraries (h5py for Python, rhdf5 for R) to extract metadata, structural information, and spectral arrays without proprietary vendor tools. This enables cross-language, cross-platform reproducibility of MS data workflows.

## When to use

When you have converted multidimensional MS data to MZA HDF5 format and need to programmatically read spectra, metadata, and ion mobility or mass-to-charge arrays in Python or R without vendor-specific dependencies. Also applicable when you need to validate the internal structure of an HDF5 MS file or compare outputs across programming languages.

## When NOT to use

- Input is raw proprietary vendor data (.raw, .d, or .mzML); use MZA conversion tool first, not generic HDF5 libraries directly.
- You require real-time streaming or on-disk editing of spectra; HDF5 generic libraries read data into memory and are optimized for batch access.
- You need vendor-specific instrument metadata (e.g., calibration parameters, instrument model details) not stored in the MZA HDF5 structure; consult original vendor files.

## Inputs

- MZA-converted HDF5 file (.mza extension) containing metadata dataset and spectral arrays
- Optionally: intensity threshold value (numeric, default behavior includes all signals)
- Optionally: scan number filter or ion mobility/retention time range

## Outputs

- Extracted metadata table (DataFrame or list of dictionaries with Scan, MSLevel, RetentionTime, IonMobilityTime, etc.)
- Spectral arrays (m/z and intensity pairs per spectrum, or mzbin indices linked to Full_mz_array)
- File structure report (JSON or text) documenting group hierarchy, dataset names, shapes, and data types
- Optionally: serialized subsets or filtered spectra in HDF5, CSV, or JSON format

## How to apply

Load the MZA HDF5 file using h5py (Python) or rhdf5 (R) and traverse the file hierarchy to enumerate top-level groups (Arrays_intensity, Arrays_mz, Arrays_mzbin, and metadata table). Extract dimensions, data types, and dataset shapes for each spectrum. For ion mobility data, resolve mzbin indices against the Full_mz_array dataset. Apply intensity thresholds (if desired) by filtering spectra where TIC or individual peak intensities fall below a user-defined minimum. Serialize extracted structure and arrays to a human-readable format (JSON, CSV, or HDF5 subset) for downstream analysis or cross-validation. The rationale is that HDF5's generic libraries provide vendor-independent access while preserving the original data structure and enabling reproducible workflows across platforms.

## Related tools

- **h5py** (Generic HDF5 file read/write API for Python; loads MZA files and exposes metadata, intensity, and m/z datasets as NumPy arrays)
- **rhdf5** (Generic HDF5 file read/write API for R; loads MZA files and exposes spectral arrays and metadata as R data structures)
- **MZA** (Prerequisite converter tool that transforms multidimensional MS data from vendor formats (.d, .raw, .mzML) into the simple HDF5-based MZA structure) — https://github.com/PNNL-m-q/mza
- **hdf5plugin** (Python extension enabling transparent decompression of HDF5 compressed datasets in MZA files)
- **NumPy** (Python array manipulation library; provides in-memory representation of spectral arrays returned by h5py)

## Examples

```
import h5py
import numpy as np
with h5py.File('data.mza', 'r') as f:
  metadata = f['Metadata'][:]
  scan_630_intensity = f['Arrays_intensity/630'][:]
  scan_630_mz = f['Arrays_mz/630'][:]
```

## Evaluation signals

- Successfully enumerated all top-level groups (Metadata, Arrays_intensity, Arrays_mz, Arrays_mzbin if present, Full_mz_array if present) with correct dataset/group counts matching the number of spectra in the file.
- Metadata table row count equals number of spectra; all required columns (Scan, MSLevel, RetentionTime, IonMobilityBin, IonMobilityTime if IM data) are present and non-null where expected.
- For each spectrum, intensity and m/z arrays have matching lengths; intensity values are numeric and positive; m/z values are in expected range (typically 50–2000 m/z).
- Cross-language consistency: identical metadata and spectral arrays retrieved from the same MZA file using h5py and rhdf5 (byte-level equality or within floating-point tolerance).
- For ion mobility data, mzbin indices successfully resolve to Full_mz_array without out-of-bounds errors; TIC reconstructed from intensity arrays matches metadata TIC column within <1% relative error.

## Limitations

- MZA HDF5 files omit zero-intensity values to save storage; reconstructing full spectra with zeros requires knowledge of the instrument's m/z binning scheme, which is not stored.
- For files with many spectra (>100k), data may be partitioned across multiple HDF5 groups (e.g., Arrays_intensity1, Arrays_intensity2); the MzaPath column in metadata identifies the correct group partition for each spectrum.
- CCS calibration coefficients (CCScalDT, CCScalSLIM, CCScalTIMS) are included only if detected during MZA conversion; their presence is not guaranteed, and ion mobility interpretation is incomplete without them.
- Generic HDF5 libraries read entire datasets into memory; very large MZA files (>10 GB) may exceed available RAM on resource-constrained systems.
- The MZA file structure does not preserve raw detector counts or instrument-specific quality metrics; only the converted simple structure (metadata + arrays) is accessible via HDF5 libraries.

## Evidence

- [readme] Once converted, MZA files can be easily accessed from any programming language and operating system using generic HDF5 libraries available (e.g., h5py and rhdf5).: "Once converted, MZA files can be easily accessed from any programming language and operating system using generic HDF5 libraries available (e.g., h5py and rhdf5)."
- [readme] The MZA file structure is simple: a metadata table and two groups with 1D arrays stored individually as HDF5 datasets per spectrum.: "The MZA file structure is simple: a metadata table and two groups with 1D arrays stored individually as HDF5 datasets per spectrum."
- [readme] Metadata (HDF5 dataset): each row in the metadata table represents a spectrum and the columns represent the properties of the spectrum such as scan number, MS level, activation, retention time, ion mobility arrival time, etc.: "Metadata (HDF5 dataset): each row in the metadata table represents a spectrum and the columns represent the properties of the spectrum such as scan number, MS level, activation, retention time, ion"
- [readme] Spectra are stored omitting zero-intensity values and as two jagged arrays, one in each corresponding group and named as the "Scan" value in the metadata table: Arrays_intensity (HDF5 group) contains 1D arrays with intensity values. Arrays_mz (HDF5 group) contains 1D arrays with mass-to-charge (m/z) values.: "Spectra are stored omitting zero-intensity values and as two jagged arrays, one in each corresponding group and named as the "Scan" value in the metadata table: Arrays_intensity (HDF5 group) contains"
- [readme] For IM spectra the m/z dimension is stored as indexes (mzbins): Arrays_mzbin (HDF5 group) contains 1D arrays with indexes to Full_mz_array.: "For IM spectra the m/z dimension is stored as indexes (mzbins): Arrays_mzbin (HDF5 group) contains 1D arrays with indexes to Full_mz_array."
- [readme] Example scripts are provided in the respective folders. R requires the rhdf5 package and Python requires the h5py, hdf5plugin, numpy and matplotlib packages.: "Example scripts are provided in the respective folders. R requires the rhdf5 package and Python requires the h5py, hdf5plugin, numpy and matplotlib packages."
- [readme] Partitions may be created for files with too many spectra. Having too many datasets within a single group can slow down data reading performance. HDF5 is more efficient when using multiple groups instead of storing many datasets within one group.: "Partitions may be created for files with too many spectra. Having too many datasets within a single group can slow down data reading performance. HDF5 is more efficient when using multiple groups"
