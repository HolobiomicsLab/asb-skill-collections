---
name: hdf5-hierarchical-data-access
description: Use when you have multidimensional MS data converted to MZA HDF5 format (from Agilent .d, Bruker .d with ion mobility, Thermo .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3375
  tools:
  - h5py
  - hdf5plugin
  - numpy
  - pandas
  - mzapy
  - mza (command-line tool)
derived_from:
- doi: 10.1021/acs.analchem.3c01653
  title: mzapy
- doi: 10.1021/acs.jproteome.2c00313
  title: ''
evidence_spans:
- '* ``h5py``'
- '* ``hdf5plugin``'
- '* ``numpy``'
- Dependencies ------------------------------ * ``numpy``
- '* ``pandas``'
- Dependencies ... * ``pandas``
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzapy_cq
    doi: 10.1021/acs.analchem.3c01653
    title: mzapy
  dedup_kept_from: coll_mzapy_cq
schema_version: 0.2.0
---

# HDF5 hierarchical data access

## Summary

Access multidimensional mass spectrometry data stored in HDF5 format by querying hierarchical groups and datasets containing metadata, m/z arrays, intensity arrays, and ion mobility dimensions. This skill enables efficient retrieval of spectra, chromatograms, and 2D data arrays from converted vendor MS files without loading entire datasets into memory.

## When to use

Apply this skill when you have multidimensional MS data converted to MZA HDF5 format (from Agilent .d, Bruker .d with ion mobility, Thermo .raw, or mzML) and need to extract specific spectra, extracted ion chromatograms (XICs), arrival time distributions (ATDs), or 2D RT–m/z / RT–DT / DT–m/z arrays for analysis or visualization. Use it when vendor file formats are unavailable or when cross-platform and cross-programming-language access is required.

## When NOT to use

- Input is in proprietary vendor format (.raw, .d, .wiff) — convert to MZA HDF5 first using the MZA command-line tool.
- Data is already loaded in memory as a feature matrix or spectral library — use direct in-memory access instead.
- You require real-time or streaming access to MS data during acquisition — MZA is designed for post-acquisition analysis of complete files.

## Inputs

- MZA HDF5 file (.mza) containing metadata table and hierarchical groups (Arrays_intensity, Arrays_mz, Arrays_mzbin, Full_mz_array)
- Retention time (RT) range or single value (in minutes)
- Drift time (DT) or ion mobility arrival time range or single value (in milliseconds or Vs/cm²)
- Mass-to-charge (m/z) value or range (in Da)
- Optional: scan cache file for pre-computed indices

## Outputs

- 1D intensity and m/z arrays (numpy arrays) or pandas DataFrames with m/z, intensity, RT, DT, and metadata columns
- Extracted ion chromatogram (XIC) arrays indexed by RT or DT
- Arrival time distribution (ATD) arrays indexed by DT or RT
- 2D data matrices: RT–m/z, RT–DT, or DT–m/z intensity grids
- Metadata table with scan properties (scan number, MS level, polarity, activation, precursor m/z, collision energy, TIC)

## How to apply

Load the MZA HDF5 file using h5py and instantiate the mzapy.MZA class, optionally specifying cache_metadata_headers (default, empty list, or 'all') to control in-memory caching of metadata for faster repeated access. Query spectra by retention time (RT), drift time (DT), or m/z using getter methods: collect_ms1_arrays_by_rt() or collect_ms2_arrays_by_dt() return intensity and m/z arrays or pandas DataFrames; collect_xic_arrays_by_mz() and collect_atd_arrays_by_rt_mz() extract ion chromatograms and arrival time distributions for targeted m/z or RT+m/z windows; collect_rtmz_arrays() generates 2D matrices. For repeated queries on the same file, use load_scan_cache() to accelerate access. Close file handles and release cached data with close() when finished.

## Related tools

- **h5py** (Low-level HDF5 file reading and dataset access via Python)
- **hdf5plugin** (Decompression support for HDF5 datasets using various compression filters)
- **mzapy** (High-level Python interface and query API for MZA HDF5 files; wraps h5py with methods for MS data extraction) — https://github.com/PNNL-m-q/mzapy
- **mza (command-line tool)** (Converts vendor MS formats (Agilent .d, Bruker .d, Thermo .raw, mzML) to MZA HDF5 format) — https://github.com/PNNL-m-q/mza
- **numpy** (Array representation and manipulation of intensity, m/z, and 2D data grids)
- **pandas** (DataFrame output option for spectra and extracted data with labeled columns)

## Examples

```
from mzapy import MZA; mza = MZA('example.mza', cache_metadata_headers='all'); ms1_arrays = mza.collect_ms1_arrays_by_rt(rt_min=5.0, rt_max=10.0); xic = mza.collect_xic_arrays_by_mz(mz=500.5, mz_tol=0.1); mza.close()
```

## Evaluation signals

- Returned m/z and intensity arrays have matching length and span the expected m/z range and intensity values for the specified RT/DT window.
- XIC intensity profiles show expected peak shapes (Gaussian-like with baseline) when plotted against RT or DT.
- 2D data matrices have correct dimensions (rows and columns match RT bins, DT bins, or m/z bins) and nonzero intensities only in regions where spectra exist.
- Metadata columns (MS level, polarity, activation, precursor m/z) match expected values from the original vendor file or mzML.
- Repeated queries on the same file with load_scan_cache() show measurable latency reduction compared to first query.

## Limitations

- MZA HDF5 files store only nonzero-intensity m/z–intensity pairs; zero values are omitted, so reconstruction of true baseline requires external knowledge.
- Ion mobility (IM) spectra are stored as m/z bin indices (mzbins) pointing to a common Full_mz_array; direct m/z-space queries on IM data require bin-to-m/z lookup.
- Large files with many spectra may be partitioned into multiple HDF5 groups (e.g., Arrays_intensity0, Arrays_intensity1) to avoid HDF5 performance degradation; queries must handle partition indices (MzaPath column).
- CCS (collision cross-section) calibration coefficients are included only if detected during conversion; not all vendor formats or instruments provide calibration data.
- Intensity thresholding during MZA conversion (via -intensityThreshold parameter) removes low-intensity peaks; original data cannot be recovered from the MZA file.

## Evidence

- [other] mzapy is a Python package that provides an interface to unprocessed MS data in the MZA format, built using h5py and hdf5plugin as core dependencies for HDF5 file access.: "mzapy is a Python package that provides an interface to unprocessed MS data in the MZA format, built using h5py and hdf5plugin as core dependencies for HDF5 file access."
- [other] Initialize the MZA class with optional cache_metadata_headers parameter (default, empty list, or 'all') to control in-memory caching of metadata.: "The ``cache_metadata_headers`` kwarg is used to control which metadata headers are cached in memory for faster access"
- [readme] MZA is a stand-alone and self-contained command-line executable which converts multidimensional mass spectrometry (MS) data from files in proprietary vendor formats to the MZA simple data structure based on the HDF5 format.: "MZA is a stand-alone and self-contained command-line executable which converts multidimensional mass spectrometry (MS) data from files in proprietary vendor formats to the MZA simple data structure"
- [readme] The MZA file structure is simple: a metadata table and two groups with 1D arrays stored individually as HDF5 datasets per spectrum. Spectra are stored omitting zero-intensity values and as two jagged arrays, one in each corresponding group and named as the 'Scan' value in the metadata table.: "The MZA file structure is simple: a metadata table and two groups with 1D arrays stored individually as HDF5 datasets per spectrum."
- [readme] For IM spectra the m/z dimension is stored as indexes (mzbins): Arrays_mzbin (HDF5 group): contains 1D arrays with indexes to Full_mz_array.: "For IM spectra the m/z dimension is stored as indexes (mzbins): Arrays_mzbin (HDF5 group) contains 1D arrays with indexes to Full_mz_array."
- [other] Getter methods for metadata, extracted ion chromatograms (by m/z and m/z + drift time), arrival time distributions (by retention time + m/z), MS1 spectra (by retention time, drift time, or both; as arrays or DataFrames), MS2 spectra (by drift time or retention time + drift time; as arrays or DataFrames), and 2D data (RT–m/z, RT–DT, DT–m/z arrays).: "Implement getter methods for metadata, extracted ion chromatograms (by m/z and m/z + drift time), arrival time distributions (by retention time + m/z), MS1 spectra"
- [other] Provide scan caching methods (load_scan_cache, save_scan_cache) to accelerate repeated data access.: "Provide scan caching methods (load_scan_cache, save_scan_cache) to accelerate repeated data access."
