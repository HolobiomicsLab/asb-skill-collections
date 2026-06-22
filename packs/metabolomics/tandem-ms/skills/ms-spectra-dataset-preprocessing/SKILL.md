---
name: ms-spectra-dataset-preprocessing
description: Use when when you have a raw or partially processed MS/MS spectra collection (e.g., GNPS-sourced Orbitrap or Q-TOF spectra in MGF format) and need to (1) restrict to a specific instrument type (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - FIDDLE
  - msfiddle
  techniques:
  - tandem-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# MS/MS Spectra Dataset Preprocessing

## Summary

Prepare and partition tandem mass spectrometry (MS/MS) spectra datasets for deep learning model training by filtering spectra according to instrument type allowlists, quality thresholds, and metadata criteria, then splitting into training and test sets with target compound counts. This skill ensures reproducible dataset composition and verifiable alignment with downstream model training requirements.

## When to use

When you have a raw or partially processed MS/MS spectra collection (e.g., GNPS-sourced Orbitrap or Q-TOF spectra in MGF format) and need to (1) restrict to a specific instrument type (e.g., add 'ftms' to an Orbitrap allowlist), (2) enforce metadata and quality filters, and (3) produce training and test partitions with known compound counts for reproducibility or paper-replication purposes.

## When NOT to use

- Input spectra are already partitioned and verified for a published benchmark (e.g., CASMI 2016, NIST23 official test set); re-preprocessing risks contamination or score inflation.
- You need real-time or streaming prediction on new spectra; preprocessing is a batch operation suitable for dataset curation, not online inference.
- The raw spectra collection already has certified ground truth and is locked for external validation; modifying the instrument allowlist or filters breaks traceability.

## Inputs

- Raw or semi-processed MS/MS spectra collection in MGF format
- FIDDLE configuration file (YAML) specifying instrument allowlist, quality thresholds, and split parameters
- Metadata annotations per spectrum (instrument type, collision energy, precursor m/z, precursor type)

## Outputs

- Preprocessed training set (MGF or internal representation; compound count verified)
- Preprocessed test set (MGF or internal representation; compound count verified)
- Preprocessing report (filtering statistics, counts before/after, instrument-type breakdown)

## How to apply

Load the preprocessing configuration file (e.g., config/fiddle_tcn_orbitrap.yml) that specifies the instrument allowlist, quality thresholds (collision energy, precursor m/z range, spectrum intensity criteria), and train/test split ratios. Modify the instrument allowlist to include or exclude specific instrument types (e.g., add 'ftms' to capture Orbitrap Fourier-transform mass spectrometry data). Run the FIDDLE dataset preprocessing pipeline, which applies filters to exclude spectra missing required MGF fields (TITLE, PRECURSOR_MZ, PRECURSOR_TYPE, COLLISION_ENERGY), normalizes intensities, and partitions the filtered spectra deterministically into training and test sets. Verify the output counts against target values (e.g., 28,751 training and 3,195 test compounds for a canonical Orbitrap dataset) to confirm the configuration change achieved the expected dataset expansion.

## Related tools

- **FIDDLE** (Core preprocessing and dataset pipeline orchestration; executes configuration-driven filtering, intensity normalization, and train/test partitioning of MS/MS spectra.) — https://github.com/JosieHong/FIDDLE
- **msfiddle** (CLI and Python API for FIDDLE; provides command-line interface to run preprocessing and inference with pre-configured MGF input validation and model checkpoint management.) — https://github.com/josiehong/msfiddle

## Examples

```
python run_fiddle.py --test_data ./demo/input_msms.mgf --config_path ./config/fiddle_tcn_orbitrap.yml --resume_path ./check_point/fiddle_tcn_orbitrap.pt --rescore_resume_path ./check_point/fiddle_rescore_orbitrap.pt --result_path ./demo/output_fiddle.csv --device 0
```

## Evaluation signals

- Training set compound count matches or exceeds the target threshold (e.g., 28,751 for Orbitrap after 'ftms' addition); test set count aligns with expected split (e.g., 3,195).
- All retained spectra contain required MGF fields (TITLE, PRECURSOR_MZ, PRECURSOR_TYPE, COLLISION_ENERGY); filtering log shows no data loss due to missing metadata.
- Instrument type distribution in preprocessed dataset reflects the updated allowlist (e.g., increase in 'ftms' spectra after configuration change); before/after instrument histograms confirm expected shift.
- Precursor m/z, collision energy, and intensity statistics fall within configured thresholds; outliers are removed consistently across train and test sets.
- Train/test split is deterministic and reproducible; re-running the same configuration produces identical partition assignments and identical compound counts.

## Limitations

- Configuration file must explicitly define the instrument allowlist; adding or removing instrument types (e.g., 'ftms') requires manual YAML editing and re-run; no dynamic instrument discovery.
- Preprocessing pipeline assumes well-formed MGF input with standardized field names and values; malformed or non-standard entries may be silently dropped or cause pipeline failure.
- Target compound counts (28,751 training, 3,195 test) are specific to the GNPS Orbitrap dataset after 'ftms' inclusion; other datasets or instrument configurations require respecification of expected counts.
- Quality thresholds (collision energy range, precursor m/z bounds, intensity normalization) are dataset- and instrument-specific; applying Orbitrap preprocessing rules to Q-TOF spectra may over- or under-filter and produce misaligned train/test splits.

## Evidence

- [other] Does adding 'ftms' to the gnps_orbitrap instrument allowlist in the FIDDLE configuration expand the Orbitrap dataset to the target size of 28,751 training and 3,195 test compounds?: "Does adding 'ftms' to the gnps_orbitrap instrument allowlist in the FIDDLE configuration expand the Orbitrap dataset to the target size of 28,751 training and 3,195 test compounds?"
- [readme] FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra: "FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra"
- [readme] The required MGF fields are `TITLE`, `PRECURSOR_MZ`, `PRECURSOR_TYPE`, and `COLLISION_ENERGY`: "The required MGF fields are `TITLE`, `PRECURSOR_MZ`, `PRECURSOR_TYPE`, and `COLLISION_ENERGY`"
- [other] Load the config/fiddle_tcn_orbitrap.yml configuration file. 2. Modify the gnps_orbitrap instrument allowlist to include 'ftms' as an additional allowed instrument type. 3. Run the FIDDLE dataset preprocessing pipeline with the updated configuration to filter and partition the Orbitrap spectra.: "Load the config/fiddle_tcn_orbitrap.yml configuration file. 2. Modify the gnps_orbitrap instrument allowlist to include 'ftms' as an additional allowed instrument type. 3. Run the FIDDLE dataset"
- [readme] For the full experimental codebase, see https://github.com/JosieHong/FIDDLE.: "For the full experimental codebase, see https://github.com/JosieHong/FIDDLE."
