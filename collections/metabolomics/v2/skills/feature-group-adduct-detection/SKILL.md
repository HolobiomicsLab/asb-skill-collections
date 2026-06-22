---
name: feature-group-adduct-detection
description: Use when you have a feature table from LC-MS analysis (containing m/z, retention time, and intensity values) and need to identify which detected features represent the same molecular species ionized under different adduction states.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-025-60640-5
  all_source_dois:
  - 10.1038/s41467-025-60640-5
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-group-adduct-detection

## Summary

Automated detection and grouping of LC-MS features related by common adduct mass shifts (e.g., +H, +Na, +NH4, +K, –H) to consolidate redundant ion species into coherent feature groups. This skill is essential in nontargeted metabolomics to reduce false feature inflation and improve annotation confidence.

## When to use

You have a feature table from LC-MS analysis (containing m/z, retention time, and intensity values) and need to identify which detected features represent the same molecular species ionized under different adduction states. Apply this skill when you observe multiple peaks at similar retention times with m/z differences matching known adduct mass shifts, and you want to collapse them into single annotated groups before downstream statistical or identification analysis.

## When NOT to use

- Input is already a consolidated feature group table (adduct annotation already performed)
- Analysis requires all individual ion forms preserved for targeted adduct-specific quantification
- Data originates from targeted methods with predefined adduct forms (e.g., selected reaction monitoring where adducts are already controlled)

## Inputs

- Feature table (CSV or tabular format with columns: m/z, retention time, intensity)
- LC-MS feature detection output (nontargeted peak detection results)

## Outputs

- Annotated feature table with group ID assignments
- Adduct annotation labels per feature group
- Feature group membership (parent–adduct relationships)

## How to apply

Load the feature table and apply masscube's adduct detection logic to systematically identify features related by characteristic adduct mass shifts including +H (1.008 Da), +Na (22.990 Da), +NH4 (18.034 Da), +K (38.963 Da), and –H (−1.008 Da). For each feature, search for coeluting features (within the same retention time window) whose m/z values differ by these canonical shifts. Assign matching features to the same group ID with annotation label 'adduct', allowing the algorithm to determine parent–daughter relationships and multiplicity. Output the annotated feature table with group membership and adduct type labels, which consolidates redundant ion species and enables more confident molecular identification.

## Related tools

- **masscube** (Integrated LC-MS data processing package that implements adduct detection via common adduct mass shift patterns) — https://github.com/huaxuyu/masscube/
- **Python** (Runtime environment for masscube)

## Examples

```
from masscube import FeatureGroupAnnotation; annotated_features = FeatureGroupAnnotation.detect_adducts(feature_table, mz_tolerance=0.005, rt_window=10)
```

## Evaluation signals

- All features assigned a group ID; no feature left ungrouped (except singletons, which are valid single-feature groups)
- Each adduct-annotated group contains features with m/z differences matching canonical adduct mass shifts (±0.005 Da tolerance typical for high-resolution MS)
- All features within a single adduct group coelute within the specified retention time window (no spurious cross-retention-time assignments)
- Feature group count is significantly lower than raw feature count, confirming redundancy reduction
- Annotated adduct types match known ionization patterns for the LC-MS method (e.g., +H, +Na, +NH4 prevalence aligns with solvent and sample composition)

## Limitations

- Relies on accurate m/z and retention time measurements; poor peak detection or high mass calibration error will degrade adduct pairing accuracy
- Cannot distinguish between true adducts and coincidental m/z overlaps unless retention time tolerance is carefully tuned to the LC method
- May misassign features if isotope patterns or in-source fragments overlap with adduct mass shifts; requires sequential or cascading logic (isotope → adduct → fragment detection) to avoid conflicts
- No changelog provided; algorithm parameters and thresholds not explicitly documented in the README

## Evidence

- [intro] Confident annotation of feature groups including isotopes, adducts and in-source fragments.: "Confident annotation of feature groups including isotopes, adducts and in-source fragments."
- [other] Apply adduct detection to identify features related by common adduct mass shifts (e.g., +H, +Na, +NH4, +K, –H).: "Apply adduct detection to identify features related by common adduct mass shifts (e.g., +H, +Na, +NH4, +K, –H)."
- [other] Assign each feature a group ID and annotation label (isotope, adduct, or fragment) based on detected relationships.: "Assign each feature a group ID and annotation label (isotope, adduct, or fragment) based on detected relationships."
- [other] Load the feature table (containing m/z, retention time, and intensity values for detected features).: "Load the feature table (containing m/z, retention time, and intensity values for detected features)."
- [readme] masscube is an integrated Python package for liquid chromatography-mass spectrometry (LC-MS) data processing.: "masscube is an integrated Python package for liquid chromatography-mass spectrometry (LC-MS) data processing."
