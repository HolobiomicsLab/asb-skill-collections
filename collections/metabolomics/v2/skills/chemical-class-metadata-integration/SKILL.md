---
name: chemical-class-metadata-integration
description: Use when you have generated a GNPS molecular network (classical or feature-based
  workflow) and possess chemical class annotations (from GNPS library matching, ClassyFire,
  or other structural classifiers) that you wish to propagate onto network nodes and
  edges to enable chemical family-level.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3359
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3520
  tools:
  - pyMolNetEnhancer
  - Python
  - RMolNetEnhancer
  - GNPS
  - Cytoscape
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.3390/metabo9070144
  title: molnetenhancer
evidence_spans:
- pyMolNetEnhancer is a python module integrating chemical class and substructure
  information
- pyMolNetEnhancer is a python module
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_molnetenhancer_cq
    doi: 10.3390/metabo9070144
    title: molnetenhancer
  dedup_kept_from: coll_molnetenhancer_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo9070144
  all_source_dois:
  - 10.3390/metabo9070144
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chemical-class-metadata-integration

## Summary

Integrate chemical class metadata annotations into GNPS mass spectral molecular networks using pyMolNetEnhancer or RMolNetEnhancer to enrich network nodes and edges with putative compound family assignments. This skill bridges untargeted metabolomics annotations with chemical ontology information, enabling network-level chemical reasoning and visualization.

## When to use

You have generated a GNPS molecular network (classical or feature-based workflow) and possess chemical class annotations (from GNPS library matching, ClassyFire, or other structural classifiers) that you wish to propagate onto network nodes and edges to enable chemical family-level interpretation and Cytoscape visualization of metabolite clusters.

## When NOT to use

- You do not yet have chemical class annotations for your compounds (e.g., GNPS library matches or ClassyFire predictions have not been computed).
- Your molecular network was not created via GNPS (e.g., homemade network from custom spectral similarity calculations).
- You need substructural motif-level (Mass2Motif) annotation rather than broad chemical class labeling.

## Inputs

- GNPS molecular network edge table (TSV or GraphML format)
- GNPS molecular network node attribute table
- Chemical class annotation table (feature ID or cluster ID keyed, with chemical class labels)

## Outputs

- Enhanced network edge table with chemical class annotations (TSV)
- Enhanced network node attribute table with chemical class labels (TSV)
- GraphML network file suitable for Cytoscape visualization

## How to apply

Load the GNPS molecular network file (edge table and node attributes) and the chemical class annotation table into pyMolNetEnhancer (Python) or RMolNetEnhancer (R). Map chemical class metadata to network nodes by matching feature identifiers or cluster IDs. Merge the chemical class columns with the node and edge attribute tables. Configure output format for import into Cytoscape (TSV for nodes and edges, or GraphML). Validate that chemical class labels are correctly attached to the appropriate network components before downstream visualization and interpretation.

## Related tools

- **pyMolNetEnhancer** (Primary Python module for integrating chemical class metadata into GNPS networks) — https://github.com/madeleineernst/pyMolNetEnhancer
- **RMolNetEnhancer** (Analogous R package for integrating chemical class metadata into GNPS networks) — https://github.com/madeleineernst/RMolNetEnhancer
- **GNPS** (Source platform for molecular network generation and library annotations) — https://gnps.ucsd.edu/
- **Cytoscape** (Visualization tool for rendering annotated networks with chemical class node/edge styling) — https://cytoscape.org/

## Evaluation signals

- Chemical class labels appear in the output node attribute table and are non-null for nodes that had corresponding annotations in the input metadata.
- Edge tables correctly report chemical class interactions (e.g., edges between nodes of the same chemical class are labeled accordingly).
- GraphML or TSV output can be imported into Cytoscape without schema errors or identifier mismatches.
- Nodes can be colored or filtered by chemical class in Cytoscape without data loss or ambiguous mappings.
- Network component indices (molecular family identifiers) are preserved and correctly linked to their aggregated chemical class information.

## Limitations

- Chemical class integration quality depends entirely on the completeness and accuracy of input annotations; missing or incorrect chemical class labels will propagate into the enhanced network.
- Node matching relies on consistent identifier formats (feature IDs or cluster IDs) between the GNPS network and the chemical class annotation table; mismatched or reformatted IDs will cause silent loss of annotations.
- The module does not perform de novo chemical class prediction; it only maps pre-computed annotations onto the network structure.
- Feature-based and classical GNPS workflows use different identifier schemes; separate execution paths are required for each workflow type.

## Evidence

- [readme] chemical_class_metadata_integration_primary_function: "integrating chemical class and substructure information within mass spectral molecular networks created through the Global Natural Products Social Molecular Networking (GNPS) platform"
- [readme] chemical_class_mapping_output_format: "import the 'Mass2Motifs_Edges_Classical.tsv' output file as network into Cytoscape. Select column 'CLUSTERID1' as Source Node, column 'interact' as Interaction Type and 'CLUSTERID2' as Target Node"
- [other] chemical_class_standalone_mapping: "Map chemical class information to mass spectral molecular networks"
- [other] combined_chemical_class_motif_integration: "Map chemical class and MS2LDA substructural information to mass spectral molecular networks"
