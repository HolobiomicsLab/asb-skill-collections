---
name: graph-community-detection
description: Use when you have a sparse inverse covariance graph (GLASSO output) and
  multivariate PCA scores for the same samples/variables, and you need to partition
  the network into functionally or statistically coherent sub-networks rather than
  treating the graph as a monolithic structure.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3920
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3572
  tools:
  - Python
  - pcaGLASSO
  license_tier: restricted
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# graph-community-detection

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Identify and label significant sub-networks within GLASSO-generated correlation graphs by overlaying PCA scores and applying community-detection algorithms. This skill reveals latent modular structure in high-dimensional biological or systems data.

## When to use

Apply this skill when you have a sparse inverse covariance graph (GLASSO output) and multivariate PCA scores for the same samples/variables, and you need to partition the network into functionally or statistically coherent sub-networks rather than treating the graph as a monolithic structure.

## When NOT to use

- Input graph is already a hierarchical tree or pre-defined module assignment (use skill only for unsupervised discovery from raw GLASSO output).
- PCA scores are not derived from the same data matrix used to generate the GLASSO graph (score-to-node mapping will be invalid).
- Network has < 10 nodes or is fully connected; community detection algorithms require sufficient sparsity and size to be meaningful.

## Inputs

- GLASSO-generated sparse inverse covariance graph (edge list or adjacency matrix)
- PCA scores matrix (samples × principal components or nodes × PCs)
- Node identifiers (variable/gene names matching graph nodes)

## Outputs

- Annotated graph with sub-network cluster assignments
- Sub-network membership table (node → cluster_id)
- Visualization of overlay (network graph with PCA score-colored nodes and sub-network boundaries highlighted)

## How to apply

Load the GLASSO-generated network graph and associated PCA scores from the prior dimensionality reduction step. Map PCA scores to network nodes and overlay them as node attributes or visual properties (e.g., color, size) onto the graph structure. Apply a significance threshold or community-detection algorithm (e.g., modularity optimization, hierarchical clustering on the combined graph-PCA feature space) to identify clusters of nodes that exhibit coherent PCA score patterns and are topologically connected. Export the annotated graph with sub-network assignments and produce a visualization showing both the network topology and the overlaid PCA score patterns to validate that sub-networks are interpretable.

## Related tools

- **pcaGLASSO** (Python package for overlaying PCA scores onto GLASSO graphs and identifying sub-networks) — github.com/jlichtarge/pcaGLASSO

## Evaluation signals

- Sub-network assignments are non-trivial: no single cluster contains >80% of nodes, and modularity or silhouette score exceeds baseline (random partitioning).
- Overlaid PCA scores show coherent patterns within sub-networks (e.g., nodes in the same cluster have similar PC values; inter-cluster differences are significant by t-test or ANOVA).
- Sub-network structure is reproducible: re-running the algorithm with small parameter perturbations (e.g., ±10% threshold) yields Adjusted Rand Index > 0.7 with the original partition.
- Network visualization is interpretable: exported graph clearly delineates sub-networks by spatial layout or color, and node positions correlate with PCA scores.
- Sub-network size distribution is reasonable: no single cluster is a singleton, and the number of clusters is stable across reasonable algorithm hyperparameter ranges.

## Limitations

- No changelog or versioning information available for the pcaGLASSO package, limiting reproducibility and change tracking.
- Method assumes PCA is an appropriate dimensionality reduction for the data; if data violates PCA assumptions (e.g., non-linear or heavy-tailed), PCA scores may not align with network modularity.
- Community detection is sensitive to algorithm choice and hyperparameter tuning (e.g., significance threshold, clustering method); results may vary with different tools or thresholds.
- GLASSO sparsity is controlled by regularization parameter λ; sub-networks are artifacts of the chosen λ and may differ substantially with alternative regularization settings.

## Evidence

- [readme] Graphs generated by GLASSO are overlaid with PCA scores to identify significant sub-networks: "Graphs generated by GLASSO are overlaid with PCA scores to identify significant sub-networks"
- [other] Map PCA scores to network nodes and overlay the scores as node attributes or visual properties onto the graph structure. Apply a significance threshold or community-detection algorithm to identify and label sub-networks based on PCA score patterns and network topology.: "Map PCA scores to network nodes and overlay the scores as node attributes or visual properties onto the graph structure. Apply a significance threshold or community-detection algorithm to identify"
- [other] Load the GLASSO-generated network graph and associated PCA scores from the prior step.: "Load the GLASSO-generated network graph and associated PCA scores from the prior step."
- [other] Export the annotated graph with sub-network assignments and produce a visualization showing the overlay.: "Export the annotated graph with sub-network assignments and produce a visualization showing the overlay."
