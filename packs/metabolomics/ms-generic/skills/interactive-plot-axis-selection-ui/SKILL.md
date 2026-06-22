---
name: interactive-plot-axis-selection-ui
description: Use when when you have a high-resolution mass spectrometry dataset with m/z values and need to generate Kendrick mass plots where users should choose between plotting raw m/z or computed Normalized Kendrick Mass (NKM) on the x-axis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0532
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  tools:
  - Punc'data
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1021/jasms.5c00151
  title: Punc’data
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_punc_data_cq
    doi: 10.1021/jasms.5c00151
    title: Punc’data
  dedup_kept_from: coll_punc_data_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.5c00151
  all_source_dois:
  - 10.1021/jasms.5c00151
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# interactive-plot-axis-selection-ui

## Summary

Enable users to dynamically select between alternative coordinate systems (e.g., m/z versus normalized Kendrick mass) as the x-axis variable for mass spectrometry visualizations. This skill wraps computed abscissa alternatives in a selector control and conditionally passes the chosen column to the plot renderer.

## When to use

When you have a high-resolution mass spectrometry dataset with m/z values and need to generate Kendrick mass plots where users should choose between plotting raw m/z or computed Normalized Kendrick Mass (NKM) on the x-axis. Specifically apply this when the input data table contains m/z column(s) recognized by keyword-based parsing, and your visualization workflow supports multiple coordinate representations for the same intensity series.

## When NOT to use

- Input data lacks recognized m/z column (missing keyword match)
- Visualization target is not Kendrick mass plot (e.g., matrix or network plots do not require axis selection)
- User interface does not support interactive controls or conditional rendering

## Inputs

- Parsed peak list data table with m/z column
- Intensity values corresponding to each m/z
- Base mass parameter (default 14.0157 for CH₂)
- User selection state from selector control

## Outputs

- Selected abscissa vector (m/z or NKM values)
- Interactive Kendrick mass plot with chosen x-axis coordinate
- Canvas visualization with selectable axis modes

## How to apply

Parse the input data table to extract m/z values using keyword recognition (Punc'data identifies 'm/z' columns automatically). Compute NKM for each peak using the formula NKM = round(m/z × base_mass) − (m/z × base_mass rounded), where base_mass is typically 14.0157 for CH₂ homolog series. Instantiate a selector control (dropdown or toggle) that stores the user's choice of x-axis coordinate ('m/z' or 'NKM'). Implement conditional logic: if x-axis mode is 'm/z', return the original m/z column; if 'NKM', return the computed NKM column. Pass the selected abscissa vector and corresponding intensity values to the Kendrick mass plot renderer.

## Related tools

- **Punc'data** (Interactive canvas and plot renderer that recognizes m/z columns by keyword, computes derived mass coordinates, and renders conditional visualizations with user-controlled axis selection) — https://github.com/WTVoe/puncdata

## Evaluation signals

- Selector control is visible and functional in the Canvas or Kendrick mass plot interface; user can toggle between 'm/z' and 'NKM' modes without error
- X-axis label and tick values update correctly when selection is changed (m/z values are within expected mass range; NKM values fall in [0, 1) range as defect mass)
- Plot data points and intensities remain synchronized across both coordinate systems (same peaks appear in same relative order, only x-position changes)
- NKM computation is accurate: spot-check 2–3 peaks by manual calculation (NKM = round(m/z × 14.0157) − (m/z × 14.0157 rounded)) and verify plot position matches
- No data loss or missing intensities when switching axes; all peaks visible in both modes

## Limitations

- Base mass parameter is hardcoded or user-configurable but not validated; incorrect choice yields chemically meaningless NKM coordinates
- Keyword-based column recognition may fail if input data uses non-standard column headers; manual parameter editing is available but adds friction
- NKM computation assumes homologous series structure (CH₂ or other regular intervals); heterogeneous or non-series datasets may not benefit from Kendrick visualization
- No statistical validation or benchmarking of axis choice impact reported; skill is presentational only, does not modify peak assignment or formula calculation

## Evidence

- [methods] Kendrick mass plot x-axis selection mechanism: "Create a selector control (dropdown or toggle) that stores the user's choice of x-axis coordinate ('m/z' or 'NKM'). Implement conditional logic to return the selected abscissa vector"
- [intro] M/Z column recognition by keyword: "Punc'data recognizes which column corresponds to which information based on keywords"
- [methods] NKM formula specification: "NKM = round(m/z × base mass) − (m/z × base mass rounded), where base mass is the mass unit of interest (typically 14.0157 for CH₂ homolog series)"
- [readme] Canvas tab visualization support: ""Table", "Stats", "Canvas A/B" and "Network" allow different types of tables and charts to be produced. On Canvas A,B and Stats, charts are interactive"
- [readme] Interactive plot capability: "to zoom on a chart, shift+click; to unzoom and go to the initial state: double click"
