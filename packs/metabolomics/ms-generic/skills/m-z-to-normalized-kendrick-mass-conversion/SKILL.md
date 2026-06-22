---
name: m-z-to-normalized-kendrick-mass-conversion
description: Use when you have uploaded peak list data containing m/z values and wish to construct a Kendrick mass plot where alkane homolog series (or other homologous families) are expected to appear as horizontal lines.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Punc'data
  - d3.js
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

# m/z to Normalized Kendrick Mass Conversion

## Summary

Convert m/z (mass-to-charge) values from high-resolution mass spectrometry data to Normalized Kendrick Mass (NKM) coordinates for homolog series visualization. This enables detection and display of alkane and substituted alkane patterns in Kendrick mass plots.

## When to use

Apply this skill when you have uploaded peak list data containing m/z values and wish to construct a Kendrick mass plot where alkane homolog series (or other homologous families) are expected to appear as horizontal lines. Use it specifically when you need to switch between m/z and NKM as the x-axis coordinate in an interactive Kendrick visualization, or when creating multiple views of the same data in different coordinate systems.

## When NOT to use

- Input data lacks m/z values or does not originate from high-resolution mass spectrometry: NKM conversion requires accurate mass data.
- Kendrick analysis is not appropriate for your molecular mixture (e.g., samples without expected homolog series or families with different mass increments than the selected base mass).
- Peak list already contains pre-computed Kendrick coordinates or is in a non-tabular format incompatible with Punc'data's keyword-based column recognition.

## Inputs

- Parsed peak list with m/z column extracted from uploaded CSV/delimiter-separated file
- Intensity values corresponding to each m/z entry
- Base mass parameter (mass unit of interest, e.g. 14.0157 for CH₂)

## Outputs

- Normalized Kendrick Mass (NKM) vector with decimal defect values
- m/z vector (original, passed through unchanged)
- Abscissa selection control storing user choice ('m/z' or 'NKM')
- Interactive Kendrick mass plot with selected coordinate as x-axis

## How to apply

First, parse the uploaded data file and extract the m/z column, recognized by Punc'data using column keyword matching. Then compute NKM for each peak using the formula: NKM = round(m/z × base_mass) − (m/z × base_mass rounded), where base_mass is typically 14.0157 for CH₂ homolog series analysis. Create a selector control (dropdown or toggle UI element) to store the user's choice of x-axis mode. Implement conditional logic: if x-axis mode is 'm/z', pass the original m/z values to the Kendrick plot renderer; if 'NKM', pass the computed NKM column instead. Both coordinate choices should be plotted against the same intensity (y-axis) values to preserve peak heights and relative abundances.

## Related tools

- **Punc'data** (Interactive visualization and data manager tool that recognizes m/z columns, enables selector controls for coordinate switching, and renders interactive Kendrick mass plots with user-selected abscissa.) — https://github.com/WTVoe/puncdata
- **d3.js** (JavaScript library used by Punc'data to implement interactive plot rendering, including dynamic axis switching.)

## Evaluation signals

- NKM values fall in the expected range [0, 1) representing decimal defect (fractional mass excess).
- Peaks belonging to the same homolog series (differing by integer multiples of base_mass) appear at the same NKM y-coordinate but different m/z x-coordinates.
- When coordinate mode is toggled from 'm/z' to 'NKM', the x-axis relabels and data points reposition without loss or duplication of intensity information.
- Original m/z and NKM columns contain identical row counts and are aligned by peak index.
- Horizontal lines in NKM-mode plots confirm proper grouping of homologous compounds.

## Limitations

- Accuracy of NKM calculation depends on precise m/z values; low-resolution MS data will produce unreliable homolog alignments.
- Base mass selection is user-determined and must match the actual chemical homolog series present; incorrect base_mass values will misalign homologs or produce scattered patterns.
- The skill assumes the first line of the uploaded file contains column headers and that subsequent lines represent valid m/z entries; malformed or headerless files may fail column keyword recognition.
- Interactive canvas plots require modern web browser support for d3.js rendering; very large peak lists (thousands of peaks) may experience performance degradation.

## Evidence

- [other] Workflow step describing NKM calculation: "Compute Normalized Kendrick Mass (NKM) values for each peak using the formula NKM = round(m/z × base mass) − (m/z × base mass rounded), where base mass is the mass unit of interest (typically 14.0157"
- [readme] Column recognition mechanism: "Punc'data recognizes which column corresponds to which information based on keywords."
- [other] Selector control implementation: "Create a selector control (dropdown or toggle) that stores the user's choice of x-axis coordinate ('m/z' or 'NKM')."
- [other] Conditional logic for abscissa selection: "Implement conditional logic to return the selected abscissa vector: if x-axis mode is 'm/z', return the original m/z column; if 'NKM', return the computed NKM column."
- [readme] Data manager and upload capability: "To vizualise data, you need to upload a file with separation (; , ...) between the columns. You can change the separator with the gear icon"
