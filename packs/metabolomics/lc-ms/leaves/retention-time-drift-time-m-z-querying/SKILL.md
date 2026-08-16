---
name: retention-time-drift-time-m-z-querying
description: 'Use when you have multidimensional MS data converted to MZA HDF5 format and need to retrieve specific spectra or chromatographic slices defined by one or more of: retention time (in minutes), ion mobility arrival time (in milliseconds for DT/SLIM or Vs/cm² for TimsTOF), or m/z value (as a float or.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - h5py
  - hdf5plugin
  - numpy
  - pandas
  - mzapy
  - mza.exe
  techniques:
  - LC-MS
  - ion-mobility-MS
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c01653
  all_source_dois:
  - 10.1021/acs.analchem.3c01653
  - 10.1021/acs.jproteome.2c00313
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# retention-time-drift-time-m-z-querying

## Summary

Query multidimensional mass spectrometry data by retention time (RT), ion mobility drift time (DT), and mass-to-charge (m/z) coordinates to extract MS1 spectra, MS2 spectra, extracted ion chromatograms (XICs), and arrival time distributions (ATDs) from HDF5-format MZA files. This skill enables efficient access to specific spectral subsets from ion mobility-enhanced LC–MS workflows without loading entire raw files.

## When to use

You have multidimensional MS data converted to MZA HDF5 format and need to retrieve specific spectra or chromatographic slices defined by one or more of: retention time (in minutes), ion mobility arrival time (in milliseconds for DT/SLIM or Vs/cm² for TimsTOF), or m/z value (as a float or range). Typical triggers: building feature detection pipelines, extracting XICs for targeted ions, visualizing ATDs at specific RT–m/z combinations, or sampling MS1/MS2 spectra at discrete retention times.

## When NOT to use

- Input data is in proprietary vendor formats (Agilent .d, Bruker .d, Thermo .raw, mzML) and has not yet been converted to MZA HDF5; use the standalone mza.exe converter tool first.
- You need to access raw detector counts or non-zero-suppressed spectral data; MZA stores only non-zero intensity values, so full sparse reconstruction may be lossy for low-intensity signals below the intensity threshold used during conversion.
- Your analysis requires metadata fields not included in the standard MZA metadata table (e.g. instrument-specific tuning parameters); these are lost during conversion to the simplified HDF5 structure.

## Inputs

- MZA HDF5 file (.mza format, containing metadata table and spectral arrays)
- Retention time value or range (in minutes)
- Ion mobility drift time value or range (in milliseconds or Vs/cm², depending on instrument type)
- m/z value or range (float, Daltons)
- Optional cache_metadata_headers parameter ('all', [], or default)

## Outputs

- 1D NumPy arrays or Pandas DataFrames of MS1 spectra (m/z and intensity pairs at specified RT and/or DT)
- 1D NumPy arrays or Pandas DataFrames of MS2 spectra (fragmentation data at specified RT and/or DT)
- 1D NumPy arrays of extracted ion chromatograms (intensity vs. retention time at specified m/z)
- 1D NumPy arrays of arrival time distributions (intensity vs. ion mobility arrival time at specified RT and m/z)
- 2D arrays (RT–m/z, RT–DT, or DT–m/z heatmaps)

## How to apply

Initialize an mzapy.MZA object by loading an MZA HDF5 file with h5py and hdf5plugin decompression; optionally set cache_metadata_headers (empty list, default, or 'all') to control in-memory caching of metadata for faster repeated queries. Call the appropriate getter method based on your query dimensions: use collect_xic_arrays_by_mz() for extracted ion chromatograms at specific m/z values; use collect_atd_arrays_by_rt_mz() for arrival time distributions at specific (RT, m/z) pairs; use collect_ms1_arrays_by_rt() to retrieve MS1 spectra at specific retention times (optionally filtered by drift time); or use collect_ms2_arrays_by_dt() to retrieve MS2 spectra at specific drift times (optionally filtered by retention time). Each method returns data as NumPy arrays or Pandas DataFrames. For repeated queries on the same file, consider calling load_scan_cache() to pre-cache frequently accessed scans, reducing I/O latency. Release file handles and cached memory after analysis with close().

