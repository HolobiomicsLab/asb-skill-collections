---
name: tandem-mass-spectrometry-mirror-plot-construction
description: Use when when you have raw LC-MS or LC-IMS-MS data in instrument format (Agilent .d, Thermo .raw, Bruker .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3634
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Mirador
  - IonToolPack
  - TandemMatch
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

# tandem-mass-spectrometry-mirror-plot-construction

## Summary

Construct MS/MS mirror plots by extracting and formatting tandem mass spectrometry fragmentation spectra for precursor ions within user-specified m/z and retention time ranges, then exporting them as PDF or CSV alongside raw ion chromatograms and mobility heatmaps. Mirror plots enable visual comparison of experimental MS/MS spectra against reference spectra or between different samples.

## When to use

When you have raw LC-MS or LC-IMS-MS data in instrument format (Agilent .d, Thermo .raw, Bruker .d, mzML) with DDA or DIA fragmentation spectra and need to visualize precursor ion fragmentation patterns within specific m/z, retention time (RT), or arrival time (mobility) windows for spectral library matching, quality assessment, or comparative analysis across samples or methods.

## When NOT to use

- Input data lacks MS/MS fragmentation spectra (MS1-only or MS0 data) — use Mirador's XIC/XIM visualization instead
- Precursor ions fall outside all m/z, RT, or mobility ranges defined by the user — adjust parameter ranges or verify data acquisition window
- Data is already processed into a feature table or peak list with no link to raw spectra — use TandemMatch (spectral library matching) on the CSV feature list instead

## Inputs

- Raw mass spectrometry data files (Agilent .d, Thermo .raw, Bruker .d, or mzML format)
- User-specified m/z range (lower and upper bounds in Da)
- User-specified retention time range (in minutes or scan indices)
- User-specified arrival time / ion mobility range (if LC-IMS-MS data)
- Mass tolerance parameter (in Da or ppm)
- Time tolerance parameter (in minutes or mobility drift bins)

## Outputs

- MS/MS mirror plot visualizations (PDF format)
- MS/MS spectral data tables (CSV format) with m/z, intensity, and metadata
- Extracted ion chromatograms (XIC) for precursor ions (PDF and CSV)
- Extracted ion mobility (XIM) heatmaps (if IMS data present; PDF and CSV)

## How to apply

Load raw MS data containing MS/MS spectra into Mirador (part of IonToolPack). Specify the m/z range, retention time range, and arrival-time (if IMS data) range that define your precursor ions of interest, along with mass tolerances. Mirador extracts all MS/MS spectra matching these parameters and automatically formats them as mirror plots, showing experimental spectra aligned against reference or comparative spectra. Export the formatted mirror plots as PDF (for visualization) or CSV (for tabular data and downstream analysis). The extraction respects user-customizable m/z and time tolerances to handle measurement uncertainty and chromatographic peak width.

## Related tools

- **Mirador** (Primary tool that extracts, formats, and exports MS/MS mirror plots from raw MS data using customizable m/z, RT, and arrival-time ranges) — https://github.com/pnnl/IonToolPack
- **TandemMatch** (Performs MS/MS spectral library matching on the CSV-exported mirror plot spectra to annotate fragment ions and identify precursor compounds) — https://github.com/pnnl/IonToolPack
- **IonToolPack** (Software suite hosting Mirador and providing multi-format MS data reading (Agilent, Thermo, Bruker, mzML) and omics-agnostic GUI) — https://github.com/pnnl/IonToolPack

## Evaluation signals

- Mirror plots contain aligned MS/MS spectra with correct m/z axis range and intensity normalization, showing clear fragment ion peaks
- Exported CSV files list all fragment m/z values, intensities, and precursor m/z with no missing or truncated rows
- All exported spectra fall within the user-specified m/z ± tolerance, RT ± tolerance, and arrival-time ± tolerance windows (if applicable)
- PDF and CSV export file sizes are proportional to the number of precursor ions in the specified ranges (no unexpected truncation or bloat)
- Mirror plots can be successfully imported into spectral library matching tools (e.g., TandemMatch) without format errors

## Limitations

- Mirador requires raw data in supported instrument formats (Agilent .d, Thermo .raw, Bruker .d, mzML); other vendor formats may fail silently or require prior conversion
- Mirror plots are only informative when MS/MS spectra are present in the data; DDA mode captures fragmentation only for precursors that exceed signal thresholds, so rare or low-abundance precursors may not appear
- IMS arrival-time range specification requires LC-IMS-MS data; classical LC-MS data will ignore arrival-time parameters and only filter on m/z and RT
- Very large m/z ranges or tight time tolerances may produce insufficient precursor ions to generate meaningful mirror plots; visualization utility depends on precursor abundance
- No changelog is publicly available, limiting visibility into version-specific bug fixes or feature additions

## Evidence

- [other] Mirador exports raw MS visualizations in PDF and CSV formats, including XIC, XIM heatmaps, and MS/MS mirror plots, with user-customizable m/z, retention time, and arrival time ranges and tolerances.: "Mirador exports raw MS visualizations in PDF and CSV formats, including XIC, XIM heatmaps, and MS/MS mirror plots, with user-customizable m/z, retention time, and arrival time ranges and tolerances."
- [other] Extract and format MS/MS mirror plots for precursor ions within the specified ranges.: "Extract and format MS/MS mirror plots for precursor ions within the specified ranges."
- [readme] Raw MS data visualization and export (PDF, CSV) including extracted ion chromatograms (XIC), extracted ion mobility (XIM) heatmaps, and MS/MS mirror plots with customizable m/z, RT, and arrival time ranges and tolerances.: "Raw MS data visualization and export (PDF, CSV) including extracted ion chromatograms (XIC), extracted ion mobility (XIM) heatmaps, and MS/MS mirror plots with customizable m/z, RT, and arrival time"
- [readme] It reads data from multiple instrument formats, requires no installation and provides omics agnostic functionalities (metabolomics, lipidomics, proteomics, etc.): "It reads data from multiple instrument formats, requires no installation and provides omics agnostic functionalities"
- [readme] Supported formats include Agilent 'd', Thermo '.raw', Bruker 'd', and mzML, and for different types of MS acquisition methods: LC-MS, LC-IMS-MS, With/without fragmentation spectra in DDA or DIA mode, Direct infusion: "Supported formats include Agilent 'd', Thermo '.raw', Bruker 'd', and mzML, and for different types of MS acquisition methods: LC-MS, LC-IMS-MS"
