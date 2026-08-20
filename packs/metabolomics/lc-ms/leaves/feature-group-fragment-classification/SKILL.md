---
name: feature-group-fragment-classification
description: Use when you have a detected LC-MS feature table (with m/z, retention time, and intensity columns) and need to identify which features are derivatives of the same parent molecule rather than distinct metabolites.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3647
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - masscube
  - Python
  techniques:
  - LC-MS
derived_from:
- doi: 10.1038/s41467-025-60640-5
  title: MassCube
evidence_spans:
- masscube is an integrated Python package for liquid chromatography-mass spectrometry (LC-MS) data processing.
- masscube is an integrated Python package for liquid chromatography-mass spectrometry (LC-MS) data processing
- masscube is an integrated Python package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_masscube_cq
    doi: 10.1038/s41467-025-60640-5
    title: MassCube
  dedup_kept_from: coll_masscube_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-025-60640-5
  all_source_dois:
  - 10.1038/s41467-025-60640-5
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-group-fragment-classification

## Summary

Annotate and group LC-MS features as isotopes, adducts, or in-source fragments by applying mass-shift detection logic and neutral-loss pattern matching. This skill produces a labeled feature table that disambiguates related peaks, enabling more accurate downstream metabolite identification and reduces false positives in nontargeted metabolomics.

## When to use

Apply this skill when you have a detected LC-MS feature table (with m/z, retention time, and intensity columns) and need to identify which features are derivatives of the same parent molecule rather than distinct metabolites. Use it before MS/MS annotation or statistical analysis to collapse redundant features and improve annotation confidence.

## When NOT to use

- Input is already a curated, manually validated feature group assignment.
- Analysis does not require disambiguation of related features (e.g., targeted assay with known metabolite list).
- Raw spectrum data have not yet undergone peak detection and segmentation.

## Inputs

- LC-MS feature table (m/z, retention time, intensity columns)
- Detection parameters (isotope mass tolerance, retention time window, adduct mass shifts, neutral loss patterns)

## Outputs

- Annotated feature table with group ID and annotation label per feature
- Feature group membership assignments (isotope, adduct, or in-source fragment)

## How to apply

Load the feature table containing m/z, retention time, and intensity values. Apply isotope detection by identifying features that differ by 1.003 Da (carbon-13 isotope shift) within a shared retention time window. Apply adduct detection to identify features related by common mass shifts (+H, +Na, +NH4, +K, –H). Apply in-source fragment detection to identify features related by characteristic neutral loss patterns (–H2O, –NH3). Assign each feature a group ID and annotation label (isotope, adduct, or fragment) based on detected relationships. Output the annotated feature table with group membership and annotation type for downstream use.

## Related tools

- **masscube** (Integrated LC-MS data processing package implementing feature group annotation via isotope, adduct, and in-source fragment detection) — https://github.com/huaxuyu/masscube/
- **Python** (Language environment for executing masscube annotation workflows)

## Evaluation signals

- All features in the output table have a non-null group ID and annotation label (isotope, adduct, or fragment).
- Isotope-grouped features differ by 1.003 ± tolerance Da and share retention time within specified window.
- Adduct-grouped features match known mass shifts (+H, +Na, +NH4, +K, –H) and share retention time.
- Fragment-grouped features are linked to parent features by documented neutral loss patterns (–H2O, –NH3).
- Number of unique group IDs is less than the total number of features (feature collapsing has occurred).
- No feature is assigned to multiple groups (group membership is mutually exclusive).

## Limitations

- Annotation accuracy depends on correct specification of isotope mass tolerance, retention time window, and adduct/neutral loss parameters; misaligned windows may merge unrelated features or fail to link true relatives.
- In-source fragments are detected only if their neutral loss patterns are predefined; unexpected loss patterns will not be captured.
- Features with very similar m/z and retention time may be conflated if tolerance windows are too wide.
- No changelog is provided for the masscube package, limiting visibility into method updates or bug fixes.

## Evidence

- [other] masscube implements a feature group annotation mechanism that confidently labels features as isotopes, adducts, and in-source fragments.: "masscube implements a feature group annotation mechanism that confidently labels features as isotopes, adducts, and in-source fragments."
- [other] Load the feature table (containing m/z, retention time, and intensity values for detected features). Apply isotope detection logic to identify features differing by 1.003 Da (carbon-13 isotope shift) within a retention time window.: "Load the feature table (containing m/z, retention time, and intensity values for detected features). Apply isotope detection logic to identify features differing by 1.003 Da (carbon-13 isotope shift)"
- [other] Apply adduct detection to identify features related by common adduct mass shifts (e.g., +H, +Na, +NH4, +K, –H).: "Apply adduct detection to identify features related by common adduct mass shifts (e.g., +H, +Na, +NH4, +K, –H)."
- [other] Apply in-source fragment detection to identify features related by characteristic neutral loss patterns (e.g., –H2O, –NH3).: "Apply in-source fragment detection to identify features related by characteristic neutral loss patterns (e.g., –H2O, –NH3)."
- [readme] Confident annotation of feature groups including isotopes, adducts and in-source fragments.: "Confident annotation of feature groups including isotopes, adducts and in-source fragments."
