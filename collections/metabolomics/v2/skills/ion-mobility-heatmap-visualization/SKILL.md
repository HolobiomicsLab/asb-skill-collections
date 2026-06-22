---
name: ion-mobility-heatmap-visualization
description: Use when you have raw LC-IMS-MS data (Agilent, Thermo, Bruker, or mzML format) and need to visualize and export the spatial distribution of a specific ion species (or ion family) across both ion mobility and retention time dimensions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Mirador
  - IonToolPack
  - PeakQC
  techniques:
  - LC-MS
  - ion-mobility-MS
  - tandem-MS
derived_from:
- doi: 10.1021/jasms.4c00146
  title: PeakQC
evidence_spans:
- 'Mirador: Raw MS data visualization and export (PDF, CSV) including extracted ion chromatograms (XIC), extracted ion mobility (XIM) heatmaps, and MS/MS mirror plots'
- IonToolPack is a software suite housing tools for mass spectrometry data
- IonToolPack is a software suite housing tools for mass spectrometry data.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_peakqc_cq
    doi: 10.1021/jasms.4c00146
    title: PeakQC
  dedup_kept_from: coll_peakqc_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.4c00146
  all_source_dois:
  - 10.1021/jasms.4c00146
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ion-mobility-heatmap-visualization

## Summary

Generate extracted ion mobility (XIM) heatmaps from raw LC-IMS-MS data by specifying m/z and arrival-time ranges, enabling visualization of ion intensity distributions across mobility and retention time dimensions. This skill is essential for interpreting ion separation and structural dynamics in multidimensional mass spectrometry.

## When to use

You have raw LC-IMS-MS data (Agilent, Thermo, Bruker, or mzML format) and need to visualize and export the spatial distribution of a specific ion species (or ion family) across both ion mobility and retention time dimensions. Apply this skill when you want to extract a subset of ions by m/z and arrival-time range, generate a 2D heatmap representation, and export the visualization as PDF or tabular data (CSV) for publication or further analysis.

## When NOT to use

- Input data is from a traditional LC-MS (without ion mobility dimension) — use extracted ion chromatogram (XIC) instead.
- You require MS/MS fragmentation spectra or spectral library matching — use TandemMatch or Mirador's MS/MS mirror plot feature instead.
- You need to compare heatmaps across multiple acquisition methods or cohorts — use Comparador for harmonized feature comparison.

## Inputs

- Raw mass spectrometry data file (Agilent .d directory, Thermo .raw, Bruker .d, or mzML format)
- m/z range and tolerance (e.g., 500–510 m/z, ±5 ppm)
- Retention time (RT) range in seconds or minutes
- Arrival time (ion mobility) range in milliseconds or inverse reduced mobility units

## Outputs

- Extracted ion mobility (XIM) heatmap in PDF format
- Tabular XIM data in CSV format (retention time, arrival time, intensity matrix)
- Optional: customized visualization parameters logged for reproducibility

## How to apply

Load raw MS data in a supported instrument format (Agilent .d, Thermo .raw, Bruker .d, or mzML) into Mirador. Specify the target m/z range (with user-defined tolerance, typically ppm-based), the retention time window, and the arrival-time (mobility) range boundaries. Mirador extracts all ion intensity signals matching these three-dimensional constraints, bins them into a 2D grid indexed by (retention time, arrival time), and generates a heatmap where intensity is represented as color or gradient. Export the result as both a high-resolution PDF visualization (suitable for figures) and a CSV table containing the binned intensity matrix. Verify output by confirming that the m/z, RT, and arrival-time ranges match your input parameters and that intensity maxima align with expected ion separation patterns for your compounds.

## Related tools

- **Mirador** (Primary tool for raw MS data visualization and XIM heatmap generation, supporting customizable m/z, RT, and arrival-time range extraction and PDF/CSV export.) — https://github.com/pnnl/IonToolPack
- **IonToolPack** (Container suite providing unified GUI access to Mirador and companion tools; handles multi-format data loading and no-installation deployment.) — https://github.com/pnnl/IonToolPack
- **PeakQC** (Optional companion tool for quality assessment of ion signals used to generate heatmaps; applies PCA-based QC and outlier detection on MS1 data.) — https://github.com/pnnl/IonToolPack

## Evaluation signals

- Verify that the exported heatmap intensity range corresponds to the ion count or signal intensity in the input raw file; compare min/max values to raw data statistics.
- Confirm that the CSV matrix dimensions match the binned retention time and arrival-time grid; check for missing or zero-padded cells at grid edges.
- Visual inspection: heatmap should show clustered intensity in expected mobility and RT regions; absence of signal outside specified m/z tolerance indicates correct extraction.
- Reproducibility check: regenerate the heatmap with identical parameters and verify pixel-for-pixel match with previous output.
- Cross-validation: overlay exported CSV data on the PDF heatmap to ensure color/intensity mapping is consistent and colorbar labels are accurate.

## Limitations

- XIM heatmaps require ion mobility (IMS) dimension in the input data; conventional LC-MS data will not produce meaningful 2D mobility separations.
- Arrival-time range and tolerance parameters are instrument-specific and user-defined; incorrect settings may exclude target ions or include chemical noise.
- Export formats (PDF, CSV) are suitable for static visualization and tabular export but do not preserve raw centroid or profile peak shapes; users working with high-resolution isotope patterns may need to inspect raw data directly.
- No changelog provided in repository; version-to-version changes in Mirador heatmap binning or export precision are not formally documented.

## Evidence

- [readme] Mirador: Raw MS data visualization and export (PDF, CSV) including extracted ion chromatograms (XIC), extracted ion mobility (XIM) heatmaps, and MS/MS mirror plots: "**Mirador**: Raw MS data visualization and export (PDF, CSV) including extracted ion chromatograms (XIC), extracted ion mobility (XIM) heatmaps, and MS/MS mirror plots with customizable m/z, RT, and"
- [other] Generate extracted ion mobility (XIM) heatmaps for the specified m/z and arrival-time ranges: "Generate extracted ion mobility (XIM) heatmaps for the specified m/z and arrival-time ranges."
- [readme] Supported formats include Agilent 'd', Thermo '.raw', Bruker 'd', and mzML, and for different types of MS acquisition methods: LC-MS, LC-IMS-MS: "Supported formats include Agilent 'd', Thermo '.raw', Bruker 'd', and mzML, and for different types of MS acquisition methods: * LC-MS * LC-IMS-MS"
- [other] Parse user-specified m/z, retention time (RT), and arrival-time (mobility) range parameters: "Parse user-specified m/z, retention time (RT), and arrival-time (mobility) range parameters."
- [other] Export all visualizations and tabular data as PDF and CSV files: "Export all visualizations and tabular data as PDF and CSV files."
