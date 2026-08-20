---
name: molecular-network-metadata-organization
description: 'Use when when you have a GNPS molecular networking task ID (from GNPS1 or GNPS2 workflows: METABOLOMICS-SNETS, METABOLOMICS-SNETS-V2, FEATURE-BASED-MOLECULAR-NETWORKING, classical_networking_workflow, or feature_based_molecular_networking_workflow) and need to prepare the job archive for NPLinker.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2409
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3407
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
evidence_spans:
- It provides the tools [`GNPSDownloader`][nplinker.metabolomics.gnps.GNPSDownloader] and [`GNPSExtractor`][nplinker.metabolomics.gnps.GNPSExtractor]
- '[![github repo badge](https://img.shields.io/badge/github-nplinker-000.svg?color=blue)](https://github.com/NPLinker/nplinker)'
- Python version ≥3.11
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_npclassscore_cq
    doi: 10.1186/s40168-022-01444-3
    title: NPClassScore
  dedup_kept_from: coll_npclassscore_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s40168-022-01444-3
  all_source_dois:
  - 10.1186/s40168-022-01444-3
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-network-metadata-organization

## Summary

A skill for fetching, extracting, and standardizing GNPS molecular networking job archives into a structured directory with normalized file names and formats. This enables downstream integration of genomics and metabolomics data in natural products discovery pipelines.

## When to use

When you have a GNPS molecular networking task ID (from GNPS1 or GNPS2 workflows: METABOLOMICS-SNETS, METABOLOMICS-SNETS-V2, FEATURE-BASED-MOLECULAR-NETWORKING, classical_networking_workflow, or feature_based_molecular_networking_workflow) and need to prepare the job archive for NPLinker or similar metabolomics-genomics integration analysis.

## When NOT to use

- GNPS data is already extracted and standardized in the expected directory structure with correct file names
- You are working with metabolomics data from a non-GNPS source (e.g., MzMine output, Metabolomics Workbench) without prior GNPS molecular networking analysis
- The GNPS task ID is invalid, the job has not completed, or the archive cannot be accessed online

## Inputs

- GNPS task ID (string identifier for a completed GNPS molecular networking job)
- downloads directory path (writeable local directory for archive storage)
- target gnps directory path (writeable local directory for extracted and renamed files)

## Outputs

- spectra.mgf (mass spectrometry fragmentation spectra in MGF format)
- molecular_families.tsv (molecular networking families with node/edge relationships)
- annotations.tsv (spectral annotations and library matches)
- file_mappings.tsv or file_mappings.csv (mapping between sample files and spectral features)
- gnps directory (directory structure containing all four standardized files)

## How to apply

First, initialize a GNPSDownloader with the GNPS task ID and a downloads directory path, then call download() to fetch the job archive and obtain its local file path. Second, initialize a GNPSExtractor with the downloaded archive path and a target gnps directory, then call the extraction method to decompress the archive. The extractor automatically identifies the workflow type and extracts relevant data files. Third, rename and move extracted files to NPLinker standard names: spectra.mgf, molecular_families.tsv, annotations.tsv, and file_mappings.tsv (or file_mappings.csv). Finally, verify that all four required files are present, accessible, and properly formatted in the gnps directory before passing to downstream data loading operations.

## Related tools

- **GNPSDownloader** (Fetches GNPS job archive from GNPS servers using task ID and returns local file path) — https://github.com/NPLinker/nplinker
- **GNPSExtractor** (Decompresses archive, identifies workflow type, and extracts constituent data files to target directory) — https://github.com/NPLinker/nplinker
- **nplinker** (Python framework that depends on standardized GNPS metadata organization as input for natural products mining) — https://github.com/NPLinker/nplinker

## Examples

```
from nplinker.gnps import GNPSDownloader, GNPSExtractor; downloader = GNPSDownloader('task_id_12345', './downloads'); archive_path = downloader.download(); extractor = GNPSExtractor(archive_path, './gnps'); extractor.extract()
```

## Evaluation signals

- All four required files (spectra.mgf, molecular_families.tsv, annotations.tsv, file_mappings.tsv/csv) are present in the gnps directory with correct naming
- File formats are valid: MGF is parseable by mass spectrometry tools, TSV/CSV files have expected headers and consistent column counts
- spectra.mgf contains MS/MS fragmentation data with BEGIN IONS / END IONS blocks and peptide mass fingerprint values
- molecular_families.tsv contains network node/edge topology aligned with spectra.mgf scan indices
- file_mappings links sample identifiers to spectral features; counts should match features present in spectra.mgf
- No data loss during extraction: file sizes are consistent with original GNPS archive contents

## Limitations

- Only compatible with GNPS1 (https://gnps.ucsd.edu) and GNPS2 (https://gnps2.org) molecular networking workflows; other GNPS analysis types are not supported
- Requires online access to GNPS servers at download time; offline archives must be pre-downloaded and provided as file paths
- Archive extraction depends on correct workflow type detection; non-standard or custom GNPS workflows may fail to extract correctly
- File naming conventions are specific to NPLinker; integration with other metabolomics pipelines may require additional mapping

## Evidence

- [other] GNPSDownloader fetches a GNPS molecular networking job archive and returns its file path; second, GNPSExtractor extracts the archive contents into a designated `gnps` directory for subsequent data loading operations.: "GNPSDownloader fetches a GNPS molecular networking job archive and returns its file path; second, GNPSExtractor extracts the archive contents into a designated `gnps` directory for subsequent data"
- [other] identify the relevant data files based on the GNPS workflow type (METABOLOMICS-SNETS, METABOLOMICS-SNETS-V2, FEATURE-BASED-MOLECULAR-NETWORKING for GNPS1, or classical_networking_workflow, feature_based_molecular_networking_workflow for GNPS2): "identify the relevant data files based on the GNPS workflow type (METABOLOMICS-SNETS, METABOLOMICS-SNETS-V2, FEATURE-BASED-MOLECULAR-NETWORKING for GNPS1, or classical_networking_workflow,"
- [other] Rename and move the extracted files to the standard NPLinker names (spectra.mgf, molecular_families.tsv, annotations.tsv, file_mappings.tsv or file_mappings.csv): "Rename and move the extracted files to the standard NPLinker names (spectra.mgf, molecular_families.tsv, annotations.tsv, file_mappings.tsv or file_mappings.csv)"
- [other] Verify that all four required files are present and accessible in the gnps directory with correct naming and format.: "Verify that all four required files are present and accessible in the gnps directory with correct naming and format."
- [readme] NPLinker is a python framework for data mining microbial natural products by integrating genomics and metabolomics data.: "NPLinker is a python framework for data mining microbial natural products by integrating genomics and metabolomics data."
