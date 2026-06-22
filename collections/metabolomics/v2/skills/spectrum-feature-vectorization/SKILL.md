---
name: spectrum-feature-vectorization
description: Use when you have raw mass spectrometry spectra (peak lists or intensity arrays) that must be fed into a pre-trained deep learning model for substance classification (e.g., PS²MS for NPS detection).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_3372
  tools:
  - PS2MS
  - PS²MS
  - NEIMS
  - DeepEI
  techniques:
  - mass-spectrometry
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
  - build: coll_ps2ms
    doi: 10.1021/acs.analchem.3c05019
    title: ps2ms
  dedup_kept_from: coll_ps2ms
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c05019
  all_source_dois:
  - 10.1021/acs.analchem.3c05019
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectrum-feature-vectorization

## Summary

Convert raw mass spectrometry spectra into tokenized numerical vectors suitable for deep learning inference by normalizing m/z and intensity pairs according to model input schema. This preprocessing step transforms unstructured spectral data into the fixed-format feature matrices required by PS²MS and similar neural network classifiers.

## When to use

You have raw mass spectrometry spectra (peak lists or intensity arrays) that must be fed into a pre-trained deep learning model for substance classification (e.g., PS²MS for NPS detection). The model expects fixed-dimensional numerical inputs (vectorized m/z–intensity pairs), but your input is in raw or partially processed form.

## When NOT to use

- Input is already a trained or fitted model checkpoint — use this skill to prepare *inputs to* the model, not the model itself.
- Your goal is exploratory data visualization or statistical summary — vectorization prepares data for neural networks, not for human-readable reporting.
- The spectra come from a different instrument or chemical domain with incompatible normalization or m/z calibration — vectorization assumes the input adheres to PS²MS training assumptions (e.g., NPS mass spectrometry data).

## Inputs

- Raw mass spectrometry spectra (peak lists with m/z and intensity values)
- Processed feature matrices or partially normalized spectra
- Input schema specification for PS²MS or equivalent deep learning model

## Outputs

- Tokenized and vectorized feature matrices (m/z–intensity pairs in numerical form)
- Fixed-dimensional numerical arrays compatible with deep learning model input
- Preprocessed spectra ready for forward inference

## How to apply

Load raw mass spectrometry input data in a format compatible with PS²MS (raw spectra or processed feature matrices). Tokenize and vectorize the m/z (mass-to-charge) and intensity pairs according to PS²MS normalization and feature extraction requirements. Apply any required normalization (e.g., intensity scaling, m/z binning) to align with the model's training schema. The resulting feature matrix should have consistent dimensionality across all spectra to match the deep learning model's input layer. Verify that the vectorized output can be loaded and ingested by the downstream inference pipeline without shape mismatches or missing-value errors.

## Related tools

- **PS²MS** (Target deep learning system that receives vectorized spectra as input for NPS classification inference) — https://github.com/jhhung/PS2MS
- **NEIMS** (Generates predicted mass spectra for synthetic NPS database compounds; used in PS²MS pipeline to create reference spectra that are themselves vectorized for fingerprint comparison)
- **DeepEI** (Predicts chemical fingerprints from vectorized spectra; processes the same m/z–intensity inputs to extract fingerprint features used in similarity scoring)

## Evaluation signals

- Vectorized feature matrices have consistent shape across all input spectra (e.g., all rows have the same dimensionality) matching the PS²MS model's expected input layer size
- Numerical values fall within the range used during model training (e.g., normalized intensity [0, 1] or standardized m/z bins); check for out-of-range or NaN values
- Forward inference pass on the vectorized data completes without shape mismatch or input validation errors
- Resulting predictions (NPS class labels and confidence scores) are generated and fall within expected probability ranges [0, 1]
- Comparison of predictions on the same spectrum before/after vectorization is stable (i.e., vectorization does not introduce random variation or lossy transformation)

## Limitations

- Vectorization assumes input spectra conform to PS²MS training data characteristics (mass spectrometry instruments, NPS chemical space, m/z and intensity calibration); spectra from different instruments or non-NPS compounds may require domain-specific re-normalization
- No changelog or version history is available in the PS²MS repository, so reproducibility of the exact vectorization scheme across different releases may be uncertain
- The article and README do not explicitly specify the exact normalization formula, tokenization scheme (e.g., bin width, m/z range), or handling of missing/zero-intensity peaks; practitioners must infer requirements from the PS²MS source code or supplementary materials

## Evidence

- [other] Load mass spectrometry input data (raw spectra or processed feature matrices) compatible with PS2MS input schema.: "Load mass spectrometry input data (raw spectra or processed feature matrices) compatible with PS2MS input schema."
- [other] Preprocess spectra according to PS2MS normalization and feature extraction requirements (tokenization/vectorization of m/z and intensity pairs).: "Preprocess spectra according to PS2MS normalization and feature extraction requirements (tokenization/vectorization of m/z and intensity pairs)."
- [readme] PS²MS builds a synthetic NPS database by enumerating possible derivatives based on the core structure of a preselected illicit drug.: "PS²MS builds a synthetic NPS database by enumerating possible derivatives based on the core structure of a preselected illicit drug."
- [readme] The system leverages two deep learning tools, NEIMS and DeepEI, to generate mass spectra and chemical fingerprints, respectively.: "The system leverages two deep learning tools, NEIMS and DeepEI, to generate mass spectra and chemical fingerprints, respectively."
