---
name: retention-time-range-filtering
description: Use when you have raw IM-MS data (Agilent MassHunter .d or UIMF format)
  and need to exclude early or late chromatographic regions—e.g., to skip dead volume,
  exclude blank runs, focus on a known analyte window, or reduce file size for faster
  processing.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - PNNL PreProcessor
  - Agilent MassHunter
  techniques:
  - ion-mobility-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/jasms.4c00220
  title: PNNL PreProcessor
- doi: 10.1021/acs.jproteome.1c00425
  title: ''
evidence_spans:
- we have developed this user-friendly tool for Agilent MassHunter (.d) and UIMF mass
  spectrometry data files
- we have developed this user-friendly tool for Agilent MassHunter (.d) and UIMF mass
  spectrometry data files (MS-files) from drift tube (DT) and structure for lossless
  ion manipulations (SLIM) IM-MS
- Agilent MassHunter (.d) and UIMF mass spectrometry data files (MS-files)
- Agilent MassHunter (.d) and UIMF mass spectrometry data files
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metabcombiner_cq
    doi: 10.1021/acs.analchem.0c03693
    title: metabCombiner
  - build: coll_pnnl_preprocessor_cq
    doi: 10.1021/jasms.4c00220
    title: PNNL PreProcessor
  dedup_kept_from: coll_pnnl_preprocessor_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.4c00220
  all_source_dois:
  - 10.1021/jasms.4c00220
  - 10.1021/acs.jproteome.1c00425
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# retention-time-range-filtering

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Selectively isolate IM-MS data within a user-defined retention time window to focus downstream preprocessing on the relevant chromatographic region. This reduces computational overhead and concentrates analysis on regions of interest before compression, interpolation, and demultiplexing.

## When to use

Apply this skill when you have raw IM-MS data (Agilent MassHunter .d or UIMF format) and need to exclude early or late chromatographic regions—e.g., to skip dead volume, exclude blank runs, focus on a known analyte window, or reduce file size for faster processing. Use it as the first filtering step after loading raw MS-files into PNNL PreProcessor and before applying data compression.

## When NOT to use

- Input data are already compressed, interpolated, or demultiplexed; filtering must occur before these downstream steps.
- The analyte(s) of interest have unknown or broad elution profiles that may span an unpredictable retention time range; exploratory analysis without pre-filtering is more appropriate.
- The analysis goal requires retention of the full chromatographic dimension for statistical or quality-control comparisons across the entire run.

## Inputs

- Raw IM-MS data file (Agilent MassHunter .d format or UIMF format)
- Retention time range specification (minimum and maximum retention time in minutes)

## Outputs

- Retention-time-filtered raw IM-MS data (intermediate format, ready for compression and interpolation)
- Metadata indicating applied retention time bounds

## How to apply

In the PNNL PreProcessor workflow, specify a retention time range (minimum and maximum bounds in minutes) during the data loading and compression step. The tool will filter frames by the specified retention time range, discarding all scans and frames outside the window. This filtering occurs before data compression by frame and mobility dimension and before interpolation of the ion mobility dimension. The rationale is that limiting the temporal scope reduces memory footprint and processing time while preserving the signal in the region of interest for subsequent HRdm demultiplexing and peak deconvolution steps.

## Related tools

- **PNNL PreProcessor** (Primary software platform in which retention time range filtering is applied as a configurable parameter during data loading and compression) — https://github.com/PNNL-Comp-Mass-Spec/PNNL-PreProcessor
- **Agilent MassHunter** (Instrument vendor software that produces the raw .d format input files compatible with retention time filtering in PNNL PreProcessor)

## Evaluation signals

- Verify that the output frame count and retention time range in the filtered data match the specified bounds (e.g., if filtering 2–8 min, all frames should have retention times ≥ 2.0 and ≤ 8.0 min).
- Confirm that frames outside the specified retention time window are absent from the filtered dataset by spot-checking metadata or header information.
- Check that the total file size of the filtered output is smaller than the unfiltered input (indicating successful exclusion of out-of-range scans).
- Validate that downstream processing steps (compression, interpolation, demultiplexing) complete without error and produce expected output dimensionality.
- Compare ion count and intensity histograms before and after filtering to confirm signal preservation within the window and signal removal outside it.

## Limitations

- Retention time range filtering is irreversible; discarded data outside the window cannot be recovered. Incorrect or overly narrow bounds will permanently lose chromatographic information.
- The tool does not automatically detect the optimal retention time window; users must specify bounds manually based on prior knowledge of analyte elution or exploratory preview of the raw file.
- Filtering by a single continuous retention time range cannot handle complex study designs with multiple disjoint regions of interest (e.g., analytes eluting in two separate windows); multiple preprocessing runs would be required.
- The filtering step assumes retention time values are accurately recorded in the raw data; clock drift, gradient errors, or instrument artifacts may cause retention time misalignment and lead to unexpected exclusion of valid data.

## Evidence

- [methods] Data compression (by frame and mobility) and filtering by retention time range: "Data compression (by frame and mobility) and filtering by retention time range"
- [other] Apply data compression by frame and mobility dimension, and filter frames by retention time range if specified.: "Apply data compression by frame and mobility dimension, and filter frames by retention time range if specified"
- [other] Load raw MS-file (Agilent MassHunter .d or UIMF format) into PNNL PreProcessor.: "Load raw MS-file (Agilent MassHunter .d or UIMF format) into PNNL PreProcessor"
- [readme] data compression and interpolation, ion mobility demultiplexing, multidimensional smoothing, noise filtering by low intensity threshold and spike removal, saturation repair and metadata export: "data compression and interpolation, ion mobility demultiplexing, multidimensional smoothing, noise filtering by low intensity threshold and spike removal, saturation repair and metadata export"