## Related tools

- **h5py** (Low-level HDF5 file I/O backend for reading and writing MZA datasets and groups)
- **hdf5plugin** (Decompression codec support for HDF5 compression filters used in MZA files)
- **numpy** (Array data structure and operations for spectral data returned by query methods)
- **pandas** (Optional DataFrame wrapper for returned spectra and metadata for tabular access patterns)
- **mzapy** (Python package providing MZA class and query interface methods (collect_*_arrays_by_*)) — https://github.com/PNNL-m-q/mzapy
- **mza.exe** (Standalone command-line tool to convert vendor MS data formats to MZA HDF5 format before querying) — https://github.com/PNNL-m-q/mza

## Examples

```
from mzapy import MZA
mza = MZA('example.h5', cache_metadata_headers='all')
ms1_arrays = mza.collect_ms1_arrays_by_rt(rt=15.5)
xic_arrays = mza.collect_xic_arrays_by_mz(mz=500.5)
atd_arrays = mza.collect_atd_arrays_by_rt_mz(rt=15.5, mz=500.5)
mza.close()
```

## Evaluation signals

- Returned spectra contain valid (m/z, intensity) pairs with m/z and intensity values within physically expected ranges for the instrument type (e.g., m/z > 0, intensity ≥ 0).
- Retention time values in returned metadata are within the observed range of the experiment; drift time values match the ion mobility type declared in MZA metadata (ms for DT, Vs/cm² for TimsTOF, etc.).
- XICs show monotonic or smoothly varying intensity across retention time; ATDs show expected peak structure at the queried m/z and RT.
- Query latency for cached scans (via load_scan_cache / save_scan_cache) is substantially lower than uncached queries on the same file.
- Total intensity (sum of all spectral intensities) at a given RT in MS1 spectra is consistent with Total Ion Current (TIC) value in metadata for that scan.

## Limitations

- Intensity values below the intensity threshold used during MZA conversion are permanently discarded; XICs and spectra will not recover low-abundance signals below that threshold.
- Metadata caching (via cache_metadata_headers='all') consumes RAM proportional to file size; very large files may require selective caching or chunked queries.
- Ion mobility arrival time representation differs by instrument vendor (milliseconds for Agilent DT and SLIM, Vs/cm² for Bruker TimsTOF, 1/k0 units); queries must use the correct units for the source instrument.
- Partitioning of spectra into multiple HDF5 groups (for files with many spectra) is transparent to the user but may impact query performance for datasets spanning partition boundaries.
- No built-in support for m/z calibration refinement or retention time alignment; raw MZA coordinates are used as stored.

## Evidence

- [intro] HDF5 file access foundation: "mzapy is a Python package that provides an interface to unprocessed MS data in the MZA format, built using h5py and hdf5plugin as core dependencies for HDF5 file access."
- [other] Metadata caching control: "Initialize the MZA class with optional cache_metadata_headers parameter (default, empty list, or 'all') to control in-memory caching of metadata."
- [other] XIC querying by m/z: "extracted ion chromatograms (by m/z and m/z + drift time)"
- [other] ATD and MS1 query methods: "arrival time distributions (by retention time + m/z), MS1 spectra (by retention time, drift time, or both; as arrays or DataFrames)"
- [other] MS2 and 2D data query methods: "MS2 spectra (by drift time or retention time + drift time; as arrays or DataFrames), and 2D data (RT–m/z, RT–DT, DT–m/z arrays)."
- [other] Scan caching for performance: "Provide scan caching methods (load_scan_cache, save_scan_cache) to accelerate repeated data access."
- [readme] MZA structure overview: "The MZA file structure is simple: a metadata table and two groups with 1D arrays stored individually as HDF5 datasets per spectrum."
- [readme] Metadata table column definitions: "RetentionTime (numeric, minutes), IonMobilityTime (numeric, Arrival time in milliseconds for DT and SLIM; 1/k0 in Vs/cm2 for TimsTOF)"
- [readme] Intensity threshold during conversion: "The minimum intensity that must be exceeded for signals to be included in the output mza file."
