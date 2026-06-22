---
name: retention-time-mass-alignment
description: Use when you have two independent LC-MS untargeted metabolomic feature datasets (each with retention time and m/z values) and need to identify which features in one dataset correspond to features in the other.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - M2S
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.1c03592
  title: m2s
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_m2s
    doi: 10.1021/acs.analchem.1c03592
    title: m2s
  dedup_kept_from: coll_m2s
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c03592
  all_source_dois:
  - 10.1021/acs.analchem.1c03592
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# retention-time-mass-alignment

## Summary

Align and match untargeted LC-MS metabolomic features across two datasets by leveraging retention time and mass-to-charge ratio similarity. This skill enables cross-dataset feature correspondence, producing matched feature tables with alignment scores suitable for comparative metabolomics studies.

## When to use

You have two independent LC-MS untargeted metabolomic feature datasets (each with retention time and m/z values) and need to identify which features in one dataset correspond to features in the other. Use this skill when dataset integration, batch effect assessment, or cross-platform feature validation is required.

## When NOT to use

- Input datasets are not LC-MS-derived or lack both retention time and m/z annotations
- You are attempting to match features within a single dataset rather than across two independent datasets
- Feature tables have already been pre-aligned or merged through other means

## Inputs

- LC-MS untargeted metabolomic feature table 1 (with retention time and m/z columns)
- LC-MS untargeted metabolomic feature table 2 (with retention time and m/z columns)

## Outputs

- Matched feature table with feature correspondences across datasets
- Feature matching scores quantifying alignment confidence

## How to apply

Load both LC-MS feature tables into Matlab, each containing retention time and mass-to-charge ratio annotations. Initialize the M2S package with both feature datasets as input. Execute the M2S matching algorithm, which identifies and links corresponding features across the two datasets based on retention time and m/z similarity. The algorithm compares features by computing similarity in both dimensions (retention time proximity and mass accuracy) to establish confident feature pairs. Export the resulting matched feature table, which records feature correspondences and associated matching scores that quantify alignment confidence.

## Related tools

- **M2S** (Matlab package that executes the retention time and mass-to-charge ratio matching algorithm across two LC-MS feature datasets) — https://github.com/rjdossan/M2S

## Evaluation signals

- Matched feature table contains feature pairs with corresponding retention time and m/z values from both input datasets
- Matching scores are within expected range (typically 0–1, where higher indicates greater confidence in alignment)
- Number of matched features is reasonable relative to input dataset sizes and biological overlap expectations
- Retention time deltas and m/z deltas between matched pairs remain within acceptable instrumental error margins (e.g., typical LC-MS tolerance: <0.5 min RT, <5 ppm m/z)
- No duplicate assignments of a single feature to multiple features across datasets (one-to-one matching integrity)

## Limitations

- Algorithm performance depends on sufficient retention time and m/z overlap between the two datasets; datasets with minimal biological similarity may yield few matches
- Matching is sensitive to retention time drift and instrument calibration differences between LC-MS runs; systematic shifts may require pre-alignment
- Features present in only one dataset will remain unmatched; the skill cannot recover missing or non-overlapping features
- No explicit handling of isomers or isobars (features with identical m/z but different retention times) is documented

## Evidence

- [other] M2S Matlab package designed to match untargeted metabolomic features of two LC-MS datasets: "Matlab package to match untargeted metabolomic features of two LC-MS datasets"
- [full_text] M2S matching algorithm identifies and links corresponding features based on retention time and m/z similarity: "Execute the M2S matching algorithm to identify and link corresponding features across the two datasets based on retention time and mass-to-charge ratio similarity"
- [full_text] Workflow produces matched feature table with feature correspondences and matching scores: "Generate and export the matched feature table containing feature correspondences and matching scores"
