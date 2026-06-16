---
name: spectral-similarity-computation
description: Use when after inferring Mass2Motif definitions from LDA modeling when you need to build a network representation of motif relationships.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MS2LDA
  - Python
  - Latent Dirichlet Allocation (LDA)
  - Spec2Vec
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

# spectral-similarity-computation

## Summary

Compute pairwise spectral similarity (e.g., cosine similarity) between Mass2Motif pseudo-spectra or fragment compositions to identify and weight relationships in mass spectrometry fragmentation networks. This skill is essential for constructing motif networks that encode similarity-based connectivity and enable integrated visualization of substructure relationships.

## When to use

Apply this skill after inferring Mass2Motif definitions from LDA modeling when you need to build a network representation of motif relationships. Specifically, use it when you have extracted probability-weighted fragment and neutral-loss compositions from the motifset and must compute pairwise similarities between all motifs to determine which should be connected in the motif network graph with weighted edges.

## When NOT to use

- Input is already a pre-computed similarity matrix or distance matrix — use it directly without recomputing.
- Motif definitions have not yet been inferred from LDA modeling — preprocess and run LDA first.
- The goal is only to annotate individual motifs with known substructures without building a network graph — use direct library matching (e.g., MotifDB lookup) instead.

## Inputs

- motifset.json or motifset_optimized.json (inferred LDA model output containing Mass2Motif definitions)
- Probability-weighted fragment compositions per motif
- Probability-weighted neutral-loss compositions per motif
- Motif pseudo-spectra vectors (reconstructed from fragments and losses)

## Outputs

- Pairwise spectral similarity matrix (motif × motif)
- Weighted network edges between motifs (filtered by similarity threshold)
- Annotated network representation with similarity scores on edges
- network.graphml (GraphML-formatted network artifact for visualization and export)

## How to apply

Retrieve or reconstruct pseudo-spectra representations from each Mass2Motif's probability-weighted fragments and losses (the most abundant fragment ions and neutral losses composing each motif). Compute pairwise spectral similarity (typically cosine similarity) between all Mass2Motif pseudo-spectra vectors. Apply a similarity threshold to filter weak relationships, retaining only motif pairs exceeding the threshold to reduce noise and focus the network on strong structural similarities. Annotate graph edges with the computed similarity scores to preserve quantitative relationship strength for downstream visualization and interpretation.

## Related tools

- **MS2LDA** (Framework that organizes the complete motif discovery pipeline including postprocessing and network construction from inferred motifset outputs) — https://github.com/vdhooftcompmet/MS2LDA
- **Latent Dirichlet Allocation (LDA)** (Generates the motifset (Mass2Motif definitions and probability weights) that serve as input to spectral similarity computation)
- **Spec2Vec** (Provides spectral embedding and similarity computation methods that can be used for motif pseudo-spectra representation and comparison) — https://zenodo.org/records/15688609
- **Python** (Implementation language for spectral similarity computation and network construction workflows)

## Evaluation signals

- Similarity matrix is symmetric (if computing undirected motif relationships) and has diagonal values near 1.0 (self-similarity).
- Number of weighted edges in the final network equals the count of motif pairs above the similarity threshold; absent edges have scores below threshold.
- Similarity scores range between 0 and 1 (for cosine similarity) and are consistently populated in the edge annotations of the GraphML output.
- GraphML file can be parsed without errors and contains all expected node attributes (motif ID, fragment composition, spectra count) and edge attributes (similarity score).
- Network topology reflects expected structural relationships — motifs sharing common fragment ions or neutral losses have higher similarity scores and are connected.

## Limitations

- Pseudo-spectra reconstruction quality depends on accurate probability weighting from the LDA model; poorly inferred motifs will yield unreliable similarities.
- Similarity threshold selection is a hyperparameter; too high a threshold may fragment the network into isolated components, while too low a threshold introduces spurious edges.
- Cosine similarity is the default metric but may not capture non-linear or structural dissimilarity relationships; alternative metrics (e.g., Euclidean, Wasserstein) may be more appropriate for specific applications.
- The workflow assumes spectra have been properly normalized and preprocessed (noise filtered, neutral losses extracted) before motif discovery; invalid or incomplete motif definitions will propagate through similarity computation.
- Network export to GraphML is lossy for high-dimensional spectral vectors; full pseudo-spectra are not retained in the GraphML artifact, only aggregate similarity scores.

## Evidence

- [other] Compute pairwise spectral similarity (e.g., cosine similarity) between all Mass2Motif pseudo-spectra: "Compute pairwise spectral similarity (e.g., cosine similarity) between all Mass2Motif pseudo-spectra."
- [other] Load the inferred motifset from motifset.json or motifset_optimized.json, extracting Mass2Motif definitions (fragment and neutral-loss compositions): "Load the inferred motifset from motifset.json or motifset_optimized.json, extracting Mass2Motif definitions (fragment and neutral-loss compositions)."
- [other] Retrieve or reconstruct pseudo-spectra representations from each motif's probability-weighted fragments and losses: "Retrieve or reconstruct pseudo-spectra representations from each motif's probability-weighted fragments and losses."
- [other] Build a directed or undirected graph where each Mass2Motif is a node, with weighted edges between motifs exceeding a similarity threshold: "Build a directed or undirected graph where each Mass2Motif is a node, with weighted edges between motifs exceeding a similarity threshold."
- [other] MS2LDA provides a postprocessing pipeline that reads discovered motifs and LDA model outputs to generate a network representation (network.graphml) where nodes represent spectra annotated with their motif memberships and edges encode spectral similarity relationships: "MS2LDA provides a postprocessing pipeline that reads discovered motifs and LDA model outputs to generate a network representation (network.graphml) where nodes represent spectra annotated with their"
