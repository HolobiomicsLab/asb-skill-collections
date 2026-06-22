---
name: mass-spectrum-visualization
description: Use when when you have extracted m/z and intensity arrays from an MZA file (or similar HDF5-backed MS data structure) and need to visually inspect a single MS1 or MS2 spectrum, verify peak characteristics, or diagnose data quality issues before downstream analysis (peak fitting, isotope pattern.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - numpy
  - matplotlib.pyplot
  - mzapy.view.plot_spectrum
  - mzapy.peaks.find_peaks_1d_localmax
  techniques:
  - ion-mobility-MS
  - tandem-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrum-visualization

## Summary

Render mass spectrometry intensity data as an interactive 2D plot (intensity vs. m/z) using matplotlib, with support for m/z range windowing, custom styling, and conditional output (display, save, or return axes object). Essential for inspecting spectral quality, peak distribution, and data validity in MS workflows.

## When to use

When you have extracted m/z and intensity arrays from an MZA file (or similar HDF5-backed MS data structure) and need to visually inspect a single MS1 or MS2 spectrum, verify peak characteristics, or diagnose data quality issues before downstream analysis (peak fitting, isotope pattern recognition, or quantification).

## When NOT to use

- Input m/z and intensity arrays are not paired or have mismatched lengths — validate array shape before calling.
- Data is already a 2D chromatogram (retention time × m/z) or 3D tensor (RT × IM × m/z) — use a 2D heatmap or contour plot instead via mzapy.view functions for chromatograms or ion mobility distributions.
- You need statistical analysis of peak properties (height, area, width, signal-to-noise) — defer to mzapy.peaks.find_peaks_1d_localmax or find_peaks_1d_gauss for peak detection and quantification.

## Inputs

- numpy.ndarray of m/z values (1D, float64)
- numpy.ndarray of intensity values (1D, float64, same length as m/z)
- optional m/z range tuple (min_mz, max_mz) to window the spectrum
- optional matplotlib.axes.Axes object for overlay on existing figure
- optional color string (e.g., 'blue', '#FF5733')
- optional label string for legend
- optional figsize tuple (width, height in inches)
- optional figname string ('show' for interactive display, file path for save, or None to return ax only)

## Outputs

- matplotlib.axes.Axes object with plotted spectrum
- optional: PNG/PDF/SVG file saved to disk (if figname contains a path)
- optional: interactive matplotlib figure displayed in notebook or GUI (if figname='show')

## How to apply

Accept paired 1D numpy arrays of m/z values and intensity values, along with optional parameters: m/z range window (to focus on a spectral region), line or stem plot style, custom color, and axis labels. Initialize a matplotlib figure and axis (via decorator or user-supplied ax), plot intensity as a function of m/z respecting the specified window, apply styling (color, label, axis labels), and conditionally add a legend if a label is provided. Return the axes object for further customization, display interactively if figname='show', or save to a file path via plt.savefig. The decorator pattern (_setup_and_save_or_show_plot) centralizes figure lifecycle management.

## Related tools

- **matplotlib.pyplot** (Low-level plotting backend; provides figure, axis, line/stem plot, savefig, and show functions) — https://matplotlib.org
- **numpy** (Array storage and slicing; enables windowing of m/z and intensity arrays by index or value range) — https://numpy.org
- **mzapy.view.plot_spectrum** (High-level wrapper function implementing this skill; encapsulates decorator, plot logic, and output routing) — https://github.com/PNNL-m-q/mzapy
- **mzapy.peaks.find_peaks_1d_localmax** (Complementary peak detection on 1D spectrum; identifies local maxima in intensity for annotation or ROI extraction) — https://github.com/PNNL-m-q/mzapy

## Examples

```
from mzapy.view import plot_spectrum; import numpy as np; mz = np.array([100.5, 101.2, 102.8, ...], dtype=float); intensity = np.array([150, 450, 200, ...], dtype=float); ax = plot_spectrum(mz, intensity, mz_range=(100, 103), label='MS1 Scan 42', figname='show')
```

## Evaluation signals

- Plotted m/z axis spans the requested window (or full data range if no window specified); inspect axis limits via ax.get_xlim().
- Intensity values are correctly mapped to y-axis; verify by comparing plot peak heights to raw array max/min.
- Line or stem plot is visually continuous with no gaps unless m/z values are non-contiguous in the input array.
- If figname='show', plot appears interactively; if figname is a path, verify file exists and is readable; if figname is None, ax object is returned without side effects.
- Legend is present if and only if a label was provided; verify ax.get_legend() is not None when label is set.

## Limitations

- Performance degrades for very large spectra (>100k points); consider downsampling or focusing on a narrow m/z range before plotting.
- Decorator assumes caller has matplotlib imported and configured; mixing manual plt.show() calls with decorator-managed output may cause unexpected figure lifecycle behavior.
- m/z windowing is applied after plotting; if array is very large, consider slicing arrays in-memory before calling plot_spectrum to reduce rendering overhead.
- No built-in support for overlaying multiple spectra or adding reference spectra; use separate plot_spectrum calls with different ax objects or manually overlay via ax.plot().
- Interactive display (figname='show') requires a live matplotlib backend; headless environments or non-interactive shells will fail silently or raise an error.

## Evidence

- [other] Accept input arrays (m/z values, intensity values) and optional parameters (m/z range, color, label, figsize). Initialize matplotlib figure and axis using _setup_and_save_or_show_plot decorator or accept existing ax.: "Accept input arrays (m/z values, intensity values) and optional parameters (m/z range, color, label, figsize). Initialize matplotlib figure and axis using _setup_and_save_or_show_plot decorator or"
- [other] Plot intensity as a line or stem plot against m/z values using matplotlib.pyplot, respecting the specified m/z range window.: "Plot intensity as a line or stem plot against m/z values using matplotlib.pyplot, respecting the specified m/z range window."
- [other] Return ax for further customization, display interactively if figname='show', or save to file if figname contains a path using plt.savefig.: "Return ax for further customization, display interactively if figname='show', or save to file if figname contains a path using plt.savefig."
- [readme] A Python package that provides an interface to unprocessed MS data in the MZA format.: "A Python package that provides an interface to unprocessed MS data in the MZA format."
- [other] mzapy provides a Python interface to unprocessed MS data in the MZA format, with matplotlib as a dependency for visualization operations.: "mzapy provides a Python interface to unprocessed MS data in the MZA format, with matplotlib as a dependency for visualization operations."
