---
name: sparse-feature-vector-handling
description: Use when when you have tandem mass spectra (mz/intensity pairs with precursor m/z) and need to train an interpretable model (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - ChemEcho
  - Mass Query Language (MassQL)
  - Decision Tree Classifier (scikit-learn or equivalent)
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.5c02591
  title: ChemEcho
- doi: 10.1145/2939672.2939778
  title: ''
evidence_spans:
- github.com__biorack__chemecho
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

# Sparse Feature Vector Handling

## Summary

Convert tandem mass spectra into sparse, high-dimensional feature vectors where each dimension represents a unique peak m/z or neutral loss formula, enabling direct chemical interpretation and compatibility with tree-based machine learning models. This skill is essential when interpretability of learned fragmentation patterns is required.

## When to use

When you have tandem mass spectra (mz/intensity pairs with precursor m/z) and need to train an interpretable model (e.g., decision trees) on fragmentation patterns, or when you require direct mapping between model predictions and chemical features (peaks or neutral losses) rather than latent representations. Specifically applicable when model outputs must be convertible to MassQL queries for experimental validation.

## When NOT to use

- Input data is already in a dense feature table or latent representation — reconversion to sparse chemical features would lose information and add unnecessary preprocessing.
- Fragmentation patterns are not available or spectra lack sufficient peak diversity — sparse vectors will be too empty to train meaningful classifiers.
- Model interpretability is not a requirement and black-box neural network performance is acceptable — overhead of sparse feature engineering is not justified.

## Inputs

- tandem mass spectra (mz/intensity pairs with precursor m/z)
- binary or categorical labels (e.g., presence/absence of functional group)

## Outputs

- sparse feature matrix (spectra × features, in CSV or sparse matrix format)
- feature vocabulary (mapping of unique peak m/z and neutral loss m/z to feature indices)
- optional: decision tree classifier trained on sparse vectors

## How to apply

Load tandem mass spectra data as mz/intensity pairs and precursor m/z values. Parse fragmentation patterns to identify all observed peaks and compute neutral losses (precursor m/z minus each observed peak m/z). Enumerate unique peak m/z values and unique neutral loss m/z values as feature axes, creating a sparse feature vocabulary. For each spectrum, construct a sparse binary or count vector where each position corresponds to a unique peak or neutral loss formula, with entries marking presence or abundance of that feature. Aggregate individual vectors into a sparse matrix format (e.g., CSR or COO) with spectra as rows and peak/neutral-loss features as columns. This representation is well-suited for regression and tree-based classifiers because sparse inputs are computationally efficient and each learned split directly corresponds to presence or absence of a specific fragmentation feature.

## Related tools

- **ChemEcho** (Convert tandem mass spectra into sparse feature vectors representing unique peaks and neutral loss formulas) — https://github.com/biorack/chemecho
- **Mass Query Language (MassQL)** (Domain-specific language for describing fragmentation patterns; decision tree paths trained on ChemEcho vectors can be converted to MassQL queries for deployment and experimental validation) — https://mwang87.github.io/MassQueryLanguage_Documentation/
- **Decision Tree Classifier (scikit-learn or equivalent)** (Train shallow tree-based models on sparse ChemEcho vectors; tree splits are directly interpretable as fragmentation criteria)

## Examples

```
from chemecho import ChemEcho; ce = ChemEcho(); spectra = load_spectra('tandem_ms.mzML'); sparse_vectors, vocab = ce.vectorize(spectra); from sklearn.tree import DecisionTreeClassifier; clf = DecisionTreeClassifier(max_depth=3); clf.fit(sparse_vectors, sulfo_labels); mql_query = ce.tree_to_massql(clf, vocab)
```

## Evaluation signals

- Feature matrix sparsity is > 90% (expected for high-dimensional peak/neutral-loss vocabularies); density should remain low even after aggregation across spectra.
- Each feature index maps to a unique chemical entity (peak m/z or neutral loss formula); no duplicates or ambiguous features exist in the vocabulary.
- Decision tree paths extracted from trained models convert unambiguously to MassQL query syntax without information loss.
- Prediction accuracy on held-out spectra is ≥ baseline (e.g., stratified label distribution); interpretability of learned splits matches chemical domain expectations (e.g., specific neutral losses associated with functional groups).
- Sparse matrix dimensions and non-zero counts are consistent across training runs; feature vocabulary remains stable when re-processing the same spectral dataset.

## Limitations

- Sparse feature vectors are high-dimensional (vocabulary size grows with dataset size); memory and computational cost scale with the number of unique peaks and neutral losses observed.
- Binary or count encoding may lose intensity information; if relative abundance is critical for prediction, additional normalization or stratified binning may be necessary.
- Tree-based models trained on sparse vectors assume feature independence and may not capture complex multi-feature fragmentation relationships or mass shifts; shallow trees (as recommended) further limit expressiveness.
- Conversion of tree paths to MassQL queries assumes exact m/z matching; mass spectrometry measurement error or isotope effects may require tolerance windows not explicitly represented in the sparse feature encoding.

## Evidence

- [readme] ChemEcho converts tandem mass spectra into sparse feature vectors and chemical interpretation: "ChemEcho is a tool for converting tandem mass spectra into sparse feature vectors, enabling the training of interpretable machine learning models. Rather than mapping fragmentation data into a latent"
- [readme] Sparse vectors suit tree-based classifiers: "The resulting sparse, high-dimensional feature vectors are well-suited for models that handle sparse inputs, such as regression and tree-based architectures."
- [readme] Tree paths convert to MassQL for deployment: "Using ChemEcho vectors, we can train decision trees which are able to be directly converted to MassQL for straightforward deployment, and to more easily evaluate the prediction criteria."
- [other] Workflow: parse spectra, extract peaks and neutral losses, construct sparse vector: "Parse fragmentation patterns to identify all observed peaks and compute neutral losses (precursor m/z minus each observed peak m/z). Enumerate unique peak m/z values and unique neutral loss m/z"
- [readme] Interpretability is central application: "This tool is designed for applications where interpretability is essential, including: Evaluating model predictions to ensure reliability and trust. Generating hypotheses about underlying"
