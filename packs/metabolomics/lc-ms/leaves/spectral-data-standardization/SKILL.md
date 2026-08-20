---
name: spectral-data-standardization
description: Use when you have completed a GNPS1 (METABOLOMICS-SNETS, METABOLOMICS-SNETS-V2, FEATURE-BASED-MOLECULAR-NETWORKING) or GNPS2 (classical_networking_workflow, feature_based_molecular_networking_workflow) molecular networking job and need to access its output files in a standardized format for.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - nplinker
  - Python
  - GNPS
  techniques:
  - LC-MS
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-data-standardization

## Summary

Retrieve and extract molecular networking job results from GNPS workflows to obtain standardized spectral data files (spectra.mgf, molecular_families.tsv, annotations.tsv) needed for downstream natural products mining. This skill bridges GNPS output heterogeneity across workflow versions by identifying and renaming files according to detected workflow type.

## When to use

You have completed a GNPS1 (METABOLOMICS-SNETS, METABOLOMICS-SNETS-V2, FEATURE-BASED-MOLECULAR-NETWORKING) or GNPS2 (classical_networking_workflow, feature_based_molecular_networking_workflow) molecular networking job and need to access its output files in a standardized format for integration with downstream tools like NPLinker. You possess a GNPS task ID and need a reproducible way to download and extract the compressed results archive.

## When NOT to use

- Your GNPS job has not yet completed or returned an error state; wait for job completion and check the GNPS interface before attempting download.
- You already possess locally extracted and properly named GNPS output files in your working directory; skip directly to data loading and link computation.
- You are working with metabolomics data from a non-GNPS source (e.g., raw LC-MS/MS spectra, vendor software outputs, or alternative networking platforms); this skill is GNPS-specific.

## Inputs

- GNPS task ID (string identifier for a completed GNPS job)
- download directory path (filesystem path for archive storage)
- target gnps directory path (filesystem location for extracted files)

## Outputs

- spectra.mgf (standardized mass spectrometry data file)
- molecular_families.tsv (standardized molecular networking results)
- annotations.tsv (standardized spectral annotations)
- file_mappings.tsv or file_mappings.csv (standardized file mapping table)

## How to apply

First, instantiate a GNPSDownloader with your GNPS task ID and a target download directory path, then invoke its download() method to retrieve the compressed archive from GNPS servers and capture the returned archive file path. Second, instantiate a GNPSExtractor with the downloaded archive path and a target gnps directory path, then invoke extraction which automatically detects the GNPS workflow version from the archive structure and renames the workflow-specific output files (spectra.mgf, molecular_families.tsv, annotations.tsv, file_mappings.tsv or .csv) according to an internal mapping table. This two-step process eliminates manual file hunting and version-specific renaming logic, ensuring consistent input for molecular networking analysis.

## Related tools

- **nplinker** (Python framework providing GNPSDownloader and GNPSExtractor classes for automated GNPS data retrieval and standardization) — https://github.com/NPLinker/nplinker
- **GNPS** (Global Natural Products Social molecular networking platform generating the job results being downloaded and extracted) — https://gnps.ucsd.edu

## Examples

```
from nplinker.downloader import GNPSDownloader, GNPSExtractor
downloader = GNPSDownloader('f.abc123def456', './downloads')
archive_path = downloader.download()
extractor = GNPSExtractor(archive_path, './gnps')
extractor.extract()
```

## Evaluation signals

- Archive file path returned by download() method points to a valid .zip file that is readable and not truncated (file size > 1 MB typical for networking results).
- Extraction completes without error and produces all four expected standardized output files (spectra.mgf, molecular_families.tsv, annotations.tsv, file_mappings.tsv/.csv) in the target gnps directory.
- Output file headers and row counts match expectations for the detected GNPS workflow version (e.g., spectra.mgf contains valid MS/MS scan blocks, molecular_families.tsv contains cluster ID and member columns).
- Downstream tools (e.g., npl.load_data()) successfully ingest the extracted files without file-not-found or schema mismatch errors.
- Workflow version detected by GNPSExtractor matches the known workflow used to generate the GNPS job (verifiable via GNPS web interface or job metadata).

## Limitations

- GNPSExtractor supports only GNPS1 (METABOLOMICS-SNETS, METABOLOMICS-SNETS-V2, FEATURE-BASED-MOLECULAR-NETWORKING) and GNPS2 (classical_networking_workflow, feature_based_molecular_networking_workflow) workflow outputs; other GNPS workflow types are not handled.
- Download success depends on network connectivity and GNPS server availability; transient network failures will cause the download() method to fail.
- File extraction is version-sensitive: if GNPS introduces new workflow types or renames output files without updating the internal GNPSExtractor mapping table, extraction will fail or produce incorrectly named outputs.

## Evidence

- [other] NPLinker uses a two-step process: Download GNPS data & get the path to the downloaded archive, then Extract GNPS data to `gnps` directory, enabling access to molecular networking results for subsequent computational analysis.: "NPLinker uses a two-step process: Download GNPS data & get the path to the downloaded archive, then Extract GNPS data to `gnps` directory"
- [other] Instantiate GNPSDownloader with a GNPS task ID and download directory path, then invoke the download() method to retrieve the compressed archive from GNPS servers and obtain the archive file path.: "Instantiate GNPSDownloader with a GNPS task ID and download directory path, then invoke the download() method to retrieve the compressed archive from GNPS servers"
- [other] Instantiate GNPSExtractor with the downloaded archive path and target gnps directory path, then invoke extraction to identify and rename the workflow-specific files (spectra.mgf, molecular_families.tsv, annotations.tsv, file_mappings.tsv or .csv) according to the mapping table for the detected GNPS workflow version (METABOLOMICS-SNETS, METABOLOMICS-SNETS-V2, FEATURE-BASED-MOLECULAR-NETWORKING for GNPS1; classical_networking_workflow or feature_based_molecular_networking_workflow for GNPS2).: "Instantiate GNPSExtractor with the downloaded archive path and target gnps directory path, then invoke extraction to identify and rename the workflow-specific files"
- [readme] NPLinker is a python framework for data mining microbial natural products by integrating genomics and metabolomics data.: "NPLinker is a python framework for data mining microbial natural products by integrating genomics and metabolomics data"
- [other] NPLinker requires GNPS molecular networking data as input: "NPLinker requires GNPS molecular networking data as input"
