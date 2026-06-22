---
name: sample-spectrum-metadata-alignment
description: Use when you have a GNPS task ID from a completed molecular networking workflow (METABOLOMICS-SNETS, METABOLOMICS-SNETS-V2, FEATURE-BASED-MOLECULAR-NETWORKING on GNPS1, or classical_networking_workflow / feature_based_molecular_networking_workflow on GNPS2) and need to access the resulting spectral.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - nplinker
  - Python
  - GNPSDownloader
  - GNPSExtractor
  - GNPS
  - NPLinker
derived_from:
- doi: 10.1101/2024.10.11.617756
  title: NPLinker
evidence_spans:
- NPLinker is a python framework for data mining microbial natural products
- GNPSDownloader, GNPSExtractor
- Python version ≥3.11
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nplinker_2_cq
    doi: 10.1101/2024.10.11.617756
    title: NPLinker
  dedup_kept_from: coll_nplinker_2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2024.10.11.617756
  all_source_dois:
  - 10.1101/2024.10.11.617756
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# sample-spectrum-metadata-alignment

## Summary

Retrieve and extract molecular networking job results from GNPS (versions 1 and 2) to obtain standardized spectral and metadata files required for downstream computational analysis of natural product spectra and their associated sample metadata.

## When to use

You have a GNPS task ID from a completed molecular networking workflow (METABOLOMICS-SNETS, METABOLOMICS-SNETS-V2, FEATURE-BASED-MOLECULAR-NETWORKING on GNPS1, or classical_networking_workflow / feature_based_molecular_networking_workflow on GNPS2) and need to access the resulting spectral data (spectra.mgf), molecular family annotations, file mappings, and metadata for integration with genomic data in NPLinker or similar multi-omics frameworks.

## When NOT to use

- Your GNPS workflow has not yet completed or the task ID is invalid; wait for GNPS job completion before attempting download.
- You already have local copies of spectra.mgf, molecular_families.tsv, and file mappings; extraction is redundant if these files are already aligned to your working directory.
- You are using a non-standard or custom GNPS workflow variant not listed in the supported versions (METABOLOMICS-SNETS*, FEATURE-BASED-MOLECULAR-NETWORKING for GNPS1, or classical/feature_based for GNPS2); detection and file renaming may fail silently.

## Inputs

- GNPS task ID (string)
- download directory path (string)
- GNPS workflow version (inferred from compressed archive contents)

## Outputs

- spectra.mgf (standardized mass spectrometry spectral data file)
- molecular_families.tsv (molecular network cluster assignments)
- annotations.tsv (GNPS spectral library matches and metadata)
- file_mappings.tsv or .csv (mapping between spectral features and input samples)
- gnps directory (standardized output directory tree)

## How to apply

Execute a two-step download-and-extract workflow: (1) Instantiate a GNPSDownloader with your GNPS task ID and target download directory, invoke download() to retrieve the compressed archive from GNPS servers, and capture the returned archive file path; (2) Instantiate a GNPSExtractor with the archive path and a target gnps directory, invoke extraction to automatically detect the GNPS workflow version (GNPS1 or GNPS2) and rename the resulting files according to the version-specific mapping (spectra.mgf, molecular_families.tsv, annotations.tsv, and file_mappings.tsv or .csv). This standardization enables consistent downstream access to molecular networking results across heterogeneous GNPS releases.

## Related tools

- **GNPSDownloader** (Retrieves compressed GNPS workflow output archive from remote GNPS servers (GNPS1 or GNPS2) given a task ID and returns the local archive file path.) — https://github.com/NPLinker/nplinker
- **GNPSExtractor** (Unpacks and standardizes the contents of a GNPS output archive by detecting workflow version and renaming spectral, annotation, and mapping files to canonical names (spectra.mgf, molecular_families.tsv, etc.) for downstream use.) — https://github.com/NPLinker/nplinker
- **GNPS** (Remote spectral networking platform that generates molecular networking results (task output archives) consumed by this skill.) — https://gnps.ucsd.edu
- **NPLinker** (Python framework that orchestrates this download–extract workflow as a prerequisite to multi-omics data integration (genomics + metabolomics).) — https://github.com/NPLinker/nplinker
- **Python** (Runtime environment (≥3.11) for executing GNPSDownloader and GNPSExtractor class instantiation and method invocation.)

