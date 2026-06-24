---
name: ion-chromatogram-mobilogram-visualization-and-interpretation
description: Use when after loading raw diaPASEF or DIA mass spectrometry data (mzML
  format) and search results (DIA-NN, OpenSwath, or equivalent) to visually inspect
  extracted ion chromatograms and mobilograms for selected peptide precursors.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
  tools:
  - MassDash
  - MzMLDataLoader
  - InteractiveTwoDimensionPlotter
  - MRMTransitionGroupPicker
  - pyMRMTransitionGroupPicker
  - Bokeh
  techniques:
  - LC-MS
  - ion-mobility-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.jproteome.4c00026
  title: MassDash
evidence_spans:
- MassDash is a modular and flexible python package that has a streamlit graphical
  user interface (GUI)
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ion-chromatogram-mobilogram-visualization-and-interpretation

## Summary

Visualize extracted ion chromatograms (XIC) and ion mobilograms (IM) from Data-Independent Acquisition mass spectrometry data to inspect peak shape, retention time alignment, and ion mobility separation for targeted analyte validation. This skill enables interactive exploration of one-dimensional (1D) and two-dimensional (2D) mass spectrometry traces to assess feature quality and optimize extraction parameters.

## When to use

Apply this skill after loading raw diaPASEF or DIA mass spectrometry data (mzML format) and search results (DIA-NN, OpenSwath, or equivalent) to visually inspect extracted ion chromatograms and mobilograms for selected peptide precursors. Use it when you need to validate that identified features exhibit coherent retention time, m/z, and ion mobility coordinates; diagnose peak picking failures or boundary misidentifications; or interactively adjust extraction windows (m/z tolerance in ppm, retention time window, ion mobility window) on the fly.

## When NOT to use

- Input is already a processed feature matrix or peak table (e.g., aligned quantification results); use this skill to validate the intermediate raw traces, not the final quantified values.
- Raw mass spectrometry data is in a format other than mzML (e.g., raw vendor formats without prior conversion); MzMLDataLoader requires mzML input.
- Search results are missing retention time, m/z, or ion mobility annotations; extraction windows cannot be meaningfully applied without ground-truth feature metadata.

## Inputs

- Raw diaPASEF mass spectrometry data file (mzML format)
- Search results file (DIA-NN, OpenSwath, or similar; contains feature identification metadata: m/z, retention time, ion mobility, Q-value)
- Transition list or analyte selection (protein, peptide, precursor m/z, charge state)
- Extraction parameters: m/z tolerance (ppm), retention time window, ion mobility window

## Outputs

- One-dimensional extracted ion chromatogram plot (retention time vs. intensity)
- One-dimensional extracted ion mobilogram plot (ion mobility vs. intensity)
- One-dimensional extracted spectrum plot (m/z vs. intensity)
- Two-dimensional heatmap (retention time vs. ion mobility)
- Peak boundary annotations and peak picking results (if applied)
- Tabular export of extracted data and feature metadata (CSV format)

## How to apply

Load the raw DIA mass spectrometry data via MzMLDataLoader, specifying the file or directory path containing mzML-format diaPASEF data. Retrieve feature identification metadata (retention time, ion mobility, m/z coordinates) from search results. Define extraction parameters: m/z tolerance window (typically in parts per million, ppm), retention time window (in seconds or minutes), and ion mobility window (in 1/K₀ units or Vs/cm²). Apply these windows to raw spectra to extract the ion chromatogram (intensity vs. retention time at a fixed m/z and ion mobility) and ion mobilogram (intensity vs. ion mobility at a fixed m/z and retention time). Render one-dimensional plots (extracted spectra, chromatogram, mobilogram) and optional two-dimensional heatmaps (retention time vs. ion mobility) using Bokeh or InteractiveTwoDimensionPlotter. Optionally apply on-the-fly peak picking (MRMTransitionGroupPicker or pyMRMTransitionGroupPicker) to automatically identify and overlay peak boundaries on chromatograms for validation.

## Related tools

