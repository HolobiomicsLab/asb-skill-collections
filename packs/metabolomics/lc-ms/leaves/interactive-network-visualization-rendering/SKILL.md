---
name: interactive-network-visualization-rendering
description: Use when after structural clustering (isotopologue grouping, adduct detection, cross-assay linking) and correlation clustering of LC-MS features, when you need to inspect and communicate the topology of structural relationships—particularly when the number of features or link types is too dense for.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3083
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - pyvis
  - pandas
  - Cytoscape
  - networkx
  - MamsiStructSearch
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# interactive-network-visualization-rendering

## Summary

Convert structural cluster assignments (isotopologue, adduct, and cross-assay links) into an interactive network graph suitable for dynamic exploration and annotation in web-based or desktop environments. This skill bridges programmatic network construction with human-centered curation by rendering NetworkX objects as interactive HTML visualizations or exporting to specialized tools like Cytoscape.

## When to use

After structural clustering (isotopologue grouping, adduct detection, cross-assay linking) and correlation clustering of LC-MS features, when you need to inspect and communicate the topology of structural relationships—particularly when the number of features or link types is too dense for static plots, or when domain experts need to interactively filter, drag, and annotate nodes to validate or refine cluster membership.

## When NOT to use

- Input contains <50 features or <100 edges — static plots (matplotlib/seaborn) are more efficient and publication-ready.
- Network is fully disconnected or consists only of isolated nodes — interactive rendering adds no interpretive value.
- Goal is statistical summary only (e.g., degree distribution, centrality metrics) rather than visual exploration — compute graph statistics directly without rendering.

## Inputs

- pandas DataFrame with feature metadata (m/z, retention time, assay, cluster membership, annotations)
- Isotopologue cluster assignments (feature pairs linked by 1.00335 Da mass differences)
- Adduct cluster assignments (feature groups with matching hypothetical neutral masses within 15 ppm)
- Cross-assay link references ([M+H]+/[M-H]- feature pairs across assays)
- Correlation cluster assignments from hierarchical flattening
- MamsiStructSearch object containing all structural and correlation cluster data

## Outputs

- NetworkX graph object with features as nodes and weighted edges representing structural links
- Interactive HTML visualization (pyvis.network) with spring layout, node colors by cluster, edge weights
- Network artifact suitable for import into Cytoscape for further interactive curation

## How to apply

Load structural cluster data (isotopologue groups, adduct groups, cross-assay links, and correlation cluster assignments) as a pandas DataFrame or MamsiStructSearch object. Instantiate a NetworkX graph with features as nodes and assign node attributes (assay, m/z, retention time, cluster membership, compound annotation) from feature metadata. Create directed edges weighted by structural link type: weight 1 for isotopologue links, weight 5 for adduct links, weight 10 for cross-assay links, and weight 15 for correlation cluster co-membership. Optionally filter to structurally linked features only via the `include_all` parameter to reduce visual clutter. Generate a pyvis.network visualization using spring layout with node coloring by correlation cluster and edge thickness proportional to link weight. Save the rendered HTML artifact for web-based exploration and return the NetworkX object for downstream curation in Cytoscape or programmatic analysis.

## Related tools

- **networkx** (Construct and represent structural networks as graphs; manage node/edge attributes and weights)
- **pyvis** (Render NetworkX graphs as interactive HTML visualizations with spring layout physics and user interaction (drag, zoom, filter))
- **Cytoscape** (Import and curate NetworkX objects for advanced interactive network analysis, annotation, and publication-quality visualization) — https://cytoscape.org
- **pandas** (Load, merge, and structure feature metadata and cluster assignments for node attribute assignment)
- **MamsiStructSearch** (Container for structural cluster, cross-assay link, and correlation cluster data; provides get_structural_network() method) — https://github.com/kopeckylukas/py-mamsi

## Examples

```
struct = MamsiStructSearch(rt_win=5, ppm=10); struct.load_lcms(selected); struct.get_structural_clusters(); struct.get_correlation_clusters(flat_method='silhouette', max_clusters=11); network = struct.get_structural_network(include_all=True, interactive=False, labels=True, return_nx_object=True)
```

## Evaluation signals

- NetworkX object contains correct node count equal to number of input features and edge count equal to total structural + correlation links.
- Node attributes (assay, m/z, retention time, cluster membership) match input metadata without loss or mismatch.
- Edge weights follow specification: isotopologue=1, adduct=5, cross-assay=10, correlation co-membership=15.
- Interactive HTML renders without JavaScript errors; nodes are draggable and edges respond to hover with weight/type information.
- Visual inspection: nodes cluster spatially by color (correlation cluster membership); edge thickness correlates visually with link strength.
- When imported into Cytoscape, network topology is preserved and cluster annotations are readable in node labels.

## Limitations

- pyvis spring layout is computationally expensive for >1000 nodes; performance degrades and layout becomes difficult to interpret visually.
- Edge weight encoding (visual thickness) can become ambiguous if many link types have similar weights; domain-driven weight tuning may be needed.
- Interactive rendering in pyvis does not natively support statistical network analysis (centrality, community detection, motif discovery)—those require separate computation.
- HTML output is browser-specific; some versions may not render advanced CSS or have performance issues on large networks.
- Correlation cluster co-membership links (weight 15) can dominate visual layout if correlation clusters are large; filter via `include_all=False` to show only structural links.
- Node labels can overlap on small screens or densely packed regions; Cytoscape provides better label management and layout options for curation.

## Evidence

- [other] structural cluster assignments into an interactive network graph representation: "Reconstruct the structural network graph generation from significant features: How does MAMSI convert structural cluster assignments into an interactive network graph representation suitable for"
- [methods] Create NetworkX graph with node attributes and edges weighted by structural link type: "Create NetworkX graph with features as nodes, assigning node attributes (assay, m/z, retention time, cluster membership, compound annotation) extracted from feature metadata. 3. Add edges between"
- [methods] Generate pyvis visualization with spring layout and save as HTML: "Generate interactive pyvis.network visualization with spring layout, node coloring by correlation cluster membership, and edge thickness proportional to link weight; save as HTML artifact."
- [methods] Return NetworkX object for downstream curation in Cytoscape: "Return NetworkX object for downstream curation in Cytoscape or additional programmatic analysis."
- [readme] Save network as NX object and review in Cytoscape: "You can also save the network as an NX object and review in Cytoscape to get better insight on what the structural relationships between individual features are (e.g. adduct links, isotopologues,"
- [methods] Optionally include or filter features via include_all parameter: "Optionally include all features or filter to structurally linked features only via include_all parameter."
