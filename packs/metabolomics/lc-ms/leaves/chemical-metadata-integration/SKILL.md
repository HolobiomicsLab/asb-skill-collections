---
name: chemical-metadata-integration
description: Use when when you have a GNPS molecular network (graphml or cytoscape format) and wish to annotate it with chemical class labels or MS2LDA-derived mass2motifs to highlight shared structural features or chemical families across spectral clusters.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chemical-metadata-integration

## Summary

Integrate chemical class and MS2LDA substructural motif metadata onto nodes and edges of a GNPS mass spectral molecular network. This skill enriches network visualizations with semantic chemical information, enabling pattern recognition and biological interpretation across networked spectra.

## When to use

When you have a GNPS molecular network (graphml or cytoscape format) and wish to annotate it with chemical class labels or MS2LDA-derived mass2motifs to highlight shared structural features or chemical families across spectral clusters. Use this skill if your research question requires mapping molecular annotations back onto network topology for exploratory or publication visualization.

## When NOT to use

- Input network is not a GNPS-derived molecular network (e.g., a generic graph with no cluster IDs or spectral provenance).
- Chemical class or motif metadata does not align with the network's cluster identifiers (no common join key).
- Your goal is to filter or prune the network based on chemical criteria; use feature selection or network reduction instead.

## Inputs

- GNPS molecular network file (graphml or cytoscape format)
- GNPS job ID (for metadata retrieval)
- MS2LDA job ID and summary table (if mapping mass2motifs)
- Chemical class metadata (optional; can be retrieved from GNPS public library)
- User-defined threshold parameters (prob, overlap, top N)

## Outputs

- Annotated network graphml file with chemical class labels embedded in node/edge attributes
- Mass2Motifs_Edges_Classical.tsv or _FeatureBased.tsv (edge list with interaction/motif annotations)
- Mass2Motifs_Nodes_Classical.tsv or _FeatureBased.tsv (node table with TopSharedMotifs attribute)
- Cytoscape-compatible visualization with colored edges (by shared motifs) and nodes (by chemical family)

## How to apply

Load a GNPS-generated network file (graphml or edge/node TSV) and either retrieve chemical class metadata from the GNPS public library or export a mass2motifs summary from ms2lda.org. Specify filtering thresholds (e.g., prob ≥ 0.01, overlap ≥ 0.3 for motifs; top N shared motifs per network component) to control annotation density. Use pyMolNetEnhancer (Python) or RMolNetEnhancer (R) to programmatically map the metadata onto network nodes and edges by matching cluster IDs or feature identifiers. Export the annotated network in graphml format and import into Cytoscape, using 'Discrete Mapping' to color edges by 'interaction' attribute (shared motifs) and nodes by 'TopSharedMotifs' (network component–level summaries). Validate that all target clusters received annotations and that the threshold parameters filtered the metadata as intended.

## Related tools

- **pyMolNetEnhancer** (Python module that integrates chemical class and substructure information by mapping metadata onto GNPS network nodes and edges; used to automate annotation and export graphml files.) — https://github.com/madeleineernst/pyMolNetEnhancer
- **RMolNetEnhancer** (Analogous R package providing equivalent functionality for mapping chemical class and MS2LDA metadata onto molecular networks.) — https://github.com/madeleineernst/RMolNetEnhancer
- **GNPS** (Platform that generates the initial mass spectral molecular networks and provides public chemical class library; source of cluster IDs and network topology.) — https://gnps.ucsd.edu/
- **MS2LDA** (Platform for running Latent Dirichlet Allocation experiments on MGF spectra to generate mass2motifs (substructural motifs); exports summary tables used for network annotation.) — http://ms2lda.org/
- **Cytoscape** (Desktop application for interactive visualization and styling of annotated network graphml files; enables discrete mapping of node/edge attributes to visual properties.) — https://cytoscape.org/

## Examples

```
From Python with pyMolNetEnhancer: import pyMolNetEnhancer; net = pyMolNetEnhancer.load_network('gnps_network.graphml'); annotated = net.map_chemical_classes(metadata='gnps_library.tsv'); annotated.export_graphml('annotated_network.graphml'). Or from R with RMolNetEnhancer: devtools::load_all('RMolNetEnhancer'); source('Example_notebooks/Mass2Motifs_2_Network_Classical.ipynb') with GNPS_job_ID and MS2LDA_job_ID specified.
```

