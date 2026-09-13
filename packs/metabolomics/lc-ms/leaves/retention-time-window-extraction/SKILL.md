---
name: retention-time-window-extraction
description: Use when you have loaded sqMass files containing pre-extracted transition
  group chromatograms and need to isolate chromatographic traces within a specific
  retention time interval—either defined by OpenSwath feature metadata (apex retention
  time ± margin) or by manual user selection.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
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
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jproteome.4c00026
  title: MassDash
evidence_spans:
- 'Chromatogram Loaders: Raw data stores chromatograms, this allows for faster loading
  however since extraction has already been performed by the upstream analysis tool.
  This includes SqMassLoader'
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# retention-time-window-extraction

## Summary

Extract ion chromatogram (XIC) data within user-specified or feature-derived retention time windows from DIA mass spectrometry files using SqMassLoader. This skill enables targeted visualization and analysis of peptide precursor signals by restricting the chromatographic domain to regions of analytical interest.

## When to use

Apply this skill when you have loaded sqMass files containing pre-extracted transition group chromatograms and need to isolate chromatographic traces within a specific retention time interval—either defined by OpenSwath feature metadata (apex retention time ± margin) or by manual user selection. Use when you want to reduce visual clutter, focus on a putative peak region, or prepare windowed data for peak picking or intensity quantification.

## When NOT to use

- When the input chromatogram data has not yet been extracted from raw DIA files; use raw file loading and XIC extraction first.
- When you need to visualize the full chromatographic profile across all retention times; windowing discards out-of-bounds signal.
- When peak boundaries or retention time metadata are unavailable and automatic windowing cannot be performed.

## Inputs

- sqMass file(s) containing pre-extracted ion chromatograms and transition group data
- Transition group metadata (retention time, intensity, Q-value, charge state)
- Feature metadata from search results (retention time, apex intensity, Q-value)
- User-specified or feature-derived retention time window boundaries (min_rt, max_rt in minutes or seconds)

## Outputs

- Filtered chromatogram traces restricted to the retention time window
- Interactive Bokeh figure(s) displaying windowed XIC with mutable legend and hover metadata
- Peak boundary rectangles (if peak picking applied to windowed region) with apex retention time and intensity annotations
- massdash.structs.FeatureMap or equivalent structure containing windowed chromatogram and metadata

## How to apply

Initialize SqMassLoader with the sqMass file path(s). Load transition group chromatogram data and extract associated feature metadata, including retention time and Q-value. Define a retention time window either from feature metadata (e.g., apex retention time with user-configurable margin) or accept user-specified bounds via the massdash UI. Filter analytes by Q-value threshold (default 1%) to ensure high-confidence features. Apply the retention time window to slice the loaded chromatogram traces, removing signal outside the boundaries. Render the windowed traces as interactive Bokeh figures with the extracted region highlighted or bounded. Optionally overlay peak boundaries from OpenSwath or apply on-the-fly peak picking to the windowed data to refine peak apex and boundaries within the extracted interval.

## Related tools

- **SqMassLoader** (Load pre-extracted ion chromatogram data and transition group metadata from sqMass files) — https://github.com/Roestlab/massdash
- **massdash.plotting.InteractivePlotter** (Render windowed chromatogram traces as interactive Bokeh figures with filtering and hover controls) — https://github.com/Roestlab/massdash
- **Bokeh** (Generate interactive scatter and line plots for windowed XIC visualization with panning, zooming, and export toolbar)
- **massdash.peakPickers.MRMTransitionGroupPicker** (Apply peak picking on-the-fly to windowed chromatogram region to identify and annotate peak boundaries) — https://github.com/Roestlab/massdash
- **massdash.structs.FeatureMap** (Store and manage retention time-windowed feature and chromatogram metadata) — https://github.com/Roestlab/massdash
- **massdash.loaders.ResultsLoader** (Load search results containing feature retention time and Q-value metadata to define windowing boundaries) — https://github.com/Roestlab/massdash

## Examples

```
from massdash.loaders import SqMassLoader; loader = SqMassLoader('data.sqMass'); chroms = loader.load(protein='ProteinA', peptide='PEPTIDEK', charge=2, rt_min=25.5, rt_max=28.0); plotter = massdash.plotting.InteractivePlotter(); fig = plotter.plot_chromatogram(chroms, title='XIC [25.5–28.0 min]')
```

## Evaluation signals

- Rendered Bokeh figure displays only chromatogram signal within the specified retention time interval; traces outside the window are absent or visually bounded.
- Feature metadata (retention time, intensity, Q-value) displayed in hover tooltips corresponds to data points within the selected window.
- If peak picking is applied post-windowing, peak apex retention time and boundary coordinates fall within the window bounds.
- Q-value filtering correctly excludes analytes above the specified threshold (e.g., default 1%) before or during windowing.
- Interactive legend allows muting/unmuting of individual MS1/MS2 traces within the windowed region without loss of data integrity.

## Limitations

- Retention time window extraction requires pre-computed feature metadata (from search results or OpenSwath); if metadata is absent or malformed, automatic windowing cannot proceed.
- Window boundaries are fixed after extraction; dynamic or adaptive windowing during interactive exploration is not explicitly supported in the described workflow.
- Peak picking applied post-windowing may identify false peak boundaries if the window is too narrow and excludes the true peak apex or boundaries.
- Q-value filtering is applied globally before windowing; features filtered out due to high Q-value cannot be recovered by narrowing the retention time window.

## Evidence

- [other] Load transition group chromatogram data and associated feature metadata (retention time, intensity, Q-values).: "Load transition group chromatogram data and associated feature metadata (retention time, intensity, Q-values)."
- [other] Filter analytes by Q-value threshold (default 1%) and populate analyte selection dropdowns (protein, peptide, charge state).: "Filter analytes by Q-value threshold (default 1%) and populate analyte selection dropdowns (protein, peptide, charge state)."
- [other] Apply optional trace smoothing and MS1/MS2 trace filtering based on user settings in plotting controls.: "Apply optional trace smoothing and MS1/MS2 trace filtering based on user settings in plotting controls."
- [other] Render interactive Bokeh figures with chromatogram traces and interactive legend for muting individual traces.: "Render interactive Bokeh figures with chromatogram traces and interactive legend for muting individual traces."
- [other] peak boundaries identified by OpenSwath: "possible to visualize the peak boundaries identified by OpenSwath"
- [other] The main area will be populated with interactive Bokeh figures: "The main area will be populated with interactive Bokeh figures"
