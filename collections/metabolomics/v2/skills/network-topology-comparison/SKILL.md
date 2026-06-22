---
name: network-topology-comparison
description: Use when after executing a molecular networking workflow on GC-MS data that has been processed through auto-deconvolution, and a published reference network exists from a prior analysis of the same or analogous dataset.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3439
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - MSHub
  - GNPS
  - bittremieux/GNPS_GC
  techniques:
  - LC-MS
  - GC-MS
derived_from:
- doi: 10.1038/s41587-020-0700-3
  title: mshub
evidence_spans:
- MSHub auto-deconvolution
- Auto-deconvolution and molecular networking of gas chromatography–mass spectrometry data
- GNPS molecular networking
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

# network-topology-comparison

## Summary

Compare the topology of a newly constructed molecular network against a published reference network to validate that an auto-deconvolution and molecular networking workflow has been successfully reproduced. This skill assesses whether nodes (spectra/compounds), edges (similarity scores), and overall network structure match the reported results.

## When to use

After executing a molecular networking workflow on GC-MS data that has been processed through auto-deconvolution, and a published reference network exists from a prior analysis of the same or analogous dataset. Use this skill to validate reproducibility and to detect deviations caused by parameter changes, software updates, or algorithmic differences.

## When NOT to use

- The new network was constructed with significantly different preprocessing parameters (e.g., different deconvolution settings, retention time alignment, or ionization mode) and no published network from equivalent parameters exists for comparison.
- No reference network or published topology description is available, making validation against ground truth impossible.
- Input data are from a different instrument type, ionization method, or chemical domain (e.g., comparing GC-MS to LC-MS networks), as network topology is instrument- and chemistry-dependent.

## Inputs

- newly constructed molecular network (node/edge list or GraphML format)
- published reference molecular network in compatible format
- deconvolved GC-MS spectra (MGF or mzTab) used to construct the new network
- metadata associating nodes to compounds of interest (optional)

## Outputs

- topology comparison report (node count, edge count, degree distribution, clustering metrics)
- visual network overlay or alignment highlighting concordant vs. discordant regions
- list of preserved vs. lost edges and nodes relative to reference
- parametric deviation summary (e.g., cosine similarity threshold changes)

## How to apply

Obtain both the newly constructed molecular network and the published reference network in a comparable format (e.g., GraphML, GXF, or as node/edge tables). Extract and compare key topological features: (1) node count (deconvolved spectra/compounds), (2) edge count and edge weight distribution (cosine similarity scores), (3) degree distribution and clustering coefficient, and (4) major connected components or hub nodes. Perform visual alignment of network layouts and spot-check that high-confidence matches (e.g., known standards or unique molecular ions) occupy analogous positions in both networks. Document any systematic shifts in cosine similarity thresholds or edge-filtering parameters that might explain topology discrepancies. Success is indicated by concordance in the set of dominant clusters and preservation of key biochemical relationships (e.g., homolog families, related lipids).

## Related tools

- **GNPS** (Executes molecular networking workflow to construct the network graph from deconvolved spectra; provides node and edge outputs for topology comparison) — https://gnps.ucsd.edu
- **MSHub** (Performs auto-deconvolution of overlapping GC-MS chromatographic peaks to generate individual compound spectra that serve as input to GNPS)
- **bittremieux/GNPS_GC** (Companion repository enabling re-execution of the published auto-deconvolution and molecular networking workflow on the deposited GC-MS dataset for topology validation) — https://github.com/bittremieux/GNPS_GC

## Evaluation signals

- Node count in reconstructed network matches published network (±5% tolerance for minor deconvolution variations)
- Edge count and cumulative cosine similarity score distribution are concordant within expected bounds
- Major network clusters (connected components with >5 nodes) are preserved and occupy analogous topological positions
- Known reference compounds (e.g., standards or uniquely annotated ions) cluster together in both networks
- No systematic offset or scaling artifact in cosine similarity edge weights relative to published network

## Limitations

- Network topology is sensitive to cosine similarity threshold and spectral processing parameters; comparison requires documentation of exact parameters used in both the published and reconstructed workflows.
- GC-MS deconvolution quality depends on peak separation and baseline resolution; poor chromatographic resolution can produce spurious nodes and edges not present in the reference.
- Molecular networking relies on spectral similarity, which may not capture structural relationships; isomers and regiomers with similar fragmentation patterns will appear closely connected regardless of true chemical relatedness.
- Visual or automated topology comparison can be ambiguous if network layouts are rendered with different algorithms; direct comparison of adjacency matrices or degree distributions is more robust than visual inspection alone.

## Evidence

- [other] Retrieve and visualize the resulting molecular network (nodes = spectra/compounds, edges = similarity scores) and compare topology to the published network.: "Retrieve and visualize the resulting molecular network (nodes = spectra/compounds, edges = similarity scores) and compare topology to the published network."
- [other] A companion repository (bittremieux/GNPS_GC) has been established to enable re-execution of the auto-deconvolution and molecular networking workflow on the deposited GC-MS dataset associated with the Nature Biotechnology 2020 publication.: "A companion repository (bittremieux/GNPS_GC) has been established to enable re-execution of the auto-deconvolution and molecular networking workflow on the deposited GC-MS dataset"
- [other] Upload deconvolved spectra to GNPS and execute molecular networking workflow with default or reported parameters to cluster spectra by cosine similarity and construct the network graph.: "execute molecular networking workflow with default or reported parameters to cluster spectra by cosine similarity and construct the network graph"
