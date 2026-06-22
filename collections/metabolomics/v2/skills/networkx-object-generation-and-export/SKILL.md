---
name: networkx-object-generation-and-export
description: Use when after identifying statistically significant features and assigning them to structural clusters (isotopologue groups, adduct groups, cross-assay links) and correlation clusters via MamsiStructSearch.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3359
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - networkx
  - pyvis
  - pandas
  - Cytoscape
  - MamsiStructSearch
derived_from:
- doi: 10.1021/acs.analchem.5c01327
  title: mamsi
- doi: 10.1371/journal.pcbi.1011814
  title: ''
evidence_spans:
- MAMSI is a Python framework
- networkx
- import ... networkx
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

# NetworkX object generation and export

## Summary

Convert structural cluster assignments and feature metadata into a NetworkX graph object, optionally visualizing it with pyvis and exporting for interactive analysis in Cytoscape. This skill enables programmatic construction of metabolite feature networks where nodes represent features and edges encode structural relationships (isotopologues, adducts, cross-assay links, correlation clusters).

## When to use

After identifying statistically significant features and assigning them to structural clusters (isotopologue groups, adduct groups, cross-assay links) and correlation clusters via MamsiStructSearch. Use this skill when you need to represent pairwise structural relationships between features as a graph for visualization, curation, or downstream analysis in network tools.

## When NOT to use

- Features have not yet been assigned to structural clusters or correlation clusters; run MamsiStructSearch.get_structural_clusters() and get_correlation_clusters() first.
- Input is already a NetworkX object or graph file format; use import/load functions instead.
- Goal is to identify structural relationships de novo; this skill assumes upstream structural search has already been completed.

## Inputs

- Feature metadata table (assay, m/z, retention time, cluster membership, compound annotation)
- Structural cluster assignments (isotopologue groups, adduct groups, cross-assay links)
- Correlation cluster assignments from hierarchical clustering
- Boolean parameter: include_all (True to include all features, False to filter to structurally linked features only)

## Outputs

- NetworkX graph object (nodes=features, edges=structural links with weights)
- Interactive HTML visualization (pyvis network graph with spring layout)
- Node attributes (assay, m/z, retention time, cluster membership, annotation)
- Edge attributes (weight, link_type)

## How to apply

Load feature metadata (m/z, retention time, assay identifier, cluster membership, compound annotation) and structural link assignments from MamsiStructSearch outputs. Create a NetworkX DiGraph or Graph with features as nodes, assigning node attributes from the metadata. Add weighted edges between nodes based on structural link type: weight 1 for isotopologue links (mass difference 1.00335 Da), weight 5 for adduct links (matching neutral masses within 15 ppm tolerance), weight 10 for cross-assay links ([M+H]+/[M-H]− references), and weight 15 for correlation cluster co-membership. Optionally filter to include only structurally linked features or include all features. Generate an interactive pyvis visualization with spring layout and node colors by correlation cluster; save as HTML. Return the NetworkX object for programmatic analysis or import into Cytoscape for manual curation and inspection of edge types.

## Related tools

- **networkx** (Core library for graph construction, node/edge attribute assignment, and programmatic analysis) — https://networkx.org
- **pyvis** (Interactive HTML visualization of NetworkX graph with spring layout, node coloring, and edge thickness scaling) — https://pyvis.readthedocs.io
- **Cytoscape** (Desktop application for manual curation, filtering, and exploratory analysis of exported NetworkX objects) — https://cytoscape.org
- **pandas** (Load and manipulate feature metadata tables before graph construction) — https://pandas.pydata.org
- **MamsiStructSearch** (Upstream tool that generates structural and correlation cluster assignments consumed by this skill) — https://github.com/kopeckylukas/py-mamsi

## Examples

```
network = struct.get_structural_network(include_all=True, interactive=False, labels=True, return_nx_object=True)
```

## Evaluation signals

- NetworkX object has non-zero number of nodes equal to the number of features and edges equal to the number of identified structural relationships.
- All nodes have assigned attributes (assay, m/z, retention time, cluster membership, annotation) with no missing values for required fields.
- All edges have assigned weights matching the expected link types (isotopologue=1, adduct=5, cross-assay=10, correlation=15); sum of edge weights correlates with number of each link type.
- Interactive HTML visualization renders without errors, node colors correspond to correlation cluster membership, and edge thickness is proportional to weight.
- NetworkX object can be serialized and imported into Cytoscape without data loss or corruption; manual inspection confirms edge types match upstream structural search output.

## Limitations

- Visualization with pyvis can become cluttered and difficult to interpret with >500 nodes; filtering to structurally linked features only (include_all=False) is recommended for large datasets.
- Edge weight scheme is fixed; custom link type definitions or weights require modification to the underlying MamsiStructSearch code.
- Cytoscape import requires manual steps for interactive exploration; no automated curation or filtering is performed by this skill.
- Correlation cluster assignment depends on hierarchical clustering parameters (flat_method, max_clusters); different choices produce different network topologies.
- Cross-assay links use [M+H]+/[M-H]− as references only; other adduct pairs or ionization modes are not supported in the current implementation.

## Evidence

- [other] Create NetworkX graph with features as nodes, assigning node attributes (assay, m/z, retention time, cluster membership, compound annotation) extracted from feature metadata.: "Create NetworkX graph with features as nodes, assigning node attributes (assay, m/z, retention time, cluster membership, compound annotation) extracted from feature metadata."
- [other] Add edges between nodes based on structural link type: assign weight 1 for isotopologue links, weight 5 for adduct links, weight 10 for cross-assay links, and weight 15 for correlation cluster co-membership.: "Add edges between nodes based on structural link type: assign weight 1 for isotopologue links, weight 5 for adduct links, weight 10 for cross-assay links, and weight 15 for correlation cluster"
- [other] Generate interactive pyvis.network visualization with spring layout, node coloring by correlation cluster membership, and edge thickness proportional to link weight; save as HTML artifact.: "Generate interactive pyvis.network visualization with spring layout, node coloring by correlation cluster membership, and edge thickness proportional to link weight; save as HTML artifact."
- [readme] You can also save the network as an NX object and review in Cytoscape to get better insight on what the structural relationships between individual features are: "You can also save the network as an NX object and review in Cytoscape to get better insight on what the structural relationships between individual features are"
- [readme] The different node colours represent different flattened hierarchical correlation clusters, while the edges between nodes identify their structural links.: "The different node colours represent different flattened hierarchical correlation clusters, while the edges between nodes identify their structural links."
