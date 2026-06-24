---
name: multidimensional-spectral-array-extraction
description: Use when you have multidimensional MS data (with LC and/or ion mobility
  dimensions) converted to MZA HDF5 format and need to retrieve raw spectral intensity
  and m/z values for specific scans, retention times, drift times, or mass ranges.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3673
  tools:
  - h5py
  - hdf5plugin
  - numpy
  - pandas
  - mzapy
  - mza
  techniques:
  - LC-MS
  - ion-mobility-MS
  license_tier: open
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

# multidimensional-spectral-array-extraction

## Summary

Extract intensity and mass-to-charge arrays from multidimensional mass spectrometry data stored in MZA HDF5 format, supporting orthogonal separations (LC, ion mobility) and multiple MS levels. This skill enables programmatic access to raw spectra organized by retention time, drift time, and m/z dimensions for downstream analysis or machine learning.

## When to use

You have multidimensional MS data (with LC and/or ion mobility dimensions) converted to MZA HDF5 format and need to retrieve raw spectral intensity and m/z values for specific scans, retention times, drift times, or mass ranges. Use this skill when building custom analysis workflows that require direct access to jagged arrays rather than pre-processed features, or when preparing data for machine learning on heterogeneous spectral collections.

## When NOT to use

- Input is vendor proprietary format (.raw, .d, mzML) — use the mza conversion tool first to generate .mza files.
- You need only summary statistics (TIC, precursor m/z) — use metadata table lookup instead of full array extraction.
- Data is already in processed feature format (peak lists, aligned features) — this skill retrieves raw, unprocessed spectra.

## Inputs

- MZA HDF5 file (.mza extension) containing metadata table and HDF5 groups (Arrays_intensity, Arrays_mz, optionally Arrays_mzbin)
- Query parameters: retention time (minutes), drift time (milliseconds or 1/k0), m/z value, or m/z range
- Optional cache strategy: 'default' (empty list), specific metadata column names, or 'all'

## Outputs

- 1D numpy arrays of intensity values (sparse, zero-intensity omitted)
- 1D numpy arrays of m/z values (or mzbin indices for ion mobility spectra)
- Optional: pandas DataFrames with intensity and m/z columns for convenience
- Extracted ion chromatograms (1D intensity vs. retention time or drift time)
- Arrival time distributions (2D or 3D intensity arrays indexed by RT, DT, m/z)

## How to apply

Load an MZA HDF5 file via h5py with hdf5plugin decompression support. Initialize the mzapy.MZA class, optionally specifying cache_metadata_headers to control in-memory caching of metadata for performance tuning. Call the appropriate collector method based on your analysis goal: collect_ms1_arrays_by_rt() or collect_ms1_arrays_by_rt_dt() for MS1 spectra, collect_ms2_arrays_by_dt() or collect_ms2_arrays_by_rt_dt() for MS2 spectra, collect_xic_arrays_by_mz() for extracted ion chromatograms, or collect_atd_arrays_by_rt_mz() for arrival time distributions. Each method returns intensity and m/z arrays indexed by the queried dimension(s); arrays are sparse (zero-intensity values omitted). For repeated access patterns, invoke load_scan_cache() to accelerate lookups. Always call close() to release file handles when finished.

## Related tools

- **h5py** (HDF5 file reading and dataset/group traversal)
- **hdf5plugin** (HDF5 decompression codec support for compressed spectral arrays)
- **numpy** (In-memory sparse array storage and vectorized intensity/m/z operations)
- **pandas** (Optional tabular representation (DataFrame output) of spectra and metadata)
- **mzapy** (High-level Python interface to MZA HDF5 files with collector methods) — https://github.com/PNNL-m-q/mzapy
- **mza** (Command-line data converter from vendor formats to MZA HDF5) — https://github.com/PNNL-m-q/mza

## Examples

```
from mzapy import MZA; mza = MZA('example.mza', cache_metadata_headers='default'); ms1_spec = mza.collect_ms1_arrays_by_rt(rt=10.5, rt_tol=0.1); mza.close()
```

## Evaluation signals

- Returned intensity and m/z arrays are non-empty and have matching lengths (jagged arrays indexed by Scan ID stored consistently).
- Intensity values are non-negative and total ion current (TIC) from summed intensities matches metadata TIC field.
- m/z values are in valid mass range (e.g., 50–2000 m/z for proteomics) and monotonically increasing within each spectrum.
- Retrieved spectra for a given retention time ± tolerance cluster correctly by drift time dimension if ion mobility is present.
- Extracted ion chromatogram intensities for a specific m/z match the summed intensities of all scans queried at that m/z ± mass tolerance.
- Scan cache (when enabled) reduces repeated array-access latency by >50% compared to uncached lookups on the same file.

## Limitations

- MZA format requires vendor file conversion step via mza.exe; native vendor format access is not supported by mzapy.
- For ion mobility spectra, m/z values are stored as indices (mzbins) into a shared Full_mz_array, not unique per spectrum; this reduces storage but requires index dereferencing.
- Large-scale querying without scan caching can be I/O-bound due to HDF5 random access; pre-load cache via load_scan_cache() for workflows making >1000 lookups.
- Zero-intensity values are omitted in stored arrays; reconstructing full m/z ranges requires external m/z grid definition.
- Metadata columns (retention time, drift time) depend on instrument type (Agilent, Bruker TimsTOF, Thermo, etc.) and may have different units (milliseconds vs. 1/k0); verify units from CCS calibration coefficients in file header.

## Evidence

- [other] mzapy is a Python package that provides an interface to unprocessed MS data in the MZA format, built using h5py and hdf5plugin as core dependencies for HDF5 file access.: "mzapy is a Python package that provides an interface to unprocessed MS data in the MZA format, built using h5py and hdf5plugin as core dependencies"
- [other] Initialize the MZA class with optional cache_metadata_headers parameter to control in-memory caching of metadata.: "The ``cache_metadata_headers`` kwarg is used to control which metadata headers are cached in memory for faster access"
- [other] Implement getter methods for extracted ion chromatograms, arrival time distributions, MS1 spectra, MS2 spectra, and 2D data arrays.: "Implement getter methods for metadata, extracted ion chromatograms (by m/z and m/z + drift time), arrival time distributions (by retention time + m/z), MS1 spectra (by retention time, drift time, or"
- [readme] Spectra are stored omitting zero-intensity values and as two jagged arrays, one in each corresponding group and named as the Scan value in the metadata table.: "Spectra are stored omitting zero-intensity values and as two jagged arrays, one in each corresponding group and named as the "Scan" value in the metadata table"
- [readme] For IM spectra the m/z dimension is stored as indexes (mzbins) into a Full_mz_array common for all spectra.: "For IM spectra the m/z dimension is stored as indexes (mzbins): Arrays_mzbin (HDF5 group) contains 1D arrays with indexes to Full_mz_array"
- [other] Provide scan caching methods to accelerate repeated data access.: "Implement getter methods for metadata, extracted ion chromatograms (by m/z and m/z + drift time), arrival time distributions (by retention time + m/z), MS1 spectra (by retention time, drift time, or"
- [readme] MZA is a stand-alone executable which converts multidimensional mass spectrometry data from vendor formats to the MZA simple data structure based on HDF5.: "MZA is a stand-alone and self-contained command-line executable which converts multidimensional mass spectrometry (MS) data from files in proprietary vendor formats to the MZA simple data structure"
