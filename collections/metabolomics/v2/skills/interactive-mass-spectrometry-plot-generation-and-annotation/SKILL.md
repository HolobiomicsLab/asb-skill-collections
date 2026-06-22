---
name: interactive-mass-spectrometry-plot-generation-and-annotation
description: Use when when you have extracted ion chromatograms (XICs), ion mobilograms (IMs), or mass spectra from diaPASEF or other DIA workflows and need to visualize them interactively to inspect peak boundaries, compare MS1 vs MS2 traces, validate feature identifications, or communicate results.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3937
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MassDash
  - MzMLDataLoader
  - InteractiveTwoDimensionPlotter
  - MRMTransitionGroupPicker
  - pyMRMTransitionGroupPicker
  - Bokeh
  - Plotly
  - MRMTransitionGroupPicker / pyMRMTransitionGroupPicker
derived_from:
- doi: 10.1021/acs.jproteome.4c00026
  title: MassDash
evidence_spans:
- MassDash is a modular and flexible python package that has a streamlit graphical user interface (GUI)
- ':mod:`massdash.loaders`: Classes for loading data'
- MzMLDataLoader
- InteractiveTwoDimensionPlotter
- MRMTransitionGroupPicker
- pyMRMTransitionGroupPicker
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_massdash_cq
    doi: 10.1021/acs.jproteome.4c00026
    title: MassDash
  dedup_kept_from: coll_massdash_cq
schema_version: 0.2.0
---

# interactive-mass-spectrometry-plot-generation-and-annotation

## Summary

Generate interactive one-, two-, and three-dimensional visualizations of extracted ion chromatograms, mobilograms, and spectra from Data-Independent Acquisition mass spectrometry data using Bokeh-backed plotters. This skill enables real-time exploration and annotation of targeted peptide precursors across retention time, ion mobility, and m/z dimensions.

## When to use

When you have extracted ion chromatograms (XICs), ion mobilograms (IMs), or mass spectra from diaPASEF or other DIA workflows and need to visualize them interactively to inspect peak boundaries, compare MS1 vs MS2 traces, validate feature identifications, or communicate results. Use this skill specifically after loading raw DIA data and search results but before or instead of exporting static tabular summaries.

## When NOT to use

- Input is a pre-computed static image or already-rendered static plot (use this skill to generate the interactive version from raw data instead).
- Data lacks retention time or ion mobility dimensions (e.g., single-dimensional spectra without trace context; alternative: generate simple line plots without heatmap overlays).
- Interactive exploration is not required and only static PDF/PNG export for publication is needed (use a static plotting library instead; however, note that MassDash also supports Plotly snapshots for export).

## Inputs

- extracted ion chromatogram (XIC) intensity trace with retention time coordinates
- extracted ion mobilogram (IM) intensity trace with ion mobility coordinates
- mass spectrum (m/z and intensity pairs)
- search result metadata (feature Q-value, retention time, ion mobility, m/z)
- raw DIA mass spectrometry data (mzML format, loaded via MzMLDataLoader)

## Outputs

- interactive Bokeh figure (one-dimensional: extracted spectra, chromatogram, or mobilogram plot)
- interactive Bokeh figure (two-dimensional: retention time vs. ion mobility heatmap)
- interactive Bokeh figure (three-dimensional: spectrum-chromatogram or scatter heatmap plot)
- annotated visualization with peak boundaries and feature metadata overlaid
- HTML rendering with pan, zoom, and hover tooltips for coordinate inspection

## How to apply

Load extracted chromatogram and mobilogram data (raw m/z, retention time, ion mobility coordinates) into MassDash's InteractiveTwoDimensionPlotter, specifying which dimensions to display (e.g., retention time vs. ion mobility as a heatmap, or extracted spectra as line plots). The plotter generates Bokeh-backed interactive HTML figures allowing pan, zoom, and hover inspection of peak coordinates and intensities. For one-dimensional traces, visualize the extracted spectra, chromatogram, and mobilogram individually; for two-dimensional views, render retention time vs. ion mobility heatmaps; for three-dimensional exploration, use spectrum-chromatogram or scatter heatmap plots. Enable optional filtering controls (MS1/MS2 trace toggle, trace smoothing) via the sidebar to allow users to isolate signals of interest. Validate correct application by confirming that peak boundaries, retention times, and ion mobility windows align with metadata from search results (DIA-NN, OpenSwath) at the specified Q-value cutoff (typically 1%).

## Related tools

