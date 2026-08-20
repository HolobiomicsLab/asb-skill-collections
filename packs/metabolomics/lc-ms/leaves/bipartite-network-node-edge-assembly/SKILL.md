---
name: bipartite-network-node-edge-assembly
description: Use when after completing dereplication and cosine similarity clustering in the MolNotator workflow, when you have merged, dereplicated molecular and ion data (output from mode_merger and dereplicator steps) and need to assemble the final molecular network representation connecting predicted.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0365
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_0091
  tools:
  - MolNotator
  - Cytoscape
  - Python (matchms, pandas, networkx)
  techniques:
  - LC-MS
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

# bipartite-network-node-edge-assembly

## Summary

Assemble predicted molecules and their parent ions into a bipartite network graph, where molecules form one node class, ions form another, and edges connect each molecule to all ions that generated it during MS/MS fragmentation and annotation. This final step in the MolNotator pipeline outputs network-ready node and edge tables compatible with visualization tools like Cytoscape.

## When to use

After completing dereplication and cosine similarity clustering in the MolNotator workflow, when you have merged, dereplicated molecular and ion data (output from mode_merger and dereplicator steps) and need to assemble the final molecular network representation connecting predicted neutral molecules to their parent m/z ions for visualization and interpretation.

## When NOT to use

- Input is unannotated or unmerged MS/MS data (use preceding pipeline steps: duplicate_filter, sample_slicer, fragnotator, adnotator, mode_merger, dereplicator first).
- You lack cosine similarity or dereplication results; the molnet step assumes annotated, dereplicated molecule-ion associations from prior steps.
- You are attempting to visualize only raw spectral clusters without predicted neutral molecules; use earlier intermediate steps instead.

## Inputs

- Merged ion-molecule data table (output from mode_merger)
- Deduplicated molecular predictions and ion associations (output from dereplicator)
- Adduct annotations and fragmentation relationships (from adnotator)
- Cosine similarity clustering results (from cosiner)

## Outputs

- Node table (CSV): molecule and ion nodes with attributes (formula, InChI/SMILES, neutral mass, m/z, adduct, intensity rank)
- Edge table (CSV): bipartite connections between molecule nodes and ion nodes
- Network file (GraphML or GML): complete bipartite network ready for Cytoscape visualization

## How to apply

Load the merged and deduplicated molecular and ion data as structured tables or JSON records from preceding pipeline steps. Construct a bipartite graph where predicted molecules (neutral nodes) form one class and their parent ions (m/z values with adduct annotations) form a second class. Create edges between each molecule node and all ions associated with it during fragmentation annotation (adnotator output) and molecular prediction. Assign node attributes including molecular formula, InChI/SMILES identifiers, neutral mass for molecules, and m/z values, adduct types, and intensity ranks for ions. Export the network in standard format (GraphML, GML, or paired edge/node CSV tables) compatible with Cytoscape. The rationale is to make the relationship between predicted molecular entities and their generating spectral features explicit and queryable for downstream analysis.

## Related tools

- **MolNotator** (Python package providing the molnet() function to assemble and export bipartite molecular networks) — https://github.com/ZzakB/MolNotator
- **Cytoscape** (Network visualization software that imports node and edge CSV tables or GraphML files for interactive exploration and annotation) — https://cytoscape.org/
- **Python (matchms, pandas, networkx)** (Core libraries for graph construction, attribute assignment, and tabular data manipulation within MolNotator)

## Examples

```
from MolNotator.molnet import molnet
import yaml
with open("./params/params.yaml") as info:
    params = yaml.load(info, Loader=yaml.FullLoader)
molnet(params = params)
```

## Evaluation signals

- Node tables contain all predicted molecules with populated molecular formula, InChI/SMILES, and neutral mass fields; ion nodes contain populated m/z, adduct code, and intensity rank fields.
- Edge table row count equals the sum of edges from all molecules to their associated ions; no orphaned molecules or ions without edges.
- Network exports successfully in GraphML/GML format and loads into Cytoscape without parsing errors; node and edge attributes are preserved.
- Bipartite structure is maintained: edges only connect molecule nodes to ion nodes, never molecule-to-molecule or ion-to-ion.
- Sample-level networks (if export_samples=true in params.yaml) correctly partition the global network by sample while preserving all molecule-ion associations.

## Limitations

- Multiple charge adducts are not supported; only single-charge ions are processed and annotated.
- Network assembly depends critically on the accuracy of prior annotation and dereplication steps; errors propagate to the final network.
- Node and edge attribute completeness varies with the quality of input database matches and fragmentation annotations; missing or ambiguous annotations result in sparse or missing attributes.
- GraphML and GML export may produce large files for high-complexity networks (many molecules, many ions per molecule); very large networks may require subsampling or filtering before Cytoscape visualization.

## Evidence

- [other] The molnet function is the final step in the MolNotator pipeline that produces molecular networks, taking dereplication and cosine similarity results as input and generating network output with predicted molecules as nodes connected to their generated ions.: "The molnet function is the final step in the MolNotator pipeline that produces molecular networks, taking dereplication and cosine similarity results as input and generating network output with"
- [other] Construct a bipartite network graph where predicted molecules form one node class and their parent ions (m/z values from MS data) form a second node class.: "Construct a bipartite network graph where predicted molecules form one node class and their parent ions (m/z values from MS data) form a second node class."
- [other] Create edges between each molecule node and all ions that generated or were associated with it during fragmentation annotation (adnotator) and molecular prediction.: "Create edges between each molecule node and all ions that generated or were associated with it during fragmentation annotation (adnotator) and molecular prediction."
- [other] Assign node attributes including molecular formula, InChI/SMILES identifiers, neutral mass, and ion m/z values, adduct types, and intensity ranks.: "Assign node attributes including molecular formula, InChI/SMILES identifiers, neutral mass, and ion m/z values, adduct types, and intensity ranks."
- [other] Export the network in a standard format (e.g., GraphML, GML, or edge/node CSV tables) compatible with network visualization tools such as Cytoscape.: "Export the network in a standard format (e.g., GraphML, GML, or edge/node CSV tables) compatible with network visualization tools such as Cytoscape."
- [readme] The final network with molecules, adducts, in-source fragments, with dereplication and a degree of cosine clustering can be opened after the `Cosiner` function. Simplified versions of the network (only neutrals and adducts or neutrals only) can be produced after the `MolNet` function.: "The final network with molecules, adducts, in-source fragments, with dereplication and a degree of cosine clustering can be opened after the `Cosiner` function. Simplified versions of the network"
- [readme] Multiple charge adduct processing is not implemented as of yet, we would suggest only using single charge ions.: "Multiple charge adduct processing is not implemented as of yet, we would suggest only using single charge ions."
