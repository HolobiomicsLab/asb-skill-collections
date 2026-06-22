---
name: graph-node-edge-attribute-assignment
description: Use when you have statistically significant LC-MS features grouped into structural clusters (isotopologue groups, adduct groups, cross-assay links) and correlation cluster assignments from upstream MamsiStructSearch, and you need to create an interactive graph representation suitable for Cytoscape.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - pyvis
  - pandas
  - Cytoscape
  - NetworkX
  - MamsiStructSearch
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

# graph-node-edge-attribute-assignment

## Summary

Construct a NetworkX graph representation of mass spectrometry feature relationships by assigning nodes for individual features and edges for structural links (isotopologue, adduct, cross-assay, correlation), with typed weights and metadata attributes. This enables interactive visualization and systematic network analysis of metabolomic structural associations.

## When to use

You have statistically significant LC-MS features grouped into structural clusters (isotopologue groups, adduct groups, cross-assay links) and correlation cluster assignments from upstream MamsiStructSearch, and you need to create an interactive graph representation suitable for Cytoscape review or programmatic curation of feature relationships.

## When NOT to use

- Input features have not yet been partitioned into structural clusters (isotopologue, adduct, cross-assay searches must be complete first).
- Feature metadata is incomplete or lacks critical fields (assay, m/z, retention time) needed for node attributes.
- Graph scale exceeds ~5,000 nodes; pyvis spring layout and interactive rendering become computationally intractable.

## Inputs

- isotopologue cluster assignments (feature pairs with 1.00335 Da mass differences)
- adduct cluster assignments (features with matching hypothetical neutral masses within 15 ppm tolerance)
- cross-assay cluster links ([M+H]+/[M-H]- reference pairs)
- correlation cluster membership assignments (from hierarchical clustering with silhouette or other flat method)
- feature metadata table (assay, m/z, retention time, annotation)

## Outputs

- NetworkX graph object with typed nodes and weighted edges
- interactive pyvis.network HTML visualization (spring layout with node colors and edge weights)
- edge list with link type and weight annotations

## How to apply

Load structural cluster data and correlation cluster assignments from MamsiStructSearch outputs. Create a NetworkX graph with each feature as a node, assigning node attributes from feature metadata (assay identifier, m/z, retention time, cluster membership, compound annotation). Add edges between nodes based on link type: assign weight 1 for isotopologue links, weight 5 for adduct links, weight 10 for cross-assay links, and weight 15 for correlation cluster co-membership. Optionally filter to structurally linked features only using the include_all parameter, or retain all features. Generate interactive pyvis.network visualization with spring layout, node coloring by correlation cluster, and edge thickness proportional to link weight; save as HTML. Return the NetworkX object for downstream curation or additional analysis.

## Related tools

- **NetworkX** (Core library for constructing, manipulating, and analyzing the feature relationship graph)
- **pyvis** (Generates interactive network visualization with spring layout, node coloring, and edge weight representation as HTML artifact)
- **Cytoscape** (Desktop platform for downstream review, curation, and interactive exploration of the saved NetworkX object) — https://cytoscape.org
- **MamsiStructSearch** (Upstream tool that produces structural cluster assignments and correlation clusters required as input) — https://github.com/kopeckylukas/py-mamsi
- **pandas** (Stores and manipulates feature metadata and cluster assignment tables)

## Examples

```
network = struct.get_structural_network(include_all=True, interactive=False, labels=True, return_nx_object=True)
```

## Evaluation signals

- NetworkX graph contains a node for each input feature; node count matches feature metadata table row count.
- All edges are present and correctly typed: each isotopologue link has weight 1, each adduct link weight 5, each cross-assay link weight 10, each correlation cluster co-membership link weight 15.
- Node attributes (assay, m/z, retention time, cluster membership, annotation) are populated from input metadata and accessible via NetworkX node attribute dictionary.
- Interactive HTML visualization renders without errors; nodes are color-coded by correlation cluster membership and edge thickness is visually proportional to weight.
- NetworkX object can be serialized and reloaded in Cytoscape or via programmatic nx.read_graphml()/nx.write_graphml() without loss of attributes or edges.

## Limitations

- Edge weight scheme (1, 5, 10, 15) is heuristic and based on structural relationship type; interpretation requires domain knowledge of metabolomic ionization and adduction chemistry.
- Spring layout in pyvis is stochastic; repeated calls may produce visually different but topologically equivalent layouts; use fixed random seed for reproducibility.
- Correlation cluster assignment method (silhouette, other) affects node colors; choice of method and max_clusters parameter should be documented and justified separately.
- Cross-assay link detection relies on exact [M+H]+/[M-H]- neutral mass matching; features in assays with different mass calibration or retention time resolution may be missed.
- Large graphs (>5,000 nodes) become difficult to visualize interactively; consider filtering to a subgraph of interest or using alternative layout algorithms in Cytoscape.

## Evidence

- [other] Create NetworkX graph with features as nodes, assigning node attributes (assay, m/z, retention time, cluster membership, compound annotation) extracted from feature metadata.: "Create NetworkX graph with features as nodes, assigning node attributes (assay, m/z, retention time, cluster membership, compound annotation) extracted from feature metadata."
- [other] Add edges between nodes based on structural link type: assign weight 1 for isotopologue links, weight 5 for adduct links, weight 10 for cross-assay links, and weight 15 for correlation cluster co-membership.: "Add edges between nodes based on structural link type: assign weight 1 for isotopologue links, weight 5 for adduct links, weight 10 for cross-assay links, and weight 15 for correlation cluster"
- [other] Generate interactive pyvis.network visualization with spring layout, node coloring by correlation cluster membership, and edge thickness proportional to link weight; save as HTML artifact.: "Generate interactive pyvis.network visualization with spring layout, node coloring by correlation cluster membership, and edge thickness proportional to link weight; save as HTML artifact."
- [readme] You can also save the network as an NX object and review in Cytoscape to get better insight on what the structural relationships between individual features are: "You can also save the network as an NX object and review in Cytoscape to get better insight on what the structural relationships between individual features are"
- [methods] Overlapping adduct clusters and isotopologue clusters are then merged to form structural clusters. Further, we search cross-assay clusters using [M+H]+/[M-H]- as link references.: "Overlapping adduct clusters and isotopologue clusters are then merged to form structural clusters. Further, we search cross-assay clusters using [M+H]+/[M-H]- as link references."
