---
name: graph-clustering-community-detection
description: Use when after constructing a spectral similarity network from pairwise
  cosine similarity scores between deconvolved GC-MS spectra.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3439
  edam_topics:
  - http://edamontology.org/topic_0080
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - GNPS_GC
  techniques:
  - GC-MS
  - ion-mobility-MS
  license_tier: open
derived_from:
- doi: 10.1038/s41587-020-0700-3
  title: mshub
evidence_spans:
- bittremieux/GNPS_GC
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mshub_cq
    doi: 10.1038/s41587-020-0700-3
    title: mshub
  dedup_kept_from: coll_mshub_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41587-020-0700-3
  all_source_dois:
  - 10.1038/s41587-020-0700-3
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# graph-clustering-community-detection

## Summary

Detect connected components and community clusters within a spectral similarity graph to group gas chromatography–mass spectrometry spectra by structural or chemical relatedness. This skill organizes deconvolved spectra into interpretable molecular families for downstream annotation and comparative analysis.

## When to use

Apply this skill after constructing a spectral similarity network from pairwise cosine similarity scores between deconvolved GC-MS spectra. Use it when you have a weighted or unweighted graph with spectra as nodes and similarity relationships as edges, and you need to partition spectra into cohesive groups that share common fragmentation patterns or chemical properties.

## When NOT to use

- Input is a raw (non-deconvolved) GC-MS data file or an unprocessed mass spectrum; apply auto-deconvolution first.
- Similarity matrix is sparse or contains only low-confidence pairs below the similarity threshold; clustering will yield fragmented or singleton clusters.
- Spectra are already pre-classified or annotated by an external reference library; use annotation matching instead of de novo clustering.

## Inputs

- Undirected weighted graph (nodes=spectra, edges=cosine similarity scores above threshold)
- Normalized m/z and intensity values for each spectrum
- Pairwise cosine similarity matrix or edge list with similarity thresholds applied

## Outputs

- Cluster membership assignments (spectrum ID → cluster ID mapping)
- Connected component or community structure (graph partition)
- Node-link JSON summary table with spectrum identifiers, cluster assignments, and similarity statistics
- GraphML-formatted network file with cluster membership node attributes

## How to apply

Detect connected components and community clusters within the spectral similarity graph by applying graph partitioning or modularity-optimization algorithms (e.g., greedy modularity optimization, Louvain method) on the undirected graph constructed from high-confidence spectral pairs above a similarity threshold. Assign each spectrum a cluster membership identifier based on its community or connected component. Export node attributes including cluster assignment and spectral metadata (e.g., retention time, m/z, intensity). Verify cluster coherence by inspecting intra-cluster edge density and inter-cluster sparsity; clusters should exhibit high internal similarity and low cross-cluster similarity to reflect true spectral families.

## Related tools

- **GNPS_GC** (Orchestrates auto-deconvolution, cosine similarity computation, spectral graph construction, and community detection on deconvolved GC-MS spectra) — https://github.com/bittremieux/GNPS_GC

## Evaluation signals

- Cluster size distribution is non-trivial: not all spectra are assigned to a single cluster, and singletons are rare or absent (indicating meaningful structure).
- Intra-cluster cosine similarity scores are consistently higher than inter-cluster scores (validates cluster coherence).
- Cluster membership is stable across multiple runs or graph re-sampling (reproducibility check).
- GraphML output contains valid node and edge attributes with no missing cluster assignments or metadata fields.
- Connected components or communities are well-separated in a 2D or 3D projection (t-SNE, UMAP, or force-directed layout) of the similarity graph.

## Limitations

- Community detection algorithms are sensitive to the similarity threshold: too lenient thresholds produce oversized clusters; too stringent thresholds fragment the network into many singletons. Threshold selection requires empirical tuning or cross-validation.
- Highly similar isomers or isobars may be erroneously merged into a single cluster if cosine similarity alone is used; additional orthogonal metadata (e.g., retention index, retention time, ion mobility) may be needed to disambiguate them.
- Large networks (>10,000 spectra) may incur computational overhead in exact modularity optimization; scalable approximations (e.g., Louvain heuristic) are recommended.
- No changelog or versioning strategy documented for the GNPS_GC repository, limiting reproducibility across updates.

## Evidence

- [other] Detect connected components and community clusters within the spectral graph.: "Detect connected components and community clusters within the spectral graph."
- [other] Compute pairwise cosine similarity scores between all deconvolved spectra using normalized m/z and intensity values. Apply a similarity threshold to retain only high-confidence spectral pairs and construct an undirected graph.: "Compute pairwise cosine similarity scores between all deconvolved spectra using normalized m/z and intensity values. Apply a similarity threshold to retain only high-confidence spectral pairs and"
- [other] Export the molecular network in GraphML format with nodes representing spectra, edges representing similarity relationships, and node attributes containing cluster membership and spectral metadata.: "Export the molecular network in GraphML format with nodes representing spectra, edges representing similarity relationships, and node attributes containing cluster membership and spectral metadata."
- [other] Generate a node-link JSON summary table mapping spectrum identifiers to cluster assignments and similarity statistics.: "Generate a node-link JSON summary table mapping spectrum identifiers to cluster assignments and similarity statistics."
- [readme] This is a companion repository to the following manuscript: Aksenov, A.A., Laponogov, I., Zhang, Z. et al. Auto-deconvolution and molecular networking of gas chromatography–mass spectrometry data.: "This is a companion repository to the following manuscript: Aksenov, A.A., Laponogov, I., Zhang, Z. et al. Auto-deconvolution and molecular networking of gas chromatography–mass spectrometry data."
