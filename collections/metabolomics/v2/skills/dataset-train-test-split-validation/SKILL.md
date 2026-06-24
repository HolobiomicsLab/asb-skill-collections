---
name: dataset-train-test-split-validation
description: Use when when preparing MS/MS spectra for deep learning model training
  on a specific instrument type (e.g., Orbitrap, Q-TOF), and you need to verify that
  configuration-driven filtering (e.g., adding 'ftms' to an instrument allowlist)
  produces training and test sets of the expected size (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - FIDDLE
  - msfiddle
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1038/s41467-025-66060-9
  title: fiddle
evidence_spans:
- FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_fiddle_cq
    doi: 10.1038/s41467-025-66060-9
    title: fiddle
  dedup_kept_from: coll_fiddle_cq
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

# dataset-train-test-split-validation

## Summary

Partition a curated MS/MS spectral dataset into training and test subsets according to instrument-specific allowlists and target class distributions, then validate that the resulting splits match expected compound counts and maintain reproducibility across preprocessing runs.

## When to use

When preparing MS/MS spectra for deep learning model training on a specific instrument type (e.g., Orbitrap, Q-TOF), and you need to verify that configuration-driven filtering (e.g., adding 'ftms' to an instrument allowlist) produces training and test sets of the expected size (e.g., 28,751 training and 3,195 test compounds for Orbitrap).

## When NOT to use

- The input dataset has already been split and validated for a different instrument type (e.g., Q-TOF); re-splitting may introduce data leakage or biased estimates.
- The target training/test counts are unknown or unavailable; validation cannot proceed without a documented ground truth.
- The spectra are already labeled with train/test assignments; modifying the allowlist may violate the original experimental design.

## Inputs

- FIDDLE YAML configuration file (e.g., config/fiddle_tcn_orbitrap.yml)
- Raw MS/MS spectral dataset (MGF or internal format)
- Instrument type allowlist (string array)

## Outputs

- Training set compound partition (filtered spectra)
- Test set compound partition (filtered spectra)
- Count report (train_count, test_count)

## How to apply

Load the instrument-specific FIDDLE configuration file (e.g., config/fiddle_tcn_orbitrap.yml) and modify the gnps_orbitrap instrument allowlist to include the target instrument type (e.g., 'ftms'). Run the FIDDLE dataset preprocessing pipeline with the updated configuration to filter spectra by the allowlisted instruments and apply any additional partitioning logic (e.g., stratified random split). After preprocessing completes, count the total compounds in the resulting training set and test set. Compare the observed counts against the documented target values (e.g., 28,751 training, 3,195 test). If counts match, the split is validated; if they diverge, investigate whether the configuration change or filtering logic was applied correctly.

## Related tools

- **FIDDLE** (Orchestrates dataset preprocessing, filtering by instrument allowlist, and train/test partitioning for MS/MS spectra.) — https://github.com/JosieHong/FIDDLE
- **msfiddle** (Provides CLI and Python API for FIDDLE model inference and dataset validation.) — https://github.com/josiehong/msfiddle

## Examples

```
cd FIDDLE && python -c "import yaml; config = yaml.safe_load(open('config/fiddle_tcn_orbitrap.yml')); config['gnps_orbitrap']['instruments'].append('ftms'); print(f'Train: {config[\"train_size\"]}, Test: {config[\"test_size\"]}')"
```

## Evaluation signals

- Training set compound count equals or exceeds the documented target (e.g., 28,751 for Orbitrap).
- Test set compound count matches the documented target (e.g., 3,195 for Orbitrap).
- No spectra appear in both training and test partitions (disjoint sets).
- All spectra in each partition originate from the allowlisted instrument types.
- Re-running the preprocessing pipeline with the same configuration produces identical train/test counts (reproducibility).

## Limitations

- The task card indicates 'no direct evidence' that the expected dataset sizes (28,751 training, 3,195 test) were achieved after modification, suggesting validation may not have been completed or documented.
- Configuration-driven allowlist changes depend on correct YAML syntax and field naming; errors in the configuration file will silently propagate and produce incorrect splits.
- The preprocessing pipeline may apply additional filtering steps (e.g., mass range, collision energy) beyond the instrument allowlist, which could reduce the final counts below targets if those filters are not explicitly controlled.

## Evidence

- [other] Does adding 'ftms' to the gnps_orbitrap instrument allowlist in the FIDDLE configuration expand the Orbitrap dataset to the target size of 28,751 training and 3,195 test compounds?: "research_question from task_004 defining the target counts and validation objective"
- [other] Modify the gnps_orbitrap instrument allowlist to include 'ftms' as an additional allowed instrument type. Run the FIDDLE dataset preprocessing pipeline with the updated configuration to filter and partition the Orbitrap spectra. Count the resulting training set compounds (expected: 28,751) and test set compounds (expected: 3,195) and verify both counts match the target values.: "workflow steps from task_004 describing the exact sequence of configuration, preprocessing, and validation"
- [readme] Load the config/fiddle_tcn_orbitrap.yml configuration file.: "README instruction showing exact configuration file naming and loading procedure"
- [readme] FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra. This repository contains the full research codebase for model training, evaluation, and paper reproduction.: "README description of FIDDLE's purpose and dataset preprocessing role"
- [other] Run the FIDDLE dataset preprocessing pipeline with the updated configuration to filter and partition the Orbitrap spectra.: "task_004 workflow describing dataset preprocessing and partitioning pipeline"
