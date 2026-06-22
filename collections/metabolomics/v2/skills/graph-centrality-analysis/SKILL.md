---
name: graph-centrality-analysis
description: Use when after constructing a network (adjacency matrix, edge list, or correlation network) when you need to identify which nodes are most central to network topology.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_0128
  - http://edamontology.org/topic_3674
  tools:
  - MetaNet
  - R
  - pcutils
  - igraph
derived_from:
- doi: 10.1101/2025.06.26.661636v1
  title: MetaNet
evidence_spans:
- MetaNet, a high-performance R package that unifies network construction, visualization, and analysis across diverse omics layers.
- MetaNet, a high-performance R package that unifies network construction, visualization, and analysis across diverse omics layers
- MetaNet, a high-performance R package
- devtools::install_github("Asa12138/pcutils")
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metanet_cq
    doi: 10.1101/2025.06.26.661636v1
    title: MetaNet
  dedup_kept_from: coll_metanet_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2025.06.26.661636v1
  all_source_dois:
  - 10.1101/2025.06.26.661636v1
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# graph-centrality-analysis

## Summary

Compute node-level centrality metrics (degree, betweenness, closeness, eigenvector centrality) from a network object to identify topologically influential nodes. This skill is essential for ranking nodes by their structural importance in network characterization and for prioritizing hub or bridge nodes in multi-omics networks.

## When to use

Apply this skill after constructing a network (adjacency matrix, edge list, or correlation network) when you need to identify which nodes are most central to network topology. Use it when your analysis goal is to rank nodes by influence, find hub metabolites or genes, or detect bottleneck species in microbial networks. Centrality analysis is particularly valuable in multi-omics integration to highlight which features bridge different omics layers.

## When NOT to use

- The network is extremely sparse (fewer than 10 nodes or disconnected components) where centrality metrics may not be interpretable.
- Your goal is community detection rather than node ranking—use c_net_module() instead.
- You only need edge weights or correlation strength; centrality analysis adds no value if topology is not the analysis goal.

## Inputs

- network object (MetaNet class, igraph object, or adjacency matrix)
- constructed network from c_net_build() or multi_net_build() output

## Outputs

- centrality metrics table (rows = nodes; columns = degree, betweenness, closeness, eigenvector centrality, or custom metrics)
- ranked node list by centrality score
- delimited or Excel file with aggregated metrics

## How to apply

Load or construct a network object in MetaNet (from adjacency matrix, edge list, or correlation output). Invoke MetaNet's centrality functions from its metrics module—the igraph-based backend computes standard measures including degree (count of incident edges), betweenness (number of shortest paths passing through the node), closeness (inverse of average distance to all other nodes), and eigenvector centrality (influence based on connections to high-influence neighbors). Aggregate computed centrality scores into a structured table with rows = nodes and columns = centrality metric names and values. Export the centrality table as a delimited or Excel file for downstream ranking, visualization, or downstream filtering by threshold (e.g., degree > 90th percentile for hub detection).

## Related tools

- **MetaNet** (R package providing metrics module with centrality and topological analysis functions; core computation engine for degree, betweenness, closeness, and eigenvector centrality on network objects) — https://github.com/Asa12138/MetaNet
- **igraph** (Underlying graph library used by MetaNet for network representation and centrality computation; accessed via MetaNet's wrapper functions)
- **pcutils** (Utility R package for data manipulation and export; used in conjunction with MetaNet for aggregating and writing metrics tables) — https://github.com/Asa12138/pcutils
- **R** (Programming language and environment hosting MetaNet and enabling interactive centrality computation and table export)

## Examples

```
library(MetaNet); net <- c_net_build(cor, r_threshold = 0.65); metrics <- data.frame(degree = degree(net), betweenness = betweenness(net)); write.csv(metrics, 'centrality_metrics.csv')
```

## Evaluation signals

- Centrality metrics table has no missing or NaN values for all nodes; sum of degrees equals 2 × number of edges (invariant).
- Degree values are non-negative integers and match edge count visible in the network object.
- Betweenness and closeness centrality values fall within expected ranges (betweenness: [0, n(n−1)/2]; closeness: (0, 1] for connected graphs).
- Hub nodes identified by high degree or betweenness correspond to known influential features in domain literature (e.g., abundant species, ubiquitous metabolites in metabolomics).
- Centrality metrics exported to file preserve node names and match node order in the original network object.

## Limitations

- Centrality metrics are topology-only and do not account for edge weights (correlation strength); use weighted centrality variants if edge correlation magnitude is biologically relevant.
- In disconnected networks or networks with multiple components, closeness centrality may be undefined or uninformative for nodes in separate components.
- Eigenvector centrality is undefined for disconnected graphs and can be unstable in graphs with very small diameter; igraph may return NaN or require damping factor tuning.
- High-dimensional omics networks (>10,000 nodes) may produce computational overhead; MetaNet is optimized for scalability but real-time re-computation on very large networks may be slow.

## Evidence

- [intro] It further offers comprehensive topological and stability metrics for in-depth network characterization.: "It further offers comprehensive topological and stability metrics for in-depth network characterization."
- [other] Invoke MetaNet's metrics module to compute comprehensive topological metrics (e.g., degree, centrality, clustering coefficient, path length).: "Invoke MetaNet's metrics module to compute comprehensive topological metrics (e.g., degree, centrality, clustering coefficient, path length)."
- [other] Aggregate all computed metrics into a structured table (rows = nodes or network properties; columns = metric names and values).: "Aggregate all computed metrics into a structured table (rows = nodes or network properties; columns = metric names and values)."
- [readme] its core functionality is built upon the widely used igraph package. Its architecture comprises several core functional modules: Calculation, Manipulation, Layout, Visualization, Topology analysis, Module analysis, Stability analysis, and I/O: "its core functionality is built upon the widely used igraph package. Its architecture comprises several core functional modules: Calculation, Manipulation, Layout, Visualization, Topology analysis,"
