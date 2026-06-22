---
name: mass-spectrum-normalization-and-preprocessing
description: Use when you have raw tandem mass spectra data (mz/intensity pairs and precursor m/z values) and need to train interpretable machine learning models (regression or tree-based) where feature interpretability and direct chemical meaning are required.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Mass Query Language (MassQL)
  - ChemEcho
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.5c02591
  title: ChemEcho
- doi: 10.1145/2939672.2939778
  title: ''
evidence_spans:
- The Mass Query Language (MassQL) is a domain specific language used to describe fragmentation patterns
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrum-normalization-and-preprocessing

## Summary

Convert raw tandem mass spectra (mz/intensity pairs with precursor m/z) into normalized, interpretable sparse feature vectors by parsing fragmentation patterns, computing neutral losses, and enumerating unique peak and loss formulas. This preprocessing step is essential for training interpretable machine learning models on mass spectrometry data.

## When to use

You have raw tandem mass spectra data (mz/intensity pairs and precursor m/z values) and need to train interpretable machine learning models (regression or tree-based) where feature interpretability and direct chemical meaning are required. Apply this skill when you want features that directly map to chemical formulas rather than latent representations, and when downstream model decisions must be translatable to deployment languages like MassQL.

## When NOT to use

- Input is already a feature table or pre-computed feature matrix — skip directly to model training.
- You require latent feature representations or dimensionality reduction — use alternative embedding methods instead.
- Raw m/z and intensity data are missing or incomplete — preprocessing cannot enumerate features reliably.

## Inputs

- tandem mass spectra data (mz/intensity pairs)
- precursor m/z values
- spectral fragmentation patterns (text or binary format)

## Outputs

- sparse feature matrix (spectra × features)
- feature vocabulary (mapping of feature indices to peak/neutral-loss formulas)
- CSV or sparse matrix file format

## How to apply

Load tandem mass spectra from input files containing mz/intensity pairs and precursor m/z values. Parse the fragmentation patterns to identify all observed peaks and compute neutral losses (precursor m/z minus each observed peak m/z). Enumerate unique peak m/z values and unique neutral loss m/z values as feature axes, creating a feature vocabulary that directly corresponds to chemical formulas. For each spectrum, construct a sparse binary or count vector where each position corresponds to a unique peak or neutral loss formula, marking presence or abundance of that feature. Aggregate individual spectrum vectors into a matrix with spectra as rows and features (peak/neutral-loss formulas) as columns, then serialize in CSV or sparse matrix format suitable for downstream machine learning.

## Related tools

- **ChemEcho** (Primary tool for converting tandem mass spectra into sparse feature vectors via peak and neutral loss enumeration) — https://github.com/biorack/chemecho
- **Mass Query Language (MassQL)** (Domain-specific language used to describe fragmentation patterns and validate feature vocabularies; downstream target for decision tree conversion) — https://mwang87.github.io/MassQueryLanguage_Documentation/

## Examples

```
pip install git+https://github.com/biorack/chemecho.git#egg=chemecho && python -c "from chemecho import ChemEcho; ce = ChemEcho(); vectors = ce.convert_spectra('input_spectra.txt'); ce.save_vectors(vectors, 'output_features.csv')"
```

## Evaluation signals

- Feature vocabulary contains all unique peak m/z values and all computed neutral loss formulas with no duplicates.
- Sparse feature matrix has dimensions matching the number of input spectra (rows) and unique features (columns).
- Each spectrum vector is sparse (majority of entries are zero) and composed only of binary or count values consistent with presence/abundance encoding.
- Neutral loss calculations are correct: for each observed peak, |precursor_mz − peak_mz| matches expected loss formulas.
- Output matrix can be successfully loaded and parsed by downstream tree-based or regression models without schema errors.

## Limitations

- Feature vocabulary grows with the diversity of fragmentation patterns; high-dimensional sparse matrices may become computationally expensive for very large spectral datasets.
- Neutral loss computation assumes accurate precursor m/z annotation; errors in precursor mass will propagate as incorrect loss features.
- Binary or count encoding discards intensity magnitude information; only presence/frequency is preserved in the sparse vector representation.
- The resulting high-dimensional, sparse feature space may suffer from sparsity-related statistical challenges (e.g., overfitting in small sample regimes).

## Evidence

- [intro] Load and parse fragmentation patterns from tandem mass spectra: "Load tandem mass spectra data (mz/intensity pairs and precursor m/z) from input file. 2. Parse fragmentation patterns to identify all observed peaks and compute neutral losses"
- [intro] Compute neutral losses and enumerate unique features: "compute neutral losses (precursor m/z minus each observed peak m/z). 3. Enumerate unique peak m/z values and unique neutral loss m/z values as feature axes"
- [intro] Construct sparse feature vectors per spectrum: "For each spectrum, construct a sparse binary or count vector where each position corresponds to a unique peak or neutral loss formula"
- [intro] Aggregate into matrix and serialize: "Aggregate vectors into a matrix with spectra as rows and features (peak/neutral-loss formulas) as columns, and save in CSV or sparse matrix format"
- [readme] ChemEcho tool overview and purpose: "ChemEcho is a tool for converting tandem mass spectra into sparse feature vectors, enabling the training of interpretable machine learning models"
- [readme] Sparse features suit tree-based and regression models: "The resulting sparse, high-dimensional feature vectors are well-suited for models that handle sparse inputs, such as regression and tree-based architectures"
