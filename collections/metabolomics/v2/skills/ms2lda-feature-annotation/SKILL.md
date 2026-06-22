---
name: ms2lda-feature-annotation
description: Use when after creating a GNPS mass spectral molecular network and running an MS2LDA experiment, use this skill when you want to identify and visualize which substructural motifs (Mass2Motifs) are shared across clustered spectra, particularly to highlight fragmentation pattern similarities between.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - pyMolNetEnhancer
  - Python
  - RMolNetEnhancer
  - GNPS (Global Natural Products Social Molecular Networking)
  - MS2LDA (Mass2Motifs Latent Dirichlet Allocation)
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
  - build: coll_molnetenhancer
    doi: 10.3390/metabo9070144
    title: molnetenhancer
  dedup_kept_from: coll_molnetenhancer
schema_version: 0.2.0
---

# ms2lda-feature-annotation

## Summary

Annotate mass spectral molecular network nodes with MS2LDA-derived substructural motifs (Mass2Motifs) to reveal recurrent fragmentation patterns and enable motif-based edge coloring and node labeling. This skill maps probabilistic substructure information onto GNPS network components using either classical or feature-based LDA approaches.

## When to use

After creating a GNPS mass spectral molecular network and running an MS2LDA experiment, use this skill when you want to identify and visualize which substructural motifs (Mass2Motifs) are shared across clustered spectra, particularly to highlight fragmentation pattern similarities between network nodes and to color network edges by shared motif composition.

## When NOT to use

- Input GNPS network is from a classical (non-feature-based) workflow and you have only feature-based MS2LDA results (or vice versa; ensure workflow alignment).
- MS2LDA job has not completed or summary data is unavailable and no manual download is possible.
- Your goal is to annotate the network with chemical class information only (use the chemical class mapping skill instead or in parallel).

## Inputs

- GNPS mass spectral molecular network (specified by GNPS job ID)
- MS2LDA experiment results (specified by MS2LDA job ID or downloaded summary file)
- Clustered MGF file (exported from GNPS, used to generate MS2LDA experiment)

## Outputs

- Annotated network graph (.graphml format for Cytoscape visualization)
- Mass2Motifs_Nodes_Classical.tsv or Mass2Motifs_Nodes_FeatureBased.tsv (node attributes including top shared motifs)
- Mass2Motifs_Edges_Classical.tsv or Mass2Motifs_Edges_FeatureBased.tsv (edge attributes with shared motif annotations)
- Network visualization with edges colored by shared Mass2Motif interactions and nodes labeled by top motifs per family

## How to apply

First, export the clustered MGF file from GNPS and use it to create an LDA experiment at http://ms2lda.org/. Download the MS2LDA summary results (or retrieve via API using the MS2LDA job ID). Then, load both the GNPS network (identified by GNPS job ID) and MS2LDA summary data into pyMolNetEnhancer or RMolNetEnhancer. Set user-defined filtering thresholds: `prob` (minimum probability score for a Mass2Motif, default 0.01) and `overlap` (minimum overlap score, default 0.3) to control motif inclusion stringency. Specify the `top` parameter to limit the number of most-shared motifs per molecular family/network component to display (default 5). The tool will map each Mass2Motif probabilistically to network nodes based on feature-motif associations, then merge both layers into a single annotated graph. Export the result as .graphml (for Cytoscape import) and .tsv node/edge tables. Rationale: MS2LDA discovers latent fragmentation patterns in tandem MS data; mapping these onto a network reveals structural homology and guides chemical interpretation of molecular families.

## Related tools

