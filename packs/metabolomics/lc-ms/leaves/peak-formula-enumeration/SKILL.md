---
name: peak-formula-enumeration
description: Use when when you have tandem mass spectra (mz/intensity pairs with precursor m/z) and need to train interpretable machine learning models—particularly decision trees or regression models—where each feature must correspond to a concrete chemical entity (peak or neutral loss) rather than a latent.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3375
  tools:
  - ChemEcho
  - Mass Query Language (MassQL)
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.5c02591
  title: ChemEcho
- doi: 10.1145/2939672.2939778
  title: ''
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_chemecho_cq
    doi: 10.1021/acs.analchem.5c02591
    title: ChemEcho
  dedup_kept_from: coll_chemecho_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c02591
  all_source_dois:
  - 10.1021/acs.analchem.5c02591
  - 10.1145/2939672.2939778
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peak-formula-enumeration

## Summary

Enumerate unique peak m/z values and neutral loss formulas from tandem mass spectra to create a feature vocabulary for sparse vector representation. This foundational step converts raw fragmentation patterns into interpretable chemical features suitable for machine learning.

## When to use

When you have tandem mass spectra (mz/intensity pairs with precursor m/z) and need to train interpretable machine learning models—particularly decision trees or regression models—where each feature must correspond to a concrete chemical entity (peak or neutral loss) rather than a latent representation.

## When NOT to use

- Input is already a feature table or pre-computed feature matrix; skip directly to model training.
- You require latent or distributed representations of spectra; ChemEcho features are sparse and directly interpretable, not low-rank embeddings.
- Your workflow demands real-valued spectral intensities as features; this skill produces binary presence/absence or count vectors, not intensity-weighted features.

## Inputs

- tandem mass spectra (mz/intensity pairs)
- precursor m/z values
- mass spectrometry data file (e.g., mzML, mzXML, or proprietary format with spectral metadata)

## Outputs

- unique peak m/z list
- unique neutral loss m/z list
- feature vocabulary (enumerated peak and neutral loss formulas)
- feature axis mapping (position → formula)

## How to apply

Load tandem mass spectra data containing observed peak m/z values and precursor m/z. For each spectrum, compute neutral losses by subtracting each observed peak m/z from the precursor m/z. Enumerate all unique peak m/z values across the dataset as one feature axis, and all unique neutral loss m/z values as another. Combine these into a unified feature vocabulary where each axis position corresponds to a specific peak or neutral loss formula. This vocabulary then serves as the reference for constructing sparse binary or count vectors in downstream feature vectorization. The rationale is that explicit, interpretable features enable direct conversion of trained decision trees to MassQL queries for deployment and validation of fragmentation criteria.

## Related tools

- **ChemEcho** (Framework for converting tandem mass spectra into sparse feature vectors via peak and neutral loss enumeration and vectorization) — https://github.com/biorack/chemecho
- **Mass Query Language (MassQL)** (Domain-specific language for describing fragmentation patterns; decision trees trained on enumerated peak/neutral-loss features can be directly converted to MassQL queries) — https://mwang87.github.io/MassQueryLanguage_Documentation/

## Evaluation signals

- Verify that all observed peak m/z values in the input spectra appear in the enumerated peak vocabulary; no peaks should be silently dropped.
- Verify that computed neutral losses (precursor m/z − observed peak m/z) are non-negative and physically plausible; check for computational errors or malformed precursor/peak pairs.
- Confirm that the feature vocabulary is exhaustive and non-redundant: each unique peak and neutral loss formula appears exactly once in the final axis mapping.
- Check that sparse vectors constructed from the vocabulary have non-zero entries only at positions corresponding to peaks/losses actually observed in each spectrum.
- Validate that downstream decision trees can be converted to MassQL queries with selection criteria (peaks/losses present/absent) that are unambiguously interpretable.

## Limitations

- High-dimensional sparse feature vectors can become unwieldy if spectra are very diverse; feature selection or filtering may be necessary before model training.
- Neutral loss computation assumes accurate precursor m/z annotation; erroneous or missing precursor values will introduce spurious or missing neutral loss features.
- The method does not account for isotope patterns or charge state variation; all m/z values are treated as independent features.
- Enumeration-based vocabulary is static once created; unseen peaks or neutral losses in new spectra will not be represented unless the vocabulary is recomputed.

## Evidence

- [other] Parse fragmentation patterns to identify all observed peaks and compute neutral losses (precursor m/z minus each observed peak m/z).: "Parse fragmentation patterns to identify all observed peaks and compute neutral losses (precursor m/z minus each observed peak m/z)."
- [other] Enumerate unique peak m/z values and unique neutral loss m/z values as feature axes, creating a feature vocabulary.: "Enumerate unique peak m/z values and unique neutral loss m/z values as feature axes, creating a feature vocabulary."
- [readme] ChemEcho represents features as unique peak or neutral loss formulas. The resulting sparse, high-dimensional feature vectors are well-suited for models that handle sparse inputs, such as regression and tree-based architectures.: "ChemEcho represents features as unique peak or neutral loss formulas. The resulting sparse, high-dimensional feature vectors are well-suited for models that handle sparse inputs, such as regression"
- [readme] Using ChemEcho vectors, we can train decision trees which are able to be directly converted to MassQL for straightforward deployment, and to more easily evaluate the prediction criteria.: "Using ChemEcho vectors, we can train decision trees which are able to be directly converted to MassQL for straightforward deployment, and to more easily evaluate the prediction criteria."
- [readme] ChemEcho is a tool for converting tandem mass spectra into sparse feature vectors, enabling the training of interpretable machine learning models.: "ChemEcho is a tool for converting tandem mass spectra into sparse feature vectors, enabling the training of interpretable machine learning models."
