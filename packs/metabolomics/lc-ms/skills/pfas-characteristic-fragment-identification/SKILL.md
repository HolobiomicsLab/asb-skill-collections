---
name: pfas-characteristic-fragment-identification
description: Use when you have centroided data-dependent acquisition (ddMS2) mzML spectra from LC- or GC-HRMS and need to prioritize putative PFAS features.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3647
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# PFAS Characteristic Fragment Identification

## Summary

Identify and prioritize PFAS features in non-target HRMS data by analyzing characteristic fragment mass differences and diagnostic fragments in MS2 spectra. This skill isolates fragments indicative of perfluoroalkyl structures (e.g., CF₂ loss, perfluoroalkyl chain fragments) to distinguish PFAS from confounding compounds.

## When to use

Apply this skill when you have centroided data-dependent acquisition (ddMS2) mzML spectra from LC- or GC-HRMS and need to prioritize putative PFAS features. Use it after feature detection when you have a pool of candidate m/z–retention time pairs and wish to leverage MS2 fragment patterns to enrich the hit list for manual validation or prioritize annotation effort.

## When NOT to use

- Input spectra are profile (non-centroided) or lack MS2 data (MS1-only measurements).
- Data were acquired in data-independent acquisition (DIA) or scanning mode rather than data-dependent acquisition (ddMS2).
- Feature list is already manually validated or annotated with confirmed PFAS identities; use this skill during exploratory prioritization, not post-confirmation.

## Inputs

- Centroided data-dependent acquisition (ddMS2) mzML files from LC- or GC-HRMS (ESI or APCI ionization)
- Feature list (m/z, retention time, and precursor intensity) from pyOpenMS feature detection or external peak-picking software
- Reference set of characteristic PFAS fragment mass differences (e.g., CF₂ unit = 49.9922 Da)

## Outputs

- Per-feature hit table with diagnostic fragment assignments (fragment m/z values matched to each precursor)
- Diagnostic fragment count and mass difference annotation per feature
- Prioritized feature ranking incorporating diagnostic fragment counts alongside MD/C-m/C and Kendrick mass defect scores
- Highlighted MS2 spectra in RawDataVisualization output showing matched fragment mass differences

## How to apply

For each detected feature, extract all associated MS2 fragment m/z values using pyOpenMS. Compute mass differences between the precursor ion and each fragment. Search this list for characteristic PFAS mass differences (e.g., sequential CF₂ losses of 49.9922 Da, perfluoroalkyl chain fragments). Annotate each feature with the count and identities of matched diagnostic fragments. Features with multiple characteristic fragments are scored higher and ranked accordingly. The rationale is that genuine PFAS compounds produce consistent, repeatable fragment patterns; random noise or background ions do not.

## Related tools

- **pyOpenMS** (Extract MS2 fragment m/z values and compute mass differences from centroided spectra) — https://github.com/OpenMS/OpenMS
- **PFΔScreen** (Integrated software implementing diagnostic fragment detection alongside MD/C-m/C and KMD analysis for PFAS prioritization) — https://github.com/JonZwe/PFAScreen
- **MSConvert** (Convert vendor-specific raw mass spectrometry files to mzML format compatible with PFΔScreen)

## Evaluation signals

- Each feature in the output table has a non-null diagnostic fragment count; features with ≥2 diagnostic fragments are retained and ranked higher than those with 0–1.
- Mass differences between precursor and fragment ions match expected PFAS fragmentations (CF₂ = 49.9922 Da ± mass tolerance, typically 5–10 ppm) when inspected against reference libraries.
- Diagnostic fragment annotations are consistent across replicate measurements (same precursor m/z produces the same diagnostic fragments in multiple spectra).
- Features prioritized by diagnostic fragment counts show better manual validation rates and literature-concordant PFAS identifications compared to unprioritized or non-PFAS features.
- Runtime for fragment analysis scales linearly with total MS2 spectrum count (e.g., <1 min for 4000 spectra per sample).

## Limitations

- Diagnostic fragment detection depends on precursor ion fragmentation in MS2; very stable PFAS or low-intensity precursors may produce few or no diagnostic fragments, reducing sensitivity.
- Mass tolerance (ppm) and reference fragment mass library must be appropriately calibrated; miscalibration leads to false negatives (missed fragments) or false positives (spurious matches).
- MS2 spectra from data-dependent acquisition are biased toward high-intensity features; low-abundance PFAS may not trigger MS2 acquisition and thus lack diagnostic fragment data.
- Fragment annotation alone is not definitive identification; diagnostic fragments must be combined with other evidence (MD/C-m/C ratios, Kendrick mass defect, isotope patterns) for confident PFAS annotation.

## Evidence

- [other] For each detected feature, extract all associated MS2 fragment m/z values. Search for diagnostic fragment patterns by computing mass differences between precursor and fragment ions. Identify characteristic fragment mass differences indicative of PFAS compounds (e.g., CF2 loss, perfluoroalkyl chain fragments).: "For each detected feature, extract all associated MS2 fragment m/z values. Search for diagnostic fragment patterns by computing mass differences between precursor and fragment ions. Identify"
- [intro] PFΔScreen uses several techniques for prioritization such as the MD/C-m/C approach, Kendrick mass defect (KMD) analysis and fragment mass differences and diagnostic fragments in the MS2 data: "PFΔScreen uses several techniques for prioritization such as the MD/C-m/C approach, Kendrick mass defect (KMD) analysis and fragment mass differences and diagnostic fragments in the MS2 data"
- [readme] Raw mass spectrometric data can be included vendor-independently in the mzML format (data-dependent acquisition with centroided spectra, mzML files can be generated via the MSConvert software tool).: "Raw mass spectrometric data can be included vendor-independently in the mzML format (data-dependent acquisition with centroided spectra"
- [readme] Sample and blank for raw data input in PFΔScreen should have been measured under data-dependent acquisition (ddMS2) with centroided spectra, ideally with one collision energy per precursor.: "Sample and blank for raw data input in PFΔScreen should have been measured under data-dependent acquisition (ddMS2) with centroided spectra"
- [readme] After executing the PFASPrioritization tab, the PFΔScreen results table (Excel format) and several interactive HTML plots are saved in a folder named after the sample that can be easily inspected, including a MD/C-m/C plot, a m/z vs. RT plot (with and without MS2 raw data), a KMD vs. m/z with linked m/z vs. RT plot (to verify systematic RT-shifts), and a m/C histogram. Afterwards, MS2 spectra displayed by the RawDataVisualization tool (MS2 extractor), have highlighted fragment mass differences and diagnostic fragments, if some were detected.: "MS2 spectra displayed by the RawDataVisualization tool (MS2 extractor), have highlighted fragment mass differences and diagnostic fragments, if some were detected."
