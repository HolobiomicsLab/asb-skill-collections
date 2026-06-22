---
name: phylogenetic-tree-validation
description: Use when after generating a Chemical Feature Tree from q2-qemistree (or any tree artifact) and before using it for alpha-diversity or beta-diversity phylogenetic analyses.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2423
  edam_topics:
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  tools:
  - q2-qemistree
  - QIIME 2 artifact inspection tools
  - SIRIUS / CSI:FingerID
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

# phylogenetic-tree-validation

## Summary

Validate the structural integrity and correctness of a phylogenetic tree artifact produced by q2-qemistree or similar tree-building pipelines. This skill ensures the tree is properly formatted, correctly connected, and suitable for downstream phylogenetic diversity analyses.

## When to use

Apply this skill after generating a Chemical Feature Tree from q2-qemistree (or any tree artifact) and before using it for alpha-diversity or beta-diversity phylogenetic analyses. Validation is critical when tree-building depends on predicted molecular substructures (fingerprints) that may be incomplete or when merging multiple datasets into a single hierarchy.

## When NOT to use

- Input is a raw fragmentation tree or SiriusFolder artifact — validate only after hierarchy construction via make-hierarchy.
- Tree has not been pruned or filtered — validate after any pruning step to confirm expected structural changes.
- Input feature table still contains features with no fingerprints — filtered feature table must be used as the reference for node validation.

## Inputs

- Phylogeny[Rooted] artifact (qemistree.qza or equivalent)
- FeatureTable[Frequency] artifact (paired feature table)
- FeatureData[Molecules] artifact (feature metadata with parent_mass, retention_time, csi_smiles)

## Outputs

- Validation report (node count, tree depth, branching statistics, connectivity status)
- Feature correspondence matrix (tree nodes vs. feature table rows)
- Tree structure summary (rooted status, acyclic confirmation, orphan/malformed branch list)

## How to apply

Load the tree artifact using QIIME 2 artifact inspection tools and verify file format (Newick or QIIME 2 serialized object). Parse the tree structure to confirm it is rooted and acyclic, then count total nodes (leaf nodes representing MS1 features plus internal nodes). Validate tree connectivity by ensuring every internal node has exactly two or more children and no orphaned branches exist. Check that node labels (feature identifiers) are unique and correspond to the associated feature table (features without fingerprints should have been filtered during hierarchy construction). Verify tree depth is reasonable given the number of features and branching statistics (e.g., degree distribution, balance metrics). Report structural properties and compare node count to expected feature count to detect silent filtering or corruption.

## Related tools

- **q2-qemistree** (Generates the Chemical Feature Tree (make-hierarchy command) that is then validated; also provides prune-hierarchy for post-validation filtering) — https://github.com/biocore/q2-qemistree
- **QIIME 2 artifact inspection tools** (Load, deserialize, and inspect tree artifact format and content)
- **SIRIUS / CSI:FingerID** (Upstream tool that predicts molecular substructures (fingerprints) used to construct the tree; validation ensures all features with fingerprints are represented as nodes) — https://bio.informatik.uni-jena.de/

## Examples

```
qiime tools inspect-metadata qemistree.qza && qiime tools peek qemistree.qza && python -c "from qiime2 import Artifact; tree=Artifact.load('qemistree.qza'); print(f'Nodes: {len(tree.view(skbio.TreeNode))}')"
```

## Evaluation signals

- Tree is rooted with exactly one root node and no cycles detected during depth-first traversal.
- Node count equals the number of rows in the filtered feature table (features with fingerprints); discrepancies indicate silent filtering or data corruption.
- All feature identifiers in tree node labels are unique and match corresponding entries in FeatureData[Molecules] artifact.
- Tree connectivity is intact: every internal node has ≥2 children, all leaf nodes are features, no orphaned or dangling branches.
- Tree depth is proportional to the number of features (typically 10–30 levels for thousands of features); unexpectedly shallow or deep trees suggest imbalance or structural anomaly.

## Limitations

- SIRIUS predicts molecular substructures (fingerprints) for only a subset of MS1 features (typically 70–90%), so features without fingerprints are filtered out during tree construction; validation should account for this expected feature loss.
- Tree structure depends on the quality and format of input MGF files; malformed MGF entries (missing MS1, MS2 mismatches, formatting errors) cause SIRIUS to skip features and produce incomplete trees.
- When merging multiple datasets via make-hierarchy with multiple --i-csi-results and --i-feature-tables, feature identifiers are hashed to prevent collisions; validation must use the hashed feature IDs from the output, not original feature names.
- Tree validity also depends on SIRIUS and CSI:FingerID version (q2-qemistree adapted from SIRIUS 4.0.1 to ≥4.4.29); version mismatches may produce inconsistent fingerprint predictions and tree topology.

## Evidence

- [other] Parse tree structure and count total nodes (leaves + internal nodes). Verify tree connectivity and absence of malformed branches.: "Parse tree structure and count total nodes (leaves + internal nodes). 4. Verify tree connectivity and absence of malformed branches."
- [readme] MS1 features without fingerprints are filtered out of this feature table. This is done because SIRIUS predicts molecular substructures for a subset of features (typically for 70-90% of all MS1 features) in an experiment: "MS1 features without fingerprints are filtered out of this feature table. This is done because SIRIUS predicts molecular substructures for a subset of features (typically for 70-90% of all MS1"
- [readme] A tree relating the MS1 features in these data based on molecular substructures predicted for MS1 features. This is of type `Phylogeny[Rooted]`.: "A tree relating the MS1 features in these data based on molecular substructures predicted for MS1 features. This is of type `Phylogeny[Rooted]`."
- [readme] If the MGF file has formatting errors (eg. no MS1 are included in the MGF, or if an MS1 entry does not have a corresponding MS2 entry), then an appropriate error message will help users troubleshoot this step: "If the MGF file has formatting errors (eg. no MS1 are included in the MGF, or if an MS1 entry does not have a corresponding MS2 entry)"
- [other] Report structural properties including tree depth, branching statistics, and node labels.: "Report structural properties including tree depth, branching statistics, and node labels."
