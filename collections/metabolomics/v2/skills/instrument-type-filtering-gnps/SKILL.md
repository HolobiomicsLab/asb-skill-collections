---
name: instrument-type-filtering-gnps
description: Use when you have a large, mixed-instrument GNPS spectral dataset and
  need to create an instrument-specific training set for FIDDLE or similar deep learning
  models. Use this skill when your configuration file specifies an instrument allowlist
  (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
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

# instrument-type-filtering-gnps

## Summary

Filter MS/MS spectra from GNPS datasets by instrument type (e.g., adding 'ftms' to an allowlist) to curate instrument-specific training and test partitions for deep learning models. This skill is essential when preprocessing heterogeneous spectral databases to match model instrument specificity and achieve target dataset sizes.

## When to use

You have a large, mixed-instrument GNPS spectral dataset and need to create an instrument-specific training set for FIDDLE or similar deep learning models. Use this skill when your configuration file specifies an instrument allowlist (e.g., gnps_orbitrap) but the resulting dataset size falls short of your target (e.g., fewer than 28,751 training compounds), suggesting the allowlist is too restrictive. Apply this skill to expand the allowlist by adding related instrument types (e.g., 'ftms' for Orbitrap high-resolution instruments) and verify the expanded dataset meets your target compound counts.

## When NOT to use

- Your dataset already contains only a single instrument type and does not require filtering by instrument.
- You are working with non-GNPS spectral data or data without instrument type metadata; the skill is GNPS-specific.
- Your target dataset size is already achieved with the current allowlist; expanding further may introduce unwanted instrumental heterogeneity that degrades model performance.

## Inputs

- FIDDLE configuration YAML file (e.g., config/fiddle_tcn_orbitrap.yml) specifying instrument allowlist
- Raw GNPS spectral dataset (MGF or mzML format, unfiltered by instrument type)
- Target dataset size specification (e.g., 28,751 training compounds, 3,195 test compounds)

## Outputs

- Filtered and partitioned training set of MS/MS spectra matching expanded instrument allowlist
- Filtered and partitioned test set of MS/MS spectra matching expanded instrument allowlist
- Count of training set compounds (should match or exceed target, e.g., 28,751)
- Count of test set compounds (should match or exceed target, e.g., 3,195)
- Updated FIDDLE configuration YAML with expanded gnps_orbitrap instrument allowlist

## How to apply

Load the FIDDLE configuration YAML file (e.g., config/fiddle_tcn_orbitrap.yml) that specifies the gnps_orbitrap instrument allowlist. Identify the current allowlist and determine which additional instrument identifiers (e.g., 'ftms') should be included based on instrumental compatibility (e.g., Fourier-transform mass spectrometers related to Orbitrap). Modify the allowlist in the configuration to include the additional instrument type(s). Run the FIDDLE dataset preprocessing pipeline with the updated configuration to filter and partition the raw GNPS spectra by the expanded instrument allowlist. After preprocessing completes, count the resulting training set compounds and test set compounds and verify both counts match or exceed your target values (e.g., 28,751 training and 3,195 test). If counts still fall short, iteratively add further compatible instrument types or review GNPS data availability.

## Related tools

- **FIDDLE** (Deep learning framework for molecular formula prediction from MS/MS spectra; runs the preprocessing pipeline that applies instrument-type filtering to partition GNPS data) — https://github.com/JosieHong/FIDDLE
- **msfiddle** (CLI and Python API for FIDDLE; provides command-line access to model prediction and configuration management) — https://github.com/josiehong/msfiddle

## Examples

```
python run_fiddle.py --test_data ./demo/input_msms.mgf --config_path ./config/fiddle_tcn_orbitrap.yml --resume_path ./check_point/fiddle_tcn_orbitrap.pt --rescore_resume_path ./check_point/fiddle_rescore_orbitrap.pt --result_path ./demo/output_fiddle.csv --device 0
```

## Evaluation signals

- Training set compound count after preprocessing equals or exceeds the target (e.g., ≥28,751 compounds)
- Test set compound count after preprocessing equals or exceeds the target (e.g., ≥3,195 compounds)
- Configuration YAML file successfully loads without parsing errors and the expanded allowlist is present in the gnps_orbitrap section
- No loss of valid spectra; the filtering operation removes only spectra with instrument types outside the expanded allowlist
- Model trained on the expanded dataset maintains or improves prediction accuracy on external benchmarks (e.g., CASMI 2016/2017) compared to models trained on smaller, more restrictive instrument sets

## Limitations

- Adding incompatible or distant instrument types (e.g., ion traps or TOF instruments to an Orbitrap model) may introduce spectral heterogeneity that degrades model performance; careful instrument compatibility assessment is required.
- GNPS data availability for specific instrument types varies; expanding the allowlist may not yield expected dataset growth if GNPS has limited data for the added instruments.
- The skill addresses only dataset size and instrument filtering; it does not handle other preprocessing steps such as quality filtering, mass accuracy calibration, or charge state normalization.
- No direct mechanism to verify that added instrument types (e.g., 'ftms') are correctly mapped to GNPS metadata; manual review of a sample of filtered spectra is recommended.

## Evidence

- [other] Does adding 'ftms' to the gnps_orbitrap instrument allowlist in the FIDDLE configuration expand the Orbitrap dataset to the target size of 28,751 training and 3,195 test compounds?: "Does adding 'ftms' to the gnps_orbitrap instrument allowlist in the FIDDLE configuration expand the Orbitrap dataset to the target size of 28,751 training and 3,195 test compounds?"
- [other] Modify the gnps_orbitrap instrument allowlist to include 'ftms' as an additional allowed instrument type. Run the FIDDLE dataset preprocessing pipeline with the updated configuration to filter and partition the Orbitrap spectra. Count the resulting training set compounds (expected: 28,751) and test set compounds (expected: 3,195): "Modify the gnps_orbitrap instrument allowlist to include 'ftms' as an additional allowed instrument type. Run the FIDDLE dataset preprocessing pipeline with the updated configuration to filter and"
- [readme] FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra: "FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra"
- [readme] Load the config/fiddle_tcn_orbitrap.yml configuration file. The input format is mgf, where title, precursor_mz, precursor_type, collision_energy fields are required.: "Load the config/fiddle_tcn_orbitrap.yml configuration file. The input format is mgf, where title, precursor_mz, precursor_type, collision_energy fields are required."
