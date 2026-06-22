---
name: feature-node-identifier-matching
description: Use when you have created a feature-based GNPS molecular network and a corresponding MS2LDA experiment, and you need to propagate substructural motif annotations from the MS2LDA output back to the network nodes by matching feature IDs.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2409
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0749
  tools:
  - pyMolNetEnhancer
  - Python
  - RMolNetEnhancer
  - GNPS
  - MS2LDA
  - Cytoscape
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
  - build: coll_molnetenhancer_cq
    doi: 10.3390/metabo9070144
    title: molnetenhancer
  dedup_kept_from: coll_molnetenhancer_cq
schema_version: 0.2.0
---

# feature-node-identifier-matching

## Summary

Match MS2LDA Mass2Motif substructural information to feature-based GNPS molecular network nodes by aligning feature identifiers across the two datasets. This skill bridges spectral feature annotations from MS2LDA into network visualization and analysis.

## When to use

You have created a feature-based GNPS molecular network and a corresponding MS2LDA experiment, and you need to propagate substructural motif annotations from the MS2LDA output back to the network nodes by matching feature IDs. Use this when working with feature-based (rather than classical/clustered) network workflows where features are preserved as discrete nodes.

## When NOT to use

- Input network was generated via the classical (not feature-based) GNPS workflow; use the classical mapping pathway instead.
- MS2LDA motif assignments have not yet been computed or exported from http://ms2lda.org/.
- Feature identifiers are not consistent or traceable between the GNPS network and MS2LDA output (data integrity mismatch).

## Inputs

- Feature-based GNPS molecular network file (GraphML or edge/node table format)
- MS2LDA Mass2Motif summary output table with feature identifiers and motif assignments
- User-defined parameters: probability threshold, overlap threshold, top-N motifs per family

## Outputs

- Annotated network file (GraphML) with MS2LDA substructure labels attached to nodes
- Annotated edges table (TSV) with motif interaction information
- Annotated nodes table (TSV) with node IDs and attached Mass2Motif labels

## How to apply

Load both the feature-based GNPS molecular network file (in classical network format) and the MS2LDA Mass2Motif summary output table containing feature-to-motif assignments. Execute the feature-based mapping function in pyMolNetEnhancer or RMolNetEnhancer that performs inner join or lookup matching on the feature identifier column present in both datasets. Apply user-defined thresholds for minimal probability score (default 0.01) and overlap score (default 0.3) to filter weak motif-feature associations before merging. The result is an annotated network table where each node (feature) carries attached MS2LDA substructure labels, enabling subsequent visualization in Cytoscape or edge/node table export for downstream analysis.

## Related tools

- **pyMolNetEnhancer** (Python module that executes feature-based identifier matching and merges MS2LDA motif annotations onto GNPS network nodes) — https://github.com/madeleineernst/pyMolNetEnhancer
- **RMolNetEnhancer** (Analogous R package providing identical feature-based motif-to-node matching and annotation workflow) — https://github.com/madeleineernst/RMolNetEnhancer
- **GNPS** (Source platform for feature-based molecular network generation; provides network files and feature definitions) — https://gnps.ucsd.edu/
- **MS2LDA** (Upstream annotation tool that assigns Mass2Motif substructures to features; outputs summary table used for matching) — http://ms2lda.org/
- **Cytoscape** (Visualization and interpretation tool; loads annotated GraphML output to display shared motifs across network edges and nodes) — https://cytoscape.org/

## Evaluation signals

- Feature identifiers in the output network match those present in both the GNPS and MS2LDA input files; verify no unmatched or orphaned nodes.
- MS2LDA motif labels are present in node and edge attribute tables; spot-check that motif probabilities and overlap scores in the merged table respect the user-specified thresholds.
- When imported into Cytoscape, edges can be colored by interaction type (shared motif) and nodes can be colored by TopSharedMotifs, confirming annotation propagation.
- Output TSV files (Edges, Nodes) are properly formatted and contain all expected columns (CLUSTERID1, CLUSTERID2, interact, Mass2Motif labels); row counts match expected network size.
- No data loss on merge: total number of annotated nodes equals or exceeds the count of nodes in the original GNPS network (any divergence indicates failed matching).

## Limitations

- Server connection timeouts may occur when downloading large MS2LDA summary files; manual download from http://ms2lda.org/ is an alternative.
- Probability and overlap thresholds set within the MS2LDA web app filter the summary table upstream; the thresholds applied in pyMolNetEnhancer or RMolNetEnhancer operate on already-filtered data.
- Matching depends on consistent feature identifier formatting between GNPS and MS2LDA; mismatches or ID reformatting will result in unmatched nodes.
- Feature-based workflow compatibility is required; the classical network mapping pathway uses different input formats and matching logic.

## Evidence

- [other] Execute pyMolNetEnhancer's feature-based mapping function to overlay MS2LDA substructural information onto network nodes, matching nodes by feature identifiers.: "Execute pyMolNetEnhancer's feature-based mapping function to overlay MS2LDA substructural information onto network nodes, matching nodes by feature identifiers."
- [other] Load the feature-based GNPS molecular network file (in classical network format) and MS2LDA Mass2Motif output containing substructure assignments.: "Load the feature-based GNPS molecular network file (in classical network format) and MS2LDA Mass2Motif output containing substructure assignments."
- [readme] prob: minimal probability score for a Mass2Motif to be included. Default is 0.01. overlap: minimal overlap score for a Mass2Motif to be included. Default is 0.3.: "prob: minimal probability score for a Mass2Motif to be included. Default is 0.01. overlap: minimal overlap score for a Mass2Motif to be included. Default is 0.3."
- [other] Output the annotated network table with node identifiers, edges, and attached MS2LDA substructure labels and chemical class information.: "Output the annotated network table with node identifiers, edges, and attached MS2LDA substructure labels and chemical class information."
- [readme] Create a feature based molecular network through the Global Natural Products Social Molecular Networking (GNPS) platform. Create an LDA experiment on http://ms2lda.org/ using the MGF file created within MZmine.: "Create a feature based molecular network through the GNPS platform. Create an LDA experiment on http://ms2lda.org/ using the MGF file created within MZmine."
