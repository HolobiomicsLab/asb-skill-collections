---
name: dda-spectrum-association-to-features
description: Use when you have centroided DDA mzML data and have already detected
  MS1 features (either via pyOpenMS or external feature finding), and need to extract
  MS2 fragment m/z values and diagnostic patterns (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0621
  tools:
  - pyOpenMS
  - Python
  - MSConvert
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

# DDA Spectrum Association to Features

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Associate MS2 fragment spectra from data-dependent acquisition (DDA) to their parent features detected in MS1, enabling diagnostic fragment analysis and mass difference calculation for PFAS prioritization. This skill bridges raw spectral data to feature-level annotations by linking precursor ions to their fragment mass patterns.

## When to use

Apply this skill when you have centroided DDA mzML data and have already detected MS1 features (either via pyOpenMS or external feature finding), and need to extract MS2 fragment m/z values and diagnostic patterns (e.g., CF2 losses, perfluoroalkyl chain fragments) to annotate and prioritize potential PFAS compounds. Use it specifically when you want to move beyond retention time and mass accuracy filtering to leverage fragmentation patterns as a secondary prioritization signal.

## When NOT to use

- Input is data-independent acquisition (DIA) or untargeted MS1-only data without MS2 fragmentation spectra.
- Feature list was generated from external software and corresponding mzML file is not available (MS2 data cannot be retrieved).
- MS2 spectra are profile-mode rather than centroided (fragment m/z values cannot be reliably extracted).

## Inputs

- centroided DDA mzML file (data-dependent acquisition with MS1 and MS2 spectra)
- detected MS1 features table (m/z, retention time, intensity)
- diagnostic fragment mass difference library (e.g., CF2 loss, expected m/z shifts)

## Outputs

- per-feature MS2 fragment m/z value list
- per-feature diagnostic fragment match table (fragment m/z, mass difference, fragment identity)
- per-feature diagnostic fragment count and annotation
- annotated feature table with MS2 hit counts and fragment assignments

## How to apply

For each detected MS1 feature (precursor m/z and retention time), query the DDA mzML file to retrieve all associated MS2 scans within the feature's RT window. Extract fragment m/z values from each MS2 spectrum and compute mass differences between the precursor ion and each fragment. Search for characteristic PFAS diagnostic patterns by comparing observed mass differences against known losses (e.g., CF2 = 50.0078 Da, perfluoroalkyl chain fragments). Annotate each feature with the count and identity of matched diagnostic fragments. The rationale is that PFAS compounds exhibit stereotyped fragmentation patterns reflecting their perfluorinated structure; features with multiple diagnostic fragments are more likely true PFAS signals and should be prioritized over features lacking this corroborating MS2 evidence. This approach complements mass defect and MD/C-m/C filtering by adding orthogonal chemical specificity.

## Related tools

- **pyOpenMS** (loads and parses centroided DDA mzML spectra and enables programmatic access to MS1 and MS2 scan data for feature-spectrum linking) — https://github.com/OpenMS/OpenMS
- **Python** (orchestrates mzML parsing, feature-spectrum association logic, and diagnostic fragment matching and annotation)
- **MSConvert** (converts vendor-specific raw mass spectrometry data to vendor-independent mzML format with centroided spectra for input to the association workflow)

## Examples

```
import pyopenms as pms; exp = pms.MSExperiment(); pms.MzMLFile().load('sample.mzML', exp); [extract_ms2_for_feature(feature, exp, diagnostic_fragments_library) for feature in feature_list]
```

## Evaluation signals

- Each detected feature has at least one associated MS2 spectrum (non-null MS2 fragment list) when MS2 scans exist within its RT window.
- Mass differences between precursor and observed fragments match known PFAS diagnostic losses (e.g., CF2 = 50.0078 Da) within instrument mass accuracy tolerance (typically ≤5 ppm).
- Per-feature diagnostic fragment count is ≥1 for high-confidence PFAS candidates and correlates with expected fragmentation patterns of perfluorinated compounds.
- MS2 fragment m/z values are within the 0–2000 m/z range typical for HRMS analyzers and below the precursor m/z.
- Feature-to-MS2 linkage is consistent across sample replicates (same m/z and RT yield the same diagnostic fragment pattern).

## Limitations

- Diagnostic fragment detection depends on MS2 scan frequency and DDA trigger settings; features with very low abundance or co-eluting precursors may not be selected for MS2 fragmentation, yielding missing MS2 data.
- Diagnostic fragment library must be curated for the specific PFAS class of interest (e.g., PFOA vs. PFOS); generic mass difference cutoffs may miss structural variants or cause false matches.
- MS2 spectral quality (signal-to-noise, fragment intensity) affects reliability of mass difference calculation; low-abundance fragments near baseline noise may be falsely matched.
- One collision energy per precursor is assumed in the workflow; variable collision energies or stepped fragmentation may alter fragment patterns and complicate diagnostic matching.

## Evidence

- [other] extract all associated MS2 fragment m/z values: "For each detected feature, extract all associated MS2 fragment m/z values."
- [other] compute mass differences between precursor and fragment ions: "Search for diagnostic fragment patterns by computing mass differences between precursor and fragment ions."
- [other] characteristic fragment mass differences indicative of PFAS compounds: "Identify characteristic fragment mass differences indicative of PFAS compounds (e.g., CF2 loss, perfluoroalkyl chain fragments)."
- [other] pyOpenMS for loading centroided DDA spectra: "Load centroided DDA spectra from mzML file using pyOpenMS."
- [readme] Sample and blank for raw data input should have been measured under data-dependent acquisition (ddMS2) with centroided spectra: "Sample and blank for raw data input in PFΔScreen should have been measured under data-dependent acquisition (ddMS2) with centroided spectra"
- [readme] diagnostic fragments are displayed in MS2 spectra after prioritization: "MS2 spectra displayed by the RawDataVisualization tool (MS2 extractor), have highlighted fragment mass differences and diagnostic fragments, if some were detected."
