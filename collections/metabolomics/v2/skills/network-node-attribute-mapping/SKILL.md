---
name: network-node-attribute-mapping
description: Use when you have a GLASSO-generated network graph and corresponding PCA scores from a prior dimensionality-reduction step, and you need to identify which nodes or sub-networks are associated with high or significant PCA scores.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3562
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - pcaGLASSO
derived_from:
- doi: 10.3389/fnins.2024.1520982
  title: MetaboLINK/ PCA-GLASSO
evidence_spans:
- A python package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metabolink_pca_glasso_cq
    doi: 10.3389/fnins.2024.1520982
    title: MetaboLINK/ PCA-GLASSO
  dedup_kept_from: coll_metabolink_pca_glasso_cq
schema_version: 0.2.0
---

# network-node-attribute-mapping

## Summary

Map computed scores (e.g., PCA scores) to network nodes and overlay them as visual or structural attributes to enable identification of significant sub-networks. This skill bridges dimensionality-reduction results with graph topology to reveal patterns in network structure.

## When to use

You have a GLASSO-generated network graph and corresponding PCA scores from a prior dimensionality-reduction step, and you need to identify which nodes or sub-networks are associated with high or significant PCA scores. Use this skill when visual or topological inspection of score-to-node correspondence is necessary to flag functionally coherent sub-networks.

## When NOT to use

- The input graph is not derived from GLASSO (different network inference method may have different edge semantics or reliability assumptions).
- PCA scores have not been computed or are not aligned to the same node set as the network.
- The goal is only to visualize the network topology without incorporating external score information.

## Inputs

- GLASSO-generated network graph (node–edge list or adjacency matrix)
- PCA score vector aligned to graph nodes
- Node identifier mapping (to align scores to graph structure)

## Outputs

- Annotated graph object with PCA scores as node attributes
- Sub-network assignments (node-to-subnetwork mapping)
- Visualization of overlaid PCA scores on network topology
- Exported annotated graph file (e.g., GraphML, GML, or adjacency list with attributes)

## How to apply

Load the GLASSO-generated network graph structure and the associated PCA score vector into the same computational context (e.g., Python with networkx or igraph). Map each PCA score to its corresponding node by matching node IDs, then assign scores as node attributes (e.g., node properties or visual properties such as color, size, or label). Apply a significance threshold or community-detection algorithm to cluster nodes by PCA score patterns and network topology; nodes with similar high scores and direct connectivity form sub-network candidates. Export the annotated graph (with sub-network labels and score metadata) and generate a visualization showing the overlay, typically as a node-colored or node-sized graph where visual prominence indicates score magnitude.

## Related tools

- **pcaGLASSO** (Python package that performs PCA-score-to-GLASSO-graph overlay and sub-network identification) — https://github.com/jlichtarge/pcaGLASSO

## Evaluation signals

- All nodes in the graph have been assigned a PCA score attribute and no nodes are left unmapped.
- Sub-networks identified by the method show higher internal edge density and score homogeneity than random node groups of the same size.
- Visualization renders without errors, node visual properties (color/size) correlate monotonically with PCA score magnitude.
- Exported graph file contains complete node attribute tables and sub-network labels; reimporting and spot-checking a sample of nodes confirms correct score mapping.
- Significance threshold or community-detection parameters are documented and reproducible; re-running with the same parameters yields identical sub-network assignments.

## Limitations

- Requires GLASSO graph and PCA scores to be pre-computed; this skill does not generate them.
- Quality and interpretability depend on the quality of the upstream GLASSO network inference and PCA dimensionality reduction.
- No changelog documented for the pcaGLASSO package, limiting traceability of changes or known issues.
- Threshold selection for significance filtering is not fully specified; practitioners must justify their choice or use automated community-detection.
- Visualization scalability may be limited for very large networks (thousands of nodes).

## Evidence

- [other] Map PCA scores to network nodes and overlay the scores as node attributes or visual properties onto the graph structure.: "Map PCA scores to network nodes and overlay the scores as node attributes or visual properties onto the graph structure."
- [other] Apply a significance threshold or community-detection algorithm to identify and label sub-networks based on PCA score patterns and network topology.: "Apply a significance threshold or community-detection algorithm to identify and label sub-networks based on PCA score patterns and network topology."
- [readme] Graphs generated by GLASSO are overlaid with PCA scores to identify significant sub-networks.: "Graphs generated by GLASSO are overlaid with PCA scores to identify significant sub-networks."
- [other] Export the annotated graph with sub-network assignments and produce a visualization showing the overlay.: "Export the annotated graph with sub-network assignments and produce a visualization showing the overlay."
