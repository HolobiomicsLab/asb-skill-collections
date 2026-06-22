---
name: mass-spectrometry-feature-tree-interpretation
description: Use when after running qiime qemistree make-hierarchy and obtaining a tree artifact (qemistree.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0566
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - q2-qemistree
  - QIIME 2
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
---

# mass-spectrometry-feature-tree-interpretation

## Summary

Inspect, validate, and characterize the structural properties of a Chemical Feature Tree artifact produced by q2-qemistree to understand the hierarchy and connectivity of mass-spectrometry features for downstream chemically-informed metabolomic analysis. This skill confirms tree integrity before using it for alpha/beta-diversity calculations or feature interpretation.

## When to use

After running qiime qemistree make-hierarchy and obtaining a tree artifact (qemistree.qza of type Phylogeny[Rooted]), or when receiving a pre-computed tree from collaborators and needing to verify its format, node structure, and branching properties before downstream diversity or visualization analyses.

## When NOT to use

- Input is a raw MGF mass-spectrometry file or feature table; tree construction has not yet been performed.
- Tree artifact is from a non-chemical phylogenetic method (e.g., 16S rRNA tree); Qemistree-specific metadata validation will fail.
- You only need to assign taxonomy or filter features by chemical class; use get-classyfire-taxonomy or prune-hierarchy instead.

## Inputs

- Phylogeny[Rooted] artifact (qemistree.qza)
- FeatureData[Molecules] artifact (feature-data.qza) containing node metadata

## Outputs

- Tree structure report (node count, depth, branching statistics)
- Validated Newick or QIIME 2 tree object suitable for diversity analyses
- Node label inventory and feature-to-node mapping

## How to apply

Load the Chemical Feature Tree artifact using QIIME 2 artifact inspection tools (e.g., qiime tools peek or direct deserialization). Validate the file format as either Newick or QIIME 2 serialized object by inspecting the artifact metadata and structure. Parse the tree and enumerate total nodes (leaf nodes corresponding to individual MS1 features plus internal nodes representing inferred molecular relationships). Verify tree connectivity by confirming that all nodes are reachable from the root, that no branches are malformed or orphaned, and that the tree is fully rooted. Report structural properties including tree depth (maximum distance from root to leaf), branching statistics (average/max degree of internal nodes), and node label contents (feature IDs, molecular properties used to build the hierarchy). The tree should reflect the chemical substructure similarities predicted by CSI:FingerID or MS2 spectral matches, with internal nodes representing shared molecular properties among child features.

## Related tools

- **q2-qemistree** (Produces the Chemical Feature Tree artifact via make-hierarchy command using predicted molecular substructures (CSI:FingerID fingerprints) and MS1 feature abundance data.) — https://github.com/biocore/q2-qemistree
- **QIIME 2** (Provides artifact inspection, deserialization, and tree manipulation framework; supports reading and validating Phylogeny[Rooted] objects.)
- **SIRIUS / CSI:FingerID** (Predicts molecular substructures (2936 molecular properties or 489 PubChem fingerprint positions) that define the chemical relationships encoded in the tree hierarchy.) — https://bio.informatik.uni-jena.de/sirius/

## Examples

```
qiime tools peek qemistree.qza && python -c "import skbio; tree = skbio.io.read('qemistree.qza', format='qza', constructor=skbio.tree.TreeNode); print(f'Nodes: {len(tree.nodes())}, Depth: {tree.height()}')"
```

## Evaluation signals

- Tree file format validates as valid Newick or QIIME 2 serialized object with no parsing errors.
- All node IDs in the tree match feature identifiers in the accompanying FeatureData[Molecules] artifact.
- Tree is fully connected (no orphaned subtrees) and has exactly one root node with all internal nodes and leaves reachable via unique paths.
- Tree depth and branching statistics are consistent with the number of input features (e.g., depth grows logarithmically with leaf count for balanced trees).
- No duplicate or malformed node labels; internal node labels correspond to inferred molecular properties from CSI:FingerID predictions.

## Limitations

- SIRIUS predicts molecular substructures for only 70–90% of all MS1 features, so some features may be absent from the tree; filtering is applied during make-hierarchy.
- Tree structure depends on CSI:FingerID version and PubChem fingerprint database version (latest release uses PubChem from 13 August 2017); trees from different SIRIUS versions may have different node counts.
- Tree interpretation requires understanding that internal nodes represent shared molecular substructures, not taxonomic ranks; chemical distance does not imply evolutionary relationship.
- Node labels may be ambiguous if features have identical or near-identical molecular fingerprints; inspection of accompanying feature-data (parent_mass, retention_time, csi_smiles) is often needed for disambiguation.

## Evidence

- [readme] A tool to build a tree of mass-spectrometry (LC-MS/MS) features to perform chemically-informed comparison of untargeted metabolomic profiles.: "A tool to build a tree of mass-spectrometry (LC-MS/MS) features to perform chemically-informed comparison of untargeted metabolomic profiles."
- [readme] We use molecular substructures predicted by SIRIUS to build a hierarchy of the MS1 features in a dataset.: "We use molecular substructures predicted by SIRIUS to build a hierarchy of the MS1 features in a dataset."
- [readme] A tree relating the MS1 features in these data based on molecular substructures predicted for MS1 features. This is of type `Phylogeny[Rooted]`. By default, we retain all fingerprint positions i.e. 2936 molecular properties).: "A tree relating the MS1 features based on molecular substructures predicted for MS1 features. This is of type `Phylogeny[Rooted]`. By default, we retain all fingerprint positions i.e. 2936 molecular"
- [readme] SIRIUS predicts molecular substructures for a subset of features (typically for 70-90% of all MS1 features) in an experiment (based on factors such as sample type, the quality MS2 spectra, and user-defined tolerances such as `--p-ppm-max`, `--p-zodiac-threshold`).: "SIRIUS predicts molecular substructures for a subset of features (typically for 70-90% of all MS1 features) in an experiment"
- [other] Parse tree structure and count total nodes (leaves + internal nodes). Verify tree connectivity and absence of malformed branches.: "Parse tree structure and count total nodes (leaves + internal nodes). Verify tree connectivity and absence of malformed branches."
