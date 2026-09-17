---
name: targeted-dia-data-extraction-from-raw-spectra
description: Use when when you have raw diaPASEF mzML files, a transition list with
  target analytes (protein, peptide, charge state), and search results (DIA-NN, OpenSwath
  output) containing feature metadata (retention time, ion mobility, m/z coordinates),
  and you need to isolate and visualize signal for.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MassDash
  - MzMLDataLoader
  - InteractiveTwoDimensionPlotter
  - MRMTransitionGroupPicker
  - pyMRMTransitionGroupPicker
  - MRMTransitionGroupPicker / pyMRMTransitionGroupPicker
  - Bokeh
  - Streamlit
  techniques:
  - LC-MS
  - ion-mobility-MS
  license_tier: open
  provenance_tier: literature
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

# targeted-dia-data-extraction-from-raw-spectra

## Summary

Extract ion chromatograms (XIC), ion mobilograms (IM), and spectra from raw diaPASEF mass spectrometry data by applying mass-to-charge (m/z), retention time, and ion mobility tolerance windows to analytes of interest. This skill enables targeted visualization and quantification of peptide precursors in Data-Independent Acquisition workflows.

## When to use

When you have raw diaPASEF mzML files, a transition list with target analytes (protein, peptide, charge state), and search results (DIA-NN, OpenSwath output) containing feature metadata (retention time, ion mobility, m/z coordinates), and you need to isolate and visualize signal for specific peptide precursors across multiple dimensions (m/z, retention time, ion mobility).

## When NOT to use

- Input is already a quantified feature table or pre-processed peak area summary — use targeted DIA data extraction only when you need to inspect raw traces and validate feature boundaries.
- Raw data is in formats other than mzML (e.g., raw vendor format without conversion) — MzMLDataLoader requires mzML-formatted input.
- Search results are missing or incomplete (no retention time, ion mobility, or m/z annotations for target analytes) — extraction parameters cannot be defined without search metadata.

## Inputs

- raw diaPASEF mass spectrometry data (mzML format file or directory path)
- transition list file (CSV or tabular format) containing analyte information (protein, peptide, charge state)
- search results file (DIA-NN, OpenSwath, or equivalent software output) with feature identification metadata (retention time, ion mobility, m/z coordinates, Q-value)

## Outputs

- extracted ion chromatogram (XIC) trace(s) for each analyte
- extracted ion mobilogram (IM) trace(s) for each analyte
- one-dimensional plots: extracted spectra, chromatogram, mobilogram
- two-dimensional heatmap plots (retention time vs. ion mobility)
- peak boundary annotations (if peak picking applied)
- tabular export (CSV) of raw extracted data and feature metadata

## How to apply

Load raw diaPASEF data via MzMLDataLoader, specifying the file or directory path. Parse the transition list to identify target analytes, then load the corresponding search results to retrieve feature identification metadata. For each analyte, define extraction windows: m/z tolerance (in ppm), retention time window, and ion mobility window. Apply these windows to the raw spectra to extract one-dimensional ion chromatograms and mobilograms, and construct two-dimensional heatmaps (retention time vs. ion mobility). Optionally apply on-the-fly peak picking (MRMTransitionGroupPicker or pyMRMTransitionGroupPicker) to identify peak boundaries on extracted chromatograms. Visualize using InteractiveTwoDimensionPlotter in Bokeh and export extracted data and metadata to CSV. The rationale is to isolate signal-of-interest from high-dimensional raw data, enabling qualitative assessment of peak shape, co-elution behavior, and ion mobility separation before or after quantification.

## Related tools

