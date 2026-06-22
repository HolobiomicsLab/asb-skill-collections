---
name: mass-spectral-peak-annotation
description: Use when you have centroided MS2 spectra (in mzML format from data-dependent acquisition) and a list of known or suspect PFAS diagnostic fragment masses, and you need to systematically flag which detected features contain fragments characteristic of PFAS compounds (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3645
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
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
  - build: coll_corems_cq
    doi: 10.5281/zenodo.14009575
    title: corems
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Mass-Spectral Peak Annotation

## Summary

Annotate MS/MS spectral peaks by matching precursor–product mass pairs against diagnostic fragment databases and flagging characteristic mass differences to identify potential PFAS features in non-target HRMS data. This skill assigns chemical identity and structural relevance to detected fragments, enabling prioritization of suspect compounds.

## When to use

You have centroided MS2 spectra (in mzML format from data-dependent acquisition) and a list of known or suspect PFAS diagnostic fragment masses, and you need to systematically flag which detected features contain fragments characteristic of PFAS compounds (e.g., perfluorocarbon chains, sulfamate groups) to reduce false positives in non-target screening workflows.

## When NOT to use

- Input MS2 spectra are profile (non-centroided) — preprocessing via centroiding is required first.
- No reference diagnostic fragment database is available or the target analyte class has no known characteristic fragments.
- Data were acquired in data-independent acquisition (DIA) mode without precursor isolation — fragment-to-precursor linkage may be ambiguous.

## Inputs

- mzML file with centroided MS2 spectra (data-dependent acquisition format)
- Feature list with precursor m/z and retention time
- PFAS diagnostic fragment mass database with mass tolerance thresholds

## Outputs

- Annotated feature table (Excel format) with diagnostic fragment match flags and identities
- Spectrum list with highlighted fragment mass differences and diagnostic fragments in MS2 data
- HTML visualization of annotated MS2 spectra with fragment annotations

## How to apply

Load centroided MS2 spectra from mzML files using pyOpenMS; define or retrieve a reference database of PFAS diagnostic fragment masses and characteristic mass difference thresholds (e.g., CF₂ = 50.0037 Da repeating units). For each MS2 spectrum, extract all product ion m/z values and scan precursor–product mass pairs against the diagnostic fragment database using a mass tolerance window (typically < 5 ppm for HRMS). Flag each feature whose MS2 spectra contain one or more diagnostic fragment matches or characteristic fragment mass differences (e.g., homologous series stepping patterns) within the specified tolerance. Output an annotated feature table or spectrum list with fragment match flags, matched fragment identities, and mass errors to support manual validation and downstream PFAS structural elucidation.

## Related tools

- **pyOpenMS** (Load and parse centroided MS2 spectra from mzML files for fragment extraction and m/z matching) — https://github.com/OpenMS/OpenMS
- **PFΔScreen** (Complete PFAS feature prioritization tool integrating diagnostic fragment annotation alongside MD/C-m/C and KMD analysis) — https://github.com/JonZwe/PFAScreen
- **MSConvert** (Convert vendor mass spectrometry data formats to vendor-independent mzML with centroided spectra)

## Evaluation signals

- All flagged features have at least one product ion m/z within specified mass tolerance of a known diagnostic fragment mass from the reference database.
- Fragment mass errors (observed m/z minus reference m/z) are consistently < 5 ppm for HRMS-quality data; outliers indicate calibration drift or incorrect database entries.
- Homologous series stepping patterns (e.g., recurring CF₂ mass differences of ~50.0037 Da) are correctly identified and linked across flagged features.
- Manual inspection of highlighted MS2 spectra confirms that flagged fragments correspond to visible peaks in the raw spectrum (not noise or artifacts).
- Output annotation table is consistent with input feature table row count and matches precursor m/z values without loss or duplication.

## Limitations

- Diagnostic fragment annotation relies on the completeness and accuracy of the reference database; unknown or emerging PFAS with novel structural motifs will not be detected.
- Mass tolerance window selection is user-specified; too narrow a window may miss true fragments due to calibration drift, while too wide a window increases false positives.
- Centroided spectra may lose intensity information and complicate detection of low-abundance diagnostic fragments; high noise levels can obscure weak characteristic peaks.
- Fragment-to-precursor assignment assumes data-dependent acquisition (ddMS2); in DIA or broad precursor isolation experiments, fragments cannot be confidently linked to a single precursor.
- Isobaric or isomeric PFAS compounds with overlapping diagnostic fragments cannot be distinguished by mass alone; orthogonal evidence (e.g., retention time, MS3 fragmentation) is required.

## Evidence

- [other] For each MS2 spectrum, scan precursor–product mass pairs against the diagnostic fragment database using mass tolerance matching.: "For each MS2 spectrum, scan precursor–product mass pairs against the diagnostic fragment database using mass tolerance matching."
- [other] Flag features whose MS2 spectra contain one or more diagnostic fragment matches or mass differences within tolerance.: "Flag features whose MS2 spectra contain one or more diagnostic fragment matches or mass differences within tolerance."
- [other] PFΔScreen uses diagnostic fragments and fragment mass differences detected in MS2 data as one of several prioritization techniques to identify potential PFAS features: "PFΔScreen uses diagnostic fragments and fragment mass differences detected in MS2 data as one of several prioritization techniques to identify potential PFAS features"
- [readme] pyOpenMS (Python interface to the C++ OpenMS library) is used for feature detection in MS raw data: "pyOpenMS (Python interface to the C++ OpenMS library) is used for feature detection in MS raw data"
- [readme] MS2 spectra displayed by the RawDataVisualization tool (MS2 extractor), have highlighted fragment mass differences and diagnostic fragments, if some were detected.: "MS2 spectra displayed by the RawDataVisualization tool (MS2 extractor), have highlighted fragment mass differences and diagnostic fragments, if some were detected."
- [readme] Sample and blank for raw data input in PFΔScreen should have been measured under data-dependent acquisition (ddMS2) with centroided spectra: "Sample and blank for raw data input in PFΔScreen should have been measured under data-dependent acquisition (ddMS2) with centroided spectra"
