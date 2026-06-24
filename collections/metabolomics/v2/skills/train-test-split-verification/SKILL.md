---
name: train-test-split-verification
description: Use when after applying a configuration fix (e.g., adding an instrument
  type to an allowlist, updating filtering thresholds) to a dataset preprocessing
  pipeline, you need to confirm that the change produces the documented training/test
  split counts.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0091
  tools:
  - msfiddle
  - FIDDLE
  techniques:
  - LC-MS
  license_tier: restricted
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

# train-test-split-verification

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Verify that dataset preprocessing and filtering operations (e.g., instrument allowlist updates) produce expected training and test set sizes by rerunning the splitting workflow and comparing counts against reported baselines. This skill detects when configuration changes or bug fixes have the intended effect on dataset composition.

## When to use

After applying a configuration fix (e.g., adding an instrument type to an allowlist, updating filtering thresholds) to a dataset preprocessing pipeline, you need to confirm that the change produces the documented training/test split counts. This is essential for reproducibility and to catch regressions when the actual counts diverge from the reported baseline.

## When NOT to use

- Input dataset has not undergone any configuration or code changes — use this skill only when you are verifying the effect of a specific fix or update.
- Reported baseline counts are unavailable or unreliable — this skill requires a ground truth to compare against.
- You are designing a dataset split strategy for the first time (use exploratory data analysis instead).

## Inputs

- Raw GNPS spectral dataset (MGF or native format)
- Instrument metadata configuration file
- Instrument allowlist or filtering configuration (YAML or JSON)
- Reported baseline training/test split counts (integers)

## Outputs

- Actual training set compound count (integer)
- Actual test set compound count (integer)
- Verification report (pass/fail) comparing actual vs. reported counts
- Preprocessed dataset files (filtered training and test splits)

## How to apply

Load the raw spectral dataset and instrument metadata used in preprocessing. Update the instrument allowlist configuration (e.g., adding 'ftms' to the gnps_orbitrap category in msfiddle). Re-run the dataset filtering and splitting logic using the preprocessing tool with the updated configuration. Extract the training set compound count and test set compound count from the preprocessed output files. Compare the actual counts against the reported baseline (e.g., 28,751 training and 3,195 test compounds) and verify the difference is zero; if not, investigate which filtering step caused the discrepancy.

## Related tools

- **msfiddle** (Preprocessing and dataset filtering tool used to apply instrument allowlist updates and split the GNPS spectral dataset into training and test sets) — https://github.com/josiehong/msfiddle
- **FIDDLE** (Research codebase containing the full dataset preprocessing, filtering, and splitting logic; provides reference scripts and configurations for reproducibility) — https://github.com/JosieHong/FIDDLE

## Examples

```
python run_fiddle.py --test_data ./gnps_raw.mgf --config_path ./config/fiddle_tcn_orbitrap.yml --result_path ./preprocessed_output.csv --device 0 && grep -c '^' ./preprocessed_output.csv
```

## Evaluation signals

- Actual training set count equals reported baseline (28,751 for Orbitrap dataset)
- Actual test set count equals reported baseline (3,195 for Orbitrap dataset)
- Total compound count (training + test) is consistent across reruns
- No compounds are duplicated or lost between preprocessing runs
- Instrument allowlist configuration change is reflected in the filtering logic (e.g., 'ftms' is now accepted in gnps_orbitrap category)

## Limitations

- The document does not contain explicit reporting of dataset split counts or allowlist methodology, making direct comparison difficult; the workflow must infer steps from msfiddle's source code.
- If the instrument metadata or raw dataset has been updated since the reported baseline, actual counts may diverge for reasons unrelated to the configuration fix.
- Preprocessing pipelines may have randomness (e.g., random train/test splitting); use a fixed random seed to ensure reproducibility.

## Evidence

- [other] Does applying the updated instrument allowlist fix (adding 'ftms' to gnps_orbitrap) to the dataset result in the reported training and test split counts of 28,751 and 3,195 compounds respectively?: "applying the updated instrument allowlist fix (adding 'ftms' to gnps_orbitrap) to the dataset result in the reported training and test split counts of 28,751 and 3,195 compounds respectively"
- [other] Load the raw GNPS spectral dataset and instrument metadata used in FIDDLE preprocessing. Update the instrument allowlist configuration to include 'ftms' in the gnps_orbitrap category. Re-run the dataset filtering and splitting logic with the updated allowlist using msfiddle.: "Load the raw GNPS spectral dataset and instrument metadata used in FIDDLE preprocessing. Update the instrument allowlist configuration to include 'ftms' in the gnps_orbitrap category. Re-run the"
- [other] Extract and verify the training set compound count (expected: 28,751) and test set compound count (expected: 3,195) from the preprocessed output.: "Extract and verify the training set compound count (expected: 28,751) and test set compound count (expected: 3,195) from the preprocessed output"
- [readme] CLI and Python API: [msfiddle](https://github.com/josiehong/msfiddle): "CLI and Python API: msfiddle"
- [readme] msfiddle is the PyPI package for FIDDLE, a deep learning method for chemical formula prediction from tandem mass spectra (MS/MS).: "msfiddle is the PyPI package for FIDDLE, a deep learning method for chemical formula prediction from tandem mass spectra (MS/MS)"
