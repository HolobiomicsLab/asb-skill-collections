---
name: interactive-plot-customization-bokeh
description: Use when when you have loaded extracted ion chromatogram traces (via SqMassLoader from sqMass files) and need to render them as interactive web-based visualizations where users can pan, zoom, hover for metadata, mute individual traces, and optionally visualize peak boundaries from OpenSwath results.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0571
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - SqMassLoader
  - massdash.plotting.InteractivePlotter
  - Bokeh
  - massdash.peakPickers.MRMTransitionGroupPicker
  - massdash.peakPickers.pyMRMTransitionGroupPicker
  - massdash.structs.FeatureMap
  - massdash.loaders.ResultsLoader
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1021/acs.jproteome.4c00026
  title: MassDash
evidence_spans:
- 'Chromatogram Loaders: Raw data stores chromatograms, this allows for faster loading however since extraction has already been performed by the upstream analysis tool. This includes SqMassLoader'
- InteractivePlotter
- The main area will be populated with interactive Bokeh figures
- MRMTransitionGroupPicker
- pyMRMTransitionGroupPicker
- FeatureMap
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.4c00026
  all_source_dois:
  - 10.1021/acs.jproteome.4c00026
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Interactive Plot Customization with Bokeh

## Summary

Configure and render interactive mass spectrometry chromatogram visualizations using Bokeh, enabling dynamic user interaction (panning, zooming, hovering, legend toggling) and on-the-fly parameter adjustments. This skill allows practitioners to build explorable, web-based figures from extracted ion chromatogram (XIC) data with overlaid peak boundaries and customizable trace filtering.

## When to use

When you have loaded extracted ion chromatogram traces (via SqMassLoader from sqMass files) and need to render them as interactive web-based visualizations where users can pan, zoom, hover for metadata, mute individual traces, and optionally visualize peak boundaries from OpenSwath results or on-the-fly peak picking. Use this skill when static plots are insufficient and downstream interpretation requires interactive exploration of retention time, intensity, and Q-value relationships.

## When NOT to use

- Input data is not chromatogram intensity time-series (e.g., raw spectrum arrays without retention time dimension)
- Peak boundaries or analyte metadata are unavailable and static single-trace visualization is sufficient
- User requires batch rendering of thousands of figures; Bokeh interactivity becomes computationally expensive

## Inputs

- Loaded transition group chromatogram data (massdash.structs.FeatureMap)
- Feature metadata (retention time, intensity, Q-values)
- MS1/MS2 trace arrays (intensity vs. retention time)
- Optional peak boundary annotations (OpenSwath results or MRMTransitionGroupPicker output)
- User-specified filter settings (Q-value cutoff, trace smoothing parameters, MS1/MS2 visibility flags)

## Outputs

- Interactive Bokeh figure object populated in massdash GUI main visualization area
- Rendered chromatogram traces with interactive legend for muting
- Peak boundary rectangles with hover metadata (if peak picking applied)
- Configured toolbar with pan, zoom, hover, and export tools

## How to apply

After loading transition group chromatogram data and populating analyte selection controls (filtered by Q-value threshold, typically 1%), initialize a Bokeh figure object via massdash.plotting.InteractivePlotter. Load the MS1/MS2 traces corresponding to the selected analyte, apply optional trace smoothing and MS1/MS2 filtering based on user settings in the sidebar controls, then render the traces as Bokeh glyphs with an interactive legend to allow muting. If peak boundaries are available (from OpenSwath or on-the-fly peak picking using MRMTransitionGroupPicker or pyMRMTransitionGroupPicker), overlay them as rectangles with hover tooltips displaying apex retention time, apex intensity, and Q-value. Finally, configure the interactive toolbar to enable panning, zooming, hovering, and figure export, then populate the main visualization panel with the rendered Bokeh figure object.

## Related tools