- **MassDash** (Web-based dashboard and modular Python package providing the complete extraction, visualization, and export workflow for targeted DIA data) — https://github.com/Roestlab/massdash
- **MzMLDataLoader** (Massdash.loaders component responsible for loading and parsing raw diaPASEF mass spectrometry data files in mzML format) — https://github.com/Roestlab/massdash
- **InteractiveTwoDimensionPlotter** (Massdash visualization component for generating one-dimensional plots (spectra, chromatogram, mobilogram) and two-dimensional heatmaps (retention time vs. ion mobility)) — https://github.com/Roestlab/massdash
- **MRMTransitionGroupPicker / pyMRMTransitionGroupPicker** (Optional on-the-fly peak picking algorithms to identify peak boundaries on extracted ion chromatograms) — https://github.com/Roestlab/massdash
- **Bokeh** (Interactive visualization library used by MassDash to render the main interactive figures for extracted traces and heatmaps)
- **Streamlit** (Web application framework providing the graphical user interface (GUI) for MassDash dashboard)

## Evaluation signals

- Extracted chromatogram and mobilogram traces show localized, non-zero signal within the retention time and ion mobility windows specified by the search results; signal outside these windows should be minimal or zero.
- Peak boundaries identified by peak picking algorithms align visually with the observed inflection points and valley boundaries on the extracted chromatogram trace.
- Two-dimensional heatmaps (retention time vs. ion mobility) exhibit concentrated intensity in a single or few coherent region(s) corresponding to the target analyte; scattered or multi-region intensity suggests contamination or co-elution.
- Exported CSV table contains one row per analyte with non-null entries for retention time, ion mobility, m/z, Q-value, and extracted intensity; null or out-of-range values indicate extraction failure.
- Q-value filtering applied to search results is reflected in the dropdown selection: only analytes with Q-value ≤ 1% (or the specified cutoff) are available for extraction, confirming correct metadata integration.

## Limitations

- The provided article excerpt does not contain sufficient technical detail on the operation, inputs, outputs, or parameters of MzMLDataLoader itself; implementation details for data loading may require consultation of source code or detailed API documentation.
- Peak picking on extracted chromatograms is optional and accuracy depends on the selected algorithm (MRMTransitionGroupPicker vs. pyMRMTransitionGroupPicker) and tuning of peak detection thresholds; no explicit threshold values or default parameters are provided in the article.
- Extraction windows (m/z ppm tolerance, retention time window, ion mobility window) must be provided by the user or derived from search results metadata; inappropriate window sizes may result in loss of signal or inclusion of noise.
- Visualization quality and computational performance may degrade with very large raw data files or when extracting many analytes simultaneously; the article does not discuss scalability limits or optimization strategies.

## Evidence

- [other] Load the transition list file containing analyte information (protein, peptide, charge) using MassDash's transition list parser. Load raw diaPASEF mass spectrometry data (mzML format) via MzMLDataLoader, specifying the file or directory path containing the DIA data.: "Load the transition list file containing analyte information (protein, peptide, charge) using MassDash's transition list parser. Load raw diaPASEF mass spectrometry data (mzML format) via"
- [other] Load search results experiment (DIA-NN, OpenSwath, or other software output) to retrieve feature identification metadata (retention time, ion mobility, m/z coordinates). Extract ion chromatogram (XIC) by applying mass-to-charge (m/z) tolerance window (in ppm), retention time window, and ion mobility window extraction parameters to raw spectra for each selected analyte.: "Load search results experiment (DIA-NN, OpenSwath, or other software output) to retrieve feature identification metadata (retention time, ion mobility, m/z coordinates). Extract ion chromatogram"
- [other] Extract ion mobilogram (IM) using the same m/z, retention time, and ion mobility extraction windows from raw data. Generate one-dimensional plots (extracted spectra, chromatogram, mobilogram) and two-dimensional plots (retention time vs. ion mobility heatmap) using InteractiveTwoDimensionPlotter for visualization.: "Extract ion mobilogram (IM) using the same m/z, retention time, and ion mobility extraction windows from raw data. Generate one-dimensional plots (extracted spectra, chromatogram, mobilogram) and"
- [other] The main area will be populated with interactive Bokeh figures: "The main area will be populated with interactive Bokeh figures"
- [other] The sidebar provides settings to control results at a specified Q-value cutoff: "The sidebar provides settings to control results at a specified Q-value cutoff"
- [readme] MassDash is a modular and flexible python package that has a streamlit graphical user interface (GUI): "MassDash is a modular and flexible python package that has a streamlit graphical user interface (GUI)"
