---
name: kendrick-mass-calculation
description: Use when you have uploaded m/z values from a high-resolution mass spectrometry
  analysis of a complex sample (e.g., crude oil, natural organic matter) and need
  to visualize homolog series trends.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
  tools:
  - Punc'data
  techniques:
  - mass-spectrometry
  license_tier: open
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

# kendrick-mass-calculation

## Summary

Calculate Normalized Kendrick Mass (NKM) values from m/z measurements in high-resolution mass spectrometry data to enable visualization and homolog series analysis. NKM transforms m/z data into a standardized coordinate system that reveals hydrocarbon-like homolog patterns in complex mixtures.

## When to use

You have uploaded m/z values from a high-resolution mass spectrometry analysis of a complex sample (e.g., crude oil, natural organic matter) and need to visualize homolog series trends. Use this skill when you intend to generate a Kendrick mass plot with a choice between m/z and NKM as the x-axis, or when you need to group or filter peaks by their position in Kendrick space relative to a selected base mass unit (typically CH₂ homologs with base mass 14.0157).

## When NOT to use

- Input data lacks an m/z column or does not originate from mass spectrometry analysis
- You need to compare samples using multivariate statistics (use PCA, Matrix, or Venn instead)
- Data are already in formula-space or require network-based homolog relationships (use Network tab)

## Inputs

- Delimiter-separated data file (CSV, semicolon, or comma) with column headers
- Column labeled or recognized by keyword 'm/z' containing mass-to-charge ratios
- Column labeled or recognized by keyword 'intensity' containing peak intensities
- Base mass parameter (default: 14.0157 for CH₂; user-editable in parameters tab)

## Outputs

- Normalized Kendrick Mass (NKM) vector aligned 1:1 with input m/z values
- Interactive Kendrick mass plot (Canvas A or B) with selectable x-axis (m/z or NKM)
- Tooltip data containing both m/z, NKM, and intensity for each plotted point

## How to apply

Extract the m/z column from the uploaded data file using Punc'data's keyword-based column recognition (m/z values are identified automatically). For each m/z value, compute NKM using the formula: NKM = round(m/z × base_mass) − (m/z × base_mass_rounded), where base_mass defaults to 14.0157 for CH₂ homolog series but can be adjusted in the parameters tab for other units of interest. Store both the original m/z and computed NKM vectors alongside their corresponding intensity values. Create a selector control (dropdown or toggle) to allow users to choose whether the x-axis of the Kendrick plot displays 'm/z' or 'NKM'. Pass the user's selected abscissa vector and intensity values to the Canvas renderer to generate the interactive Kendrick mass plot.

## Related tools

- **Punc'data** (Interactive platform for uploading data files, recognizing m/z and intensity columns by keyword, computing NKM values, and rendering the interactive Kendrick mass plot with x-axis selector) — https://github.com/WTVoe/puncdata

## Evaluation signals

- NKM values are computed and stored for every input m/z point; output vector length matches input m/z length
- X-axis toggle correctly switches between displaying m/z and NKM without loss of intensity or tooltip data
- NKM values fall within expected range (typically 0–1 in normalized form) and reflect the periodic structure of homolog series
- Interactive plot responds to ctrl+click (pinpoint tooltip), shift+click (zoom), and double-click (reset); points can be selected and deleted
- Base mass parameter in the parameters tab can be edited and plot updates correspondingly

## Limitations

- Base mass unit is assumed constant across all m/z values; heterogeneous samples may not fit a single homolog series
- No validation or quality control metrics are documented for m/z accuracy or tolerance
- NKM calculation does not account for instrumental resolution or peak mass accuracy beyond the input precision
- Kendrick plots are visual diagnostic tools; no statistical thresholding or automated homolog assignment is provided

## Evidence

- [other] Compute Normalized Kendrick Mass (NKM) values for each peak using the formula NKM = round(m/z × base mass) − (m/z × base mass rounded), where base mass is the mass unit of interest (typically 14.0157 for CH₂ homolog series).: "Compute Normalized Kendrick Mass (NKM) values for each peak using the formula NKM = round(m/z × base mass) − (m/z × base mass rounded), where base mass is the mass unit of interest (typically 14.0157"
- [readme] Punc'data recognizes column information based on keywords such as m/z value, intensity, and formula.: "Punc'data recognizes which column corresponds to which information based on keywords."
- [other] Create a selector control (dropdown or toggle) that stores the user's choice of x-axis coordinate ('m/z' or 'NKM').: "Create a selector control (dropdown or toggle) that stores the user's choice of x-axis coordinate ('m/z' or 'NKM')."
- [other] Implement conditional logic to return the selected abscissa vector: if x-axis mode is 'm/z', return the original m/z column; if 'NKM', return the computed NKM column.: "Implement conditional logic to return the selected abscissa vector: if x-axis mode is 'm/z', return the original m/z column; if 'NKM', return the computed NKM column."
- [readme] Punc'data is an interactive attribution and vizualization tool made for high resolution mass spectrometry results.: "Punc'data is an interactive attribution and vizualization tool made for high resolution mass spectrometry results."
