---
name: network-file-format-export
description: Use when after completing dereplication and cosine similarity clustering
  in the MolNotator pipeline, when you have finalized molecular network data with
  molecule–ion relationships and need to visualize, analyze, or share the network
  in external software.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0226
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - MolNotator
  - MolNotator.molnet
  - Cytoscape
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2021.12.21.473622v1
  all_source_dois:
  - 10.1101/2021.12.21.473622v1
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# network-file-format-export

## Summary

Export molecular network node and edge tables into standard graph formats (GraphML, GML, or edge/node CSV pairs) compatible with visualization tools like Cytoscape. This skill transforms the final MolNotator bipartite network (predicted molecules as nodes, parent ions as edges) into portable, tool-agnostic representations.

## When to use

After completing dereplication and cosine similarity clustering in the MolNotator pipeline, when you have finalized molecular network data with molecule–ion relationships and need to visualize, analyze, or share the network in external software. Use this step when the internal MolNotator representation must be converted to a format consumable by Cytoscape or other graph analysis platforms.

## When NOT to use

- Input data has not been deduplicated or merged across ionization modes; run dereplicator and mode_merger first.
- Ion–molecule associations are incomplete or lack cosine similarity annotations; the network will be uninformative without edge confidence metrics.
- Target is statistical analysis or machine learning rather than interactive visualization; CSV tables alone may be sufficient without format export.

## Inputs

- Merged and deduplicated molecular prediction table (output from dereplicator)
- Ion metadata and cosine similarity results (output from cosiner)
- Ion–molecule associations from adnotator and fragnotator steps
- Molecular formula, InChI, SMILES, and neutral mass annotations

## Outputs

- Node table (CSV): predicted molecules with attributes (formula, InChI, SMILES, mass)
- Edge table (CSV): ion–molecule connections with m/z, adduct type, intensity
- GraphML or GML format network file (optional, single-file representation)
- Cytoscape-compatible network visualization files

## How to apply

The molnet function takes merged, deduplicated molecular and ion data (output from mode_merger and dereplicator steps) and constructs a bipartite network where predicted molecules form one node class and their parent ions (m/z values) form a second node class. Create edges between molecule nodes and all ions that generated them, assigning node attributes including molecular formula, InChI/SMILES identifiers, neutral mass, ion m/z values, adduct types, and intensity ranks. Export the network in GraphML, GML, or edge/node CSV table formats; CSV export is the recommended pathway for Cytoscape import, as it separates node attributes and connectivity into two linked tables.

## Related tools

- **MolNotator.molnet** (Final pipeline step that constructs and exports the bipartite network from deduplicated molecular predictions and ion associations) — https://github.com/ZzakB/MolNotator
- **Cytoscape** (Graph visualization and analysis platform that imports the exported node and edge CSV tables to render and explore the molecular network interactively) — https://cytoscape.org/

## Examples

```
from MolNotator.molnet import molnet
import yaml
with open('./params/params.yaml') as f:
    params = yaml.load(f, Loader=yaml.FullLoader)
molnet(params=params)
```

## Evaluation signals

- Node table contains all predicted molecules with non-null molecular formula, InChI, SMILES, and neutral mass fields.
- Edge table has one row per ion–molecule association, with valid m/z values, adduct annotations, and intensity ranks matching input data.
- CSV tables import successfully into Cytoscape without schema errors; bipartite structure is preserved (molecules and ions are distinct node types).
- GraphML or GML file (if generated) is valid XML/text and opens in standard graph editors without parsing errors.
- Network topology reflects expected dereplication and cosine clustering results: related molecules are connected via shared or similar ions.

## Limitations

- Multiple-charge adducts are not supported; only single-charge ions are processed correctly.
- Export format choice (GraphML vs. GML vs. CSV) depends on downstream visualization tool; Cytoscape strongly prefers CSV node/edge pairs over single-file formats.
- Node and edge attributes are limited to those assigned during earlier pipeline steps (adnotator, fragnotator, dereplicator); missing annotations will result in sparse or null attribute fields.
- Large networks (>10,000 nodes or edges) may be computationally expensive to visualize in Cytoscape; sample-level export (via export_samples parameter) is recommended for networks spanning multiple samples.

## Evidence

- [other] The molnet function is the final step in the MolNotator pipeline that produces molecular networks, taking dereplication and cosine similarity results as input and generating network output with predicted molecules as nodes connected to their generated ions.: "The molnet function is the final step in the MolNotator pipeline that produces molecular networks, taking dereplication and cosine similarity results as input and generating network output with"
- [other] Construct a bipartite network graph where predicted molecules form one node class and their parent ions (m/z values from MS data) form a second node class. Create edges between each molecule node and all ions that generated or were associated with it during fragmentation annotation (adnotator) and molecular prediction.: "Construct a bipartite network graph where predicted molecules form one node class and their parent ions (m/z values from MS data) form a second node class. Create edges between each molecule node and"
- [other] Assign node attributes including molecular formula, InChI/SMILES identifiers, neutral mass, and ion m/z values, adduct types, and intensity ranks. Export the network in a standard format (e.g., GraphML, GML, or edge/node CSV tables) compatible with network visualization tools such as Cytoscape.: "Assign node attributes including molecular formula, InChI/SMILES identifiers, neutral mass, and ion m/z values, adduct types, and intensity ranks. Export the network in a standard format (e.g.,"
- [readme] After most steps, CSV files are exported including a node table and an edge table. Networks can thus be visualized after each step using softwares like Cytoscape by importing the two tables.: "After most steps, CSV files are exported including a node table and an edge table. Networks can thus be visualized after each step using softwares like Cytoscape by importing the two tables."
- [readme] The final network with molecules, adducts, in-source fragments, with dereplication and a degree of cosine clustering can be opened after the Cosiner function. Simplified versions of the network (only neutrals and adducts or neutrals only) can be produced after the MolNet function.: "The final network with molecules, adducts, in-source fragments, with dereplication and a degree of cosine clustering can be opened after the Cosiner function. Simplified versions of the network (only"
