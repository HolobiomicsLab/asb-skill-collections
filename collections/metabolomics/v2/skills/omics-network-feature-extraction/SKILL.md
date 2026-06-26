---
name: omics-network-feature-extraction
description: Use when after you have built a network object (adjacency matrix, edge
  list, or correlation output) from omics data and need to quantitatively describe
  network properties beyond visualization.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3562
  edam_topics:
  - http://edamontology.org/topic_3673
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3390
  tools:
  - MetaNet
  - R
  - pcutils
  - igraph
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1101/2025.06.26.661636v1
  title: MetaNet
evidence_spans:
- MetaNet, a high-performance R package that unifies network construction, visualization,
  and analysis across diverse omics layers.
- MetaNet, a high-performance R package that unifies network construction, visualization,
  and analysis across diverse omics layers
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

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Extract and aggregate comprehensive topological and stability metrics from a constructed omics network to quantify node-level and global network properties. This skill enables characterization of network robustness, centrality, clustering, and perturbation-response behavior—essential for identifying hub features and assessing network fragility in multi-omics datasets.

## When to use

Apply this skill after you have built a network object (adjacency matrix, edge list, or correlation output) from omics data and need to quantitatively describe network properties beyond visualization. Use it when comparing networks across conditions, identifying critical nodes for follow-up validation, or documenting network robustness as part of reproducible reporting.

## When NOT to use

- Input is a raw correlation matrix without network construction; first call c_net_build() or equivalent to threshold edges before metrics extraction.
- Network object has fewer than 3 nodes; most topological metrics become undefined or trivial below this threshold.
- You require only visualization or layout; metrics extraction is unnecessary if the goal is static plotting alone.

## Inputs

- network object (igraph format or MetaNet metanet class)
- adjacency matrix or edge list representation
- correlation matrix output from c_net_calculate() or equivalent

## Outputs

- structured metrics table (rows = nodes or network; columns = metric names and values)
- delimited or Excel file (.csv, .xlsx) with aggregated metrics
- topological metric vectors (degree, centrality, clustering coefficient, path length per node)
- stability metrics (network robustness indices, perturbation-response values)

## How to apply

Invoke MetaNet's metrics module on your constructed network object to compute topological metrics (degree, centrality measures, clustering coefficient, path length) and stability assessment functions (network robustness, perturbation-response metrics). For each node or the full network, record metric values in a structured table (rows = nodes or network-level properties; columns = metric names). Aggregate results and export as a delimited or Excel file. Interpret metric distributions to identify hub nodes (high degree/centrality), modular structure (clustering coefficient), and fragility hotspots (perturbation sensitivity).

## Related tools

- **MetaNet** (Primary package providing metrics module and stability assessment functions for topological and robustness quantification) — https://github.com/Asa12138/MetaNet
- **igraph** (Underlying graph library on which MetaNet's core functionality is built; used internally for metric computation)
- **pcutils** (Companion utility package for data manipulation and pre/post-processing of network tables) — https://github.com/Asa12138/pcutils
- **R** (Host language and environment for executing MetaNet metric functions)

## Examples

```
# Construct network, then compute and export metrics
net <- c_net_build(cor, r_threshold = 0.65)
# Compute topological metrics (degree, centrality, clustering, path length are typically computed internally)
# Export aggregated metrics table
metrics_table <- data.frame(node = V(net)$name, degree = degree(net))
write.csv(metrics_table, 'network_metrics.csv', row.names = FALSE)
```

## Evaluation signals

- Metrics table is non-empty, rectangular (all rows same column count), and contains numeric values for all topological and stability metrics.
- Node-level metrics (degree, centrality, clustering) are within plausible ranges (e.g., degree ≤ network size − 1; clustering coefficient ∈ [0, 1]).
- Metrics correlate logically (e.g., hub nodes with high degree also show high centrality; densely connected regions show elevated clustering).
- Exported file is readable in downstream tools (R, Python, Excel) and retains row/column structure without truncation or encoding errors.
- Network-level summary statistics (mean degree, average path length, global clustering coefficient) match independent calculations on the adjacency matrix.

## Limitations

- Metric computation scales with network size; MetaNet optimizes for datasets with >10,000 features, but very dense networks (edge-heavy) may still incur high memory or runtime cost.
- Perturbation-response metrics depend on simulation parameters and random seed; reproducibility requires seed fixing and explicit parameter documentation.
- Path length and diameter metrics are undefined or infinite in disconnected networks; pre-filter to the largest connected component or document missing values.
- Topological metrics are most interpretable on networks with correlation thresholds tuned to biological relevance; arbitrary low thresholds produce dense, less discriminative networks.

## Evidence

- [other] MetaNet provides comprehensive topological and stability metrics as part of its network analysis capabilities for in-depth network characterization.: "It further offers comprehensive topological and stability metrics for in-depth network characterization."
- [other] The workflow includes invoking MetaNet's metrics module to compute degree, centrality, clustering coefficient, path length, robustness and perturbation-response metrics.: "Invoke MetaNet's metrics module to compute comprehensive topological metrics (e.g., degree, centrality, clustering coefficient, path length). 3. Invoke MetaNet's stability assessment functions to"
- [other] Results are aggregated into a structured table with rows = nodes or network properties and columns = metric names and values, then exported as delimited or Excel file.: "Aggregate all computed metrics into a structured table (rows = nodes or network properties; columns = metric names and values). 5. Export the metrics table as a delimited or Excel file for downstream"
- [readme] MetaNet's architecture comprises core functional modules including Topology analysis and Stability analysis, supporting end-to-end analytical process from network construction to characterization.: "Its architecture comprises several core functional modules: Calculation, Manipulation, Layout, Visualization, Topology analysis, Module analysis, Stability analysis, and I/O (Figure 1A), supporting"
