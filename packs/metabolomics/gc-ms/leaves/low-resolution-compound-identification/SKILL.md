---
name: low-resolution-compound-identification
description: Use when you have low-resolution GC-MS data (e.g., ANDI NetCDF format) with detected peaks that lack high mass accuracy, and you need to assign compound identities using a combination of retention index (RI) calibration and mass spectral library matching.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3520
  tools:
  - CoreMS
  - GC_RI_Calibration
  - LowResMassSpectralMatch
  - PNNLMetV20191015.MSL
  techniques:
  - GC-MS
derived_from:
- doi: 10.5281/zenodo.14009575
  title: corems
evidence_spans:
- from corems.transient.input.brukerSolarix import ReadBrukerSolarix
- '**CoreMS** is a comprehensive mass spectrometry framework for software development and data analysis of small molecules analysis.'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_corems_cq
    doi: 10.5281/zenodo.14009575
    title: corems
  dedup_kept_from: coll_corems_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.5281/zenodo.14009575
  all_source_dois:
  - 10.5281/zenodo.14009575
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# low-resolution-compound-identification

## Summary

Identifies chemical compounds in low-resolution GC-MS data by matching retention-index-calibrated peaks against a reference spectral library using spectral similarity algorithms. This skill enables automated compound annotation when only nominal m/z and retention time information are available.

## When to use

Apply this skill when you have low-resolution GC-MS data (e.g., ANDI NetCDF format) with detected peaks that lack high mass accuracy, and you need to assign compound identities using a combination of retention index (RI) calibration and mass spectral library matching. Use it when FAMES standards or equivalent RI calibrants are available to normalize retention times across runs.

## When NOT to use

- Input data are already high-resolution accurate-mass spectra (use molecular formula assignment instead)
- No retention index calibration standards or reference spectra are available
- The compound of interest is absent from the reference spectral library

## Inputs

- ANDI NetCDF GC-MS dataset (.cdf)
- mass spectrum objects with detected peaks
- retention index calibration data (FAMES standards)
- reference mass spectral library (e.g., PNNLMetV20191015.MSL)

## Outputs

- annotated mass spectra with compound identities
- match scores for each peak-to-library assignment
- retention index alignment confidence metrics
- compound identity table (CSV/Excel export)

## How to apply

Load the ANDI NetCDF GC-MS dataset using CoreMS input modules, then compute retention indices for each detected peak using GC_RI_Calibration with FAMES standards as reference. Initialize the LowResMassSpectralMatch algorithm with a reference spectral library (e.g., PNNLMetV20191015.MSL) and execute spectral matching on the RI-calibrated peaks. The algorithm filters and ranks candidate library entries by combining m/z-based mass spectral similarity with retention index alignment confidence. Export the matched results with compound identities, match scores, and RI alignment confidence metrics. Quality is assessed by evaluating match score distributions and the consistency of RI assignments relative to calibration standards.

## Related tools

- **CoreMS** (Framework providing GC-MS input/output modules, peak detection, baseline subtraction, and spectral matching algorithm implementations) — https://github.com/EMSL-Computing/CoreMS
- **GC_RI_Calibration** (CoreMS module that computes retention indices for detected peaks using FAMES standards as calibration reference) — https://github.com/EMSL-Computing/CoreMS
- **LowResMassSpectralMatch** (CoreMS algorithm that performs spectral matching against bundled reference library using m/z similarity and RI-based filtering) — https://github.com/EMSL-Computing/CoreMS
- **PNNLMetV20191015.MSL** (Reference mass spectral library bundled with CoreMS for GC-MS compound identification) — https://github.com/EMSL-Computing/CoreMS

## Examples

```
from corems.transient.input.andi_netcdf import ReadANDINetCDF; from corems.ms_peaks.spectral_match import LowResMassSpectralMatch; ms_data = ReadANDINetCDF('sample.cdf'); ms_data.apply_gc_ri_calibration(); matched_peaks = LowResMassSpectralMatch(ms_data, library='PNNLMetV20191015.MSL').match_peaks()
```

## Evaluation signals

- Match scores are above a defined threshold (typically cosine similarity or entropy similarity > 0.7) for true positives
- Retention index values fall within expected range for known calibration standards (e.g., FAMES alkane series)
- Matched compound identities have consistent RI alignment confidence across replicate analyses
- Mass spectral peak patterns in matched spectrum visually align with library reference for top candidate
- Number of unmatched peaks or low-confidence assignments is consistent with instrument resolution and library coverage

## Limitations

- Accuracy is limited by spectral library completeness; compounds absent from library cannot be identified
- RI calibration depends on availability and quality of FAMES standards or equivalent RI reference materials
- Spectral similarity-based matching may produce false positives when structurally similar compounds yield overlapping fragmentation patterns
- Low mass resolution inherently limits discrimination between isobaric compounds
- Performance degrades when baseline noise is high or when peaks are insufficiently resolved chromatographically

## Evidence

- [other] LowResMassSpectralMatch performs spectral matching against a bundled GCMS spectral library after retention index calibration using FAMES standards, enabling automated compound identification in GC-MS data.: "LowResMassSpectralMatch performs spectral matching against a bundled GCMS spectral library after retention index calibration using FAMES standards, enabling automated compound identification in GC-MS"
- [other] Apply GC_RI_Calibration to compute retention indices for each detected peak.: "Apply GC_RI_Calibration to compute retention indices for each detected peak."
- [other] Initialize LowResMassSpectralMatch spectral matching algorithm with PNNLMetV20191015.MSL spectral library as reference database.: "Initialize LowResMassSpectralMatch spectral matching algorithm with PNNLMetV20191015.MSL spectral library as reference database."
- [other] Execute spectral matching using retention-index-calibrated peaks to filter and rank library candidates.: "Execute spectral matching using retention-index-calibrated peaks to filter and rank library candidates."
- [readme] Retention Index Calibration; Automatic local (SQLite) or external (MongoDB or PostgreSQL) database check, generation, and search; Automatic molecular match algorithm with all spectral similarity methods: "Retention Index Calibration; Automatic molecular match algorithm with all spectral similarity methods"
- [other] Load ANDI NetCDF GC-MS dataset using CoreMS input module for GC-MS format support.: "Load ANDI NetCDF GC-MS dataset using CoreMS input module for GC-MS format support."
