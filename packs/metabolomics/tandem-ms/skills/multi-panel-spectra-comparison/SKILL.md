---
name: multi-panel-spectra-comparison
description: Use when when you need to visually compare two or more spectra (MS1, MS2, or extracted ion chromatograms) across different retention times, m/z ranges, or ion mobility bins in a single figure. Apply this skill after extracting spectra arrays from MZA files (e.
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
  - mzapy.MZA
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

# multi-panel-spectra-comparison

## Summary

Render and compare multiple mass spectra side-by-side or in a grid layout using matplotlib, enabling visual inspection of spectral differences across retention time, m/z windows, MS levels, or ion mobility conditions. This skill is essential for quality assessment and pattern recognition in multidimensional mass spectrometry workflows.

## When to use

When you need to visually compare two or more spectra (MS1, MS2, or extracted ion chromatograms) across different retention times, m/z ranges, or ion mobility bins in a single figure. Apply this skill after extracting spectra arrays from MZA files (e.g., via collect_ms1_arrays_by_rt, collect_ms2_arrays_by_dt, or collect_xic_arrays_by_mz) and before reporting or archiving results. Typical triggers: validating peak picking consistency, comparing fragmentation patterns across adducts, or inspecting ion mobility separation quality.

## When NOT to use

- Input is a single spectrum — use plot_spectrum directly instead of multi-panel layout.
- Spectra have incompatible m/z ranges or vastly different intensity scales that cannot be meaningfully compared on a single display — consider normalization or separate figure groups first.
- The goal is statistical comparison (e.g., cosine similarity, peak overlap quantification) rather than visual inspection — use dedicated similarity metrics instead of visualization.

## Inputs

- m/z value arrays (1D numpy arrays)
- intensity value arrays (1D numpy arrays, same length as m/z arrays)
- spectrum metadata (retention time, scan number, MS level, ion mobility bin — optional but recommended for labeling)
- optional m/z range windows [min_mz, max_mz] per subplot
- optional figure dimensions (figsize tuple)
- optional color and label strings per spectrum

## Outputs

- matplotlib Figure object with multiple Axes (one per spectrum)
- interactive display (if figname='show')
- saved PNG/PDF/SVG file (if figname contains a valid file path)

## How to apply

Create a figure with subplots (one per spectrum or spectral pair) using matplotlib.pyplot.subplots() with explicit row/column layout. For each subplot, call the plot_spectrum function (or equivalent line/stem plot) with the corresponding m/z and intensity arrays, respecting optional m/z range windows. Apply consistent axis scaling, color schemes, and labeling across panels to enable visual comparison. Use the decorator _setup_and_save_or_show_plot to handle figure initialization, legend placement, and output routing (display interactively via 'show', or save to a file path). Return the figure object for further customization or directly display/save based on the figname parameter.

## Related tools

- **matplotlib.pyplot** (provides subplots(), line/stem plotting functions, and figure management for multi-panel rendering)
- **numpy** (provides array slicing, windowing, and masking for m/z range filtering and intensity manipulation)
- **mzapy.view.plot_spectrum** (core function that renders a single spectrum; wrapped in decorator for output routing; called per subplot) — https://github.com/PNNL-m-q/mzapy
- **mzapy.MZA** (provides methods collect_ms1_arrays_by_rt, collect_ms2_arrays_by_dt, collect_xic_arrays_by_mz, collect_atd_arrays_by_rt_mz to extract spectrum arrays for comparison) — https://github.com/PNNL-m-q/mzapy

## Examples

```
import matplotlib.pyplot as plt; from mzapy.view import plot_spectrum; fig, axes = plt.subplots(1, 2, figsize=(12, 4)); plot_spectrum(mz_array_1, intensity_1, ax=axes[0], label='MS1 RT=5.2min'); plot_spectrum(mz_array_2, intensity_2, ax=axes[1], label='MS1 RT=5.3min', mz_range=[100, 1000]); plt.savefig('spectrum_comparison.png')
```

## Evaluation signals

- All subplots render without error and display correct m/z and intensity ranges.
- Axis labels, titles, and legends are consistent and readable across panels.
- Spectra are visually alignable (same m/z window and intensity scaling per row/column group, unless intentionally varied).
- Output file (if saved) is valid and opens in standard image viewers or PDF readers.
- Visual inspection confirms expected patterns (e.g., precursor peaks in MS1 at expected m/z, MS2 fragments lower m/z; or consistent peak position across ion mobility bins).

## Limitations

- Very large numbers of spectra (>100 panels) may create cluttered, unreadable figures; consider filtering or pagination strategies.
- Matplotlib's default color palette has limited distinct colors; manual color assignment recommended for >10 spectra.
- The MZA format stores spectra as sparse (omitting zero-intensity values); ensure proper m/z window slicing to avoid misleading gaps.
- Ion mobility spectra (with mzbin indexing) require conversion from mzbins to Full_mz_array before comparison; see MZA HDF5 structure documentation.
- No built-in interactive zoom/pan in static output; use matplotlib's interactive mode ('show') for exploration, or export to interactive formats (e.g., plotly) for archival.

## Evidence

- [other] Initialize matplotlib figure and axis using _setup_and_save_or_show_plot decorator or accept existing ax: "Initialize matplotlib figure and axis using _setup_and_save_or_show_plot decorator or accept existing ax."
- [other] Plot intensity as a line or stem plot against m/z values using matplotlib.pyplot, respecting the specified m/z range window: "Plot intensity as a line or stem plot against m/z values using matplotlib.pyplot, respecting the specified m/z range window."
- [other] Return ax for further customization, display interactively if figname='show', or save to file if figname contains a path using plt.savefig: "Return ax for further customization, display interactively if figname='show', or save to file if figname contains a path using plt.savefig."
- [readme] Spectra are stored omitting zero-intensity values and as two jagged arrays, one in each corresponding group and named as the "Scan" value in the metadata table: "Spectra are stored omitting zero-intensity values and as two jagged arrays, one in each corresponding group and named as the "Scan" value in the metadata table:"
- [other] MS1 Spectra ... MS2 Spectra ... 2-Dimensional Data ... Extracted Ion Chromatograms ... Arrival Time Distributions: "MS1 Spectra ... MS2 Spectra ... 2-Dimensional Data ... Extracted Ion Chromatograms ... Arrival Time Distributions"