- **pyMolNetEnhancer** (Python module that integrates MS2LDA motif data and chemical class annotations onto GNPS networks; executes motif-to-node mapping using classical or feature-based approaches and exports annotated .graphml and .tsv outputs) — https://github.com/madeleineernst/pyMolNetEnhancer
- **RMolNetEnhancer** (R package providing equivalent functionality to pyMolNetEnhancer for mapping MS2LDA motifs and chemical classes onto GNPS networks) — https://github.com/madeleineernst/RMolNetEnhancer
- **GNPS (Global Natural Products Social Molecular Networking)** (Public platform for building mass spectral molecular networks from MS/MS data; provides clustered spectra and network job IDs required for downstream MS2LDA and MolNetEnhancer annotation) — https://gnps.ucsd.edu/
- **MS2LDA (Mass2Motifs Latent Dirichlet Allocation)** (Web platform (http://ms2lda.org/) that performs unsupervised LDA on fragmentation patterns to discover recurrent Mass2Motifs; outputs are integrated by MolNetEnhancer onto GNPS networks) — http://ms2lda.org/
- **Cytoscape** (Network visualization and analysis software used to import and visualize the annotated .graphml network output, with discrete mapping of edge 'interaction' attribute (shared motifs) to stroke color and node motif pie charts) — https://cytoscape.org/

## Examples

```
devtools::install_github("madeleineernst/RMolNetEnhancer"); source("Example_notebooks/Mass2Motifs_2_Network_Classical.ipynb") # then specify GNPS_job_ID, MS2LDA_job_ID, prob=0.01, overlap=0.3, top=5
```

## Evaluation signals

- The exported .graphml file is valid XML and imports successfully into Cytoscape without errors; network structure is preserved (same nodes and edges as input GNPS network).
- Node attributes in the .tsv output include 'TopSharedMotifs' column with motif identifiers and probability scores; edge attributes include 'interact' column with shared motif names.
- Filtering parameters (prob, overlap, top) were applied correctly: only Mass2Motifs meeting the probability and overlap thresholds appear in output; per-family motif counts match the specified `top` value.
- When imported into Cytoscape and colored by motif annotations, edges between nodes with shared Mass2Motifs display non-null 'interaction' values and nodes from the same molecular family show consistent high-frequency motifs in their pie charts.
- Row count in node output file equals the number of clusters in the input GNPS network; row count in edge output file matches the number of edges in the input network (both may be expanded with additional motif columns).

## Limitations

- MS2LDA job may experience server timeout for large datasets; manual download from http://ms2lda.org/ is recommended as a fallback.
- Probability and overlap thresholds should ideally be set within the MS2LDA web app during experiment creation for consistency; post-hoc filtering in MolNetEnhancer may not align perfectly with web-app results.
- The 'classical' approach requires clustering via GNPS classical workflow; the 'feature-based' approach requires GNPS feature-based molecular networking (e.g., from MZmine) — the two workflows produce incompatible network topologies and cannot be mixed.
- Motif interpretation depends on MS2LDA's unsupervised decomposition; latent motifs may represent genuine substructures or statistical artifacts and require expert validation against reference spectra or chemical structures.

## Evidence

- [readme] pyMolNetEnhancer is a python module integrating chemical class and substructure information within mass spectral molecular networks created through the Global Natural Products Social Molecular Networking (GNPS) platform: "pyMolNetEnhancer is a python module integrating chemical class and substructure information within mass spectral molecular networks created through the Global Natural Products Social Molecular"
- [readme] Map MS2LDA substructural information to mass spectral molecular networks (classical) and (feature based): "Map MS2LDA substructural information to mass spectral molecular networks (classical) and (feature based)"
- [readme] Create an LDA experiment on http://ms2lda.org/ using the MGF clustered spectra downloaded from GNPS: "Create an LDA experiment on http://ms2lda.org/ using the MGF clustered spectra downloaded from GNPS"
- [readme] The only things you need to specify are: Your GNPS job ID, Your MS2LDA job ID, User-defined parameters for mapping the Mass2Motifs onto the network: "The only things you need to specify are: Your GNPS job ID, Your MS2LDA job ID, User-defined parameters for mapping the Mass2Motifs onto the network"
- [readme] prob: minimal probability score for a Mass2Motif to be included. Default is 0.01. overlap: minimal overlap score for a Mass2Motif to be included. Default is 0.3.: "prob: minimal probability score for a Mass2Motif to be included. Default is 0.01. overlap: minimal overlap score for a Mass2Motif to be included. Default is 0.3."
- [readme] top: This parameter specifies how many most shared motifs per molecular family (network component index) should be shown. Default is 5.: "top: This parameter specifies how many most shared motifs per molecular family (network component index) should be shown. Default is 5."
- [readme] To color edges based on shared Mass2Motifs in between nodes select 'Stroke Color' in the 'Edge' tab to the left and choose 'interaction' as Column and 'Discrete Mapping' as Mapping Type: "To color edges based on shared Mass2Motifs in between nodes select 'Stroke Color' in the 'Edge' tab to the left and choose 'interaction' as Column and 'Discrete Mapping' as Mapping Type"
- [readme] To color nodes by the most shared Mass2Motifs per molecular family (network component index) select 'Image/Chart' in the 'Node' tab to the left and select Mass2Motifs shown in 'TopSharedMotifs' in the Edge Table: "To color nodes by the most shared Mass2Motifs per molecular family (network component index) select 'Image/Chart' in the 'Node' tab to the left and select Mass2Motifs shown in 'TopSharedMotifs' in"
