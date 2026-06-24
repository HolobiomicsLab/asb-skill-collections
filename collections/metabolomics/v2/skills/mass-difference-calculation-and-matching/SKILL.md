---
name: mass-difference-calculation-and-matching
description: Use when you have centroided data-dependent acquisition (DDA) MS2 spectra
  from LC- or GC-HRMS and need to annotate detected features with PFAS-specific diagnostic
  fragments. Use it after feature detection (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
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

# Mass-difference calculation and matching

## Summary

Computes and matches characteristic fragment mass differences between precursor and fragment ions in MS2 data to identify diagnostic PFAS patterns (e.g., CF₂ loss, perfluoroalkyl chain fragments). This is one of several prioritization techniques used alongside MD/C-m/C and Kendrick mass defect analysis to screen potential PFAS features in non-target HRMS measurements.

## When to use

Apply this skill when you have centroided data-dependent acquisition (DDA) MS2 spectra from LC- or GC-HRMS and need to annotate detected features with PFAS-specific diagnostic fragments. Use it after feature detection (e.g., via pyOpenMS) when you want to enrich each feature with fragment-level chemical evidence before prioritization ranking.

## When NOT to use

- Input spectra are profile (centroid=false) rather than centroided; mass accuracy and peak resolution will be insufficient for reliable mass difference matching.
- Data acquisition is data-independent (DIA) or MS1-only; no MS2 fragment data are available for mass difference calculation.
- Feature list has already been manually curated or filtered by other orthogonal methods (e.g., chromatographic or isotope pattern matching); mass differences add marginal incremental value and may waste computational effort.

## Inputs

- centroided DDA MS2 spectra (mzML format)
- list of detected precursor m/z values with retention time
- reference table of characteristic PFAS neutral loss mass differences (e.g., CF₂ = 50.0, CF₄ = 100.0)

## Outputs

- per-feature annotation table with diagnostic fragment assignments
- diagnostic fragment count per feature
- list of matched mass differences and their chemical interpretation
- enhanced feature table with MS2-derived prioritization scores

## How to apply

For each detected feature in the MS2 data, extract all associated fragment m/z values from the centroided spectrum. Calculate the mass difference between the precursor m/z and each fragment m/z. Search these differences against a reference set of characteristic PFAS fragment patterns (e.g., neutral losses of CF₂, CF₄, or perfluoroalkyl chain units). Annotate each feature with matched diagnostic fragments and record the count and identities of diagnostic fragments found. Features with multiple diagnostic fragment matches receive higher prioritization scores. The rationale is that PFAS compounds produce reproducible, characteristic neutral loss patterns due to the stability of C–F bonds and perfluoroalkyl backbone fragmentation.

## Related tools

- **pyOpenMS** (parses centroided MS2 spectra from mzML files and provides programmatic access to precursor and fragment m/z values) — https://github.com/OpenMS/OpenMS
- **PFΔScreen** (integrates mass difference matching with MD/C-m/C and KMD analysis for automated PFAS feature prioritization; outputs annotated results table and MS2 spectra with highlighted diagnostic fragments) — https://github.com/JonZwe/PFAScreen
- **MSConvert** (converts vendor-specific raw mass spectrometry data to vendor-independent mzML format with centroided spectra)

## Evaluation signals

- All detected features have a diagnostic fragment count ≥ 0 and the count distributions are internally consistent (no NaN or missing values).
- Matched mass differences fall within expected PFAS neutral loss patterns (e.g., 50 ± 0.005 Da for CF₂, 100 ± 0.005 Da for CF₄) based on instrument mass resolution and calibration.
- Features with known PFAS compounds (positive controls) receive diagnostic fragment annotations with counts > 0; non-PFAS features have counts of 0 or very low counts.
- The number of per-feature diagnostic fragment assignments is > 0 for PFAS-positive features and correlates positively with feature prioritization rank.
- Output annotations (fragment m/z, mass difference, chemical identity) are traceable back to the input MS2 spectrum and can be visually verified in the RawDataVisualization MS2 extractor tool.

## Limitations

- Mass difference matching relies on accurate precursor m/z determination and centroided peak picking; artifacts or miscalibrated spectra will produce false positive diagnostic assignments.
- Characteristic PFAS neutral loss reference table must be curated and may not cover all emerging or unusual PFAS structures; novel compounds with atypical fragmentation will not be recognized.
- Fragment ions near the noise floor may be missed; setting appropriate signal-to-noise thresholds during feature detection is critical to avoid false negatives.
- The skill does not address coelution or overlapping precursor ions; co-fragmenting compounds may produce ambiguous mass difference patterns.
- Data acquisition must be data-dependent (ddMS2) with ideally one collision energy per precursor; variable or undocumented collision energies reduce reproducibility of fragment patterns.

## Evidence

- [other] For each detected feature, extract all associated MS2 fragment m/z values. Search for diagnostic fragment patterns by computing mass differences between precursor and fragment ions.: "For each detected feature, extract all associated MS2 fragment m/z values. Search for diagnostic fragment patterns by computing mass differences between precursor and fragment ions."
- [other] Identify characteristic fragment mass differences indicative of PFAS compounds (e.g., CF2 loss, perfluoroalkyl chain fragments). Annotate each feature with matched diagnostic fragments and mass difference values.: "Identify characteristic fragment mass differences indicative of PFAS compounds (e.g., CF2 loss, perfluoroalkyl chain fragments). Annotate each feature with matched diagnostic fragments and mass"
- [other] PFΔScreen uses fragment mass differences and diagnostic fragments detected in MS2 data as one of several prioritization techniques alongside the MD/C-m/C approach and Kendrick mass defect analysis: "PFΔScreen uses fragment mass differences and diagnostic fragments detected in MS2 data as one of several prioritization techniques alongside the MD/C-m/C approach and Kendrick mass defect analysis"
- [readme] Sample and blank for raw data input in PFΔScreen should have been measured under data-dependent acquisition (ddMS2) with centroided spectra, ideally with one collision energy per precursor.: "Sample and blank for raw data input in PFΔScreen should have been measured under data-dependent acquisition (ddMS2) with centroided spectra, ideally with one collision energy per precursor."
- [readme] Afterwards, MS2 spectra displayed by the RawDataVisualization tool (MS2 extractor), have highlighted fragment mass differences and diagnostic fragments, if some were detected.: "Afterwards, MS2 spectra displayed by the RawDataVisualization tool (MS2 extractor), have highlighted fragment mass differences and diagnostic fragments, if some were detected."
