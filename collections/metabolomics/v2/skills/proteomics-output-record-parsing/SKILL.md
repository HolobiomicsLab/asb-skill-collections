---
name: proteomics-output-record-parsing
description: Use when after the Proteomics_Data_Processor tool has completed analysis of raw mass spectrometry files and returned structured output records.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - RTKlab-BYU/Proteomics_Data_Processor
  - Proteomics_Data_Processor
  - Raw_File_Uploader
  - MSConnect (Django + Python + SQL database)
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

# proteomics-output-record-parsing

## Summary

Parse and collect processed proteomics output records (feature tables, quantification matrices, mass spectrometry feature lists) returned by the Proteomics_Data_Processor tool, then associate them with metadata tags linking to the original upload session and user project. This skill bridges the processor's raw output to persistent, queryable storage within the MSConnect platform.

## When to use

After the Proteomics_Data_Processor tool has completed analysis of raw mass spectrometry files and returned structured output records. Specifically, use this skill when you need to capture processor outputs (feature tables, quantification matrices, or MS feature lists), validate their schema and integrity, and store them with provenance metadata so they remain traceable to the original data collection event and user project.

## When NOT to use

- Input is raw, unprocessed mass spectrometry data (e.g., .raw or .mzML files) — use Raw_File_Uploader intake instead.
- Processor tool has not yet completed execution or output queue is empty — wait for processor completion.
- Output records do not conform to expected proteomics data structures (e.g., malformed tables, missing quantification values) — validate and debug processor configuration first.

## Inputs

- Proteomics_Data_Processor output records (feature tables, quantification matrices, mass spectrometry feature lists)
- Raw file metadata (filename, upload path, file format, upload session ID)
- User project identifier
- Processing session identifier

## Outputs

- Parsed and tagged proteomics output records stored in MSConnect SQL database
- Metadata-linked data structures (records with session, project, and file provenance)
- Queryable proteomics results accessible via web interface or programmatic API

## How to apply

Receive the structured output from the Proteomics_Data_Processor (e.g., feature tables or quantification matrices) from the designated processing queue. Parse each output record to extract its schema, dimensionality, and data type (e.g., numerical matrix, feature annotation table). Validate that the parsed structure matches the expected format for the processor module in use. Extract or construct metadata tags that include: the original raw file name and upload path (from the Raw_File_Uploader metadata), the processing session identifier, and the user project identifier. Append these metadata tags as linked attributes to each output record. Store the tagged records in the MSConnect SQL database using the linked data structure, ensuring they remain queryable by session, project, file, or analysis type via the web interface or programmatic API.

## Related tools

- **Proteomics_Data_Processor** (Generates proteomics output records (feature tables, quantification matrices, MS feature lists) that are parsed and stored by this skill) — https://github.com/RTKlab-BYU/Proteomics_Data_Processor
- **Raw_File_Uploader** (Provides raw file metadata (filename, upload path, file format) that is linked to parsed processor outputs for provenance tracking) — https://github.com/RTKlab-BYU/Raw_File_Uploader
- **MSConnect (Django + Python + SQL database)** (Hosts the linked data structure and SQL database where parsed and tagged proteomics records are persisted and made queryable via web interface or Django REST API) — https://github.com/RTKlab-BYU/MSConnect

## Evaluation signals

- Parsed output records can be retrieved from the MSConnect SQL database by session ID, project ID, or original raw file name without data loss or corruption.
- Each parsed record contains a complete quantification matrix or feature table with expected dimensionality (rows = features/peptides, columns = samples) and numerical values in appropriate ranges for the instrument type.
- Metadata tags on each record correctly reference the original upload session and raw file path, enabling full traceability back to the source data and user project.
- Records are queryable via the web interface or programmatic API (Django REST framework or Jupyter Notebook) and return results consistent with the input processor output.
- No duplicate or orphaned records exist in storage; all parsed outputs are linked to valid upload session and project identifiers.

## Limitations

- MSConnect does not include third-party processor software or licenses; the Proteomics_Data_Processor must be separately installed, configured, and licensed by the user.
- Parsing logic is dependent on the output schema defined by the specific processor module in use; schema changes or custom processor implementations may require updates to the parsing logic.
- The skill assumes the Proteomics_Data_Processor has successfully completed and produced valid output; malformed, partial, or error outputs from the processor will not be parsed correctly.
- SQL database linked data structure requires proper server setup and maintenance; no changelog is documented for the platform, so version compatibility and data migration pathways are not formally specified.

## Evidence

- [other] Workflow step 4 and storage requirement: "Collect and log processed proteomics output records (e.g., feature tables, quantification matrices, or mass spectrometry feature lists) returned by the Processor. Store processed records with"
- [readme] Platform data structure and queryability: "A SQL database linked data structure that allows users to search data and files through a web interface or programmatically."
- [readme] Third-party integration and wrapper role: "MSConnect does not come with any data processor or analysis software/license, it provides a wrapper/interface to interact with them."
- [other] Input metadata from Raw_File_Uploader: "Receive raw file metadata (filename, upload path, file format) from the Raw_File_Uploader repository output."
