---
name: molecular-network-attribute-enrichment
description: Use when you have a GNPS mass spectral molecular network (in .graphml
  or Cytoscape format) and wish to annotate its nodes and edges with chemical class
  assignments from the GNPS library and/or MS2LDA motif probabilities from an independent
  LDA experiment.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3925
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  tools:
  - pyMolNetEnhancer
  - Python
  - RMolNetEnhancer
  - GNPS
  - ms2lda.org
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-network-attribute-enrichment

## Summary

Integrate chemical class and MS2LDA substructural motif information onto nodes and edges of a GNPS mass spectral molecular network, enabling functional and structural annotation of molecular families. This enriches network topology with chemical semantics that reveal shared structural motifs and taxonomic patterns across related compounds.

## When to use

You have a GNPS mass spectral molecular network (in .graphml or Cytoscape format) and wish to annotate its nodes and edges with chemical class assignments from the GNPS library and/or MS2LDA motif probabilities from an independent LDA experiment. Apply this skill when you need to overlay chemical structure or substructural motif consensus onto a molecular family network to identify which structural features link co-clustered spectra.

## When NOT to use

- Your molecular network was not created through GNPS (the tool expects GNPS network topology and metadata formats).
- You do not have an independent MS2LDA experiment or chemical class annotations to map; the skill requires external enrichment data.
- Your input is a raw mass spectrometry dataset or feature table rather than an already-constructed molecular network; preprocessing and network construction must precede this skill.

## Inputs

- GNPS molecular network file (.graphml or Cytoscape format)
- GNPS job ID (identifier for the network job)
- MS2LDA job ID and summary table (from ms2lda.org LDA experiment on clustered or MZmine-derived MGF)
- Chemical class metadata (from GNPS public library or user-provided)

## Outputs

- Annotated .graphml network file with chemical class labels on nodes
- Annotated .graphml network file with MS2LDA motif labels on edges and nodes
- Mass2Motifs_Edges_Classical.tsv or Mass2Motifs_Edges_FeatureBased.tsv (edge table with motif interaction annotations)
- Mass2Motifs_Nodes_Classical.tsv or Mass2Motifs_Nodes_FeatureBased.tsv (node table with top shared motifs)

## How to apply

First, create a molecular network through GNPS using either the classical workflow (with clustered MGF spectra) or the feature-based workflow (with MZmine output). In parallel, create an LDA experiment on ms2lda.org using the same MGF input, then retrieve the MS2LDA summary table or export file. Load the GNPS network file (.graphml) into pyMolNetEnhancer or RMolNetEnhancer, specify your GNPS job ID and MS2LDA job ID, and set filtering thresholds: minimum probability score (default 0.01) and minimum overlap score (default 0.3) for motifs to be included. Optionally set the `top` parameter to control how many most-shared motifs per component are displayed (default 5). The tool will map motif labels and chemical class names as node and edge attributes. Export the annotated network in .graphml format and import into Cytoscape, then use Discrete Mapping on the 'interaction' column to color edges by shared motifs, and use Image/Chart on nodes to display top motifs per component.

## Related tools

- **pyMolNetEnhancer** (Python module that loads GNPS molecular networks and maps chemical class and MS2LDA substructural motif information onto nodes and edges) — https://github.com/madeleineernst/pyMolNetEnhancer
- **RMolNetEnhancer** (R package providing equivalent functionality to pyMolNetEnhancer for mapping chemical class and MS2LDA motif information to GNPS molecular networks) — https://github.com/madeleineernst/RMolNetEnhancer
- **GNPS** (Global Natural Products Social Molecular Networking platform; generates the mass spectral molecular networks that are the input substrate for enrichment) — https://gnps.ucsd.edu/
- **ms2lda.org** (MS2LDA web application used to create latent Dirichlet allocation experiments on clustered or feature-based MGF spectra, generating motif probabilities and overlap scores for mapping) — http://ms2lda.org/
- **Cytoscape** (Network visualization and analysis software; imports annotated .graphml output files and enables color mapping and discrete styling of nodes and edges by motif and chemical class attributes) — https://cytoscape.org/

## Evaluation signals

- The output .graphml file contains no null or missing chemical class or motif attributes on nodes that passed the probability and overlap thresholds; inspect the graphml XML to confirm attribute embedding.
- When imported into Cytoscape, edges are colorable by the 'interaction' column derived from shared motifs, and nodes display non-empty 'TopSharedMotifs' charts, indicating successful mapping.
- The .tsv output files (Mass2Motifs_Edges_*.tsv, Mass2Motifs_Nodes_*.tsv) contain expected columns (CLUSTERID1, CLUSTERID2, motif IDs, probability, overlap) and row counts match the thresholded motif–document relations from the ms2lda.org summary.
- Motif and chemical class labels on network nodes and edges match the GNPS library and MS2LDA experiment outputs; spot-check a sample of cluster IDs against source files.
- The number of top motifs per component displayed in the output matches the user-specified `top` parameter (e.g., if top=5, each component shows ≤5 motifs).

## Limitations

- MS2LDA job IDs may trigger server connection timeouts depending on file size; the README recommends manual download from ms2lda.org as a fallback.
- Probability and overlap filtering thresholds set in the ms2lda.org web app apply to the summary table export; thresholds must be coordinated between the web interface and the enrichment tool to avoid unexpected filtering.
- No changelog is available for either pyMolNetEnhancer or RMolNetEnhancer, making it difficult to track updates or breaking changes across versions.
- Chemical class mapping relies on GNPS public library entries; compounds not yet in GNPS or with ambiguous spectral matches may not receive enriched chemical class annotations.

## Evidence

- [intro] pyMolNetEnhancer is a python module integrating chemical class and substructure information within mass spectral molecular networks created through the GNPS platform.: "pyMolNetEnhancer is a python module integrating chemical class and substructure information within mass spectral molecular networks"
- [other] Load a GNPS mass spectral molecular network file (e.g., graphml or cytoscape format). Prepare chemical class metadata or retrieve it from the GNPS public library. Use pyMolNetEnhancer to map chemical class information onto nodes and edges of the molecular network.: "Load a GNPS mass spectral molecular network file (e.g., graphml or cytoscape format). Prepare chemical class metadata or retrieve it from the GNPS public library. Use pyMolNetEnhancer to map chemical"
- [intro] Map MS2LDA substructural information to mass spectral molecular networks (classical) and (feature based). Map chemical class and MS2LDA substructural information to mass spectral molecular networks.: "Map MS2LDA substructural information to mass spectral molecular networks (classical) and (feature based)"
- [readme] Create a molecular network through the Global Natural Products Social Molecular Networking (GNPS) platform. Create an LDA experiment on ms2lda.org using the MGF clustered spectra downloaded from GNPS. Specify your GNPS job ID and your MS2LDA job ID. Set user-defined parameters: prob (minimal probability score, default 0.01), overlap (minimal overlap score, default 0.3), and top (most shared motifs per component, default 5).: "Create a molecular network through the Global Natural Products Social Molecular Networking (GNPS) platform. Create an LDA experiment on ms2lda.org using the MGF clustered spectra downloaded from GNPS"
- [readme] To visualize results import the .graphml output file into Cytoscape. To color edges based on shared Mass2Motifs select 'Stroke Color' in the 'Edge' tab and choose 'interaction' as Column and 'Discrete Mapping' as Mapping Type. To color nodes by the most shared Mass2Motifs select 'Image/Chart' in the 'Node' tab.: "To visualize results import the .graphml output file into Cytoscape. To color edges based on shared Mass2Motifs select 'Stroke Color' in the 'Edge' tab and choose 'interaction' as Column and"
