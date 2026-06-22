---
name: network-topology-validation
description: Use when after retrieving a molecular network file (GraphML or JSON format) from GNPS_GC following submission of deconvolved GC-MS spectra. Use this skill to confirm the network structure is sound before performing chemical similarity searches, community detection, or annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0593
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

# network-topology-validation

## Summary

Validate the structural integrity and connectivity of a molecular network output from GC-MS deconvolution by checking node and edge counts, connectivity metrics, and GraphML/JSON format compliance. This ensures the network was correctly assembled and is suitable for downstream interpretation.

## When to use

After retrieving a molecular network file (GraphML or JSON format) from GNPS_GC following submission of deconvolved GC-MS spectra. Use this skill to confirm the network structure is sound before performing chemical similarity searches, community detection, or annotation.

## When NOT to use

- Input network is already published or from a trusted, previously validated run with documented topology — skip validation if provenance is known.
- Raw (non-deconvolved) GC-MS spectra are being submitted — this skill applies only to deconvolved output already in GNPS_GC input format.
- Network topology metrics are not relevant to your downstream analysis (e.g., you only need node identities for targeted lookup, not graph structure).

## Inputs

- molecular network file in GraphML format
- molecular network file in JSON format
- deconvolved GC-MS spectra batch metadata (sample count, expected networking parameters)

## Outputs

- validated network topology report (node count, edge count, connectivity metrics)
- flagged anomalies or missing attributes
- confirmed GraphML/JSON structural integrity

## How to apply

Parse the returned molecular network file (GraphML or JSON) and programmatically extract node and edge counts. Compute basic connectivity metrics such as average degree, clustering coefficient, and number of connected components. Compare these metrics against expected ranges for the input spectra batch size (e.g., for N input spectra, expect node count ≥ N if network is fully connected, or identify isolated components). Validate that all nodes have assigned mass-to-charge (m/z) and retention time (RT) attributes, and that edges carry cosine similarity or other spectral similarity scores. Flag any nodes with missing metadata, self-loops, or edges with similarity scores below the submission threshold. Document the network structure before proceeding to interpretation.

## Related tools

- **GNPS_GC** (generates the molecular network (GraphML/JSON) whose topology is validated by this skill) — https://github.com/bittremieux/GNPS_GC

## Evaluation signals

- Node count ≥ number of input deconvolved spectra; edge count > 0 indicating connected spectra pairs.
- All nodes carry valid m/z and retention time attributes; no missing or null metadata fields.
- Network connectivity metrics (average degree, clustering coefficient) are consistent with the input batch size and similarity threshold used during networking.
- GraphML or JSON file parses without schema errors; all edges reference valid source and target nodes.
- No isolated nodes (degree = 0) unless they represent true singletons from the deconvolution; document singletons separately if present.

## Limitations

- This skill validates structure only; it does not assess the chemical accuracy or biological relevance of the network.
- Metric thresholds (e.g., minimum edge count, expected degree range) depend on the deconvolution algorithm and GNPS_GC parameters (cosine threshold, minimum matched peaks) used upstream; no universal cutoffs are provided in the paper.
- Very large networks (>10,000 nodes) may require specialized graph databases or memory-efficient parsing; basic validation scripts may be slow.
- The paper does not specify expected connectivity patterns for different sample types (e.g., complex mixtures vs. standards), so anomalies must be interpreted with domain knowledge.

## Evidence

- [other] Validate network structure (node and edge counts, connectivity metrics).: "Validate network structure (node and edge counts, connectivity metrics)."
- [other] Retrieve and parse the resulting molecular network file (GraphML or JSON format).: "Retrieve and parse the resulting molecular network file (GraphML or JSON format)."
- [other] The method integrates auto-deconvolution with molecular networking for gas chromatography–mass spectrometry data, enabling structured network analysis of deconvolved spectra.: "The method integrates auto-deconvolution with molecular networking for gas chromatography–mass spectrometry data, enabling structured network analysis of deconvolved spectra."
