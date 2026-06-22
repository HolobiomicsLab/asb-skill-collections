---
name: fiams-spectra-window-extraction-and-merging
description: Use when you have raw FIA-MS full-scan data in mzML format and need to prepare it for untargeted metabolite discovery. Apply this skill when your goal is to detect and annotate unknown metabolites across a wide m/z range (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - SmartPeak
  - SmartPeakGUI
  - SmartPeakCLI
  - OpenMS
  - pyOpenMS
  techniques:
  - direct-infusion-MS
derived_from:
- doi: 10.1021/acs.analchem.0c03421
  title: SmartPeak
evidence_spans:
- SmartPeak automates targeted and quantitative metabolomics data processing
- SmartPeak GUI provides functionality to facilitate users to get up and running as quickly as possible
- SmartPeak CLI provides an equivalent of SmartPeak GUI application, however with a possibility to run in headless mode
- SmartPeak CLI provides an equivalent of SmartPeak GUI application
- The software is based on the OpenMS toolkit
- The software is based on the OpenMS toolkit.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_smartpeak_cq
    doi: 10.1021/acs.analchem.0c03421
    title: SmartPeak
  dedup_kept_from: coll_smartpeak_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.0c03421
  all_source_dois:
  - 10.1021/acs.analchem.0c03421
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# FIA-MS Spectra Window Extraction and Merging

## Summary

Extract and merge mass spectrometry spectra windows from full-scan FIA-MS data to compress multi-dimensional spectral arrays into time-integrated feature matrices suitable for MS1 peak detection. This skill bridges raw data acquisition and untargeted metabolite annotation by reducing data volume while preserving spectral information across the acquisition time window.

## When to use

You have raw FIA-MS full-scan data in mzML format and need to prepare it for untargeted metabolite discovery. Apply this skill when your goal is to detect and annotate unknown metabolites across a wide m/z range (e.g., 0–1500 m/z) without predefined transitions, and you want to reduce computational burden by binning spectra temporally rather than analyzing each spectrum individually.

## When NOT to use

- Input is already a peak-picked feature table or mzTab file — use only with raw spectra.
- You are performing targeted metabolomics with predefined MRM transitions — use chromatogram extraction instead.
- Your FIA-MS data has very low resolution or extremely wide m/z ranges requiring different binning strategies than those supported by your SmartPeak configuration.

## Inputs

- Raw mass spectrometry data (mzML format)
- FIA-MS acquisition parameters (time range, m/z range, resolution)

## Outputs

- Merged spectra matrix (time-binned, m/z-resolved)
- Time-binned spectral feature intensity data ready for MS1 peak detection

## How to apply

First, load raw mass spectrometry data using LOAD_RAW_DATA. Then extract spectra windows over your full acquisition time range (e.g., 0–30 min) using EXTRACT_SPECTRA_WINDOWS, setting mass resolution (e.g., FIAMS resolution = 12000) and maximum m/z threshold (e.g., max_mz = 1500) appropriate for your instrument and compound targets. Next, merge the extracted spectra along the time axis using MERGE_SPECTRA with a temporal bin step (e.g., bin_step = 20 seconds) to aggregate signals and reduce noise. This consolidation is critical for FIA-MS workflows because it converts a large time-series of individual spectra into a smaller set of composite spectra, reducing memory and computation while retaining signal intensity for subsequent peak picking. The bin step and resolution settings should be chosen based on your ion source dwell time and target compound mass accuracy requirements.

## Related tools

- **SmartPeak** (Orchestrates the full workflow including EXTRACT_SPECTRA_WINDOWS and MERGE_SPECTRA operations via configuration files) — https://github.com/AutoFlowResearch/SmartPeak
- **SmartPeakCLI** (Command-line interface for running spectra extraction and merging without GUI) — https://github.com/AutoFlowResearch/SmartPeak
- **OpenMS** (Underlying C++ toolkit providing spectral window extraction and merging algorithms)
- **pyOpenMS** (Python bindings enabling programmatic access to spectral processing functions)

## Examples

```
docker run --rm -ti -v C:/data:/sample-data autoflowresearch/smartpeak-cli:latest SmartPeakCLI --input_path /sample-data/workflow_FIAMS_Unknowns.csv --output_path /sample-data/results
```

## Evaluation signals

- Merged spectra matrix dimensions are consistent with expected time bins and m/z resolution (e.g., (n_timepoints, n_mz_bins))
- Total signal intensity is conserved or increases after merging (no loss of ionization counts)
- Spectral noise is reduced compared to individual raw spectra (signal-to-noise ratio improves for low-intensity features)
- Downstream MS1 peak picking on merged spectra yields stable, reproducible feature lists across replicate FIA-MS injections
- m/z axis maintains specified mass accuracy (e.g., <5 ppm deviation for 12000 resolution setting)

## Limitations

- Temporal binning may blur transient peaks if bin_step is too coarse relative to ion source dwell time; narrow peaks may be lost.
- High m/z resolution settings (e.g., 12000) increase memory footprint during merging; very wide m/z ranges (>1500 m/z) may require iterative processing.
- The skill assumes spectra are uniformly sampled in time; variable acquisition rates or instrument dropouts may cause artifacts in merged spectra.
- No built-in quality flagging; invalid or saturated spectra are merged without filtering, potentially degrading feature quality downstream.

## Evidence

- [methods] Extract spectra windows over the acquisition time range (0–30 min) using EXTRACT_SPECTRA_WINDOWS with FIAMS resolution set to 12000 and max_mz to 1500.: "Extract spectra windows over the acquisition time range (0–30 min) using EXTRACT_SPECTRA_WINDOWS with FIAMS resolution set to 12000 and max_mz to 1500."
- [methods] Merge spectra along the time axis using bin_step of 20 with MERGE_SPECTRA.: "Merge spectra along the time axis using bin_step of 20 with MERGE_SPECTRA."
- [methods] SmartPeak automates workflow steps from peak detection and integration over calibration curve optimization, to quality control reporting, which form the basis for configuring analysis types such as FIAMS FullScan Unknowns.: "SmartPeak automates workflow steps from peak detection and integration over calibration curve optimization, to quality control reporting"
- [readme] The software is based on the OpenMS toolkit.: "The software is based on the OpenMS toolkit."
- [methods] These files can be parsed and processed by the pyOpenMS Python package.: "These files can be parsed and processed by the pyOpenMS Python package."
