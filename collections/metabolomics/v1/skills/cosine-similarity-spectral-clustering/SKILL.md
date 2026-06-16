---
name: cosine-similarity-spectral-clustering
description: Use when you have a collection of deconvolved mass spectra (in MGF or mzTab format) from GC-MS analysis and need to group them into a molecular network to identify structural relationships and enable compound annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3932
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - MSHub
  - GNPS
derived_from:
- doi: 10.1038/s41587-020-0700-3
  title: mshub
evidence_spans:
- MSHub auto-deconvolution
- Auto-deconvolution and molecular networking of gas chromatography–mass spectrometry data
- GNPS molecular networking
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mshub
    doi: 10.1038/s41587-020-0700-3
    title: mshub
  dedup_kept_from: coll_mshub
schema_version: 0.2.0
---

# cosine-similarity-spectral-clustering

## Summary

Cluster mass spectra by computing pairwise cosine similarity scores and constructing a molecular network where nodes represent spectra and edges represent similarity above a threshold. This skill is essential for organizing GC-MS deconvolved spectra into groups of structurally related compounds.

## When to use

Apply this skill when you have a collection of deconvolved mass spectra (in MGF or mzTab format) from GC-MS analysis and need to group them into a molecular network to identify structural relationships and enable compound annotation. Specifically use it after auto-deconvolution has separated overlapping chromatographic peaks into individual compound spectra.

## When NOT to use

- Input spectra are raw, overlapping GC-MS chromatographic peaks that have not been deconvolved—apply auto-deconvolution first.
- Spectra are from liquid chromatography–mass spectrometry (LC-MS) data with very high spectral complexity or wide m/z range where cosine similarity alone may be insufficient for reliable clustering.
- A similarity threshold has already been fixed by external constraints (e.g., regulatory or instrument-specific) that differs substantially from the default GNPS parameters.

## Inputs

- deconvolved mass spectra in MGF format
- deconvolved mass spectra in mzTab format
- auto-deconvolution output from MSHub

## Outputs

- molecular network graph (nodes = spectra/compounds, edges = similarity scores)
- network topology visualization
- spectral clustering assignments

## How to apply

Submit deconvolved spectra (exported from MSHub in MGF or mzTab format) to the GNPS molecular networking workflow. The workflow computes all-against-all cosine similarity scores between spectra pairs, clusters spectra based on similarity edges, and constructs a network graph where each node represents a spectrum/compound and each edge represents a similarity score above the default threshold. The topology of the resulting network (node degree, connected components, cluster structure) can then be compared to published reference networks to validate the deconvolution and clustering fidelity.

## Related tools

- **GNPS** (executes molecular networking workflow to cluster deconvolved spectra by cosine similarity and constructs network graph) — https://gnps.ucsd.edu
- **MSHub** (auto-deconvolves overlapping GC-MS chromatographic peaks to produce individual spectra suitable for cosine similarity clustering)

## Evaluation signals

- Network graph successfully generates with nodes corresponding to submitted spectra and edges representing cosine similarity scores
- Network topology matches the published reference network structure (same number of major clusters, similar degree distribution, consistent connected components)
- Deconvolved spectra that should be chemically related cluster together with high similarity scores (cosine > 0.7 or above reported threshold)
- No spurious edges connect spectra from chemically unrelated compounds, indicating appropriate similarity threshold
- Exportable network visualization is generated and can be compared visually to the published network from the associated Nature Biotechnology manuscript

## Limitations

- Cosine similarity depends on spectral peak abundance and m/z accuracy; significant noise, isotope patterns, or fragmentation artifacts in deconvolved spectra can reduce clustering fidelity.
- The skill assumes spectra have been properly deconvolved; remaining co-eluting or partially separated compounds will produce misleading similarity scores and network topology.
- Default GNPS parameters may not be optimal for all GC-MS datasets; network parameters (e.g., cosine threshold, minimum matched peaks) may require tuning depending on the complexity and mass range of the analyzed compound set.

## Evidence

- [other] Upload deconvolved spectra to GNPS and execute molecular networking workflow with default or reported parameters to cluster spectra by cosine similarity and construct the network graph.: "Upload deconvolved spectra to GNPS and execute molecular networking workflow with default or reported parameters to cluster spectra by cosine similarity and construct the network graph."
- [other] Retrieve and visualize the resulting molecular network (nodes = spectra/compounds, edges = similarity scores) and compare topology to the published network.: "Retrieve and visualize the resulting molecular network (nodes = spectra/compounds, edges = similarity scores) and compare topology to the published network."
- [intro] Auto-deconvolution and molecular networking methods for gas chromatography–mass spectrometry data analysis: "Auto-deconvolution and molecular networking methods for gas chromatography–mass spectrometry data analysis"
