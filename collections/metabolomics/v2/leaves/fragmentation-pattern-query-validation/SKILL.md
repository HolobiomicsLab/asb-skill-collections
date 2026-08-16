---
name: fragmentation-pattern-query-validation
description: Use when after converting a decision tree path into a MassQL query string,
  before deployment to production mass spectrometry workflows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - Mass Query Language (MassQL)
  - ChemEcho
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

# fragmentation-pattern-query-validation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Validate that a decision tree path trained on ChemEcho mass spectrometry features has been correctly translated into a MassQL domain-specific language query by checking syntactic correctness and comparing predictions against a reference dataset. This ensures interpretable fragmentation patterns are accurately represented and deployable.

## When to use

After converting a decision tree path into a MassQL query string, before deployment to production mass spectrometry workflows. Specifically, when you have a shallow decision tree trained on ChemEcho feature vectors (peak or neutral loss formulas) and need to verify that each split condition (feature index and threshold) has been correctly mapped to MassQL FILTER clauses and that the resulting query produces identical predictions to the original tree on held-out spectra.

## When NOT to use

- Input MassQL query has not yet been generated from a decision tree path; use the conversion workflow first.
- Reference dataset does not have ground-truth labels or pre-computed decision tree predictions; validation cannot proceed without a ground truth.
- The decision tree is very deep (many conditions per path) or uses continuous features not representable in MassQL syntax; validation may be infeasible or reveal fundamental expressiveness gaps.

## Inputs

- trained decision tree model (shallow tree with node split conditions)
- MassQL query string (translated from one path of the tree)
- reference dataset of tandem mass spectra with known ground-truth labels or tree predictions

## Outputs

- validation report with agreement/disagreement counts
- syntactic correctness verdict (boolean: query parses or fails)
- prediction comparison matrix (tree output vs. MassQL output per spectrum)
- corrected MassQL query (if errors were found and fixed)

## How to apply

Execute the generated MassQL query string against a reference dataset of tandem mass spectra for which you know the ground-truth decision tree predictions. First, validate syntactic correctness by parsing the query against MassQL domain-specific language grammar to catch translation errors (malformed FILTER clauses, incorrect m/z or mass difference constraints). Then execute the query and compare its output predictions (e.g., presence or absence of a target feature like a sulfo group) to the predictions from the original decision tree on the same spectra. The predictions must match exactly; any divergence indicates an error in the path-to-query translation step (feature mapping, threshold conversion, or clause combination). Document agreement rate and any discrepancies.

## Related tools

- **Mass Query Language (MassQL)** (Domain-specific language used to express and execute fragmentation pattern queries; the validation target) — https://mwang87.github.io/MassQueryLanguage_Documentation/
- **ChemEcho** (Tool that converts tandem mass spectra into sparse feature vectors (peak or neutral loss formulas) used to train decision trees; context for understanding feature mapping in translation) — https://github.com/biorack/chemecho

## Evaluation signals

- MassQL query string passes syntactic validation against MassQL grammar (no parse errors).
- Prediction agreement rate between tree and MassQL query on reference spectra is 100% (no divergences on any test sample).
- Each split condition in the decision tree path maps to exactly one corresponding FILTER clause in the MassQL query with correct m/z or mass difference thresholds.
- Query execution completes without runtime errors and returns a non-empty result set on valid reference spectra.
- Feature annotations (peak or neutral loss formulas) used in FILTER clauses match the ChemEcho feature indices in the original tree splits.

## Limitations

- Validation assumes the reference dataset is representative of the deployment domain; bias in reference data will not be caught.
- Decision tree paths with many nested conditions may produce complex MassQL queries prone to human translation error; shallow trees are easier to validate.
- MassQL syntax may not be able to express all types of tree splits (e.g., non-linear thresholds or feature interactions); validation will reveal expressiveness gaps but not resolve them.
- Validation only checks prediction equivalence on the reference spectra; it does not validate biological interpretability or real-world deployment performance.

## Evidence

- [other] Validate the generated MassQL query for syntactic correctness and execute it against a reference dataset to confirm output matches the decision tree prediction for that path.: "Validate the generated MassQL query for syntactic correctness and execute it against a reference dataset to confirm output matches the decision tree prediction for that path."
- [other] Map each split condition in the path (feature index and threshold) to corresponding ChemEcho feature annotations (peak or neutral loss formula). Translate each mapped condition into MassQL query syntax.: "Map each split condition in the path (feature index and threshold) to corresponding ChemEcho feature annotations (peak or neutral loss formula). Translate each mapped condition into MassQL query"
- [readme] The Mass Query Language (MassQL) is a domain specific language used to describe fragmentation patterns and other attributes of tandem mass spectra.: "The Mass Query Language (MassQL) is a domain specific language used to describe fragmentation patterns (and other attributes) of tandem mass spectra."
- [readme] Using ChemEcho vectors, we can train decision trees which are able to be directly converted to MassQL for straightforward deployment, and to more easily evaluate the prediction criteria.: "Using ChemEcho vectors, we can train decision trees which are able to be directly converted to MassQL for straightforward deployment, and to more easily evaluate the prediction criteria."
- [readme] ChemEcho represents features as unique peak or neutral loss formulas, resulting in sparse, high-dimensional feature vectors well-suited for tree-based architectures.: "ChemEcho represents features as unique peak or neutral loss formulas. The resulting sparse, high-dimensional feature vectors are well-suited for models that handle sparse inputs, such as regression"
