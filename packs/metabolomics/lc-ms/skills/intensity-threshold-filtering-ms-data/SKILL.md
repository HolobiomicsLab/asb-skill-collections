---
name: intensity-threshold-filtering-ms-data
description: Use when when you have loaded aligned peak data (from a preceding molecular networking alignment task) as a structured table with peak intensity, m/z, retention time, and alignment quality metrics, and you need to reduce false positives, remove noise, or focus analysis on peaks above a.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - Plotly
  - D3.js
  - pandas
  - Dash
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/jasms.5c00237
  title: MMSA
evidence_spans:
- interactive visualization
- interactive visualization and analysis
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mmsa_cq
    doi: 10.1021/jasms.5c00237
    title: MMSA
  dedup_kept_from: coll_mmsa_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.5c00237
  all_source_dois:
  - 10.1021/jasms.5c00237
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Intensity-Threshold Filtering of Mass Spectrometry Data

## Summary

Filter aligned mass spectrometry peaks by intensity threshold and alignment-quality metrics to retain only peaks meeting user-defined criteria. This skill removes low-intensity noise and poor-quality alignments, enabling focused downstream analysis of high-confidence molecular networking peak sets.

## When to use

When you have loaded aligned peak data (from a preceding molecular networking alignment task) as a structured table with peak intensity, m/z, retention time, and alignment quality metrics, and you need to reduce false positives, remove noise, or focus analysis on peaks above a user-specified intensity threshold or alignment score cutoff.

## When NOT to use

- Input is raw, unaligned mass spectrometry data: use this skill only after alignment has been performed.
- All peaks in the dataset are already known to be high-confidence or you require no filtering: this skill is unnecessary if no quality or intensity thresholds need to be applied.
- Peak intensity and alignment quality metrics are not available in the input table: filtering cannot be applied without these columns.

## Inputs

- Aligned peak table (structured tabular data with columns: peak intensity, m/z, retention time, alignment quality score, spectrum identifier)
- Filter parameter set (intensity threshold value, alignment quality score cutoff)

## Outputs

- Filtered peak table (subset of input peaks meeting all filter criteria)
- Interactive multi-spectrum visualization with filtered peaks (Plotly/D3.js overlay plot or heatmap)

## How to apply

Parse user-supplied filter parameters (intensity threshold and alignment score cutoff) from the web interface input state. Apply row-wise boolean filtering to the peak table: retain only rows where the intensity column meets the threshold AND the alignment quality column meets the score cutoff. Combine multiple filter constraints using AND logic so that peaks must satisfy ALL active filter criteria. After filtering, re-render the multi-spectrum visualization (overlay plot or heatmap with m/z on x-axis, intensity on y-axis, and spectrum identity as color/facet) to display only the retained peaks. Validate that all displayed peaks pass the active filter criteria and that the rendering correctly represents the filtered data without loss or corruption.

## Related tools

- **Plotly** (Interactive charting library for rendering filtered peak alignment visualizations with axes for m/z, intensity, and spectrum identity)
- **D3.js** (Alternative web-capable visualization library for multi-spectrum overlay plots and heatmaps of filtered peaks)
- **pandas** (Python data manipulation library for loading structured peak tables and applying row-wise boolean filtering logic)
- **Dash** (Interactive web application framework for building filter control interfaces (sliders, checkboxes) and real-time visualization updates) — github.com/Wang-Bioinformatics-Lab/NetworkFamily_MultipleAlignment_Website

## Evaluation signals

- All peaks in the final visualization have intensity ≥ the specified intensity threshold.
- All peaks in the final visualization have alignment quality score ≥ the specified score cutoff.
- The count of retained peaks is less than or equal to the count of input peaks (filtering never adds peaks).
- When filter thresholds are loosened (lowered), the number of displayed peaks increases; when tightened, the number decreases.
- SVG export of the filtered visualization renders correctly and displays only peaks passing active filter criteria.

## Limitations

- Filter effectiveness depends on the quality and reliability of the alignment quality metrics in the input table; poorly calibrated scores may not remove true false positives.
- No changelog is documented in the repository, so version-specific filter behavior changes are not tracked.
- Real-time visualization updates may be slow or unresponsive if the input peak table is very large (millions of peaks) or filter operations are complex.

## Evidence

- [other] Load aligned peak-alignment data (from preceding molecular networking alignment task) into memory as a structured table with peak intensity, m/z, retention time, and alignment quality metrics.: "Load aligned peak-alignment data (from preceding molecular networking alignment task) into memory as a structured table with peak intensity, m/z, retention time, and alignment quality metrics."
- [other] Parse user-supplied filter parameters (intensity threshold, alignment score cutoff, peak presence/absence criteria) from the web interface input state.: "Parse user-supplied filter parameters (intensity threshold, alignment score cutoff, peak presence/absence criteria) from the web interface input state."
- [other] Apply row-wise filtering to the peak table using boolean logic on intensity and alignment-quality columns, retaining only peaks that satisfy all active filter constraints.: "Apply row-wise filtering to the peak table using boolean logic on intensity and alignment-quality columns, retaining only peaks that satisfy all active filter constraints."
- [other] Render the filtered peak set as an interactive multi-spectrum visualization (e.g. overlay plot or heatmap) with axes for m/z (x), intensity (y), and spectrum identity (color/facet), using a web-capable charting library (Plotly, D3.js, or Canvas).: "Render the filtered peak set as an interactive multi-spectrum visualization (e.g. overlay plot or heatmap) with axes for m/z (x), intensity (y), and spectrum identity (color/facet), using a"
- [readme] Advanced Filtering: Custom spectrum ordering, m/z range filtering, and top-10 peak intensity analysis: "Advanced Filtering: Custom spectrum ordering, m/z range filtering, and top-10 peak intensity analysis"
