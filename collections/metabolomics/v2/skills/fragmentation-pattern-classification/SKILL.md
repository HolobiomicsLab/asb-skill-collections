---
name: fragmentation-pattern-classification
description: Use when you have tandem mass spectra for compounds with known binary or categorical molecular properties (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3502
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  tools:
  - ChemEcho
  - scikit-learn DecisionTreeClassifier
  - Mass Query Language (MassQL)
  techniques:
  - tandem-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# fragmentation-pattern-classification

## Summary

Train interpretable decision trees on ChemEcho sparse feature vectors derived from tandem mass spectra to classify molecular properties (e.g., sulfo group presence). The learned tree paths can be converted directly to MassQL queries for deployment and transparent evaluation of fragmentation-based prediction criteria.

## When to use

You have tandem mass spectra for compounds with known binary or categorical molecular properties (e.g., presence/absence of a functional group), and you need a model that is both predictive and interpretable—where individual decision rules can be mapped back to specific fragmentation patterns (peak formulas or neutral losses) for hypothesis generation or regulatory justification.

## When NOT to use

- Your input is already a pre-extracted feature table or learned model—skip directly to tree training or conversion.
- You require a black-box model with maximum predictive power and have no regulatory or hypothesis-generation need for interpretability.
- Your target property is continuous rather than discrete, or your dataset is too small (< 50 samples) to reliably train and validate a tree.

## Inputs

- tandem mass spectra (raw or preprocessed spectral data)
- ChemEcho sparse feature vectors (high-dimensional binary or count representations of peak/neutral loss formulas)
- binary or categorical labels for molecular property of interest (e.g., sulfo group presence)

## Outputs

- trained shallow decision tree classifier
- decision tree structure (node splits, thresholds, leaf predictions, decision paths)
- MassQL query strings derived from tree paths
- tree performance metrics (accuracy, precision, recall, or AUC on test set)
- interpretable feature importance or split documentation

## How to apply

First, convert each tandem mass spectrum to a sparse, high-dimensional ChemEcho feature vector representing unique peak or neutral loss formulas. Load these vectors alongside binary labels for your target property. Train a shallow decision tree classifier (e.g., scikit-learn's DecisionTreeClassifier with max_depth ≤ 5) on the sparse input; shallow trees maintain interpretability and prevent overfitting. Extract the learned tree structure, including node splits (thresholds on ChemEcho features), internal decision paths, and leaf predictions. Validate tree performance by checking prediction accuracy on a hold-out test set and by inspecting the interpretability of learned splits—each split should correspond to a chemically meaningful fragmentation criterion. Finally, convert selected tree paths to MassQL queries by translating feature thresholds and Boolean logic into domain-specific query syntax for deployment on mass spectrometry databases.

## Related tools

- **ChemEcho** (Converts tandem mass spectra into sparse feature vectors representing unique peak or neutral loss formulas, enabling training of interpretable tree-based classifiers.) — https://github.com/biorack/chemecho
- **scikit-learn DecisionTreeClassifier** (Tree-based classifier algorithm optimized for sparse, high-dimensional inputs to learn shallow decision rules from ChemEcho vectors.)
- **Mass Query Language (MassQL)** (Domain-specific language for describing fragmentation patterns; decision tree paths are converted to MassQL queries for deployment and evaluation on tandem mass spectrometry databases.) — https://mwang87.github.io/MassQueryLanguage_Documentation/

## Examples

```
from chemecho import ChemEcho; from sklearn.tree import DecisionTreeClassifier; X = ChemEcho().transform(spectra); clf = DecisionTreeClassifier(max_depth=4).fit(X, sulfo_labels); tree_path = clf.decision_path(X[0]); mql_query = convert_tree_to_mql(clf, feature_names=ChemEcho().get_feature_names())
```

## Evaluation signals

- Prediction accuracy (or AUC) on held-out test set meets or exceeds baseline or domain benchmarks.
- Each learned tree split corresponds to a chemically interpretable fragmentation criterion (e.g., presence of a known peak formula or neutral loss).
- Decision tree depth and number of leaves are shallow enough (e.g., max_depth ≤ 5) to allow human inspection and conversion to MassQL without exponential complexity.
- MassQL queries derived from tree paths execute successfully and return spectra matching the predicted property with precision consistent with tree leaf confidence.
- Feature importance or split documentation aligns with known fragmentation biochemistry or prior hypothesis.

## Limitations

- Shallow trees sacrifice some predictive capacity for interpretability; deep or ensemble models may achieve better accuracy but lose transparent rule extraction.
- ChemEcho feature vectors are sparse and high-dimensional; small or imbalanced datasets may lead to overfitting or unstable tree structures.
- Conversion of tree paths to MassQL assumes a one-to-one mapping between tree thresholds and MassQL filter operators; complex Boolean logic in large trees may be cumbersome to translate.
- The method is designed for binary or discrete properties; continuous outcomes require regression tree variants and may be harder to translate to MassQL query logic.

## Evidence

- [readme] ChemEcho feature vector definition and sparse representation: "ChemEcho is a tool for converting tandem mass spectra into sparse feature vectors, enabling the training of interpretable machine learning models. Rather than mapping fragmentation data into a latent"
- [readme] Suitability of ChemEcho vectors for tree-based models: "The resulting sparse, high-dimensional feature vectors are well-suited for models that handle sparse inputs, such as regression and tree-based architectures."
- [readme] Direct conversion of decision tree paths to MassQL queries: "Using ChemEcho vectors, we can train decision trees which are able to be directly converted to MassQL for straightforward deployment, and to more easily evaluate the prediction criteria."
- [readme] MassQL as fragmentation pattern query language: "The Mass Query Language (MassQL) is a domain specific language used to describe fragmentation patterns (and other attributes) of tandem mass spectra."
- [readme] Interpretability use case and LIME approximation: "This tool is designed for applications where interpretability is essential, including: Evaluating model predictions to ensure reliability and trust. Generating hypotheses about underlying"
