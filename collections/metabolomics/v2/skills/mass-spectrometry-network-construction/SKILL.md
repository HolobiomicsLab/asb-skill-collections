---
name: mass-spectrometry-network-construction
description: Use when you have deconvolved GC-MS spectra (output from auto-deconvolution) and want to group similar spectra into clusters to discover spectral families, identify co-eluting compounds, or organize unknown metabolites by structural similarity.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3520
  tools:
  - GNPS_GC
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-network-construction

## Summary

Construct a spectral similarity network from deconvolved gas chromatography–mass spectrometry spectra by computing pairwise cosine similarity scores and applying a threshold to form an undirected graph. This organizes spectra into communities and reveals molecular relationships at scale.

## When to use

You have deconvolved GC-MS spectra (output from auto-deconvolution) and want to group similar spectra into clusters to discover spectral families, identify co-eluting compounds, or organize unknown metabolites by structural similarity. Apply this when you need to move beyond individual spectrum annotation to network-level interpretation.

## When NOT to use

- Input spectra are not yet deconvolved (apply auto-deconvolution first).
- You require quantitative abundance correlation; this skill builds on spectral shape similarity only.
- Your goal is single-spectrum identification rather than group-level pattern discovery.

## Inputs

- deconvolved mass spectra table (normalized m/z and intensity pairs)
- similarity threshold parameter (0–1 scale, typically >0.5–0.7 for GC-MS)

## Outputs

- molecular network in GraphML format
- node-link JSON summary table mapping spectrum IDs to cluster assignments
- similarity statistics per edge (cosine similarity scores)

## How to apply

Load the deconvolved mass spectra table from the auto-deconvolution output, normalized to m/z and intensity values. Compute pairwise cosine similarity scores between all spectra. Apply a similarity threshold (cutoff value determined by empirical validation or prior knowledge of your compound class) to retain only high-confidence spectral pairs, then construct an undirected graph with spectra as nodes and similarity relationships as edges. Detect connected components and community clusters within the graph using standard graph partitioning algorithms. Export the result in GraphML format with node attributes annotated by cluster membership and spectral metadata (e.g., retention index, ionization mode).

## Related tools

- **GNPS_GC** (implements molecular networking for deconvolved GC-MS spectra, computes cosine similarity, detects graph clusters, and exports network in GraphML format) — https://github.com/bittremieux/GNPS_GC

## Evaluation signals

- All spectrum nodes in the GraphML output have valid cluster membership attributes and no orphaned or malformed edges.
- Cosine similarity scores on all edges fall within the applied threshold range (e.g., all ≥0.7 if threshold was 0.7).
- Connected components and clusters are non-overlapping; each spectrum belongs to exactly one cluster.
- Node-link JSON summary table row count matches the number of input deconvolved spectra.
- GraphML graph is acyclic and undirected; degree distribution and modularity are consistent with prior validation on standard reference spectra.

## Limitations

- Performance scales quadratically with the number of input spectra; large datasets (>10,000 spectra) may require distributed computation or dimension reduction.
- Similarity threshold choice is critical and data-dependent; no single threshold generalizes across all GC-MS applications or compound classes.
- Deconvolution quality directly impacts network quality; overlapping or misassigned peaks in auto-deconvolution will corrupt spectral similarity and cluster assignments.

## Evidence

- [other] how_to_apply_step_1: "Load the deconvolved mass spectra table from the auto-deconvolution output."
- [other] how_to_apply_step_2: "Compute pairwise cosine similarity scores between all deconvolved spectra using normalized m/z and intensity values."
- [other] how_to_apply_step_3: "Apply a similarity threshold to retain only high-confidence spectral pairs and construct an undirected graph."
- [other] how_to_apply_step_4: "Detect connected components and community clusters within the spectral graph."
- [other] how_to_apply_step_5: "Export the molecular network in GraphML format with nodes representing spectra, edges representing similarity relationships, and node attributes containing cluster membership and spectral metadata."
- [other] output_format: "Generate a node-link JSON summary table mapping spectrum identifiers to cluster assignments and similarity statistics."
- [other] tool_implementation: "The manuscript presents a companion repository (bittremieux/GNPS_GC) that implements molecular networking as a method to organize deconvolved GC-MS spectra, following the auto-deconvolution step."
- [other] research_context: "How does molecular networking organize deconvolved gas chromatography–mass spectrometry spectra into a spectral similarity network?"
