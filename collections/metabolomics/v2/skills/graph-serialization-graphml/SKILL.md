---
name: graph-serialization-graphml
description: Use when after constructing a network graph where nodes represent Mass2Motifs
  (or spectra) and edges encode pairwise spectral similarity scores, and you need
  to export the network for visualization, post-processing, or sharing with collaborators
  using standard graph software (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0571
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - MS2LDA
  - Python
  - NetworkX
  - Cytoscape or Gephi
  license_tier: open
derived_from:
- doi: 10.1073/pnas.1608041113
  title: MS2LDA
evidence_spans:
- MS2LDA (Mass Spectrometry–Latent Dirichlet Allocation) is a framework
- MS2LDA uses Latent Dirichlet Allocation (LDA) to infer which motifs are most likely
  to explain the observed fragmentation patterns
- Configure the Python environment (set PYTHONPATH, activate conda, etc.)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2lda
    doi: 10.1073/pnas.1608041113
    title: MS2LDA
  dedup_kept_from: coll_ms2lda
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1073/pnas.1608041113
  all_source_dois:
  - 10.1073/pnas.1608041113
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Graph Serialization to GraphML

## Summary

Serialize a weighted, annotated network graph to GraphML format for persistent storage and downstream visualization. This skill converts in-memory graph objects (nodes representing Mass2Motifs, edges encoding spectral similarity) into standardized XML-based GraphML files suitable for import into network analysis and visualization tools.

## When to use

Apply this skill after constructing a network graph where nodes represent Mass2Motifs (or spectra) and edges encode pairwise spectral similarity scores, and you need to export the network for visualization, post-processing, or sharing with collaborators using standard graph software (e.g., Cytoscape, Gephi). Specifically, use this skill in the MS2LDA visualization and export stage, after motif discovery and spectral similarity computation are complete.

## When NOT to use

- Input is a simple feature table or spectral matrix that has not yet been converted to a network representation.
- Spectral similarity has not yet been computed; export requires pre-computed pairwise similarity scores.
- Network is intended for real-time interactive querying; GraphML is a static serialization format suitable for static visualization, not streaming or live updates.

## Inputs

- motifset.json or motifset_optimized.json (inferred LDA model output)
- Mass2Motif definitions (fragment and neutral-loss probability distributions)
- Pseudo-spectra representations (intensity-weighted fragments and losses per motif)
- Spectral similarity matrix or pairwise similarity scores (e.g., cosine similarity between motif pseudo-spectra)
- Similarity threshold parameter (e.g., cosine similarity ≥ 0.5)

## Outputs

- network.graphml (GraphML-formatted network file)
- Graph object with annotated nodes (motif ID, composition, loading) and weighted edges (similarity scores)

## How to apply

After building a directed or undirected graph where each Mass2Motif is a node annotated with metadata (motif ID, fragment/loss composition, spectra count) and edges are weighted by spectral similarity scores (typically computed via cosine similarity on pseudo-spectra), filter edges to retain only those exceeding a similarity threshold to reduce noise. Use Python's NetworkX library (or equivalent) to construct the graph object with node and edge attributes, then serialize to GraphML format using the library's native export function. Write the resulting GraphML file (typically named network.graphml) to disk. Verify the file contains expected nodes, edge weights, and metadata annotations by spot-checking the XML structure or reloading and inspecting graph statistics.

## Related tools

- **NetworkX** (Python library for graph construction, annotation, and serialization to GraphML format)
- **MS2LDA** (Parent framework providing motif definitions and spectral similarity outputs that serve as inputs to graph construction and serialization) — https://github.com/vdhooftcompmet/MS2LDA
- **Cytoscape or Gephi** (Downstream visualization tools that import and render GraphML network files)

## Examples

```
import networkx as nx
from networkx.algorithms import similarity
G = nx.Graph()
for motif_id, metadata in motifset.items():
    G.add_node(motif_id, composition=metadata['fragments'], loading=metadata['count'])
for (m1, m2), score in similarity_scores.items():
    if score >= 0.5:
        G.add_edge(m1, m2, weight=score)
nx.write_graphml(G, 'network.graphml')
```

## Evaluation signals

- GraphML file is well-formed XML (parseable by standard XML parsers and GraphML validators).
- Node count in serialized graph matches expected number of Mass2Motifs; edge count reflects similarity pairs above threshold.
- Node attributes include motif ID, fragment/loss composition, and spectra loading; edge attributes include similarity scores.
- File can be successfully imported and rendered in NetworkX, Cytoscape, or Gephi without errors.
- Reloading the GraphML file and computing basic graph statistics (density, clustering, degree distribution) yields plausible values consistent with the input similarity threshold and motif count.

## Limitations

- GraphML export is a static snapshot; subsequent changes to the motif set or similarity thresholds require re-computation and re-export.
- Similarity threshold choice is critical: too lenient produces a densely connected graph that may obscure structure; too stringent produces fragmented or empty networks.
- Large networks (thousands of motifs) may produce GraphML files too large for efficient manipulation in some visualization tools.
- No built-in provenance tracking in GraphML format; metadata such as similarity metric (cosine vs. other), threshold value, and timestamp should be documented externally or embedded as graph attributes.

## Evidence

- [other] Build a directed or undirected graph where each Mass2Motif is a node, with weighted edges between motifs exceeding a similarity threshold.: "Build a directed or undirected graph where each Mass2Motif is a node, with weighted edges between motifs exceeding a similarity threshold."
- [other] Annotate nodes with motif metadata (ID, fragment/loss composition, spectra count loading on motif) and edges with similarity scores.: "Annotate nodes with motif metadata (ID, fragment/loss composition, spectra count loading on motif) and edges with similarity scores."
- [other] Serialize the network to GraphML format and write to network.graphml.: "Serialize the network to GraphML format and write to network.graphml."
- [other] MS2LDA provides a postprocessing pipeline that reads discovered motifs and LDA model outputs to generate a network representation (network.graphml) where nodes represent spectra annotated with their motif memberships and edges encode spectral similarity relationships, enabling integrated workflow visualization and export.: "MS2LDA provides a postprocessing pipeline that reads discovered motifs and LDA model outputs to generate a network representation (network.graphml) where nodes represent spectra annotated with their"
