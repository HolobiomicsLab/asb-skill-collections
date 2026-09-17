---
name: tandem-mass-spectra-fragmentation-parsing
description: Use when when you have raw tandem mass spectra in mz/intensity format
  with precursor m/z values, and need to extract all fragmentation features (observed
  peaks and neutral losses) as a foundation for building interpretable machine learning
  models.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Mass Query Language (MassQL)
  - ChemEcho
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.5c02591
  title: ChemEcho
- doi: 10.1145/2939672.2939778
  title: ''
evidence_spans:
- The Mass Query Language (MassQL) is a domain specific language used to describe
  fragmentation patterns
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

# Tandem Mass Spectra Fragmentation Parsing

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Parse tandem mass spectra (mz/intensity pairs and precursor m/z) to identify all observed peaks and compute neutral losses, establishing the feature vocabulary for sparse chemical feature vector construction. This parsing step is essential for converting raw fragmentation data into interpretable, directly-chemical feature representations.

## When to use

When you have raw tandem mass spectra in mz/intensity format with precursor m/z values, and need to extract all fragmentation features (observed peaks and neutral losses) as a foundation for building interpretable machine learning models. Use this skill when interpretability—not latent representation—is the goal, and when downstream models (e.g., decision trees) will benefit from explicit chemical feature semantics.

## When NOT to use

- Input data already contains pre-computed latent embeddings or dimensionality-reduced features—parsing would be redundant.
- Fragmentation patterns are unknown or precursor m/z values are missing—neutral loss computation requires both observed peaks and precursor mass.
- The analysis goal requires hidden or abstract feature representations rather than direct chemical interpretation.

## Inputs

- tandem mass spectra (mz/intensity pairs)
- precursor m/z values
- fragmentation data file (CSV, mzML, or similar mass spectrometry format)

## Outputs

- unique peak m/z vocabulary
- unique neutral loss m/z vocabulary
- sparse feature matrix (spectra × features)
- sparse binary or count vectors per spectrum

## How to apply

Load tandem mass spectra data containing mz/intensity pairs and precursor m/z from your input file (e.g., CSV or mzML). For each spectrum, identify all observed peak m/z values and compute neutral losses by subtracting each observed peak m/z from the precursor m/z. Enumerate both the unique observed peaks and unique neutral loss m/z values to construct a feature vocabulary. For each spectrum, construct a sparse binary or count vector where each position corresponds to a unique peak or neutral loss formula, marking the presence or abundance of that feature. This direct chemical interpretation—rather than a latent encoding—ensures that downstream models trained on these vectors remain explainable and can be directly converted to domain-specific queries (e.g., MassQL).

## Related tools

- **ChemEcho** (Converts parsed tandem mass spectra into sparse feature vectors and trains interpretable decision tree models on chemical features) — https://github.com/biorack/chemecho
- **Mass Query Language (MassQL)** (Domain-specific language used to describe and query fragmentation patterns; decision tree paths trained on ChemEcho vectors are converted to MassQL for deployment) — https://mwang87.github.io/MassQueryLanguage_Documentation/

## Evaluation signals

- All observed peaks in the input spectra are present in the unique peak vocabulary; no peaks are omitted or duplicated.
- Neutral loss values are correctly computed as (precursor m/z − observed peak m/z) for every peak; spot-check at least 3 spectra manually.
- Sparse feature vectors have non-zero entries only at positions corresponding to peaks/neutral losses actually observed in that spectrum.
- The feature vocabulary size and sparsity statistics (e.g., % non-zero entries) are consistent with the scale of the input data and fragmentation complexity.
- Downstream decision trees or regression models trained on the resulting vectors achieve interpretable paths that can be converted to human-readable MassQL queries.

## Limitations

- Parsing accuracy depends on input data quality; missing or noisy mz/intensity pairs or incorrect precursor m/z values will propagate errors into the feature vocabulary.
- Neutral loss computation assumes precursor m/z is accurate; systematic mass calibration errors will skew all computed losses.
- Very large spectral datasets may generate high-cardinality feature vocabularies, making the resulting sparse matrices memory-intensive or computationally expensive for downstream models.
- Features are represented as exact m/z or neutral loss values; no binning or tolerance window is applied by default, so minor mass measurement variations may fragment the vocabulary unnecessarily.

## Evidence

- [other] Load tandem mass spectra data and parse fragmentation patterns: "Load tandem mass spectra data (mz/intensity pairs and precursor m/z) from input file. 2. Parse fragmentation patterns to identify all observed peaks and compute neutral losses (precursor m/z minus"
- [other] Create feature vocabulary from peaks and neutral losses: "Enumerate unique peak m/z values and unique neutral loss m/z values as feature axes, creating a feature vocabulary."
- [other] Construct sparse vectors for each spectrum: "For each spectrum, construct a sparse binary or count vector where each position corresponds to a unique peak or neutral loss formula, marking presence or abundance of that feature."
- [readme] Features as direct chemical interpretations: "ChemEcho represents features as unique peak or neutral loss formulas. The resulting sparse, high-dimensional feature vectors are well-suited for models that handle sparse inputs, such as regression"
- [readme] Sparse vectors enable conversion to MassQL: "Using ChemEcho vectors, we can train decision trees which are able to be directly converted to MassQL for straightforward deployment, and to more easily evaluate the prediction criteria."
