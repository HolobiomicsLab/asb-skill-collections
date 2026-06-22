---
name: retention-time-correlation-filtering
description: Use when you have detected multiple LC-MS features (m/z peaks) across a chromatogram and need to distinguish true chemical relationships (isotopes differing by 1.003 Da, adducts with characteristic mass shifts, neutral loss fragments) from noise or unrelated peaks.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
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

# retention-time-correlation-filtering

## Summary

Filter and group LC-MS features by retention time proximity to identify related ion species (isotopes, adducts, in-source fragments). This skill removes spurious or unrelated features and clusters true feature families for confident annotation.

## When to use

Apply this skill when you have detected multiple LC-MS features (m/z peaks) across a chromatogram and need to distinguish true chemical relationships (isotopes differing by 1.003 Da, adducts with characteristic mass shifts, neutral loss fragments) from noise or unrelated peaks. Use it as a prerequisite step before assigning feature group annotations, especially when peak detection may have introduced redundant or artifactual signals.

## When NOT to use

- Input is already a feature table with pre-assigned group IDs and validated annotations — skip to MS/MS annotation.
- Retention time information is missing or unreliable (e.g., retention time noise exceeds the expected mass shift tolerance).
- Data is from targeted MS or single-reaction monitoring (SRM) where only a few known m/z values are monitored — feature grouping is unnecessary.

## Inputs

- Feature table (CSV, TSV, or in-memory table with columns: m/z, retention time (seconds), intensity, feature ID)
- Retention time tolerance window (numeric, in seconds)
- Expected mass shift dictionary (isotope offset, adduct masses, neutral losses)

## Outputs

- Annotated feature table with group ID and annotation type (isotope, adduct, in-source fragment, or singleton)
- Feature group membership report (feature ID → group ID mapping)
- Filtered/clustered feature matrix ready for downstream MS/MS annotation

## How to apply

Load a feature table containing m/z, retention time, and intensity values for all detected peaks. Define a retention time window (typically narrow, e.g., ±5–10 seconds) around each feature. Within that window, search for co-eluting features whose m/z values match expected mass differences: isotope shifts (1.003 Da for ¹³C), common adduct mass shifts (+H, +Na, +NH₄, +K, –H), or characteristic neutral losses (–H₂O, –NH₃). Group features sharing the same retention time envelope and matching mass relationships. Assign each group a group ID and annotation label. Features outside the retention time window or without matching mass offsets are retained as singletons or discarded based on quality thresholds.

## Related tools

- **masscube** (Implements feature group annotation mechanism with isotope, adduct, and in-source fragment detection logic applied within retention time windows) — https://github.com/huaxuyu/masscube/
- **Python** (Language and runtime environment for masscube package and custom filtering workflows)

## Evaluation signals

- Verify that all features within each group share a common retention time window (check max Δ RT ≤ tolerance).
- Verify that each feature pair within a group exhibits a mass offset matching one of the expected shifts (isotope +1.003 Da, adduct offset, or neutral loss mass).
- Verify that singleton features (those not grouped) have no co-eluting features with matching mass relationships within the RT window.
- Compare feature count before and after filtering; expect reduction if spurious peaks or noise are present.
- Spot-check annotated groups visually or via MS/MS confirmation to ensure isotope/adduct/fragment labels match chemical expectations (e.g., isotope group should show intensity ratio ~1:0.01 for ¹²C:¹³C).

## Limitations

- Accuracy depends critically on the retention time tolerance window; too narrow and true co-eluting features are missed; too wide and unrelated peaks are grouped.
- Mass shift dictionary must be comprehensive and accurate; missing or incorrectly specified adducts/losses will result in false negatives.
- No changelog found in repository documentation, limiting visibility into algorithm changes or bug fixes.
- Overlapping or poorly resolved chromatographic peaks may confound retention time correlation, leading to incorrect grouping.

## Evidence

- [other] isotope detection logic to identify features differing by 1.003 Da (carbon-13 isotope shift) within a retention time window: "Apply isotope detection logic to identify features differing by 1.003 Da (carbon-13 isotope shift) within a retention time window."
- [other] adduct detection to identify features related by common adduct mass shifts: "Apply adduct detection to identify features related by common adduct mass shifts (e.g., +H, +Na, +NH4, +K, –H)."
- [other] in-source fragment detection to identify features related by characteristic neutral loss patterns: "Apply in-source fragment detection to identify features related by characteristic neutral loss patterns (e.g., –H2O, –NH3)."
- [intro] Confident annotation of feature groups including isotopes, adducts and in-source fragments: "Confident annotation of feature groups including isotopes, adducts and in-source fragments."
- [other] Load the feature table (containing m/z, retention time, and intensity values for detected features): "Load the feature table (containing m/z, retention time, and intensity values for detected features)."