- **MzMLDataLoader** (Loads and parses raw diaPASEF mass spectrometry data in mzML format, providing access to spectra and metadata for chromatogram and mobilogram extraction.) — https://github.com/Roestlab/massdash
- **InteractiveTwoDimensionPlotter** (Generates two-dimensional interactive heatmaps (e.g., retention time vs. ion mobility) using Bokeh for visualization of extracted ion traces.) — https://github.com/Roestlab/massdash
- **MRMTransitionGroupPicker** (Applies on-the-fly peak picking to identify peak boundaries and integrate areas on extracted ion chromatograms.) — https://github.com/Roestlab/massdash
- **pyMRMTransitionGroupPicker** (Python-based alternative implementation of peak picking for automated boundary identification on extracted chromatograms.) — https://github.com/Roestlab/massdash
- **Bokeh** (Renders interactive one-dimensional and two-dimensional figures for chromatogram and mobilogram visualization.)
- **MassDash** (Modular Python package and Streamlit GUI that orchestrates data loading, extraction, visualization, and parameter optimization workflows.) — https://github.com/Roestlab/massdash

## Evaluation signals

- Extracted ion chromatogram exhibits a single, well-defined peak or multiplet at the expected retention time; peak width is consistent with typical peptide peak width for the instrument and gradient.
- Extracted ion mobilogram shows coherent ion mobility distribution centered near the expected ion mobility value from search results; no artifactual multi-modal distributions suggest m/z or RT window misalignment.
- Two-dimensional retention time vs. ion mobility heatmap shows concentrated signal in a localized region, not diffuse or spread across unrelated m/z-RT-IM space.
- Q-value of the feature from search results is below the specified Q-value cutoff (e.g., ≤ 1%) and remains stable across different extraction parameter choices (within reason), indicating robust identification.
- Peak boundaries identified by on-the-fly peak picking align visually with the observed chromatographic trace; integrated peak area is positive and non-zero.

## Limitations

- Extraction quality depends critically on accuracy of feature metadata (retention time, m/z, ion mobility) from upstream search results; poor alignment or systematic retention time drift will compromise visual interpretation.
- Interactive visualization and on-the-fly parameter tuning are human-driven; no automated algorithm for optimal window selection is described; users must manually adjust m/z tolerance, RT window, and IM window based on trial and error.
- Peak picking results (MRMTransitionGroupPicker, pyMRMTransitionGroupPicker) may fail or misidentify boundaries for co-eluting peptides, overlapping isotope patterns, or low signal-to-noise features; visual inspection is required to validate automated annotations.
- The skill is designed for DIA workflows (diaPASEF, data-independent acquisition); applicability to targeted SRM/MRM or untargeted LC-MS data is unclear and not discussed in the article.

## Evidence

- [other] The main panel provides visualizations of the extraction ion chromatogram and the extracted ion mobilogram: "The main panel provides visualizations of the extraction ion chromatogram and the extracted ion mobilogram"
- [other] Extract ion chromatogram (XIC) by applying mass-to-charge (m/z) tolerance window (in ppm), retention time window, and ion mobility window extraction parameters to raw spectra for each selected analyte.: "Extract ion chromatogram (XIC) by applying mass-to-charge (m/z) tolerance window (in ppm), retention time window, and ion mobility window extraction parameters to raw spectra for each selected analyte"
- [other] Two dimensional plots allow heatmap style visualizations of two dimensions, i.e. retention time vs ion mobility: "Two dimensional plots allow heatmap style visualizations of two dimensions, i.e. retention time vs ion mobility"
- [other] Peak-picking can also be applied as in the first workflow, specifically for the extracted ion chromatograms: "Peak-picking can also be applied as in the first workflow, specifically for the extracted ion chromatograms"
- [other] The main area will be populated with interactive Bokeh figures: "The main area will be populated with interactive Bokeh figures"
- [other] the file or directory path containing raw Data-Independent Acquisition (DIA) mass spectrometry data: "the file or directory path containing raw Data-Independent Acquisition (DIA) mass spectrometry data"
- [other] the analytes populated in the drop down selection boxes are filtered based on the feature Q-value of 1%: "the analytes populated in the drop down selection boxes are filtered based on the feature Q-value of 1%"
