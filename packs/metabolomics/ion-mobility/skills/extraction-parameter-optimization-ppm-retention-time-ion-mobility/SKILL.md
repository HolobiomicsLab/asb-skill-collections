---
name: extraction-parameter-optimization-ppm-retention-time-ion-mobility
description: Use when you are reconstructing targeted ion chromatograms (XIC) and ion mobilograms (IM) from raw diaPASEF data and need to balance sensitivity (wide extraction windows) against specificity (narrow windows that reject interference).
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
  - Bokeh
  - Streamlit
  techniques:
  - LC-MS
  - ion-mobility-MS
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

# Extraction Parameter Optimization (ppm, Retention Time, Ion Mobility)

## Summary

Optimize mass-to-charge (m/z), retention time, and ion mobility extraction windows to maximize signal recovery and minimize noise when isolating targeted analytes from raw diaPASEF DIA mass spectrometry data. This skill is essential for recovering high-fidelity ion chromatograms and mobilograms that support accurate peak picking and quantification.

## When to use

You are reconstructing targeted ion chromatograms (XIC) and ion mobilograms (IM) from raw diaPASEF data and need to balance sensitivity (wide extraction windows) against specificity (narrow windows that reject interference). Optimization is triggered when search results (DIA-NN, OpenSwath) provide coarse feature coordinates (m/z, retention time, ion mobility) and you must determine which window widths yield clean, interpretable traces suitable for on-the-fly peak picking or quantitative comparison.

## When NOT to use

- Input data is already processed into a feature table or quantified matrix; optimization applies only to raw spectral extraction.
- Search results lack retention time, m/z, or ion mobility metadata; optimization requires coarse reference coordinates.
- DIA data is from a different acquisition mode (e.g., traditional windowed DIA, not diaPASEF); ion mobility dimension is not applicable.

## Inputs

- Transition list file (protein, peptide, charge identifiers)
- Raw diaPASEF mass spectrometry data (mzML format, file or directory path)
- Search results experiment metadata (DIA-NN, OpenSwath, or equivalent; feature m/z, retention time, ion mobility, Q-value)

## Outputs

- Optimized extraction parameter set (m/z tolerance in ppm, retention time window in seconds, ion mobility window in Vs/cm²)
- Extracted ion chromatogram (XIC) traces for all selected analytes
- Extracted ion mobilogram (IM) traces for all selected analytes
- One-dimensional visualization plots (extracted spectra, chromatogram, mobilogram)
- Two-dimensional visualization plots (retention time vs. ion mobility heatmap)
- Peak boundary metadata (if on-the-fly peak picking is applied)

## How to apply

Load the transition list (protein, peptide, charge), raw diaPASEF mzML data, and search results metadata containing reference feature coordinates (m/z, retention time, ion mobility). Begin with conservative defaults (e.g., ±5 ppm m/z tolerance, ±30–60 s retention time window, ±0.05 Vs/cm² ion mobility window) and iteratively extract XIC and IM traces for representative analytes. Visualize one-dimensional plots (extracted spectra, chromatogram, mobilogram) and two-dimensional plots (retention time vs. ion mobility heatmap) using InteractiveTwoDimensionPlotter to assess peak shape, baseline noise, and co-eluting interference. Adjust ppm, retention time, and ion mobility windows based on visual inspection and peak quality until extracted traces exhibit clear peak boundaries, minimal background, and no obvious truncation of the feature. Once optimized, apply the final parameters uniformly across all analytes in the cohort.

## Related tools

