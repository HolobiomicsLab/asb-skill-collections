---
name: correlation-cluster-network-integration
description: Use when after identifying structural clusters (isotopologue groups,
  adduct groups, and cross-assay links) and assigning features to correlation clusters
  via hierarchical clustering.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3083
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - pyvis
  - pandas
  - Cytoscape
  - networkx
  - MamsiStructSearch
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Reconstruct the structural network graph generation from significant features

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Integrate structural cluster assignments and correlation cluster memberships into an interactive NetworkX graph representation suitable for visualization and analysis in Cytoscape. This skill converts feature relationships (isotopologues, adducts, cross-assay links, and correlation co-membership) into a weighted network where node attributes and edge weights encode structural and statistical relationships.

## When to use

Apply this skill after identifying structural clusters (isotopologue groups, adduct groups, and cross-assay links) and assigning features to correlation clusters via hierarchical clustering. Use it when you need to visualize and curate the relationships between statistically significant LC-MS features to understand compound structure, annotation ambiguity, and multi-assay coherence.

## When NOT to use

- Structural clusters have not yet been computed or validated (run MamsiStructSearch.get_structural_clusters() first).
- Correlation clusters have not been assigned (run get_correlation_clusters() with a chosen flattening method first).
- Input features lack complete metadata (m/z, retention time, or assay prefix) required for node attributes.

## Inputs

- Structural cluster assignments (isotopologue groups, adduct groups, cross-assay links) from MamsiStructSearch
- Correlation cluster membership vector from hierarchical clustering (flattened via silhouette or elbow method)
- LC-MS feature metadata (m/z, retention time, assay, compound annotation)
- Feature intensity or abundance matrix

## Outputs

- NetworkX graph object (NX) with nodes as features and weighted edges as structural relationships
- Interactive HTML network visualization (pyvis format) with spring layout and colored nodes
- Node attribute table (assay, m/z, retention time, cluster membership, annotation)
- Edge list with link type and weight

## How to apply

Load structural cluster data (isotopologue groups, adduct groups, and cross-assay links) along with correlation cluster assignments from upstream MamsiStructSearch outputs. Create a NetworkX graph object with LC-MS features as nodes, assigning node attributes (assay prefix, m/z, retention time, correlation cluster membership, compound annotation) extracted from feature metadata. Add edges between nodes based on structural link type: assign weight 1 for isotopologue links, weight 5 for adduct links, weight 10 for cross-assay links, and weight 15 for correlation cluster co-membership. Optionally filter to structurally linked features only or include all features via an include_all parameter. Generate an interactive pyvis.network visualization with spring layout, color nodes by correlation cluster membership, and scale edge thickness proportional to link weight. Save the HTML artifact and return the NetworkX object for downstream curation in Cytoscape or additional programmatic analysis.

## Related tools

- **networkx** (Create and manipulate the graph structure with nodes and weighted edges representing feature relationships) — https://networkx.org
- **pyvis** (Generate interactive network visualization with spring layout, node coloring by cluster, and edge thickness by weight)
- **pandas** (Manage feature metadata tables and correlation cluster membership assignments)
- **Cytoscape** (Interactive curation and exploration of the saved NetworkX object for detailed structural relationship analysis) — https://cytoscape.org
- **MamsiStructSearch** (Upstream component that computes structural clusters and provides link annotations) — https://github.com/kopeckylukas/py-mamsi

## Examples

```
network = struct.get_structural_network(include_all=True, interactive=False, labels=True, return_nx_object=True)
```

## Evaluation signals

- NetworkX graph contains all LC-MS features as nodes with complete metadata (m/z, RT, assay, cluster ID, annotation).
- Edge weights follow the prescribed schema: isotopologue = 1, adduct = 5, cross-assay = 10, correlation co-membership = 15.
- Interactive HTML visualization renders without errors, with nodes colored distinctly by correlation cluster and edge opacity/thickness proportional to weight.
- Cytoscape import succeeds and displays the same topological structure as the pyvis output.
- Node counts in the NetworkX object match the input feature count (or match the structurally linked subset if include_all=False).

## Limitations

- Network visualization quality degrades when >1000 features are included; filtering to structurally linked features or subnetworks is recommended.
- Edge weight scheme is empirically chosen; relative magnitude (1, 5, 10, 15) may need tuning for specific data domains or correlation thresholds.
- Interactive HTML rendering in pyvis is browser-dependent and may be slow for very dense networks (many edges); static matplotlib rendering is an alternative.
- Cytoscape integration requires manual export/import; no direct programmatic bridge is provided in the MAMSI code.
- Correlation cluster assignment method (silhouette, elbow, max distance) affects the visual separation of nodes; results should be validated against dendrograms or silhouette plots.

## Evidence

- [methods] Create NetworkX graph with features as nodes, assigning node attributes (assay, m/z, retention time, cluster membership, compound annotation) extracted from feature metadata.: "Create NetworkX graph with features as nodes, assigning node attributes (assay, m/z, retention time, cluster membership, compound annotation) extracted from feature metadata."
- [methods] Add edges between nodes based on structural link type: assign weight 1 for isotopologue links, weight 5 for adduct links, weight 10 for cross-assay links, and weight 15 for correlation cluster co-membership.: "assign weight 1 for isotopologue links, weight 5 for adduct links, weight 10 for cross-assay links, and weight 15 for correlation cluster co-membership."
- [methods] Generate interactive pyvis.network visualization with spring layout, node coloring by correlation cluster membership, and edge thickness proportional to link weight; save as HTML artifact.: "Generate interactive pyvis.network visualization with spring layout, node coloring by correlation cluster membership, and edge thickness proportional to link weight; save as HTML artifact."
- [readme] You can also save the network as an NX object and review in Cytoscape to get better insight on what the structural relationships between individual features are (e.g. adduct links, isotopologues, cross-assay links).: "You can also save the network as an NX object and review in Cytoscape to get better insight on what the structural relationships between individual features are"
- [methods] Load structural cluster data (isotopologue groups, adduct groups, and cross-assay links) along with correlation cluster assignments from upstream MamsiStructSearch outputs.: "Load structural cluster data (isotopologue groups, adduct groups, and cross-assay links) along with correlation cluster assignments from upstream MamsiStructSearch outputs."
- [methods] Optionally include all features or filter to structurally linked features only via include_all parameter.: "Optionally include all features or filter to structurally linked features only via include_all parameter."
