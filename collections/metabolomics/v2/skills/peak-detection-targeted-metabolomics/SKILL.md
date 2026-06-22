---
name: peak-detection-targeted-metabolomics
description: Use when you have mass spectrometry data in .raw, .d, or mzXML format and a predefined list of target compounds (m/z and retention time ranges) you wish to quantify.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3630
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - R GUI
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
---

# peak-detection-targeted-metabolomics

## Summary

Identifies and localizes known metabolite peaks in targeted mass spectrometry data by applying peak detection algorithms tuned for specific m/z and retention time windows. This skill bridges raw MS data import and quantitative annotation, enabling targeted metabolite profiling in SMART's integrated workflow.

## When to use

You have mass spectrometry data in .raw, .d, or mzXML format and a predefined list of target compounds (m/z and retention time ranges) you wish to quantify. Use this skill when you need to detect peaks only for known metabolites rather than discover all features in the dataset, or when you are transitioning from untargeted discovery to focused validation of candidate compounds.

## When NOT to use

- Input is already a processed peak table or feature matrix — use this skill only on raw or minimally preprocessed MS data.
- You aim to discover novel or unexpected metabolites; targeted peak detection will miss features outside predefined m/z and RT windows.
- Data has already undergone peak detection; applying this skill again risks duplicate annotation or unnecessary recalculation.

## Inputs

- Mass spectrometry data files (.raw, .d, mzXML format)
- Target compound list (m/z values, retention time windows, or reference spectra)

## Outputs

- Peak table with columns: peak identifiers, m/z, retention time, intensity
- Annotated targeted peaks linked to known compounds

## How to apply

Load the MS data in a supported format (.raw, .d, mzXML) via SMART's R data import module. Supply the target compound list with expected m/z values and retention time windows. Apply the targeted peak analysis algorithm, which identifies significant peaks within the specified m/z and RT boundaries for each target. The algorithm outputs peak tables populated with peak identifiers, observed m/z, retention time, and intensity values. Validate output by checking that detected peaks align with expected retention time windows and m/z tolerances, and that no peaks are missing for well-represented targets.

## Related tools

- **R** (Core language for implementing and executing targeted peak detection algorithms within SMART) — github.com/YuJenL/SMART
- **R GUI** (User-friendly interface for specifying target compound parameters and launching targeted peak analysis workflows) — github.com/YuJenL/SMART

## Evaluation signals

- Detected peaks fall within expected retention time and m/z tolerance windows for each target compound.
- Peak table contains no null or invalid entries for m/z, retention time, or intensity in rows corresponding to targets.
- Detected peaks align with visual inspection of mass spectra and total ion chromatograms (TIC) at target RT ranges.
- All targeted compounds present in the sample are represented in the output peak table; absence of expected peaks indicates detection failure or data quality issues.
- Intensity values are positive and within the dynamic range of the mass spectrometer; outliers suggest poor peak picking or instrumental noise.

## Limitations

- Requires pre-specification of target m/z and retention time windows; incorrect or overly tight tolerances will cause target peaks to be missed.
- Peak detection performance depends on data quality and signal-to-noise ratio; low-abundance targets may not be reliably detected.
- Targeted analysis cannot identify unexpected metabolites or isotopologues outside the predefined target list.
- No changelog is available for the SMART tool, limiting reproducibility tracking across versions.

## Evidence

- [other] Apply targeted peak analysis for known compound detection in targeted mode.: "Apply targeted peak analysis for known compound detection in targeted mode."
- [intro] Peak Analysis and annotation: Implement peak analysis for both untargeted and targeted data and peak annotation.: "Peak Analysis and annotation: Implement peak analysis for both untargeted and targeted data and peak annotation."
- [other] Load mass spectrometry data in supported formats (.raw, .d, mzXML) using R data import module.: "Load mass spectrometry data in supported formats (.raw, .d, mzXML) using R data import module."
- [other] Compile results into a peak table containing peak identifiers, m/z, retention time, intensity, and assigned annotations.: "Compile results into a peak table containing peak identifiers, m/z, retention time, intensity, and assigned annotations."
- [readme] Data Import: Analyze different data file formats (e.g., .raw, .d, and mzXML).: "Data Import: Analyze different data file formats (e.g., .raw, .d, and mzXML)."
