---
name: tree-structural-integrity-assessment
description: Use when after generating a Chemical Feature Tree artifact (Phylogeny[Rooted]) from q2-qemistree's make-hierarchy method, or when importing a tree from external sources, to confirm it is well-formed before proceeding to alpha/beta-diversity analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3440
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - q2-qemistree
  - QIIME 2 artifact inspection tools
derived_from:
- doi: 10.1038/s41589-020-00677-3
  title: qemistree
evidence_spans:
- A tool to build a tree of mass-spectrometry (LC-MS/MS) features to perform chemically-informed comparison of untargeted metabolomic profiles.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_qemistree
    doi: 10.1038/s41589-020-00677-3
    title: qemistree
  dedup_kept_from: coll_qemistree
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41589-020-00677-3
  all_source_dois:
  - 10.1038/s41589-020-00677-3
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# tree-structural-integrity-assessment

## Summary

Validate the structural integrity of a Chemical Feature Tree artifact produced by q2-qemistree by inspecting file format, counting nodes, verifying connectivity, and confirming absence of malformed branches. This ensures the tree is suitable for downstream phylogenetic diversity analysis on metabolomic data.

## When to use

After generating a Chemical Feature Tree artifact (Phylogeny[Rooted]) from q2-qemistree's make-hierarchy method, or when importing a tree from external sources, to confirm it is well-formed before proceeding to alpha/beta-diversity analysis. Use this skill when you need assurance that the tree topology is valid and all nodes are properly connected without corruption.

## When NOT to use

- Tree has already been validated by upstream pipeline and you only need to import it for immediate analysis.
- You are comparing trees and need phylogenetic distance metrics rather than structural integrity.

## Inputs

- Phylogeny[Rooted] artifact from q2-qemistree make-hierarchy
- FeatureTable[Frequency] (corresponding feature table, for node validation)

## Outputs

- Structural validation report (node count, tree depth, branching statistics)
- Confirmed well-formed tree artifact suitable for diversity analysis

## How to apply

Load the Chemical Feature Tree artifact using QIIME 2 artifact inspection tools to validate the file format (Newick or QIIME 2 serialized object). Parse the tree structure and count total nodes (leaves + internal nodes), recording tree depth and branching statistics. Verify tree connectivity by confirming each non-root node has exactly one parent, that all leaf nodes correspond to features in the accompanying feature table, and that there are no cycles or orphaned subtrees. Inspect node labels for consistency with feature identifiers and confirm absence of duplicate or null labels. Report structural properties including total node count, tree depth, branching factor statistics, and any anomalies detected.

## Related tools

- **q2-qemistree** (Generates Chemical Feature Tree artifact (Phylogeny[Rooted]) that is the subject of integrity assessment) — https://github.com/biocore/q2-qemistree
- **QIIME 2 artifact inspection tools** (Load and deserialize tree artifact for format validation and node enumeration)

## Evaluation signals

- Tree file deserializes without errors in Newick or QIIME 2 serialized format
- Total node count (leaves + internal) matches expected count from feature count and tree structure rules
- Tree is connected: all internal nodes have in-degree 1 (except root, which has 0) and out-degree ≥ 2; all leaves have out-degree 0
- All leaf node labels correspond to feature identifiers in the accompanying FeatureTable[Frequency]
- No cycles, duplicate node IDs, or orphaned subtrees detected; tree depth is consistent with branching statistics

## Limitations

- SIRIUS predicts molecular substructures (fingerprints) for only 70–90% of MS1 features, meaning some features are filtered out during hierarchy generation; structural integrity assessment cannot confirm completeness relative to the original feature set.
- Tree validation does not assess chemical correctness or biological meaningfulness of the hierarchy—it only checks formal graph properties.
- Node labels depend on upstream MZmine2 or SIRIUS feature naming; label consistency cannot be verified without access to original peak detection output.

## Evidence

- [other] q2-qemistree is designed to build a tree of mass-spectrometry features for chemically-informed metabolomic profile comparison.: "q2-qemistree is designed to build a tree of mass-spectrometry features for chemically-informed metabolomic profile comparison."
- [other] Load the Chemical Feature Tree artifact using QIIME 2 artifact inspection tools. Validate file format as either Newick or QIIME 2 serialized object. Parse tree structure and count total nodes (leaves + internal nodes). Verify tree connectivity and absence of malformed branches.: "Load the Chemical Feature Tree artifact using QIIME 2 artifact inspection tools. Validate file format as either Newick or QIIME 2 serialized object. Parse tree structure and count total nodes (leaves"
- [readme] A tree relating the MS1 features in these data based on molecular substructures predicted for MS1 features. This is of type `Phylogeny[Rooted]`.: "A tree relating the MS1 features in these data based on molecular substructures predicted for MS1 features. This is of type `Phylogeny[Rooted]`."
- [readme] SIRIUS predicts molecular substructures for a subset of features (typically for 70-90% of all MS1 features) in an experiment: "SIRIUS predicts molecular substructures for a subset of features (typically for 70-90% of all MS1 features) in an experiment"
- [readme] These can be used as inputs to perform chemical phylogeny-based alpha-diversity and beta-diversity analyses.: "These can be used as inputs to perform chemical phylogeny-based alpha-diversity and beta-diversity analyses."
