---
name: spectral-mz-window-filtering
description: Use when when you have resolved mzML or mzXML spectrum files and need to isolate signals for a target m/z value (e.g., 870.954) across all retention times or a specific scan.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - GNPS LCMS Visualization Dashboard
  - pyteomics
  - mzmine
  techniques:
  - LC-MS
  - tandem-MS
derived_from:
- doi: 10.1038/s41592-021-01339-5
  title: GNPS Dashboard
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_gnps_dashboard_cq
    doi: 10.1038/s41592-021-01339-5
    title: GNPS Dashboard
  dedup_kept_from: coll_gnps_dashboard_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41592-021-01339-5
  all_source_dois:
  - 10.1038/s41592-021-01339-5
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-mz-window-filtering

## Summary

Filter mass spectrometry scans to extract signals within a specified mass-to-charge (m/z) tolerance window, isolating ions of interest for downstream chromatographic or spectral analysis. This is a foundational step in extracted-ion chromatogram (XIC) computation and targeted metabolite detection.

## When to use

When you have resolved mzML or mzXML spectrum files and need to isolate signals for a target m/z value (e.g., 870.954) across all retention times or a specific scan. Use this skill when you want to compute XICs, perform targeted feature extraction, or visually inspect intensity profiles for a known compound mass with a defined tolerance (e.g., ±0.5 Th or in ppm).

## When NOT to use

- Input is already a feature table or pre-computed XIC matrix—filtering has already been applied.
- MS2/MS3 fragmentation scans are the primary target; this skill is designed for MS1-level isolation.
- Mass tolerance is not specified or cannot be justified by instrument specifications; filtering without a well-defined window risks loss of true signal or inclusion of noise.

## Inputs

- mzML or mzXML spectrum file (resolved, centroided or profile MS1 scans)
- target m/z value (numeric, e.g., 870.954)
- mass tolerance parameter (numeric, e.g., 0.5 Th or 5 ppm)

## Outputs

- Filtered m/z signals within the tolerance window for each scan
- Paired retention time and summed intensity values (two-column data format)
- Extracted-ion chromatogram (XIC) intensity-vs-retention-time profile

## How to apply

Load the mzML or mzXML file using a mass spectrometry data parser (e.g., pyteomics or mzmine). For each MS1 scan, filter all m/z signals to retain only those within the specified mass tolerance window—typically defined as xicmz ± tolerance in Daltons or parts-per-million. Record the retention time and summed intensity across the filtered m/z range for each scan. The filtering decision should account for the instrument's mass accuracy and the width of the isotopic envelope; common practice uses 0.5 Th tolerance for high-resolution instruments. Export or tabulate the filtered retention time and intensity as paired values.

## Related tools

- **GNPS LCMS Visualization Dashboard** (Web interface for accepting resolved mzML/mzXML files and parameters (xicmz, xic_tolerance, xic_norm) to compute and visualize filtered XICs interactively) — github.com/Wang-Bioinformatics-Lab/GNPS_LCMSDashboard
- **pyteomics** (Python library for parsing and reading MS data formats (mzML, mzXML) programmatically)
- **mzmine** (Desktop/batch tool for mass spectrometry data processing, including m/z window filtering and feature extraction)

## Examples

```
https://gnps-lcms.ucsd.edu/?usi=mzspec%3AMSV000084951%3AAH22&xicmz=870.9543493652343&xic_tolerance=0.5&xic_norm=False&show_ms2_markers=True
```

## Evaluation signals

- Verify that all retained m/z values fall within xicmz ± tolerance (e.g., 870.954 ± 0.5 Th ⟹ [870.454, 871.454]).
- Check that summed intensities are positive and non-zero for at least some scans; zero or NaN intensity across all scans indicates filtering removed all signal.
- Confirm output XIC profile shows a coherent retention-time peak (single or multi-modal distribution), not random or uniform intensity across time.
- Compare the m/z window filter output against the raw spectrum image preview to visually validate that the correct ion envelope was isolated.
- For multi-file comparisons, verify that the same m/z and tolerance parameters produce comparable XIC shapes across files (e.g., same peak location in retention time).

## Limitations

- Mass tolerance must be specified a priori; incorrect tolerance (too narrow or too wide) will either miss the target signal or include interfering ions.
- Profile-mode data may include baseline noise; summing raw intensities without peak-picking can inflate the extracted signal if not pre-filtered.
- High mass accuracy instruments (e.g., <5 ppm) may require narrower tolerance windows; low-resolution instruments (e.g., >100 ppm) may need broader windows, affecting selectivity.
- Overlapping isotopic envelopes or isobaric compounds within the tolerance window will be co-extracted and cannot be separated by this filtering step alone.

## Evidence

- [other] The dashboard accepts resolved mzML/mzXML spectrum files and parameters including xicmz (target m/z value, e.g. 870.954), xic_tolerance (mass tolerance window, e.g. 0.5): "The dashboard accepts resolved mzML/mzXML spectrum files and parameters including xicmz (target m/z value, e.g. 870.954), xic_tolerance (mass tolerance window, e.g. 0.5)"
- [other] Filter all MS1 scans to extract signals within the specified m/z tolerance window (e.g., xicmz ± tolerance in ppm or Th).: "Filter all MS1 scans to extract signals within the specified m/z tolerance window (e.g., xicmz ± tolerance in ppm or Th)"
- [other] Load the mzML or mzXML file using a mass spectrometry data parser (e.g., pyteomics or mzmine).: "Load the mzML or mzXML file using a mass spectrometry data parser (e.g., pyteomics or mzmine)"
- [other] For each scan, record the retention time and summed intensity across the filtered m/z range.: "For each scan, record the retention time and summed intensity across the filtered m/z range"
- [other] Tabulate retention time and intensity as paired values and export as a two-column data file (retention_time, intensity).: "Tabulate retention time and intensity as paired values and export as a two-column data file (retention_time, intensity)"
