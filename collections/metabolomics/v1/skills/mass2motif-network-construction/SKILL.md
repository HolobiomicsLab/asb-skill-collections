---
name: mass2motif-network-construction
description: Use when after MS2LDA has inferred a motifset and you need to visualize and export the relationships between discovered Mass2Motifs for post-processing exploration, comparative annotation, or integration with external tools. Use this skill when you have motifset.json or motifset_optimized.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3083
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3520
  tools:
  - MS2LDA
  - Python
  - Latent Dirichlet Allocation (LDA)
derived_from:
- doi: 10.1093/bioinformatics/btx582
  title: ms2lda
evidence_spans:
- MS2LDA (Mass Spectrometry–Latent Dirichlet Allocation) is a framework
- MS2LDA uses Latent Dirichlet Allocation (LDA) to infer which motifs are most likely to explain the observed fragmentation patterns
- Configure the Python environment (set PYTHONPATH, activate conda, etc.)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2lda
    doi: 10.1093/bioinformatics/btx582
    title: ms2lda
  dedup_kept_from: coll_ms2lda
schema_version: 0.2.0
---

# mass2motif-network-construction

## Summary

Construct a network graph representation of Mass2Motifs discovered by MS2LDA, where nodes represent motifs annotated with their fragment/neutral-loss compositions and edges encode spectral similarity relationships. This enables integrated workflow visualization and export of the motif structure for downstream analysis and interpretation.

## When to use

After MS2LDA has inferred a motifset and you need to visualize and export the relationships between discovered Mass2Motifs for post-processing exploration, comparative annotation, or integration with external tools. Use this skill when you have motifset.json or motifset_optimized.json output and want to generate a network artifact (GraphML format) that represents both motif identities and their spectral similarity patterns.

## When NOT to use

- When you have not yet run the MS2LDA modeling step and do not have an inferred motifset — network construction requires completed LDA output.
- If your analysis goal is only to identify or annotate individual motifs without exploring their inter-relationships — simpler annotation workflows suffice.
- When input spectra have not been preprocessed (bag-of-fragments format not generated) — upstream preprocessing must complete first.

## Inputs

- motifset.json (or motifset_optimized.json)
- LDA model outputs
- Mass2Motif definitions (fragment and neutral-loss compositions)

## Outputs

- network.graphml
- Annotated network graph with nodes (Mass2Motifs) and weighted edges (spectral similarity)

## How to apply

Load the inferred motifset from motifset.json or motifset_optimized.json, extracting Mass2Motif definitions (fragment and neutral-loss compositions). Reconstruct pseudo-spectra representations from each motif's probability-weighted fragments and losses. Compute pairwise spectral similarity (e.g., cosine similarity) between all Mass2Motif pseudo-spectra. Build a graph where each Mass2Motif is a node, with weighted edges between motifs exceeding a similarity threshold. Annotate nodes with motif metadata (ID, fragment/loss composition, spectra count loading on motif) and edges with similarity scores. Serialize the network to GraphML format using Python and write to network.graphml for visualization in external tools.

## Related tools

- **MS2LDA** (Infers motifset and LDA model that provides input for network construction) — https://github.com/vdhooftcompmet/MS2LDA
- **Python** (Primary language for implementing graph construction, similarity computation, and GraphML serialization)
- **Latent Dirichlet Allocation (LDA)** (Underlying statistical model whose outputs (motif definitions and spectra loadings) are structured into network form)

## Evaluation signals

- network.graphml file is valid XML/GraphML with proper node and edge elements; can be parsed by standard graph tools
- Every discovered Mass2Motif from motifset.json appears as a node in the network with metadata annotations (ID, fragment composition, spectra count)
- Edges exist between motifs with spectral similarity above the defined threshold; edge weights are symmetric or justify directionality
- Similarity scores on edges fall within expected range (e.g., 0–1 for cosine similarity) and show expected clustering of related motifs
- Network can be successfully imported and visualized in external tools (e.g., Cytoscape, Gephi, or MS2LDAViz) without parsing errors

## Limitations

- Network quality depends on the motifset quality — poor LDA inference produces uninformative motif relationships.
- Pseudo-spectra reconstruction relies on probability weighting; rare fragments or losses may not be well represented in similarity computation.
- Similarity threshold is a manual choice; too strict thresholds yield sparse networks; too loose thresholds create dense hairballs with limited interpretability.
- GraphML export is static; real-time interactive filtering or dynamic threshold adjustment requires post-export tooling.
- Motifs with very few spectra assignments may have unstable pseudo-spectra and produce unreliable similarity edges.

## Evidence

- [other] MS2LDA provides a postprocessing pipeline that reads discovered motifs and LDA model outputs to generate a network representation (network.graphml) where nodes represent spectra annotated with their motif memberships and edges encode spectral similarity relationships, enabling integrated workflow visualization and export.: "MS2LDA provides a postprocessing pipeline that reads discovered motifs and LDA model outputs to generate a network representation (network.graphml)"
- [other] Load the inferred motifset from motifset.json or motifset_optimized.json, extracting Mass2Motif definitions (fragment and neutral-loss compositions). Retrieve or reconstruct pseudo-spectra representations from each motif's probability-weighted fragments and losses. Compute pairwise spectral similarity (e.g., cosine similarity) between all Mass2Motif pseudo-spectra. Build a directed or undirected graph where each Mass2Motif is a node, with weighted edges between motifs exceeding a similarity threshold.: "Load the inferred motifset from motifset.json or motifset_optimized.json, extracting Mass2Motif definitions (fragment and neutral-loss compositions)"
- [other] Annotate nodes with motif metadata (ID, fragment/loss composition, spectra count loading on motif) and edges with similarity scores. Serialize the network to GraphML format and write to network.graphml.: "Annotate nodes with motif metadata (ID, fragment/loss composition, spectra count loading on motif) and edges with similarity scores. Serialize the network to GraphML format"
- [readme] MS2LDA is an advanced tool designed for unsupervised substructure discovery in mass spectrometry data, utilizing topic modeling and providing automated annotation of discovered motifs. This tool significantly enhances the capabilities described in the original MS2LDA paper (2016), offering users an integrated workflow with improved usability, detailed visualizations, and a searchable motif database (MotifDB).: "MS2LDA is an advanced tool designed for unsupervised substructure discovery in mass spectrometry data, utilizing topic modeling and providing automated annotation of discovered motifs"
- [methods] MS2LDA uses Latent Dirichlet Allocation (LDA) to infer which motifs are most likely to explain the observed fragmentation patterns: "MS2LDA uses Latent Dirichlet Allocation (LDA) to infer which motifs are most likely to explain the observed fragmentation patterns"
