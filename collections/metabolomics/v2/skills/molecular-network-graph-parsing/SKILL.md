---
name: molecular-network-graph-parsing
description: Use when after GNPS_GC molecular networking job completion, when you have retrieved raw network output files and need to extract, validate, and structure the network topology for further metabolite assignment, comparative network analysis, or visualization.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3359
  edam_topics:
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

# molecular-network-graph-parsing

## Summary

Parse and validate molecular network output files (GraphML or JSON format) produced by GNPS_GC to extract node and edge structures, connectivity metrics, and network topology for downstream analysis. This skill ensures the network graph is well-formed and interpretable before downstream metabolite annotation or cluster analysis.

## When to use

After GNPS_GC molecular networking job completion, when you have retrieved raw network output files and need to extract, validate, and structure the network topology for further metabolite assignment, comparative network analysis, or visualization. Use this skill when you need to verify network construction succeeded (check node/edge counts and connectivity) before committing to downstream interpretation.

## When NOT to use

- Input is raw (non-deconvolved) GC-MS spectra; use deconvolution and networking submission first.
- Network output file is missing or network job failed; retrieve job logs and resubmit.
- You need to perform *de novo* molecular networking (not just parse an existing result); use GNPS_GC submission skill instead.

## Inputs

- GNPS_GC molecular network file (GraphML format)
- GNPS_GC molecular network file (JSON format)
- Deconvolved GC-MS spectra batch metadata (sample identifiers, retention times, m/z values)

## Outputs

- Parsed network graph object (nodes, edges, attributes)
- Network topology metrics (node count, edge count, connectivity statistics)
- Validation report (format compatibility, schema compliance, structural integrity)
- Network adjacency data structure suitable for downstream clustering or annotation

## How to apply

Load the molecular network file output by GNPS_GC in GraphML or JSON format. Parse the graph structure to extract node identifiers (corresponding to deconvolved mass spectra), edge lists (molecular similarities or networking links), and associated node/edge attributes (e.g., m/z, retention time, cosine similarity scores). Validate the network by checking that node and edge counts are non-zero and consistent with the submitted spectra batch, verify connectivity metrics (e.g., connected components, degree distribution) to detect fragmentation or anomalies in the networking step, and confirm that all nodes are assigned unique identifiers and edge weights fall within the expected similarity range (typically 0–1 for cosine similarity). This structured validation step ensures the deconvolution and networking pipeline executed correctly before you interpret the network clusters.

## Related tools

- **GNPS_GC** (Produces deconvolved GC-MS spectra and molecular network output files in GraphML/JSON format; this skill parses and validates those outputs.) — https://github.com/bittremieux/GNPS_GC

## Evaluation signals

- Network file parses without schema errors; GraphML or JSON is well-formed and all required fields (node IDs, edge sources/targets, similarity scores) are present.
- Node count matches or is slightly less than the number of input deconvolved spectra (expected loss due to low-abundance or singleton spectra being filtered).
- Edge weights (e.g., cosine similarity) fall within the expected range (0–1) and are consistent with the networking parameters used in GNPS_GC submission.
- Connectivity metrics (e.g., average node degree, connected component sizes) show a realistic distribution; isolated nodes and large clusters are both present and proportional to the data complexity.
- All nodes have associated metadata (m/z, retention time, spectrum count); all edges have associated weight/similarity scores and source–target identifiers are resolvable to node IDs.

## Limitations

- Parsing and validation only confirm structural integrity; they do not assess the biochemical correctness of the network—i.e., whether the deconvolution or networking parameters were appropriate for the sample composition.
- GraphML and JSON are supported formats; other output formats may not be compatible without conversion.
- Network validation depends on submission metadata; if the original spectra batch was poorly quality-controlled, the resulting network may be valid but of low analytical value.
- Large networks (>10,000 nodes) may require streaming or chunked parsing depending on available memory; standard tools may encounter performance bottlenecks.

## Evidence

- [other] Retrieve and parse the resulting molecular network file (GraphML or JSON format).: "Retrieve and parse the resulting molecular network file (GraphML or JSON format). 5. Validate network structure (node and edge counts, connectivity metrics)."
- [other] Validate network structure (node and edge counts, connectivity metrics).: "4. Retrieve and parse the resulting molecular network file (GraphML or JSON format). 5. Validate network structure (node and edge counts, connectivity metrics)."
- [other] The method integrates auto-deconvolution with molecular networking for gas chromatography–mass spectrometry data, enabling structured network analysis of deconvolved spectra.: "The method integrates auto-deconvolution with molecular networking for gas chromatography–mass spectrometry data, enabling structured network analysis of deconvolved spectra."
