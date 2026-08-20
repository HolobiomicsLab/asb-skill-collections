---
name: interpretable-machine-learning
description: Use when when you have tandem mass spectra data and need to predict a
  binary molecular property (e.g., presence of a functional group like a sulfo group)
  while maintaining full interpretability of the model's decision logic.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_1812
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3674
  tools:
  - ChemEcho
  - Decision tree classifier (scikit-learn or equivalent)
  - Mass Query Language (MassQL)
  - LIME
  techniques:
  - LC-MS
  license_tier: restricted
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

# interpretable-machine-learning

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Train shallow decision trees on sparse, high-dimensional ChemEcho feature vectors derived from tandem mass spectra fragmentation patterns to produce human-readable models whose decision paths can be directly converted to MassQL queries for transparent deployment and validation of fragmentation-based prediction criteria.

## When to use

When you have tandem mass spectra data and need to predict a binary molecular property (e.g., presence of a functional group like a sulfo group) while maintaining full interpretability of the model's decision logic. Use this skill when stakeholders require transparent, auditable predictions and the ability to extract and deploy individual prediction rules as domain-specific queries rather than opaque model artifacts.

## When NOT to use

- When input spectra have already been reduced to a latent/dense representation (e.g., neural network embeddings) — interpretability is lost.
- When the target property is continuous (regression) or multi-class — this skill focuses on binary classification and direct MassQL conversion.
- When deep tree ensembles (random forests, boosting) are required for accuracy — shallow trees are the intentional trade-off for interpretability.

## Inputs

- Tandem mass spectra (raw or preprocessed fragmentation data)
- ChemEcho feature vectors (sparse, high-dimensional representation of peak/neutral loss formulas)
- Binary labels for target molecular property (e.g., sulfo group presence: 0/1)

## Outputs

- Shallow decision tree model (fitted tree-based classifier)
- Decision tree structure (node splits, thresholds, leaf predictions)
- MassQL queries derived from individual tree decision paths
- Model performance metrics (accuracy, precision, recall, tree depth)

## How to apply

First, convert your tandem mass spectra into sparse, high-dimensional ChemEcho feature vectors, where each dimension represents a unique peak or neutral loss formula observed in the fragmentation patterns. Load the resulting vectors alongside binary labels for your target property. Train a shallow decision tree classifier (e.g., scikit-learn DecisionTreeClassifier with constrained depth) on these vectors; shallow trees maximize interpretability. Extract the trained tree structure—including node splits (which feature/formula and threshold), thresholds, and leaf predictions. Validate that individual tree paths are convertible to human-readable MassQL queries by confirming that splits align with fragmentation-pattern features. Evaluate performance using standard metrics (accuracy, precision, recall) while also checking that the learned splits are scientifically plausible given the known fragmentation chemistry.

## Related tools

- **ChemEcho** (Converts tandem mass spectra into sparse feature vectors representing unique peak or neutral loss formulas for tree-based model training) — https://github.com/biorack/chemecho
- **Decision tree classifier (scikit-learn or equivalent)** (Trains shallow tree-based model on sparse ChemEcho vectors with interpretable node splits and thresholds)
- **Mass Query Language (MassQL)** (Domain-specific language for expressing and querying fragmentation patterns; decision tree paths are converted to MassQL for deployment and evaluation) — https://mwang87.github.io/MassQueryLanguage_Documentation/
- **LIME** (Post-hoc interpretability method for approximating black-box predictions; complementary to transparent decision tree approach) — https://dl.acm.org/doi/10.1145/2939672.2939778

## Examples

```
from chemecho import ChemEchoFeaturizer
from sklearn.tree import DecisionTreeClassifier
import numpy as np
X_sparse = ChemEchoFeaturizer().fit_transform(spectra)
dt = DecisionTreeClassifier(max_depth=4, random_state=42)
dt.fit(X_sparse, sulfo_labels)
print(dt.tree_.feature, dt.tree_.threshold)
```

## Evaluation signals

- Decision tree depth and number of leaves are consistent with interpretability goal (e.g., depth ≤ 5 for manual inspection of all paths)
- Each tree split corresponds to a valid ChemEcho feature (peak or neutral loss formula) with a scientifically plausible threshold
- All decision tree paths are successfully convertible to syntactically valid MassQL queries without loss of splitting logic
- Model predictions on held-out test spectra match the rules encoded in extracted MassQL queries (no discrepancies between tree and query predictions)
- Feature importance and split thresholds align with known fragmentation chemistry for the target property (e.g., characteristic neutral losses for sulfo groups)

## Limitations

- Shallow trees inherently sacrifice predictive accuracy for interpretability; performance may be lower than deep ensemble methods.
- The approach assumes ChemEcho vectors are sufficiently informative for the prediction task; if fragmentation patterns are insufficient, accuracy will suffer.
- Conversion of tree paths to MassQL queries requires that all split features map to valid MassQL syntax; novel or ambiguous features may not convert cleanly.
- Binary classification focus limits applicability to multi-class or continuous prediction problems without modification.

## Evidence

- [readme] ChemEcho converts tandem mass spectra into sparse feature vectors representing unique peak or neutral loss formulas for interpretable ML: "ChemEcho is a tool for converting tandem mass spectra into sparse feature vectors, enabling the training of interpretable machine learning models. Rather than mapping fragmentation data into a latent"
- [intro] Sparse, high-dimensional ChemEcho vectors are well-suited for tree-based architectures: "The resulting sparse, high-dimensional feature vectors are well-suited for models that handle sparse inputs, such as regression and tree-based architectures."
- [readme] Decision trees trained on ChemEcho vectors can be converted directly to MassQL queries for deployment: "Using ChemEcho vectors, we can train decision trees which are able to be directly converted to MassQL for straightforward deployment, and to more easily evaluate the prediction criteria."
- [readme] MassQL is a domain-specific language for describing tandem mass spectra fragmentation patterns: "The Mass Query Language (MassQL) is a domain specific language used to describe fragmentation patterns (and other attributes) of tandem mass spectra."
- [readme] Example application: shallow decision tree trained to predict sulfo group presence: "Shown here is a shallow decision tree trained to predict the presence of a sulfo group, and the resulting query built from one path of the tree."
