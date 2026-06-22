---
name: chromatogram-extraction-and-visualization
description: Use when you have sqMass files containing pre-extracted transition group chromatograms from DIA-MS experiments and need to interactively visualize individual peptide precursor chromatograms, inspect peak quality via Q-values (typically 1% FDR cutoff), and overlay peak boundaries or apply on-the-fly.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - SqMassLoader
  - massdash.plotting.InteractivePlotter
  - massdash.peakPickers.MRMTransitionGroupPicker
  - massdash.peakPickers.pyMRMTransitionGroupPicker
  - massdash.structs.FeatureMap
  - massdash.loaders.ResultsLoader
  - Bokeh
  - MRMTransitionGroupPicker
  - pyMRMTransitionGroupPicker
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1021/acs.jproteome.4c00026
  title: MassDash
evidence_spans:
- 'Chromatogram Loaders: Raw data stores chromatograms, this allows for faster loading however since extraction has already been performed by the upstream analysis tool. This includes SqMassLoader'
- InteractivePlotter
- MRMTransitionGroupPicker
- pyMRMTransitionGroupPicker
- FeatureMap
- ResultsLoader
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

# Chromatogram Extraction and Visualization

## Summary

Load extracted ion chromatogram (XIC) data from sqMass files, filter by Q-value thresholds, and render interactive Bokeh visualizations with optional peak boundary overlays and trace smoothing. This skill bridges raw DIA mass spectrometry data and exploratory chromatogram analysis in massdash.

## When to use

You have sqMass files containing pre-extracted transition group chromatograms from DIA-MS experiments and need to interactively visualize individual peptide precursor chromatograms, inspect peak quality via Q-values (typically 1% FDR cutoff), and overlay peak boundaries or apply on-the-fly peak picking to compare different apex retention time and intensity estimates.

## When NOT to use

- sqMass file does not contain pre-extracted chromatograms (use raw DIA-MS data loading instead)
- analytes of interest do not meet the Q-value threshold — adjust cutoff or reconsider feature quality criteria
- peak picking parameters are unknown or require systematic optimization across many transitions — use batch parameter sweep workflow instead

## Inputs

- sqMass file(s) with extracted ion chromatogram data
- transition list containing analyte information (protein, peptide, charge state)
- feature metadata (retention time, intensity, Q-values)
- optional: OpenSwath peak boundary results or raw DIA-MS data for on-the-fly peak picking

## Outputs

- interactive Bokeh figure(s) with chromatogram traces
- filtered analyte selection dropdowns
- peak boundary rectangles with hover tooltips (apex RT, apex intensity, Q-value)
- exportable figure snapshot

## How to apply

Initialize SqMassLoader with sqMass file path(s) to load transition group chromatogram data and associated feature metadata (retention time, intensity, Q-values). Filter analytes by Q-value threshold (default 1%) and populate analyte selection dropdowns (protein, peptide, charge state). Apply optional trace smoothing via InteractivePlotter settings and MS1/MS2 trace filtering based on user selections. Render interactive Bokeh figures using massdash.plotting.InteractivePlotter with chromatogram traces and interactive legend for trace toggling. Optionally overlay peak boundaries from OpenSwath results or apply on-the-fly peak picking using MRMTransitionGroupPicker or pyMRMTransitionGroupPicker to render peak boundary rectangles with hover metadata (apex retention time, apex intensity, Q-value). Configure interactive toolbar for panning, zooming, hovering, and figure export.

## Related tools

- **SqMassLoader** (loads extracted ion chromatogram data and feature metadata from sqMass binary files) — https://github.com/Roestlab/massdash
- **massdash.plotting.InteractivePlotter** (renders chromatogram traces as interactive Bokeh visualizations with filtering and smoothing controls) — https://github.com/Roestlab/massdash
- **Bokeh** (interactive plotting library used to generate interactive figures with panning, zooming, and export toolbar)
- **MRMTransitionGroupPicker** (applies on-the-fly peak picking to extract peak boundaries and apex metadata for overlay) — https://github.com/Roestlab/massdash
- **pyMRMTransitionGroupPicker** (alternative deep learning-based peak picking approach for on-the-fly boundary detection) — https://github.com/Roestlab/massdash
- **massdash.structs.FeatureMap** (data structure for storing and retrieving feature metadata (retention time, intensity, Q-value)) — https://github.com/Roestlab/massdash
- **massdash.loaders.ResultsLoader** (loads OpenSwath or other search results containing peak boundary annotations) — https://github.com/Roestlab/massdash

## Examples

```
from massdash.loaders import SqMassLoader; from massdash.plotting import InteractivePlotter; loader = SqMassLoader('data.sqMass'); xic_data = loader.load_chromatograms(); plotter = InteractivePlotter(xic_data, q_value_threshold=0.01, smoothing=True); fig = plotter.render_interactive_chromatogram('Q1_peptide', ms_trace='MS2'); fig.show()
```

## Evaluation signals

- All analytes displayed in selection dropdowns pass the Q-value threshold (default ≤ 1%)
- Chromatogram traces render without gaps or artifacts and are visually continuous across retention time domain
- Peak boundary rectangles (if overlaid) align with visually apparent peaks and hover tooltips display non-null apex RT, apex intensity, and Q-value metadata
- Interactive toolbar functions (pan, zoom, export) operate without errors and exported figures are valid PNG/SVG files
- Trace smoothing (when enabled) produces monotonically reduced noise without over-smoothing apex intensity or shifting retention time

## Limitations

- Q-value filtering at 1% may be too stringent for exploratory analysis of borderline features or low-abundance peptides; requires manual threshold adjustment for each dataset
- on-the-fly peak picking (MRMTransitionGroupPicker, pyMRMTransitionGroupPicker) may produce inconsistent or incorrect peak boundaries if chromatogram baseline or signal-to-noise ratio deviates from training assumptions
- trace smoothing is applied uniformly across all transitions and cannot be selectively disabled for individual traces via the UI
- sqMass binary format is specific to OpenSwath/DIA-UMPIRE workflows; alternative DIA tools or vendor formats require separate loader implementations

## Evidence

- [other] Initialize SqMassLoader with sqMass file path(s) containing pre-extracted chromatograms.: "Initialize SqMassLoader with sqMass file path(s) containing pre-extracted chromatograms"
- [other] Filter analytes by Q-value threshold (default 1%) and populate analyte selection dropdowns.: "the analytes populated in the drop down selection boxes are filtered based on the feature Q-value of 1%"
- [other] The XIC workflow operates by loading extracted ion chromatogram data and rendering the output as interactive Bokeh figures.: "The XIC workflow operates by loading extracted ion chromatogram data and rendering the output as interactive Bokeh figures in the main visualization area"
- [other] Apply optional trace smoothing and MS1/MS2 trace filtering based on user settings.: "allows for smoothing of the traces and allows for displaying or hiding MS1 or MS2 traces"
- [other] Optionally overlay peak boundaries from OpenSwath results or apply on-the-fly peak picking.: "possible to visualize the peak boundaries identified by OpenSwath and Peak-picking can also be applied as in the first workflow, specifically for the extracted ion chromatograms"
- [other] Configure interactive toolbar for panning, zooming, hovering, and figure export.: "Configure interactive toolbar for panning, zooming, hovering, and figure export"
- [other] The main panel provides visualizations of the extraction ion chromatogram with peak boundary rectangles.: "The main panel provides visualizations of the extraction ion chromatogram and the extracted ion mobilogram"
