---
name: interactive-plot-generation
description: Use when you have loaded m/z and intensity arrays from an MZA file (via
  mzapy) and need to inspect a mass spectrum, extracted ion chromatogram (XIC), or
  arrival time distribution (ATD) visually, either for QC purposes, method development,
  or publication-ready output.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - numpy
  - matplotlib
  - mzapy
  - h5py
  techniques:
  - mass-spectrometry
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

# interactive-plot-generation

## Summary

Generate interactive matplotlib visualizations of mass spectrometry data (spectrum plots, chromatograms, mobility distributions) from HDF5-stored m/z and intensity arrays in MZA format. This skill enables rapid visual inspection and customization of multidimensional MS data before downstream analysis.

## When to use

Apply this skill when you have loaded m/z and intensity arrays from an MZA file (via mzapy) and need to inspect a mass spectrum, extracted ion chromatogram (XIC), or arrival time distribution (ATD) visually, either for QC purposes, method development, or publication-ready output. Use it when you want to overlay multiple spectra, apply m/z range filters, or export figures to disk.

## When NOT to use

- Input arrays are not paired or have mismatched lengths — validate array shape consistency before calling.
- Data has not yet been extracted from the MZA file or is still in HDF5 dataset form — use mzapy data collection methods (collect_ms1_arrays_by_rt, collect_xic_arrays_by_mz, etc.) first.
- You need statistical peak detection or quantification, not visual inspection — use mzapy.peaks.find_peaks_1d_localmax or find_peaks_1d_gauss instead.

## Inputs

- m/z array (1D numpy array of mass-to-charge ratios)
- intensity array (1D numpy array of signal intensities)
- optional m/z range window (tuple: [min_mz, max_mz])
- optional matplotlib axis object (ax)
- optional plot parameters (color, label, figsize)

## Outputs

- matplotlib axis object (ax) with plotted spectrum
- interactive display (if figname='show')
- saved figure file (if figname contains a file path)

## How to apply

Accept paired 1D input arrays: m/z values and corresponding intensity values (optionally filtered by a user-specified m/z range window). Initialize a matplotlib figure and axis, optionally accepting a pre-existing axis for subplot integration. Plot intensity as a line or stem plot against m/z using matplotlib.pyplot, respecting the specified m/z range bounds. Apply customizations including line color, axis labels, plot title or legend (if a label is provided). Return the axis object to enable further manipulation, display the plot interactively (figname='show'), or persist to disk via plt.savefig(figname) if a file path is provided. The decorator _setup_and_save_or_show_plot abstracts these display/save decisions.

## Related tools

- **matplotlib** (Core rendering engine for figure creation, axis setup, line/stem plotting, and interactive/file-based display control)
- **numpy** (Array manipulation and filtering (e.g., boolean indexing for m/z range windowing))
- **mzapy** (Data loading and array extraction from MZA HDF5 files (collect_ms1_arrays_by_rt, collect_xic_arrays_by_mz, collect_atd_arrays_by_rt_mz)) — https://github.com/PNNL-m-q/mzapy
- **h5py** (Low-level HDF5 file access (wrapped by mzapy but may be used directly for custom data retrieval))

## Examples

```
from mzapy.view import plot_spectrum; import numpy as np; mz_arr = np.array([400.1, 401.2, 450.5, 500.3]); intensity_arr = np.array([1000, 5000, 3000, 2000]); ax = plot_spectrum(mz_arr, intensity_arr, mz_range=[400, 510], color='blue', label='MS1 Scan 100', figname='spectrum.png')
```

## Evaluation signals

- Axis object is returned and contains a plotted line or stem series with non-zero data points corresponding to input m/z and intensity arrays.
- If m/z range filtering is applied, verify that all plotted points fall within [min_mz, max_mz] bounds and that points outside this range are absent.
- If figname='show', plot appears in an interactive window; if figname is a file path, the file is created and is valid (file size > 0, format matches expected suffix).
- Axis labels, legend (if label provided), and color customizations are correctly applied and visible in the rendered output.
- Multiple invocations on the same axis (passed as parameter) correctly overlay spectra without clearing previous data; single invocation with no ax parameter creates a new figure.

## Limitations

- Performance degrades for very large arrays (>>100k points); consider downsampling or subsampling m/z windows for real-time interaction.
- stem plots can become visually cluttered when m/z ranges are very wide; narrow the m/z range window or switch to line plots for dense spectra.
- Interactive display (figname='show') requires a display environment (X11, GUI backend); will fail in headless contexts unless redirected to file output.
- No built-in mass accuracy validation or unit conversion; assumes input m/z values are in Daltons and intensity in arbitrary units as stored in MZA.
- Overlay of multiple spectra on the same axis requires manual loop and axis reuse; no built-in spectral alignment or normalization.

## Evidence

- [other] 1. Accept input arrays (m/z values, intensity values) and optional parameters (m/z range, color, label, figsize). 2. Initialize matplotlib figure and axis using _setup_and_save_or_show_plot decorator or accept existing ax.: "Accept input arrays (m/z values, intensity values) and optional parameters (m/z range, color, label, figsize). 2. Initialize matplotlib figure and axis using _setup_and_save_or_show_plot decorator or"
- [other] 3. Plot intensity as a line or stem plot against m/z values using matplotlib.pyplot, respecting the specified m/z range window.: "Plot intensity as a line or stem plot against m/z values using matplotlib.pyplot, respecting the specified m/z range window."
- [other] 4. Customize plot appearance (color, label, axis labels) and conditionally add legend if label is provided. 5. Return ax for further customization, display interactively if figname='show', or save to file if figname contains a path using plt.savefig.: "Customize plot appearance (color, label, axis labels) and conditionally add legend if label is provided. 5. Return ax for further customization, display interactively if figname='show', or save to"
- [other] A Python package that provides an interface to unprocessed MS data in the MZA format, with matplotlib as a dependency for visualization operations.: "mzapy provides a Python interface to unprocessed MS data in the MZA format, with matplotlib as a dependency for visualization operations."
- [readme] Spectra are stored omitting zero-intensity values and as two jagged arrays, one in each corresponding group and named as the "Scan" value in the metadata table: * Arrays_intensity (HDF5 group): contains 1D arrays with intensity values. * Arrays_mz (HDF5 group): contains 1D arrays with mass-to-charge (m/z) values.: "Spectra are stored omitting zero-intensity values and as two jagged arrays, one in each corresponding group: Arrays_intensity (HDF5 group): contains 1D arrays with intensity values. Arrays_mz (HDF5"
