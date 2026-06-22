---
name: mass-spectrometry-metadata-caching
description: Use when you plan to perform repeated queries or filtering on MS metadata attributes (e.g., extract all MS2 spectra with collision energy > 30 eV, or collect all scans in a retention time window) across a large MZA HDF5 file.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - h5py
  - hdf5plugin
  - numpy
  - pandas
  - mzapy
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-metadata-caching

## Summary

Selectively cache MS metadata headers in memory during HDF5 file access to balance query performance against memory footprint. This skill applies the mzapy.MZA class's cache_metadata_headers parameter to control which metadata—such as retention time, ion mobility arrival time, MS level, precursor m/z, and activation type—are held in RAM for faster repeated access.

## When to use

Apply this skill when you plan to perform repeated queries or filtering on MS metadata attributes (e.g., extract all MS2 spectra with collision energy > 30 eV, or collect all scans in a retention time window) across a large MZA HDF5 file. Caching is beneficial when the same metadata columns are accessed many times per analysis session; it trades upfront memory consumption for eliminated disk I/O on subsequent accesses.

## When NOT to use

- Input file is already in a columnar database or memory-mapped format (e.g., Parquet, NetCDF) that provides native lazy evaluation; use native indexing instead.
- Memory budget is extremely tight (< 1 GB available) and the metadata table is very large (> 1 million spectra); default to empty list or streaming access.
- Analysis requires only a single sequential scan through the file without repeated metadata lookups; caching adds overhead with no benefit.

## Inputs

- MZA HDF5 file (.mza) containing unprocessed MS data with metadata and jagged m/z and intensity arrays
- cache_metadata_headers parameter: empty list, list of metadata column names, or string 'all'

## Outputs

- Initialized mzapy.MZA object with metadata headers cached in memory according to the specified strategy
- Cached metadata table as a pandas DataFrame or equivalent in-memory structure
- Subsequent fast retrieval of spectra filtered by metadata criteria

## How to apply

Initialize the mzapy.MZA class with the cache_metadata_headers parameter set to one of three modes: (1) an empty list (default) to disable caching and read metadata on demand; (2) a list of specific column names (e.g., ['RetentionTime', 'IonMobilityTime', 'PrecursorMonoisotopicMz']) to cache only those columns; or (3) the string 'all' to cache every metadata column. Choose the strategy based on your query patterns and available system memory: use 'all' for interactive exploratory analysis with multiple filter passes; use a targeted list for workflows that repeatedly query a fixed subset of columns; use the default (empty list) for memory-constrained environments or single-pass linear scans. After initialization, invoke getter methods such as collect_ms1_arrays_by_rt(), collect_ms2_arrays_by_dt(), or collect_xic_arrays_by_mz() to retrieve spectra; the cached metadata will accelerate these lookups.

## Related tools

- **h5py** (Core HDF5 library for reading MZA files and accessing datasets and groups)
- **hdf5plugin** (Provides decompression codecs for HDF5 filters to uncompress stored MS arrays)
- **pandas** (Constructs and manages cached metadata tables; returns spectra as DataFrames)
- **numpy** (Underlying array storage for cached metadata and raw m/z and intensity data)
- **mzapy** (Python package providing the MZA class with cache_metadata_headers parameter) — https://github.com/PNNL-m-q/mzapy

## Examples

```
from mzapy import MZA
mza = MZA('example.h5', cache_metadata_headers=['RetentionTime', 'IonMobilityTime', 'PrecursorMonoisotopicMz'])
ms2_arrays = mza.collect_ms2_arrays_by_dt(retention_time=25.0, drift_time=50.0)
```

## Evaluation signals

- Verify that the MZA object initializes without error and the cache_metadata_headers parameter is accepted (check object's __init__ signature).
- Confirm that requested metadata columns are present in memory: inspect the cached metadata table size and column names after initialization.
- Measure wall-clock time for repeated metadata-filtered queries (e.g., collect_ms2_arrays_by_dt() called 10 times); cached mode should show faster average latency than uncached mode on identical queries.
- Validate that spectra returned by getter methods are correctly filtered according to cached metadata (e.g., all returned spectra have RetentionTime within expected range if RetentionTime was cached).
- Check memory usage: compare resident set size (RSS) or heap size before and after initialization with different cache_metadata_headers settings; 'all' should consume more RAM than a targeted list or empty list.

## Limitations

- Caching entire metadata tables ('all' mode) can exhaust available system memory for very large MS runs (> 10 million spectra); monitor memory consumption and fall back to targeted caching or default mode if needed.
- The mzapy package caches only metadata headers; actual m/z and intensity arrays remain on disk and must be decompressed and read on demand—caching does not accelerate spectrum data retrieval, only metadata queries.
- Cache coherence is not maintained if the underlying MZA HDF5 file is modified externally during the analysis session; the MZA class does not re-read or invalidate cached metadata.
- Metadata caching is most effective for repeated queries on the same columns; if each query requests different metadata subsets, the overhead of maintaining a large cache may outweigh benefits.

## Evidence

- [other] cache_metadata_headers parameter controls in-memory caching: "Initialize the MZA class with optional cache_metadata_headers parameter (default, empty list, or 'all') to control in-memory caching of metadata."
- [other] metadata caching accelerates repeated queries: "The ``cache_metadata_headers`` kwarg is used to control which metadata headers are cached in memory for faster access"
- [other] MZA class supports multiple metadata column access: "Implement getter methods for metadata, extracted ion chromatograms (by m/z and m/z + drift time), arrival time distributions (by retention time + m/z), MS1 spectra (by retention time, drift time, or"
- [readme] mzapy as Python interface for MZA HDF5 format: "mzapy is a Python package that provides an interface to unprocessed MS data in the MZA format."
- [readme] dependencies for HDF5 access and decompression: "Example scripts for visualization of mobility distributions from total (or mass extracted) ion intensities in the raw data in mza files can be found is this"