- **massdash.plotting.InteractivePlotter** (Core API for initializing and rendering interactive Bokeh figures for chromatogram visualization) — https://github.com/Roestlab/massdash
- **Bokeh** (Backend plotting library providing interactive figure rendering, glyphs, hover tools, legend toggling, and toolbar configuration)
- **massdash.peakPickers.MRMTransitionGroupPicker** (Generates peak boundary annotations (apex RT, apex intensity, Q-value) overlaid as hover-enabled rectangles on chromatogram) — https://github.com/Roestlab/massdash
- **massdash.peakPickers.pyMRMTransitionGroupPicker** (Deep learning–based alternative peak picker for on-the-fly peak boundary annotation) — https://github.com/Roestlab/massdash
- **SqMassLoader** (Loads sqMass files containing pre-extracted transition group chromatograms and associated feature metadata prior to Bokeh rendering) — https://github.com/Roestlab/massdash
- **massdash.structs.FeatureMap** (Data structure holding loaded feature metadata (retention time, intensity, Q-value) used to populate selection controls and Bokeh hover tooltips) — https://github.com/Roestlab/massdash

## Examples

```
from massdash.plotting import InteractivePlotter; from massdash.loaders import SqMassLoader; loader = SqMassLoader('data.sqMass'); traces = loader.load_chromatograms(protein='HUMAN_PROT', peptide='PEPTIDE', charge=2); plotter = InteractivePlotter(traces, smoothing=True, show_ms1=True, show_ms2=True); fig = plotter.render_bokeh(overlay_peak_picker='MRMTransitionGroupPicker'); display(fig)
```

## Evaluation signals

- Bokeh figure is rendered and visible in the massdash main visualization panel (not blank or error)
- Interactive toolbar is functional: panning and zooming respond to user mouse/touch input without lag
- Hover tooltip displays accurate metadata (analyte name, retention time, intensity, Q-value) when cursor hovers over traces or peak boundaries
- Legend toggle buttons successfully mute/unmute individual MS1/MS2 traces; DOM inspection confirms glyph visibility toggling
- Peak boundary rectangles (if rendered) have correct x-axis (retention time range) and y-axis (intensity range) positioning relative to overlaid chromatogram traces
- Figure export functionality (PNG/SVG via toolbar button) produces valid image file without data loss

## Limitations

- Bokeh rendering performance degrades when rendering >10 traces simultaneously or when peak boundaries overlap densely; recommend pre-filtering by Q-value threshold (default 1%)
- Hover tooltips and legend interactivity require sufficient vertical/horizontal screen real estate; on narrow mobile viewports or when many traces are present, UI responsiveness may suffer
- Peak picking on-the-fly (MRMTransitionGroupPicker) requires sufficient data points in the chromatogram; sparse or noisy traces may produce unreliable or missing peak boundaries
- The article does not specify memory or performance limits for Bokeh figure serialization; very large sqMass files or high-resolution chromatograms may cause browser memory exhaustion

## Evidence

- [other] The main area will be populated with interactive Bokeh figures: "The main area will be populated with interactive Bokeh figures"
- [other] Render interactive Bokeh figures with chromatogram traces and interactive legend for muting individual traces.: "Render interactive Bokeh figures with chromatogram traces and interactive legend for muting individual traces."
- [other] Optionally overlay peak boundaries from OpenSwath results or apply on-the-fly peak picking (MRMTransitionGroupPicker or pyMRMTransitionGroupPicker) and render peak boundary rectangles with hover metadata (apex retention time, apex intensity, Q-value).: "Optionally overlay peak boundaries from OpenSwath results or apply on-the-fly peak picking (MRMTransitionGroupPicker or pyMRMTransitionGroupPicker) and render peak boundary rectangles with hover"
- [other] Configure interactive toolbar for panning, zooming, hovering, and figure export.: "Configure interactive toolbar for panning, zooming, hovering, and figure export."
- [other] Apply optional trace smoothing and MS1/MS2 trace filtering based on user settings in plotting controls.: "Apply optional trace smoothing and MS1/MS2 trace filtering based on user settings in plotting controls."
- [other] Filter analytes by Q-value threshold (default 1%) and populate analyte selection dropdowns (protein, peptide, charge state).: "Filter analytes by Q-value threshold (default 1%) and populate analyte selection dropdowns (protein, peptide, charge state)."
