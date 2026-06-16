---
name: substructural-motif-annotation
description: Use when you have created a GNPS molecular network (classical or feature-based workflow) and separately run an MS2LDA experiment on the corresponding MGF file, and you want to associate each network node with its constituent substructural motifs and visualize which motifs are shared between.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3778
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
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

# substructural-motif-annotation

## Summary

Maps MS2LDA-derived Mass2Motif substructural annotations onto nodes in GNPS mass spectral molecular networks, enabling integration of substructure assignments with molecular family relationships. This skill bridges LDA-based motif discovery and network visualization to annotate spectra with shared chemical building blocks.

## When to use

You have created a GNPS molecular network (classical or feature-based workflow) and separately run an MS2LDA experiment on the corresponding MGF file, and you want to associate each network node with its constituent substructural motifs and visualize which motifs are shared between connected compounds.

## When NOT to use

- You have not yet created a GNPS molecular network or do not have MS2LDA results for your spectral data.
- Your MS2LDA experiment was run on a different MGF file than the one used for GNPS network creation, causing precursor m/z and spectral metadata mismatches.
- You only have pre-existing spectral annotations (e.g., from library matching) and do not need de novo substructure discovery via LDA motifs.

## Inputs

- GNPS molecular network file (graphml or JSON format)
- MS2LDA Mass2Motif summary table or job results
- MGF clustered spectra file (used to generate both GNPS and MS2LDA analyses)

## Outputs

- Annotated molecular network file (.graphml or JSON) with motif metadata in node attributes
- Mass2Motifs_Edges_Classical.tsv or Mass2Motifs_Edges_FeatureBased.tsv (motif-sharing relationships between nodes)
- Mass2Motifs_Nodes_Classical.tsv or Mass2Motifs_Nodes_FeatureBased.tsv (node-motif assignments and top shared motifs per component)

## How to apply

Load the GNPS molecular network file (graphml or JSON format) and the MS2LDA Mass2Motif summary table into pyMolNetEnhancer or RMolNetEnhancer. Align MS2LDA motif identifiers to network nodes using the classical or feature-based mapping function, which matches motifs to nodes based on precursor m/z and spectral similarity. Set filtering thresholds: minimal probability score (default 0.01) and overlap score (default 0.3) to exclude low-confidence motif assignments. Optionally configure the 'top' parameter to select the N most shared motifs per molecular family (network component). Annotate each node with mapped motif IDs and confidence indicators, then export the enhanced network as a .graphml file with motif metadata embedded in node attributes for downstream visualization in Cytoscape.

## Related tools

- **pyMolNetEnhancer** (Python module that loads GNPS networks and MS2LDA motif data, performs node-motif alignment, filters by probability and overlap thresholds, and exports annotated network files.) — https://github.com/madeleineernst/pyMolNetEnhancer
- **RMolNetEnhancer** (R package providing equivalent functionality for classical and feature-based MS2LDA motif mapping onto GNPS networks.) — https://github.com/madeleineernst/RMolNetEnhancer
- **GNPS** (Platform for creating molecular networks from tandem MS data; provides classical and feature-based network construction workflows and outputs graphml/JSON network files.)
- **MS2LDA (ms2lda.org)** (Web platform for running Latent Dirichlet Allocation experiments on clustered MGF spectra to extract Mass2Motif substructural motif assignments.)
- **Cytoscape** (Network visualization and analysis software used to import and color the annotated .graphml network files by motif sharing patterns and node attributes.)

## Evaluation signals

- All nodes in the output network file carry non-empty motif metadata attributes (TopSharedMotifs or motif IDs) matching MS2LDA assignments.
- Edges between nodes include 'interaction' or 'interact' columns showing shared motif identities, confirming cross-node motif relationships were correctly propagated.
- Node-motif probability and overlap scores are consistent with the specified thresholds (prob ≥ 0.01, overlap ≥ 0.3 by default), verifiable in the accompanying .tsv node tables.
- When imported into Cytoscape, nodes and edges can be colored by motif assignments without schema errors, and visual clustering of nodes sharing the same motifs aligns with expected molecular family structure.
- The 'top' parameter correctly limits per-component motif reporting; e.g., if top=5, TopSharedMotifs lists exactly the 5 most prevalent motifs within each network component.

## Limitations

- Mapping accuracy depends on precursor m/z and spectral similarity alignment between GNPS and MS2LDA; server connection timeouts during MS2LDA data retrieval may require manual file download.
- Probability and overlap thresholds are user-configurable but must be set consistently in both the ms2lda.org web app and the mapping function to avoid conflicting filtered motif-document relations.
- The classical workflow maps motifs to clustered nodes, while the feature-based workflow maps to individual features; results are not directly comparable if different GNPS workflows are used.
- MS2LDA motif discovery is probabilistic and sensitive to LDA hyperparameters and MGF composition; low-quality or small datasets may yield motifs with poor interpretability.

## Evidence

- [other] pyMolNetEnhancer integrates chemical class and substructure information within mass spectral molecular networks created through the GNPS platform: "pyMolNetEnhancer is a python module integrating chemical class and substructure information within mass spectral molecular networks created through the Global Natural Products Social Molecular"
- [other] MS2LDA motif data is loaded and aligned to molecular network nodes based on precursor m/z and spectral properties: "Use pyMolNetEnhancer's classical-mode mapping function to align MS2LDA motif identifiers to corresponding nodes in the molecular network based on precursor m/z and spectral similarity"
- [readme] User-configurable probability and overlap thresholds control which motif assignments are included in the final output: "prob: minimal probability score for a Mass2Motif to be included. Default is 0.01. overlap: minimal overlap score for a Mass2Motif to be included. Default is 0.3."
- [readme] The 'top' parameter limits the number of most shared motifs reported per molecular family component: "top: This parameter specifies how many most shared motifs per molecular family (network component index) should be shown. Default is 5."
- [readme] Network visualization in Cytoscape requires importing the annotated .graphml file and mapping node/edge attributes to visual properties: "To visualize results import the .graphml output file into Cytoscape. To color edges based on shared Mass2Motifs in between nodes select 'Stroke Color' in the 'Edge' tab to the left and choose"
