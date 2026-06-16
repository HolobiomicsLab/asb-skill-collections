---
name: mass-spectral-network-annotation
description: Use when you have a GNPS-generated molecular network (graphml or JSON format) and corresponding MS2LDA experiment results or chemical class assignments, and you want to annotate network nodes with substructural motifs or chemical classes to facilitate structural interpretation and identify.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0361
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_0594
  tools:
  - pyMolNetEnhancer
  - Python
  - RMolNetEnhancer
  - GNPS (Global Natural Products Social Molecular Networking)
  - MS2LDA (MS2 Latent Dirichlet Allocation) at ms2lda.org
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

# mass-spectral-network-annotation

## Summary

Integrate MS2LDA-derived Mass2Motif substructural motifs and chemical class information onto nodes and edges of GNPS mass spectral molecular networks (classical or feature-based modes) to annotate molecular families with interpretable structural fragments and metabolite classes. This enriches network topology with chemical meaning, enabling discovery of shared structural features across related compounds.

## When to use

You have a GNPS-generated molecular network (graphml or JSON format) and corresponding MS2LDA experiment results or chemical class assignments, and you want to annotate network nodes with substructural motifs or chemical classes to facilitate structural interpretation and identify compounds sharing common mass spectral fragmentation patterns or metabolite families.

## When NOT to use

- You do not have MS2LDA results or chemical class assignments—the tool requires these external annotations as input.
- Your molecular network was created outside GNPS and lacks compatible node identifiers (CLUSTERID) or precursor m/z metadata needed for motif alignment.
- You are working with a pre-annotated network where all MS2 fragmentation patterns have already been mapped via orthogonal spectral database matching (e.g., NIST, MassBank); motif discovery adds redundant or conflicting information.

## Inputs

- GNPS molecular network file (graphml or JSON format)
- MS2LDA job ID or manually downloaded MS2LDA summary table (TSV/CSV)
- MS2LDA motif-document assignment data with probability and overlap scores
- Chemical class annotation table (optional, for chemical-class mapping)

## Outputs

- Annotated molecular network file (graphml or JSON) with motif IDs and chemical classes embedded in node attributes
- Mass2Motifs_Edges_Classical.tsv or Mass2Motifs_Edges_FeatureBased.tsv (edge table with motif interaction annotations)
- Mass2Motifs_Nodes_Classical.tsv or Mass2Motifs_Nodes_FeatureBased.tsv (node table with TopSharedMotifs per cluster)
- Cytoscape-compatible network visualization file

## How to apply

Obtain your GNPS job ID and MS2LDA job ID (or download the MS2LDA summary table manually if server timeout occurs). Load the GNPS classical or feature-based molecular network file and the MS2LDA motif output data into pyMolNetEnhancer (Python) or RMolNetEnhancer (R). Set filtering thresholds for motif inclusion: `prob` (minimum probability score, default 0.01) and `overlap` (minimum overlap score, default 0.3)—these should match thresholds set in the ms2lda.org web app. Specify the `top` parameter to control how many most-shared motifs per molecular family (network component/cluster) are retained (default 5). The tool aligns motif identifiers to network nodes by matching precursor m/z and spectral similarity, then embeds motif IDs and chemical class metadata as node and edge attributes. Export the result as an annotated graphml or JSON file, optionally including TSV tables of edges and nodes for separate import into Cytoscape, where you can visualize motif sharing via discrete edge stroke color mapping and node pie-chart visualization of top shared motifs.

## Related tools

- **pyMolNetEnhancer** (Primary Python module that integrates MS2LDA motifs and chemical class information into classical or feature-based GNPS molecular networks; performs node/edge attribute mapping and outputs annotated network files.) — https://github.com/madeleineernst/pyMolNetEnhancer
- **RMolNetEnhancer** (Analogous R package with identical functionality; alternative implementation for users preferring R workflows.) — https://github.com/madeleineernst/RMolNetEnhancer
- **GNPS (Global Natural Products Social Molecular Networking)** (Source platform for generating classical and feature-based molecular networks; provides network topology, node IDs, and precursor m/z data consumed by pyMolNetEnhancer.) — https://gnps.ucsd.edu/
- **MS2LDA (MS2 Latent Dirichlet Allocation) at ms2lda.org** (Upstream tool that generates Mass2Motif assignments and probability/overlap scores; motif output is the primary annotation source fed into the mapping workflow.) — http://ms2lda.org/
- **Cytoscape** (Visualization and analysis platform for importing the annotated graphml/JSON network files and rendering motif/chemical-class annotations as node and edge visual properties (stroke color, pie charts).) — https://cytoscape.org/

## Evaluation signals

- Annotated network graphml/JSON file is valid and loads without schema errors; all input nodes retain their original CLUSTERID identifiers.
- Each node with MS2LDA coverage contains non-empty motif attributes (motif IDs, associated confidence scores) corresponding to the input MS2LDA summary data.
- Motif filtering is correctly applied: only motifs with probability ≥ `prob` threshold and overlap ≥ `overlap` threshold appear in output; `top` parameter correctly limits the number of TopSharedMotifs shown per molecular family (cluster).
- Edge annotations correctly reflect shared motifs between connected nodes: inspect Mass2Motifs_Edges_Classical.tsv and verify the 'interact' column contains motif IDs only for node pairs that share ≥1 motif above threshold.
- Network visualization in Cytoscape successfully renders discrete edge stroke colors corresponding to distinct shared motifs and pie-chart node annotations match the TopSharedMotifs column from the node output table.

## Limitations

- Server connection timeouts may occur when programmatically fetching large MS2LDA summary files; manual download from ms2lda.org is a required fallback.
- Motif-to-node mapping relies on matching precursor m/z and spectral similarity; ambiguous or misaligned m/z values may result in missed or spurious motif assignments.
- Probability and overlap thresholds must be set consistently in both the ms2lda.org web app and the annotation tool; mismatched thresholds will produce inconsistent results and may exclude expected motifs.
- No changelog or version tracking is available, limiting reproducibility tracking across different releases.

## Evidence

- [intro] pyMolNetEnhancer integrates chemical class and substructure information within mass spectral molecular networks created through the GNPS platform: "pyMolNetEnhancer integrates chemical class and substructure information within mass spectral molecular networks created through the GNPS platform"
- [other] Load GNPS network and MS2LDA data, align motif identifiers to nodes by precursor m/z and spectral similarity, annotate nodes with motif IDs and confidence, export enhanced network: "Load the GNPS-generated classical molecular network file (graphml or JSON format) and MS2LDA Mass2Motif output data containing substructural motif assignments. 2. Use pyMolNetEnhancer's"
- [readme] Parameters: prob (minimum probability, default 0.01), overlap (minimum overlap, default 0.3), top (most shared motifs per family, default 5): "`prob`: minimal probability score for a Mass2Motif to be included. Default is 0.01. `overlap`: minimal overlap score for a Mass2Motif to be included. Default is 0.3. `top`: This parameter specifies"
- [readme] Thresholds should match settings in ms2lda.org web app; summary table contains filtered motif-document relations using set thresholds: "The probability and overlap thresholds can be set within the ms2lda.org app as well under the Experimental Options tab. It is recommendable to do so when inspecting results in the web app."
- [readme] Import graphml output into Cytoscape; color edges by shared motifs via discrete mapping on 'interaction' column; color nodes by TopSharedMotifs pie-chart visualization: "To visualize results import the .graphml output file into Cytoscape. To color edges based on shared Mass2Motifs in between nodes select 'Stroke Color' in the 'Edge' tab to the left and choose"
