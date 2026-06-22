---
name: gc-ms-spectral-similarity-clustering
description: Use when when you have deconvolved GC-MS spectra (post-deconvolution output compatible with GNPS_GC input specification) and need to group them by chemical similarity to construct a molecular network.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  tools:
  - GNPS_GC
  techniques:
  - LC-MS
  - GC-MS
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
  - build: coll_mshub
    doi: 10.1038/s41587-020-0700-3
    title: mshub
  dedup_kept_from: coll_mshub
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

# gc-ms-spectral-similarity-clustering

## Summary

Groups deconvolved gas chromatography–mass spectrometry spectra by spectral similarity to identify and cluster chemically related compounds within complex mixtures. This enables structured molecular network assembly where nodes represent unique deconvolved spectra and edges reflect cosine similarity-based relationships.

## When to use

When you have deconvolved GC-MS spectra (post-deconvolution output compatible with GNPS_GC input specification) and need to group them by chemical similarity to construct a molecular network. Apply this skill before network topology analysis when you want to discover co-eluting or structurally related metabolites without prior compound annotation.

## When NOT to use

- Input spectra have not yet been deconvolved (i.e. contain unresolved co-eluting peaks); perform auto-deconvolution first.
- You require spectral annotation or compound identification; this skill performs similarity clustering only—library matching or structure elucidation is a separate workflow step.
- Data are from liquid chromatography–mass spectrometry (LC-MS) or other non-GC platforms; GNPS_GC is GC-MS specific.

## Inputs

- Deconvolved GC-MS spectra (GNPS_GC input format: spectral data with m/z and intensity pairs, retention time annotations)
- GNPS_GC networking parameters (similarity threshold, network assembly options)

## Outputs

- Molecular network file in GraphML or JSON format
- Network nodes (one per unique deconvolved spectrum with metadata: retention time, precursor m/z, peak intensity)
- Network edges (annotated with cosine similarity scores and edge metrics)

## How to apply

Load deconvolved spectra in GNPS_GC-compatible format and submit the batch to the GNPS_GC molecular networking pipeline with standard similarity parameters. The pipeline computes pairwise cosine similarity scores across all deconvolved spectra, then clusters or connects spectra exceeding a similarity threshold to form edges in the output network. Monitor job completion and retrieve the resulting molecular network file (GraphML or JSON format). Validate the clustering by inspecting node counts (one per unique deconvolved spectrum), edge counts (reflecting similarity pairs), and connectivity metrics (e.g., degree distribution, connected components) to confirm that chemically related spectra are grouped appropriately.

## Related tools

- **GNPS_GC** (Web service and command-line interface for auto-deconvolution and cosine similarity-based molecular networking of GC-MS data; computes spectral similarity, clusters spectra, and outputs network topology.) — https://github.com/bittremieux/GNPS_GC

## Evaluation signals

- Network node count equals the number of unique deconvolved spectra submitted (one spectrum per node).
- Edge count and distribution reflect expected chemical similarity: edges connect spectra with cosine similarity above the applied threshold; validate by sampling edges and confirming the annotated cosine scores are consistent with similarity computation.
- Network connectivity metrics (e.g., number of connected components, average degree) are reasonable for the sample complexity; highly fragmented networks (many isolated nodes) or fully connected networks may indicate incorrect threshold or data quality issues.
- GraphML/JSON output structure is valid and parseable; nodes carry retention time and m/z metadata; edges carry cosine similarity annotations.
- Spot-check: manually inspect a small cluster of connected nodes and confirm they represent chemically plausible or co-eluting compounds (e.g., same parent ion, similar retention times, related fragmentation patterns).

## Limitations

- Clustering depends critically on the cosine similarity threshold and other networking parameters; threshold selection is not automated in this skill and must be set based on the sample and research question.
- Spectral similarity alone does not establish compound identity or causality; two spectra may cluster due to coincidental m/z overlap rather than true chemical relationship.
- Performance and network density scale with the number of deconvolved spectra; very large batches (>10,000 unique spectra) may require parameter tuning or resource optimization.
- The method assumes deconvolution has been performed correctly upstream; poor-quality deconvolution (missed peaks, false artifacts, incomplete peak separation) propagates into the similarity network.

## Evidence

- [other] The method integrates auto-deconvolution with molecular networking for gas chromatography–mass spectrometry data, enabling structured network analysis of deconvolved spectra.: "The method integrates auto-deconvolution with molecular networking for gas chromatography–mass spectrometry data, enabling structured network analysis of deconvolved spectra."
- [other] Load deconvolved spectra output (in format compatible with GNPS_GC input specification). Submit spectra batch to GNPS_GC web service or command-line interface with standard networking parameters. Monitor job status until completion. Retrieve and parse the resulting molecular network file (GraphML or JSON format). Validate network structure (node and edge counts, connectivity metrics).: "Load deconvolved spectra output (in format compatible with GNPS_GC input specification). Submit spectra batch to GNPS_GC web service or command-line interface with standard networking parameters."
- [intro] Auto-deconvolution and molecular networking of gas chromatography–mass spectrometry data: "Auto-deconvolution and molecular networking of gas chromatography–mass spectrometry data"
- [readme] Auto-deconvolution and molecular networking of gas chromatography–mass spectrometry data. _Nature Biotechnology_ (2020): "Auto-deconvolution and molecular networking of gas chromatography–mass spectrometry data"
