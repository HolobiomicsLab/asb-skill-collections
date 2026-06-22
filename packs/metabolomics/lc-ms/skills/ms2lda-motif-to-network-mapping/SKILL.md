---
name: ms2lda-motif-to-network-mapping
description: Use when when you have a GNPS molecular network (classical or feature-based) and corresponding MS2LDA experiment results, and you want to annotate network nodes with discovered substructural motifs to support structural elucidation and chemical family interpretation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3762
  edam_topics:
  - http://edamontology.org/topic_3371
  - http://edamontology.org/topic_0154
  tools:
  - pyMolNetEnhancer
  - Python
  - RMolNetEnhancer
  - GNPS
  - MS2LDA
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

# ms2lda-motif-to-network-mapping

## Summary

Map MS2LDA-derived substructural motifs (Mass2Motifs) onto GNPS mass spectral molecular networks using pyMolNetEnhancer or RMolNetEnhancer. This skill integrates LDA-inferred molecular fragments into network visualizations, enabling annotation of nodes and edges with chemical substructure information.

## When to use

When you have a GNPS molecular network (classical or feature-based) and corresponding MS2LDA experiment results, and you want to annotate network nodes with discovered substructural motifs to support structural elucidation and chemical family interpretation. Use this skill specifically when MS2LDA probability and overlap scores are available as filters.

## When NOT to use

- When MS2LDA experiment has not been run on the corresponding mass spectral data, or LDA results are unavailable.
- When the input network lacks proper node identifiers (CLUSTERID) or is in an unsupported format incompatible with pyMolNetEnhancer/RMolNetEnhancer.
- When you seek only chemical class annotations rather than substructural motif information—use the dedicated chemical class mapping workflow instead.

## Inputs

- GNPS molecular network file (GraphML or JSON format)
- MS2LDA experiment results or exported summary table with motif-document relations
- GNPS job ID
- MS2LDA job ID

## Outputs

- Annotated molecular network in GraphML format with embedded MS2LDA substructural metadata
- Mass2Motifs_Edges_Classical.tsv or equivalent feature-based edge table (CLUSTERID1, interact, CLUSTERID2 columns)
- Mass2Motifs_Nodes_Classical.tsv or equivalent feature-based node table with TopSharedMotifs annotation

## How to apply

Obtain your GNPS job ID and MS2LDA job ID (or download the MS2LDA summary table manually if server timeout occurs). Load the GNPS network file (GraphML or JSON format for feature-based, or classical clustered spectra) and MS2LDA motif-document relations into pyMolNetEnhancer or RMolNetEnhancer. Set user-defined filtering thresholds: `prob` (minimum probability score, default 0.01) and `overlap` (minimum overlap score, default 0.3) to control which motifs are retained. Optionally set `top` parameter to display the top N most-shared motifs per molecular family (default 5). Execute the mapping function, which merges motif annotations into the network graph, assigning substructure labels and confidence scores to nodes and edges. Export the annotated network as GraphML with embedded motif metadata for visualization in Cytoscape.

## Related tools

- **pyMolNetEnhancer** (Python module that executes MS2LDA motif-to-network mapping and integration for both classical and feature-based GNPS workflows) — https://github.com/madeleineernst/pyMolNetEnhancer
- **RMolNetEnhancer** (Analogous R package providing equivalent MS2LDA substructural annotation functionality) — https://github.com/madeleineernst/RMolNetEnhancer
- **GNPS** (Global Natural Products Social Molecular Networking platform that generates the input molecular networks (classical and feature-based)) — https://gnps.ucsd.edu/
- **MS2LDA** (LDA-based tool that discovers and quantifies substructural motifs in mass spectra; provides motif-document relations and probability/overlap scores for filtering) — http://ms2lda.org/
- **Cytoscape** (Network visualization software used to import and visualize the GraphML output with motif-colored edges and nodes) — https://cytoscape.org/

## Evaluation signals

- GraphML output file contains valid graph structure with all original nodes and edges plus new motif annotation attributes.
- Each network node (feature or cluster) carries TopSharedMotifs attribute populated with up to `top` motifs, and each motif annotation includes probability and overlap scores above the specified thresholds.
- Edge interactions in the TSV output correctly reference CLUSTERID1 and CLUSTERID2 with non-null 'interact' column values reflecting shared motifs.
- Import of GraphML into Cytoscape successfully renders nodes and edges; discrete mapping of the 'interaction' column to edge stroke color produces distinct visual groupings by motif.
- Probability and overlap filtering thresholds are consistently applied: no motif with prob < threshold or overlap < threshold appears in output, and manual inspection of a sample of retained motifs confirms they meet or exceed the set cutoffs.

## Limitations

- MS2LDA job download may trigger server connection timeout for large files; manual download from ms2lda.org is recommended as an alternative.
- Probability and overlap thresholds should ideally be set in the ms2lda.org web app before exporting the summary table; thresholds set only at mapping time apply post-hoc filtering and may not align with interactive web app inspection.
- The `top` parameter limits the number of displayed motifs per molecular family but does not reduce computational overhead; users must manually manage large motif counts for clarity.
- Feature-based mapping requires an MGF file created within MZmine during the GNPS feature-based molecular networking workflow; classical clustering uses the clustered spectra MGF from GNPS directly.

## Evidence

- [intro] pyMolNetEnhancer integrates chemical class and substructure information within mass spectral molecular networks created through the GNPS platform: "pyMolNetEnhancer is a python module integrating chemical class and substructure information within mass spectral molecular networks"
- [intro] The workflow supports both classical and feature-based mapping approaches for MS2LDA substructural information: "Map MS2LDA substructural information to mass spectral molecular networks (classical) and (feature based)"
- [readme] prob parameter controls minimum probability score for motif inclusion (default 0.01); overlap parameter controls minimum overlap score (default 0.3): "prob: minimal probability score for a Mass2Motif to be included. Default is 0.01. overlap: minimal overlap score for a Mass2Motif to be included. Default is 0.3."
- [readme] top parameter specifies how many most-shared motifs per molecular family should be shown (default 5): "top: This parameter specifies how many most shared motifs per molecular family (network component index) should be shown. Default is 5."
- [readme] GraphML output file can be imported into Cytoscape for edge coloring based on shared motifs and node coloring by TopSharedMotifs: "To visualize results import the .graphml output file into Cytoscape. To color edges based on shared Mass2Motifs in between nodes select 'Stroke Color'"
- [readme] Alternative import method uses separate TSV files with CLUSTERID1, interact, and CLUSTERID2 columns for edges and node metadata: "import the 'Mass2Motifs_Edges_Classical.tsv' output file as network into Cytoscape. Select column 'CLUSTERID1' as Source Node, column 'interact' as Interaction Type and 'CLUSTERID2' as Target Node"
- [readme] MS2LDA server download timeout may occur; manual download from ms2lda.org is recommended as alternative: "Depending on the size of this file, a server connection timeout may occur. Alternatively, you may download the file manually at http://ms2lda.org/"
- [readme] Feature-based workflow requires MGF file from MZmine created during GNPS feature-based molecular networking: "Create an LDA experiment on http://ms2lda.org/ using the MGF file created within MZmine (see GNPS documentation)"
