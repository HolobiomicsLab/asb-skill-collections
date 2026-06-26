---
name: m-z-intensity-feature-extraction
description: Use when you have imported mass spectrometry data in .raw, .d, or mzXML
  format and need to inspect peak structure, verify instrument performance, or generate
  baseline visualizations before downstream peak annotation or statistical analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - R
  - R GUI
  - SMART
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# m-z-intensity-feature-extraction

## Summary

Extract and visualize mass-to-charge (m/z) ratio and ion intensity features from raw mass spectrometry data by loading imported MS files, aggregating intensities across retention time ranges, and generating publication-quality TIC and mass spectrum plots. This skill bridges raw instrumental output to interpretable metabolomics visualizations.

## When to use

Apply this skill when you have imported mass spectrometry data in .raw, .d, or mzXML format and need to inspect peak structure, verify instrument performance, or generate baseline visualizations before downstream peak annotation or statistical analysis. Use it as an early exploratory step to confirm data integrity and identify retention time windows of interest.

## When NOT to use

- Data has already been preprocessed, normalized, or converted to a feature table; use visualization on the feature table directly instead.
- Only aggregate-level statistics or statistical test results are needed; this skill is for raw feature inspection, not statistical modeling.
- Input is a different mass spectrometry format not supported by the Data Import module (e.g., proprietary vendor formats outside .raw, .d, mzXML).

## Inputs

- Mass spectrometry data file (.raw, .d, or mzXML format)
- Retention time range or scan index range (optional, for targeted spectrum extraction)

## Outputs

- Total Ion Chromatogram (TIC) plot (intensity vs. retention time)
- Mass spectrum plot(s) (m/z vs. ion intensity for selected retention time/scan range)
- High-resolution image files (exported visualizations)

## How to apply

Load the imported MS data file into the R environment via SMART's Data Import module (supporting .raw, .d, and mzXML formats). Extract TIC data by aggregating ion intensities across all m/z values for each scan/retention time point, then generate a TIC plot with intensity (y-axis) versus retention time (x-axis). For detailed mass spectrum inspection, select one or more specific retention time points or scan ranges of interest, extract the corresponding m/z and intensity pairs, and generate mass spectrum plots with m/z (x-axis) versus ion intensity (y-axis). Export all visualizations as high-resolution image files suitable for downstream reporting and publication.

## Related tools

- **SMART** (R-based metabolomics platform providing Data Import and Data Visualization modules for m/z-intensity feature extraction and TIC/mass spectrum rendering) — github.com/YuJenL/SMART
- **R** (Underlying statistical and graphical programming language in which SMART is written)
- **R GUI** (User-friendly graphical interface for SMART workflows, reducing command-line overhead for interactive m/z-intensity visualization)

## Evaluation signals

- TIC plot shows a single smooth or multi-modal intensity trace across retention time with no missing data or gaps in the chromatogram.
- Mass spectrum plots display distinct m/z peaks with ion intensities that match the intensity range reported in the instrument's raw output metadata.
- Exported image files are high-resolution and render peaks with sharp, reproducible visual geometry across multiple exports.
- TIC and mass spectrum features align with known reference standards or positive controls run on the same instrument/day.
- Retention time ranges extracted correspond to the correct scan indices in the source file, verified by spot-checking against the raw file's scan metadata.

## Limitations

- The skill depends on successful import of the source file; .raw, .d, or mzXML formats must be correctly formatted and not corrupted.
- TIC aggregation assumes all m/z values are equally relevant; high-abundance background ions or solvent peaks may dominate the chromatogram if not pre-filtered.
- Mass spectrum plots at a single retention time point may not capture temporal dynamics of co-eluting compounds; multi-scan integration may be needed for complex mixtures.
- No changelog is available for SMART, so reproducibility across software versions may require explicit version pinning or local installation testing.

## Evidence

- [readme] File format support and aggregation method: "Data Import: Analyze different data file formats (e.g., .raw, .d, and mzXML)."
- [readme] TIC and mass spectrum visualization outputs: "Data Visualization: Visually represent various types of data features (e.g., total ion chromatogram (TIC) and mass spectra)."
- [intro] Workflow details for TIC construction: "Extract and prepare TIC data by aggregating ion intensities across retention time."
- [intro] Mass spectrum extraction procedure: "Extract and prepare mass spectrum data for selected retention time points or scan ranges."
- [intro] Export format specification: "Export all visualizations as high-resolution image files suitable for downstream analysis and reporting."
