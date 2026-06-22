---
name: mass-spectrometry-peak-alignment-visualization
description: Use when when you have aligned peak data from molecular networking (with m/z, intensity, retention time, and alignment quality metrics across multiple spectra) and need to interactively explore peak alignments under multiple filtering criteria (intensity thresholds, alignment score cutoffs, peak.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3630
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - Plotly
  - D3.js
  - Dash
  - Flask
  - pandas
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-peak-alignment-visualization

## Summary

This skill enables interactive web-based visualization and real-time filtering of aligned peaks across multiple mass spectrometry spectra, supporting molecular networking analysis. It combines structured peak-alignment data (m/z, intensity, retention time, alignment quality) with dynamic filter controls to render multi-spectrum overlays or heatmaps and validate peak presence under user-defined constraints.

## When to use

When you have aligned peak data from molecular networking (with m/z, intensity, retention time, and alignment quality metrics across multiple spectra) and need to interactively explore peak alignments under multiple filtering criteria (intensity thresholds, alignment score cutoffs, peak presence/absence patterns). Use this skill when stakeholders require real-time parameter adjustment without regenerating alignments.

## When NOT to use

- Input is unaligned raw spectra or has not yet undergone molecular networking peak alignment.
- Alignment data lacks retention time or quality metrics needed for informed filtering.
- User requires batch processing or non-interactive analysis; real-time parameter adjustment is not needed.

## Inputs

- Structured peak-alignment table (DataFrame with columns: m/z, intensity, retention time, alignment quality score, spectrum identity)
- User filter parameters (intensity threshold, alignment score cutoff, peak presence/absence criteria)
- Molecular networking alignment data (e.g., from GNPS Task ID, USI, or FBMN input formats)

## Outputs

- Interactive multi-spectrum visualization (overlay plot or heatmap) with m/z, intensity, and spectrum identity dimensions
- Filtered peak set satisfying all active constraints
- Real-time interactive filter control layer (sliders, checkboxes)
- SVG export for high-resolution figures (optional)

## How to apply

Load the structured peak-alignment table (e.g., from a preceding GNPS molecular networking task) into memory as a pandas DataFrame or equivalent. Parse user-supplied filter parameters (intensity threshold, alignment score cutoff, peak presence/absence criteria) from the web interface input state. Apply row-wise boolean filtering to retain only peaks satisfying all active constraints across the intensity and alignment-quality columns. Render the filtered peak set using an interactive charting library (Plotly or D3.js) with axes for m/z (x-axis), intensity (y-axis), and spectrum identity (color or facet), optionally as an overlay plot or heatmap. Attach interactive sliders and checkboxes to the rendering layer so users can dynamically adjust thresholds and observe visualization updates in real-time. Validate that all displayed peaks pass the active filter criteria and that the rendering accurately represents the input alignment data without loss or corruption.

## Related tools

- **Plotly** (Interactive charting library for rendering multi-spectrum peak alignment overlays and heatmaps with real-time filter responsiveness)
- **D3.js** (Web-capable visualization framework for custom multi-dimensional peak alignment rendering)
- **Dash** (Interactive web application framework (built on Plotly) for attaching filter controls and state management to peak visualizations) — github.com/Wang-Bioinformatics-Lab/NetworkFamily_MultipleAlignment_Website
- **Flask** (Web framework for serving data input and visualization endpoints) — github.com/Wang-Bioinformatics-Lab/NetworkFamily_MultipleAlignment_Website
- **pandas** (Data manipulation and row-wise boolean filtering of peak-alignment tables) — github.com/Wang-Bioinformatics-Lab/NetworkFamily_MultipleAlignment_Website

## Evaluation signals

- All displayed peaks in the rendering satisfy the active filter criteria (intensity threshold, alignment score cutoff, peak presence/absence constraints).
- Sliders and checkboxes respond in real-time without requiring page refresh or data reprocessing.
- Peak positions (m/z, intensity) and spectrum identities in the visualization match the input alignment table exactly (no loss or corruption).
- Toggling a filter on/off produces a visible, correct change in peak set size and rendering without anomalies.
- SVG export (if used) renders identically to the on-screen visualization and is readable in external graphics software.

## Limitations

- Filtering performance may degrade with very large peak tables (>100k rows) without query optimization or spatial indexing.
- Real-time rendering responsiveness depends on browser capabilities and network latency; extremely dense spectra may cause lag.
- Alignment quality metrics must be present in input data; missing or poorly calibrated quality scores reduce filter reliability.
- No changelog available in the source repository, limiting traceability of feature or API changes.

## Evidence

- [other] Describes the core input and filtering workflow for peak alignment visualization.: "Load aligned peak-alignment data (from preceding molecular networking alignment task) into memory as a structured table with peak intensity, m/z, retention time, and alignment quality metrics. Parse"
- [other] Describes the rendering and interactive control layer.: "Render the filtered peak set as an interactive multi-spectrum visualization (e.g., overlay plot or heatmap) with axes for m/z (x), intensity (y), and spectrum identity (color/facet), using a"
- [readme] States the high-level application capability from the README abstract.: "A web-based application for interactive visualization and analysis of molecular networking peak alignments."
- [readme] Specifies the advanced filtering and analysis capabilities for aligned peaks.: "Advanced Filtering: Custom spectrum ordering, m/z range filtering, and top-10 peak intensity analysis"
- [other] Confirms validation requirement for filtering correctness.: "Validate that all displayed peaks pass the active filter criteria and that the rendering correctly represents the input alignment data without loss or corruption."
