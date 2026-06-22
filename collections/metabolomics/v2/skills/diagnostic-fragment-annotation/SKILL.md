---
name: diagnostic-fragment-annotation
description: Use when when you have centroided, data-dependent acquisition (ddMS2) spectra in mzML format with extracted precursor m/z values and associated fragment ion lists, and you need to discriminate PFAS features from background signals using characteristic fragmentation patterns.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3663
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - pyOpenMS
  - Python
  - PFΔScreen
  - MSConvert
derived_from:
- doi: 10.1007/s00216-023-05070-2
  title: pfdeltascreen
evidence_spans:
- pyOpenMS (Python interface to the C++ OpenMS library) is used for feature detection in MS raw data
- PFΔScreen is an open-source Python based non-target screening software tool
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pfdeltascreen_cq
    doi: 10.1007/s00216-023-05070-2
    title: pfdeltascreen
  dedup_kept_from: coll_pfdeltascreen_cq
schema_version: 0.2.0
---

# diagnostic-fragment-annotation

## Summary

Annotate MS2 fragment ions with diagnostic mass differences and characteristic loss patterns to prioritize putative PFAS features in non-target HRMS data. This skill identifies perfluoroalkyl chain fragments and neutral losses (e.g., CF₂ units) by computing precursor–fragment mass differences, enabling rapid triage of candidate compounds in large feature sets.

## When to use

When you have centroided, data-dependent acquisition (ddMS2) spectra in mzML format with extracted precursor m/z values and associated fragment ion lists, and you need to discriminate PFAS features from background signals using characteristic fragmentation patterns. Apply this when feature finding has already been completed and you seek to enrich prioritization beyond mass defect analysis alone.

## When NOT to use

- Input spectra are not centroided or lack MS2 data (MS1-only or uncentroided data cannot be reliably matched to reference loss patterns).
- Feature finding has not been performed and you only have raw, unprocessed mzML files without precursor m/z assignments.
- You are working with non-PFAS analytes or compounds without known characteristic fragmentation losses (this skill is PFAS-specific and relies on the CF₂ and perfluoroalkyl chemistry).

## Inputs

- centroided MS2 spectra in mzML format (data-dependent acquisition)
- precursor m/z values and associated fragment ion m/z arrays
- mass tolerance threshold (ppm)
- PFAS diagnostic fragment/loss pattern reference library

## Outputs

- per-feature diagnostic fragment hit table (feature ID, matched fragment m/z, mass difference, loss type, match count)
- annotated feature list with diagnostic fragment scores
- MS2 spectra visualization with highlighted diagnostic fragments and mass differences

## How to apply

For each detected feature: (1) Extract all MS2 fragment m/z values associated with the precursor ion using pyOpenMS or equivalent mzML parser. (2) Compute mass differences between the precursor m/z and each fragment m/z. (3) Search the observed mass difference set against a catalog of diagnostic PFAS losses (e.g., CF₂ = 50.0078 Da, perfluoroalkyl chain fragments). (4) Match fragments within a mass tolerance window (typically 5–10 ppm) to account for instrumental resolution and calibration drift. (5) Count and annotate matched diagnostic fragments per feature, recording both the mass difference values and matched loss types. (6) Assign a diagnostic fragment score (e.g., count or presence/absence flag) to each feature for downstream prioritization ranking. Features with multiple diagnostic matches are scored higher.

## Related tools

- **pyOpenMS** (Parse centroided MS2 spectra from mzML files and extract precursor–fragment m/z pairs) — https://github.com/OpenMS/OpenMS
- **PFΔScreen** (Integrated PFAS prioritization framework that applies diagnostic fragment annotation alongside MD/C-m/C and KMD analysis in a graphical workflow) — https://github.com/JonZwe/PFAScreen
- **MSConvert** (Convert vendor-proprietary MS raw files to mzML format before diagnostic fragment annotation) — https://proteowizard.sourceforge.io/

## Evaluation signals

- Diagnostic fragment matches fall within the specified mass tolerance window (e.g., ±5 ppm of expected CF₂ or chain-fragment mass difference).
- Each feature in the output table has a non-null diagnostic fragment count and at least one matched loss type (CF₂, perfluoroalkyl chain, etc.) if MS2 data are present.
- Annotated MS2 spectra show highlighted fragment ions and mass difference values that correspond to known PFAS fragmentation patterns (visual inspection in PFΔScreen RawDataVisualization tool).
- Features with high diagnostic fragment match counts rank higher in prioritization output compared to features with zero matches, demonstrating discrimination between PFAS and background.
- Mass difference annotations are reproducible across replicate runs and consistent with literature or in-house PFAS fragmentation reference libraries.

## Limitations

- Diagnostic fragment matching relies on accurate mass calibration (typical <5 ppm error) and precise precursor m/z assignment; poor calibration leads to false negatives or false positives.
- The skill requires centroided (not profile) MS2 spectra; uncentroided data will result in fragmented or unmatched mass difference patterns.
- Detection sensitivity depends on MS instrument resolution and fragment ion abundance; weak or co-eluting fragments may be lost or misassigned.
- Diagnostic fragment patterns are PFAS-specific (CF₂-based); the approach does not generalize to non-fluorinated compounds or PFAS analogs with atypical fragmentation.
- Custom reference libraries of diagnostic losses must be curated and validated; incorrect or incomplete loss catalogs reduce specificity and recall.

## Evidence

- [other] For each detected feature, extract all associated MS2 fragment m/z values. Search for diagnostic fragment patterns by computing mass differences between precursor and fragment ions. Identify characteristic fragment mass differences indicative of PFAS compounds (e.g., CF2 loss, perfluoroalkyl chain fragments).: "For each detected feature, extract all associated MS2 fragment m/z values. 3. Search for diagnostic fragment patterns by computing mass differences between precursor and fragment ions. 4. Identify"
- [other] PFΔScreen uses fragment mass differences and diagnostic fragments detected in MS2 data as one of several prioritization techniques alongside the MD/C-m/C approach and Kendrick mass defect analysis to screen potential PFAS features.: "PFΔScreen uses fragment mass differences and diagnostic fragments detected in MS2 data as one of several prioritization techniques alongside the MD/C-m/C approach and Kendrick mass defect analysis"
- [other] Annotate each feature with matched diagnostic fragments and mass difference values. Output per-feature hit table with diagnostic fragment assignments and diagnostic fragment counts.: "Annotate each feature with matched diagnostic fragments and mass difference values. 6. Output per-feature hit table with diagnostic fragment assignments and diagnostic fragment counts."
- [readme] Raw mass spectrometric data can be included vendor-independently in the mzML format (data-dependent acquisition with centroided spectra, mzML files can be generated via the MSConvert software tool).: "Raw mass spectrometric data can be included vendor-independently in the mzML format (data-dependent acquisition with centroided spectra"
- [readme] Afterwards, MS2 spectra displayed by the RawDataVisualization tool (MS2 extractor), have highlighted fragment mass differences and diagnostic fragments, if some were detected.: "MS2 spectra displayed by the RawDataVisualization tool (MS2 extractor), have highlighted fragment mass differences and diagnostic fragments, if some were detected."
