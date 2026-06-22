---
name: tree-to-query-translation
description: Use when you have a shallow decision tree trained on ChemEcho feature vectors (peak or neutral loss formulas) and need to deploy it as an executable query against tandem mass spectrometry data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2945
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - Mass Query Language (MassQL)
  - ChemEcho
  techniques:
  - tandem-MS
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

# tree-to-query-translation

## Summary

Convert a decision tree path trained on ChemEcho sparse feature vectors into a deployable MassQL query by mapping tree split conditions to fragmentation pattern constraints. This skill enables direct translation of interpretable tree-based models into executable domain-specific language queries for tandem mass spectrometry data.

## When to use

You have a shallow decision tree trained on ChemEcho feature vectors (peak or neutral loss formulas) and need to deploy it as an executable query against tandem mass spectrometry data. Use this skill when you need to validate tree predictions by running them as domain-specific language queries, or when you want to generate hypothesis-driven fragmentation pattern searches from a single tree path.

## When NOT to use

- Input decision tree was trained on latent representations or non-interpretable feature spaces (not ChemEcho vectors).
- Tree is too deep or complex; MassQL query becomes intractable or unvalidatable due to combinatorial path explosion.
- Reference tandem mass spectrometry dataset is unavailable or incompatible with MassQL execution environment.

## Inputs

- Trained decision tree model (sklearn or equivalent)
- ChemEcho feature vector mapping (feature indices to peak/neutral loss formulas)
- Single decision tree path (sequence of split conditions from root to leaf)

## Outputs

- MassQL query string (executable domain-specific language query)
- Validation report (syntactic correctness and predicted vs. observed output match)

## How to apply

Extract a single decision path from the trained tree (root to leaf node), mapping each split condition (feature index and threshold) to its corresponding ChemEcho feature annotation (peak formula or neutral loss). Translate each mapped condition into MassQL syntax—typically FILTER clauses that constrain m/z values or mass differences. Combine the translated conditions into a single MassQL query string following MassQL grammar. Validate syntactic correctness and execute the generated query against a reference dataset, confirming that output matches the tree's prediction for that specific path. The rationale is that ChemEcho's sparse, interpretable features map directly to fragmentation patterns describable in MassQL, eliminating latent space decoding.

## Related tools

- **ChemEcho** (Converts tandem mass spectra into sparse feature vectors (peak or neutral loss formulas) that train interpretable decision trees and map to MassQL conditions.) — https://github.com/biorack/chemecho
- **Mass Query Language (MassQL)** (Domain-specific language used to describe fragmentation patterns and translate tree split conditions into executable queries against tandem mass spectrometry data.) — https://mwang87.github.io/MassQueryLanguage_Documentation/

## Evaluation signals

- Generated MassQL query passes syntactic validation against MassQL grammar.
- MassQL query executes without runtime errors against reference tandem mass spectrometry dataset.
- Predicted outcomes from the MassQL query match the decision tree's predictions for the same test samples on that path.
- All tree split conditions are represented in the query; no conditions are lost or misaligned during translation.
- Query output cardinality and fragmentation pattern matches align with expected ChemEcho feature interpretation (e.g., correct peak or neutral loss formulas are retrieved).

## Limitations

- Skill applies only to shallow decision trees; deep trees produce complex MassQL queries difficult to validate and interpret.
- ChemEcho feature space must be fully documented and traceable to peak/neutral loss formulas; missing or ambiguous annotations block translation.
- MassQL execution environment and reference dataset availability determine whether validation is feasible; offline or restricted datasets cannot be queried.
- Single-path translation loses ensemble or multi-path decision logic; only one path of the tree is converted at a time.

## Evidence

- [intro] ChemEcho converts tandem mass spectra into sparse feature vectors representing unique peak or neutral loss formulas for interpretable machine learning: "ChemEcho is a tool for converting tandem mass spectra into sparse feature vectors, enabling the training of interpretable machine learning models. Rather than mapping fragmentation data into a latent"
- [intro] Sparse, high-dimensional feature vectors from ChemEcho are well-suited for tree-based machine learning: "The resulting sparse, high-dimensional feature vectors are well-suited for models that handle sparse inputs, such as regression and tree-based architectures."
- [intro] Decision trees trained on ChemEcho vectors can be converted directly to MassQL queries for deployment: "Using ChemEcho vectors, we can train decision trees which are able to be directly converted to MassQL for straightforward deployment, and to more easily evaluate the prediction criteria."
- [readme] MassQL is a domain specific language used to describe fragmentation patterns of tandem mass spectra: "The Mass Query Language (MassQL) is a domain specific language used to describe fragmentation patterns (and other attributes) of tandem mass spectra."
- [readme] Example workflow: shallow decision tree trained to predict sulfo group presence, converted from one tree path to MassQL query: "Shown here is a shallow decision tree trained to predict the presence of a sulfo group, and the resulting query built from one path of the tree."
