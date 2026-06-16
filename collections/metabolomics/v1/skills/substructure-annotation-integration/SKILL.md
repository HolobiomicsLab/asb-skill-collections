---
name: substructure-annotation-integration
description: Use when you have created a GNPS molecular network (either classical or feature-based) and have computed MS2LDA motif assignments (probability and overlap scores) for the same spectra.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
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

# substructure-annotation-integration

## Summary

Integrate MS2LDA-derived substructural motif information onto GNPS mass spectral molecular networks (classical or feature-based) to annotate network nodes and edges with chemical substructure labels and confidence metrics. This enables exploration of shared structural fragments across molecular families within a single visualization.

## When to use

You have created a GNPS molecular network (either classical or feature-based) and have computed MS2LDA motif assignments (probability and overlap scores) for the same spectra. You wish to label nodes with the most prevalent substructural motifs per molecular family and edge interactions with shared motifs, producing a GraphML file suitable for visualization and interpretation in Cytoscape.

## When NOT to use

- MS2LDA experiment has not been created or motif data is unavailable for your spectral dataset.
- GNPS molecular network has not been computed; the skill requires an existing network graph as input.
- Your research question focuses on absolute abundance or fragmentation intensity rather than substructural composition; motif annotations provide chemical class information, not quantitative peak analysis.

## Inputs

- GNPS molecular network file (GraphML or JSON format)
- MS2LDA job ID or manually downloaded MS2LDA summary table (TSV)
- User-defined filtering parameters: prob, overlap, top

## Outputs

- Annotated molecular network in GraphML format with embedded substructural metadata
- TSV edge file (Mass2Motifs_Edges_*.tsv) with motif interaction annotations
- TSV node file (Mass2Motifs_Nodes_*.tsv) with TopSharedMotifs per component

## How to apply

Obtain your GNPS job ID and MS2LDA job ID (or manually download the MS2LDA summary file from ms2lda.org to avoid timeout). Load the GNPS network file (GraphML or JSON) and MS2LDA motif summary into pyMolNetEnhancer or RMolNetEnhancer. Set filtering thresholds: prob (minimum probability score; default 0.01) and overlap (minimum overlap score; default 0.3) to exclude low-confidence motif-feature associations. Specify the top parameter (default 5) to retain only the N most-shared motifs per molecular family (network component index). Execute the feature-based or classical mapping function to merge motif annotations into the network graph, assigning substructure labels and confidence scores to nodes and edges. Export the annotated network as GraphML for import into Cytoscape, where edges can be colored by shared motif interactions and nodes by TopSharedMotifs.

## Related tools

- **pyMolNetEnhancer** (Python module that executes feature-based and classical MS2LDA-to-network mapping; loads GNPS networks, filters and merges motif annotations, exports annotated GraphML) — https://github.com/madeleineernst/pyMolNetEnhancer
- **RMolNetEnhancer** (Analogous R package providing equivalent feature-based and classical mapping workflows for MS2LDA substructural integration) — https://github.com/madeleineernst/RMolNetEnhancer
- **GNPS** (Global Natural Products Social Molecular Networking platform; provides classical and feature-based molecular network creation and job IDs required for downstream motif mapping) — https://gnps.ucsd.edu/
- **MS2LDA (ms2lda.org)** (Latent Dirichlet Allocation tool for discovering and scoring MS2 motifs; produces probability and overlap scores for motif-feature associations that are mapped onto the network) — http://ms2lda.org/
- **Cytoscape** (Network visualization and analysis software for importing annotated GraphML files, coloring nodes and edges by motif annotations, and exploring shared substructures) — https://cytoscape.org/

## Evaluation signals

- Output GraphML file is syntactically valid and imports without error into Cytoscape; node and edge attributes are present.
- Nodes in the output network are labeled with TopSharedMotifs matching expected molecular family cluster IDs; TopSharedMotifs count does not exceed the user-specified 'top' parameter.
- Edge 'interaction' attribute contains motif names where applicable; edges lacking shared motifs are unmarked or empty.
- Motif annotations respect the specified prob and overlap filtering thresholds; motifs below these thresholds do not appear in the output.
- TSV node and edge files are populated, properly delimited, and contain CLUSTERID and motif columns; no null or malformed entries in key annotation fields.

## Limitations

- MS2LDA summary file may trigger server timeout during download; manual download from ms2lda.org is recommended for large experiments.
- Probability and overlap thresholds set in the pyMolNetEnhancer/RMolNetEnhancer code may not match thresholds already applied in the ms2lda.org web interface; the summary table may be pre-filtered, leading to inconsistency.
- The 'top' parameter controls display density but does not guarantee discovery of all relevant motifs; rare or low-scoring motifs shared across only 1–2 nodes may be discarded.
- Feature-based workflow requires MGF file created by MZmine (not classical spectra download) to ensure proper feature-motif alignment.
- Visualization quality in Cytoscape depends on manual configuration of color mappings for 'Stroke Color' (edges) and 'Image/Chart' (nodes); default import does not automatically apply these styling rules.

## Evidence

- [intro] pyMolNetEnhancer integrates chemical class and substructure information within mass spectral molecular networks created through the GNPS platform, supporting both classical and feature-based mapping approaches for MS2LDA substructural information.: "pyMolNetEnhancer is a python module integrating chemical class and substructure information within mass spectral molecular networks created through the Global Natural Products Social Molecular"
- [readme] Describe the three user-defined parameters for MS2LDA motif filtering.: "prob: minimal probability score for a Mass2Motif to be included. Default is 0.01. overlap: minimal overlap score for a Mass2Motif to be included. Default is 0.3. top: This parameter specifies how"
- [other] Execute the mapping function, merge motif annotations, and export as GraphML.: "Execute pyMolNetEnhancer's feature-based mapping function to annotate network nodes with MS2LDA substructural information. Merge motif annotations into the network graph, assigning substructure"
- [readme] MS2LDA summary file download timeout workaround.: "Depending on the size of this file, a server connection timeout may occur. Alternatively, you may download the file manually at http://ms2lda.org/"
- [readme] Visualization in Cytoscape using node and edge color mapping.: "To color nodes by the most shared Mass2Motifs per molecular family (network component index) select 'Image/Chart' in the 'Node' tab to the left and select Mass2Motifs shown in 'TopSharedMotifs'"
