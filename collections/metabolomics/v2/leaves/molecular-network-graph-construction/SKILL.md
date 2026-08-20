---
name: molecular-network-graph-construction
description: Use when after completing dereplication and cosine similarity clustering
  in the MolNotator pipeline, when you have merged deduplicated molecular predictions
  and ion annotations and need to construct the final network representation for visualization
  and compound identification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3625
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MolNotator
  - MolNotator.molnet
  - Cytoscape
  - MolNotator.mode_merger
  - MolNotator.dereplicator
  techniques:
  - LC-MS
  license_tier: open
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

# molecular-network-graph-construction

## Summary

Assemble predicted molecules and their parent ions into a bipartite network graph where molecule nodes are connected to all m/z ions that generated them, with standardized node attributes (molecular formula, InChI/SMILES, neutral mass, adduct type, intensity rank). This final step transforms dereplication and cosine similarity results into visualization-ready network output compatible with tools like Cytoscape.

## When to use

Apply this skill after completing dereplication and cosine similarity clustering in the MolNotator pipeline, when you have merged deduplicated molecular predictions and ion annotations and need to construct the final network representation for visualization and compound identification. Use when your goal is to expose the relationship between predicted neutral molecules and their MS-derived ion variants (adducts, fragments) in a single interpretable graph.

## When NOT to use

- When input ion data has not yet been deduplicated or annotated with adduct types; molnet requires complete adnotator and dereplicator output.
- When you need only a feature intensity table or spectral similarity matrix rather than a network graph visualization.
- If your LC-MS/MS data are single-ionization mode and you have not run mode_merger; molnet expects pre-merged data.

## Inputs

- Merged deduplicated molecular prediction table (output from mode_merger and dereplicator steps)
- Ion annotation metadata with m/z values, adduct assignments, and intensity ranks (from adnotator)
- Cosine similarity clustering results and dereplication scores
- YAML parameters file specifying export format and output folder

## Outputs

- Bipartite network in GraphML or GML format with molecule and ion nodes
- Node table (CSV) with molecule identifiers, formulas, InChI/SMILES, neutral mass, and adduct annotations
- Edge table (CSV) with molecule-ion connections and edge attributes
- Optional simplified networks: neutrals + adducts only, or neutrals only

## How to apply

Load the merged and deduplicated molecular data and ion metadata (from mode_merger and dereplicator outputs) as structured tables or JSON records. Construct a bipartite network where predicted molecules form one node class and their parent ions (m/z values with adduct annotations) form a second node class. Create directed or undirected edges connecting each molecule node to all ions that were generated from or associated with it during MS/MS fragmentation annotation (adnotator step) and molecular prediction. Assign node attributes including molecular formula, InChI/SMILES strings, neutral mass, ion m/z values, adduct type codes, and intensity ranks from the input metadata. Export the complete network in a standard format (GraphML, GML, or edge/node CSV pair tables) compatible with Cytoscape and similar network visualization software. Optionally generate simplified network variants (neutrals and adducts only, or neutrals only) by filtering node or edge subsets.

## Related tools

- **MolNotator.molnet** (Core function that performs bipartite network construction and export; final step in the MolNotator pipeline) — https://github.com/ZzakB/MolNotator
- **Cytoscape** (Downstream network visualization and analysis software compatible with GraphML/GML and CSV node/edge tables exported by molnet) — https://cytoscape.org/
- **MolNotator.mode_merger** (Prerequisite step that merges positive and negative ionization mode data into unified molecular predictions before molnet input) — https://github.com/ZzakB/MolNotator
- **MolNotator.dereplicator** (Prerequisite step that filters and deduplicates molecules using spectral and exact-mass database matching, producing final molecule list for molnet) — https://github.com/ZzakB/MolNotator

## Examples

```
molnet(params = params)
```

## Evaluation signals

- Node table contains all predicted molecules with non-null molecular formula, InChI/SMILES, and neutral mass; no duplicate molecule nodes.
- Edge table contains all parent-ion relationships with edges from each molecule to ≥1 ion; total edge count matches or exceeds ion count (accounting for shared adducts).
- All node attributes (adduct type, intensity rank, m/z) are populated and consistent with input ion metadata.
- Exported network file(s) load successfully in Cytoscape without parse errors and render bipartite layout correctly (molecules and ions visually separable).
- Optional simplified networks (neutrals only or neutrals+adducts) preserve molecular nodes and remove only appropriate ion subsets without losing connectivity information.

## Limitations

- Multiple charge adducts are not implemented; only single-charge ions are supported.
- Network complexity scales with dereplication database size and ion abundance; large datasets may produce dense, difficult-to-visualize networks.
- Adduct triangulation and secondary annotation (used in adnotator) must complete successfully before molnet; incomplete or missing adduct assignments will reduce edge count and network informativeness.
- No built-in filtering for low-intensity or low-confidence ions; users must pre-filter input data via params if needed.

## Evidence

- [other] The molnet function is the final step in the MolNotator pipeline that produces molecular networks, taking dereplication and cosine similarity results as input and generating network output with predicted molecules as nodes connected to their generated ions.: "The molnet function is the final step in the MolNotator pipeline that produces molecular networks, taking dereplication and cosine similarity results as input and generating network output with"
- [other] Construct a bipartite network graph where predicted molecules form one node class and their parent ions (m/z values from MS data) form a second node class.: "Construct a bipartite network graph where predicted molecules form one node class and their parent ions (m/z values from MS data) form a second node class."
- [other] Create edges between each molecule node and all ions that generated or were associated with it during fragmentation annotation (adnotator) and molecular prediction.: "Create edges between each molecule node and all ions that generated or were associated with it during fragmentation annotation (adnotator) and molecular prediction."
- [other] Assign node attributes including molecular formula, InChI/SMILES identifiers, neutral mass, and ion m/z values, adduct types, and intensity ranks.: "Assign node attributes including molecular formula, InChI/SMILES identifiers, neutral mass, and ion m/z values, adduct types, and intensity ranks."
- [other] Export the network in a standard format (e.g., GraphML, GML, or edge/node CSV tables) compatible with network visualization tools such as Cytoscape.: "Export the network in a standard format (e.g., GraphML, GML, or edge/node CSV tables) compatible with network visualization tools such as Cytoscape."
- [readme] After most steps, CSV files are exported including a node table and an edge table. Networks can thus be visualized after each step using softwares like Cytoscape by importing the two tables.: "After most steps, CSV files are exported including a node table and an edge table. Networks can thus be visualized after each step using softwares like Cytoscape by importing the two tables."
- [readme] Simplified versions of the network (only neutrals and adducts or neutrals only) can be produced after the `MolNet` function.: "Simplified versions of the network (only neutrals and adducts or neutrals only) can be produced after the `MolNet` function."
- [readme] Multiple charge adduct processing is not implemented as of yet, we would suggest only using single charge ions.: "Multiple charge adduct processing is not implemented as of yet, we would suggest only using single charge ions."
