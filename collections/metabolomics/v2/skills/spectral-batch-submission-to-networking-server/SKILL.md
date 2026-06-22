---
name: spectral-batch-submission-to-networking-server
description: Use when you have deconvolved GC-MS spectra in GNPS_GC input-compatible format and want to construct a molecular network to identify relationships between unknown compounds and perform structured chemical similarity analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - GNPS_GC
  techniques:
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-batch-submission-to-networking-server

## Summary

Submit a batch of deconvolved gas chromatography–mass spectrometry spectra to the GNPS_GC web service or command-line interface to generate a molecular network. This skill bridges auto-deconvolved spectra and structured network analysis by orchestrating remote or local job submission, monitoring, and retrieval of GraphML/JSON network outputs.

## When to use

You have deconvolved GC-MS spectra in GNPS_GC input-compatible format and want to construct a molecular network to identify relationships between unknown compounds and perform structured chemical similarity analysis. Use this when you need to process multiple spectra together rather than analyze single spectra in isolation.

## When NOT to use

- Input spectra have not been deconvolved or are in a format incompatible with GNPS_GC input specification
- You require real-time interactive visualization or parameter tuning during the networking step rather than batch processing
- Your analysis goal is limited to pairwise spectral similarity scoring and does not require network topology or graph-based structural analysis

## Inputs

- deconvolved GC-MS spectra in GNPS_GC input format
- networking parameters (cosine similarity threshold, mass tolerance)
- spectra batch manifest or directory

## Outputs

- molecular network file (GraphML or JSON format)
- job status/log information
- network statistics (node count, edge count, connectivity metrics)

## How to apply

Load deconvolved spectra output formatted according to the GNPS_GC input specification. Submit the spectra batch to the GNPS_GC web service or command-line interface, supplying standard networking parameters (e.g., minimum cosine similarity threshold, precursor mass tolerance). Monitor job status until completion via the service's status endpoint or CLI output. Once the job finishes, retrieve and parse the resulting molecular network file in GraphML or JSON format. Validate the network structure by checking node counts, edge counts, and connectivity metrics to confirm the networking step completed successfully and produced expected network density.

## Related tools

- **GNPS_GC** (web service or command-line interface that accepts deconvolved GC-MS spectra and produces molecular network output in GraphML or JSON format) — https://github.com/bittremieux/GNPS_GC

## Evaluation signals

- Job submission is accepted by the GNPS_GC service without validation errors on input format
- Job completes with non-error exit code and produces a network file with non-zero node and edge counts
- Retrieved network file parses successfully as valid GraphML or JSON with expected schema (contains node, edge, and attribute elements)
- Network connectivity metrics (e.g., number of connected components, average degree) are within expected ranges for the input spectra size and similarity threshold used
- Network node identifiers correspond to input spectrum IDs and edge weights reflect cosine similarity or other scoring metric specified in submission parameters

## Limitations

- Network quality and density depend critically on the quality of the upstream deconvolution step; poor deconvolution produces fragmented networks with spurious nodes
- The GNPS_GC service imposes timeout and memory constraints on batch size; very large spectra batches may require splitting and iterative submission
- The molecular network output format (GraphML vs. JSON) may require conversion or re-parsing depending on downstream visualization or analysis tools
- No built-in handling of batch resubmission or resumption; failed jobs must be resubmitted from scratch

## Evidence

- [other] Submit spectra batch to GNPS_GC web service or command-line interface with standard networking parameters: "Submit spectra batch to GNPS_GC web service or command-line interface with standard networking parameters."
- [other] Retrieve and parse the resulting molecular network file (GraphML or JSON format): "Retrieve and parse the resulting molecular network file (GraphML or JSON format)."
- [other] Validate network structure (node and edge counts, connectivity metrics): "Validate network structure (node and edge counts, connectivity metrics)."
- [intro] The method integrates auto-deconvolution with molecular networking for gas chromatography–mass spectrometry data: "The method integrates auto-deconvolution with molecular networking for gas chromatography–mass spectrometry data"