- **InteractiveTwoDimensionPlotter** (Renders interactive Bokeh figures for two-dimensional retention time vs. ion mobility heatmaps and one-dimensional trace plots (chromatogram, mobilogram, spectra) with hover tooltips and pan/zoom controls.) — https://github.com/Roestlab/massdash
- **Bokeh** (Underlying interactive visualization library that generates HTML figures with client-side interactivity (pan, zoom, hover inspection) for chromatogram and mobilogram displays.)
- **MzMLDataLoader** (Loads and parses raw diaPASEF mass spectrometry data (mzML format) to extract spectra and trace data fed into the interactive plotter.) — https://github.com/Roestlab/massdash
- **Plotly** (Optional secondary visualization engine; supports snapshot export of interactive plots to static image formats.)
- **MRMTransitionGroupPicker / pyMRMTransitionGroupPicker** (Optional peak picking algorithms that can annotate peak boundaries on extracted chromatograms prior to or during interactive visualization.) — https://github.com/Roestlab/massdash

## Examples

```
massdash gui  # Launch the MassDash web interface, load a transition list and DIA data file, select an analyte from the dropdown (filtered at Q-value 1%), then inspect the auto-generated Bokeh chromatogram, mobilogram, and retention time vs. ion mobility heatmap in the main panel.
```

## Evaluation signals

- Verify that peak boundaries identified by OpenSwath or DIA-NN are visually aligned with chromatogram peaks in the interactive plot.
- Confirm that retention time and ion mobility windows from search results match the plotted trace coordinates within measurement precision (e.g., ±0.5 min for RT, ±0.02 Vs/cm² for IM).
- Inspect hover tooltips to confirm intensities, m/z values, and coordinates are populated and match raw data metadata (no null or misaligned values).
- Validate that MS1 and MS2 traces can be toggled on/off via sidebar controls without rendering errors and that trace smoothing produces visually coherent intensity profiles.
- Confirm that Q-value filtering at the specified cutoff (e.g., 1%) populates only analytes meeting that threshold in the selection dropdown.

## Limitations

- Interactive plot generation performance may degrade with very large datasets (many thousands of transitions or high-resolution spectra); consider subsampling or filtering to a region of interest (defined retention time/m/z window) before plotting.
- The provided excerpt does not detail parametric control over figure size, color palettes, or font sizes, limiting customization for accessibility or publication requirements.
- Three-dimensional plots (spectrum-chromatogram, scatter heatmap) are mentioned but technical details on rendering, interaction modality (e.g., 3D rotation), and data dimensionality constraints are not elaborated in the article.
- Peak boundary visualization depends on upstream peak picking output (MRMTransitionGroupPicker); if peak picking is not applied or fails, no boundary annotations will appear.

## Evidence

- [other] The main area will be populated with interactive Bokeh figures: "The main area will be populated with interactive Bokeh figures"
- [other] For one dimensional plots, the user can visualize the extracted spectra, chromatogram and mobilogram: "For one dimensional plots, the user can visualize the extracted spectra, chromatogram and mobilogram"
- [other] Two dimensional plots allow heatmap style visualizations of two dimensions, i.e. retention time vs ion mobility: "Two dimensional plots allow heatmap style visualizations of two dimensions, i.e. retention time vs ion mobility"
- [other] Three dimensional plots allow you to visualize spectrum-chromatogram plots, scatter heatmap plots: "Three dimensional plots allow you to visualize spectrum-chromatogram plots, scatter heatmap plots"
- [other] Extract ion chromatogram (XIC) by applying mass-to-charge (m/z) tolerance window (in ppm), retention time window, and ion mobility window extraction parameters to raw spectra for each selected analyte.: "Extract ion chromatogram (XIC) by applying mass-to-charge (m/z) tolerance window (in ppm), retention time window, and ion mobility window extraction parameters to raw spectra for each selected analyte"
- [other] Generate one-dimensional plots (extracted spectra, chromatogram, mobilogram) and two-dimensional plots (retention time vs. ion mobility heatmap) using InteractiveTwoDimensionPlotter for visualization.: "Generate one-dimensional plots (extracted spectra, chromatogram, mobilogram) and two-dimensional plots (retention time vs. ion mobility heatmap) using InteractiveTwoDimensionPlotter for visualization"
- [other] allows for displaying or hiding MS1 or MS2 traces: "allows for displaying or hiding MS1 or MS2 traces"
- [other] allows for smoothing of the traces: "allows for smoothing of the traces"
