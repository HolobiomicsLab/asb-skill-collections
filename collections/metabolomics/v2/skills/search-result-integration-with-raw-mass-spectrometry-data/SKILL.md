---
name: search-result-integration-with-raw-mass-spectrometry-data
description: Use when when you have completed a DIA-MS proteomics search (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3634
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - MassDash
  - MzMLDataLoader
  - InteractiveTwoDimensionPlotter
  - MRMTransitionGroupPicker
  - pyMRMTransitionGroupPicker
  - Bokeh
  - Streamlit
derived_from:
- doi: 10.1021/acs.jproteome.4c00026
  title: MassDash
evidence_spans:
- MassDash is a modular and flexible python package that has a streamlit graphical user interface (GUI)
- ':mod:`massdash.loaders`: Classes for loading data'
- MzMLDataLoader
- InteractiveTwoDimensionPlotter
- MRMTransitionGroupPicker
- pyMRMTransitionGroupPicker
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

# search-result-integration-with-raw-mass-spectrometry-data

## Summary

Integration of peptide/protein search results (feature identification metadata: retention time, ion mobility, m/z coordinates) with raw diaPASEF mass spectrometry data (mzML format) to enable targeted extraction and visualization of ion chromatograms, mobilograms, and multi-dimensional peak landscapes. This skill bridges computational search output with raw spectral data, enabling on-the-fly parameter optimization and cross-validation of identifications.

## When to use

When you have completed a DIA-MS proteomics search (e.g., DIA-NN, OpenSwath) and possess raw diaPASEF mzML data files, and need to visualize, validate, and extract targeted ion signatures (chromatograms, mobilograms, heatmaps) for specific peptide precursors, or when you wish to apply peak picking algorithms and optimize extraction windows in real time without re-searching.

## When NOT to use

- Input search results already contain preprocessed extracted chromatograms or peak areas (integration already performed upstream)
- Raw mass spectrometry data is in a format other than mzML (e.g., proprietary vendor formats without conversion)
- Search results use a Q-value cutoff threshold higher than the desired analytical stringency (e.g., >5% FDR when 1% filtering is required)

## Inputs

- Search result file (DIA-NN, OpenSwath, or equivalent output format) containing feature identification metadata (retention time, ion mobility, m/z, charge state, Q-value)
- Raw diaPASEF mass spectrometry data in mzML format (file or directory path)
- Transition list file (optional) containing analyte information (protein, peptide, charge state)
- Extraction parameters: m/z tolerance (ppm), retention time window, ion mobility window

## Outputs

- Extracted ion chromatogram (XIC) traces for selected analytes
- Extracted ion mobilogram (IM) traces
- One-dimensional visualization plots (extracted spectra, chromatogram, mobilogram)
- Two-dimensional retention time vs. ion mobility heatmap visualizations
- Peak boundary annotations (if peak picking applied)
- Tabular export (CSV) of raw extracted data and feature metadata

## How to apply

Load the search results file (DIA-NN, OpenSwath, or equivalent output) to retrieve feature identification metadata including retention time, ion mobility, and m/z coordinates for each analyte. Simultaneously load raw diaPASEF mzML data via MzMLDataLoader, specifying the file or directory path. Define extraction windows: m/z tolerance (typically in ppm), retention time window, and ion mobility window based on the search result metadata and instrument resolution. Apply these windows to the raw spectra to extract ion chromatograms (XIC) and ion mobilograms (IM) for each selected analyte. Visualize the extracted traces using InteractiveTwoDimensionPlotter (retention time vs. ion mobility heatmaps) and one-dimensional plots (extracted spectra, chromatogram, mobilogram). Optionally apply on-the-fly peak picking (MRMTransitionGroupPicker or pyMRMTransitionGroupPicker) to identify and refine peak boundaries on the extracted chromatograms. Export the raw extracted data and feature metadata to CSV for downstream analysis.

## Related tools

- **MzMLDataLoader** (Loads and parses raw diaPASEF mass spectrometry data files (mzML format) into memory for targeted extraction workflows) — https://github.com/Roestlab/massdash
- **InteractiveTwoDimensionPlotter** (Generates interactive two-dimensional heatmap visualizations (retention time vs. ion mobility) of extracted ion traces and spectra) — https://github.com/Roestlab/massdash
- **MRMTransitionGroupPicker** (Applies on-the-fly peak picking to identify and annotate peak boundaries on extracted ion chromatograms) — https://github.com/Roestlab/massdash
- **pyMRMTransitionGroupPicker** (Python-based alternative peak picker for identifying peak boundaries on extracted chromatograms) — https://github.com/Roestlab/massdash
- **Bokeh** (Interactive visualization library used to render the main panel figures for extracted chromatograms and mobilograms)
- **Streamlit** (Web-based graphical user interface framework for the MassDash dashboard enabling parameter input and real-time visualization updates) — https://github.com/Roestlab/massdash

## Evaluation signals

- Extracted XIC and IM traces display expected chromatographic and ion mobility peak shapes matching the retention time and ion mobility coordinates from search results
- Two-dimensional heatmap (retention time vs. ion mobility) shows concentrated signal intensity in the region predicted by search result metadata, not scattered across the full acquisition space
- Peak picking correctly identifies peak boundaries on extracted chromatograms with visually identifiable start/apex/end coordinates
- Exported CSV files contain matching counts of rows between search result features and extracted ion traces (no missing or orphaned analytes)
- Q-value filtering at specified cutoff (e.g., 1%) reduces the set of visualized analytes as expected; only features passing the cutoff appear in dropdown selection boxes
- On-the-fly parameter adjustment (m/z tolerance, RT window, IM window) visibly changes the extent of extracted signal intensity without breaking downstream export

## Limitations

- The document references MzMLDataLoader and massdash.loaders components but does not provide sufficient technical detail describing their operation, inputs, outputs, or exact parameters for implementing the mechanism independently
- Peak boundary identification depends on upstream search software (OpenSwath, DIA-NN) output format and quality; misaligned or poorly predicted retention time / ion mobility coordinates will yield empty or uninformative extractions
- On-the-fly parameter optimization is exploratory and subjective; no automated algorithm is described for determining optimal m/z tolerance, RT window, or IM window widths from raw data alone

## Evidence

- [other] Load search results experiment (DIA-NN, OpenSwath, or other software output) to retrieve feature identification metadata (retention time, ion mobility, m/z coordinates).: "Load search results experiment (DIA-NN, OpenSwath, or other software output) to retrieve feature identification metadata (retention time, ion mobility, m/z coordinates)."
- [other] Extract ion chromatogram (XIC) by applying mass-to-charge (m/z) tolerance window (in ppm), retention time window, and ion mobility window extraction parameters to raw spectra for each selected analyte.: "Extract ion chromatogram (XIC) by applying mass-to-charge (m/z) tolerance window (in ppm), retention time window, and ion mobility window extraction parameters to raw spectra"
- [other] The main panel provides visualizations of the extraction ion chromatogram and the extracted ion mobilogram: "The main panel provides visualizations of the extraction ion chromatogram and the extracted ion mobilogram"
- [other] For one dimensional plots, the user can visualize the extracted spectra, chromatogram and mobilogram; Two dimensional plots allow heatmap style visualizations of two dimensions, i.e. retention time vs ion mobility: "For one dimensional plots, the user can visualize the extracted spectra, chromatogram and mobilogram; Two dimensional plots allow heatmap style visualizations of two dimensions, i.e. retention time"
- [other] the analytes populated in the drop down selection boxes are filtered based on the feature Q-value of 1%: "the analytes populated in the drop down selection boxes are filtered based on the feature Q-value of 1%"
- [other] The sidebar provides settings to control results at a specified Q-value cutoff; Peak-picking can also be applied as in the first workflow, specifically for the extracted ion chromatograms: "The sidebar provides settings to control results at a specified Q-value cutoff; Peak-picking can also be applied as in the first workflow, specifically for the extracted ion chromatograms"
