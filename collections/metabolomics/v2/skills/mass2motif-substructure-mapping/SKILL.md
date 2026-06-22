---
name: mass2motif-substructure-mapping
description: Use when you have created a GNPS molecular network (classical or feature-based workflow) and run an MS2LDA experiment on the corresponding MGF spectra, and you want to annotate network nodes with shared Mass2Motifs and chemical class information to interpret the structural basis of network.
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

# mass2motif-substructure-mapping

## Summary

Map MS2LDA-derived Mass2Motif substructural annotations onto GNPS molecular networks (either classical or feature-based) to enrich network nodes and edges with substructural and chemical class information. This skill integrates fragmentation pattern motifs with network topology to enable motif-based interpretation of mass spectral molecular families.

## When to use

You have created a GNPS molecular network (classical or feature-based workflow) and run an MS2LDA experiment on the corresponding MGF spectra, and you want to annotate network nodes with shared Mass2Motifs and chemical class information to interpret the structural basis of network clustering and edge connectivity.

## When NOT to use

- MS2LDA experiment has not been run on your clustered MGF spectra; no Mass2Motif assignments exist.
- Your molecular network was created using non-standard preprocessing or lacks proper cluster IDs linking to MS2LDA documents.
- You only have fragment ion intensities without LDA-derived motif models; classical spectral similarity alone is insufficient.

## Inputs

- GNPS molecular network edge table (from classical or feature-based networking)
- MS2LDA job ID or manually downloaded MS2LDA summary table (TSV or CSV)
- GNPS job ID

## Outputs

- Mass2Motifs_Edges_Classical.tsv or Mass2Motifs_Edges_FeatureBased.tsv (edge table with motif annotations)
- Mass2Motifs_Nodes_Classical.tsv or Mass2Motifs_Nodes_FeatureBased.tsv (node table with top shared motifs per molecular family)
- .graphml network file for Cytoscape visualization (optional)

## How to apply

Load your GNPS job ID and MS2LDA job ID (or manually download the MS2LDA summary table from http://ms2lda.org/ to avoid server timeouts on large files). Use pyMolNetEnhancer (Python) or RMolNetEnhancer (R) to parse the network edge table and motif assignments. Set probability and overlap thresholds (default prob=0.01, overlap=0.3) to filter low-confidence motif-document relations; these thresholds can also be applied in the MS2LDA web app's Experimental Options tab. Specify the 'top' parameter to define how many most-shared motifs per molecular family (network component) to retain (default 5). The module outputs TSV edge and node tables with motif annotations and optionally a .graphml file for visualization in Cytoscape, where edges can be colored by shared motif identity and nodes by their top-ranked motifs.

## Related tools

- **pyMolNetEnhancer** (Python module that parses GNPS and MS2LDA outputs, maps motifs to network nodes, and generates annotated edge/node tables and .graphml files) — https://github.com/madeleineernst/pyMolNetEnhancer
- **RMolNetEnhancer** (R package providing analogous functionality to pyMolNetEnhancer for motif and chemical class mapping onto GNPS networks) — https://github.com/madeleineernst/RMolNetEnhancer
- **GNPS** (Platform for creating classical and feature-based molecular networks from MS/MS data; generates edge tables and cluster identifiers used as input to motif mapping) — https://gnps.ucsd.edu/
- **MS2LDA** (Latent Dirichlet allocation service that discovers Mass2Motifs from clustered spectra; produces motif-document probability and overlap scores used for annotation) — http://ms2lda.org/
- **Cytoscape** (Network visualization and analysis platform used to import .graphml output and color nodes/edges by motif identity and molecular family clustering) — https://cytoscape.org/

## Examples

```
pip install pyMolNetEnhancer; python Example_notebooks/Mass2Motifs_2_Network_Classical.ipynb (then specify GNPS_JOB_ID, MS2LDA_JOB_ID, prob=0.01, overlap=0.3, top=5)
```

## Evaluation signals

- Output TSV files contain expected columns: CLUSTERID1, CLUSTERID2, 'interact' (edge table); TopSharedMotifs, molecular family index (node table).
- Number of retained motif-document relations matches the applied probability and overlap thresholds; spot-check a few motif assignments in MS2LDA web interface to confirm filtering.
- Edges in the .graphml output file are labeled with interaction type based on shared Mass2Motifs; edges with no shared motifs should be absent or marked distinctly.
- When imported into Cytoscape, discrete edge coloring by 'interaction' attribute produces distinct colors for different shared motifs; nodes colored by TopSharedMotifs show expected within-family consistency.
- Top parameter (default 5) correctly limits the number of motifs shown per molecular family; verify by inspecting the TopSharedMotifs field in output node table.

## Limitations

- Server connection timeouts may occur when fetching large MS2LDA summary files; manual download from http://ms2lda.org/ under the Export button is recommended as a fallback.
- Motif-document probability and overlap thresholds must be set carefully; thresholds applied in MS2LDA web app are reflected in the downloaded summary table, so coordinate filtering between platforms to avoid double-filtering or missing annotations.
- The 'top' parameter (number of most-shared motifs per molecular family) is independent of family size; small families may report fewer than 'top' motifs if fewer exist above threshold.
- Mapping relies on exact matching of cluster IDs between GNPS and MS2LDA; if preprocessing steps differ between platforms or cluster IDs are remapped, motif-to-node assignment may fail or be incomplete.

## Evidence

- [other] pyMolNetEnhancer is a python module integrating chemical class and substructure information within mass spectral molecular networks created through the GNPS platform, enabling mapping of MS2LDA substructural information to networks via classical approaches.: "pyMolNetEnhancer is a python module integrating chemical class and substructure information within mass spectral molecular networks"
- [other] The module maps MS2LDA substructural information to network nodes using the classical molecular networking approach.: "Map MS2LDA substructural information to mass spectral molecular networks (classical)"
- [readme] prob: minimal probability score for a Mass2Motif to be included. Default is 0.01. overlap: minimal overlap score for a Mass2Motif to be included. Default is 0.3.: "prob: minimal probability score for a Mass2Motif to be included. Default is 0.01. overlap: minimal overlap score for a Mass2Motif to be included. Default is 0.3."
- [readme] top: This parameter specifies how many most shared motifs per molecular family (network component index) should be shown. Default is 5.: "top: This parameter specifies how many most shared motifs per molecular family (network component index) should be shown. Default is 5."
- [readme] To visualize results import the .graphml output file into Cytoscape. To color edges based on shared Mass2Motifs in between nodes select 'Stroke Color' in the 'Edge' tab to the left and choose 'interaction' as Column and 'Discrete Mapping' as Mapping Type.: "To visualize results import the .graphml output file into Cytoscape. To color edges based on shared Mass2Motifs in between nodes select 'Stroke Color' in the 'Edge' tab"
- [readme] Depending on the size of this file, a server connection timeout may occur. Alternatively, you may download the file manually at http://ms2lda.org/: "Depending on the size of this file, a server connection timeout may occur. Alternatively, you may download the file manually at http://ms2lda.org/"
- [readme] In order to map substructural information to a mass spectral molecular network you need to: Create a molecular network through the Global Natural Products Social Molecular Networking (GNPS) platform; Create an LDA experiment on http://ms2lda.org/ using the MGF clustered spectra downloaded from GNPS.: "Create a molecular network through the Global Natural Products Social Molecular Networking (GNPS) platform; Create an LDA experiment on http://ms2lda.org/"
