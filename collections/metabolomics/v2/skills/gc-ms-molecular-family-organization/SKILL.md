---
name: gc-ms-molecular-family-organization
description: Use when after auto-deconvolution of GC-MS data has produced a table
  of individual deconvolved mass spectra (one per detected peak), and your goal is
  to group spectra into molecular families based on mass spectral similarity rather
  than retention time or chemical class.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3172
  tools:
  - GNPS_GC
  techniques:
  - GC-MS
  license_tier: open
  provenance_tier: literature
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

# gc-ms-molecular-family-organization

## Summary

Organize deconvolved gas chromatography–mass spectrometry spectra into spectral similarity networks by computing pairwise cosine similarity scores and constructing a spectral graph, enabling discovery of structurally related metabolite families. This skill assigns spectra to molecular families based on spectral similarity, facilitating compound annotation and metabolite clustering without prior identification.

## When to use

Apply this skill after auto-deconvolution of GC-MS data has produced a table of individual deconvolved mass spectra (one per detected peak), and your goal is to group spectra into molecular families based on mass spectral similarity rather than retention time or chemical class. Use this when you need to discover previously unknown relationships between compounds, prioritize spectra for manual curation, or leverage consensus spectral properties across a family to improve compound identification confidence.

## When NOT to use

- Input spectra have not been deconvolved; spectra still contain unresolved co-eluting compounds or overlapping fragments.
- Goal is to annotate individual spectra against a reference library; use spectral library search instead of molecular networking.
- GC-MS data are from a single isolated compound or very small sample set where clustering offers no statistical power.

## Inputs

- deconvolved mass spectra table (rows = spectra, columns = m/z values, cells = normalized intensities)
- auto-deconvolution output (e.g., from GNPS_GC deconvolution module)
- spectral metadata (e.g., retention index, peak ID, chemical class annotations if available)

## Outputs

- molecular network in GraphML format (nodes = spectra, edges = similarity links, node attributes = cluster ID and metadata)
- node-link JSON summary table (spectrum ID → cluster assignment and similarity statistics)
- spectral clusters / molecular families (grouped spectra with consensus properties)

## How to apply

Load the deconvolved mass spectra table from auto-deconvolution output. Compute pairwise cosine similarity scores between all deconvolved spectra using normalized m/z and intensity values; apply a similarity threshold (typically derived from empirical or statistical validation) to retain only high-confidence spectral pairs and construct an undirected graph where nodes are spectra and edges represent similarity relationships. Detect connected components and community clusters within this spectral graph using graph clustering algorithms. Export the resulting molecular network in GraphML format with nodes annotated with cluster membership and spectral metadata (e.g., retention index, chemical class). The rationale is that spectra sharing high cosine similarity often originate from structurally related compounds or isomers, and grouping them reveals metabolite families that would be difficult to discover by retention time alone.

## Related tools

- **GNPS_GC** (Implements auto-deconvolution and molecular networking workflow for GC-MS data; computes cosine similarity, constructs spectral graphs, detects clusters, and exports networks in GraphML format.) — https://github.com/bittremieux/GNPS_GC

## Evaluation signals

- All deconvolved spectra are assigned to exactly one cluster (no orphaned spectra, no missing nodes in output network).
- Edges in the output network only connect spectra with cosine similarity above the applied threshold; no spurious or below-threshold connections.
- Cluster sizes and inter-cluster similarity statistics match expectations from the input data (e.g., a large cluster should show higher intra-cluster cosine similarity than inter-cluster similarity).
- GraphML and JSON outputs contain consistent cluster assignments (same spectrum ID maps to the same cluster in both formats).
- Exported spectral metadata (retention index, chemical class) are preserved and annotated correctly on all nodes in the network.

## Limitations

- Molecular networking relies on spectral similarity (cosine score) and cannot distinguish between constitutional isomers or stereoisomers that produce identical or near-identical mass spectra.
- Performance and cluster quality depend on appropriate choice of similarity threshold; no universally optimal threshold is provided in the article, and threshold tuning may require manual inspection or empirical validation.
- Networks become computationally expensive and visually complex for very large deconvolved datasets (thousands of spectra); scalability and visualization may be limiting.
- Spectra with low signal-to-noise or incomplete fragmentation patterns may form spurious clusters or fail to cluster with true structural relatives.

## Evidence

- [other] Compute pairwise cosine similarity scores between all deconvolved spectra using normalized m/z and intensity values.: "Compute pairwise cosine similarity scores between all deconvolved spectra using normalized m/z and intensity values."
- [other] Apply a similarity threshold to retain only high-confidence spectral pairs and construct an undirected graph.: "Apply a similarity threshold to retain only high-confidence spectral pairs and construct an undirected graph."
- [other] Detect connected components and community clusters within the spectral graph.: "Detect connected components and community clusters within the spectral graph."
- [other] Export the molecular network in GraphML format with nodes representing spectra, edges representing similarity relationships, and node attributes containing cluster membership and spectral metadata.: "Export the molecular network in GraphML format with nodes representing spectra, edges representing similarity relationships, and node attributes containing cluster membership and spectral metadata."
- [readme] This is a companion repository to the following manuscript: Aksenov, A.A., Laponogov, I., Zhang, Z. _et al_. Auto-deconvolution and molecular networking of gas chromatography–mass spectrometry data.: "companion repository to the following manuscript: Aksenov, A.A., Laponogov, I., Zhang, Z. _et al_. Auto-deconvolution and molecular networking of gas chromatography–mass spectrometry data."
