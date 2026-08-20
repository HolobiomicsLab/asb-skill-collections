---
name: feature-relationship-edge-weighting
description: Use when after structural clusters have been identified by MamsiStructSearch
  (via isotopologue, adduct, and cross-assay link detection), and you need to construct
  a NetworkX graph where edges encode the biochemical relationship type and strength
  between features for downstream curation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3562
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - networkx
  - pyvis
  - matplotlib
  - pandas
  - Python
  - NetworkX
  - MamsiStructSearch
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

# feature-relationship-edge-weighting

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Assign weighted edges in a metabolomics feature network graph based on structural relationship types (isotopologue, adduct, cross-assay) detected from mass-to-charge ratio and retention time patterns. This differentiates the strength and type of biochemical linkage between features during network visualization and interpretation.

## When to use

After structural clusters have been identified by MamsiStructSearch (via isotopologue, adduct, and cross-assay link detection), and you need to construct a NetworkX graph where edges encode the biochemical relationship type and strength between features for downstream curation, visualization, or network analysis.

## When NOT to use

- Input features have not yet been clustered by MamsiStructSearch (no isotopologue, adduct, or cross-assay relationships detected)—edge weighting requires pre-computed structural relationships.
- Goal is exploratory visualization of raw feature correlations rather than biochemical relationship networks—consider correlation-based edge weighting (e.g., Pearson r) instead.
- Feature set is dominated by a single ionization mode without cross-assay data—cross-assay weight=10 will not contribute, reducing the benefit of differentiated edge weights.

## Inputs

- MamsiStructSearch output DataFrame (columns: Feature, Assay, Isotopologue group, Isotopologue pattern, Adduct group, Adduct, Structural cluster, Correlation cluster, Cross-assay link, optional cpdName)
- Feature metadata (mass-to-charge ratio, retention time, assay identifier per feature)

## Outputs

- NetworkX graph object with weighted edges (networkx.Graph or networkx.DiGraph)
- Interactive HTML network visualization (pyvis force-directed layout) or static matplotlib figure with edge weights visible
- Edge table/adjacency matrix with columns: source_feature, target_feature, relationship_type, weight

## How to apply

Within the NetworkX graph construction workflow, iterate over identified structural relationships and assign edge weights according to the relationship category: isotopologue links receive weight=1 (lightest), adduct links receive weight=5 (moderate), and cross-assay links receive weight=10 (heaviest). These weight assignments reflect the biochemical significance and rarity of each relationship type—isotopologues are common natural variation, adducts represent different ionization forms of the same neutral mass, and cross-assay links (using [M+H]⁺/[M-H]⁻ reference masses) are the most informative for compound identity confirmation across ionization modes. The weights serve dual purposes: they visually encode relationship strength in force-directed layouts (where heavier edges pull nodes closer) and enable quantitative prioritization when mining the graph for high-confidence feature clusters.

## Related tools

- **NetworkX** (Core graph construction and edge weight assignment; stores nodes (features) and weighted edges (structural relationships) with attributes) — https://networkx.org
- **pyvis** (Interactive HTML visualization of weighted network with force-directed layout; edge weights influence node repulsion/attraction) — https://pyvis.readthedocs.io
- **matplotlib** (Static network rendering option; plots edges with line widths or colors scaled to weights) — https://matplotlib.org
- **MamsiStructSearch** (Predecessor tool that identifies isotopologue, adduct, and cross-assay relationships; outputs clustering assignments needed to derive edge types) — https://github.com/kopeckylukas/py-mamsi
- **pandas** (Loads and processes MamsiStructSearch output DataFrame; filters features and relationships before graph construction) — https://pandas.pydata.org

## Examples

```
network = struct.get_structural_network(include_all=True, interactive=False, labels=True, return_nx_object=True); edges = [(u, v, data['weight']) for u, v, data in network.edges(data=True)]; import pandas as pd; pd.DataFrame(edges, columns=['source', 'target', 'weight']).to_csv('network_edges.csv')
```

## Evaluation signals

- Edge weight distribution is non-uniform and reflects the three relationship types (weight 1, 5, 10) with no edges outside these values—verify via edge_data['weight'] histogram or summary statistics.
- Force-directed layout visually clusters heavily weighted (cross-assay, weight=10) edges into tight knots, while loosely weighted (isotopologue, weight=1) edges allow nodes to spread—confirm with pyvis interactive inspection or matplotlib edge-width scaling.
- Edges are correctly attributed: all isotopologue relationship edges have weight=1, all adduct relationship edges have weight=5, all cross-assay relationship edges have weight=10; verify by querying graph edges with relationship type filters.
- NetworkX graph object has no isolated nodes unless include_all=True and those nodes genuinely have no structural links—confirm node count matches expected feature count and check node degree distribution.
- Exported HTML visualization renders without errors and edge transparency/thickness reflects weight ordering (heavier edges darker/thicker than light edges)—manual inspection of output HTML file.

## Limitations

- Edge weights are fixed heuristics (1, 5, 10) and not learned from data; the relative magnitude may not reflect true biochemical confidence in all cohorts or instrument configurations.
- Cross-assay links rely on [M+H]⁺/[M-H]⁻ reference masses only; other ionization modes (e.g., [M+Na]⁺, [M+NH₄]⁺) are not used for cross-assay weighting in the default MAMSI implementation.
- Isotopologue detection uses fixed mass difference of 1.00335 Da and 5-second RT windows; if biological samples contain natural isotopologues with unusual mass shifts or features with RT drift, isotopologue assignment may be incomplete or spurious, affecting edge weight accuracy.
- Network visualization scales poorly for >5000 features—force-directed layout becomes computationally expensive and visual interpretation degrades; consider node filtering or community detection for large networks.
- No parameter tuning is available for edge weights; users cannot adjust the 1:5:10 ratio to reflect domain knowledge or prior data about relationship reliability in their specific assay or organism.

## Evidence

- [methods] Create edges between features based on structural relationships: isotopologue links (weight=1), adduct links (weight=5), and cross-assay links (weight=10).: "Create edges between features based on structural relationships: isotopologue links (weight=1), adduct links (weight=5), and cross-assay links (weight=10)."
- [methods] all features are split into retention time (RT) windows of 5 seconds intervals, then each RT window is searched for isotopologue signatures by searching mass differences of 1.00335 Da: "all features are split into retention time (RT) windows of 5 seconds intervals, then each RT window is searched for isotopologue signatures by searching mass differences of 1.00335 Da"
- [methods] Further, we search cross-assay clusters using [M+H]⁺/[M-H]⁻ as link references.: "Further, we search cross-assay clusters using [M+H]⁺/[M-H]⁻ as link references."
- [other] Construct a NetworkX graph with features as nodes, assigning node attributes (assay, cluster membership, compound name). Create edges between features based on structural relationships.: "Construct a NetworkX graph with features as nodes, assigning node attributes (assay, cluster membership, compound name). Create edges between features based on structural relationships."
- [other] Render the graph interactively using pyvis with force-directed layout and save as HTML output_file, or display statically using NetworkX and matplotlib with optional node labels.: "Render the graph interactively using pyvis with force-directed layout and save as HTML output_file, or display statically using NetworkX and matplotlib with optional node labels."
- [readme] The different node colours represent different flattened hierarchical correlation clusters, while the edges between nodes identify their structural links.: "The different node colours represent different flattened hierarchical correlation clusters, while the edges between nodes identify their structural links."
