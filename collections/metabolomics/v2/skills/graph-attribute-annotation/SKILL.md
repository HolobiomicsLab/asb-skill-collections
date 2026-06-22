---
name: graph-attribute-annotation
description: Use when after dereplication and cosine similarity clustering have been completed on merged LC-MS/MS data, when you need to construct the final molecular network output with predicted molecules as nodes and their parent ions as a second node class, connected by edges that preserve the fragmentation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3359
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MolNotator
  - MolNotator.molnet
  - Cytoscape
  - MolNotator.mode_merger
  - MolNotator.dereplicator
  - MolNotator.cosiner
derived_from:
- doi: 10.1101/2021.12.21.473622v1
  title: MolNotator
evidence_spans:
- from MolNotator.duplicate_filter import duplicate_filter
- from MolNotator.sample_slicer import sample_slicer
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_molnotator_cq
    doi: 10.1101/2021.12.21.473622v1
    title: MolNotator
  dedup_kept_from: coll_molnotator_cq
schema_version: 0.2.0
---

# graph-attribute-annotation

## Summary

Annotate molecular network graph nodes and edges with chemical identifiers, mass values, adduct types, and intensity ranks to create a complete, queryable network representation. This skill transforms dereplication and similarity results into a structured bipartite graph suitable for visualization and downstream analysis.

## When to use

Apply this skill after dereplication and cosine similarity clustering have been completed on merged LC-MS/MS data, when you need to construct the final molecular network output with predicted molecules as nodes and their parent ions as a second node class, connected by edges that preserve the fragmentation and prediction relationships.

## When NOT to use

- Input data has not been deduplicated or merged across ionization modes — apply dereplicator and mode_merger first.
- Cosine similarity clustering has not been performed — run cosiner before exporting the final network.
- Raw MZmine output is still in its original MGF/CSV form — apply duplicate_filter and sample_slicer first.

## Inputs

- Merged molecular and ion data tables (CSV or JSON) from mode_merger
- Dereplication results linking predicted molecules to database entries
- Cosine similarity clustering output (node similarity edges)
- Ion metadata including m/z, adduct type, intensity, retention time

## Outputs

- Bipartite network graph in GraphML, GML, or edge/node CSV format
- Node table with columns: molecule_id, formula, InChI, SMILES, neutral_mass, and ion_id, m/z, adduct_code, intensity_rank
- Edge table with columns: source_node_id, target_node_id, edge_type (molecule_ion or similarity), cosine_score

## How to apply

Load the merged and deduplicated molecular and ion data (output from mode_merger and dereplicator steps) as structured tables. Construct a bipartite network graph in which predicted molecules form one node class and their parent ions (m/z values from MS data) form a second node class. Create edges between each molecule node and all ions that generated or were associated with it during fragmentation annotation (adnotator) and molecular prediction. Assign node attributes including molecular formula, InChI/SMILES identifiers, neutral mass, and ion m/z values, adduct types, and intensity ranks. Export the network in a standard format (e.g., GraphML, GML, or edge/node CSV tables) compatible with network visualization tools such as Cytoscape.

## Related tools

- **MolNotator.molnet** (Primary function that constructs the bipartite molecular network graph and assigns node/edge attributes) — https://github.com/ZzakB/MolNotator
- **Cytoscape** (Network visualization and exploration tool that imports the exported node and edge CSV tables) — https://cytoscape.org/
- **MolNotator.mode_merger** (Upstream step that produces merged molecular and ion data consumed by graph-attribute-annotation) — https://github.com/ZzakB/MolNotator
- **MolNotator.dereplicator** (Upstream step that produces dereplication results linking predicted molecules to database entries) — https://github.com/ZzakB/MolNotator
- **MolNotator.cosiner** (Upstream step that computes cosine similarity between nodes to populate edge weights) — https://github.com/ZzakB/MolNotator

## Examples

```
from MolNotator.molnet import molnet
molnet(params = params)
```

## Evaluation signals

- Node table contains all predicted molecules with non-null molecular formula, InChI/SMILES, and neutral mass values.
- Node table contains all parent ions with non-null m/z, adduct_code, and intensity_rank values.
- Edge table contains one row per molecule–ion association and one row per cosine-similarity edge; no duplicate edges.
- All edge_type values are either 'molecule_ion' or 'similarity'; cosine_score is ≥0 and ≤1 for similarity edges.
- Exported network file (GraphML, GML, or CSV) successfully imports into Cytoscape without parsing errors and displays both node classes and edge types.

## Limitations

- Multiple charge adduct processing is not implemented; only single-charge ions are supported (per README).
- Network visualization quality depends on the accuracy of upstream dereplication and cosine similarity steps; garbage input produces garbage output.
- Export format choice (GraphML vs. GML vs. CSV) may affect compatibility with downstream tools; verify format requirements before export.
- Node attribute richness depends on availability of metadata from earlier pipeline steps (e.g., retention time, intensity ranks); missing upstream data will result in incomplete node attributes.

## Evidence

- [other] The molnet function is the final step in the MolNotator pipeline that produces molecular networks, taking dereplication and cosine similarity results as input and generating network output with predicted molecules as nodes connected to their generated ions.: "The molnet function is the final step in the MolNotator pipeline that produces molecular networks, taking dereplication and cosine similarity results as input and generating network output with"
- [other] Construct a bipartite network graph where predicted molecules form one node class and their parent ions (m/z values from MS data) form a second node class. Create edges between each molecule node and all ions that generated or were associated with it during fragmentation annotation (adnotator) and molecular prediction.: "Construct a bipartite network graph where predicted molecules form one node class and their parent ions (m/z values from MS data) form a second node class. Create edges between each molecule node and"
- [other] Assign node attributes including molecular formula, InChI/SMILES identifiers, neutral mass, and ion m/z values, adduct types, and intensity ranks. Export the network in a standard format (e.g., GraphML, GML, or edge/node CSV tables) compatible with network visualization tools such as Cytoscape.: "Assign node attributes including molecular formula, InChI/SMILES identifiers, neutral mass, and ion m/z values, adduct types, and intensity ranks. Export the network in a standard format (e.g.,"
- [readme] After most steps, CSV files are exported including a node table and an edge table. Networks can thus be visualized after each step using softwares like Cytoscape by importing the two tables.: "After most steps, CSV files are exported including a node table and an edge table. Networks can thus be visualized after each step using softwares like Cytoscape by importing the two tables."
- [readme] Multiple charge adduct processing is not implemented as of yet, we would suggest only using single charge ions.: "Multiple charge adduct processing is not implemented as of yet, we would suggest only using single charge ions."
