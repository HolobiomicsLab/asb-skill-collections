---
name: sub-network-detection-from-scored-graphs
description: Use when you have a GLASSO-inferred sparse network graph and associated PCA scores (e.g., from prior dimension reduction of omics or imaging data), and you need to identify which nodes cluster together based on both their PCA score patterns and their connectivity in the graph.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3766
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3391
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3389/fnins.2024.1520982
  all_source_dois:
  - 10.3389/fnins.2024.1520982
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# sub-network-detection-from-scored-graphs

## Summary

Overlay dimensionality-reduced scores (PCA) onto sparse network graphs (GLASSO) to identify and label significant sub-networks based on joint patterns of node attributes and network topology. This skill bridges dimensionality reduction and network community detection to reveal functionally coherent clusters in high-dimensional biological or systems data.

## When to use

You have a GLASSO-inferred sparse network graph and associated PCA scores (e.g., from prior dimension reduction of omics or imaging data), and you need to identify which nodes cluster together based on both their PCA score patterns and their connectivity in the graph. Use this skill when you want to flag sub-networks whose members share both low-dimensional signal (high PCA scores on key components) and structural proximity (edges in the sparse graph).

## When NOT to use

- Input graph is already fully connected or lacks sparse structure; GLASSO is designed for sparse inference, and overlaying scores on dense graphs offers limited insight.
- PCA scores have not been computed or validated; the skill depends on reliable dimensionality reduction upstream.
- You have no a priori reason to expect node-level variation in PCA scores (e.g., all nodes score similarly); the overlay would be uninformative.

## Inputs

- GLASSO-generated network graph (nodes and edges; e.g., adjacency matrix or edge list)
- PCA score matrix (rows = nodes; columns = principal components)
- Node-to-sample/feature mapping (to align scores with graph nodes)

## Outputs

- Annotated network graph with sub-network assignments per node
- Sub-network membership labels and significance scores
- Visualization (rendered image or interactive plot) showing PCA score overlay and sub-network boundaries on the graph
- Optionally: GML, GraphML, or JSON export of annotated graph

## How to apply

Load the GLASSO-generated network graph (nodes and edges) and the associated PCA score matrix from the prior analysis step. Map each PCA score to its corresponding network node and assign scores as node attributes or visual properties (e.g., node color, size). Apply a significance threshold to PCA scores and/or use a community-detection algorithm (e.g., modularity-based, hierarchical clustering, or connected-component analysis) on the scored graph to identify contiguous sub-networks where nodes exceed the threshold or share high co-occurrence. Label and annotate each detected sub-network with its PCA-based signature. Export the annotated graph structure and produce a publication-ready visualization overlaying PCA scores onto the network topology, clearly delineating sub-network boundaries.

## Related tools

- **pcaGLASSO** (Python package that implements the full workflow: GLASSO graph generation, PCA score overlay, and sub-network visualization) — github.com/jlichtarge/pcaGLASSO

## Evaluation signals

- Sub-networks are contiguous in the graph (all nodes within a sub-network are reachable via edges; no disconnected components mislabeled as one sub-network).
- Nodes assigned to the same sub-network have coherent PCA score signatures (low within-sub-network variance on key PCs; high between-sub-network variance).
- The visualization clearly shows spatial separation of sub-networks on the graph and distinguishes node scores by color, size, or label.
- Exported graph file contains valid node/edge data and sub-network membership attributes; round-trip import/export preserves annotations.
- Significance threshold or community-detection parameters are documented and reproducible (threshold value, algorithm name, hyperparameters all recorded).

## Limitations

- The method is sensitive to the choice of significance threshold and community-detection algorithm; different thresholds or algorithms may yield different sub-network boundaries.
- GLASSO sparsity and PCA dimensionality are both upstream parameters that affect the quality of sub-network detection; poor or overfitted priors upstream propagate downstream.
- Sub-network detection assumes that PCA scores and graph topology are both meaningful signals; if either is noisy or misspecified, sub-networks may be artifacts.
- Visualization scalability is limited for very large networks (>10,000 nodes); readability degrades without specialized layout or filtering strategies.

## Evidence

- [intro] Graphs generated by GLASSO are overlaid with PCA scores to identify significant sub-networks.: "Graphs generated by GLASSO are overlaid with PCA scores to identify significant sub-networks."
- [other] Map PCA scores to network nodes and overlay the scores as node attributes or visual properties onto the graph structure.: "Map PCA scores to network nodes and overlay the scores as node attributes or visual properties onto the graph structure."
- [other] Apply a significance threshold or community-detection algorithm to identify and label sub-networks based on PCA score patterns and network topology.: "Apply a significance threshold or community-detection algorithm to identify and label sub-networks based on PCA score patterns and network topology."
- [readme] A python package to visualize networks.: "A python package to visualize networks."