## Examples

```
from nplinker.gnps import GNPSDownloader, GNPSExtractor
downloader = GNPSDownloader('task_id_12345', './downloads')
archive_path = downloader.download()
extractor = GNPSExtractor(archive_path, './gnps')
extractor.extract()
```

## Evaluation signals

- Archive download succeeds and archive file path is returned and non-empty (file size > 0 bytes).
- Extraction completes without errors and the target gnps directory contains exactly four expected files: spectra.mgf (non-empty, valid MS/MS format), molecular_families.tsv, annotations.tsv, and either file_mappings.tsv or file_mappings.csv (all non-zero byte size).
- GNPS workflow version is correctly detected (log or return value indicates METABOLOMICS-SNETS, METABOLOMICS-SNETS-V2, FEATURE-BASED-MOLECULAR-NETWORKING, classical_networking_workflow, or feature_based_molecular_networking_workflow) and file renaming is applied accordingly.
- File format integrity: spectra.mgf conforms to MGF schema, TSV files are tab-delimited with consistent column structure, and no truncation or corruption is present.
- Downstream NPLinker module (npl.load_data()) successfully loads the extracted files without schema or path errors, confirming alignment with expected metadata structure.

## Limitations

- Requires an active internet connection to GNPS1 (https://gnps.ucsd.edu) or GNPS2 (https://gnps2.org) servers; network outages or server maintenance will cause download failure.
- GNPS task ID must correspond to a completed workflow; incomplete or failed GNPS tasks will produce an invalid or corrupted archive that extraction may not detect or report clearly.
- Only supports four GNPS1 workflow variants (METABOLOMICS-SNETS, METABOLOMICS-SNETS-V2, FEATURE-BASED-MOLECULAR-NETWORKING) and two GNPS2 variants; custom or future GNPS workflows not in this list will not be recognized and may extract to incorrect file names.
- File naming is fixed and cannot be customized; if downstream tools expect alternative names or directory structures, post-extraction renaming or symlinking is required.
- Storage requirements depend on GNPS dataset size; large spectral libraries (>10 GB archives) may consume significant disk space and transfer time.

## Evidence

- [other] NPLinker uses a two-step process: Download GNPS data & get the path to the downloaded archive, then Extract GNPS data to `gnps` directory, enabling access to molecular networking results for subsequent computational analysis.: "NPLinker uses a two-step process: Download GNPS data & get the path to the downloaded archive, then Extract GNPS data to `gnps` directory"
- [other] Instantiate GNPSDownloader with a GNPS task ID and download directory path, then invoke the download() method to retrieve the compressed archive from GNPS servers and obtain the archive file path.: "Instantiate GNPSDownloader with a GNPS task ID and download directory path, then invoke the download() method to retrieve the compressed archive from GNPS servers"
- [other] Instantiate GNPSExtractor with the downloaded archive path and target gnps directory path, then invoke extraction to identify and rename the workflow-specific files (spectra.mgf, molecular_families.tsv, annotations.tsv, file_mappings.tsv or .csv) according to the mapping table for the detected GNPS workflow version: "invoke extraction to identify and rename the workflow-specific files (spectra.mgf, molecular_families.tsv, annotations.tsv, file_mappings.tsv or .csv)"
- [other] METABOLOMICS-SNETS, METABOLOMICS-SNETS-V2, FEATURE-BASED-MOLECULAR-NETWORKING for GNPS1; classical_networking_workflow or feature_based_molecular_networking_workflow for GNPS2: "for the detected GNPS workflow version (METABOLOMICS-SNETS, METABOLOMICS-SNETS-V2, FEATURE-BASED-MOLECULAR-NETWORKING for GNPS1; classical_networking_workflow or"
- [other] currently accepts data from both GNPS1 (https://gnps.ucsd.edu) and GNPS2 (https://gnps2.org) workflows: "currently accepts data from both GNPS1 (https://gnps.ucsd.edu) and GNPS2 (https://gnps2.org) workflows"
