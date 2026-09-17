---
name: compound-count-verification
description: Use when after modifying a FIDDLE configuration file to add or remove
  instrument types from the allowlist (e.g., adding 'ftms' to gnps_orbitrap), run
  the full preprocessing pipeline and validate that the resulting training and test
  set sizes match documented targets.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - FIDDLE
  - msfiddle
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
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

# compound-count-verification

## Summary

Verify that dataset preprocessing with modified instrument allowlist filters produce the expected number of training and test compounds. This skill validates reproducibility of dataset partitioning after configuration changes to instrument inclusion rules.

## When to use

After modifying a FIDDLE configuration file to add or remove instrument types from the allowlist (e.g., adding 'ftms' to gnps_orbitrap), run the full preprocessing pipeline and validate that the resulting training and test set sizes match documented targets. Use this skill to confirm that configuration changes propagate correctly through the filtering and partitioning stages.

## When NOT to use

- When the baseline (unmodified) configuration has never been run or its expected counts are unknown—establish baseline counts first.
- When the input spectrum dataset itself has changed between runs—verify data provenance and versioning before comparing counts.
- When the modification to the allowlist is syntactically invalid or the YAML file is malformed—validate configuration file structure before running preprocessing.

## Inputs

- FIDDLE YAML configuration file with instrument allowlist (e.g., config/fiddle_tcn_orbitrap.yml)
- MS/MS spectrum dataset in GNPS or similar format
- Preprocessed or raw spectral records filtered by the modified configuration

## Outputs

- Training set compound count (integer)
- Test set compound count (integer)
- Boolean pass/fail verification against target counts
- Dataset partitioning report or log summarizing filtering steps applied

## How to apply

Load the modified FIDDLE YAML configuration file (e.g., config/fiddle_tcn_orbitrap.yml) with the updated gnps_orbitrap instrument allowlist. Execute the dataset preprocessing pipeline to filter spectra against the new allowlist and partition into training and test sets. Count the resulting compounds in each set using the output dataset objects or CSV logs. Compare the training set count (e.g., 28,751 expected) and test set count (e.g., 3,195 expected) against the documented targets. If counts match, the configuration change and preprocessing chain are working correctly; if not, investigate whether the allowlist was properly loaded, whether all preprocessing steps executed, and whether any filtering steps inadvertently removed additional records.

## Related tools

- **FIDDLE** (Deep learning pipeline for molecular formula prediction; provides configuration, preprocessing, dataset partitioning, and model training infrastructure) — https://github.com/JosieHong/FIDDLE
- **msfiddle** (CLI and Python API wrapper around FIDDLE; used for running prediction and accessing preprocessing workflows via command-line or code) — https://github.com/josiehong/msfiddle

## Evaluation signals

- Training set compound count equals or closely matches the documented target (e.g., 28,751 for expanded Orbitrap dataset).
- Test set compound count equals or closely matches the documented target (e.g., 3,195 for expanded Orbitrap dataset).
- No errors or warnings in preprocessing logs indicating failed filter operations or malformed records.
- Instrument allowlist modification is visible in the loaded configuration and is applied during spectrum filtering (traceable in debug logs or filter statistics).
- Total compound count (training + test) is consistent with the expected data availability after instrument filtering.

## Limitations

- The exact expected counts depend on the specific GNPS dataset version and any intervening data cleaning or deduplication rules; counts may vary if the underlying spectrum repository is updated.
- Instrument allowlist changes may interact with other filters in the configuration (e.g., mass range, collision energy, charge state), so unexpected count changes may reflect interactions rather than allowlist logic alone.
- No direct verification method is provided in the article; counts must be extracted from dataset objects or preprocessing logs, which may require custom parsing or inspection of intermediate files.
- The article does not provide explicit verification of the 28,751 / 3,195 target counts being met after adding 'ftms', so this skill documents the verification process rather than a confirmed outcome.

## Evidence

- [other] Does adding 'ftms' to the gnps_orbitrap instrument allowlist in the FIDDLE configuration expand the Orbitrap dataset to the target size of 28,751 training and 3,195 test compounds?: "Does adding 'ftms' to the gnps_orbitrap instrument allowlist in the FIDDLE configuration expand the Orbitrap dataset to the target size of 28,751 training and 3,195 test compounds?"
- [other] Modify the gnps_orbitrap instrument allowlist to include 'ftms' as an additional allowed instrument type. 3. Run the FIDDLE dataset preprocessing pipeline with the updated configuration to filter and partition the Orbitrap spectra. 4. Count the resulting training set compounds (expected: 28,751) and test set compounds (expected: 3,195) and verify both counts match the target values.: "Modify the gnps_orbitrap instrument allowlist to include 'ftms' as an additional allowed instrument type. 3. Run the FIDDLE dataset preprocessing pipeline with the updated configuration to filter and"
- [readme] All scripts should be run from the repository root (`FIDDLE/`). | Script | Description | |---|---| | `running_scripts/experiments_test_benchmark.sh` | Evaluate on external benchmarks (CASMI 2016, CASMI 2017, EMBL-MCF 2.0) |: "All scripts should be run from the repository root (`FIDDLE/`). | Script | Description"
- [readme] python run_fiddle.py --test_data ./demo/input_msms.mgf --config_path ./config/fiddle_tcn_orbitrap.yml --resume_path ./check_point/fiddle_tcn_orbitrap.pt --rescore_resume_path ./check_point/fiddle_rescore_orbitrap.pt --result_path ./demo/output_fiddle.csv --device 0: "python run_fiddle.py --test_data ./demo/input_msms.mgf --config_path ./config/fiddle_tcn_orbitrap.yml --resume_path ./check_point/fiddle_tcn_orbitrap.pt"
