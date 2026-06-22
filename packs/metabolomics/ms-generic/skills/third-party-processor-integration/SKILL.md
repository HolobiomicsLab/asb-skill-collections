---
name: third-party-processor-integration
description: Use when when you have raw MS files (e.g., .raw, vendor-specific formats) stored in a centralized repository and need to invoke a third-party proteomics analysis tool—such as a mass spectrometry feature detector or quantification engine—without manually managing file transfers or output.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3644
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - RTKlab-BYU/Proteomics_Data_Processor
  - Raw_File_Uploader
  - Proteomics_Data_Processor
  - MSConnect
  - Django REST framework
  techniques:
  - mass-spectrometry
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

# third-party-processor-integration

## Summary

Integrate vendor-specific or third-party proteomics data processors into an automated workflow by routing validated raw MS files through external analysis tools and collecting their structured outputs (e.g., feature tables, quantification matrices) back into a centralized repository. This skill enables autonomous end-to-end data processing while maintaining provenance and metadata linkage to the original upload session.

## When to use

When you have raw MS files (e.g., .raw, vendor-specific formats) stored in a centralized repository and need to invoke a third-party proteomics analysis tool—such as a mass spectrometry feature detector or quantification engine—without manually managing file transfers or output consolidation. Use this skill when your workflow requires vendor-independent, repeatable processing with automatic backup, logging, and result indexing.

## When NOT to use

- Raw MS files are already processed (e.g., already converted to mzML or feature tables); invoking a Processor tool a second time risks data loss or incorrect re-normalization.
- The third-party Processor tool is not installed, licensed, or accessible; MSConnect provides the wrapper only and does not include or license third-party software.
- File format validation fails or raw file integrity is compromised; do not attempt to force processing of corrupted or incompatible files.

## Inputs

- raw MS file (vendor-specific format: .raw, .d, .ms, etc.)
- raw file metadata (filename, upload path, file format)
- Processor tool specification (supported formats, I/O schema)
- processing queue or output directory path

## Outputs

- processed proteomics data records (feature tables, quantification matrices)
- mass spectrometry feature lists
- processing logs (timestamps, module version, error states)
- metadata-tagged database records (linked to upload session and user project)

## How to apply

First, receive raw file metadata (filename, upload path, file format) from your file uploader repository output. Validate that the raw file format and integrity match the third-party Processor tool's specifications (e.g., supported vendors, file size, integrity checksums). Invoke the Processor tool programmatically, passing the raw file path as input and specifying the output queue or target directory. Collect and log all processed records returned by the Processor (e.g., feature tables, quantification matrices, mass spectrometry feature lists) along with processing timestamps and error states. Finally, store processed records in your database with metadata tags that link them back to the original upload session, user project, and processing module version, enabling full traceability and re-processing if needed.

## Related tools

- **Raw_File_Uploader** (Source repository: delivers raw file metadata and file paths to the Processor integration workflow) — https://github.com/RTKlab-BYU/Raw_File_Uploader
- **Proteomics_Data_Processor** (Third-party analysis engine: accepts raw file paths, performs MS data analysis, returns feature tables and quantification matrices) — https://github.com/RTKlab-BYU/Proteomics_Data_Processor
- **MSConnect** (Orchestration platform: wraps and invokes the Processor tool, manages file routing, metadata tagging, and result storage) — https://github.com/RTKlab-BYU/MSConnect
- **Django REST framework** (API layer for programmatic invocation of Processor workflows and result queries)

## Evaluation signals

- Processed output records are present in the database with expected schema (e.g., feature tables contain m/z, retention time, intensity columns; quantification matrices have sample × feature dimensions).
- Metadata tags correctly link processed records back to the original raw file upload session ID and user project; traceability chain is unbroken.
- Processing logs record the Processor module version, invocation timestamp, and any error/warning states; re-processing is reproducible with the same module version.
- Output file paths and formats match the Processor tool's documented I/O specification; no data loss or format corruption detected.
- Backup and purging rules (if enabled) have been applied consistently; data integrity is maintained throughout the pipeline.

## Limitations

- MSConnect is not a standalone data analysis tool; it depends entirely on third-party software for data processing and does not include any Processor license or executable.
- Processor tool compatibility is vendor-specific and format-specific; not all MS instruments or file formats are supported by every Processor. Users must verify compatibility before invoking.
- Processing speed and resource consumption depend on the third-party Processor's efficiency and the host system's hardware (CPU, RAM, I/O); large batches may exceed available resources.
- No changelog is currently published; users cannot track breaking changes or bug fixes in the integration layer without consulting the development team directly.

## Evidence

- [other] Receive raw file metadata (filename, upload path, file format) from the Raw_File_Uploader repository output.: "Receive raw file metadata (filename, upload path, file format) from the Raw_File_Uploader repository output."
- [other] Validate raw file integrity and format compatibility with the Proteomics_Data_Processor tool specifications.: "Validate raw file integrity and format compatibility with the Proteomics_Data_Processor tool specifications."
- [other] Invoke Proteomics_Data_Processor with the raw file path as input, directing output to the designated processing queue.: "Invoke Proteomics_Data_Processor with the raw file path as input, directing output to the designated processing queue."
- [other] Collect and log processed proteomics output records (e.g., feature tables, quantification matrices, or mass spectrometry feature lists) returned by the Processor.: "Collect and log processed proteomics output records (e.g., feature tables, quantification matrices, or mass spectrometry feature lists) returned by the Processor."
- [readme] MSConnect does not come with any data processor or analysis software/license, it provides a wrapper/interface to interact with them.: "MSConnect does not come with any data processor or analysis software/license, it provides a wrapper/interface to interact with them."
- [intro] streamlines the entire process from data collection, data management, data processing and to data visualization by integrating and supporting various third-party tools, allowing for a fully autonomous workflow: "streamlines the entire process from data collection, data management, data processing and to data visualization by integrating and supporting various third-party tools"
