---
name: molecular-network-annotation-integration
description: Use when you have a GNPS mass spectral molecular network (classical or feature-based) and MS2LDA-derived Mass2Motif data, and you need to annotate network nodes with both chemical class information from GNPS library matches and substructural motifs from MS2LDA to enable joint interpretation of.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3439
  edam_topics:
  - http://edamontology.org/topic_0203
  - http://edamontology.org/topic_0625
  tools:
  - pyMolNetEnhancer
  - Python
  - RMolNetEnhancer
  - GNPS
  - MS2LDA (ms2lda.org)
  - Cytoscape
derived_from:
- doi: 10.3390/metabo9070144
  title: molnetenhancer
evidence_spans:
- pyMolNetEnhancer is a python module integrating chemical class and substructure information
- pyMolNetEnhancer is a python module
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_molnetenhancer
    doi: 10.3390/metabo9070144
    title: molnetenhancer
  dedup_kept_from: coll_molnetenhancer
schema_version: 0.2.0
---

# molecular-network-annotation-integration

## Summary

Integrate chemical class annotations and MS2LDA substructural motif information onto GNPS mass spectral molecular network nodes in a unified operation. This skill enables joint visualization and analysis of both annotation types on a single network graph, supporting both classical and feature-based mapping workflows.

## When to use

You have a GNPS mass spectral molecular network (classical or feature-based) and MS2LDA-derived Mass2Motif data, and you need to annotate network nodes with both chemical class information from GNPS library matches and substructural motifs from MS2LDA to enable joint interpretation of molecular families by their chemical properties and fragmentation patterns.

## When NOT to use

- Input is a classical GNPS network but you only have MS2LDA data from a feature-based experiment (workflow mismatch)
- MS2LDA experiment has not been completed or summary export is unavailable
- Network nodes have no GNPS library matches and you require chemical class annotations (no input data for that layer)

## Inputs

- GNPS mass spectral molecular network (GraphML or JSON format)
- MS2LDA job ID or downloaded MS2LDA summary table
- GNPS job ID (for automated retrieval of network and library annotations)
- User-defined filtering parameters (prob, overlap, top thresholds)

## Outputs

- Enriched molecular network (GraphML format) with chemical class and MS2LDA motif attributes on nodes
- Mass2Motifs_Edges_Classical.tsv or equivalent (edge annotations with shared motif interactions)
- Mass2Motifs_Nodes_Classical.tsv or equivalent (node annotations with top shared motifs per component)
- Network graph compatible with Cytoscape for interactive visualization

## How to apply

Load the GNPS network file (GraphML or JSON format for feature-based; classical network output for standard workflows) and the MS2LDA summary table exported from ms2lda.org. Apply probability and overlap thresholds (default prob ≥ 0.01, overlap ≥ 0.3) to filter motif confidence; specify the 'top' parameter to show the N most shared motifs per molecular family (default 5). Use pyMolNetEnhancer (Python) or RMolNetEnhancer (R) to execute the mapping operation, which merges chemical class and motif annotations as node attributes in a single pass. Export the enriched network as GraphML with embedded metadata, then import into Cytoscape for visualization by coloring edges and nodes according to shared motifs and chemical families.

## Related tools

- **pyMolNetEnhancer** (Python module that executes the mapping and integration of chemical class and MS2LDA motif annotations onto GNPS network nodes in a single operation) — https://github.com/madeleineernst/pyMolNetEnhancer
- **RMolNetEnhancer** (R package providing equivalent functionality to pyMolNetEnhancer for the same molecular network annotation and integration workflow) — https://github.com/madeleineernst/RMolNetEnhancer
- **GNPS** (Platform that generates mass spectral molecular networks and provides library matches for chemical class annotation; requires GNPS job ID as input) — https://gnps.ucsd.edu/
- **MS2LDA (ms2lda.org)** (Web server that runs Latent Dirichlet Allocation analysis on MS/MS spectra to derive Mass2Motif substructural information; requires MS2LDA job ID or summary export as input) — http://ms2lda.org/
- **Cytoscape** (Desktop application for importing and interactively visualizing the enriched GraphML network, with edge and node coloring based on shared motifs and chemical classes) — https://cytoscape.org/

## Examples

```
devtools::install_github("madeleineernst/RMolNetEnhancer"); # Then run Mass2Motifs_2_Network_Classical.ipynb with GNPS job ID and MS2LDA job ID, specifying prob=0.01, overlap=0.3, top=5
```

## Evaluation signals

- Output GraphML file contains all nodes and edges from the input GNPS network with no loss of connectivity
- Each network node has both chemical class attributes (from GNPS library matches) and MS2LDA motif attributes (probability and overlap scores) attached
- Probability and overlap filtering was correctly applied: no motifs with prob < threshold or overlap < threshold appear in the output
- The 'TopSharedMotifs' node attribute contains the top N motifs per molecular family component, where N equals the user-specified 'top' parameter
- Network successfully imports into Cytoscape without schema errors; edges and nodes can be colored discretely by 'interaction' column and 'TopSharedMotifs' attribute respectively

## Limitations

- Server connection timeouts may occur when downloading large MS2LDA summary files; manual download from ms2lda.org is an alternative
- Probability and overlap thresholds should ideally be set in the ms2lda.org web app before export to ensure consistency between web inspection and integration results
- Feature-based and classical workflows are mutually exclusive—the mapping approach must match the type of GNPS network created (feature-based molecular networks require feature-based MS2LDA experiments and mapping)
- Chemical class annotation relies on GNPS public library matches; nodes without library hits will lack chemical class information in the integrated output

## Evidence

- [intro] pyMolNetEnhancer is a python module integrating chemical class and substructure information within mass spectral molecular networks created through the GNPS platform: "pyMolNetEnhancer is a python module integrating chemical class and substructure information within mass spectral molecular networks created through the GNPS platform"
- [other] Load the GNPS feature-based molecular network file (GraphML or JSON format). Load MS2LDA-derived substructural motif data mapping features to molecular fragments. Execute pyMolNetEnhancer's feature-based mapping function to annotate network nodes with MS2LDA substructural information.: "Load the GNPS feature-based molecular network file (GraphML or JSON format). Load MS2LDA-derived substructural motif data mapping features to molecular fragments. Execute pyMolNetEnhancer's"
- [readme] prob: minimal probability score for a Mass2Motif to be included. Default is 0.01. overlap: minimal overlap score for a Mass2Motif to be included. Default is 0.3.: "prob: minimal probability score for a Mass2Motif to be included. Default is 0.01. overlap: minimal overlap score for a Mass2Motif to be included. Default is 0.3."
- [readme] top: This parameter specifies how many most shared motifs per molecular family (network component index) should be shown. Default is 5.: "top: This parameter specifies how many most shared motifs per molecular family (network component index) should be shown. Default is 5."
- [readme] To color nodes by the most shared Mass2Motifs per molecular family (network component index) select 'Image/Chart' in the 'Node' tab to the left and select Mass2Motifs shown in 'TopSharedMotifs': "To color nodes by the most shared Mass2Motifs per molecular family (network component index) select 'Image/Chart' in the 'Node' tab to the left and select Mass2Motifs shown in 'TopSharedMotifs'"
