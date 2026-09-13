---
name: spectral-window-extraction
description: Use when you have loaded multidimensional MS data (from MZA HDF5 files
  or other formats) and need to examine a specific m/z region—for example, to visualize
  a known lipid or metabolite mass range, perform peak detection within a narrow window,
  or reduce computational overhead by working on a subset.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - numpy
  - matplotlib.pyplot
  - h5py
  - mzapy.peaks.find_peaks_1d_localmax
  - mzapy.peaks.find_peaks_1d_gauss
  techniques:
  - LC-MS
  - ion-mobility-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.3c01653
  title: mzapy
- doi: 10.1021/acs.jproteome.2c00313
  title: ''
evidence_spans:
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Spectral Window Extraction

## Summary

Extract a bounded m/z range from mass spectrometry spectral data for focused analysis or visualization. This skill isolates intensity and m/z array pairs within a user-specified mass window, enabling targeted examination of specific ion populations without processing the full spectrum.

## When to use

Apply this skill when you have loaded multidimensional MS data (from MZA HDF5 files or other formats) and need to examine a specific m/z region—for example, to visualize a known lipid or metabolite mass range, perform peak detection within a narrow window, or reduce computational overhead by working on a subset of the spectral domain. Use it when your analysis question targets a particular mass-to-charge interval rather than the full spectrum.

## When NOT to use

- Input spectrum is already pre-windowed or has been binned by vendor software — re-windowing may introduce artificial edges or loss of boundary information.
- Analysis requires full-spectrum pattern matching, spectral entropy, or whole-mass-range peak counting — windowing would compromise global spectral features.
- M/z bounds are unknown or not biologically justified — unbounded exploratory analysis should precede window selection.

## Inputs

- m/z array (1D numpy array of mass-to-charge values)
- intensity array (1D numpy array of signal intensities, same length as m/z array)
- lower m/z bound (float)
- upper m/z bound (float)
- optional: scan metadata (retention time, MS level, ion mobility arrival time from MZA metadata table)

## Outputs

- filtered m/z array (1D numpy array, subset of input m/z within window bounds)
- filtered intensity array (1D numpy array, corresponding intensities)
- window bounds applied (tuple of float, for documentation)
- count of data points retained (integer, for QC)

## How to apply

Accept m/z and intensity array pairs from the source spectrum along with explicit lower and upper m/z bounds. Filter the input arrays to retain only data points where m/z values fall within [lower_bound, upper_bound], preserving the correspondence between m/z and intensity. Return the filtered coordinate arrays and any associated metadata (scan number, retention time, MS level). The window extraction is typically applied before plotting (via matplotlib line or stem plots) or before applying peak-detection functions such as find_peaks_1d_localmax or find_peaks_1d_gauss. Ensure window bounds are biologically meaningful for the analyte class and acquisition method (e.g., lipid m/z ranges for lipidomics, or precursor isolation windows for MS2).

## Related tools

- **matplotlib.pyplot** (render windowed m/z vs. intensity arrays as line or stem plots for interactive or file-based visualization)
- **numpy** (perform boolean indexing and array slicing to filter m/z and intensity pairs based on window bounds)
- **h5py** (load m/z and intensity arrays from MZA HDF5 datasets (Arrays_mz and Arrays_intensity groups) for windowing) — https://github.com/PNNL-m-q/mza
- **mzapy.peaks.find_peaks_1d_localmax** (perform peak detection on windowed 1D intensity arrays after extraction) — https://github.com/PNNL-m-q/mzapy
- **mzapy.peaks.find_peaks_1d_gauss** (fit Gaussian peaks to windowed spectral data for more precise peak characterization) — https://github.com/PNNL-m-q/mzapy

## Examples

```
import h5py; import numpy as np; f = h5py.File('example.mza', 'r'); mz = f['Arrays_mz/630'][:]; intensity = f['Arrays_intensity/630'][:]; window_mask = (mz >= 400.0) & (mz <= 600.0); mz_windowed = mz[window_mask]; intensity_windowed = intensity[window_mask]; print(f'Extracted {len(mz_windowed)} points in m/z [400.0, 600.0]')
```

## Evaluation signals

- All returned m/z values lie within [lower_bound, upper_bound]; check min(filtered_mz) >= lower_bound and max(filtered_mz) <= upper_bound.
- Filtered arrays have equal length and correspond 1:1 (no offset or dropout).
- Count of retained points is non-zero and consistent with expected spectral density; a zero-length window typically indicates out-of-range bounds.
- Visualization of windowed spectrum shows clean isolation of the target m/z region with no data bleeding outside the defined interval.
- Downstream peak detection (find_peaks_1d_localmax or find_peaks_1d_gauss) runs without error and yields peaks only within the window bounds.

## Limitations

- Window extraction does not handle overlapping or nested windows; multiple extractions require sequential calls.
- No automatic resampling or interpolation at window edges; boundary m/z values are included or excluded exactly as specified.
- For ion-mobility-resolved spectra (IonMobilityBin > 0), window extraction operates on single (m/z, intensity) arrays; extraction across IM bins requires separate m/z-bin lookup via Arrays_mzbin and Full_mz_array.
- Very narrow windows (< 0.01 m/z units) may yield sparse data and compromise peak fitting; no warning is issued if point count falls below a recommended threshold.

## Evidence

- [other] Accept input arrays (m/z values, intensity values) and optional parameters (m/z range, color, label, figsize).: "Accept input arrays (m/z values, intensity values) and optional parameters (m/z range, color, label, figsize)."
- [other] Plot intensity as a line or stem plot against m/z values using matplotlib.pyplot, respecting the specified m/z range window.: "Plot intensity as a line or stem plot against m/z values using matplotlib.pyplot, respecting the specified m/z range window."
- [readme] Spectra are stored omitting zero-intensity values and as two jagged arrays, one in each corresponding group and named as the 'Scan' value in the metadata table: * Arrays_intensity (HDF5 group): contains 1D arrays with intensity values. * Arrays_mz (HDF5 group): contains 1D arrays with mass-to-charge (m/z) values.: "Spectra are stored omitting zero-intensity values and as two jagged arrays, one in each corresponding group and named as the 'Scan' value in the metadata table: * Arrays_intensity (HDF5 group):"
- [other] mzapy provides a Python interface to unprocessed MS data in the MZA format, with matplotlib as a dependency for visualization operations.: "mzapy provides a Python interface to unprocessed MS data in the MZA format, with matplotlib as a dependency for visualization operations."
- [other] Return ax for further customization, display interactively if figname='show', or save to file if figname contains a path using plt.savefig.: "Return ax for further customization, display interactively if figname='show', or save to file if figname contains a path using plt.savefig."
