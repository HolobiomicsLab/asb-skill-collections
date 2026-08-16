---
name: configuration-file-modification
description: Use when when you need to expand or contract a mass spectrometry dataset
  by adding or removing allowed instrument types (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
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

# configuration-file-modification

## Summary

Modify YAML configuration files to alter instrument allowlists and dataset filtering parameters in FIDDLE preprocessing pipelines, enabling expansion or refinement of training and test compound pools for mass spectrometry molecular formula prediction.

## When to use

When you need to expand or contract a mass spectrometry dataset by adding or removing allowed instrument types (e.g., 'ftms') to the gnps_orbitrap instrument allowlist in the FIDDLE configuration, or when you need to verify that configuration changes produce expected training/test partition sizes (e.g., 28,751 training and 3,195 test compounds for Orbitrap).

## When NOT to use

- Configuration file is not YAML or does not contain an instrument allowlist section
- Dataset preprocessing pipeline is already running; modifications require pipeline restart
- Target dataset size thresholds are unknown or have not been pre-established for the instrument type

## Inputs

- YAML configuration file (e.g., config/fiddle_tcn_orbitrap.yml)
- Instrument allowlist section specifying gnps_orbitrap allowed types

## Outputs

- Modified YAML configuration file with updated instrument allowlist
- Filtered and partitioned Orbitrap spectra dataset with updated compound counts
- Training and test set compound counts for validation

## How to apply

Load the target YAML configuration file (e.g., config/fiddle_tcn_orbitrap.yml) in a text editor or programmatically. Locate the gnps_orbitrap instrument allowlist section and add new instrument type strings (e.g., 'ftms') to the list. Save the modified configuration file. Pass the updated config path to the FIDDLE preprocessing pipeline via the --config_path argument when running dataset filtering. After preprocessing completes, count the resulting training and test set compounds and compare against target thresholds to confirm the allowlist modification achieved the intended dataset expansion.

## Related tools

- **FIDDLE** (Deep learning framework for predicting molecular formulas from MS/MS spectra; executes the dataset preprocessing pipeline that consumes the modified configuration file to filter and partition spectra by instrument type.) — https://github.com/JosieHong/FIDDLE
- **msfiddle** (CLI and Python API wrapper for FIDDLE that accepts configuration file paths via --config_path to control dataset preprocessing and filtering.) — https://github.com/josiehong/msfiddle

## Examples

```
# Load config, modify gnps_orbitrap allowlist to add 'ftms', then run: python run_fiddle.py --config_path ./config/fiddle_tcn_orbitrap.yml --test_data ./input_data.mgf --resume_path ./check_point/fiddle_tcn_orbitrap.pt --result_path ./output_expanded.csv
```

## Evaluation signals

- Modified configuration file is valid YAML syntax and can be parsed without errors
- New instrument type string (e.g., 'ftms') appears in the gnps_orbitrap allowlist section of the saved file
- FIDDLE preprocessing pipeline runs to completion with the updated config path without config-related exceptions
- Resulting training set compound count matches or exceeds the target threshold (e.g., 28,751 for Orbitrap with ftms added)
- Resulting test set compound count matches or exceeds the target threshold (e.g., 3,195 for Orbitrap with ftms added)

## Limitations

- Adding instrument types to the allowlist may introduce spectra with different fragmentation or quality characteristics, potentially requiring model retraining or validation on the expanded dataset.
- No direct evidence is provided in the available text regarding the specific dataset size outcome after the configuration change, so actual compound counts must be manually verified post-preprocessing.
- Configuration changes require full pipeline re-execution; intermediate results are not cached or incrementally updated.
- The YAML schema and valid allowlist values must match the FIDDLE codebase version; incompatible instrument type strings will be silently ignored or cause preprocessing errors.

## Evidence

- [other] Modify the gnps_orbitrap instrument allowlist to include 'ftms' as an additional allowed instrument type.: "Modify the gnps_orbitrap instrument allowlist to include 'ftms' as an additional allowed instrument type."
- [other] Run the FIDDLE dataset preprocessing pipeline with the updated configuration to filter and partition the Orbitrap spectra.: "Run the FIDDLE dataset preprocessing pipeline with the updated configuration to filter and partition the Orbitrap spectra."
- [other] Count the resulting training set compounds (expected: 28,751) and test set compounds (expected: 3,195) and verify both counts match the target values.: "Count the resulting training set compounds (expected: 28,751) and test set compounds (expected: 3,195) and verify both counts match the target values."
- [other] 1. Load the config/fiddle_tcn_orbitrap.yml configuration file. 2. Modify the gnps_orbitrap instrument allowlist to include 'ftms' as an additional allowed instrument type.: "Load the config/fiddle_tcn_orbitrap.yml configuration file. 2. Modify the gnps_orbitrap instrument allowlist to include 'ftms' as an additional allowed instrument type."
- [readme] python run_fiddle.py --test_data ./demo/input_msms.mgf --config_path ./config/fiddle_tcn_orbitrap.yml: "python run_fiddle.py --test_data ./demo/input_msms.mgf --config_path ./config/fiddle_tcn_orbitrap.yml"
