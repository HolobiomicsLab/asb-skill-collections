---
name: mass-spectrometry-spectral-preprocessing
description: Use when you have raw mass spectrometry spectra from an unknown analyte or a synthetic compound library and need to feed them into PS2MS or similar deep learning classifiers for NPS detection.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0092
  tools:
  - PS2MS
  - NEIMS
  - DeepEI
derived_from:
- doi: 10.1021/acs.analchem.3c05019
  title: ps2ms
evidence_spans:
- jhhung/PS2MS
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ps2ms_cq
    doi: 10.1021/acs.analchem.3c05019
    title: ps2ms
  dedup_kept_from: coll_ps2ms_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c05019
  all_source_dois:
  - 10.1021/acs.analchem.3c05019
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-spectral-preprocessing

## Summary

Prepare raw mass spectrometry spectral data into the normalized format required by deep learning models for chemical classification and identity matching. This preprocessing step ensures spectral inputs conform to model expectations before inference or similarity scoring.

## When to use

You have raw mass spectrometry spectra from an unknown analyte or a synthetic compound library and need to feed them into PS2MS or similar deep learning classifiers for NPS detection. Apply this skill when spectrum files require normalization and structural alignment to match the format specifications documented in the model repository.

## When NOT to use

- Spectra are already in the exact format and normalization expected by the PS2MS model checkpoint
- Working only with chemical structure enumeration without needing mass spectrum prediction or matching
- Input is a pre-computed feature embedding or fingerprint vector rather than raw or semi-raw spectral data

## Inputs

- raw mass spectrometry spectra (msp files or equivalent)
- peak list with m/z and intensity values
- optionally, chemical fingerprints from DeepEI or equivalent feature extraction

## Outputs

- normalized spectral matrix in model-expected format
- preprocessed spectrum files ready for deep learning inference
- spectrum metadata (compound ID, molecular weight, core structure reference)

## How to apply

Load raw mass spectra (typically in msp or similar format) and apply the preprocessing pipeline specified by PS2MS: normalize intensity values according to model specifications, verify peak alignment, ensure the spectral matrix dimensions and data types match model input requirements, and optionally merge chemical fingerprints (e.g., from DeepEI) into the spectrum representation. The normalization and formatting must be consistent with the training data pipeline so that inference produces valid predictions. Validate that output spectra pass shape and range checks before submission to the deep learning model.

## Related tools

- **NEIMS** (Predicts mass spectra for synthetic compounds in the PS2MS database; output spectra require the same preprocessing as unknown analyte spectra for consistent similarity scoring) — https://github.com/jhhung/PS2MS/tree/main/neims
- **DeepEI** (Predicts chemical fingerprints that are merged into spectral representations; fingerprint output must be normalized and integrated into the spectrum file format) — https://github.com/jhhung/PS2MS/tree/main/DeepEI
- **PS2MS** (Main deep learning system that consumes preprocessed spectra and fingerprints for NPS classification and similarity matching) — https://github.com/jhhung/PS2MS

## Evaluation signals

- Output spectral matrix dimensions and data types match the model input specification (shape, dtype, value range checks)
- Normalized intensity values fall within expected range (e.g., [0, 1] or model-specified bounds) with no NaN or inf values
- Spectral preprocessing produces deterministic, reproducible output when applied to the same raw input
- Preprocessed spectra from the synthetic database and unknown analyte are in identical format, enabling valid similarity score computation in downstream matching step
- Optional: Fingerprints successfully merge into msp files without format errors or data loss

## Limitations

- Preprocessing pipeline details are not exhaustively documented in the README; exact normalization constants and spectral matrix format must be inferred from repository code or supplementary materials
- Requires rdkit and specific Python version (3.6.9+) and dependencies (g++-10, CMake 3.16.0+) to run full pipeline; compatibility with newer versions not guaranteed
- If raw spectra deviate significantly from training data distribution (e.g., different ionization mode, instrument calibration), preprocessing alone may not correct for domain shift
- No changelog documented; preprocessing logic may change between repository commits without notice

## Evidence

- [other] Prepare mass spectrometry spectral data in the format expected by the model (structure and normalization as specified in the repository): "Prepare mass spectrometry spectral data in the format expected by the model (structure and normalization as specified in the repository)."
- [readme] The system also use the function of DeepEI to calculate the fingerprint of compounds of synthetic database. The system merges the fingerprint into the msp file.: "The system also use the function of DeepEI to calculate the fingerprint of compounds of synthetic database. The system merges the fingerprint into the msp file."
- [readme] PS2MS calculates the integrated similarity scores(SMSF) between the unknown analyte and the derivatives from synthetic database: "PS2MS calculates the integrated similarity scores(SMSF) between the unknown analyte and the derivatives from synthetic database and yields a list of potential NPS identities for the analyte."
