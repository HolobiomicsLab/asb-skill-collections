---
name: deconvolved-spectrum-comparison
description: Use when after auto-deconvolution of GC-MS data has produced a table of deconvolved mass spectra, and you need to organize these spectra into clusters or detect which compounds co-elute or share similar fragmentation patterns.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3932
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
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

# deconvolved-spectrum-comparison

## Summary

Compute pairwise cosine similarity scores between deconvolved gas chromatography–mass spectrometry spectra to identify spectral relationships and construct a similarity network. This skill bridges auto-deconvolution output and molecular networking by quantifying spectral resemblance based on normalized m/z and intensity values.

## When to use

After auto-deconvolution of GC-MS data has produced a table of deconvolved mass spectra, and you need to organize these spectra into clusters or detect which compounds co-elute or share similar fragmentation patterns. Apply this skill when the input is a structured deconvolved spectra table (not raw GC-MS chromatograms) and your goal is to build a spectral similarity network rather than perform single-spectrum identification.

## When NOT to use

- Input is raw GC-MS chromatogram data (not yet deconvolved) — apply auto-deconvolution first.
- Spectra are already assigned to known compounds via database matching — use spectral identification instead.
- Goal is to quantify presence/absence of a single target compound across samples — use peak extraction or targeted analysis.

## Inputs

- deconvolved mass spectra table (rows=spectra, columns=m/z and intensity pairs)
- spectrum identifiers (e.g., retention time, compound index)

## Outputs

- pairwise cosine similarity score matrix
- spectral similarity graph (nodes=spectra, edges=similarity relationships)
- connected components and community cluster assignments
- GraphML-formatted network file with cluster membership and spectral metadata
- node-link JSON summary table (spectrum identifiers to cluster assignments and similarity statistics)

## How to apply

Load the deconvolved mass spectra table from the auto-deconvolution output, ensuring each spectrum is represented as a vector of normalized m/z values paired with intensity values. Compute pairwise cosine similarity scores between all deconvolved spectra; the cosine metric quantifies the angle between normalized feature vectors and is robust to intensity scaling. Apply a similarity threshold (e.g., cosine similarity > 0.7) to retain only high-confidence spectral pairs and construct an undirected graph where nodes are spectra and edges represent similarity relationships. Detect connected components and community clusters within this spectral graph using standard graph algorithms. The rationale is that cosine similarity on normalized spectra captures compositional resemblance in fragmentation patterns independent of absolute peak heights, and thresholding filters noise while preserving meaningful chemical relationships.

## Related tools

- **GNPS_GC** (Implements molecular networking for deconvolved GC-MS spectra; provides the repository and workflow for cosine similarity computation, graph construction, and cluster detection) — https://github.com/bittremieux/GNPS_GC

## Evaluation signals

- Cosine similarity matrix is symmetric, with diagonal values ≈ 1.0 (self-similarity).
- Number of connected components and cluster sizes are consistent with known or expected chemical groupings (e.g., isomers, homologs, or co-eluting compounds form tight clusters).
- Nodes in the output graph have degree distribution consistent with input threshold (lower threshold → higher average degree; higher threshold → sparser graph).
- GraphML export is valid XML and contains all expected node attributes (cluster membership, spectrum ID, m/z and intensity vectors).
- Node-link JSON summary table has no missing entries and similarity statistics (min, max, mean) are bounded in [0, 1] and consistent with the underlying score matrix.

## Limitations

- Cosine similarity assumes normalized spectral vectors; unnormalized or raw m/z–intensity pairs may produce misleading results.
- Threshold selection is empirical and data-dependent; no universal 'best' cutoff is provided in the literature; practitioner must validate based on domain knowledge or benchmark data.
- Spectra with very few peaks or highly noisy deconvolution output may form spurious similarities; quality control of deconvolution is assumed upstream.
- Graph-based community detection is sensitive to network density and modularity; dense networks may yield over-fragmented clusters, while sparse networks may lose resolution.

## Evidence

- [other] Compute pairwise cosine similarity scores between all deconvolved spectra using normalized m/z and intensity values.: "Compute pairwise cosine similarity scores between all deconvolved spectra using normalized m/z and intensity values."
- [other] Apply a similarity threshold to retain only high-confidence spectral pairs and construct an undirected graph.: "Apply a similarity threshold to retain only high-confidence spectral pairs and construct an undirected graph."
- [other] Detect connected components and community clusters within the spectral graph.: "Detect connected components and community clusters within the spectral graph."
- [other] Export the molecular network in GraphML format with nodes representing spectra, edges representing similarity relationships, and node attributes containing cluster membership and spectral metadata.: "Export the molecular network in GraphML format with nodes representing spectra, edges representing similarity relationships, and node attributes containing cluster membership and spectral metadata."
- [readme] This is a companion repository to the following manuscript: Aksenov, A.A., Laponogov, I., Zhang, Z. et al. Auto-deconvolution and molecular networking of gas chromatography–mass spectrometry data.: "This is a companion repository to the following manuscript: Aksenov, A.A., Laponogov, I., Zhang, Z. et al. Auto-deconvolution and molecular networking of gas chromatography–mass spectrometry data."
