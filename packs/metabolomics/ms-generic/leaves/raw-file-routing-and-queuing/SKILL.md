---
name: raw-file-routing-and-queuing
description: Use when you have collected raw MS files via an uploader tool and need to automatically forward them to a data processor for proteomics analysis, ensuring format compatibility and maintaining linkage to the original upload session and user project.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - RTKlab-BYU/Raw_File_Uploader
  - Raw_File_Uploader
  - Proteomics_Data_Processor
  - MSConnect
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1021/acs.jproteome.4c00854
  title: MSConnect
evidence_spans:
- The platform is built with Python, Django, JavaScript, and HTML
- works with [Raw file uploader](https://github.com/RTKlab-BYU/Raw_File_Uploader)
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.4c00854
  all_source_dois:
  - 10.1021/acs.jproteome.4c00854
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# raw-file-routing-and-queuing

## Summary

Route raw MS data files from an uploader tool through format validation to a third-party proteomics processor, queuing them for autonomous downstream analysis. This skill ensures that uploaded raw files are correctly matched to compatible processor specifications before dispatch.

## When to use

Apply this skill when you have collected raw MS files via an uploader tool and need to automatically forward them to a data processor for proteomics analysis, ensuring format compatibility and maintaining linkage to the original upload session and user project.

## When NOT to use

- Raw files have already been processed or converted to feature tables
- The Proteomics_Data_Processor tool is not available or incompatible with your raw file format
- You lack metadata or provenance information required to link outputs back to the original upload session

## Inputs

- Raw MS file metadata (filename, upload path, file format)
- Raw MS data files
- Processor tool specifications

## Outputs

- Queued raw file entries
- Processed proteomics output records (feature tables, quantification matrices, mass spectrometry feature lists)
- Metadata-tagged processed records linked to upload session and user project

## How to apply

First, receive raw file metadata (filename, upload path, file format) from the Raw_File_Uploader repository output. Second, validate raw file integrity and format compatibility against the Proteomics_Data_Processor tool specifications to prevent downstream failures. Third, invoke the Proteomics_Data_Processor with the raw file path as input, directing output to the designated processing queue. Fourth, collect and log all processed proteomics output records (feature tables, quantification matrices, mass spectrometry feature lists) returned by the processor. Finally, store processed records with metadata tags linking them back to the original upload session and user project, maintaining traceability throughout the workflow.

## Related tools

- **Raw_File_Uploader** (Source tool providing raw file metadata and upload paths; supplies input to the routing workflow) — https://github.com/RTKlab-BYU/Raw_File_Uploader
- **Proteomics_Data_Processor** (Destination processor tool that receives queued raw files and produces quantification matrices and feature tables) — https://github.com/RTKlab-BYU/Proteomics_Data_Processor
- **MSConnect** (Platform orchestrating the routing and queuing workflow; integrates uploader and processor tools) — https://github.com/RTKlab-BYU/MSConnect

## Evaluation signals

- Raw file metadata (filename, path, format) successfully extracted and parsed from uploader output
- Format validation completes without errors; file format matches Proteomics_Data_Processor specification
- Processor invocation returns non-empty output (feature tables, quantification matrices, or MS feature lists)
- Processed records are tagged with metadata linking them to the original upload session ID and user project identifier
- Queued file entries are logged with timestamps and status tracking, enabling audit trail verification

## Limitations

- MSConnect is not a standalone data analysis tool; it depends on third-party software for data processing and does not come with a data processor or analysis software/license
- Routing assumes the Proteomics_Data_Processor tool is already installed and configured; incompatible file formats or tool unavailability will break the workflow
- Metadata linkage relies on the availability and consistency of upload session identifiers; missing or malformed identifiers will prevent proper traceability
- The workflow requires manual configuration of processing modules and wrapper setup as described in the MSConnect wiki

## Evidence

- [other] How does MSConnect route uploaded raw files to the third-party Processor tool during the data-processing stage?: "How does MSConnect route uploaded raw files to the third-party Processor tool during the data-processing stage?"
- [other] Receive raw file metadata (filename, upload path, file format) from the Raw_File_Uploader repository output. 2. Validate raw file integrity and format compatibility with the Proteomics_Data_Processor tool specifications. 3. Invoke Proteomics_Data_Processor with the raw file path as input, directing output to the designated processing queue.: "Receive raw file metadata (filename, upload path, file format) from the Raw_File_Uploader repository output. Validate raw file integrity and format compatibility with the Proteomics_Data_Processor"
- [other] Collect and log processed proteomics output records (e.g., feature tables, quantification matrices, or mass spectrometry feature lists) returned by the Processor.: "Collect and log processed proteomics output records (e.g., feature tables, quantification matrices, or mass spectrometry feature lists) returned by the Processor."
- [other] Store processed records with metadata tags linking them to the original upload session and user project.: "Store processed records with metadata tags linking them to the original upload session and user project."
- [readme] MSConnect is not a standalone data analysis tool. It depends on third-party software for data processing/analysis: "MSConnect is not a standalone data analysis tool. It depends on third-party software for data processing/analysis"
- [readme] Data Processing: Interfaces with third-party tools to analyze MS raw data.: "Data Processing: Interfaces with third-party tools to analyze MS raw data."
