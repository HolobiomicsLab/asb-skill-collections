---
name: network-graph-manipulation-python
description: Use when you have a molecular network graph exported from GNPS (as GraphML, JSON, or adjacency format) and separate experimental data (bioassay activity matrix, feature quantification table, or MS/MS annotations) indexed by feature ID, retention time, or m/z.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0602
  tools:
  - MZmine2
  - Jupyter notebook
  - GNPS
  - NetworkX
  - pandas
  - Cytoscape
  - Optimus
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.jnatprod.7b00737
  title: Bioactivity-Based Molecular Networking
evidence_spans:
- open bioinformatic tools, such [MZmine2](http://mzmine.github.io/)
- a Jupyter notebook, and the GNPS web-platform
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_bioactivity_based_molecular_networking_cq
    doi: 10.1021/acs.jnatprod.7b00737
    title: Bioactivity-Based Molecular Networking
  dedup_kept_from: coll_bioactivity_based_molecular_networking_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jnatprod.7b00737
  all_source_dois:
  - 10.1021/acs.jnatprod.7b00737
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# network-graph-manipulation-python

## Summary

Load and manipulate molecular network graphs (nodes, edges, attributes) exported from GNPS into Python data structures, then integrate them with external bioactivity or quantification matrices by matching on molecular feature identifiers and retention time / m/z coordinates. This skill bridges untargeted metabolomics feature networks with downstream annotation or activity scoring.

## When to use

You have a molecular network graph exported from GNPS (as GraphML, JSON, or adjacency format) and separate experimental data (bioassay activity matrix, feature quantification table, or MS/MS annotations) indexed by feature ID, retention time, or m/z. You need to merge these datasets in memory and compute per-node attributes (e.g., bioactivity scores, normalized intensities) for visualization or statistical analysis.

## When NOT to use

- Input network is already annotated with the desired attributes (e.g., bioactivity scores already present in GNPS export).
- Feature data is not indexable by ID, retention time, or m/z (e.g., completely different coordinate systems between network and matrix).
- Your goal is to construct the molecular network de novo from MS/MS spectra; use MS/MS networking tools (GNPS, MZmine2) instead.

## Inputs

- GNPS molecular network graph (GraphML, JSON, or adjacency list format with node identifiers and edges)
- Feature quantification matrix (CSV or TSV: fractions/samples × features, indexed by feature ID or retention time + m/z)
- Bioassay activity matrix (fractions/samples × bioactivity measurements, with retention time and m/z coordinates for feature matching)

## Outputs

- Annotated molecular network graph with per-node bioactivity scores or quantification values (GraphML or JSON)
- Network node attribute table (node ID, bioactivity score, matched feature metadata)
- Summary statistics (e.g., distribution of bioactivity scores across network nodes)

## How to apply

In a Jupyter notebook or Python script, load the GNPS network structure (edges and node IDs) using a graph library such as NetworkX. Separately load the experimental data matrix (e.g., fractions × bioactivity measurements or samples × feature intensities) as a pandas DataFrame. Match nodes to rows in the matrix using retention time and m/z tolerance (e.g., ±5 ppm) or exact feature ID lookup. For each matched node, aggregate the corresponding matrix values (sum, mean, or max across rows) and assign the result as a node attribute. Export the annotated graph in a Cytoscape-compatible format (GraphML or JSON) for downstream visualization and filtering.

## Related tools

- **GNPS** (Generates the molecular network graph structure (node IDs, edges) from MS/MS spectral clustering) — http://gnps.ucsd.edu
- **Jupyter notebook** (Execution environment for Python-based graph manipulation, data integration, and visualization)
- **NetworkX** (Python library for loading, manipulating, and exporting network graphs; supports GraphML I/O)
- **pandas** (Python library for loading and aligning feature quantification and bioactivity matrices)
- **Cytoscape** (Interactive visualization and filtering of annotated molecular networks) — http://www.cytoscape.org/
- **MZmine2** (Generates the feature quantification matrix and MS/MS data upstream of network integration) — http://mzmine.github.io/
- **Optimus** (Alternative LC-MS feature detection and quantification pipeline; output table can be integrated with GNPS network) — https://github.com/MolecularCartography/Optimus

## Examples

```
import networkx as nx
import pandas as pd
G = nx.read_graphml('gnps_network.graphml')
bioactivity_matrix = pd.read_csv('bioactivity_fractions.csv', index_col=0)
for node_id, node_data in G.nodes(data=True):
    rt, mz = float(node_data['retention_time']), float(node_data['mz'])
    matched_rows = bioactivity_matrix[(bioactivity_matrix['mz'] - mz).abs() < 0.005]
    node_data['bioactivity_score'] = matched_rows.iloc[:, 2:].sum(axis=1).max() if not matched_rows.empty else 0
nx.write_graphml(G, 'annotated_network.graphml')
```

## Evaluation signals

- All nodes in the GNPS network are successfully matched to rows in the feature matrix (verify match count and retention time / m/z tolerances).
- Bioactivity scores are computed for each node and fall within expected value ranges (e.g., non-negative, reasonable distribution across nodes).
- Exported GraphML or JSON file is valid and loads without errors in Cytoscape or a graph visualization tool.
- Aggregation method (sum, mean, max) is applied consistently across all nodes; spot-check a few high-activity nodes to verify correctness.
- Node attributes in the exported graph include original feature metadata (retention time, m/z, node ID) plus computed scores, confirming bidirectional traceability.

## Limitations

- Feature matching relies on retention time and m/z tolerances; misalignment can occur if tolerance windows are too broad or if the same m/z appears in many fractions.
- Bioactivity aggregation (sum, mean, max) may mask complex, non-linear relationships between feature presence and activity; post-hoc filtering or scoring refinement may be needed.
- GNPS network construction may group distinct molecular features into a single node if MS/MS spectra are highly similar; this can conflate bioactivity signals.
- The workflow does not validate or resolve structural ambiguities in spectral matches; MS/MS annotations remain at the putative level (Metabolomics Standards Initiative Level 2).
- No integrated changelog or version tracking in the Jupyter notebook; reproducibility depends on exact tool versions and parameter choices documented externally.

## Evidence

- [other] Load the molecular network graph structure (e.g., network edges and node identifiers from GNPS) and the bioassay-guided fractionation activity matrix (fractions × bioactivity measurements) into Python.: "Load the molecular network graph structure (e.g., network edges and node identifiers from GNPS) and the bioassay-guided fractionation activity matrix (fractions × bioactivity measurements) into"
- [other] Map fractionation samples to molecular network features using retention time and mass-to-charge ratio matching.: "Map fractionation samples to molecular network features using retention time and mass-to-charge ratio matching."
- [other] Aggregate bioactivity measurements across fractions for each feature, computing a per-feature bioactivity score (e.g., sum, mean, or max of activity values in fractions containing that feature).: "Aggregate bioactivity measurements across fractions for each feature, computing a per-feature bioactivity score (e.g., sum, mean, or max of activity values in fractions containing that feature)."
- [other] Annotate the molecular network with bioactivity scores as node attributes.: "Annotate the molecular network with bioactivity scores as node attributes."
- [other] Export the integrated network with bioactivity annotations in a format compatible with Cytoscape or network visualization tools (e.g., GraphML or JSON).: "Export the integrated network with bioactivity annotations in a format compatible with Cytoscape or network visualization tools (e.g., GraphML or JSON)."
- [readme] The workflow relies on open bioinformatic tools, such [MZmine2]... a Jupyter notebook, and the GNPS web-platform...The code is released as a Jupyter notebook for easiness and reproducibility.: "The workflow relies on open bioinformatic tools... a Jupyter notebook, and the GNPS web-platform...The code is released as a Jupyter notebook for easiness and reproducibility."
