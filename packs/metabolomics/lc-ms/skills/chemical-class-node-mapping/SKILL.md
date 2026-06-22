---
name: chemical-class-node-mapping
description: Use when you have a GNPS mass spectral molecular network (in graphml or cytoscape format) and want to enrich its nodes with chemical class information derived from GNPS public library spectral matches.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3359
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - pyMolNetEnhancer
  - Python
  - RMolNetEnhancer
  - GNPS
  - Cytoscape
  techniques:
  - LC-MS
derived_from:
- doi: 10.3390/metabo9070144
  title: molnetenhancer
evidence_spans:
- pyMolNetEnhancer is a python module integrating chemical class and substructure information
- pyMolNetEnhancer is a python module
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_molnetenhancer
    doi: 10.3390/metabo9070144
    title: molnetenhancer
  dedup_kept_from: coll_molnetenhancer
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo9070144
  all_source_dois:
  - 10.3390/metabo9070144
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chemical-class-node-mapping

## Summary

Maps chemical class annotations from GNPS public library matches onto nodes of a mass spectral molecular network, enabling direct integration of structural classification data into network visualization and analysis. This skill enables researchers to annotate molecular families with their putative chemical classifications.

## When to use

You have a GNPS mass spectral molecular network (in graphml or cytoscape format) and want to enrich its nodes with chemical class information derived from GNPS public library spectral matches. Use this when you need to visualize which molecular families belong to specific chemical classes (e.g., alkaloids, terpenoids, polyketides) directly on the network graph.

## When NOT to use

- Your input is an unannotated or de novo molecular network with no GNPS public library matches available.
- You only have MS1 spectral data without MS2 fragmentation patterns required for GNPS networking.
- You need to integrate MS2LDA substructural motif information only—use the feature-based motif mapping skill instead.

## Inputs

- GNPS mass spectral molecular network file (graphml or cytoscape format)
- GNPS public library matches or chemical class metadata
- GNPS job ID (for automated retrieval of network and annotations)

## Outputs

- Annotated mass spectral molecular network (graphml or cytoscape format) with chemical class attributes embedded in nodes
- Network nodes labeled with chemical class information
- Nodes and edges TSV files with chemical class metadata (optional alternative output)

## How to apply

Load your GNPS mass spectral molecular network file and retrieve or prepare chemical class metadata from GNPS public library matches using either pyMolNetEnhancer (Python) or RMolNetEnhancer (R). Map chemical class information to network nodes by matching library annotations to cluster IDs; the modules handle this via a feature-based matching approach. Export the annotated network in graphml or cytoscape format with chemical class labels and attributes embedded as node properties. Validate by importing into Cytoscape and confirming that nodes display chemical class attributes and can be styled or filtered by class.

## Related tools

- **pyMolNetEnhancer** (Python module that performs automated chemical class mapping to molecular network nodes from GNPS library annotations) — https://github.com/madeleineernst/pyMolNetEnhancer
- **RMolNetEnhancer** (R package providing equivalent chemical class mapping functionality to pyMolNetEnhancer) — https://github.com/madeleineernst/RMolNetEnhancer
- **GNPS** (Global Natural Products Social Molecular Networking platform that generates the initial molecular network and provides public library spectral matches) — https://gnps.ucsd.edu/
- **Cytoscape** (Network visualization and analysis tool for importing and styling the annotated graphml network by chemical class) — https://cytoscape.org/

## Evaluation signals

- All nodes in the exported network graph contain chemical class attributes (verified by opening graphml in a text editor or Cytoscape property inspector).
- Chemical class labels are non-null and match GNPS library taxonomy for a random sample of nodes.
- Network can be imported into Cytoscape without errors and nodes are styleable/filterable by the chemical class attribute.
- Node count and network topology are preserved after mapping (no nodes dropped due to missing chemical class data).
- Exported TSV files (if produced) list each node ID with its corresponding chemical class and match confidence score.

## Limitations

- Chemical class annotation is limited to matches present in the GNPS public library; nodes without public library matches will have missing or null chemical class values.
- Mapping quality depends on spectral library coverage and the quality of the input GNPS network (requires high cosine similarity and ion overlap thresholds in the GNPS job).
- Chemical class information reflects only spectral-based classification from library matching, not structural elucidation; putative assignments may not resolve to a single class.
- Feature-based molecular networking (required for some workflows) may produce fragmented networks that reduce the effectiveness of chemical class-based family grouping.

## Evidence

- [intro] Mapped chemical class information from GNPS public library: "pyMolNetEnhancer is a python module that integrates chemical class information within mass spectral molecular networks created through the GNPS platform"
- [other] Method: load network and map chemical class to nodes: "Load a GNPS mass spectral molecular network file (e.g., graphml or cytoscape format). Prepare chemical class metadata or retrieve it from the GNPS public library. Use pyMolNetEnhancer to map chemical"
- [other] Export annotated network with embedded chemical class attributes: "Export the annotated network in a standard format (e.g., graphml, cytoscape) with chemical class labels and attributes embedded"
- [readme] Visualization and styling by chemical class in Cytoscape: "To visualize results import the .graphml output file into Cytoscape. To color nodes by the most shared Mass2Motifs per molecular family (network component index) select 'Image/Chart' in the 'Node'"
- [readme] RMolNetEnhancer provides R implementation of same functionality: "RMolNetEnhancer is an R package integrating chemical class and substructure information within mass spectral molecular networks created through the Global Natural Products Social Molecular Networking"
