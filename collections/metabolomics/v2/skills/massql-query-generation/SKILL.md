---
name: massql-query-generation
description: Use when you have trained a shallow decision tree on ChemEcho feature
  vectors (representing unique peak or neutral loss formulas from tandem MS spectra)
  and need to deploy the learned splitting logic as a queryable, inspectable artifact.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0218
  tools:
  - Mass Query Language (MassQL)
  - ChemEcho
  - scikit-learn (or equivalent tree library)
  techniques:
  - LC-MS
  license_tier: restricted
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

# Convert decision tree paths to MassQL queries for mass spectrometry deployment

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

This skill translates decision tree splitting rules trained on ChemEcho sparse feature vectors (peak and neutral loss formulas) into executable Mass Query Language (MassQL) queries for direct deployment against tandem mass spectrometry datasets. It bridges interpretable machine learning and domain-specific query languages, enabling reproducible, explainable fragmentation pattern detection without black-box latent representations.

## When to use

You have trained a shallow decision tree on ChemEcho feature vectors (representing unique peak or neutral loss formulas from tandem MS spectra) and need to deploy the learned splitting logic as a queryable, inspectable artifact. This is especially valuable when you must validate model predictions against raw spectra, generate hypotheses about fragmentation chemistry, or share prediction criteria with domain experts who lack machine learning expertise.

## When NOT to use

- Input is already a feature table with dense or latent-space embeddings (not ChemEcho sparse vectors)—use a different model architecture or feature extraction pipeline first.
- Decision tree is too deep (many levels) or highly imbalanced—generated MassQL queries become complex and brittle; consider tree pruning or ensemble aggregation.
- Reference spectra are not accessible in a queryable format (e.g., raw binary files without indexing)—MassQL execution and validation cannot proceed.

## Inputs

- Trained shallow decision tree model (sklearn DecisionTreeClassifier or similar, fitted on ChemEcho vectors)
- ChemEcho feature dictionary or annotations (mapping feature indices to peak m/z values or neutral loss formulas)
- Reference tandem mass spectrometry dataset (spectra used for tree training, in a format queryable by MassQL, e.g., mzML or vendor format indexed in a MassQL library)

## Outputs

- MassQL query string (text, compliant with MassQL grammar, describing one decision path as a series of FILTER clauses)
- Validation report (boolean: whether generated query output matches decision tree leaf prediction on reference dataset)

## How to apply

Extract a single decision path from the trained tree by traversing from root to a leaf node, recording each split condition (feature index and threshold value). Map each split to its corresponding ChemEcho feature annotation—look up the feature index in the model's feature dictionary to recover the peak m/z or neutral loss formula that triggered the decision. Translate each mapped condition into MassQL FILTER clause syntax (e.g., FILTER m/z = [value] or FILTER neutral_loss = [formula]), preserving the logical operators (AND/OR) that combine conditions along the path. Assemble the clauses into a single MassQL query string conforming to MassQL domain-specific language grammar. Validate syntactic correctness by parsing the generated query and execute it against a reference dataset (the same spectra used to train the tree), confirming that the returned spectrum predictions match the leaf node outcome for that path.

## Related tools

- **ChemEcho** (Converts tandem mass spectra into sparse feature vectors (peak and neutral loss formulas) that serve as input to decision tree training and are mapped back to MassQL filter conditions.) — https://github.com/biorack/chemecho
- **Mass Query Language (MassQL)** (Domain-specific language for specifying fragmentation pattern queries; translated decision tree paths are emitted as MassQL queries for deployment and validation.) — https://mwang87.github.io/MassQueryLanguage_Documentation/
- **scikit-learn (or equivalent tree library)** (Provides the decision tree model implementation and path extraction interface (e.g., tree.decision_path, tree_.feature, tree_.threshold).)

## Evaluation signals

- Generated MassQL query parses without syntax errors according to MassQL grammar and can be executed by a MassQL query engine.
- Execution of the generated query against the reference dataset returns a spectrum subset whose class label (predicted outcome) matches the decision tree leaf node label for that path.
- All split thresholds and feature conditions in the query correspond exactly to the decision tree node thresholds and feature indices; no discrepancies in mapping.
- For a curated test set of spectra known to satisfy the path conditions, recall is ≥0.95 (the query returns nearly all spectra the tree would classify under that path).
- The MassQL query is human-readable and reproducible: another analyst executing the same query against the same dataset obtains identical results.

## Limitations

- Requires shallow decision trees for practical readability; deep trees generate unwieldy MassQL queries with many nested conditions.
- MassQL query expressiveness may not capture all tree splits if feature conditions involve complex thresholds or interactions not easily represented in the domain-specific language.
- Validation accuracy depends on complete, indexed access to the reference spectra; missing or incompletely indexed spectra will produce incomplete query results.
- Feature annotations (peak m/z and neutral loss formulas) must be accurate; errors in the ChemEcho feature dictionary propagate directly into incorrect MassQL filter conditions.

## Evidence

- [other] How can a decision tree path trained on ChemEcho features be converted into a MassQL query for deployment?: "How can a decision tree path trained on ChemEcho features be converted into a MassQL query for deployment?"
- [other] A shallow decision tree trained to predict the presence of a sulfo group can be converted to MassQL queries by translating one path of the tree into a domain-specific language query that describes fragmentation patterns.: "A shallow decision tree trained to predict the presence of a sulfo group can be converted to MassQL queries by translating one path of the tree into a domain-specific language query that describes"
- [other] 1. Load the trained decision tree model and extract a single decision path from root to leaf node. 2. Map each split condition in the path (feature index and threshold) to corresponding ChemEcho feature annotations (peak or neutral loss formula). 3. Translate each mapped condition into MassQL query syntax (e.g., FILTER clauses for m/z or mass difference constraints). 4. Combine translated conditions into a single MassQL query string following MassQL domain-specific language grammar. 5. Validate the generated MassQL query for syntactic correctness and execute it against a reference dataset to confirm output matches the decision tree prediction for that path.: "Load the trained decision tree model and extract a single decision path from root to leaf node. Map each split condition in the path (feature index and threshold) to corresponding ChemEcho feature"
- [readme] ChemEcho is a tool for converting tandem mass spectra into sparse feature vectors, enabling the training of interpretable machine learning models. Rather than mapping fragmentation data into a latent space, ChemEcho represents features as unique peak or neutral loss formulas.: "ChemEcho is a tool for converting tandem mass spectra into sparse feature vectors, enabling the training of interpretable machine learning models. Rather than mapping fragmentation data into a latent"
- [readme] Using ChemEcho vectors, we can train decision trees which are able to be directly converted to MassQL for straightforward deployment, and to more easily evaluate the prediction criteria.: "Using ChemEcho vectors, we can train decision trees which are able to be directly converted to MassQL for straightforward deployment, and to more easily evaluate the prediction criteria."
- [readme] The Mass Query Language (MassQL) is a domain specific language used to describe fragmentation patterns (and other attributes) of tandem mass spectra.: "The Mass Query Language (MassQL) is a domain specific language used to describe fragmentation patterns (and other attributes) of tandem mass spectra."