- **MassDash** (Web-based GUI and Python package for loading raw DIA data, applying extraction windows, visualizing chromatograms and mobilograms, and iteratively optimizing parameters) — https://github.com/Roestlab/massdash
- **MzMLDataLoader** (Component of massdash.loaders module that loads and parses raw diaPASEF mass spectrometry data files in mzML format)
- **InteractiveTwoDimensionPlotter** (Generates one-dimensional and two-dimensional interactive Bokeh visualizations (e.g., retention time vs. ion mobility heatmap) to assess extraction window quality)
- **Bokeh** (Interactive visualization library used to render chromatograms, mobilograms, and heatmap-style plots for real-time parameter inspection)
- **MRMTransitionGroupPicker** (Optional on-the-fly peak picking algorithm applied to extracted chromatograms to identify peak boundaries after extraction windows are optimized)
- **Streamlit** (Graphical user interface framework underlying MassDash GUI for interactive parameter adjustment and visualization)

## Examples

```
massdash gui  # Launch the Streamlit web interface, load raw diaPASEF mzML data, search results (DIA-NN output), and transition list; iteratively adjust m/z tolerance (±5 ppm), retention time window (±30 s), and ion mobility window (±0.05 Vs/cm²) while visualizing XIC, IM, and 2D heatmap plots until peak shape is optimal
```

## Evaluation signals

- Extracted ion chromatogram (XIC) exhibits a single, well-defined peak (or expected multiplet) with minimal baseline noise and no obvious truncation at window edges.
- Extracted ion mobilogram (IM) trace shows clear peak definition in the ion mobility dimension, consistent with literature or reference standards for the peptide.
- Two-dimensional retention time vs. ion mobility heatmap displays tight, contiguous signal cluster with minimal scattered interference outside the feature region.
- Peak picking applied downstream yields consistent peak boundary and area estimates across replicate analyte extractions with the same window parameters.
- Quantitative feature intensities are stable across a range of ±10–20% window perturbations, indicating robustness of the chosen parameters.

## Limitations

- Optimization is manual and visual; no automated algorithm is described in the article for tuning m/z, retention time, and ion mobility windows simultaneously.
- The optimal window depends on the specific diaPASEF acquisition settings, chromatographic gradient, and sample complexity; parameters may require re-tuning for different cohorts or instruments.
- Very wide extraction windows (e.g., >100 ppm or >120 s retention time) risk capturing co-eluting isobars or isotopologues, degrading specificity; very narrow windows may truncate valid signal.
- Ion mobility window optimization is only applicable to diaPASEF or other ion-mobility-enhanced DIA; traditional windowed DIA data lack this dimension.

## Evidence

- [other] Load the transition list file containing analyte information (protein, peptide, charge) using MassDash's transition list parser. Load raw diaPASEF mass spectrometry data (mzML format) via MzMLDataLoader, specifying the file or directory path containing the DIA data.: "Load the transition list file containing analyte information (protein, peptide, charge) using MassDash's transition list parser. Load raw diaPASEF mass spectrometry data (mzML format) via"
- [other] Extract ion chromatogram (XIC) by applying mass-to-charge (m/z) tolerance window (in ppm), retention time window, and ion mobility window extraction parameters to raw spectra for each selected analyte. Extract ion mobilogram (IM) using the same m/z, retention time, and ion mobility extraction windows from raw data.: "Extract ion chromatogram (XIC) by applying mass-to-charge (m/z) tolerance window (in ppm), retention time window, and ion mobility window extraction parameters to raw spectra for each selected analyte"
- [other] Generate one-dimensional plots (extracted spectra, chromatogram, mobilogram) and two-dimensional plots (retention time vs. ion mobility heatmap) using InteractiveTwoDimensionPlotter for visualization.: "Generate one-dimensional plots (extracted spectra, chromatogram, mobilogram) and two-dimensional plots (retention time vs. ion mobility heatmap) using InteractiveTwoDimensionPlotter"
- [readme] On the fly parameter optimization - Adjust peak picking parameters on the fly or experiment with novel deep learning based peak picking approaches.: "On the fly parameter optimization - Adjust peak picking parameters on the fly or experiment with novel deep learning based peak picking approaches"
- [other] The main area will be populated with interactive Bokeh figures: "The main area will be populated with interactive Bokeh figures"
