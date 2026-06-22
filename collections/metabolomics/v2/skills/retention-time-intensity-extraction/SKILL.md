---
name: retention-time-intensity-extraction
description: Use when when you have imported mass spectrometry data in .raw, .d, or mzXML format and need to generate a TIC plot to visualize overall sample ionization intensity as a function of retention time.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - R
  - R GUI
  - SMART
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1021/acs.analchem.5c03225
  title: SMART 2.0
evidence_spans:
- SMART written in R and R GUI has been developed as user-friendly software
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_smart_2_0_cq
    doi: 10.1021/acs.analchem.5c03225
    title: SMART 2.0
  dedup_kept_from: coll_smart_2_0_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c03225
  all_source_dois:
  - 10.1021/acs.analchem.5c03225
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# retention-time-intensity-extraction

## Summary

Extract and aggregate ion intensities across retention time from mass spectrometry data to prepare total ion chromatogram (TIC) data for visualization. This skill converts raw m/z and intensity observations into retention-time-indexed intensity profiles suitable for chromatographic analysis.

## When to use

When you have imported mass spectrometry data in .raw, .d, or mzXML format and need to generate a TIC plot to visualize overall sample ionization intensity as a function of retention time. Use this skill as a prerequisite step before rendering chromatographic visualizations or performing retention-time-based peak analysis.

## When NOT to use

- Input data is already in aggregated or feature-table format (e.g., peak intensity matrix or aligned feature table) — skip directly to visualization.
- Analysis goal is targeted identification of specific m/z features — use mass spectrum extraction at selected retention time points instead.
- Data contains only pre-processed peak lists without scan-level intensity arrays — TIC reconstruction from peak lists may introduce bias.

## Inputs

- Imported mass spectrometry data (formats: .raw, .d, mzXML)
- Scan-level ion intensity and retention time pairs
- Mass spectrum intensity matrix (scans × m/z)

## Outputs

- TIC data vector (retention time indexed intensity values)
- TIC plot (intensity versus retention time visualization)
- High-resolution image file of TIC plot

## How to apply

Load the imported mass spectrometry data into the R environment and extract scan-level ion intensity measurements indexed by retention time. Aggregate all m/z ion intensities within each scan (summing across the mass-to-charge dimension) to produce a single intensity value per retention time point. This aggregation produces a one-dimensional intensity profile indexed by retention time. Export the aggregated intensity-versus-retention-time vectors as data structures suitable for plotting. The rationale is that TIC aggregation compresses the full m/z dimension while preserving temporal (retention time) resolution, enabling visual inspection of ionization behavior across the entire chromatographic run.

## Related tools

- **R** (Programming environment for loading, aggregating, and manipulating mass spectrometry ion intensity and retention time data)
- **R GUI** (User-friendly graphical interface for SMART Data Visualization module to interactively extract and render TIC and mass spectrum plots) — github.com/YuJenL/SMART
- **SMART** (Integrated platform providing Data Visualization module that executes retention-time-intensity extraction and TIC rendering as part of the complete metabolomics analysis workflow) — github.com/YuJenL/SMART

## Evaluation signals

- TIC intensity values are positive and non-zero across the expected retention time range of the chromatographic run.
- Retention time values are monotonically increasing and span the full acquisition window (e.g., 0–60 minutes for typical LC–MS).
- TIC plot shows expected chromatographic peaks (local intensity maxima) at known or biologically plausible retention times.
- Exported high-resolution image file is readable and displays smooth intensity profile without artifacts or extreme spikes indicative of aggregation errors.
- Ion intensity sums per scan are consistent with raw scan-level total ion counts (summing TIC intensity across all scans should approximate total ions in raw file).

## Limitations

- Aggregation loses m/z resolution; multiplex features at the same retention time cannot be distinguished. For targeted or high-mass-resolution analyses, extract individual mass spectra at selected retention time points instead.
- Baseline drift and instrument noise are preserved in the aggregated TIC; downstream quality control and baseline correction may be required for accurate peak detection.
- TIC does not account for ionization efficiency variation across the mass range; m/z regions with naturally high ion abundance may dominate the TIC and obscure lower-abundance features.

## Evidence

- [other] Extract and prepare TIC data by aggregating ion intensities across retention time.: "Extract and prepare TIC data by aggregating ion intensities across retention time."
- [other] Generate a TIC plot displaying intensity versus retention time.: "Generate a TIC plot displaying intensity versus retention time."
- [other] Load imported mass spectrometry data (supporting .raw, .d, and mzXML formats) into the R environment.: "Load imported mass spectrometry data (supporting .raw, .d, and mzXML formats) into the R environment."
- [readme] Data Visualization: Visually represent various types of data features (e.g., total ion chromatogram (TIC) and mass spectra).: "Data Visualization: Visually represent various types of data features (e.g., total ion chromatogram (TIC) and mass spectra)."
- [other] Export all visualizations as high-resolution image files suitable for downstream analysis and reporting.: "Export all visualizations as high-resolution image files suitable for downstream analysis and reporting."
