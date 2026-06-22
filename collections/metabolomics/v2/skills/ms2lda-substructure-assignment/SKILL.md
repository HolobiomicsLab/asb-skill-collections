---
name: ms2lda-substructure-assignment
description: Use when you have a GNPS molecular network (in GML or GraphML format) and a completed MS2LDA experiment on ms2lda.org, and you want to annotate network nodes with detected substructural motifs to identify shared fragmentation patterns and structural classes across molecular families.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - pyMolNetEnhancer
  - Python
  - MS2LDA
  - RMolNetEnhancer
  - GNPS
  - Cytoscape
derived_from:
- doi: 10.3390/metabo9070144
  title: molnetenhancer
evidence_spans:
- pyMolNetEnhancer is a python module integrating chemical class and substructure information
- pyMolNetEnhancer is a python module
- Map MS2LDA substructural information to mass spectral molecular networks
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

# ms2lda-substructure-assignment

## Summary

Assign substructural motifs (Mass2Motifs) from MS2LDA experiments to mass spectral molecular network nodes, enabling annotation of fragmentation patterns and structural features across networked spectra. This skill integrates probabilistic latent Dirichlet allocation results into GNPS network visualization and analysis.

## When to use

You have a GNPS molecular network (in GML or GraphML format) and a completed MS2LDA experiment on ms2lda.org, and you want to annotate network nodes with detected substructural motifs to identify shared fragmentation patterns and structural classes across molecular families.

## When NOT to use

- MS2LDA results are not available or experiment failed to complete on ms2lda.org.
- Your GNPS network was not generated through the standard GNPS platform workflow or is in an unsupported format.
- You only need chemical class annotations without substructural motif information; use chemical class mapping separately.

## Inputs

- GNPS molecular network file (GML or GraphML format)
- MS2LDA experiment summary table (TSV or exported from ms2lda.org)
- GNPS job ID (string)
- MS2LDA job ID (string)
- MS2LDA clustered MGF file (for classical workflow) or MZmine-generated MGF file (for feature-based workflow)

## Outputs

- Annotated molecular network file (GraphML format with Mass2Motif node/edge attributes)
- Mass2Motifs_Nodes_Classical.tsv or Mass2Motifs_Nodes_FeatureBased.tsv (node attribute table)
- Mass2Motifs_Edges_Classical.tsv or Mass2Motifs_Edges_FeatureBased.tsv (edge attribute table)
- Cytoscape-compatible network visualization with motif annotations

## How to apply

Retrieve your GNPS job ID and MS2LDA job ID (or manually download the MS2LDA summary export). Load the GNPS network file and MS2LDA results into pyMolNetEnhancer or RMolNetEnhancer. Apply user-defined probability and overlap thresholds (default prob=0.01, overlap=0.3) to filter Mass2Motif-document associations. Map motifs to network nodes using either classical (consensus spectrum) or feature-based (MZmine-derived feature) workflow approaches. Specify the 'top' parameter to control how many shared motifs per molecular family are retained (default=5). Export the annotated network in GraphML format and node/edge attribute tables (TSV) for visualization in Cytoscape.

## Related tools

- **pyMolNetEnhancer** (Python module that loads GNPS networks and MS2LDA results, maps motifs to nodes via classical or feature-based approaches, and exports annotated networks and attribute tables) — https://github.com/madeleineernst/pyMolNetEnhancer
- **RMolNetEnhancer** (Analogous R package providing identical MS2LDA substructure mapping functionality for users preferring R workflows) — https://github.com/madeleineernst/RMolNetEnhancer
- **GNPS** (Global Natural Products Social platform that generates consensus molecular networks from mass spectral data; provides the input network and clustered MGF spectra for MS2LDA) — https://gnps.ucsd.edu/
- **MS2LDA** (Web application that performs latent Dirichlet allocation on fragmentation spectra to discover and assign substructural motifs (Mass2Motifs) to individual spectra) — http://ms2lda.org/
- **Cytoscape** (Network visualization and analysis software used to import and display the GraphML output files with motif-colored edges and nodes) — https://cytoscape.org/

## Evaluation signals

- Verify that all network nodes in the output GraphML file have TopSharedMotifs attributes populated (non-null, comma-separated motif names and probabilities).
- Check that edge tables contain 'interact' columns with Mass2Motif identifiers and that edge counts match expected shared motif relationships at the applied probability and overlap thresholds.
- Confirm that nodes with high motif sharing show clustered coloring in Cytoscape when mapped using 'Discrete Mapping' on the TopSharedMotifs attribute.
- Validate that the number of retained motif-node associations is reasonable relative to the applied thresholds (lower prob/overlap → more associations); compare output row counts to raw MS2LDA summary statistics.
- Ensure that GraphML file can be imported into Cytoscape without parsing errors and that node/edge attributes are readable as discrete or continuous properties.

## Limitations

- Server connection timeouts can occur when retrieving large MS2LDA result files via API; manual download from ms2lda.org is recommended as a fallback.
- Motif-node associations are filtered based on probability and overlap thresholds set in the web app; inconsistent threshold application between the web interface and local script may produce incomplete or mismatched results.
- MS2LDA motif assignments depend on the quality and size of the input spectra dataset; small or low-quality spectral libraries may yield unreliable or sparse motif associations.
- The 'top' parameter limits display to the N most-shared motifs per molecular family, potentially obscuring lower-abundance but biologically relevant motifs.

## Evidence

- [other] Load the GNPS molecular network and MS2LDA results; map motifs to nodes using classical or feature-based approaches; export annotated network.: "Map MS2LDA substructural information to mass spectral molecular networks (classical) ... Map MS2LDA substructural information to mass spectral molecular networks (feature based)"
- [readme] Thresholds for filtering MS2LDA motif assignments.: "prob: minimal probability score for a Mass2Motif to be included. Default is 0.01. overlap: minimal overlap score for a Mass2Motif to be included. Default is 0.3."
- [readme] Output artifact types from the workflow.: "Alternatively the edges and nodes output files can also be loaded separately into Cytoscape. To this end import the 'Mass2Motifs_Edges_Classical.tsv' output file as network into Cytoscape. Select"
- [readme] Input requirements for MS2LDA integration.: "Create a molecular network through the Global Natural Products Social Molecular Networking (GNPS) platform ... Create an LDA experiment on http://ms2lda.org/ using the MGF clustered spectra"
- [other] Tool capability and scope.: "pyMolNetEnhancer is a python module integrating chemical class and substructure information within mass spectral molecular networks created through the Global Natural Products Social Molecular"
