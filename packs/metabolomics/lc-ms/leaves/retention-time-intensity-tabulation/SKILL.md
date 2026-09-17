---
name: retention-time-intensity-tabulation
description: Use when when you have a resolved mzML or mzXML spectrum file and need
  to visualize or analyze the temporal intensity profile of a specific analyte (defined
  by its m/z value).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - GNPS LCMS Visualization Dashboard
  - pyteomics
  - mzmine
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# retention-time-intensity-tabulation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Extract and tabulate retention time paired with summed intensity values for a target mass-to-charge ratio across all scans in a resolved mzML/mzXML spectrum file. This skill produces a two-column chromatographic profile (retention_time, intensity) suitable for visualization and downstream analysis of LC-MS data.

## When to use

When you have a resolved mzML or mzXML spectrum file and need to visualize or analyze the temporal intensity profile of a specific analyte (defined by its m/z value). Apply this skill when you want to reconstruct an extracted-ion chromatogram (XIC) by filtering MS1 scans within a specified mass tolerance window and recovering the chromatographic shape.

## When NOT to use

- Input spectrum file is already a feature table, intensity matrix, or pre-computed chromatogram; skip to visualization or statistical analysis.
- MS level is not MS1 or the spectrum file contains only MS2/MS3 fragmentation data without parent-scan retention times.
- Target m/z value is unknown or ambiguous; use feature detection or mass calibration workflows first to identify analyte m/z values.

## Inputs

- mzML or mzXML spectrum file (resolved, centroided or profile)
- target m/z value (xicmz, e.g. 870.954)
- mass tolerance (xic_tolerance, e.g. 0.5 Th or ppm)
- normalization flag (xic_norm, boolean or string)

## Outputs

- two-column tabular data file (retention_time, intensity)
- extracted-ion chromatogram (XIC) profile
- intensity-versus-retention-time paired values

## How to apply

Load the mzML or mzXML file using a mass spectrometry parser (e.g., pyteomics or mzmine). Filter all MS1 scans to extract signals within the specified m/z tolerance window (e.g., xicmz ± tolerance in ppm or Th, such as 870.954 ± 0.5). For each scan, record the retention time and sum all intensities across the filtered m/z range. Tabulate the retention time and summed intensity as paired values and export as a two-column data file. Apply normalization if requested (e.g., xic_norm parameter) to scale intensity values relative to the chromatogram's maximum.

## Related tools

- **GNPS LCMS Visualization Dashboard** (Primary tool for accepting resolved mzML/mzXML files and parameters (xicmz, xic_tolerance, xic_norm) and computing and displaying the extracted-ion chromatogram.) — https://github.com/Wang-Bioinformatics-Lab/GNPS_LCMSDashboard
- **pyteomics** (Mass spectrometry data parser library for reading and filtering mzML/mzXML files at the programmatic level.)
- **mzmine** (Standalone mass spectrometry data processing tool for filtering MS1 scans and extracting ion chromatograms.)

## Examples

```
https://gnps-lcms.ucsd.edu/?usi=mzspec%3AMSV000084951%3AAH22&xicmz=870.9543493652343&xic_tolerance=0.5&xic_norm=False&show_ms2_markers=True&ms2_identifier=None
```

## Evaluation signals

- Output file contains exactly two columns with numeric retention time and intensity values, with no missing or malformed entries.
- All output retention times are within the observed range of the input spectrum file (e.g., 0–60 minutes).
- Summed intensity values in the output match hand-calculated sums of all signals within the specified m/z tolerance window for spot-check scans.
- When normalized, maximum intensity in the output equals 1.0 or 100 (depending on normalization scheme); unnormalized values reflect raw detector counts.
- XIC peak shape is smooth and unimodal or multimodal as expected for the analyte; sharp discontinuities or singleton spikes indicate parsing or filtering errors.

## Limitations

- Accuracy depends on correct specification of xic_tolerance; too-wide tolerance windows will co-extract isobaric or near-isobaric species, inflating intensity.
- MS1-only filtering excludes MS2/MS3 scans; if retention time metadata is absent or inconsistent, tabulation may fail or produce gaps.
- Normalization is applied globally to the entire chromatogram; if baseline drift or instrument noise is significant, normalized intensity may misrepresent true analyte abundance.
- Does not account for detector saturation, ion suppression, or chromatographic tailing; raw tabulated values reflect these artifacts.

## Evidence

- [other] The dashboard accepts resolved mzML/mzXML spectrum files and parameters including xicmz (target m/z value, e.g. 870.954), xic_tolerance (mass tolerance window, e.g. 0.5), and xic_norm (normalization option), then computes the extracted-ion chromatogram by filtering and integrating spectral intensities within the specified mass range across all retention times.: "The dashboard accepts resolved mzML/mzXML spectrum files and parameters including xicmz (target m/z value, e.g. 870.954), xic_tolerance (mass tolerance window, e.g. 0.5), and xic_norm (normalization"
- [other] Load the mzML or mzXML file using a mass spectrometry data parser (e.g., pyteomics or mzmine). Filter all MS1 scans to extract signals within the specified m/z tolerance window (e.g., xicmz ± tolerance in ppm or Th). For each scan, record the retention time and summed intensity across the filtered m/z range. Tabulate retention time and intensity as paired values and export as a two-column data file (retention_time, intensity).: "For each scan, record the retention time and summed intensity across the filtered m/z range. Tabulate retention time and intensity as paired values and export as a two-column data file"
- [other] Filter all MS1 scans to extract signals within the specified m/z tolerance window (e.g., xicmz ± tolerance in ppm or Th).: "Filter all MS1 scans to extract signals within the specified m/z tolerance window (e.g., xicmz ± tolerance in ppm or Th)."
- [readme] To get everything up and running, we've created a make target for you to get docker up and running: make server-compose-interactive. The requirements on your local system are: 1. Docker 2. Docker Compose. This will bring the server up on http://localhost:6548.: "This will bring the server up on http://localhost:6548."
