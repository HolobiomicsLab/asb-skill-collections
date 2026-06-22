---
name: ion-to-molecule-relationship-mapping
description: Use when after dereplication and cosine similarity clustering have been completed and you have merged molecular predictions with ion metadata (m/z, adduct type, intensity).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3762
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MolNotator
  - MolNotator.molnet
  - Cytoscape
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ion-to-molecule-relationship-mapping

## Summary

Construct a bipartite network graph linking predicted molecules as one node class to their parent ions (m/z values) as a second node class, with edges representing fragmentation and annotation associations. This final step in the MolNotator pipeline produces molecular networks suitable for visualization in tools like Cytoscape.

## When to use

Apply this skill after dereplication and cosine similarity clustering have been completed and you have merged molecular predictions with ion metadata (m/z, adduct type, intensity). Use it when you need to transform flat dereplication results into a network format that shows which ions generated or were associated with each predicted molecule during LC-MS/MS annotation.

## When NOT to use

- Input data has not been deduplicated or merged across ionization modes — run dereplicator and mode_merger first
- Ion-molecule associations have not been established via adnotator — fragmentation annotations are required to define edges
- You only have raw MS/MS spectra without prior feature detection and annotation steps

## Inputs

- Deduplicated molecular data table (output from dereplicator)
- Ion metadata table with m/z values and adduct assignments (output from adnotator and mode_merger)
- Cosine similarity clustering results (output from cosiner)
- Molecular predictions with associated ion identifiers and fragmentation relationships

## Outputs

- Bipartite network in GraphML or GML format
- Node table (CSV) with molecule and ion attributes
- Edge table (CSV) linking molecules to ions
- Network visualization-ready files compatible with Cytoscape

## How to apply

Load the merged and deduplicated molecular and ion data output from mode_merger and dereplicator steps as structured tables or JSON records. Construct a bipartite network where predicted molecules form one node class and their parent ions (m/z values from MS data) form a second node class. Create edges between each molecule node and all ions that generated or were associated with it during fragmentation annotation (adnotator) and molecular prediction. Assign node attributes including molecular formula, InChI/SMILES identifiers, neutral mass for molecules, and ion m/z values, adduct types, and intensity ranks for ion nodes. Export the final network in a standard format (GraphML, GML, or edge/node CSV tables) compatible with network visualization tools such as Cytoscape.

## Related tools

- **MolNotator.molnet** (Python function that executes the bipartite network construction and export) — https://github.com/ZzakB/MolNotator
- **Cytoscape** (Network visualization and interactive exploration of the resulting molecular network) — https://cytoscape.org/

## Examples

```
from MolNotator.molnet import molnet
import yaml
with open("./params/params.yaml") as info:
    params = yaml.load(info, Loader=yaml.FullLoader)
molnet(params=params)
```

## Evaluation signals

- Node table contains expected counts: number of unique molecules plus number of unique ions from the input data
- Edge table has no NULL or missing molecule-ion associations; every edge links a valid molecule node to a valid ion node
- Exported GraphML/GML file loads without parsing errors in Cytoscape
- Node attributes (molecular formula, InChI, m/z, adduct type) are populated for all rows and match the source deduplicated data
- Network topology reflects expected fragmentation patterns: each molecule node has degree ≥ 1 (connected to at least one ion)

## Limitations

- Bipartite network construction assumes one-to-many ion-to-molecule relationships; circular or many-to-many molecule-ion associations may require post-processing
- Network complexity grows with dereplication database size and sample complexity; very large networks may be slow to visualize in Cytoscape without filtering or sample-level export
- The quality and accuracy of edges depend entirely on the correctness of prior adnotator and mode_merger steps; errors in adduct assignment or fragmentation annotation propagate into the final network
- No built-in handling of alternative or ambiguous molecular assignments; each ion is assigned to only one predicted molecule per network

## Evidence

- [other] The molnet function is the final step in the MolNotator pipeline that produces molecular networks, taking dereplication and cosine similarity results as input and generating network output with predicted molecules as nodes connected to their generated ions.: "molnet step assemble predicted molecules as network nodes and connect them to the ions that generated them to produce the final molecular network output"
- [other] Construct a bipartite network graph where predicted molecules form one node class and their parent ions (m/z values from MS data) form a second node class.: "Construct a bipartite network graph where predicted molecules form one node class and their parent ions (m/z values from MS data) form a second node class"
- [other] Assign node attributes including molecular formula, InChI/SMILES identifiers, neutral mass, and ion m/z values, adduct types, and intensity ranks.: "Assign node attributes including molecular formula, InChI/SMILES identifiers, neutral mass, and ion m/z values, adduct types, and intensity ranks"
- [other] Export the network in a standard format (e.g., GraphML, GML, or edge/node CSV tables) compatible with network visualization tools such as Cytoscape.: "Export the network in a standard format (e.g., GraphML, GML, or edge/node CSV tables) compatible with network visualization tools such as Cytoscape"
- [readme] After most steps, CSV files are exported including a node table and an edge table. Networks can thus be visualized after each step using softwares like Cytoscape by importing the two tables.: "CSV files are exported including a node table and an edge table. Networks can thus be visualized after each step using softwares like Cytoscape"
- [readme] Simplified versions of the network (only neutrals and adducts or neutrals only) can be produced after the MolNet function.: "Simplified versions of the network (only neutrals and adducts or neutrals only) can be produced after the MolNet function"
