---
name: precursor-product-mass-pairing
description: Use when you have centroided MS2 spectra from data-dependent acquisition (ddMS2) in mzML format and seek to prioritize potential PFAS features by detecting diagnostic fragment masses.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0153
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
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pfdeltascreen
    doi: 10.1007/s00216-023-05070-2
    title: pfdeltascreen
  dedup_kept_from: coll_pfdeltascreen
schema_version: 0.2.0
---

# precursor-product-mass-pairing

## Summary

Match precursor–product ion mass pairs from MS2 spectra against a database of known PFAS diagnostic fragments to flag potential PFAS features in non-target HRMS screening. This skill identifies characteristic fragmentation patterns that distinguish PFAS from background features.

## When to use

Apply this skill when you have centroided MS2 spectra from data-dependent acquisition (ddMS2) in mzML format and seek to prioritize potential PFAS features by detecting diagnostic fragment masses. Use it after feature detection if MS2 data is available and you want to leverage known PFAS fragmentation patterns as a prioritization signal alongside molecular formula and Kendrick mass defect approaches.

## When NOT to use

- Input is profile (centroided=false) MS2 data; the skill requires centroided spectra for reliable m/z matching.
- No MS2 data available; diagnostic fragment matching requires product ion spectra (MS/MS required).
- You are screening for non-PFAS organic contaminants where diagnostic fragment patterns are not defined; this skill is specific to PFAS fragmentation knowledge.

## Inputs

- centroided MS2 spectra in mzML format (data-dependent acquisition, ddMS2)
- detected feature list with precursor m/z and retention time
- diagnostic fragment mass database (known PFAS fragments and mass differences)
- mass tolerance threshold (ppm)

## Outputs

- annotated feature table (Excel or CSV) with diagnostic fragment match flags
- spectrum list with highlighted diagnostic fragments in MS2 spectra
- diagnostic match metadata (fragment identity, mass accuracy, intensity)

## How to apply

Load centroided MS2 spectra from mzML files using pyOpenMS and define or retrieve known PFAS diagnostic fragment masses and characteristic mass difference thresholds specific to your chemical classes of interest. For each detected feature, extract its precursor m/z and scan the corresponding MS2 spectrum's product ion masses against the diagnostic fragment database using a mass tolerance window (typically 5–10 ppm, depending on instrument resolution). Flag any feature whose MS2 spectrum contains one or more diagnostic fragment matches or characteristic mass differences (e.g., CF₂ loss, perfluoroalkyl chain losses) within the specified tolerance. Output an annotated feature table or spectrum list with diagnostic match flags, fragment identities, and match quality metrics to enable downstream manual or automated triage.

## Related tools

- **pyOpenMS** (Load centroided MS2 spectra from mzML files and extract precursor–product mass pairs for diagnostic matching) — https://openms.de
- **PFΔScreen** (End-to-end non-target PFAS screening tool that implements this skill as part of multi-technique prioritization (MD/C-m/C, KMD, and diagnostic fragments)) — https://github.com/JonZwe/PFAScreen
- **MSConvert** (Convert vendor-specific MS raw data formats to mzML for vendor-independent input to precursor-product pairing workflows)

## Evaluation signals

- Precursor m/z and product m/z are successfully paired from the same MS2 spectrum and mass tolerance window is reported (e.g., ±5 ppm).
- Diagnostic fragment matches have documented fragment identities (e.g., [M-CF₂]⁻, perfluoroalkyl chain loss) and mass accuracy within tolerance; matches with mass accuracy >50% of tolerance are rare or absent.
- Feature flagging is consistent across replicate injections (same feature in blank and sample should show diagnostic matches in sample but not blank, if blank correction is applied).
- Output annotation includes both positive diagnostic matches and features with no diagnostic match, preserving negative results for transparency.
- Runtime scales linearly with spectrum count (e.g., <1 minute for 4000 spectra per sample as reported); extreme runtime suggests mass tolerance is too permissive or database is malformed.

## Limitations

- Skill depends on the completeness and accuracy of the diagnostic fragment database; unknown PFAS or poorly characterized homologs may not be detected.
- Mass tolerance must be calibrated to instrument resolution and calibration quality; miscalibration or very low-resolution MS2 will produce false matches or false negatives.
- Diagnostic fragments may be weak or absent in low-energy MS2 spectra; collision energy optimization per precursor is recommended (ideally one collision energy per precursor for consistency).
- Blank correction prior to diagnostic matching is highly recommended to avoid flagging background contaminants; the skill itself does not perform blank subtraction.
- Fragment mass differences alone cannot confirm identity; false positives require manual spectral review or orthogonal evidence (e.g., accurate mass fit to molecular formula, coelution with standards).

## Evidence

- [other] For each MS2 spectrum, scan precursor–product mass pairs against the diagnostic fragment database using mass tolerance matching.: "For each MS2 spectrum, scan precursor–product mass pairs against the diagnostic fragment database using mass tolerance matching."
- [other] PFΔScreen uses diagnostic fragments and fragment mass differences detected in MS2 data as one of several prioritization techniques to identify potential PFAS features: "PFΔScreen uses diagnostic fragments and fragment mass differences detected in MS2 data as one of several prioritization techniques to identify potential PFAS features"
- [intro] pyOpenMS (Python interface to the C++ OpenMS library) is used for feature detection in MS raw data: "pyOpenMS (Python interface to the C++ OpenMS library) is used for feature detection in MS raw data"
- [readme] Sample and blank for raw data input in PFΔScreen should have been measured under data-dependent acquisition (ddMS2) with centroided spectra: "Sample and blank for raw data input in PFΔScreen should have been measured under data-dependent acquisition (ddMS2) with centroided spectra"
- [readme] Afterwards, MS2 spectra displayed by the RawDataVisualization tool (MS2 extractor), have highlighted fragment mass differences and diagnostic fragments, if some were detected.: "MS2 spectra displayed by the RawDataVisualization tool have highlighted fragment mass differences and diagnostic fragments, if some were detected."
- [readme] the overall rather short runtime (e.g., less than one minute in case of 4000 spectra per sample for the whole workflow): "the overall rather short runtime (e.g., less than one minute in case of 4000 spectra per sample for the whole workflow)"
