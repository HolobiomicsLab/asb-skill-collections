---
name: mass-spectrum-m-z-alignment
description: Use when when working with multidimensional MS data (LC–IM–MS/MS) converted to MZA format where spectra are stored in jagged arrays with m/z values distributed across individual HDF5 datasets per scan, and you need to ensure m/z consistency for downstream peak detection, isotope analysis, or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - scipy
  - numpy
  - h5py
  - scipy.signal.find_peaks
  - mzapy.peaks.find_peaks_1d_localmax
  - mzapy
derived_from:
- doi: 10.1021/acs.analchem.3c01653
  title: mzapy
- doi: 10.1021/acs.jproteome.2c00313
  title: ''
evidence_spans:
- Dependencies ------------------------------ * ``scipy``
- '* ``scipy``'
- '* ``numpy``'
- Dependencies ------------------------------ * ``numpy``
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

# mass-spectrum-m-z-alignment

## Summary

Align and access mass-to-charge (m/z) values across multidimensional mass spectrometry spectra stored in HDF5-based MZA format. This skill enables consistent m/z referencing for peak detection, feature extraction, and comparative analysis across LC, ion mobility, and fragmentation dimensions.

## When to use

When working with multidimensional MS data (LC–IM–MS/MS) converted to MZA format where spectra are stored in jagged arrays with m/z values distributed across individual HDF5 datasets per scan, and you need to ensure m/z consistency for downstream peak detection, isotope analysis, or cross-scan feature alignment.

## When NOT to use

- Input is already a processed feature table or consensus m/z list (e.g., from vendor software or mzML with centroided peaks); use this skill only on raw or profile-mode MS data stored in MZA format.
- m/z values are pre-aligned in a single flat array; this skill addresses the jagged/partitioned HDF5 storage model specific to MZA.
- Analysis requires vendor-specific m/z calibration coefficients not present in the MZA metadata (e.g., CCS calibration data may be missing for some instruments).

## Inputs

- MZA file (HDF5 format) with metadata table and Arrays_mz / Arrays_mzbin groups
- Spectrum scan identifier (numeric or string from metadata Scan column)
- Ion mobility frame index (for IM spectra; optional)
- Full_mz_array dataset (for ion mobility spectra; optional)

## Outputs

- Aligned m/z array (1D numpy array, monotonically increasing)
- Aligned intensity array (1D numpy array, same length as m/z array)
- Peak detection results (indices, heights, prominence from scipy.signal.find_peaks or mzapy.peaks functions)

## How to apply

Load the MZA file using h5py and access the metadata table to identify the spectrum properties (scan number, ion mobility frame, MS level). For standard MS spectra, retrieve the corresponding m/z array from the Arrays_mz group using the scan identifier. For ion mobility spectra, use the Full_mz_array (common across all frames) and access the mzbins indices from Arrays_mzbin to reconstruct the m/z values for each spectrum. Validate m/z ordering (must be monotonically increasing) and check intensity alignment against the corresponding Arrays_intensity dataset. Use scipy.signal.find_peaks or mzapy.peaks functions on the aligned intensity–m/z pairs to detect peaks. The m/z alignment is correct when peak indices map consistently between the m/z and intensity arrays.

## Related tools

- **h5py** (Read and access m/z and intensity arrays from MZA HDF5 files)
- **numpy** (Align and validate m/z and intensity arrays; ensure monotonic ordering)
- **scipy.signal.find_peaks** (Detect peaks in aligned intensity arrays using threshold and prominence parameters)
- **mzapy.peaks.find_peaks_1d_localmax** (Perform peak fitting on aligned 1D m/z–intensity profiles using local maxima detection) — https://github.com/PNNL-m-q/mzapy
- **mzapy** (High-level interface to load MZA data and access spectrum arrays by scan identifier) — https://github.com/PNNL-m-q/mzapy

## Examples

```
import h5py; import numpy as np; from scipy import signal; f = h5py.File('data.mza', 'r'); mz = np.array(f['Arrays_mz/630']); intensity = np.array(f['Arrays_intensity/630']); peaks, props = signal.find_peaks(intensity, prominence=10); print(f'Peaks at m/z: {mz[peaks]}')
```

## Evaluation signals

- m/z array is monotonically increasing and has no NaN or infinite values
- m/z and intensity arrays have identical length and index alignment (peak_index in m/z array corresponds to same intensity_index in intensity array)
- Detected peak count and positions match synthetic ground truth or cross-validate with vendor software output
- For IM spectra: mzbins indices are within bounds of Full_mz_array and correctly reconstruct the expected m/z range
- Metadata Scan value and MzaPath correctly locate the corresponding HDF5 datasets without 'dataset not found' errors

## Limitations

- MZA format omits zero-intensity values; m/z alignment assumes no gaps in the stored jagged arrays, which may affect peak boundary and baseline estimation.
- Ion mobility spectra use a common Full_mz_array across all frames; this shared reference may not account for drift or instrument recalibration during a long acquisition.
- m/z accuracy depends on vendor calibration coefficients (CCScalDT, CCScalTIMS, CCScalSLIM) stored in the MZA file; missing or stale calibration will propagate to downstream peak detection.
- Large files with many spectra may be partitioned into multiple HDF5 groups (indicated by MzaPath field); code must handle dynamic partition routing to avoid dataset lookup failures.

## Evidence

- [readme] Spectra are stored omitting zero-intensity values and as two jagged arrays, one in each corresponding group and named as the "Scan" value in the metadata table: Arrays_intensity (HDF5 group): contains 1D arrays with intensity values. Arrays_mz (HDF5 group): contains 1D arrays with mass-to-charge (m/z) values.: "Spectra are stored omitting zero-intensity values and as two jagged arrays, one in each corresponding group and named as the "Scan" value in the metadata table: Arrays_intensity (HDF5 group):"
- [readme] For IM spectra the m/z dimension is stored as indexes (mzbins): Arrays_mzbin (HDF5 group): contains 1D arrays with indexes to Full_mz_array. Full_mz_array (HDF5 dataset): 1D array of full m/z values common for all spectra in the file.: "For IM spectra the m/z dimension is stored as indexes (mzbins): Arrays_mzbin (HDF5 group): contains 1D arrays with indexes to Full_mz_array. Full_mz_array (HDF5 dataset): 1D array of full m/z values"
- [other] Two functions are provided for performing peak fitting on 1-dimensional data: mzapy.peaks.find_peaks_1d_localmax and mzapy.peaks.find_peaks_1d_gauss: "Two functions are provided for performing peak fitting on 1-dimensional data: mzapy.peaks.find_peaks_1d_localmax and mzapy.peaks.find_peaks_1d_gauss"
- [other] Call scipy.signal.find_peaks on the intensity array with appropriate threshold and prominence parameters to identify local maxima. Extract peak indices, heights, and prominence values from the scipy output.: "Call scipy.signal.find_peaks on the intensity array with appropriate threshold and prominence parameters to identify local maxima. Extract peak indices, heights, and prominence values from the scipy"
- [readme] Partitions may be created for files with too many spectra. Having too many datasets within a single group can slow down data reading performance. HDF5 is more efficient when using multiple groups instead of storing many datasets within one group.: "Partitions may be created for files with too many spectra. Having too many datasets within a single group can slow down data reading performance. HDF5 is more efficient when using multiple groups"
