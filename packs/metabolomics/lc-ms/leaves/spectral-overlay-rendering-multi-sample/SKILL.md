---
name: spectral-overlay-rendering-multi-sample
description: Use when when you have aligned peak-alignment data from a preceding molecular networking task (structured as a table with peak intensity, m/z, retention time, and alignment quality metrics) and need to visualize and interactively filter peaks across multiple spectra to support comparative mass.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0570
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Plotly
  - D3.js
  - Dash
  - Pandas
  - Flask
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

# spectral-overlay-rendering-multi-sample

## Summary

Render aligned peaks across multiple mass spectra as an interactive overlay or heatmap visualization with dynamic filtering controls. This skill enables real-time exploration of molecular networking peak alignments by allowing users to adjust intensity thresholds, alignment quality cutoffs, and peak presence criteria while observing live updates to the multi-spectrum display.

## When to use

When you have aligned peak-alignment data from a preceding molecular networking task (structured as a table with peak intensity, m/z, retention time, and alignment quality metrics) and need to visualize and interactively filter peaks across multiple spectra to support comparative mass spectrometry analysis or quality assessment of alignments.

## When NOT to use

- Input peaks have not yet been aligned across spectra—use alignment preprocessing step first
- You need static, non-interactive visualization—use a simpler plotting library or static report generation
- Peak data lacks alignment quality metrics or spectrum identity information—cannot stratify or color by spectrum

## Inputs

- Aligned peak-alignment table (structured as CSV or in-memory DataFrame with columns: peak intensity, m/z, retention time, alignment quality metrics, spectrum identity)
- Filter parameters (intensity threshold, alignment score cutoff, peak presence/absence criteria)
- Multiple mass spectra identifiers or scan numbers

## Outputs

- Interactive multi-spectrum visualization (overlay plot or heatmap)
- Real-time rendered peak display with user-adjustable filtering
- SVG export for high-resolution figures (optional)

## How to apply

Load the aligned peak-alignment table into memory as a structured data frame with columns for intensity, m/z, retention time, alignment quality, and spectrum identity. Parse user-supplied filter parameters (e.g., intensity threshold slider, alignment score cutoff checkbox, peak presence/absence criteria) from the web interface. Apply row-wise boolean filtering to retain only peaks satisfying all active constraints. Render the filtered peak set using a web-capable charting library (Plotly, D3.js, or Canvas) with m/z on the x-axis, intensity on the y-axis, and spectrum identity encoded as color or facet. Attach interactive controls (sliders, checkboxes) to the rendering layer so users can dynamically adjust thresholds and see the visualization update in real-time. Validate that all displayed peaks pass the active filter criteria and that the rendering correctly represents the input alignment data without loss or corruption.

## Related tools

- **Plotly** (Interactive charting library for rendering multi-spectrum overlay plots and heatmaps with real-time filter responsiveness)
- **D3.js** (Web-capable visualization framework for custom multi-spectrum alignment displays with dynamic filtering)
- **Dash** (Interactive web application framework used to build the filtering interface and connect filter controls to live visualization updates)
- **Pandas** (Data manipulation library for loading, filtering, and transforming aligned peak tables before rendering)
- **Flask** (Web framework hosting the visualization endpoints and API routes for spectrum retrieval and filtering) — github.com/Wang-Bioinformatics-Lab/NetworkFamily_MultipleAlignment_Website

## Evaluation signals

- All displayed peaks satisfy the active filter criteria (e.g., intensity > threshold, alignment_score > cutoff); validate by spot-checking rendered points against filter state
- Visualization updates in real-time when user adjusts filter sliders or checkboxes without page reload
- Peak positions (m/z, intensity) in the rendered plot match the input aligned table exactly; compare plotted coordinates to input DataFrame
- Spectrum identity is correctly encoded (by color, facet, or overlay label) and all spectra in the filtered set are represented
- SVG export preserves all peak markers, axes, legend, and filter state annotations for reproducibility

## Limitations

- Rendering performance may degrade with very large peak sets (> 10,000 aligned peaks); consider aggregation or downsampling strategies
- No changelog documented; version stability and backward compatibility of filter parameter schemas not specified
- Filter responsiveness depends on client-side browser performance; complex boolean logic across many spectra may introduce latency

## Evidence

- [other] Load aligned peak-alignment data (from preceding molecular networking alignment task) into memory as a structured table with peak intensity, m/z, retention time, and alignment quality metrics.: "Load aligned peak-alignment data (from preceding molecular networking alignment task) into memory as a structured table with peak intensity, m/z, retention time, and alignment quality metrics."
- [other] Parse user-supplied filter parameters (intensity threshold, alignment score cutoff, peak presence/absence criteria) from the web interface input state.: "Parse user-supplied filter parameters (intensity threshold, alignment score cutoff, peak presence/absence criteria) from the web interface input state."
- [other] Apply row-wise filtering to the peak table using boolean logic on intensity and alignment-quality columns, retaining only peaks that satisfy all active filter constraints.: "Apply row-wise filtering to the peak table using boolean logic on intensity and alignment-quality columns, retaining only peaks that satisfy all active filter constraints."
- [other] Render the filtered peak set as an interactive multi-spectrum visualization (e.g., overlay plot or heatmap) with axes for m/z (x), intensity (y), and spectrum identity (color/facet), using a web-capable charting library (Plotly, D3.js, or Canvas).: "Render the filtered peak set as an interactive multi-spectrum visualization (e.g., overlay plot or heatmap) with axes for m/z (x), intensity (y), and spectrum identity (color/facet), using a"
- [other] Attach interactive filter controls (sliders, checkboxes) to the rendering layer so users can dynamically adjust thresholds and see the visualization update in real-time.: "Attach interactive filter controls (sliders, checkboxes) to the rendering layer so users can dynamically adjust thresholds and see the visualization update in real-time."
- [readme] Real-time peak alignment visualization with clickable peaks and set highlighting: "Real-time peak alignment visualization with clickable peaks and set highlighting"
- [readme] Custom spectrum ordering, m/z range filtering, and top-10 peak intensity analysis: "Custom spectrum ordering, m/z range filtering, and top-10 peak intensity analysis"
