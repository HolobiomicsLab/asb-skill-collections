---
name: dataset-preprocessing-and-filtering
description: Use when when you have a raw GNPS or other spectral library dataset with
  inconsistent or incomplete instrument annotations, and you need to verify or reproduce
  reported dataset split counts (e.g., training/test compound ratios). Apply this
  skill when an instrument allowlist fix (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - msfiddle
  - FIDDLE
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41467-025-66060-9
  title: fiddle
evidence_spans:
- 'CLI and Python API: [msfiddle](https://github.com/josiehong/msfiddle)'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_fiddle
    doi: 10.1038/s41467-025-66060-9
    title: fiddle
  dedup_kept_from: coll_fiddle
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-025-66060-9
  all_source_dois:
  - 10.1038/s41467-025-66060-9
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# dataset-preprocessing-and-filtering

## Summary

Filter and preprocess tandem mass spectrometry (MS/MS) spectral datasets by applying instrument-specific allowlists and re-running dataset splitting logic to obtain curated training and test compound partitions. This skill ensures that spectral records matching updated instrument metadata criteria are retained and correctly split into balanced subsets for model training and evaluation.

## When to use

When you have a raw GNPS or other spectral library dataset with inconsistent or incomplete instrument annotations, and you need to verify or reproduce reported dataset split counts (e.g., training/test compound ratios). Apply this skill when an instrument allowlist fix (e.g., adding 'ftms' to gnps_orbitrap category) has been applied and you need to confirm that the preprocessing pipeline now yields the expected training and test partition sizes.

## When NOT to use

- Input spectral dataset is already pre-filtered and split into documented training/test partitions with no missing or incorrect instrument annotations.
- The instrument metadata in your dataset is complete, consistent, and does not contain ambiguous or mislabeled instrument types that would be resolved by an allowlist update.
- You are working with a proprietary or non-GNPS spectral library with different metadata schemas that do not align with msfiddle's instrument enumeration and filtering logic.

## Inputs

- Raw GNPS spectral library (MGF or indexed format with TITLE, PRECURSOR_MZ, PRECURSOR_TYPE, COLLISION_ENERGY, and instrument metadata fields)
- Instrument allowlist configuration file (JSON or YAML with instrument type mappings)
- Preprocessing configuration (msfiddle config YAML specifying filter criteria and split ratios)

## Outputs

- Filtered spectral dataset (MGF or CSV with subset of original spectra meeting instrument allowlist criteria)
- Training set compound partition (list of compound IDs or spectra, typically CSV with counts and metadata)
- Test set compound partition (list of compound IDs or spectra, typically CSV with counts and metadata)
- Dataset split summary report (text or CSV with training count, test count, and filter statistics)

## How to apply

Load the raw GNPS spectral dataset and its associated instrument metadata. Update the instrument allowlist configuration in the msfiddle preprocessing module to include or correct instrument type mappings (e.g., adding 'ftms' to the gnps_orbitrap category). Re-run the dataset filtering and splitting logic using msfiddle's preprocessing routines with the updated allowlist. Extract the training set compound count and test set compound count from the preprocessed output (typically CSV or structured metadata). Compare the observed counts against the expected baseline (e.g., 28,751 training / 3,195 test compounds) to confirm the fix resolves previous discrepancies and produces reproducible splits.

## Related tools

- **msfiddle** (CLI and Python API for preprocessing, filtering, and splitting GNPS spectral datasets; applies instrument allowlist to filter spectra and re-partitions training/test sets) — https://github.com/josiehong/msfiddle
- **FIDDLE** (Full research codebase containing preprocessing scripts and dataset utilities; provides training and evaluation infrastructure for filtered and partitioned datasets) — https://github.com/JosieHong/FIDDLE

## Evaluation signals

- Verify that the training set compound count matches the expected value (e.g., 28,751 compounds). Exact match indicates the instrument allowlist fix was applied correctly.
- Verify that the test set compound count matches the expected value (e.g., 3,195 compounds). Exact match indicates correct train/test split ratio.
- Check that no spectra are lost or duplicated between the original and filtered datasets by comparing total counts before and after preprocessing.
- Confirm that all spectra in the filtered output contain valid instrument type annotations matching the updated allowlist (e.g., 'ftms' is now recognized in gnps_orbitrap records).
- Validate that the train/test split is deterministic and reproducible by re-running the preprocessing with the same random seed and confirming identical partition assignments.

## Limitations

- The instrument allowlist mapping is hardcoded in msfiddle and may not generalize to spectral libraries outside GNPS or with non-standard instrument nomenclature.
- Dataset split is sensitive to the random seed and the order of input records; reproducibility requires documenting and fixing the preprocessing seed.
- The expected training/test counts (28,751 / 3,195) are specific to the Orbitrap instrument allowlist fix and do not apply to Q-TOF or other instrument types without recalibration.
- No explicit discussion section in the FIDDLE documentation reports methodological constraints or failure modes of the filtering pipeline; edge cases (e.g., spectra with missing instrument metadata) are not formally described.

## Evidence

- [other] Load the raw GNPS spectral dataset and instrument metadata used in FIDDLE preprocessing. Update the instrument allowlist configuration to include 'ftms' in the gnps_orbitrap category. Re-run the dataset filtering and splitting logic with the updated allowlist using msfiddle.: "Load the raw GNPS spectral dataset and instrument metadata used in FIDDLE preprocessing. Update the instrument allowlist configuration to include 'ftms' in the gnps_orbitrap category. Re-run the"
- [other] Extract and verify the training set compound count (expected: 28,751) and test set compound count (expected: 3,195) from the preprocessed output.: "Extract and verify the training set compound count (expected: 28,751) and test set compound count (expected: 3,195) from the preprocessed output."
- [readme] FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra. This repository contains the full research codebase for model training, evaluation, and paper reproduction.: "FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra. This repository contains the full research codebase for model training, evaluation, and paper reproduction."
- [readme] The input format is `mgf`, where `title`, `precursor_mz`, `precursor_type`, `collision_energy` fields are required.: "The input format is `mgf`, where `title`, `precursor_mz`, `precursor_type`, `collision_energy` fields are required."
