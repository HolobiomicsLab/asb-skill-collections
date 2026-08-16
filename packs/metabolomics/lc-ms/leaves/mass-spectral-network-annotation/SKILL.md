---
name: mass-spectral-network-annotation
description: Use when you have a GNPS molecular network (classical or feature-based) and MS2LDA LDA experiment output (Mass2Motif assignments with probability and overlap scores) from the same experiment, and you want to annotate network nodes with structural motifs and chemical classes to infer molecular.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
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

# mass-spectral-network-annotation

## Summary

Overlay MS2LDA-derived Mass2Motif substructural annotations and chemical class information onto GNPS molecular network nodes and edges to functionally contextualize spectral clusters. This integrates structural motif discovery with network topology, enabling chemical family and substructure inference across molecular families.

## When to use

You have a GNPS molecular network (classical or feature-based) and MS2LDA LDA experiment output (Mass2Motif assignments with probability and overlap scores) from the same experiment, and you want to annotate network nodes with structural motifs and chemical classes to infer molecular family composition and shared fragmentation patterns.

## When NOT to use

- MS2LDA experiment has not been run on the same MGF spectra used to build the GNPS network—motif-to-cluster matching will fail.
- Network is already fully annotated with compound identities or InChI/SMILES structures—motif annotation is redundant with structural identity.
- Input network is not in GNPS format (e.g., a user-constructed adjacency matrix without cluster identifiers)—node matching cannot be performed.

## Inputs

- GNPS molecular network edge table (TSV: CLUSTERID1, CLUSTERID2, cosine_score columns)
- MS2LDA Mass2Motif summary export (TSV or JSON: motif identifiers, document IDs, probability scores, overlap scores)
- GNPS job ID (for automated retrieval)
- MS2LDA job ID (for automated retrieval)
- Optional: chemical class metadata table (TSV)

## Outputs

- Annotated edge table (TSV: Mass2Motifs_Edges_Classical.tsv or Mass2Motifs_Edges_FeatureBased.tsv with 'interact' and 'TopSharedMotifs' columns)
- Annotated node table (TSV: Mass2Motifs_Nodes_Classical.tsv or Mass2Motifs_Nodes_FeatureBased.tsv with node identifiers and Mass2Motif assignments)
- Network visualization file (.graphml for Cytoscape import with node and edge attributes)
- Optional: chemical class annotation merged with motif assignments

## How to apply

Load the GNPS network edge table (containing CLUSTERID1, CLUSTERID2 node identifiers) and the MS2LDA summary export (containing motif-to-document probability and overlap scores) into pyMolNetEnhancer or RMolNetEnhancer. Apply user-defined filtering thresholds: prob (default 0.01, minimum probability score for a motif to be retained) and overlap (default 0.3, minimum fragment overlap) to exclude low-confidence motif assignments. For each molecular family (network component), retain the top N most-shared motifs (default top=5) and assign them to nodes via their cluster identifiers (classical) or feature identifiers (feature-based). Optionally merge chemical class metadata. Output annotated edge table (with 'interact' column encoding shared motifs), node table (with TopSharedMotifs attribute for per-family visualization), and a .graphml file for network visualization in Cytoscape.

## Related tools

- **pyMolNetEnhancer** (Python module that performs MS2LDA Mass2Motif and chemical class mapping to GNPS networks; executes classical and feature-based workflow variants) — https://github.com/madeleineernst/pyMolNetEnhancer
- **RMolNetEnhancer** (R package providing analogous functionality to pyMolNetEnhancer for MS2LDA and chemical class integration) — https://github.com/madeleineernst/RMolNetEnhancer
- **GNPS** (Global Natural Products Social Molecular Networking platform that generates the molecular network edge table and cluster identifiers to be annotated) — https://gnps.ucsd.edu/
- **MS2LDA** (Latent Dirichlet allocation web service that discovers Mass2Motif substructures and outputs probability/overlap scores for each motif-document pair) — http://ms2lda.org/
- **Cytoscape** (Network visualization tool used to import .graphml output and color nodes by TopSharedMotifs and edges by shared motif interactions) — https://cytoscape.org/

## Examples

```
pip install pyMolNetEnhancer; then in Python: `from pyMolNetEnhancer import Mass2Motifs_2_Network_Classical; Mass2Motifs_2_Network_Classical(gnps_job_id='XXXXXXXX', ms2lda_job_id='YYYYYYYY', prob=0.01, overlap=0.3, top=5)`
```

## Evaluation signals

- Output edge table contains valid 'interact' column with motif identifiers matching MS2LDA input; no NaN or unmatched cluster pairs.
- Node table TopSharedMotifs attribute contains ≤ top parameter value (default 5) motifs per molecular family, each with probability ≥ prob threshold (default 0.01) and overlap ≥ overlap threshold (default 0.3).
- Network .graphml file imports into Cytoscape without schema errors; nodes have feature/cluster identifiers and motif attributes; edges have interaction type.
- For classical networks: CLUSTERID1 and CLUSTERID2 in output match GNPS network node IDs. For feature-based: feature identifiers from MS2LDA match GNPS feature assignments.
- Comparison of filtered vs. unfiltered motif counts shows expected reduction; motifs below prob and overlap thresholds are absent from output.

## Limitations

- Server connection timeout may occur when retrieving large MS2LDA summary files; manual download from ms2lda.org is an alternative workaround.
- Probability and overlap thresholds must be consistent between the ms2lda.org web app and the mapping tool; misalignment can produce discrepant annotations.
- Feature-based mapping requires exact feature identifier alignment between GNPS MZmine output and MS2LDA MGF input; preprocessing inconsistencies will cause node matching failures.
- No changelog is available for the tools, limiting visibility into past annotation correctness issues or parameter stability.
- Chemical class metadata integration is optional and depends on external data availability; its absence does not prevent motif mapping but limits functional inference.

## Evidence

- [intro] pyMolNetEnhancer is a python module integrating chemical class and substructure information within mass spectral molecular networks created through the GNPS platform: "pyMolNetEnhancer is a python module integrating chemical class and substructure information within mass spectral molecular networks created through the GNPS platform"
- [other] Load the GNPS network edge table and MS2LDA Mass2Motif output; execute mapping function to overlay MS2LDA substructural information onto network nodes, matching nodes by feature identifiers: "Load the feature-based GNPS molecular network file (in classical network format) and MS2LDA Mass2Motif output containing substructure assignments. 2. Execute pyMolNetEnhancer's feature-based mapping"
- [readme] User-defined parameters: prob (minimal probability score for a Mass2Motif to be included, default 0.01), overlap (minimal overlap score, default 0.3), and top (how many most shared motifs per molecular family should be shown, default 5): "prob: minimal probability score for a Mass2Motif to be included. Default is 0.01. overlap: minimal overlap score for a Mass2Motif to be included. Default is 0.3. top: This parameter specifies how"
- [readme] Import the .graphml output file into Cytoscape; color edges based on shared Mass2Motifs and nodes by the most shared Mass2Motifs per molecular family: "To visualize results import the .graphml output file into Cytoscape. To color edges based on shared Mass2Motifs in between nodes select 'Stroke Color' in the 'Edge' tab to the left and choose"
- [readme] Depending on the size of this file, a server connection timeout may occur. Alternatively, you may download the file manually at http://ms2lda.org/: "Depending on the size of this file, a server connection timeout may occur. Alternatively, you may download the file manually at http://ms2lda.org/"
- [other] Output the annotated network table with node identifiers, edges, and attached MS2LDA substructure labels and chemical class information: "Output the annotated network table with node identifiers, edges, and attached MS2LDA substructure labels and chemical class information."
