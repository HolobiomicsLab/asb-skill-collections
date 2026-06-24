---
name: ms2-diagnostic-fragment-matching
description: Use when you have centroided MS2 spectra from data-dependent LC- or GC-HRMS
  measurements and need to rapidly prioritize potential PFAS features within a larger
  feature set.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3647
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - pyOpenMS
  - Python
  - MSConvert
  - PFΔScreen
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1007/s00216-023-05070-2
  title: pfdeltascreen
evidence_spans:
- pyOpenMS (Python interface to the C++ OpenMS library) is used for feature detection
  in MS raw data
- PFΔScreen is an open-source Python based non-target screening software tool
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pfdeltascreen
    doi: 10.1007/s00216-023-05070-2
    title: pfdeltascreen
  dedup_kept_from: coll_pfdeltascreen
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1007/s00216-023-05070-2
  all_source_dois:
  - 10.1007/s00216-023-05070-2
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# MS2 Diagnostic Fragment Matching

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

A mass spectrometry screening technique that identifies potential PFAS features by matching precursor–product ion pairs in MS2 spectra against a database of known PFAS diagnostic fragments and characteristic mass differences. This prioritization method flags features whose fragmentation patterns contain diagnostic signatures indicative of PFAS structure.

## When to use

Apply this skill when you have centroided MS2 spectra from data-dependent LC- or GC-HRMS measurements and need to rapidly prioritize potential PFAS features within a larger feature set. Use it when you have or can define a reference database of PFAS diagnostic fragment masses and expect PFAS to generate characteristic neutral losses or fragment mass differences (e.g., CF₂ units, perfluoroalkyl chain fragments). This is especially valuable in non-target screening where thousands of features are detected but only a subset are true PFAS.

## When NOT to use

- Input is profile (non-centroided) MS2 spectra; MS2 matching requires centroided peaks for accurate m/z matching.
- No MS2 data or only MS1 spectra are available; diagnostic fragment matching requires tandem MS fragmentation information.
- The compound class of interest is not known to generate diagnostic fragments or characteristic mass differences (e.g., weakly fragmented or novel PFAS with unknown fragmentation behavior).

## Inputs

- Centroided MS2 spectra in mzML format (data-dependent acquisition, vendor-independent)
- Feature table with m/z and retention time (from pyOpenMS or user-supplied CSV/TSV with columns: m/z, retention time, intensity)
- Reference database of PFAS diagnostic fragment masses and/or characteristic mass differences (e.g., CF₂ = 48.0 Da, C₂F₅ = 119.0 Da)

## Outputs

- Annotated feature table (Excel format) with diagnostic fragment match flags and fragment identities for each feature
- Spectrum list or HTML visualization with highlighted diagnostic fragments and fragment mass differences detected in MS2 spectra
- Prioritized feature ranking incorporating diagnostic fragment matches alongside MD/C-m/C and KMD scores

## How to apply

Load centroided MS2 spectra from an mzML file using pyOpenMS and retrieve or define a database of known PFAS diagnostic fragment masses and characteristic mass difference thresholds (e.g., common losses or repeating units). For each detected or user-supplied feature, extract its MS2 spectrum and scan all precursor–product ion pairs (neutral losses) against the diagnostic fragment database using a defined mass tolerance (typically in ppm). Flag features whose MS2 spectra contain one or more diagnostic fragment matches or mass differences that fall within the tolerance window. Integrate these flags into a prioritization score alongside other PFAS indicators (MD/C-m/C ratio, Kendrick mass defect) to produce a ranked feature table. The rationale is that PFAS compounds exhibit characteristic fragmentation patterns due to their perfluorinated backbone, and matching these patterns dramatically increases confidence in feature identity.

## Related tools

- **pyOpenMS** (Load and parse centroided MS2 spectra from mzML files; extract precursor–product ion pairs for mass matching) — https://pyopenms.readthedocs.io
- **MSConvert** (Convert vendor-specific raw mass spectrometry data to vendor-independent mzML format with centroided spectra)
- **PFΔScreen** (End-to-end tool that implements MS2 diagnostic fragment matching as one of three prioritization techniques (alongside MD/C-m/C and KMD analysis) within an integrated GUI workflow) — https://github.com/JonZwe/PFAScreen

## Evaluation signals

- Diagnostic fragments and mass differences are correctly identified in MS2 spectra for known PFAS standards (e.g., PFOA, PFOS); compare flagged features against reference compounds.
- Fragment mass differences fall within the specified tolerance window (e.g., ±5 ppm for high-resolution MS); verify tolerance settings match instrument resolution.
- Features flagged as containing diagnostic fragments show coelution and consistent isotope patterns across replicates; check rank correlation with complementary metrics (MD/C-m/C ratio, KMD clustering).
- MS2 visualization highlights match all identified diagnostic fragments; inspect HTML output to confirm visual alignment of fragment peaks with database entries.
- False positive rate is reduced when diagnostic fragment matches are combined with other prioritization filters; compare single-metric vs. multi-metric prioritization precision.

## Limitations

- Matching accuracy depends critically on the completeness and accuracy of the diagnostic fragment database; fragmentation patterns not in the database will be missed, limiting discovery of novel PFAS structures.
- Fragment mass differences require careful definition of mass tolerance; overly loose tolerance increases false positives, while overly tight tolerance misses true matches in lower-resolution or noisy spectra.
- MS2 fragmentation behavior varies with collision energy, ionization mode (ESI, APCI), and instrument type; diagnostic fragments optimized for one condition may not appear in data acquired under different conditions (e.g., single collision energy per precursor assumed in PFΔScreen workflow).
- Features with weak or absent MS2 fragmentation (e.g., low intensity, poor dissociation) cannot be scored by this method; such features require alternative prioritization strategies.
- The method assumes data-dependent acquisition (ddMS2) with centroided spectra; other acquisition modes (e.g., data-independent acquisition, profile data) are not supported.

## Evidence

- [other] PFΔScreen uses diagnostic fragments and fragment mass differences detected in MS2 data as one of several prioritization techniques to identify potential PFAS features: "PFΔScreen uses diagnostic fragments and fragment mass differences detected in MS2 data as one of several prioritization techniques to identify potential PFAS features alongside the MD/C-m/C approach"
- [other] For each MS2 spectrum, scan precursor–product mass pairs against a diagnostic fragment database: "For each MS2 spectrum, scan precursor–product mass pairs against the diagnostic fragment database using mass tolerance matching."
- [intro] pyOpenMS is used for feature detection in MS raw data: "pyOpenMS (Python interface to the C++ OpenMS library) is used for feature detection in MS raw data"
- [intro] PFΔScreen uses several techniques for prioritization including fragment mass differences and diagnostic fragments in MS2 data: "PFΔScreen uses several techniques for prioritization such as the MD/C-m/C approach, Kendrick mass defect (KMD) analysis and fragment mass differences and diagnostic fragments in the MS2 data"
- [readme] Raw mass spectrometric data must be in mzML format with centroided spectra: "Raw mass spectrometric data can be included vendor-independently in the mzML format (data-dependent acquisition with centroided spectra, mzML files can be generated via the MSConvert software tool)."
- [readme] MS2 spectra are highlighted with fragment mass differences and diagnostic fragments after prioritization: "Afterwards, MS2 spectra displayed by the RawDataVisualization tool (MS2 extractor), have highlighted fragment mass differences and diagnostic fragments, if some were detected."
