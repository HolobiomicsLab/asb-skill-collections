---
name: decision-tree-training-and-interpretation
description: Use when you have tandem mass spectra data and need to predict a discrete molecular property (e.g., presence/absence of a sulfo group) while maintaining full interpretability of the decision logic.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_1812
  edam_topics:
  - http://edamontology.org/topic_0089
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_2258
  tools:
  - ChemEcho
  - Decision tree classifier (scikit-learn or equivalent tree-based ML framework)
  - Decision tree classifier (scikit-learn or equivalent)
  - Mass Query Language (MassQL)
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.5c02591
  title: ChemEcho
- doi: 10.1145/2939672.2939778
  title: ''
evidence_spans:
- github.com__biorack__chemecho
- Using ChemEcho vectors, we can train decision trees which are able to be directly converted to MassQL
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

# decision-tree-training-and-interpretation

## Summary

Train shallow decision trees on sparse, high-dimensional ChemEcho feature vectors derived from tandem mass spectra, then extract and validate individual tree paths as interpretable fragmentation-based prediction rules. This skill enables conversion of learned decision boundaries directly into executable MassQL queries for transparent, deployable molecular characterization.

## When to use

You have tandem mass spectra data and need to predict a discrete molecular property (e.g., presence/absence of a sulfo group) while maintaining full interpretability of the decision logic. Use this skill when: (1) ChemEcho feature vectors (sparse, high-dimensional representations of peak and neutral loss formulas) are already available or can be generated; (2) the prediction target is binary or categorical; (3) you require the learned model to be convertible into MassQL queries for direct deployment against spectral databases; and (4) stakeholders need to understand and validate the fragmentation-based criteria driving each prediction.

## When NOT to use

- Input spectra have not yet been converted to ChemEcho vectors; preprocess to sparse feature representation first.
- The prediction target is continuous (e.g., abundance or retention time); use regression trees or alternative methods instead.
- Tree interpretability is not a requirement and prediction accuracy is the only concern; consider deep learning or ensemble black-box models.
- ChemEcho feature vectors are already embedded in a latent (dense, uninterpretable) space; this skill requires explicit, chemically meaningful features.

## Inputs

- ChemEcho sparse feature vectors (high-dimensional, binary or count matrix where rows are spectra and columns are peak/neutral loss formulas)
- Binary or categorical labels (e.g., presence/absence of a functional group such as sulfo)

## Outputs

- Trained decision tree classifier (with documented node splits, thresholds, and leaf predictions)
- Tree structure documentation (node splits, feature indices, decision paths)
- MassQL queries (one or more queries derived from tree paths for deployment against spectral databases)
- Validation metrics (prediction accuracy, interpretability assessment of learned splits)

## How to apply

Load your ChemEcho sparse feature vectors and corresponding binary labels (e.g., sulfo group presence/absence). Train a shallow decision tree classifier (typically depth 2–5 to maintain interpretability) using a tree-based algorithm optimized for sparse inputs, such as scikit-learn's DecisionTreeClassifier with criterion='gini' or 'entropy'. After training, extract the tree structure: for each node, record the feature index (peak or neutral loss formula), the split threshold, and the branch decisions. Validate tree performance by computing prediction accuracy and checking that individual splits align with known fragmentation chemistry (e.g., characteristic losses associated with sulfo groups). For deployment, convert each complete tree path (root-to-leaf sequence) into a MassQL query, replacing feature indices and thresholds with their corresponding fragmentation patterns.

## Related tools

- **ChemEcho** (Converts tandem mass spectra into sparse feature vectors (peak and neutral loss formulas) suitable for training interpretable tree-based models) — https://github.com/biorack/chemecho
- **Decision tree classifier (scikit-learn or equivalent)** (Trains shallow decision trees on ChemEcho sparse feature vectors; handles high-dimensional sparse inputs efficiently)
- **Mass Query Language (MassQL)** (Domain-specific language for describing fragmentation patterns; target format for conversion of decision tree paths into deployable queries) — https://mwang87.github.io/MassQueryLanguage_Documentation/

## Examples

```
from sklearn.tree import DecisionTreeClassifier; from chemecho import load_vectors; X, y = load_vectors('spectra_features.npz', 'sulfo_labels.csv'); tree = DecisionTreeClassifier(max_depth=4, random_state=42); tree.fit(X, y); mql_queries = [convert_tree_path_to_mql(path, tree.feature_names_in_) for path in extract_paths(tree)]
```

## Evaluation signals

- Tree depth and node count are consistent with the 'shallow' design goal (typically ≤5 levels) to maintain interpretability.
- Each split feature (peak or neutral loss formula) is documented and chemically plausible for the prediction task (e.g., sulfo-characteristic losses for sulfo-group prediction).
- Validation accuracy is reported and compared against a baseline (e.g., class-prior or simpler model).
- All tree paths successfully convert to valid MassQL query syntax without loss of information.
- Converted MassQL queries, when applied to an independent test set of spectra, reproduce the tree's predictions on those same spectra.

## Limitations

- Decision trees trained on sparse, high-dimensional ChemEcho vectors may overfit if tree depth or node complexity is not carefully controlled; shallow trees mitigate this but may sacrifice predictive power.
- Interpretability depends on domain expertise to validate that learned splits correspond to known fragmentation chemistry; unexpected splits may indicate data artifacts or label noise.
- MassQL conversion assumes one-to-one mapping between feature indices and MassQL query predicates; complex non-linear interactions between features cannot be fully expressed in simple MassQL queries.
- Performance on spectra with missing or noisy peak data (sparse feature representation with many zeros) is not characterized in the provided documentation.

## Evidence

- [intro] ChemEcho feature vectors input and training: "The resulting sparse, high-dimensional feature vectors are well-suited for models that handle sparse inputs, such as regression and tree-based architectures."
- [intro] Decision trees to MassQL conversion and deployment: "Using ChemEcho vectors, we can train decision trees which are able to be directly converted to MassQL for straightforward deployment, and to more easily evaluate the prediction criteria."
- [readme] ChemEcho sparse feature representation: "ChemEcho is a tool for converting tandem mass spectra into sparse feature vectors, enabling the training of interpretable machine learning models. Rather than mapping fragmentation data into a latent"
- [readme] Example: sulfo-group prediction via shallow decision tree: "Shown here is a shallow decision tree trained to predict the presence of a sulfo group, and the resulting query built from one path of the tree."
- [readme] Interpretability and trust motivation: "This tool is designed for applications where interpretability is essential, including: Evaluating model predictions to ensure reliability and trust."
