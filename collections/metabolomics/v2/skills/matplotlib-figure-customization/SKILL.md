---
name: matplotlib-figure-customization
description: 'Use when when rendering spectrum data (m/z vs. intensity arrays) from MZA files and need to control visual presentation: applying m/z range windows, setting line colors and labels for legend identification, sizing the figure, or choosing between interactive display versus file export.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - matplotlib
  - numpy
  - mzapy
derived_from:
- doi: 10.1021/acs.analchem.3c01653
  title: mzapy
- doi: 10.1021/acs.jproteome.2c00313
  title: ''
evidence_spans:
- Dependencies ------------------------------ * ``matplotlib``
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
---

# matplotlib-figure-customization

## Summary

Customize and configure matplotlib figures for mass spectrometry data visualization by adjusting plot appearance (colors, labels, legends), axis ranges, and output format. This skill ensures publication-ready spectrum plots with proper annotation and interactive or file-based display.

## When to use

When rendering spectrum data (m/z vs. intensity arrays) from MZA files and need to control visual presentation: applying m/z range windows, setting line colors and labels for legend identification, sizing the figure, or choosing between interactive display versus file export.

## When NOT to use

- Input arrays are not aligned (different lengths or incompatible data types)—verify array shapes and dtypes before calling.
- m/z range window is invalid (e.g., mz_min >= mz_max or outside data bounds)—validate range before passing.
- Figure already fully rendered and closed—the Axes object must remain open to accept customization.

## Inputs

- m/z array (1D numpy float array)
- intensity array (1D numpy float array, same length as m/z array)
- optional m/z range tuple (mz_min, mz_max) for windowing
- optional matplotlib axis object (ax) for reuse
- optional figure size tuple (figsize)
- optional color string (e.g., 'blue', '#FF5733')
- optional label string for legend
- optional figname string ('show' or file path)

## Outputs

- matplotlib Axes object (customized and ready for display or further modification)
- interactive plot window (if figname='show')
- saved image file in PNG/PDF/other format (if figname contains valid path)

## How to apply

After initializing a matplotlib figure and axis (via mzapy's _setup_and_save_or_show_plot decorator or by accepting an existing ax), apply customization in the following order: (1) Plot intensity data as a line or stem plot against m/z values using matplotlib.pyplot, respecting the m/z range window by slicing or filtering input arrays; (2) Set axis labels, title, and other textual properties; (3) Apply color and line style to match the provided color parameter; (4) Conditionally add a legend if a label string is provided; (5) Return the ax object for further downstream customization, or trigger display by passing figname='show' for interactive viewing, or pass figname with a file path to save via plt.savefig(). The choice between line and stem plot depends on spectral resolution and density—stem plots clarify individual peaks in sparse spectra.

## Related tools

- **matplotlib** (Core library for creating and customizing static and interactive 2D plots of m/z vs. intensity spectra) — https://matplotlib.org/
- **numpy** (Provides efficient array slicing, filtering, and masking for windowing m/z and intensity data before plotting) — https://numpy.org/
- **mzapy** (Loads MZA-format MS data files and provides integration with matplotlib via _setup_and_save_or_show_plot decorator and plot_spectrum function) — https://github.com/PNNL-m-q/mzapy

## Examples

```
import numpy as np
import matplotlib.pyplot as plt
from mzapy.view import plot_spectrum
mz_data = np.array([100.0, 101.5, 103.2])
intensity_data = np.array([500, 1200, 300])
ax = plot_spectrum(mz_data, intensity_data, mz_range=(100, 104), color='blue', label='MS1 Scan 630', figsize=(10, 6))
plt.show()
```

## Evaluation signals

- Plotted data visually spans the specified m/z range window without truncation artifacts or data loss outside bounds.
- Axis labels, title, and legend (if provided) are correctly formatted, readable, and positioned.
- Color and line style are applied as specified; stem vs. line plot choice matches spectral density (sparse → stem, dense → line).
- Output file (if figname is a path) is created with correct format, non-zero file size, and readable by standard image viewers.
- Interactive display (figname='show') opens a responsive window; returned ax object can be queried for limits, labels, and data (e.g., ax.get_xlim(), ax.get_lines())

## Limitations

- Large spectra (>100k points) may render slowly or consume significant memory; consider downsampling or using stem plot for clarity.
- m/z and intensity arrays must be 1D and same length; no automatic broadcasting or resampling is performed.
- Figure resolution and DPI depend on matplotlib backend and figsize; output quality may vary across platforms and display contexts.
- Legend placement is automatic; overlapping labels or crowded legends may obscure plot data—manual positioning via ax.legend(loc=...) may be required.

## Evidence

- [other] Plot intensity as a line or stem plot against m/z values using matplotlib.pyplot, respecting the specified m/z range window: "Plot intensity as a line or stem plot against m/z values using matplotlib.pyplot, respecting the specified m/z range window."
- [other] Accept input arrays (m/z values, intensity values) and optional parameters (m/z range, color, label, figsize): "Accept input arrays (m/z values, intensity values) and optional parameters (m/z range, color, label, figsize)."
- [other] Customize plot appearance (color, label, axis labels) and conditionally add legend if label is provided: "Customize plot appearance (color, label, axis labels) and conditionally add legend if label is provided."
- [other] Return ax for further customization, display interactively if figname='show', or save to file if figname contains a path using plt.savefig: "Return ax for further customization, display interactively if figname='show', or save to file if figname contains a path using plt.savefig."
- [other] mzapy provides a Python interface to unprocessed MS data in the MZA format, with matplotlib as a dependency for visualization operations: "mzapy provides a Python interface to unprocessed MS data in the MZA format, with matplotlib as a dependency for visualization operations."
