---
name: decision-tree-path-extraction
description: Use when you have a trained shallow decision tree on ChemEcho feature vectors (sparse, high-dimensional representations of tandem mass spectra peaks and neutral losses) and need to convert it into an interpretable, deployable query for a domain-specific language like MassQL.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3766
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
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

# decision-tree-path-extraction

## Summary

Extract a single decision path from a trained decision tree model and map each split condition to interpretable feature annotations (peak or neutral loss formulas from ChemEcho), enabling conversion to deployable domain-specific language queries. This skill bridges black-box tree models and human-readable fragmentation pattern rules.

## When to use

You have a trained shallow decision tree on ChemEcho feature vectors (sparse, high-dimensional representations of tandem mass spectra peaks and neutral losses) and need to convert it into an interpretable, deployable query for a domain-specific language like MassQL. This is especially valuable when you must explain or validate prediction criteria for a specific decision boundary (e.g., presence of a sulfo group), or when you need to translate model logic into a query that can be executed independently against reference datasets.

## When NOT to use

- The decision tree is too deep or too complex to meaningfully convert to a single interpretable query; in such cases, consider simplifying or retraining a shallower model.
- ChemEcho feature annotations are not available or have not been preserved; path extraction requires the explicit mapping between feature indices and fragmentation formulas.
- The target query language (e.g., MassQL) does not support the types of conditions present in the tree (e.g., continuous thresholds that cannot be discretized into valid m/z or mass difference constraints).

## Inputs

- Trained decision tree model (root-to-leaf structure with split conditions)
- ChemEcho feature vector metadata (mapping of feature indices to peak or neutral loss formulas)
- Decision tree training dataset or reference mass spectra dataset

## Outputs

- MassQL query string (domain-specific language representation of decision path)
- Validated query execution result (binary or multi-class prediction output)
- Feature-to-formula mapping table (traceability for each split condition)

## How to apply

Load the trained decision tree model and traverse a single path from root to leaf node, recording each split condition (feature index and threshold value). For each split, map the feature index back to its corresponding ChemEcho annotation—a specific peak formula or neutral loss formula extracted during feature vectorization. Translate each condition into MassQL syntax (e.g., FILTER clauses specifying m/z or mass difference constraints that match the annotation). Concatenate the translated conditions into a single MassQL query string following MassQL domain-specific language grammar. Finally, validate the generated query for syntactic correctness and execute it against a reference dataset to confirm that the output matches the decision tree's prediction for that specific path.

## Related tools

- **ChemEcho** (Converts tandem mass spectra into sparse feature vectors (peak and neutral loss formulas) that serve as input to decision tree training and feature-to-annotation mapping during path extraction.) — https://github.com/biorack/chemecho
- **Mass Query Language (MassQL)** (Domain-specific language for describing fragmentation patterns; extracted decision tree paths are translated into MassQL query syntax for deployment and validation.) — https://mwang87.github.io/MassQueryLanguage_Documentation/

## Evaluation signals

- The extracted path's split conditions are each successfully mapped to a valid ChemEcho feature annotation (peak or neutral loss formula).
- The generated MassQL query is syntactically valid and can be parsed by the MassQL interpreter without errors.
- Execution of the MassQL query against a reference dataset produces output (prediction labels, confidence scores, or matched spectra) that matches the decision tree's prediction for the same path.
- All intermediate nodes in the path have thresholds that can be discretized into valid m/z or mass difference constraints within the MassQL domain.
- The feature-to-formula mapping remains consistent across multiple reference executions (reproducibility check).

## Limitations

- Path extraction assumes a shallow decision tree; deep trees may produce overly complex or semantically incoherent MassQL queries.
- The method is restricted to tree-based architectures; it cannot be applied to random forests, boosted models, or other ensemble methods without breaking down each tree separately.
- Translation to MassQL is specific to tandem mass spectrometry fragmentation patterns; the skill does not generalize to other domains or query languages without retraining the feature annotations and grammar rules.
- Validation requires a reference dataset with ground-truth labels; if such data is unavailable or biased, the comparison between tree prediction and query output may be unreliable.

## Evidence

- [other] Load the trained decision tree model and extract a single decision path from root to leaf node.: "Load the trained decision tree model and extract a single decision path from root to leaf node."
- [other] Map each split condition in the path (feature index and threshold) to corresponding ChemEcho feature annotations (peak or neutral loss formula).: "Map each split condition in the path (feature index and threshold) to corresponding ChemEcho feature annotations (peak or neutral loss formula)."
- [other] Translate each mapped condition into MassQL query syntax (e.g., FILTER clauses for m/z or mass difference constraints).: "Translate each mapped condition into MassQL query syntax (e.g., FILTER clauses for m/z or mass difference constraints)."
- [readme] ChemEcho is a tool for converting tandem mass spectra into sparse feature vectors, enabling the training of interpretable machine learning models.: "ChemEcho is a tool for converting tandem mass spectra into sparse feature vectors, enabling the training of interpretable machine learning models."
- [readme] Using ChemEcho vectors, we can train decision trees which are able to be directly converted to MassQL for straightforward deployment, and to more easily evaluate the prediction criteria.: "Using ChemEcho vectors, we can train decision trees which are able to be directly converted to MassQL for straightforward deployment, and to more easily evaluate the prediction criteria."
- [other] Validate the generated MassQL query for syntactic correctness and execute it against a reference dataset to confirm output matches the decision tree prediction for that path.: "Validate the generated MassQL query for syntactic correctness and execute it against a reference dataset to confirm output matches the decision tree prediction for that path."
