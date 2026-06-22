---
name: transition-group-peak-picking
description: Use when you have loaded extracted ion chromatogram (XIC) data from DIA mass spectrometry and need to identify peak boundaries for peptide precursor transitions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
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

# transition-group-peak-picking

## Summary

Peak picking identifies and extracts the temporal boundaries (apex retention time, intensity, Q-value) of eluting peptide precursor transitions from extracted ion chromatograms in DIA mass spectrometry data. This skill is essential for feature quantification and quality assessment when chromatographic peaks must be delineated either from search results (OpenSwath) or computed on-the-fly.

## When to use

Apply this skill when you have loaded extracted ion chromatogram (XIC) data from DIA mass spectrometry and need to identify peak boundaries for peptide precursor transitions. Use it when search results lack peak boundary annotations, when you want to re-optimize peak picking parameters interactively, or when comparing multiple peak-picking algorithms (e.g., rule-based vs. deep learning approaches) on the same chromatographic data.

## When NOT to use

- Input data is already a fully annotated feature table with peak boundaries — use direct visualization instead of re-picking.
- Chromatographic traces show severe baseline noise or unresolved multiplet peaks where rule-based pickers fail — consider manual inspection or alternative smoothing parameters first.
- You only need to visualize raw XIC traces without boundary identification — skip peak picking and render traces directly.

## Inputs

- sqMass file(s) containing pre-extracted ion chromatograms and transition group data
- OpenSwath feature map or search results (optional, for pre-computed peak boundaries)
- Analyte metadata: protein names, peptide sequences, charge states, retention time windows
- Q-value threshold (e.g., 1%) for analyte filtering
- Smoothing parameters and trace type filters (MS1/MS2 flags)

## Outputs

- Peak boundary rectangles with apex retention time, apex intensity, and Q-value metadata
- Interactive Bokeh figures overlaying peak boundaries on chromatogram traces
- Feature map with peak boundary annotations suitable for downstream quantification

## How to apply

Load transition group chromatogram data via SqMassLoader and populate analyte selection controls filtered by Q-value threshold (default 1%). Peak boundaries can be sourced from pre-computed OpenSwath results or computed on-the-fly using MRMTransitionGroupPicker or pyMRMTransitionGroupPicker. When applying on-the-fly peak picking, apply optional trace smoothing and MS1/MS2 trace filtering based on user-specified plotting controls before invoking the picker. Render peak boundary rectangles as interactive Bokeh overlays with hover metadata (apex retention time, apex intensity, Q-value) to enable visual validation. Compare output peaks against expected retention time windows and intensity ranges to judge picking accuracy.

## Related tools

- **SqMassLoader** (Load extracted ion chromatogram data and transition group metadata from sqMass files) — https://github.com/Roestlab/massdash
- **massdash.peakPickers.MRMTransitionGroupPicker** (Rule-based peak picker for identifying transition group peak boundaries on-the-fly) — https://github.com/Roestlab/massdash
- **massdash.peakPickers.pyMRMTransitionGroupPicker** (Alternative (possibly deep learning-based) peak picker for transition group boundary detection) — https://github.com/Roestlab/massdash
- **massdash.plotting.InteractivePlotter** (Render peak boundary overlays as interactive Bokeh figures with hover metadata) — https://github.com/Roestlab/massdash
- **Bokeh** (Interactive visualization backend for rendering chromatogram traces and peak boundary rectangles)
- **massdash.structs.FeatureMap** (Data structure for storing and annotating feature peaks with retention time, intensity, and Q-value) — https://github.com/Roestlab/massdash
- **massdash.loaders.ResultsLoader** (Load pre-computed OpenSwath peak boundaries from search result files) — https://github.com/Roestlab/massdash

## Evaluation signals

- Peak boundary rectangles align visually with the apex of each chromatographic trace when overlaid.
- Apex retention time values fall within the expected retention time window for each analyte (compare to peptide library or OpenSwath results).
- Apex intensity values are positive and correspond to the maximum point in the underlying chromatogram trace.
- Q-value metadata in hover tooltips meets the specified filtering threshold (e.g., ≤ 1% FDR).
- Comparison of on-the-fly peaks with OpenSwath pre-computed boundaries shows <5% retention time deviation and >0.95 correlation in apex intensity across a validation set.

## Limitations

- Rule-based peak pickers (MRMTransitionGroupPicker) may fail on severely noise-dominated or unresolved multiplet chromatograms; deep learning alternatives (pyMRMTransitionGroupPicker) require pre-training.
- Peak picking quality depends heavily on trace smoothing parameters; aggressive smoothing can merge adjacent peaks or lose fine structure.
- Q-value filtering at 1% threshold may exclude true low-abundance features; threshold must be tuned for the specific experiment and search engine.
- On-the-fly peak picking does not replace algorithmic validation against standards; peaks must still be inspected visually or benchmarked against reference results.
- Performance on high-complexity samples (e.g., >10,000 unique transitions) may be slow; batching or parallel processing is not documented in the README.

## Evidence

- [other] The XIC workflow operates by loading extracted ion chromatogram data and rendering the output as interactive Bokeh figures in the main visualization area.: "The XIC workflow operates by loading extracted ion chromatogram data and rendering the output as interactive Bokeh figures in the main visualization area."
- [other] Apply optional trace smoothing and MS1/MS2 trace filtering based on user settings in plotting controls.: "Apply optional trace smoothing and MS1/MS2 trace filtering based on user settings in plotting controls."
- [other] Optionally overlay peak boundaries from OpenSwath results or apply on-the-fly peak picking (MRMTransitionGroupPicker or pyMRMTransitionGroupPicker) and render peak boundary rectangles with hover metadata (apex retention time, apex intensity, Q-value).: "Optionally overlay peak boundaries from OpenSwath results or apply on-the-fly peak picking (MRMTransitionGroupPicker or pyMRMTransitionGroupPicker) and render peak boundary rectangles with hover"
- [other] Peak-picking can also be applied as in the first workflow, specifically for the extracted ion chromatograms: "Peak-picking can also be applied as in the first workflow, specifically for the extracted ion chromatograms"
- [readme] On the fly parameter optimization - Adjust peak picking parameters on the fly or experiment with novel deep learning based peak picking approaches.: "On the fly parameter optimization - Adjust peak picking parameters on the fly or experiment with novel deep learning based peak picking approaches."
