---
name: ms2-fragment-pattern-recognition
description: Use when you have data-dependent acquisition (DDA) MS2 spectra from HRMS measurements (ESI or APCI ionization) and need to prioritize potential PFAS features from a large pool of detected ions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3860
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - pyOpenMS
  - Python
  - PFΔScreen
  - MSConvert
  techniques:
  - LC-MS
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

# MS2 Fragment Pattern Recognition

## Summary

Identifies and annotates diagnostic fragment patterns in tandem MS (MS2) spectra by computing characteristic mass differences between precursor and fragment ions, enabling prioritization of PFAS features in non-target HRMS workflows. This skill leverages fragment mass losses (e.g., CF₂ losses) and perfluoroalkyl chain signatures to screen and rank potential PFAS compounds.

## When to use

Apply this skill when you have data-dependent acquisition (DDA) MS2 spectra from HRMS measurements (ESI or APCI ionization) and need to prioritize potential PFAS features from a large pool of detected ions. Use it specifically when vendor-independent mzML files with centroided MS2 spectra are available and you seek to combine fragment-level evidence with other prioritization approaches (MD/C-m/C, Kendrick mass defect) to rank candidates by chemical plausibility.

## When NOT to use

- Input spectra are profile (not centroided) mode — profile spectra require deconvolution before reliable mass difference computation.
- MS2 data were acquired in data-independent acquisition (DIA) or MS1-only mode — diagnostic fragment patterns require high-resolution MS2 spectra paired to precursor ions.
- Feature list is already curated or suspect-screened by external software — this skill is most valuable for untargeted discovery and de novo prioritization, not confirmation of known compounds.

## Inputs

- Centroided DDA MS2 spectra in mzML format (vendor-independent)
- Feature detection results (m/z, retention time, precursor ion list)
- Precursor ion m/z values with associated MS2 fragment lists

## Outputs

- Per-feature annotation table with diagnostic fragment assignments
- Diagnostic fragment count and mass difference values per feature
- Prioritization scores or flags based on fragment pattern matches
- Annotated MS2 spectra with highlighted diagnostic fragment mass differences

## How to apply

For each detected feature, extract all associated MS2 fragment m/z values from the DDA spectrum. Compute mass differences between the precursor ion m/z and each fragment m/z to detect characteristic losses (e.g., CF₂ = 50.0 Da, CF₃ or C₂F₅ losses). Match observed mass differences against a library of known PFAS diagnostic fragment patterns, recording both the mass difference values and the fragment count per feature. Annotate each feature with matched diagnostic fragments and report the diagnostic fragment count in a per-feature output table. Features with multiple characteristic PFAS fragment losses and CF₂-chain evidence receive higher priority scores in downstream filtering.

## Related tools

- **pyOpenMS** (Extract centroided MS2 fragment m/z values and precursor-fragment associations from mzML spectra) — https://github.com/OpenMS/OpenMS
- **PFΔScreen** (Integrated platform applying MS2 fragment pattern recognition alongside MD/C-m/C and KMD analysis for PFAS prioritization) — https://github.com/JonZwe/PFAScreen
- **MSConvert** (Convert vendor mass spectrometry raw files to vendor-independent mzML format for input to fragment analysis)

## Evaluation signals

- All precursor–fragment mass differences are computed and reported without missing or NaN values for valid centroided spectra.
- Diagnostic fragment assignments match known PFAS characteristic losses (e.g., CF₂ within ±5 ppm mass tolerance, CF₃ or perfluoroalkyl chain fragments).
- Features with multiple diagnostic fragments (≥2 characteristic mass differences) receive higher priority scores than features with zero or single matches.
- MS2 spectra visualization confirms that highlighted fragment mass differences correspond to actual peaks in the centroided data.
- Diagnostic fragment counts and mass difference annotations are correctly linked to precursor m/z in the output table without row misalignment.

## Limitations

- Fragment mass difference approach is most sensitive for PFAS with characteristic perfluorinated chains; compounds with partial fluorination or non-standard PFAS scaffolds may yield fewer diagnostic matches.
- Centroiding artifacts or low-abundance fragments may be missed if MS2 signal intensity falls below noise threshold; performance depends on instrument resolution and acquisition settings.
- Requires data-dependent acquisition with one collision energy per precursor; variable collision energies or dynamic settings may produce inconsistent fragment patterns across features.
- Mass difference tolerance (e.g., ±5 ppm) must be tuned empirically; overly strict tolerances may cause false negatives; overly permissive tolerances may cause false positives and interfere with non-PFAS fragment matches.

## Evidence

- [other] For each detected feature, extract all associated MS2 fragment m/z values. Search for diagnostic fragment patterns by computing mass differences between precursor and fragment ions.: "For each detected feature, extract all associated MS2 fragment m/z values. Search for diagnostic fragment patterns by computing mass differences between precursor and fragment ions."
- [other] Identify characteristic fragment mass differences indicative of PFAS compounds (e.g., CF2 loss, perfluoroalkyl chain fragments).: "Identify characteristic fragment mass differences indicative of PFAS compounds (e.g., CF2 loss, perfluoroalkyl chain fragments)."
- [other] Annotate each feature with matched diagnostic fragments and mass difference values. Output per-feature hit table with diagnostic fragment assignments and diagnostic fragment counts.: "Annotate each feature with matched diagnostic fragments and mass difference values. Output per-feature hit table with diagnostic fragment assignments and diagnostic fragment counts."
- [intro] PFΔScreen uses several techniques for prioritization such as the MD/C-m/C approach, Kendrick mass defect (KMD) analysis and fragment mass differences and diagnostic fragments in the MS2 data: "PFΔScreen uses several techniques for prioritization such as the MD/C-m/C approach, Kendrick mass defect (KMD) analysis and fragment mass differences and diagnostic fragments in the MS2 data"
- [readme] Raw mass spectrometric data can be included vendor-independently in the mzML format (data-dependent acquisition with centroided spectra, mzML files can be generated via the MSConvert software tool).: "Raw mass spectrometric data can be included vendor-independently in the mzML format (data-dependent acquisition with centroided spectra, mzML files can be generated via the MSConvert software tool)."
- [readme] Afterwards, MS2 spectra displayed by the RawDataVisualization tool (MS2 extractor), have highlighted fragment mass differences and diagnostic fragments, if some were detected.: "Afterwards, MS2 spectra displayed by the RawDataVisualization tool (MS2 extractor), have highlighted fragment mass differences and diagnostic fragments, if some were detected."
