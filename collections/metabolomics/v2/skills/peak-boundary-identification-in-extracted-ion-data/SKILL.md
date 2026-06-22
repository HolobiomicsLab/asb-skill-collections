---
name: peak-boundary-identification-in-extracted-ion-data
description: Use when after extracting ion chromatograms and ion mobilograms from raw diaPASEF or DIA data within specified m/z, retention time, and ion mobility windows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
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

# Peak Boundary Identification in Extracted Ion Data

## Summary

Identify and mark the temporal boundaries (start and end retention time) of chromatographic peaks in extracted ion chromatograms (XICs) and ion mobilograms from DIA mass spectrometry data. This skill enables precise quantification and feature delineation by automating or visualizing peak onset and offset, critical for downstream peak integration and quality control.

## When to use

Apply this skill after extracting ion chromatograms and ion mobilograms from raw diaPASEF or DIA data within specified m/z, retention time, and ion mobility windows. Use it when you need to demarcate peak boundaries for integration, validate OpenSwath or other search algorithm outputs, or optimize peak-picking parameters interactively before exporting quantitative features.

## When NOT to use

- Input chromatogram is already integrated or deconvolved by upstream software (e.g., spectral library matching) — peak boundaries are already determined.
- Data lacks sufficient retention time or ion mobility resolution; boundaries will be unreliable or ambiguous.
- Chromatogram contains unresolved co-eluting peaks; boundary identification will assign incorrect boundaries to individual analytes without prior separation or targeted extraction parameters.

## Inputs

- Extracted ion chromatogram (XIC) trace data (m/z, retention time, intensity)
- Ion mobilogram (IM) trace data (ion mobility, intensity)
- Raw diaPASEF or DIA mass spectrometry data (mzML format)
- Search results metadata (feature retention time, ion mobility, m/z from DIA-NN, OpenSwath, or equivalent)
- Transition list or analyte information (protein, peptide, precursor m/z, charge state)

## Outputs

- Peak boundary coordinates (retention time start, retention time end, peak apex retention time)
- Peak metrics (area, height, signal-to-noise ratio, symmetry)
- Annotated chromatogram plot with boundary markers (Bokeh interactive figure)
- CSV table of peak boundaries and metrics for selected analytes
- Peak picking parameter optimization report (if on-the-fly tuning applied)

## How to apply

Load the extracted ion chromatogram (XIC) or ion mobilogram (IM) into MassDash alongside search results metadata (retention time, ion mobility coordinates from DIA-NN or OpenSwath). Visualize the extracted trace(s) using MassDash's interactive Bokeh-based chromatogram viewer. Optionally apply automated peak picking (via MRMTransitionGroupPicker or pyMRMTransitionGroupPicker) to algorithmically detect boundaries, or manually inspect and adjust boundary markers in the interactive UI. Peak boundaries are identified as the local minima flanking each peak apex or as the retention time range where signal crosses a user-configurable threshold. Export identified boundary coordinates (retention time start/end, peak area, height) to CSV for validation and quantification downstream.

## Related tools

- **MassDash** (Web-based interactive GUI for visualizing extracted chromatograms and ion mobilograms; enables manual and automated boundary identification) — https://github.com/Roestlab/massdash
- **MRMTransitionGroupPicker** (Automated peak boundary detection via algorithmic peak picking on extracted ion chromatograms) — https://github.com/Roestlab/massdash
- **pyMRMTransitionGroupPicker** (Python-based variant of peak picking algorithm for programmatic boundary identification) — https://github.com/Roestlab/massdash
- **Bokeh** (Interactive visualization library for rendering chromatogram plots with boundary markers and user-adjustable thresholds)
- **InteractiveTwoDimensionPlotter** (Generates 2D retention time vs. ion mobility heatmaps with boundary overlays for visual validation) — https://github.com/Roestlab/massdash

## Evaluation signals

- Peak boundaries align with visually observable signal rise/fall in interactive chromatogram plot; no over-extension into noise baseline or under-inclusion of peak flanks.
- Peak area and height computed from identified boundaries are consistent with expected peptide/protein abundance and match OpenSwath or DIA-NN feature scores (if available).
- Boundary coordinates fall within the user-specified retention time and ion mobility windows; no boundaries extend outside extraction parameters.
- When peak-picking parameters are tuned, iterative adjustment reduces false positive (noise-derived) boundaries and improves recall on true analyte peaks (verified by manual inspection or spike-in standard).
- CSV export contains no missing or zero-valued boundary coordinates; all selected analytes yield valid start/end retention time pairs.

## Limitations

- Boundary identification is sensitive to trace smoothing and baseline subtraction settings; suboptimal preprocessing can shift or obscure true peak boundaries.
- Co-eluting isobars or overlapping peaks with similar m/z and retention time may not be resolved; boundaries will reflect the combined signal unless prior targeted extraction parameters isolate individual analytes.
- Automated peak picking (MRMTransitionGroupPicker) accuracy depends on peak shape regularity; highly asymmetric or multi-modal peaks may be mis-segmented or assigned incorrect boundaries.
- Ion mobility resolution in diaPASEF data is instrumental; low-resolution or noisy ion mobility data may prevent accurate boundary delineation in the IM dimension.

## Evidence

- [other] Peak-picking can also be applied as in the first workflow, specifically for the extracted ion chromatograms: "Peak-picking can also be applied as in the first workflow, specifically for the extracted ion chromatograms"
- [other] The main panel provides visualizations of the extraction ion chromatogram: "The main panel provides visualizations of the extraction ion chromatogram"
- [other] possible to visualize the peak boundaries identified by OpenSwath: "possible to visualize the peak boundaries identified by OpenSwath"
- [other] For one dimensional plots, the user can visualize the extracted spectra, chromatogram and mobilogram: "For one dimensional plots, the user can visualize the extracted spectra, chromatogram and mobilogram"
- [other] MassDash is a modular and flexible python package that has a streamlit graphical user interface (GUI): "MassDash is a modular and flexible python package that has a streamlit graphical user interface (GUI)"
- [readme] On the fly parameter optimization - Adjust peak picking parameters on the fly or experiment with novel deep learning based peak picking approaches.: "On the fly parameter optimization - Adjust peak picking parameters on the fly or experiment with novel deep learning based peak picking approaches."
