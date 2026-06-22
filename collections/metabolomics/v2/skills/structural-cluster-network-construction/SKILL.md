---
name: structural-cluster-network-construction
description: Use when after you have identified statistically significant LC-MS features and run MamsiStructSearch to generate structural clusters (isotopologue groups, adduct groups, cross-assay links) and computed correlation cluster assignments.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3083
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - pyvis
  - pandas
  - Cytoscape
  - networkx
  - MAMSI MamsiStructSearch
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.5c01327
  title: mamsi
- doi: 10.1371/journal.pcbi.1011814
  title: ''
evidence_spans:
- MAMSI is a Python framework
- The graph can be displayed interactively using pyvis.network
- import pandas as pd
- You can also save the network as an NX object and review in [Cytoscape](https://cytoscape.org)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mamsi
    doi: 10.1021/acs.analchem.5c01327
    title: mamsi
  dedup_kept_from: coll_mamsi
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c01327
  all_source_dois:
  - 10.1021/acs.analchem.5c01327
  - 10.1371/journal.pcbi.1011814
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Reconstruct the structural network graph generation from significant features

## Summary

Convert structural cluster assignments (isotopologues, adducts, cross-assay links) and correlation cluster memberships into an interactive NetworkX graph, then visualize in Cytoscape or pyvis for interactive exploration of metabolite structural relationships.

## When to use

After you have identified statistically significant LC-MS features and run MamsiStructSearch to generate structural clusters (isotopologue groups, adduct groups, cross-assay links) and computed correlation cluster assignments. Use this skill when you need to understand and communicate the topology of structural relationships among features—which features are linked by isotopologue signatures, adducts, or assay co-membership—and when interactive or programmatic graph analysis is required downstream.

## When NOT to use

- Input feature set has no structural clusters or cross-feature links (isolated features only)—network will be disconnected and visualization will not reveal relationships.
- You require static, publication-ready network diagrams with fine-grained layout control—pyvis interactive HTML is exploratory, not optimized for print.
- Input is already a pre-constructed NetworkX or Cytoscape session file; re-running construction will overwrite custom layouts or annotations.

## Inputs

- Structural cluster assignments (isotopologue groups, adduct groups, cross-assay links) from MamsiStructSearch
- Correlation cluster assignments from hierarchical clustering (output of get_correlation_clusters)
- Feature metadata table (m/z, retention time, assay origin, compound annotations)
- Selected LC-MS feature matrix (rows=samples, columns=significant features)

## Outputs

- NetworkX graph object (nx.Graph) with features as nodes and structural links as weighted edges
- Interactive HTML network visualization (pyvis format) with spring layout and cluster-based node coloring
- Network node and edge attributes (assay, m/z, RT, cluster IDs, link types and weights)

## How to apply

Load structural cluster data (isotopologue groups, adduct groups, and cross-assay links) along with correlation cluster assignments from MamsiStructSearch outputs. Create a NetworkX graph with features as nodes, assigning node attributes (assay, m/z, retention time, cluster membership, compound annotation) extracted from feature metadata. Add edges between nodes based on structural link type: assign weight 1 for isotopologue links, weight 5 for adduct links, weight 10 for cross-assay links, and weight 15 for correlation cluster co-membership. Optionally filter to structurally linked features only via the include_all parameter (set to False to exclude isolated features). Generate an interactive pyvis.network visualization with spring layout, coloring nodes by correlation cluster membership, and scaling edge thickness proportional to link weight. Save the visualization as an HTML artifact and return the NetworkX object for downstream curation in Cytoscape or additional programmatic analysis.

## Related tools

- **networkx** (Create and manipulate graph objects with features as nodes and structural links as weighted edges; assign node and edge attributes) — https://networkx.org/
- **pyvis** (Generate interactive HTML network visualization with spring layout, node coloring by cluster membership, and edge thickness proportional to link weight) — https://pyvis.readthedocs.io/
- **Cytoscape** (Import NetworkX graph for interactive network curation, manual layout refinement, and downstream topological analysis) — https://cytoscape.org
- **pandas** (Load and manipulate feature metadata and cluster assignment tables for graph node attribute construction) — https://pandas.pydata.org/
- **MAMSI MamsiStructSearch** (Generate structural cluster assignments (isotopologue, adduct, cross-assay links) and correlation cluster memberships that feed into graph construction) — https://github.com/kopeckylukas/py-mamsi

## Examples

```
struct = MamsiStructSearch(rt_win=5, ppm=10)
struct.load_lcms(selected)
struct.get_structural_clusters()
struct.get_correlation_clusters(flat_method='silhouette', max_clusters=11)
network = struct.get_structural_network(include_all=True, interactive=False, labels=True, return_nx_object=True)
```

## Evaluation signals

- NetworkX graph contains all input features as nodes with m/z, RT, assay, cluster ID attributes populated from metadata.
- Edge weights are assigned correctly: 1 for isotopologue, 5 for adduct, 10 for cross-assay, 15 for correlation cluster co-membership; check by inspecting edge list or `nx.get_edge_attributes(graph, 'weight')`.
- Interactive pyvis HTML displays nodes colored by correlation cluster membership (distinct colors per cluster) with edge thickness visually proportional to weight.
- Graph connectivity and node degree distribution match expected structural relationships—isolated features have degree 0 if include_all=False, or are present but unconnected if include_all=True.
- NetworkX object can be exported (e.g., `nx.write_graphml()` or `nx.write_gexf()`) and opened in Cytoscape without error, preserving all node and edge attributes.

## Limitations

- Spring layout in pyvis is stochastic and may produce different visual arrangements across runs; reproducibility requires fixing random seed or manual layout refinement in Cytoscape.
- Edge weight scaling is relative; absolute visual thickness depends on chosen weight range and pyvis rendering parameters—interpretation requires explicit reference to weight legend.
- Isolated features (no structural links) are included only if include_all=True; excluding them (include_all=False) may hide potential annotation candidates or quality-control failures.
- Cross-assay link detection relies on [M+H]+/[M-H]− reference matching; misalignment or assay-specific adducts not in the common set may be missed.
- Large feature sets (>1000 features) may produce unreadable pyvis HTML visualizations; programmatic analysis via NetworkX or export to Cytoscape is recommended for large networks.

## Evidence

- [intro] structural cluster assignments into an interactive network graph representation suitable for visualization and analysis: "How does MAMSI convert structural cluster assignments into an interactive network graph representation suitable for visualization and analysis?"
- [methods] Create NetworkX graph with features as nodes, assigning node attributes (assay, m/z, retention time, cluster membership, compound annotation) extracted from feature metadata.: "Create NetworkX graph with features as nodes, assigning node attributes (assay, m/z, retention time, cluster membership, compound annotation) extracted from feature metadata."
- [methods] Add edges between nodes based on structural link type: assign weight 1 for isotopologue links, weight 5 for adduct links, weight 10 for cross-assay links, and weight 15 for correlation cluster co-membership.: "Add edges between nodes based on structural link type: assign weight 1 for isotopologue links, weight 5 for adduct links, weight 10 for cross-assay links, and weight 15 for correlation cluster"
- [methods] Generate interactive pyvis.network visualization with spring layout, node coloring by correlation cluster membership, and edge thickness proportional to link weight; save as HTML artifact.: "Generate interactive pyvis.network visualization with spring layout, node coloring by correlation cluster membership, and edge thickness proportional to link weight; save as HTML artifact."
- [readme] You can also save the network as an NX object and review in Cytoscape to get better insight on what the structural relationships between individual features are (e.g. adduct links, isotopologues, cross-assay links).: "You can also save the network as an NX object and review in Cytoscape to get better insight on what the structural relationships between individual features are (e.g. adduct links, isotopologues,"
- [readme] network = struct.get_structural_network(include_all=True, interactive=False, labels=True, return_nx_object=True): "network = struct.get_structural_network(include_all=True, interactive=False, labels=True, return_nx_object=True)"
