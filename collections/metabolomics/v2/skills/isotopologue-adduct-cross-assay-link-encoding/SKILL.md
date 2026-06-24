---
name: isotopologue-adduct-cross-assay-link-encoding
description: Use when after structural cluster assignment and correlation clustering
  are complete, and you need to represent the full set of structural relationships
  (isotopologues, adducts, cross-assay links, and correlation co-membership) in a
  single unified graph for interactive visualization, network.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0360
  edam_topics:
  - http://edamontology.org/topic_3375
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
  license_tier: restricted
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

# Isotopologue, Adduct, and Cross-Assay Link Encoding

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

This skill encodes structural relationships between LC-MS features as weighted edges in a NetworkX graph, where edge weights (1–15) represent the type and specificity of structural link: isotopologue (weight 1), adduct (weight 5), cross-assay (weight 10), and correlation cluster co-membership (weight 15). It converts raw structural cluster assignments into a machine-readable and visualizable network representation suitable for downstream curation and analysis.

## When to use

After structural cluster assignment and correlation clustering are complete, and you need to represent the full set of structural relationships (isotopologues, adducts, cross-assay links, and correlation co-membership) in a single unified graph for interactive visualization, network analysis, or export to specialized tools like Cytoscape. Specifically when you have NetworkX-compatible feature metadata (assay, m/z, retention time, cluster membership, annotation) and want to encode link heterogeneity explicitly through edge weights.

## When NOT to use

- Structural clusters and correlation clusters have not yet been computed; this skill requires complete upstream MamsiStructSearch and clustering outputs as inputs.
- You only need unweighted or untyped edges; the explicit encoding of link heterogeneity via weights 1–15 is unnecessary for your analysis.
- Your features lack adequate metadata (assay, m/z, retention time, cluster membership); the skill depends on rich node attributes for meaningful visualization and curation.

## Inputs

- Structural cluster assignments (isotopologue groups, adduct groups, structural clusters) from MamsiStructSearch
- Correlation cluster assignments (flat hierarchical clustering output)
- Feature metadata table with columns: assay, m/z, retention time, structural cluster membership, correlation cluster membership, compound annotation
- Selected or filtered LC-MS feature matrix

## Outputs

- NetworkX graph object with features as nodes and weighted edges encoding structural link types
- Interactive pyvis HTML visualization artifact (spring layout, node colors by correlation cluster, edge thickness by weight)
- Optional: exported network in formats compatible with Cytoscape (e.g., GraphML, GML)

## How to apply

Instantiate a NetworkX graph with features as nodes, extracting node attributes (assay, m/z, retention time, cluster membership, compound annotation) from feature metadata. For each structural relationship identified by upstream MamsiStructSearch, add an edge between the corresponding nodes and assign a weight based on link type: weight 1 for isotopologue links (mass difference ~1.00335 Da within a 5 s retention time window), weight 5 for adduct links (hypothetical neutral masses matching within 15 ppm tolerance in electrospray ionisation), weight 10 for cross-assay links using [M+H]+/[M-H]− as references, and weight 15 for correlation cluster co-membership. Optionally filter to structurally linked features only via the include_all parameter (default: include all features to preserve context). Then generate an interactive pyvis.network visualization with spring layout, node coloring by correlation cluster membership, and edge thickness proportional to link weight for human review; save the HTML artifact and return the NetworkX object for programmatic analysis or curation in Cytoscape.

## Related tools

- **networkx** (Create and manipulate the structural relationship graph; add nodes (features) with attributes and edges with weights)
- **pyvis** (Generate interactive spring-layout visualization of the NetworkX graph with node coloring by cluster and edge thickness by weight)
- **pandas** (Load and manipulate feature metadata and structural/correlation cluster assignments)
- **Cytoscape** (Import NetworkX object for interactive network visualization, exploration, and manual curation of structural relationships) — https://cytoscape.org
- **MamsiStructSearch** (Upstream tool that identifies isotopologue, adduct, and cross-assay links; produces the cluster assignments and metadata consumed by this skill) — https://github.com/kopeckylukas/py-mamsi

## Examples

```
network = struct.get_structural_network(include_all=True, interactive=False, labels=True, return_nx_object=True)
```

## Evaluation signals

- NetworkX graph contains exactly one node per input feature with all expected attributes (assay, m/z, retention time, cluster membership, annotation) present and non-null where applicable.
- Edge count and weight distribution match the input structural link counts: isotopologue edges have weight 1, adduct edges weight 5, cross-assay edges weight 10, correlation co-membership edges weight 15.
- Interactive pyvis HTML renders without errors; nodes are colored distinctly by correlation cluster membership and edge thickness scales visibly with weight.
- Graph density and clustering coefficient are consistent with the biochemical expectation that related features (isotopologues, adducts) form dense subgraphs.
- Cytoscape import preserves all node attributes and edge weights; manual inspection of a sample subgraph confirms correct link type encoding (e.g., all edges within a subgraph linking isotopologue features have weight 1).

## Limitations

- Edge weight assignment is fixed and discrete (1, 5, 10, 15); no probabilistic or confidence-weighted variant is offered, so links of equal type receive identical weight regardless of match quality (e.g., adduct match at 14.9 ppm vs. 10 ppm both get weight 5).
- The skill does not perform de novo link discovery; it encodes only relationships already identified by upstream MamsiStructSearch, so spurious or missed links in the input propagate directly to the graph.
- Performance may degrade on very large feature sets (>10,000 features) due to quadratic edge enumeration in the correlation cluster co-membership step; no built-in sampling or thinning is provided.
- Interactive visualization quality depends heavily on NetworkX spring layout convergence and pyvis rendering; highly dense or clique-like subgraphs may be difficult to navigate interactively without post-hoc layout optimization in Cytoscape.

## Evidence

- [other] Create NetworkX graph with features as nodes, assigning node attributes (assay, m/z, retention time, cluster membership, compound annotation) extracted from feature metadata.: "Create NetworkX graph with features as nodes, assigning node attributes (assay, m/z, retention time, cluster membership, compound annotation) extracted from feature metadata."
- [other] Add edges between nodes based on structural link type: assign weight 1 for isotopologue links, weight 5 for adduct links, weight 10 for cross-assay links, and weight 15 for correlation cluster co-membership.: "Add edges between nodes based on structural link type: assign weight 1 for isotopologue links, weight 5 for adduct links, weight 10 for cross-assay links, and weight 15 for correlation cluster"
- [methods] each RT window is searched for isotopologue signatures by searching mass differences of 1.00335 Da between mass-to-charge ratios (m/z) of the features: "each RT window is searched for isotopologue signatures by searching mass differences of 1.00335 Da between mass-to-charge ratios (m/z) of the features"
- [methods] calculating hypothetical neutral masses based on common adducts in electrospray ionisation. If hypothetical neutral masses match for two or more features within a pre-defined tolerance (15 ppm): "calculating hypothetical neutral masses based on common adducts in electrospray ionisation. If hypothetical neutral masses match for two or more features within a pre-defined tolerance (15 ppm)"
- [other] Generate interactive pyvis.network visualization with spring layout, node coloring by correlation cluster membership, and edge thickness proportional to link weight; save as HTML artifact.: "Generate interactive pyvis.network visualization with spring layout, node coloring by correlation cluster membership, and edge thickness proportional to link weight; save as HTML artifact."
- [readme] You can also save the network as an NX object and review in Cytoscape to get better insight on what the structural relationships between individual features are (e.g. adduct links, isotopologues, cross-assay links).: "You can also save the network as an NX object and review in Cytoscape to get better insight on what the structural relationships between individual features are"