## Evaluation signals

- All target cluster IDs in the network received chemical class or motif annotations; verify by checking node/edge attribute tables in Cytoscape.
- Threshold parameters (prob, overlap) were applied consistently; confirm by comparing the counts of annotations before and after filtering, and inspect the summary statistics in output TSV files.
- Network visualization renders without missing or malformed attributes; import graphml into Cytoscape and verify that 'Discrete Mapping' for edges and 'Image/Chart' for nodes populate without errors.
- Nodes within the same network component (molecular family) display the same or overlapping TopSharedMotifs; inspect via Cytoscape node inspection tool or by querying the output node table.
- Output file format is valid graphml (parseable by standard tools) and TSV files are tab-delimited with expected column names (CLUSTERID1, interact, CLUSTERID2, TopSharedMotifs).

## Limitations

- Server connection timeouts can occur when downloading MS2LDA summary files; the README recommends manual download as a fallback.
- Filtering thresholds (prob, overlap) are set both in the ms2lda.org web interface and in the integration code; mismatches may cause confusion; always apply thresholds consistently at the source.
- No changelog is documented for either pyMolNetEnhancer or RMolNetEnhancer, making it difficult to track breaking changes or feature updates.
- The skill requires valid cluster ID alignment between GNPS network and chemical/motif metadata; if naming conventions differ, manual mapping or identifier standardization may be necessary.
- Visualization quality and interpretability depend on network size and density; very large networks may be difficult to render or interpret in Cytoscape without additional filtering or layout optimization.

## Evidence

- [readme] pyMolNetEnhancer is a python module integrating chemical class and substructure information within mass spectral molecular networks created through the Global Natural Products Social Molecular Networking (GNPS) platform.: "pyMolNetEnhancer is a python module integrating chemical class and substructure information within mass spectral molecular networks created through the Global Natural Products Social Molecular"
- [readme] To map substructural information to a mass spectral molecular network you need to create a molecular network through GNPS and create an LDA experiment on ms2lda.org using the MGF clustered spectra downloaded from GNPS.: "Create a molecular network through the Global Natural Products Social Molecular Networking (GNPS) platform. Create an LDA experiment on http://ms2lda.org/ using the MGF clustered spectra downloaded"
- [readme] User-defined parameters for mapping the Mass2Motifs onto the network include prob (minimal probability score, default 0.01), overlap (minimal overlap score, default 0.3), and top (number of most shared motifs per molecular family, default 5).: "prob: minimal probability score for a Mass2Motif to be included. Default is 0.01. overlap: minimal overlap score for a Mass2Motif to be included. Default is 0.3. top: This parameter specifies how"
- [readme] To visualize results import the .graphml output file into Cytoscape. To color edges based on shared Mass2Motifs select 'Stroke Color' in the 'Edge' tab and choose 'interaction' as Column and 'Discrete Mapping' as Mapping Type.: "import the .graphml output file into Cytoscape. To color edges based on shared Mass2Motifs in between nodes select 'Stroke Color' in the 'Edge' tab to the left and choose 'interaction' as Column and"
- [readme] Alternatively the edges and nodes output files can also be loaded separately into Cytoscape. Import the 'Mass2Motifs_Edges_Classical.tsv' output file as network selecting column 'CLUSTERID1' as Source Node, 'interact' as Interaction Type and 'CLUSTERID2' as Target Node.: "import the 'Mass2Motifs_Edges_Classical.tsv' output file as network into Cytoscape. Select column 'CLUSTERID1' as Source Node, column 'interact' as Interaction Type and 'CLUSTERID2' as Target Node"
- [intro] pyMolNetEnhancer performs mapping of chemical class information to mass spectral molecular networks, as well as mapping of MS2LDA substructural information via both classical and feature-based approaches.: "Map chemical class information to mass spectral molecular networks. Map MS2LDA substructural information to mass spectral molecular networks (classical) and (feature based)"
