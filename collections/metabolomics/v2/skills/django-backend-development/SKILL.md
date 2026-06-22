---
name: django-backend-development
description: Use when you need to build a web-based data ingestion layer that accepts raw MS files (.raw, .mzML, .mzXML) from users, validates them before storage, and tracks their processing status through a data management pipeline.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - Django
  - JavaScript
  - HTML
  - Raw File Uploader
derived_from:
- doi: 10.1021/acs.jproteome.4c00854
  title: MSConnect
evidence_spans:
- The platform is built with Python, Django, JavaScript, and HTML
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

# django-backend-development

## Summary

Design and implement a Django web backend to accept file uploads via HTTP/HTML forms, validate incoming data against schema constraints, persist files to a configured storage backend, and expose status tracking and logging for asynchronous ingestion workflows. This skill is essential for building entry-point data collection layers in high-throughput omics platforms that integrate third-party command-line or desktop analysis tools.

## When to use

You need to build a web-based data ingestion layer that accepts raw MS files (.raw, .mzML, .mzXML) from users, validates them before storage, and tracks their processing status through a data management pipeline. Use this skill when your platform must provide an HTTP/HTML upload interface as the entry point for automated, vendor-agnostic omics workflows that will later hand off files to external processors.

## When NOT to use

- Input files are already validated and stored in a repository — use this skill only to build the ingestion layer itself, not to re-ingest already-managed files.
- Your platform does not require user-facing file upload; instead, files are delivered directly by automated instruments or pre-processed data feeds.
- You are building a desktop application (not web-based) — the article explicitly states MSConnect is web-based and requires server deployment.

## Inputs

- Multipart HTTP POST request with raw MS file attachment (.raw, .mzML, .mzXML format)
- HTML form definition specifying allowed file types and size limits
- Storage backend configuration (filesystem path or cloud credentials)

## Outputs

- Persisted raw MS file in designated repository
- Upload metadata record (filename, size, format, timestamp, user)
- Status record (success/failure/pending) with error details if applicable
- Ingestion event log entries for audit and debugging

## How to apply

Create a Django application with an HTTP/HTML form endpoint that accepts multipart file uploads. Implement file validation logic to check against allowed formats (.raw, .mzML, .mzXML) and enforce size and integrity constraints before writing to disk. Configure a file storage backend (e.g., local filesystem or cloud storage) to persist validated files in a designated repository accessible to downstream data management and processing layers. Integrate upload status tracking (success/failure/pending states) with logging to record metadata about each ingestion event. Test the module end-to-end using representative MS raw files to confirm files are correctly persisted, metadata is recorded in a database, and status transitions are properly logged.

## Related tools

- **Python** (Primary language for implementing validation logic, file I/O, and status tracking)
- **Django** (Web framework providing HTTP request handling, form processing, ORM for metadata storage, and middleware for authentication)
- **JavaScript** (Client-side form submission and upload progress feedback)
- **HTML** (Form template defining file input elements and submission endpoint)
- **Raw File Uploader** (Third-party desktop/C# tool that MSConnect's Django backend receives output from or integrates with; may also serve as reference architecture for validation rules) — https://github.com/RTKlab-BYU/Raw_File_Uploader

## Evaluation signals

- Files uploaded via HTTP form are correctly persisted to the configured storage backend with intact binary content (verify via file hash or byte count).
- Validation rejects files with unsupported extensions, oversized payloads, or corrupted headers with appropriate HTTP 400 error and logged reason.
- Upload metadata (filename, size, format, timestamp, user ID) is recorded in the database and queryable by downstream components.
- Status transitions (pending → success or pending → failure) are logged with timestamps and any error messages; logs are machine-parseable for monitoring.
- End-to-end test with representative .raw, .mzML, .mzXML files confirms files are retrievable by the data management layer and processing pipeline.

## Limitations

- The skill does not cover the design of the data processing pipeline itself; it only handles ingestion and metadata recording.
- File size and format validation constraints must be configured per deployment; the skill does not provide platform-independent defaults.
- Asynchronous processing and error recovery (e.g., retry logic for failed uploads) are not addressed; logging and status tracking must be integrated with a task queue if autonomous reprocessing is required.
- The article does not specify concurrency limits, quota enforcement, or multi-tenant isolation; these must be added separately depending on deployment scale.

## Evidence

- [other] Design the Raw File Uploader module using Python and Django to accept file uploads via HTTP/HTML form interface.: "Design the Raw File Uploader module using Python and Django to accept file uploads via HTTP/HTML form interface"
- [other] Implement file validation logic to verify raw MS file formats (e.g., .raw, .mzML, .mzXML) and enforce size/integrity constraints.: "Implement file validation logic to verify raw MS file formats (e.g., .raw, .mzML, .mzXML) and enforce size/integrity constraints"
- [other] Configure file storage backend to persist uploaded raw files in a designated repository accessible to the MSConnect data management layer.: "Configure file storage backend to persist uploaded raw files in a designated repository accessible to the MSConnect data management layer"
- [other] Integrate upload status tracking (success/failure/pending) and logging to report ingestion outcomes.: "Integrate upload status tracking (success/failure/pending) and logging to report ingestion outcomes"
- [readme] The platform is built with Python, Django, JavaScript, and HTML: "The platform is built with Python, Django, JavaScript, and HTML"
- [readme] streamlines the entire process from data collection, data management, data processing and to data visualization by integrating and supporting various third-party tools: "streamlines the entire process from data collection, data management, data processing and to data visualization by integrating and supporting various third-party tools"
