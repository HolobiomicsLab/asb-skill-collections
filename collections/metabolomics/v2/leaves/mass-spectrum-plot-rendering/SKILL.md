---
name: mass-spectrum-plot-rendering
description: Use when after importing and preprocessing mass spectrometry data (in
  .raw, .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - R
  - R GUI
  - R GUI (SMART)
  techniques:
  - mass-spectrometry
  license_tier: open
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

# mass-spectrum-plot-rendering

## Summary

Generate publication-ready mass spectrum plots (m/z vs. ion intensity) from selected retention time points or scan ranges in mass spectrometry data. This skill transforms raw spectral data into interpretable visualizations for metabolomics feature identification and reporting.

## When to use

After importing and preprocessing mass spectrometry data (in .raw, .d, or mzXML format) within the SMART pipeline, when you need to visually inspect ion fragmentation patterns, identify molecular features at specific retention times, or generate figures for downstream peak annotation and metabolite identification.

## When NOT to use

- Input data has not been imported or is in an unsupported format (not .raw, .d, or mzXML) — use Data Import module first.
- No specific retention time points or scan ranges have been selected — use peak detection or targeted analysis parameters to define regions of interest.
- Only a summary total ion chromatogram (TIC) is needed — use TIC rendering instead.

## Inputs

- Preprocessed mass spectrometry data (format: .raw, .d, or mzXML)
- Retention time point(s) or scan range specification
- Ion intensity matrix indexed by m/z and scan number

## Outputs

- Mass spectrum plot (2D scatter/line plot: m/z vs. intensity)
- High-resolution image file (e.g., PNG, PDF) for reporting

## How to apply

Load preprocessed mass spectrometry data into the R environment via SMART's Data Import module. Extract mass spectrum data for one or more selected retention time points or scan ranges (user-specified as region of interest). Prepare spectral intensities aggregated by m/z value. Generate a 2D plot with m/z on the x-axis and ion intensity on the y-axis using SMART's Data Visualization module. Export the rendered plot as a high-resolution image file suitable for reporting and downstream annotation workflows. Rationale: targeted spectral visualization at specific retention times isolates the chemical complexity at those points, enabling manual or algorithmic peak identification and isotope pattern recognition.

## Related tools

- **R** (Execution engine for spectral data extraction, aggregation, and plotting logic)
- **R GUI (SMART)** (User-friendly interface for selecting retention times, configuring plot parameters, and exporting visualizations) — github.com/YuJenL/SMART

## Evaluation signals

- Plot displays correctly scaled axes: m/z values on x-axis (numeric range matching the instrument's detector), intensity on y-axis (non-negative, with scale appropriate to max peak height).
- All peaks in the specified retention time or scan range are represented; no m/z values or intensities are missing or truncated.
- Image file is generated at expected resolution and format (high-resolution PNG or PDF suitable for publication).
- Peak positions and relative intensities match the underlying mass spectrum data (spot-check against raw data array for ±1 m/z and ±5% intensity tolerance).
- Visualization is reproducible: re-running with the same retention time/scan range and export settings yields pixel-identical output.

## Limitations

- Visualization quality depends on correct retention time or scan range selection; mis-specified regions will render misleading or empty spectra.
- Very high m/z ranges or dense peak clusters may suffer from visual crowding; user may need to zoom or filter by intensity threshold for clarity.
- No changelog or version history provided in repository; potential compatibility issues across SMART versions for reproducibility.

## Evidence

- [other] Extract and prepare mass spectrum data for selected retention time points or scan ranges.: "Extract and prepare mass spectrum data for selected retention time points or scan ranges."
- [other] Generate mass spectrum plots displaying m/z values versus ion intensities.: "Generate mass spectrum plots displaying m/z values versus ion intensities."
- [other] Export all visualizations as high-resolution image files suitable for downstream analysis and reporting.: "Export all visualizations as high-resolution image files suitable for downstream analysis and reporting."
- [readme] Data Visualization: Visually represent various types of data features (e.g., total ion chromatogram (TIC) and mass spectra).: "Data Visualization: Visually represent various types of data features (e.g., total ion chromatogram (TIC) and mass spectra)."
- [other] Load imported mass spectrometry data (supporting .raw, .d, and mzXML formats) into the R environment.: "Load imported mass spectrometry data (supporting .raw, .d, and mzXML formats) into the R environment."
