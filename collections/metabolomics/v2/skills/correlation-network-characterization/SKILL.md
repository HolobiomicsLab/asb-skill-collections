---
name: correlation-network-characterization
description: Use when after constructing a correlation-based network (adjacency matrix, edge list, or correlation-thresholded output) and you need to quantify its structural properties—such as which nodes are most central, how tightly clustered communities are, or how the network responds to perturbation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3452
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

# Reconstruct topological and stability metric computation for a constructed network

## Summary

Compute comprehensive topological and stability metrics from a network object to characterize network properties, including degree, centrality, clustering coefficients, path lengths, and robustness measures. This skill quantifies structural and dynamic properties essential for interpreting biological or systems networks.

## When to use

Apply this skill after constructing a correlation-based network (adjacency matrix, edge list, or correlation-thresholded output) and you need to quantify its structural properties—such as which nodes are most central, how tightly clustered communities are, or how the network responds to perturbation. Use it when reporting network-level summaries or when filtering/ranking nodes by their topological role.

## When NOT to use

- Input is a raw, unthresholded correlation matrix; threshold and build a network object first using c_net_build().
- You only need to visualize the network layout; use layout functions (g_layout_*) instead.
- Data is already a pre-computed metric table; you are importing external metrics, not computing them de novo.

## Inputs

- Network object (igraph-compatible metanet class)
- Adjacency matrix or edge list with correlation weights
- Correlation matrix with p-values (from c_net_calculate output)

## Outputs

- Metrics table (data.frame: rows=nodes/properties, columns=metric values)
- Delimited or Excel file (.csv, .xlsx) of node- and network-level metrics
- Structured summary of topological properties (degree, centrality, clustering)
- Stability/robustness assessment metrics (perturbation-response values)

## How to apply

Load or construct a network object in MetaNet (adjacency matrix, edge list, or correlation output with a specified r_threshold, e.g., r ≥ 0.6). Invoke MetaNet's metrics module (e.g., degree(), centrality measures) to compute topological metrics such as degree, betweenness centrality, clustering coefficient, and path length. Separately invoke MetaNet's stability assessment functions to compute network robustness and perturbation-response metrics characterizing how the network degrades under node or edge removal. Aggregate all computed metrics into a structured table (rows = nodes or global network properties; columns = metric names and values). Export the metrics table as a delimited (CSV/TSV) or Excel file for downstream filtering, ranking, visualization, or statistical analysis.

## Related tools

- **MetaNet** (Core package for network construction, metrics computation, and stability analysis across omics layers) — https://github.com/Asa12138/MetaNet
- **igraph** (Underlying graph library providing core topological metric algorithms (degree, centrality, clustering) used by MetaNet)
- **pcutils** (Utility package providing data manipulation and I/O support for MetaNet workflows) — https://github.com/Asa12138/pcutils
- **R** (Programming language and environment in which MetaNet and metric computation functions execute)

## Examples

```
library(MetaNet); cor <- c_net_calculate(totu); net <- c_net_build(cor, r_threshold = 0.65); metrics <- c_net_metric(net); write.csv(metrics, 'network_metrics.csv')
```

## Evaluation signals

- Metrics table has the expected number of rows (one per node, or one global summary row) and columns (one per metric name); no NaN or Inf values except where theoretically justified.
- Degree values are non-negative integers ≤ network size; centrality measures are normalized to [0, 1] or equivalent scale.
- Clustering coefficients fall in [0, 1]; path lengths are positive numbers or infinite for disconnected pairs.
- Stability metrics show monotonic degradation (e.g., robustness decreases) as perturbation intensity increases; network metrics remain consistent across re-runs on the same input.
- Exported file is parseable (valid CSV/Excel); column names match metric names used in downstream analyses or publications.

## Limitations

- Topological metrics assume the input network is well-formed (connected or weakly connected); isolated nodes or disconnected components may yield undefined path lengths or centrality scores.
- Metric computation scales with network size; for very large networks (>10,000 nodes), some algorithms (e.g., all-pairs shortest paths) may be slow; MetaNet provides optimized implementations but users should verify runtime on their data.
- Stability metrics (robustness, perturbation-response) depend on the removal strategy (random vs. targeted); results are not comparable across different perturbation models without explicit documentation.
- Correlation-based networks are sensitive to threshold choice (r_threshold); changing the threshold produces different topologies and metrics; threshold selection should be justified a priori or reported as a sensitivity analysis.

## Evidence

- [intro] MetaNet offers comprehensive topological and stability metrics for in-depth network characterization.: "It further offers comprehensive topological and stability metrics for in-depth network characterization."
- [other] Invoke MetaNet's metrics module to compute comprehensive topological metrics and stability assessment functions for network robustness.: "Invoke MetaNet's metrics module to compute comprehensive topological metrics (e.g., degree, centrality, clustering coefficient, path length). 3. Invoke MetaNet's stability assessment functions to"
- [other] Aggregate metrics into a structured table and export for downstream analysis.: "Aggregate all computed metrics into a structured table (rows = nodes or network properties; columns = metric names and values). 5. Export the metrics table as a delimited or Excel file for downstream"
- [readme] MetaNet architecture comprises topology analysis and stability analysis modules.: "Its architecture comprises several core functional modules: Calculation, Manipulation, Layout, Visualization, Topology analysis, Module analysis, Stability analysis, and I/O"
