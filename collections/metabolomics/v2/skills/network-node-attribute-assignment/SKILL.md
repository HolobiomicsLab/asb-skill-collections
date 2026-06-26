---
name: network-node-attribute-assignment
description: Use when you have constructed a NetworkX graph with LC-MS features as
  nodes and need to annotate each node with metadata derived from the MamsiStructSearch
  output (assay source, isotopologue group, adduct group, structural cluster ID, correlation
  cluster ID, and optional compound annotation).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3359
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - networkx
  - pyvis
  - matplotlib
  - pandas
  - Python
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
- 'Dependencies: networkx'
- 'Dependencies: pyvis'
- 'Dependencies: matplotlib'
- import pandas as pd
- MAMSI is a Python framework designed for the integration of multi-assay mass spectrometry
  datasets.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mamsi_cq
    doi: 10.1021/acs.analchem.5c01327
    title: mamsi
  dedup_kept_from: coll_mamsi_cq
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

# network-node-attribute-assignment

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Assign node attributes (assay membership, structural cluster identity, correlation cluster membership, and compound name) to feature nodes in a NetworkX graph constructed from multi-assay LC-MS data. This enrichment enables downstream filtering, visualization, and structural interpretation of feature relationships.

## When to use

You have constructed a NetworkX graph with LC-MS features as nodes and need to annotate each node with metadata derived from the MamsiStructSearch output (assay source, isotopologue group, adduct group, structural cluster ID, correlation cluster ID, and optional compound annotation). This is required before rendering the network or filtering nodes by cluster membership.

## When NOT to use

- The NetworkX graph has not yet been constructed from features—use graph construction first.
- MamsiStructSearch has not been run or its output DataFrame is incomplete or missing cluster columns.
- Features in the graph do not correspond to rows in the MamsiStructSearch DataFrame (feature name mismatch).

## Inputs

- NetworkX graph object with features as nodes
- pandas DataFrame from MamsiStructSearch output (columns: Feature, Assay, Isotopologue group, Isotopologue pattern, Adduct group, Adduct, Structural cluster, Correlation cluster, Cross-assay link, optional cpdName)

## Outputs

- NetworkX graph object with enriched node attributes (assay, isotopologue_group, isotopologue_pattern, adduct_group, adduct, structural_cluster, correlation_cluster, cross_assay_link, compound_name)
- Attribute-annotated feature nodes suitable for visualization and filtering

## How to apply

Load the DataFrame output from MamsiStructSearch, which contains columns Feature, Assay, Isotopologue group, Isotopologue pattern, Adduct group, Adduct, Structural cluster, Correlation cluster, Cross-assay link, and optional cpdName. For each feature node in the NetworkX graph, retrieve the corresponding row and assign its metadata values as node attributes using NetworkX's node attribute dictionary (e.g., `G.nodes[feature_id]['assay'] = row['Assay']`, `G.nodes[feature_id]['struct_cluster'] = row['Structural cluster']`). Ensure all features present in the graph have complete attribute assignment. This enables node colorization by cluster in pyvis visualization and supports downstream node filtering or curation based on structural properties.

## Related tools

- **networkx** (Graph construction and node attribute assignment via dict-like interface) — https://github.com/networkx/networkx
- **pandas** (Read and iterate over MamsiStructSearch output DataFrame to extract node metadata) — https://github.com/pandas-dev/pandas
- **pyvis** (Render the attribute-enriched graph with node coloring by cluster membership) — https://github.com/WestHealth/pyvis
- **MamsiStructSearch** (Generate the structural cluster, correlation cluster, and feature metadata DataFrame) — https://github.com/kopeckylukas/py-mamsi

## Examples

```
struct = MamsiStructSearch(rt_win=5, ppm=10)
struct.load_lcms(selected)
struct.get_structural_clusters(annotate=True)
df_clusters = struct.get_struct_cluster_df()
for feature, row in df_clusters.iterrows():
    G.nodes[feature]['assay'] = row['Assay']
    G.nodes[feature]['structural_cluster'] = row['Structural cluster']
    G.nodes[feature]['correlation_cluster'] = row['Correlation cluster']
```

## Evaluation signals

- Every feature node in the graph has non-null values for 'assay', 'structural_cluster', and 'correlation_cluster' attributes.
- Node attribute keys match the MamsiStructSearch column names (Assay, Isotopologue group, Adduct group, Structural cluster, Correlation cluster, cpdName).
- When iterating over `G.nodes(data=True)`, each node dict contains ≥ 7 keys (feature identifier + 6 metadata attributes).
- Pyvis interactive visualization renders nodes with distinct colors for each unique structural_cluster value (if `include_all=True`) without missing or NaN-colored nodes.
- Filtering operations (e.g., `[node for node, attr in G.nodes(data=True) if attr['assay'] == 'HPOS']`) return the expected subset of features.

## Limitations

- Feature names in the NetworkX graph must exactly match feature identifiers in the MamsiStructSearch DataFrame; case-sensitive mismatches will result in missing attribute assignments.
- If MamsiStructSearch is run with `annotate=True` but the assay is not supported by the National Phenome Centre ROI database, the cpdName attribute will be None/NaN for those features.
- Large networks (>5000 features) may experience slow rendering in pyvis due to force-directed layout computation; consider filtering to structural clusters of interest before visualization.
- Cross-assay link metadata is only populated when features from different assays (e.g., positive and negative ion modes) share a hypothetical neutral mass within the specified ppm tolerance.

## Evidence

- [methods] 1. Load structural clusters and correlation clusters from MamsiStructSearch output (DataFrame with Feature, Assay, Isotopologue group, Isotopologue pattern, Adduct group, Adduct, Structural cluster, Correlation cluster, Cross-assay link, and optional cpdName columns). 2. Construct a NetworkX graph with features as nodes, assigning node attributes (assay, cluster membership, compound name).: "Load structural clusters and correlation clusters from MamsiStructSearch output (DataFrame with Feature, Assay, Isotopologue group, Isotopologue pattern, Adduct group, Adduct, Structural cluster,"
- [methods] Overlapping adduct clusters and isotopologue clusters are then merged to form structural clusters. Further, we search cross-assay clusters using [M+H]+/[M-H]- as link references.: "Overlapping adduct clusters and isotopologue clusters are then merged to form structural clusters. Further, we search cross-assay clusters using [M+H]+/[M-H]- as link references"
- [readme] The different node colours represent different flattened hierarchical correlation clusters, while the edges between nodes identify their structural links.: "The different node colours represent different flattened hierarchical correlation clusters, while the edges between nodes identify their structural links"
