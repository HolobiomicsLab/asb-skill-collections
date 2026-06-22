---
name: feature-annotation-mapping
description: Use when you have a trained decision tree model on ChemEcho sparse feature vectors and need to convert a specific decision path (root to leaf) into a deployable query.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - ChemEcho
  - Mass Query Language (MassQL)
  - LIME
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

# Feature Annotation Mapping

## Summary

Map machine learning model split conditions (feature indices and thresholds) to interpretable chemical annotations (peak or neutral loss formulas) from ChemEcho feature vectors. This bridges the gap between opaque feature spaces and domain-specific language queries by translating learned decision boundaries into human-readable chemical entities.

## When to use

You have a trained decision tree model on ChemEcho sparse feature vectors and need to convert a specific decision path (root to leaf) into a deployable query. Apply this skill when you must translate individual split conditions—each defined by a feature index and numerical threshold—back into the original chemical domain (e.g., m/z values, neutral loss formulas) so that the decision logic can be executed directly on raw spectra via MassQL or similar query languages.

## When NOT to use

- The decision tree was trained on latent or dense feature representations (not ChemEcho sparse vectors with interpretable chemical annotations)—mapping will fail or produce meaningless chemical entities.
- The model is a black-box ensemble or neural network; this skill requires direct access to individual decision paths, which are not available or interpretable in those architectures.
- The input feature vectors lack annotation metadata; without the mapping from feature indices to chemical formulas, the translation step cannot be performed.

## Inputs

- Trained decision tree model (fitted on ChemEcho feature vectors)
- ChemEcho feature vector metadata (mapping feature indices to peak or neutral loss formulas)
- Decision tree decision path (sequence of split conditions from root to leaf)

## Outputs

- Deployable query string (e.g., MassQL query)
- Set of mapped conditions (feature index → chemical annotation → query clause)
- Validation report (syntactic correctness and prediction matching against reference dataset)

## How to apply

Extract a single decision path from the trained decision tree by traversing from the root node to a leaf, collecting each split condition (feature index and threshold value). For each condition, look up the corresponding ChemEcho annotation in the feature vector metadata—this annotation describes either a unique peak formula or neutral loss formula that was originally extracted from tandem mass spectra. Translate each annotated condition into the target query syntax (e.g., MassQL FILTER clauses specifying m/z or mass difference constraints). Combine all translated conditions into a single query string that respects the domain-specific language grammar. Validate the generated query for syntactic correctness and execute it against a reference dataset to confirm that the query output matches the decision tree's prediction for that path.

## Related tools

- **ChemEcho** (Converts tandem mass spectra into sparse feature vectors with interpretable peak or neutral loss formula annotations; provides the feature metadata required for mapping decision tree indices to chemical entities) — https://github.com/biorack/chemecho
- **Mass Query Language (MassQL)** (Domain-specific language for describing fragmentation patterns; serves as the target syntax for translated decision conditions (FILTER clauses for m/z and mass difference constraints)) — https://mwang87.github.io/MassQueryLanguage_Documentation/
- **LIME** (Referenced as a method for approximating black-box predictions; contextualizes why interpretable decision trees from ChemEcho are valuable alternatives)

## Evaluation signals

- Each split condition (feature index and threshold) successfully maps to a ChemEcho annotation without gaps or unknown indices.
- The generated query string conforms to MassQL grammar (or target domain-specific language grammar) and passes syntactic validation.
- Execution of the generated query on a reference mass spectrometry dataset produces a result set that exactly matches the predictions of the decision tree for that path (100% agreement on prediction outcome).
- The mapped chemical annotations are chemically plausible (e.g., realistic m/z values, known neutral loss patterns such as sulfo group indicators mentioned in the README example).
- The translated query maintains the logical structure of the original decision path (AND/OR combinations of conditions reflect the tree's branching logic).

## Limitations

- Only shallow decision trees are suitable for direct MassQL translation; deep or complex trees may produce unwieldy or inefficient queries.
- The quality of the mapping depends entirely on the completeness and accuracy of ChemEcho's feature annotations; missing or incorrect annotations will produce invalid or misleading queries.
- A single decision path captures only one prediction rule; full model behavior may require multiple paths or ensemble combinations not directly expressible in MassQL.
- Translation assumes one-to-one correspondence between tree split conditions and chemical constraints; non-linear or complex decision boundaries may not translate cleanly to domain-specific query syntax.

## Evidence

- [other] Map each split condition to ChemEcho annotation: "Map each split condition in the path (feature index and threshold) to corresponding ChemEcho feature annotations (peak or neutral loss formula)."
- [readme] ChemEcho represents features as unique peak or neutral loss formulas: "ChemEcho represents features as unique peak or neutral loss formulas. The resulting sparse, high-dimensional feature vectors are well-suited for models that handle sparse inputs, such as regression"
- [other] Translate conditions into MassQL query syntax: "Translate each mapped condition into MassQL query syntax (e.g., FILTER clauses for m/z or mass difference constraints)."
- [readme] Decision trees can be directly converted to MassQL: "Using ChemEcho vectors, we can train decision trees which are able to be directly converted to MassQL for straightforward deployment, and to more easily evaluate the prediction criteria."
- [other] Validate the generated MassQL query for correctness: "Validate the generated MassQL query for syntactic correctness and execute it against a reference dataset to confirm output matches the decision tree prediction for that path."
