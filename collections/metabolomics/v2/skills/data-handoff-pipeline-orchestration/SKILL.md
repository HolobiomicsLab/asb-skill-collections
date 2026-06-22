---
name: data-handoff-pipeline-orchestration
description: 'Use when you have raw MS files (with associated metadata: filename, upload path, file format) staged in an uploader repository and need to route them to a proteomics processor for analysis while preserving audit trails and ensuring format compatibility before processing begins.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3937
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - RTKlab-BYU/Proteomics_Data_Processor
  - Raw_File_Uploader
  - Proteomics_Data_Processor
  - MSConnect
derived_from:
- doi: 10.1021/acs.jproteome.4c00854
  title: MSConnect
evidence_spans:
- The platform is built with Python, Django, JavaScript, and HTML
- works with [Processor](https://github.com/RTKlab-BYU/Proteomics_Data_Processor)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_msconnect_cq
    doi: 10.1021/acs.jproteome.4c00854
    title: MSConnect
  dedup_kept_from: coll_msconnect_cq
schema_version: 0.2.0
---

# data-handoff-pipeline-orchestration

## Summary

Orchestrate the handoff of raw mass spectrometry files from an upload repository through validation and into a third-party processing tool, maintaining metadata provenance and linking output back to the original collection session. This skill implements the critical juncture in an autonomous omics workflow where data transitions from storage to active analysis.

## When to use

Use this skill when you have raw MS files (with associated metadata: filename, upload path, file format) staged in an uploader repository and need to route them to a proteomics processor for analysis while preserving audit trails and ensuring format compatibility before processing begins.

## When NOT to use

- Input files are already processed or in final visualization format (feature tables, plots); skip to visualization workflow step.
- Processing tool is unavailable or incompatible with input file format; validate processor availability and format support before invoking this skill.
- Metadata from upload session has been lost or cannot be retrieved; handoff traceability requires linking results back to collection context.

## Inputs

- raw file metadata object (filename, upload path, file format)
- raw MS file binary or path reference
- processor tool specification/configuration
- upload session identifier
- user project identifier

## Outputs

- processed proteomics records (feature tables, quantification matrices, MS feature lists)
- processing output logs
- metadata-tagged result records linked to original upload session
- processing queue entry or result handle

## How to apply

Retrieve raw file metadata (filename, upload path, file format) from the Raw_File_Uploader repository output. Validate raw file integrity and confirm format compatibility against the target processor's specifications (e.g., Proteomics_Data_Processor tool requirements). Construct and invoke the processor with the validated raw file path as input, directing processed output to a designated queue. Collect and log the processor's output records (e.g., feature tables, quantification matrices, mass spectrometry feature lists) and store them with metadata tags linking each result back to the original upload session and user project. This ensures traceability through the processing pipeline and enables recovery or re-analysis if needed.

## Related tools

- **Raw_File_Uploader** (source repository providing raw file metadata and path references; supplies validated raw files for handoff to processor) — https://github.com/RTKlab-BYU/Raw_File_Uploader
- **Proteomics_Data_Processor** (target processor tool invoked with validated raw file path; produces quantified features and MS data summaries) — https://github.com/RTKlab-BYU/Proteomics_Data_Processor
- **MSConnect** (orchestration platform that manages the handoff workflow, integrates uploader and processor, maintains metadata linking, and routes outputs to visualization) — https://github.com/RTKlab-BYU/MSConnect

## Evaluation signals

- Raw file metadata (filename, path, format) is successfully retrieved from Raw_File_Uploader output and matches input specification.
- File format validation passes: uploaded file format is confirmed compatible with Proteomics_Data_Processor specifications before invocation.
- Processor is invoked with correct raw file path and output is directed to designated processing queue without errors.
- Output records (feature tables, quantification matrices) are collected and stored with metadata tags that explicitly link back to the original upload session ID and user project ID.
- Audit log entries record each transition step (retrieval, validation, invocation, collection) with timestamps and identifiers enabling traceability.

## Limitations

- Handoff assumes Raw_File_Uploader and Proteomics_Data_Processor are deployed and accessible; network/availability failures will block the pipeline.
- Format validation depends on accurate processor specifications being available; mismatches in format expectations may cause silent failures or corrupted output.
- Metadata preservation relies on consistent tagging conventions; schema mismatches or missing session IDs will break traceability and prevent result linkage.
- MSConnect does not include third-party processor software or licenses; licensing requirements must be consulted with processor owners and configured separately.

## Evidence

- [other] retrieval_and_validation: "Receive raw file metadata (filename, upload path, file format) from the Raw_File_Uploader repository output. Validate raw file integrity and format compatibility with the Proteomics_Data_Processor"
- [other] invocation_and_collection: "Invoke Proteomics_Data_Processor with the raw file path as input, directing output to the designated processing queue. Collect and log processed proteomics output records (e.g., feature tables,"
- [other] metadata_tagging_and_storage: "Store processed records with metadata tags linking them to the original upload session and user project."
- [readme] platform_integration: "MSConnect streamlines the entire process from data collection, data management, data processing and to data visualization by integrating and supporting various third-party tools, allowing for a fully"
- [readme] third_party_dependency: "MSConnect does not come with any data processor or analysis software/license, it provides a wrapper/interface to interact with them."
