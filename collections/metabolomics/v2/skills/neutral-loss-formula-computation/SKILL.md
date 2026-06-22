---
name: neutral-loss-formula-computation
description: Use when you have tandem mass spectra with precursor m/z and observed fragment peak m/z values (as mz/intensity pairs), and you need to construct interpretable feature vectors where each axis corresponds to a real chemical entity (peak or neutral loss) rather than a latent dimension.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - ChemEcho
  - Mass Query Language (MassQL)
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
---

# neutral-loss-formula-computation

## Summary

Compute neutral loss m/z values from tandem mass spectra by subtracting each observed fragment peak m/z from the precursor m/z, then enumerate unique neutral loss formulas to populate a feature axis for sparse chemical feature vectors. This enables direct chemical interpretation of fragmentation patterns without latent representations.

## When to use

You have tandem mass spectra with precursor m/z and observed fragment peak m/z values (as mz/intensity pairs), and you need to construct interpretable feature vectors where each axis corresponds to a real chemical entity (peak or neutral loss) rather than a latent dimension. This is essential when training decision trees or regression models for which you must later explain or convert predictions to domain-specific queries (e.g., MassQL).

## When NOT to use

- Input is already a pre-computed feature table or latent representation — neutral loss computation is a feature engineering step, not applicable post-hoc.
- Spectra lack reliable precursor m/z annotation or fragment peak assignments — neutral loss computation depends on accurate m/z calibration.
- Your goal is latent representation learning or black-box prediction without interpretability constraints — neutral loss features sacrifice latent dimensionality for chemical explainability.

## Inputs

- Tandem mass spectra (mz/intensity pairs and precursor m/z per spectrum)
- Input file with fragmentation data (e.g., CSV, mzML, or structured table)

## Outputs

- Sparse feature matrix (spectra × unique neutral loss formulas)
- Neutral loss formula vocabulary (enumerated list of unique m/z values)
- Sparse matrix format (CSV or matrix file suitable for downstream ML)

## How to apply

For each spectrum in your input dataset: (1) extract the precursor m/z and all observed fragment peak m/z values; (2) compute neutral loss as precursor m/z minus each fragment peak m/z; (3) collect all unique neutral loss m/z values across the dataset into a vocabulary. Enumerate each unique neutral loss value as a separate feature axis. For each spectrum, construct a sparse vector where the position corresponding to a neutral loss is marked as present (binary) or weighted by intensity/abundance (count). The resulting feature matrix has spectra as rows and unique neutral loss formulas as columns, directly encoding chemical fragmentation mechanisms. This approach grounds features in chemistry rather than latent space, enabling direct conversion of learned patterns (e.g., decision tree splits) back into mass spectrometry queries.

## Related tools

- **ChemEcho** (End-to-end tool for converting tandem mass spectra into sparse feature vectors via neutral loss and peak enumeration; integrates neutral loss computation into the full workflow) — https://github.com/biorack/chemecho
- **Mass Query Language (MassQL)** (Domain-specific language for describing fragmentation patterns; decision trees trained on neutral loss features can be converted to MassQL queries for deployment and evaluation) — https://mwang87.github.io/MassQueryLanguage_Documentation/

## Evaluation signals

- Neutral loss vocabulary is exhaustive: every unique (precursor m/z − fragment peak m/z) across the dataset appears in the feature list exactly once.
- Sparse matrix dimensions are correct: rows = number of spectra, columns = cardinality of neutral loss vocabulary; no duplicate or missing feature axes.
- Each spectrum's sparse vector contains non-zero entries only at positions corresponding to neutral losses actually observed in that spectrum (binary or intensity-weighted).
- Downstream decision trees trained on neutral loss vectors are convertible to MassQL queries without ambiguity, and individual tree splits correspond to presence/absence of specific neutral loss formulas.
- Feature interpretability check: sample neutral losses and their corresponding chemical mass differences should align with known fragmentation mechanisms (e.g., loss of water = 18.01, loss of ammonia ≈ 17.03).

## Limitations

- Neutral loss computation assumes precursor m/z and fragment peak m/z are accurately calibrated; systematic m/z error propagates into incorrect neutral loss assignments.
- High-dimensional sparse vectors (many unique neutral losses) may lead to sparsity-induced overfitting in small datasets or shallow regression models; tree-based models are more robust.
- Neutral losses do not capture multi-stage fragmentation pathways or rearrangement ions that do not correspond to simple neutral mass differences.
- Enumeration of unique neutral losses can be memory-intensive for large spectral datasets; efficient sparse matrix storage is required.

## Evidence

- [other] Parse fragmentation patterns and compute neutral losses: "Parse fragmentation patterns to identify all observed peaks and compute neutral losses (precursor m/z minus each observed peak m/z)."
- [other] Enumerate unique neutral loss formulas as feature axes: "Enumerate unique peak m/z values and unique neutral loss m/z values as feature axes, creating a feature vocabulary."
- [other] Construct sparse vectors for each spectrum: "For each spectrum, construct a sparse binary or count vector where each position corresponds to a unique peak or neutral loss formula, marking presence or abundance of that feature."
- [readme] ChemEcho represents features as unique peak or neutral loss formulas: "ChemEcho represents features as unique peak or neutral loss formulas. The resulting sparse, high-dimensional feature vectors are well-suited for models that handle sparse inputs, such as regression"
- [intro] Direct chemical interpretation rather than latent representations: "Rather than mapping fragmentation data into a latent space, ChemEcho represents features as unique peak or neutral loss formulas."
