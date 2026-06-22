---
name: archive-extraction-and-file-mapping
description: 'Use when when you have downloaded a GNPS molecular networking job archive (from GNPS1 or GNPS2 workflows: METABOLOMICS-SNETS, METABOLOMICS-SNETS-V2, FEATURE-BASED-MOLECULAR-NETWORKING, classical_networking_workflow, or feature_based_molecular_networking_workflow) and need to extract and standardize.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - nplinker
  - Python
  - GNPSDownloader
  - GNPSExtractor
  techniques:
  - LC-MS
derived_from:
- doi: 10.1186/s40168-022-01444-3
  title: NPClassScore
- doi: 10.1101/2024.10.11.617756
  title: ''
evidence_spans:
- It provides the tools [`GNPSDownloader`][nplinker.metabolomics.gnps.GNPSDownloader] and [`GNPSExtractor`][nplinker.metabolomics.gnps.GNPSExtractor]
- '[![github repo badge](https://img.shields.io/badge/github-nplinker-000.svg?color=blue)](https://github.com/NPLinker/nplinker)'
- Python version ≥3.11
- NPLinker is a python framework for data mining microbial natural products
- GNPSDownloader, GNPSExtractor
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_npclassscore_cq
    doi: 10.1186/s40168-022-01444-3
    title: NPClassScore
  - build: coll_nplinker_2_cq
    doi: 10.1101/2024.10.11.617756
    title: NPLinker
  dedup_kept_from: coll_npclassscore_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s40168-022-01444-3
  all_source_dois:
  - 10.1186/s40168-022-01444-3
  - 10.1101/2024.10.11.617756
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# archive-extraction-and-file-mapping

## Summary

Decompose a GNPS molecular networking job archive into constituent metabolomics data files (spectra, molecular families, annotations, file mappings) and standardize their naming for downstream NPLinker processing. This skill bridges raw GNPS output archives to the normalized file structure required by integrated genomics–metabolomics analysis.

## When to use

When you have downloaded a GNPS molecular networking job archive (from GNPS1 or GNPS2 workflows: METABOLOMICS-SNETS, METABOLOMICS-SNETS-V2, FEATURE-BASED-MOLECULAR-NETWORKING, classical_networking_workflow, or feature_based_molecular_networking_workflow) and need to extract and standardize its contents into spectra.mgf, molecular_families.tsv, annotations.tsv, and file_mappings files for NPLinker's load_data() workflow.

## When NOT to use

- Input is not a GNPS molecular networking job archive (e.g., raw LC–MS files, pre-extracted file set, or output from a different networking platform).
- The GNPS archive is from an unsupported workflow type or version not recognized by the GNPSExtractor.
- The target gnps directory already contains partially extracted or corrupted files; extraction should be performed on a clean directory.

## Inputs

- GNPS job archive file (compressed, e.g., .zip or .tar.gz)
- GNPS workflow type identifier (METABOLOMICS-SNETS, METABOLOMICS-SNETS-V2, FEATURE-BASED-MOLECULAR-NETWORKING for GNPS1; classical_networking_workflow, feature_based_molecular_networking_workflow for GNPS2)
- Target gnps directory path (may be created if not present)

## Outputs

- spectra.mgf file (mass spectrometry spectral data)
- molecular_families.tsv file (molecular networking clusters)
- annotations.tsv file (compound/feature annotations)
- file_mappings.tsv or file_mappings.csv file (sample–spectrum associations)
- gnps directory containing all four standardized files

## How to apply

Initialize a GNPSExtractor with the local path to the downloaded archive and a target gnps directory. Call the extraction method, which decompresses the archive and identifies relevant data files based on the workflow type. The extractor then renames and relocates the extracted files to NPLinker's standard names: spectra.mgf (mass spectrometry data), molecular_families.tsv (networking clusters), annotations.tsv (compound annotations), and file_mappings.tsv or file_mappings.csv (sample-to-spectrum mappings). Verify all four required files are present in the gnps directory with correct naming and accessible format before proceeding to load_data(). This normalization ensures compatibility with subsequent genomics integration steps.

## Related tools

- **GNPSDownloader** (Fetches the GNPS molecular networking job archive from GNPS servers and returns the local file path; prerequisite to extraction.) — https://github.com/NPLinker/nplinker
- **GNPSExtractor** (Core extraction tool that decompresses the archive, identifies files by GNPS workflow type, and renames them to NPLinker standard names.) — https://github.com/NPLinker/nplinker
- **nplinker** (Python framework that integrates the extraction step into the broader genomics–metabolomics data mining pipeline; exposes load_data() method to read standardized files.) — https://github.com/NPLinker/nplinker

## Examples

```
from nplinker.gnps import GNPSDownloader, GNPSExtractor
downloader = GNPSDownloader('task_id_123', './downloads')
archive_path = downloader.download()
extractor = GNPSExtractor(archive_path, './gnps')
extractor.extraction()
```

## Evaluation signals

- All four required files (spectra.mgf, molecular_families.tsv, annotations.tsv, file_mappings.tsv or .csv) are present in the gnps directory.
- File names exactly match NPLinker's standard naming scheme (no residual workflow-specific prefixes or extensions).
- spectra.mgf is a valid MGF format file containing MS/MS spectral records with m/z and intensity pairs.
- molecular_families.tsv and annotations.tsv contain tab-separated data with expected column headers (e.g., cluster_id, compound name, adduct).
- file_mappings contains all sample–spectrum associations without gaps; subsequent npl.load_data() executes without file-not-found errors.

## Limitations

- Extraction success depends on the GNPS archive conforming to one of the supported workflow types; archives from custom or deprecated GNPS workflows may fail silently or produce incomplete extraction.
- The extractor requires sufficient disk space to decompress large archives; no streaming or incremental extraction is available.
- File naming standardization assumes GNPS workflows follow standard output conventions; manual post-extraction checks are recommended before downstream analysis to catch workflow-specific deviations.

## Evidence

- [other] The workflow operates in two sequential steps: first, GNPSDownloader fetches a GNPS molecular networking job archive and returns its file path; second, GNPSExtractor extracts the archive contents into a designated `gnps` directory for subsequent data loading operations.: "GNPSDownloader fetches a GNPS molecular networking job archive and returns its file path; second, GNPSExtractor extracts the archive contents into a designated `gnps` directory"
- [other] Initialize a GNPSExtractor with the downloaded archive path and the target gnps directory path, then call the extraction method to decompress the archive and identify the relevant data files based on the GNPS workflow type (METABOLOMICS-SNETS, METABOLOMICS-SNETS-V2, FEATURE-BASED-MOLECULAR-NETWORKING for GNPS1, or classical_networking_workflow, feature_based_molecular_networking_workflow for GNPS2).: "Initialize a GNPSExtractor with the downloaded archive path and the target gnps directory path, then call the extraction method to decompress the archive and identify the relevant data files based on"
- [other] Rename and move the extracted files to the standard NPLinker names (spectra.mgf, molecular_families.tsv, annotations.tsv, file_mappings.tsv or file_mappings.csv) in the gnps directory.: "Rename and move the extracted files to the standard NPLinker names (spectra.mgf, molecular_families.tsv, annotations.tsv, file_mappings.tsv or file_mappings.csv)"
- [other] Verify that all four required files are present and accessible in the gnps directory with correct naming and format.: "Verify that all four required files are present and accessible in the gnps directory with correct naming and format"
- [other] NPLinker currently accepts data from both GNPS1 (https://gnps.ucsd.edu) and GNPS2 (https://gnps2.org) workflows: "NPLinker currently accepts data from both GNPS1 and GNPS2 workflows"
