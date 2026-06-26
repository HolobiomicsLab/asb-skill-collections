---
name: gnps-network-file-handling
description: Use when you have a GNPS molecular network job and need to programmatically
  load the network structure, merge external annotations (chemical class, MS2LDA substructural
  motifs), and export a unified annotated network for visualization in Cytoscape or
  other graph analysis tools.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0335
  edam_topics:
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3520
  tools:
  - pyMolNetEnhancer
  - Python
  - GNPS
  - RMolNetEnhancer
  - MS2LDA
  - Cytoscape
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.3390/metabo9070144
  title: molnetenhancer
evidence_spans:
- pyMolNetEnhancer is a python module integrating chemical class and substructure
  information
- pyMolNetEnhancer is a python module
- Global Natural Products Social Molecular Networking (GNPS)
- mass spectral molecular networks created through the Global Natural Products Social
  Molecular Networking (GNPS) platform
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

# GNPS network file handling

## Summary

Load, parse, and export mass spectral molecular networks in standard graph formats (GML, GraphML) produced by the GNPS platform, integrating node and edge annotations for downstream visualization and analysis. This skill enables interoperability between GNPS network generation, annotation enrichment tools, and network visualization software.

## When to use

You have a GNPS molecular network job and need to programmatically load the network structure, merge external annotations (chemical class, MS2LDA substructural motifs), and export a unified annotated network for visualization in Cytoscape or other graph analysis tools. Use this skill when working with GML or GraphML network files output from GNPS quickstart or feature-based molecular networking workflows.

## When NOT to use

- Input network is already in a non-standard or proprietary format incompatible with GML/GraphML parsers.
- You only need to visualize raw GNPS networks without additional annotations; direct Cytoscape import of GNPS outputs may be faster.
- Network is too large (>10,000 nodes) for in-memory annotation merging; consider streaming or chunked approaches instead.

## Inputs

- GNPS molecular network file (GML or GraphML format)
- MS2LDA substructural feature summary table (optional; typically exported from http://ms2lda.org/)
- Chemical class annotation file or lookup table (optional)
- GNPS job ID (to retrieve network metadata programmatically)

## Outputs

- Annotated molecular network (GraphML or GML format)
- Node attribute table (TSV or CSV with node IDs and annotations)
- Edge attribute table (TSV or CSV with source, target, interaction type, and shared motif labels)

## How to apply

Load the GNPS molecular network file (GML or GraphML format) into your chosen environment (pyMolNetEnhancer for Python or RMolNetEnhancer for R). Parse the network structure to access nodes and edges. Merge external annotations (e.g., MS2LDA substructural motifs or chemical class labels) into node and edge attributes using the module's integration functions. Configure filtering parameters (e.g., probability threshold `prob` ≥ 0.01, overlap threshold `overlap` ≥ 0.3 for MS2LDA motifs; `top` parameter to select the N most shared motifs per molecular family). Export the merged network and separate node and edge attribute tables in standard formats (GraphML for network, TSV for tabular attributes). Validate by importing the GraphML into Cytoscape and confirming that node and edge annotations render correctly.

## Related tools

- **pyMolNetEnhancer** (Python module to load GNPS networks, integrate MS2LDA and chemical class annotations, and export merged GraphML and TSV outputs) — https://github.com/madeleineernst/pyMolNetEnhancer
- **RMolNetEnhancer** (R package providing analogous network loading, annotation merging, and export functionality as pyMolNetEnhancer) — https://github.com/madeleineernst/RMolNetEnhancer
- **GNPS** (Global Natural Products Social Molecular Networking platform that generates initial molecular networks in GML/GraphML format) — https://gnps.ucsd.edu/
- **MS2LDA** (Generates substructural motif assignments (Mass2Motifs) that are merged into GNPS network nodes and edges) — http://ms2lda.org/
- **Cytoscape** (Network visualization software used to import, render, and interactively explore annotated GraphML networks) — https://cytoscape.org/

## Examples

```
pip install pyMolNetEnhancer; python -c "from pyMolNetEnhancer import *; net = load_gnps_network('path/to/network.graphml'); net_merged = merge_ms2lda_annotations(net, 'path/to/ms2lda_summary.txt', prob=0.01, overlap=0.3); export_network(net_merged, 'annotated_network.graphml', 'node_attributes.tsv', 'edge_attributes.tsv')"
```

## Evaluation signals

- Network file loads without parsing errors and node/edge counts match GNPS job summary
- All external annotations (chemical class labels, MS2LDA motif IDs, probability/overlap scores) are present in exported node and edge attribute tables
- Exported GraphML file can be successfully imported into Cytoscape with no missing or malformed attributes
- Edge annotations correctly reflect shared motifs; node annotations display filtered motifs ranked by frequency per molecular family (network component)
- TSV output tables contain all expected columns (CLUSTERID1, CLUSTERID2, interact for edges; node ID and Top/Shared motifs for nodes) with no null or duplicate entries

## Limitations

- MS2LDA server connection may timeout for large files; manual download from ms2lda.org/ is recommended as a fallback.
- Probability and overlap thresholds set in the ms2lda.org web interface should be applied consistently when exporting summaries, as the summary table reflects filtered relations set in the web app—discrepancies between web and code-level thresholds may produce inconsistent annotations.
- No changelog currently documented; version compatibility between pyMolNetEnhancer/RMolNetEnhancer and GNPS/MS2LDA output formats is not formally versioned.

## Evidence

- [other] Load the GNPS molecular network (GML or GraphML format) and MS2LDA substructural feature assignments into pyMolNetEnhancer.: "Load the GNPS molecular network (GML or GraphML format) and MS2LDA substructural feature assignments into pyMolNetEnhancer."
- [other] Map chemical class information to network nodes using the module's chemical class integration functions. Map MS2LDA substructural information to network nodes via both classical and feature-based approaches within pyMolNetEnhancer. Merge chemical class and MS2LDA annotations into unified node attributes.: "Map chemical class information to network nodes using the module's chemical class integration functions. Map MS2LDA substructural information to network nodes via both classical and feature-based"
- [other] Export the class-annotated network and node attribute table in standard formats (GML/GraphML and CSV).: "Export the class-annotated network and node attribute table in standard formats (GML/GraphML and CSV)."
- [readme] prob: minimal probability score for a Mass2Motif to be included. Default is 0.01. overlap: minimal overlap score for a Mass2Motif to be included. Default is 0.3.: "prob: minimal probability score for a Mass2Motif to be included. Default is 0.01. overlap: minimal overlap score for a Mass2Motif to be included. Default is 0.3."
- [readme] Depending on the size of this file, a server connection timeout may occur. Alternatively, you may download the file manually at http://ms2lda.org/: "Depending on the size of this file, a server connection timeout may occur. Alternatively, you may download the file manually at http://ms2lda.org/"
- [readme] The probability and overlap thresholds can be set within the ms2lda.org app as well under the Experimental Options tab. It is recommendable to do so when inspecting results in the web app. Importantly, the summary table contains filtered motif-document relations using the set thresholds in the web app.: "The probability and overlap thresholds can be set within the ms2lda.org app as well under the Experimental Options tab. It is recommendable to do so when inspecting results in the web app."
- [readme] To this end import the 'Mass2Motifs_Edges_Classical.tsv' output file as network into Cytoscape. Select column 'CLUSTERID1' as Source Node, column 'interact' as Interaction Type and 'CLUSTERID2' as Target Node: "To this end import the 'Mass2Motifs_Edges_Classical.tsv' output file as network into Cytoscape. Select column 'CLUSTERID1' as Source Node, column 'interact' as Interaction Type and 'CLUSTERID2' as"
