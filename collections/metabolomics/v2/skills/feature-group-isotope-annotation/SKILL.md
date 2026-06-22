---
name: feature-group-isotope-annotation
description: Use when you have a feature table from nontargeted LC-MS peak detection (containing m/z, retention time, and intensity values) and need to disambiguate whether detected features represent the same molecular entity under different ionization/modification states or are true independent signals.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0092
  tools:
  - masscube
  - Python
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
---

# feature-group-isotope-annotation

## Summary

Annotate LC-MS features as isotopes, adducts, or in-source fragments by detecting characteristic mass shifts and neutral loss patterns within retention time windows. This enables confident grouping of related features for downstream metabolite identification.

## When to use

Apply this skill when you have a feature table from nontargeted LC-MS peak detection (containing m/z, retention time, and intensity values) and need to disambiguate whether detected features represent the same molecular entity under different ionization/modification states or are true independent signals. This is essential before metabolite annotation to avoid double-counting isotopes or adducts as separate compounds.

## When NOT to use

- Input is already a metabolite annotation table or compound list (annotation is already complete)
- Raw LC-MS data (unprocessed .mzML or .raw files) — peak detection must be run first
- Single-feature queries or very small feature sets where grouping relationships cannot be reliably detected

## Inputs

- Feature table with m/z, retention time, and intensity values
- Detected LC-MS features (nontargeted peak detection output)

## Outputs

- Annotated feature table with group IDs
- Annotation labels per feature (isotope, adduct, in-source fragment)
- Feature group membership assignments

## How to apply

Load the feature table and sequentially apply three detection logics: (1) Isotope detection: identify features differing by 1.003 Da (carbon-13 shift) within a retention time window, indicating the same compound at different mass isotopologue states. (2) Adduct detection: identify features related by common adduct mass shifts (+H, +Na, +NH4, +K, –H), which represent the same molecular mass ionized differently. (3) In-source fragment detection: identify features related by characteristic neutral losses (–H2O, –NH3), representing molecular fragmentation occurring before or during ionization. Assign each feature a group ID and annotation label based on detected relationships, outputting an annotated feature table with group membership and annotation type. The rationale is that masscube implements confident grouping logic that distinguishes true chemical variants from instrumental artifacts or data processing duplicates.

## Related tools

- **masscube** (implements feature group annotation mechanism with isotope, adduct, and in-source fragment detection logic) — https://github.com/huaxuyu/masscube/
- **Python** (runtime environment for masscube package)

## Evaluation signals

- Every feature in the output table has a non-null group ID and annotation label
- Features within a group have m/z differences matching expected shifts: ~1.003 Da (isotopes), adduct mass deltas (+18.01 for NH4, +22.99 for Na, etc.), or neutral loss patterns (18.01 for H2O, 17.01 for NH3)
- Features within a group share approximately identical retention times (within the configured window)
- No feature is assigned to multiple groups (group IDs are mutually exclusive)
- Ungrouped features (singletons) retain valid group IDs and are labeled as such, indicating the annotation completed fully

## Limitations

- Detection accuracy depends on mass accuracy and resolution of the LC-MS instrument; lower resolution or higher mass error may cause false negatives in group assignment
- Retention time window tolerance must be calibrated for the specific LC method; overly strict windows miss legitimate co-eluting isotopologues, while permissive windows create false positive groupings
- In-source fragmentation detection relies on predefined neutral loss patterns; novel or compound-specific losses not in the reference list will be missed
- Overlapping groups or complex multi-isotope/multi-adduct features may not be fully disambiguated by sequential application of detection logics

## Evidence

- [other] masscube implements a feature group annotation mechanism that confidently labels features as isotopes, adducts, and in-source fragments.: "masscube implements a feature group annotation mechanism that confidently labels features as isotopes, adducts, and in-source fragments."
- [other] Apply isotope detection logic to identify features differing by 1.003 Da (carbon-13 isotope shift) within a retention time window.: "Apply isotope detection logic to identify features differing by 1.003 Da (carbon-13 isotope shift) within a retention time window."
- [other] Apply adduct detection to identify features related by common adduct mass shifts (e.g., +H, +Na, +NH4, +K, –H).: "Apply adduct detection to identify features related by common adduct mass shifts (e.g., +H, +Na, +NH4, +K, –H)."
- [other] Apply in-source fragment detection to identify features related by characteristic neutral loss patterns (e.g., –H2O, –NH3).: "Apply in-source fragment detection to identify features related by characteristic neutral loss patterns (e.g., –H2O, –NH3)."
- [intro] Confident annotation of feature groups including isotopes, adducts and in-source fragments.: "Confident annotation of feature groups including isotopes, adducts and in-source fragments."
- [readme] masscube is an integrated Python package for liquid chromatography-mass spectrometry (LC-MS) data processing.: "masscube is an integrated Python package for liquid chromatography-mass spectrometry (LC-MS) data processing."
