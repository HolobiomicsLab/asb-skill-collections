---
name: graph-visualization-interactive-rendering
description: Use when after constructing a NetworkX graph object from structural clusters
  (via MamsiStructSearch), when you need to interactively explore feature relationships
  or publish a static network diagram showing isotopologue links, adduct relationships,
  and cross-assay connections.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - networkx
  - pyvis
  - matplotlib
  - pandas
  - Python
  - MamsiStructSearch
  techniques:
  - mass-spectrometry
  license_tier: restricted
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

# graph-visualization-interactive-rendering

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Render a NetworkX graph object as an interactive force-directed network visualization using pyvis, or as a static matplotlib plot, optionally with node labels and HTML export. This skill is used to display structural relationships (isotopologue, adduct, and cross-assay links) between mass spectrometry features organized into clusters.

## When to use

After constructing a NetworkX graph object from structural clusters (via MamsiStructSearch), when you need to interactively explore feature relationships or publish a static network diagram showing isotopologue links, adduct relationships, and cross-assay connections. Triggered when return_nx_object=True or when the graph structure is ready for human interpretation.

## When NOT to use

- Graph structure is not yet constructed from structural clusters—use MamsiStructSearch first.
- You need to perform further graph analysis (centrality, clustering detection)—export the NetworkX object instead and use dedicated graph analysis libraries.
- Input is not a NetworkX graph object—validate the object type before rendering.

## Inputs

- NetworkX graph object with features as nodes
- Node attributes: assay, cluster membership, compound name (optional)
- Weighted edges: isotopologue (weight=1), adduct (weight=5), cross-assay (weight=10)

## Outputs

- Interactive HTML file with pyvis force-directed visualization
- Static matplotlib figure with optional node labels
- NetworkX graph object (if return_nx_object=True)

## How to apply

Pass the NetworkX graph object (with nodes representing features and edges representing structural relationships weighted by link type: isotopologue=1, adduct=5, cross-assay=10) to either the pyvis renderer (for interactive HTML output with force-directed layout) or the NetworkX/matplotlib combination (for static rendering). The pyvis output uses a physics-based layout to spatially separate clusters, improving readability. Set include_all=True to render all features or False to show only features with at least one structural link. Optionally enable node labels (labels=True) to display feature identifiers. Save the output as an HTML file for interactive exploration in a web browser, or display statically using matplotlib.

## Related tools

- **pyvis** (Interactive force-directed graph rendering and HTML export)
- **networkx** (Graph construction and manipulation; static rendering via matplotlib integration)
- **matplotlib** (Static 2D visualization of NetworkX graph with optional node labels)
- **pandas** (Loading structural cluster DataFrame with feature, cluster, and link attributes)
- **MamsiStructSearch** (Source tool that generates structural clusters and correlation clusters prior to graph construction) — https://github.com/kopeckylukas/py-mamsi

## Examples

```
network = struct.get_structural_network(include_all=True, interactive=True, labels=True, return_nx_object=True)
```

## Evaluation signals

- HTML file is generated and renders without errors in a web browser with interactive zoom, pan, and hover tooltips.
- Nodes are positioned spatially such that densely connected clusters (high edge weight) are grouped closer together.
- Node colors correspond to flattened hierarchical correlation clusters; edge types visually reflect link weight (isotopologue, adduct, cross-assay).
- All features specified by include_all parameter are present or only those with structural links are rendered, as configured.
- Node labels (if enabled) are readable and correspond to feature identifiers in the input DataFrame.
- Static matplotlib output can be saved as a publication-ready image with consistent layout across runs.

## Limitations

- Large graphs (>500 features) may be visually cluttered or slow to render interactively; consider filtering or subgraph extraction first.
- pyvis force-directed layout is non-deterministic; repeated renders may produce different spatial arrangements unless a random seed is set.
- Node label density can obscure edges and node positions in dense subgraphs; toggling labels or zooming is necessary.
- HTML output is browser-specific; rendering performance varies with browser capabilities and available system memory.
- The skill does not perform graph layout optimization beyond pyvis default physics parameters; custom layout algorithms require external networkx plugins.

## Evidence

- [methods] Construct a NetworkX graph with features as nodes, assigning node attributes (assay, cluster membership, compound name). Create edges between features based on structural relationships: isotopologue links (weight=1), adduct links (weight=5), and cross-assay links (weight=10).: "Construct a NetworkX graph with features as nodes, assigning node attributes (assay, cluster membership, compound name). 3. Create edges between features based on structural relationships:"
- [methods] Render the graph interactively using pyvis with force-directed layout and save as HTML output_file, or display statically using NetworkX and matplotlib with optional node labels.: "Render the graph interactively using pyvis with force-directed layout and save as HTML output_file, or display statically using NetworkX and matplotlib with optional node labels."
- [readme] the different node colours represent different flattened hierarchical correlation clusters, while the edges between nodes identify their structural links.: "the different node colours represent different flattened hierarchical correlation clusters, while the edges between nodes identify their structural links."
- [methods] Optionally include all features in the network or only those with structural links, controlled by the include_all parameter.: "Optionally include all features in the network or only those with structural links, controlled by the include_all parameter."
- [methods] If return_nx_object=True, return the NetworkX graph object for downstream curation.: "If return_nx_object=True, return the NetworkX graph object for downstream curation."
