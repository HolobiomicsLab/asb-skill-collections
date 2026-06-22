---
name: in-memory-optimization-for-large-datasets
description: Use when you are repeatedly querying or iterating over multidimensional MS data stored in MZA HDF5 format (retention time, drift time, m/z dimensions) and profiling shows that repeated disk I/O for the same metadata or scan ranges dominates runtime.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - h5py
  - hdf5plugin
  - numpy
  - pandas
  - mzapy.MZA
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

# in-memory-optimization-for-large-datasets

## Summary

Selective in-memory caching of metadata headers and scan data in multidimensional MS workflows to accelerate repeated data access without exhausting memory on large HDF5-based datasets. This skill applies the mzapy MZA class's cache_metadata_headers parameter and scan caching methods to balance read performance against memory constraints.

## When to use

You are repeatedly querying or iterating over multidimensional MS data stored in MZA HDF5 format (retention time, drift time, m/z dimensions) and profiling shows that repeated disk I/O for the same metadata or scan ranges dominates runtime. Use this skill when you need to extract ion chromatograms, arrival time distributions, or MS1/MS2 spectra multiple times from the same file within a single workflow session.

## When NOT to use

- Your workflow processes each MS scan only once and does not requery metadata or spectra; in this case, streaming reads without caching are more memory-efficient.
- The entire MZA file fits comfortably in available RAM; selective caching adds complexity without benefit.
- You are converting vendor MS formats to MZA (use the mza converter tool instead); this skill applies only to reading and querying MZA files post-conversion.

## Inputs

- MZA HDF5 file (.mza format) containing uncompressed or hdf5plugin-compressed MS data
- Metadata table with columns: Scan, MzaPath, MSLevel, RetentionTime, IonMobilityBin, IonMobilityTime, etc.
- 1D intensity and m/z arrays stored in HDF5 groups (Arrays_intensity, Arrays_mz, Arrays_mzbin)

## Outputs

- In-memory metadata header cache (dict or pandas DataFrame subset)
- In-memory scan cache (serialized or deserialized numpy arrays)
- Saved scan cache file (.pkl or equivalent) for reuse across sessions

## How to apply

Initialize the MZA class with the cache_metadata_headers parameter set to control which metadata is held in memory: use an empty list (default) for minimal caching, pass a list of specific header names (e.g., ['RetentionTime', 'IonMobilityTime', 'MzaPath']) to cache selected fields, or pass 'all' to cache all headers if memory permits. Before performing repeated queries (e.g., collecting multiple XIC arrays or MS1 spectra by retention time), call load_scan_cache() to preload frequently accessed scan data into memory. After the analysis, call save_scan_cache() to serialize the cache to disk, enabling reuse in future sessions. This avoids re-decompressing HDF5 arrays on each query. The rationale is that HDF5 decompression (via hdf5plugin) is expensive relative to in-memory array access, so strategic caching trades memory footprint for latency reduction. Always call close() to release file handles and cached data when finished.

## Related tools

- **h5py** (Low-level HDF5 file I/O and dataset access; underlying layer for MZA class file operations)
- **hdf5plugin** (Transparent decompression of HDF5 datasets; caching mitigates repeated decompression overhead)
- **mzapy.MZA** (High-level interface implementing cache_metadata_headers parameter and load_scan_cache() / save_scan_cache() methods) — https://github.com/PNNL-m-q/mzapy
- **numpy** (In-memory array representation and fast lookup of cached scan data)
- **pandas** (Optional structured representation of metadata cache for DataFrame-based queries)

## Examples

```
from mzapy import MZA
mza = MZA('example.mza', cache_metadata_headers=['RetentionTime', 'IonMobilityTime'])
mza.load_scan_cache(scan_range=(100, 500))
xic_data = mza.collect_xic_arrays_by_mz(400.5)
mza.save_scan_cache('cached_scans.pkl')
mza.close()
```

## Evaluation signals

- Elapsed wall-clock time for repeated queries (e.g., collect_xic_arrays_by_mz, collect_ms1_arrays_by_rt) is significantly lower on the second and subsequent passes compared to the first pass without cache.
- Memory usage reported by the OS or Python psutil stays below an acceptable threshold (verify cache_metadata_headers='all' is not selected if OOM risk is high).
- Saved cache file (from save_scan_cache()) exists and is non-zero in size, indicating scans were actually cached.
- Re-loaded cache from previous session (via load_scan_cache()) yields identical query results as recomputing from disk, confirming correctness.
- HDF5 decompression library calls (if profiled) drop significantly after cache population, confirming I/O reduction.

## Limitations

- Cache coherency is not automatic: if the underlying MZA file is modified between cache save and load, stale cached data may be returned without warning.
- The cache_metadata_headers parameter applies only to metadata headers (scan properties like retention time and ion mobility); individual m/z and intensity arrays are only cached via load_scan_cache(), which loads entire scan objects.
- For very large files with millions of spectra, even selective caching can exhaust RAM; practitioners must choose cache_metadata_headers carefully and avoid load_scan_cache() on the full spectrum range.
- Cache persistence (save_scan_cache) relies on pickle or equivalent serialization; binary compatibility across Python versions or platforms is not guaranteed.

## Evidence

- [other] The cache_metadata_headers kwarg is used to control which metadata headers are cached in memory for faster access: "The ``cache_metadata_headers`` kwarg is used to control which metadata headers are cached in memory for faster access"
- [other] Provide scan caching methods (load_scan_cache, save_scan_cache) to accelerate repeated data access.: "Provide scan caching methods (load_scan_cache, save_scan_cache) to accelerate repeated data access."
- [other] Initialize the MZA class with optional cache_metadata_headers parameter (default, empty list, or 'all') to control in-memory caching of metadata.: "Initialize the MZA class with optional cache_metadata_headers parameter (default, empty list, or 'all') to control in-memory caching of metadata."
- [readme] HDF5 is more efficient when using multiple groups instead of storing many datasets within one group.: "HDF5 is more efficient when using multiple groups instead of storing many datasets within one group."
- [other] mzapy is a Python package that provides an interface to unprocessed MS data in the MZA format, built using h5py and hdf5plugin as core dependencies for HDF5 file access.: "mzapy is a Python package that provides an interface to unprocessed MS data in the MZA format, built using h5py and hdf5plugin as core dependencies for HDF5 file access."
