---
name: pfas-feature-prioritization
description: Use when you have detected features in LC- or GC-HRMS data (via pyOpenMS
  or custom feature tables) and need to systematically rank them for likelihood of
  being PFAS compounds.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - Python
  - PFΔScreen
  - pyOpenMS
  - MSConvert
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1007/s00216-023-05070-2
  title: pfdeltascreen
evidence_spans:
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

# PFAS Feature Prioritization

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

A multi-criteria approach to rank potential per- and polyfluoroalkyl substance (PFAS) features from non-target HRMS data by combining mass defect analysis (MD/C-m/C), Kendrick mass defect (KMD), and MS2 fragment diagnostics. This skill identifies candidate PFAS structures in complex LC- or GC-HRMS datasets where PFAS presence is suspected but not confirmed a priori.

## When to use

Apply this skill when you have detected features in LC- or GC-HRMS data (via pyOpenMS or custom feature tables) and need to systematically rank them for likelihood of being PFAS compounds. Use it especially when analyzing environmental or biological samples where PFAS contamination is possible but the identity of individual features is unknown, and you want to reduce manual inspection burden by focusing on the most promising candidates.

## When NOT to use

- Input is already a curated or confirmed PFAS structure library — use this for suspect screening, not verification.
- Raw MS data lacks MS2 spectra or was acquired in MS1-only mode — KMD and fragment-based prioritization cannot be applied.
- Features have not been assigned molecular formulas — MD/C calculations require exact molecular composition.

## Inputs

- Feature list with m/z values and assigned molecular formulas (Excel, CSV, or internally detected via pyOpenMS)
- mzML files (centroided, data-dependent MS/MS) containing MS1 and MS2 spectra
- Optional: blank control mzML file for blank correction and coelution filtering

## Outputs

- Ranked feature list with MD/C scores, KMD values, and PFAS prioritization flags (Excel format)
- Interactive HTML plots: MD/C-m/C scatter plot, m/z vs. retention time plot, KMD vs. m/z linked plot, m/C histogram
- MS2 spectral views with highlighted diagnostic fragment mass differences

## How to apply

Load a feature list with m/z values and assigned molecular formulas (from MS1 data or external feature finding software). Calculate the exact mass for each molecular formula using standard atomic masses, then compute mass defect as (observed m/z − exact mass). Divide mass defect by the number of carbon atoms in the formula to obtain the MD/C value, and apply a threshold-based filter to flag potential PFAS (typically MD/C values characteristic of fluorine-rich structures). In parallel, compute Kendrick mass defect using fluorine as the repeating unit to detect homologous series. For features with available MS2 data, calculate fragment mass differences relative to diagnostic PFAS fragments (e.g., CF3+, CF2, SO2NH− losses) and score coelution patterns. Combine all three scores into a final ranking that orders features by priority for further investigation or structure elucidation.

## Related tools

- **PFΔScreen** (Implements the full prioritization workflow with GUI, feature detection, MD/C-m/C filtering, KMD analysis, MS2 alignment, and visualization) — https://github.com/JonZwe/PFAScreen
- **pyOpenMS** (Detects features in MS raw data and performs centroiding and feature alignment prior to prioritization)
- **MSConvert** (Converts vendor-specific MS raw data formats to vendor-independent mzML format for input to PFΔScreen)

## Evaluation signals

- MD/C values for prioritized features should cluster in the range expected for fluorinated compounds (typically higher than non-fluorinated organics); verify against a curated reference set of known PFAS.
- Kendrick mass defect plot should show homologous series (regular spacing in m/z for same KMD, indicating CF2 or similar repeating units).
- MS2 spectra for top-ranked features should contain diagnostic loss patterns (e.g., loss of CF2, SO2, NH groups) visible as peaks in the fragment mass difference histogram.
- Blank-corrected features with high PFAS scores should have sample/blank abundance ratio > ~3 to reduce false positives from contamination.
- Runtime for the full workflow on 4000 spectra per sample should be <1 minute; significant delays suggest parameter misconfiguration or data quality issues.

## Limitations

- MD/C filtering requires accurate molecular formula assignment; formula errors (e.g., misassignment of nitrogen/sulfur count) will cause false negatives or false positives.
- Kendrick mass defect analysis assumes PFAS contain repeating CF2 units; PFAS with branched or unusual fluorine patterns may not be detected.
- Fragment mass difference scoring depends on MS2 data quality and collision energy optimization; poor ionization or non-optimal fragmentation will reduce prioritization sensitivity.
- No changelog documented for the software; version stability and backward compatibility with older results uncertain.
- Requires centroided spectra and data-dependent acquisition (ddMS2) — profile-mode or targeted MS/MS data cannot be processed.

## Evidence

- [other] The MD/C approach filters and prioritizes potential PFAS features from non-target HRMS data: "Calculate mass defect (observed m/z minus exact mass) for each feature. Divide mass defect by the number of carbon atoms in the molecular formula to obtain MD/C value. Apply MD/C threshold criterion"
- [intro] Prioritization combines three independent scoring methods: "PFΔScreen uses several techniques for prioritization such as the MD/C-m/C approach, Kendrick mass defect (KMD) analysis and fragment mass differences and diagnostic fragments in the MS2 data"
- [readme] Input format and data acquisition requirements: "Sample and blank for raw data input in PFΔScreen should have been measured under data-dependent acquisition (ddMS2) with centroided spectra, ideally with one collision energy per precursor."
- [readme] Output and visualization suite: "PFΔScreen results table (Excel format) and several interactive HTML plots are saved in a folder named after the sample that can be easily inspected, including a MD/C-m/C plot, a m/z vs. RT plot (with"
- [readme] Feature detection prerequisite: "pyOpenMS (Python interface to the C++ OpenMS library) is used for feature detection in MS raw data. Optionally, custom feature lists can be included."
- [readme] Runtime performance: "The overall rather short runtime (e.g., less than one minute in case of 4000 spectra per sample for the whole workflow), allows a convenient adjustment of input parameters."
