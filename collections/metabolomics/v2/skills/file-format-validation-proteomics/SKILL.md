---
name: file-format-validation-proteomics
description: Use when when raw MS files are uploaded to MSConnect via the Raw File Uploader and must be verified for compatibility with downstream processing tools (e.g., Proteomics_Data_Processor) before routing to the processing queue.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - JavaScript
  - HTML
  - Raw File Uploader (RTKlab-BYU/Raw_File_Uploader)
  - RTKlab-BYU/Raw_File_Uploader
  - RTKlab-BYU/Proteomics_Data_Processor
  - Raw_File_Uploader
  - Proteomics_Data_Processor
  - MSConnect
derived_from:
- doi: 10.1021/acs.jproteome.4c00854
  title: MSConnect
evidence_spans:
- The platform is built with Python, Django, JavaScript, and HTML
- works with [Raw file uploader]
- works with [Raw file uploader](https://github.com/RTKlab-BYU/Raw_File_Uploader)
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

# file-format-validation-proteomics

## Summary

Validate raw mass spectrometry file formats (.raw, .mzML, .mzXML) and enforce size/integrity constraints before ingestion into the MSConnect platform. This skill ensures only compatible, uncorrupted files enter the data processing pipeline.

## When to use

When raw MS files are uploaded to MSConnect via the Raw File Uploader and must be verified for compatibility with downstream processing tools (e.g., Proteomics_Data_Processor) before routing to the processing queue. Apply this skill immediately after file upload but before invoking third-party processors.

## When NOT to use

- Input is already a processed feature table or quantification matrix (validation applies only to raw MS files)
- Files have already been validated and stored in a designated repository with integrity guarantees
- The processor tool accepts vendor-specific proprietary formats not covered by the whitelist (consult processor documentation first)

## Inputs

- Raw MS file (e.g., .raw, .mzML, .mzXML format)
- File metadata (filename, upload path, file size)
- Processor tool specifications (supported formats, size limits)

## Outputs

- Validation status (success, failure, or pending)
- Validation log entry (format, size, integrity check results)
- File metadata tag linking to original upload session (if valid)

## How to apply

Implement file validation logic that checks (1) file extension against the whitelist of supported MS raw formats (.raw, .mzML, .mzXML); (2) file size against platform constraints; and (3) file integrity by reading headers or checksums to confirm the file is not corrupted. Log all validation outcomes (success/failure/pending) and reject files that fail any check, returning detailed error messages to the user. This validation gates entry into the Proteomics_Data_Processor tool, preventing malformed or incompatible files from consuming processing resources.

## Related tools

- **Raw_File_Uploader** (Accepts and stages raw MS files for validation via HTTP/HTML form interface) — https://github.com/RTKlab-BYU/Raw_File_Uploader
- **Proteomics_Data_Processor** (Downstream consumer of validated raw files; requires format compatibility verification before invocation) — https://github.com/RTKlab-BYU/Proteomics_Data_Processor
- **MSConnect** (Platform orchestrator that routes validated files to the processing queue and logs ingestion outcomes) — https://github.com/RTKlab-BYU/MSConnect

## Evaluation signals

- All uploaded .raw, .mzML, .mzXML files are accepted; all files with incorrect extensions are rejected with error message
- File size violations (e.g., exceeding platform limits) are caught and logged before file storage
- Corrupted or truncated files are detected and rejected; valid files are confirmed readable by header inspection or checksum verification
- Validation status (success/failure/pending) is recorded in upload logs and linked to the original user session and project metadata
- Only validated files are passed to Proteomics_Data_Processor; no unvalidated files enter the processing queue

## Limitations

- Validation logic must be updated if processor tool specifications change (e.g., new supported formats or size constraints); no automatic discovery of processor requirements
- File integrity checks (checksums, header parsing) may fail for partially uploaded or network-interrupted transfers; retry/resume logic is not covered by this skill alone
- Vendor-specific metadata embedded in .raw files (e.g., Thermo Orbitrap-specific fields) is not validated; only format and size are checked
- No validation of scientific metadata (e.g., sample description, instrument configuration) embedded in file headers; only structural validity is confirmed

## Evidence

- [other] Implement file validation logic to verify raw MS file formats (e.g., .raw, .mzML, .mzXML) and enforce size/integrity constraints.: "Implement file validation logic to verify raw MS file formats (e.g., .raw, .mzML, .mzXML) and enforce size/integrity constraints."
- [other] Validate raw file integrity and format compatibility with the Proteomics_Data_Processor tool specifications.: "Validate raw file integrity and format compatibility with the Proteomics_Data_Processor tool specifications."
- [other] Integrate upload status tracking (success/failure/pending) and logging to report ingestion outcomes.: "Integrate upload status tracking (success/failure/pending) and logging to report ingestion outcomes."
- [readme] MSConnect streamlines the entire process from data collection, data management, data processing and to data visualization by integrating and supporting various third-party tools: "MSConnect streamlines the entire process from data collection, data management, data processing and to data visualization by integrating and supporting various third-party tools"
- [readme] The platform is built with Python, Django, JavaScript, and HTML and works with Raw file uploader and Processor: "The platform is built with Python, Django, JavaScript, and HTML and works with Raw file uploader and Processor"
