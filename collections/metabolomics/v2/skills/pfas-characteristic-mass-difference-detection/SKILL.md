---
name: pfas-characteristic-mass-difference-detection
description: Use when you have centroided MS2 spectra (ddMS2 data in mzML format)
  from HRMS analysis and need to identify potential PFAS compounds among thousands
  of features.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  tools:
  - pyOpenMS
  - Python
  - OpenMS
  - MSConvert
  - PFΔScreen
  techniques:
  - LC-MS
  - NMR
  license_tier: open
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

# PFAS characteristic mass difference detection

## Summary

Identifies potential PFAS features in LC/GC-HRMS data by detecting diagnostic fragment mass differences in MS2 spectra that are characteristic of PFAS structures (e.g., CF₂ repeating units). This technique prioritizes candidate features alongside Kendrick mass defect and MD/C-m/C analysis for non-target PFAS screening.

## When to use

Apply this skill when you have centroided MS2 spectra (ddMS2 data in mzML format) from HRMS analysis and need to identify potential PFAS compounds among thousands of features. Use it when you want to leverage PFAS-specific fragmentation patterns—particularly loss of CF₂ units (mass difference ~50 Da) or other diagnostic fragment pairs—to reduce false positives and enrich for known PFAS structural motifs before suspect or confirmatory analysis.

## When NOT to use

- Input spectra are profile (non-centroided) data—centroiding is required for reliable peak matching.
- MS2 data are unavailable or not aligned to the feature table—diagnostic fragment detection requires explicit precursor–product mass pairs.
- Analysis target includes non-PFAS compounds or compound classes with very different fragmentation patterns; the skill is PFAS-specific and will not identify structurally unrelated compounds.

## Inputs

- Centroided MS2 spectra in mzML format (data-dependent acquisition / ddMS2)
- Feature table with precursor m/z values and retention times
- Diagnostic fragment mass database (known PFAS fragments and mass differences)
- Mass tolerance threshold (in ppm or Da) for fragment matching

## Outputs

- Annotated feature table (Excel format) with diagnostic fragment flags
- Spectrum list with highlighted diagnostic fragment matches and mass differences
- Interactive HTML visualizations showing flagged features in m/z vs. retention time space

## How to apply

Load centroided MS2 spectra from mzML files using pyOpenMS and extract precursor–product mass pairs. Define a diagnostic fragment database containing known PFAS-characteristic fragment masses and mass differences (e.g., CF₂ losses, perfluorocarbon backbone fragments) along with a mass tolerance threshold appropriate to your instrument resolution. Systematically scan each MS2 spectrum's fragments against the diagnostic database using mass tolerance matching. Flag features whose spectra contain one or more diagnostic fragment matches or characteristic mass differences within the specified tolerance. Output an annotated feature table with flags indicating which diagnostic fragments or mass differences were detected, enabling prioritization and filtering of the full feature list for downstream manual review or suspect screening.

## Related tools

- **pyOpenMS** (Parse centroided MS2 spectra from mzML and extract precursor–product mass pairs for diagnostic fragment matching)
- **OpenMS** (Underlying C++ library providing MSData and spectrum access functionality via Python interface)
- **MSConvert** (Convert vendor-specific raw mass spectrometry data to vendor-independent mzML format with centroiding)
- **PFΔScreen** (Integrated tool that implements diagnostic fragment detection alongside MD/C-m/C and KMD analysis for end-to-end PFAS prioritization) — https://github.com/JonZwe/PFAScreen

## Evaluation signals

- Flagged features should contain MS2 fragments matching known PFAS diagnostic masses (e.g., CF₂ losses) or characteristic mass differences within the specified tolerance; verify by manual inspection of representative MS2 spectra.
- Diagnostic fragment matches should be consistently detected across replicate analyses of the same sample under identical parameters, indicating reproducibility of the detection algorithm.
- Features with no MS2 data or MS2 spectra lacking any diagnostic fragments should be unflagged; check that the filtering logic correctly handles edge cases.
- Annotated output table should include fragment identity labels (e.g., 'CF₂ loss', 'perfluorocarbon backbone fragment') and match mass errors; verify these align with the diagnostic database and tolerance used.
- After PFASPrioritization, interactive HTML plots should visually highlight flagged features in m/z vs. retention time space, enabling rapid visual validation of clustering and enrichment patterns.

## Limitations

- Diagnostic fragment detection relies on availability of accurate, curated PFAS fragment databases; incomplete or incorrect fragment definitions will reduce sensitivity or increase false positives.
- Mass tolerance thresholds must be calibrated to instrument resolution (typically ≤5 ppm for Orbitrap/Q-TOF); overly loose tolerance increases false positives; overly tight tolerance reduces sensitivity.
- Low-abundance fragments in MS2 spectra may be missed if signal is below instrumental noise thresholds or if MS/MS acquisition conditions (collision energy, isolation width) are suboptimal.
- Diagnostic fragment approach is blind to structural isomers or homologs that share identical fragments but differ in connectivity; confirmation requires complementary techniques (e.g., NMR, LC-MS/MS with authentic standards).
- The method was developed and validated on ESI and APCI ionization data for LC- and GC-HRMS; applicability to other ionization sources or instrumental platforms is not explicitly demonstrated.

## Evidence

- [other] For each MS2 spectrum, scan precursor–product mass pairs against the diagnostic fragment database using mass tolerance matching.: "For each MS2 spectrum, scan precursor–product mass pairs against the diagnostic fragment database using mass tolerance matching."
- [intro] PFΔScreen uses several techniques for prioritization such as the MD/C-m/C approach, Kendrick mass defect (KMD) analysis and fragment mass differences and diagnostic fragments in the MS2 data: "PFΔScreen uses several techniques for prioritization such as the MD/C-m/C approach, Kendrick mass defect (KMD) analysis and fragment mass differences and diagnostic fragments in the MS2 data"
- [readme] Sample and blank for raw data input in PFΔScreen should have been measured under data-dependent acquisition (ddMS2) with centroided spectra: "Sample and blank for raw data input in PFΔScreen should have been measured under data-dependent acquisition (ddMS2) with centroided spectra"
- [readme] Afterwards, MS2 spectra displayed by the RawDataVisualization tool (MS2 extractor), have highlighted fragment mass differences and diagnostic fragments, if some were detected.: "Afterwards, MS2 spectra displayed by the RawDataVisualization tool (MS2 extractor), have highlighted fragment mass differences and diagnostic fragments, if some were detected."
- [readme] Raw mass spectrometric data can be included vendor-independently in the mzML format (data-dependent acquisition with centroided spectra, mzML files can be generated via the MSConvert software tool).: "Raw mass spectrometric data can be included vendor-independently in the mzML format (data-dependent acquisition with centroided spectra, mzML files can be generated via the MSConvert software tool)."
