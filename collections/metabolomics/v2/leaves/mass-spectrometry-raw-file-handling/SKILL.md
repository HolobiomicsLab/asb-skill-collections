---
name: mass-spectrometry-raw-file-handling
description: Use when you have raw MS data files from Thermo Orbitrap or other vendor
  instruments that must be uploaded into a centralized platform for automated processing.
  Use it at the start of a multi-stage omics workflow where data collection, management,
  processing, and visualization are integrated;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - JavaScript
  - HTML
  - Raw File Uploader (RTKlab-BYU/Raw_File_Uploader)
  - Raw File Uploader
  - MSConnect
  - Django
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jproteome.4c00854
  title: MSConnect
evidence_spans:
- The platform is built with Python, Django, JavaScript, and HTML
- works with [Raw file uploader]
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

# mass-spectrometry-raw-file-handling

## Summary

Ingest, validate, and persist mass spectrometry raw files (.raw, .mzML, .mzXML) as the entry point for automated high-throughput omics workflows. This skill establishes the data collection foundation by accepting vendor-specific MS files, enforcing format and integrity constraints, and routing them to a central repository accessible to downstream data management and processing pipelines.

## When to use

Apply this skill when you have raw MS data files from Thermo Orbitrap or other vendor instruments that must be uploaded into a centralized platform for automated processing. Use it at the start of a multi-stage omics workflow where data collection, management, processing, and visualization are integrated; the skill is essential whenever new MS runs need to enter the system as the single authoritative entry point.

## When NOT to use

- Raw files are already stored and indexed in the platform — use this skill only for initial ingestion or new uploads, not for re-processing already-managed files.
- Input files are pre-processed, converted to feature tables, or already aligned to a reference — this skill handles raw MS binary/text formats only, not derived outputs.
- The workflow requires real-time streaming or live instrument data feeds rather than batch file uploads — this skill is designed for file-based ingestion.

## Inputs

- Mass spectrometry raw files in vendor formats (.raw, .mzML, .mzXML)
- File metadata (e.g., sample name, analysis date, instrument ID, experiment context)
- HTTP/HTML form upload interface

## Outputs

- Ingested raw MS files persisted in designated repository
- Validated file metadata indexed in SQL database
- Upload status records (success/failure/pending with timestamps and error logs)
- File integrity checksums or validation state

## How to apply

Design a file upload module (Python/Django HTTP/HTML form interface) that accepts raw MS files and applies validation logic to verify format compliance (.raw, .mzML, .mzXML) and enforce size/integrity constraints before storage. Configure a persistent file storage backend (e.g., designated repository) linked to the data management layer so uploaded files are indexed and tracked. Implement upload status tracking (success/failure/pending) and structured logging to report ingestion outcomes and enable rollback or retry. Test with representative MS raw files from your instrument vendor to confirm files are correctly stored, metadata is recorded, and downstream processing can access them without corruption. The rationale is that MS raw files are immutable source data; validating and centralizing them at ingestion prevents downstream failures and ensures reproducibility.

## Related tools

- **Raw File Uploader** (Desktop application (C#/.NET 4.5.1, Windows) that uploads raw MS files to the platform with metadata; serves as the third-party uploader component integrated by MSConnect) — https://github.com/RTKlab-BYU/Raw_File_Uploader
- **MSConnect** (Web-based orchestration platform (Python, Django, JavaScript, HTML) that integrates file upload ingestion, data management, processing, and visualization as a unified workflow) — https://github.com/RTKlab-BYU/MSConnect
- **Django** (Web framework used to implement the HTTP/HTML form interface and file storage backend for upload handling)
- **Python** (Primary language for implementing file validation logic, storage configuration, and logging infrastructure)

## Evaluation signals

- Uploaded raw files are present in the designated repository and accessible to downstream data management and processing components.
- File validation logs confirm that all uploaded files passed format compliance checks (.raw, .mzML, or .mzXML) and size/integrity constraints; failed uploads are logged with specific error messages.
- SQL database metadata records show that each ingested file has associated sample name, upload timestamp, instrument ID, and validation status.
- Upload status tracking (success/failure/pending) records are correctly recorded and queryable for audit and monitoring.
- Downstream processing pipeline can successfully read and parse the stored raw files without corruption or access errors; spot-check by comparing file checksums or re-opening in vendor software.

## Limitations

- The Raw File Uploader component is Windows-only (.NET 4.5.1 desktop application), so users on Linux/macOS must either use an alternative upload path or access upload functionality via the MSConnect web interface.
- File format validation is restrictive to .raw, .mzML, .mzXML; vendor-specific or emerging formats not in this list will be rejected and require manual configuration or extension.
- The skill depends on third-party tools (Raw File Uploader, Proteomics Data Processor) which are not included with MSConnect and may have separate licensing requirements; users must verify licensing compliance.
- No changelog is available for the Raw File Uploader repository, so version history and breaking changes are not documented; updates should be tested thoroughly before production deployment.

## Evidence

- [other] Design the Raw File Uploader module using Python and Django to accept file uploads via HTTP/HTML form interface. Implement file validation logic to verify raw MS file formats (e.g., .raw, .mzML, .mzXML) and enforce size/integrity constraints.: "Design the Raw File Uploader module using Python and Django to accept file uploads via HTTP/HTML form interface. Implement file validation logic to verify raw MS file formats (e.g., .raw, .mzML,"
- [other] MSConnect works with the Raw File Uploader component to enable the data collection entry point, integrating this third-party tool to support automated high-throughput MS-based omics workflows that streamline the process from data collection onward.: "MSConnect works with the Raw File Uploader component to enable the data collection entry point, integrating this third-party tool to support automated high-throughput MS-based omics workflows"
- [other] Configure file storage backend to persist uploaded raw files in a designated repository accessible to the MSConnect data management layer. Integrate upload status tracking (success/failure/pending) and logging to report ingestion outcomes.: "Configure file storage backend to persist uploaded raw files in a designated repository accessible to the MSConnect data management layer. Integrate upload status tracking (success/failure/pending)"
- [readme] Raw file uploader is a upload tool to be used with Proteomics Data Manager for uploading raw files to the database with Meta data about the analysis.: "Raw file uploader is a upload tool to be used with Proteomics Data Manager for uploading raw files to the database with Meta data about the analysis."
- [readme] The platform is built with Python, Django, JavaScript, and HTML and works with Raw file uploader and Processor.: "The platform is built with Python, Django, JavaScript, and HTML and works with Raw file uploader and Processor."
