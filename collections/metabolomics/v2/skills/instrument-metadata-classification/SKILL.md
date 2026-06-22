---
name: instrument-metadata-classification
description: Use when when preprocessing a heterogeneous spectral library (e.g., GNPS public library) that contains spectra from multiple instrument types, and you need to partition data by a single instrument class to train or evaluate a formula-prediction model.
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

# instrument-metadata-classification

## Summary

Classify and filter tandem mass spectra by instrument type using metadata allowlists to ensure training and test datasets contain only spectra from intended mass analyzers (e.g., Orbitrap, Q-TOF). This skill is essential for reproducible model training and evaluation when source datasets mix multiple instrument types.

## When to use

When preprocessing a heterogeneous spectral library (e.g., GNPS public library) that contains spectra from multiple instrument types, and you need to partition data by a single instrument class to train or evaluate a formula-prediction model. Specifically, when the instrument metadata field contains ambiguous or incomplete entries that fail to match the target instrument category, requiring an updated allowlist to recover missing valid records.

## When NOT to use

- Input dataset is already homogeneous (single instrument type confirmed); filtering adds no value and risks data loss.
- Instrument metadata is absent or unstructured; allowlist-based classification cannot proceed without a reliable metadata field.
- The goal is instrument-agnostic formula prediction; mixing multiple instruments may be intentional for robustness.

## Inputs

- Raw spectral dataset in MGF format with TITLE, PRECURSOR_MZ, PRECURSOR_TYPE, COLLISION_ENERGY fields
- Instrument metadata table or field mapping (e.g., spectrum origin to instrument class)
- Instrument allowlist configuration (YAML or JSON) specifying valid metadata values per instrument category

## Outputs

- Filtered spectral dataset (MGF or structured format) containing only spectra matching the allowlist
- Training set partition (compound count and spectrum count)
- Test set partition (compound count and spectrum count)
- Filtering audit log (count of records removed, allowlist matches applied)

## How to apply

Load the raw spectral dataset and its associated instrument metadata (e.g., from GNPS). Define or update an instrument allowlist for your target class (e.g., add 'ftms' to the gnps_orbitrap category to capture Fourier Transform Mass Spectrometry records previously missed). Apply the filtering logic using the preprocessing tool (msfiddle) to exclude spectra whose instrument metadata do not match any entry in the allowlist. Re-run the dataset splitting logic (train/test partition) on the filtered dataset. Verify the resulting training and test set sizes match expected counts (e.g., 28,751 training / 3,195 test compounds for Orbitrap) to confirm the allowlist fix recovered the intended records.

## Related tools

- **msfiddle** (Preprocessing and filtering tool that applies instrument allowlists and partitions spectra into training and test sets) — https://github.com/josiehong/msfiddle
- **FIDDLE** (Full research codebase for model training and evaluation; contains dataset filtering and splitting scripts) — https://github.com/JosieHong/FIDDLE

## Examples

```
python run_fiddle.py --test_data ./filtered_orbitrap.mgf --config_path ./config/fiddle_tcn_orbitrap.yml --resume_path ./check_point/fiddle_tcn_orbitrap.pt --result_path ./output_filtered.csv --device 0
```

## Evaluation signals

- Filtered dataset row count matches the sum of expected training and test partition sizes (e.g., 28,751 + 3,195 = 31,946 total compounds).
- Allowlist-matched records have non-null, consistent instrument metadata values; no spectra with unrecognized instrument codes remain.
- Training/test split ratio is consistent with the original design (e.g., ~90% train, ~10% test or as specified).
- Audit log reports the number of records excluded and the specific allowlist entries that matched, confirming the fix was applied.
- Downstream model training converges and produces baseline metrics consistent with published results.

## Limitations

- Allowlist effectiveness depends on metadata consistency in the source dataset; typos, abbreviations, or non-standard naming will cause valid spectra to be filtered out.
- The fix is instrument-specific; adding 'ftms' to gnps_orbitrap does not generalize to other instruments (Q-TOF, MALDI, etc.) without separate allowlist updates.
- Dataset partitioning reproducibility requires seed control; random splits without fixed seeds will yield different test/train compositions across runs.
- The approach assumes the allowlist is authoritative; incorrect or incomplete allowlists will silently bias the dataset toward unintended instrument subsets.

## Evidence

- [other] Does applying the updated instrument allowlist fix (adding 'ftms' to gnps_orbitrap) to the dataset result in the reported training and test split counts of 28,751 and 3,195 compounds respectively?: "Does applying the updated instrument allowlist fix (adding 'ftms' to gnps_orbitrap) to the dataset result in the reported training and test split counts of 28,751 and 3,195 compounds respectively?"
- [other] Update the instrument allowlist configuration to include 'ftms' in the gnps_orbitrap category. Re-run the dataset filtering and splitting logic with the updated allowlist using msfiddle.: "Update the instrument allowlist configuration to include 'ftms' in the gnps_orbitrap category. Re-run the dataset filtering and splitting logic with the updated allowlist using msfiddle."
- [readme] FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra. This repository contains the full research codebase for model training, evaluation, and paper reproduction.: "FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra. This repository contains the full research codebase for model training, evaluation, and paper reproduction."
- [readme] All scripts should be run from the repository root (`FIDDLE/`). | Script | Description | running_scripts/train_released_models.sh | Train TCN and rescore models for both Orbitrap and Q-TOF: "Train TCN and rescore models for both Orbitrap and Q-TOF"
