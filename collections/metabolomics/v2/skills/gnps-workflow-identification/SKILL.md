---
name: gnps-workflow-identification
description: Use when you have downloaded a GNPS molecular networking job archive
  and need to extract its contents (spectra.mgf, molecular_families.tsv, annotations.tsv,
  file_mappings) but do not know which GNPS workflow version produced it, preventing
  correct file naming and downstream computational analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3407
  tools:
  - nplinker
  - Python
  - GNPS
  - NPLinker
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1101/2024.10.11.617756
  title: NPLinker
evidence_spans:
- NPLinker is a python framework for data mining microbial natural products
- GNPSDownloader, GNPSExtractor
- Python version ≥3.11
- NPLinker requires GNPS molecular networking data as input
- NPLinker requires GNPS molecular networking data as input. It currently accepts
  data from both GNPS1 (https://gnps.ucsd.edu) and GNPS2 (https://gnps2.org) workflows.
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

# GNPS Workflow Identification

## Summary

Identify and map GNPS workflow versions (GNPS1 vs. GNPS2, classical vs. feature-based networking) to correctly parse and rename molecular networking output files for downstream analysis in NPLinker.

## When to use

You have downloaded a GNPS molecular networking job archive and need to extract its contents (spectra.mgf, molecular_families.tsv, annotations.tsv, file_mappings) but do not know which GNPS workflow version produced it, preventing correct file naming and downstream computational analysis.

## When NOT to use

- GNPS data has already been extracted and files renamed to standard names (spectra.mgf, molecular_families.tsv, etc.).
- You are working with non-GNPS molecular networking data (e.g., custom mass spectrometry networking output) that does not follow GNPS archive conventions.
- The GNPS job failed or the archive is corrupted and does not contain expected workflow output files.

## Inputs

- GNPS compressed archive (downloaded from GNPS1 or GNPS2 server)
- GNPS task ID or job result URL
- Target extraction directory path

## Outputs

- Standardized spectra.mgf file (renamed from workflow-specific source)
- Standardized molecular_families.tsv file
- Standardized annotations.tsv file
- Standardized file_mappings.tsv or .csv file
- Extracted gnps directory with workflow-normalized file hierarchy

## How to apply

Examine the structure and filenames within the downloaded GNPS archive to detect which workflow variant generated it. NPLinker uses a workflow-version-specific mapping table: GNPS1 workflows (METABOLOMICS-SNETS, METABOLOMICS-SNETS-V2, FEATURE-BASED-MOLECULAR-NETWORKING) and GNPS2 workflows (classical_networking_workflow, feature_based_molecular_networking_workflow) each produce distinctly named intermediate files. Once identified, instantiate the appropriate GNPSExtractor with the archive path and target gnps directory, then invoke extraction to rename workflow-specific files according to the detected version's mapping table. This ensures that renamed outputs (e.g., spectra.mgf, molecular_families.tsv) conform to NPLinker's standardized input interface for subsequent link computation.

## Related tools

- **NPLinker** (Provides GNPSExtractor class and workflow-detection logic to map GNPS archive structure to standardized output file names) — https://github.com/NPLinker/nplinker
- **Python** (Runtime environment for instantiating GNPSExtractor and executing workflow identification and file extraction)
- **GNPS** (Source platform that produces the molecular networking archives with version-specific file naming conventions) — https://gnps.ucsd.edu; https://gnps2.org

## Examples

```
from nplinker.genomics import GNPSExtractor; extractor = GNPSExtractor('/path/to/gnps_archive.zip', '/path/to/gnps'); extractor.extract()
```

## Evaluation signals

- Extracted directory contains all four expected standardized files: spectra.mgf, molecular_families.tsv, annotations.tsv, and file_mappings.tsv (or .csv).
- File contents are non-empty and conform to expected schemas (e.g., spectra.mgf is valid MGF format, molecular_families.tsv is a valid tab-delimited table).
- Workflow version detected matches the actual GNPS platform and workflow type used to generate the job (e.g., METABOLOMICS-SNETS-V2 for GNPS1 feature-based networking).
- Renamed files are accessible to downstream NPLinker modules (e.g., load_data() succeeds without file-not-found errors).
- File mapping table correctly reconciles original workflow-specific filenames to standardized output names without data loss or truncation.

## Limitations

- NPLinker currently supports only GNPS1 (gnps.ucsd.edu) and GNPS2 (gnps2.org) platforms; other GNPS instances or custom networking tools are not supported.
- Workflow detection relies on archive structure conventions; non-standard or manually edited GNPS archives may fail to identify correctly.
- The mapping table is static and may require updates if GNPS adds new workflow types or changes internal file naming schemes.
- File extraction assumes Unix-compatible file paths; Windows path handling or special characters in filenames may introduce platform-specific issues.

## Evidence

- [other] Extract GNPS data to `gnps` directory, enabling access to molecular networking results for subsequent computational analysis.: "Extract GNPS data to `gnps` directory, enabling access to molecular networking results for subsequent computational analysis."
- [other] Instantiate GNPSExtractor with the downloaded archive path and target gnps directory path, then invoke extraction to identify and rename the workflow-specific files (spectra.mgf, molecular_families.tsv, annotations.tsv, file_mappings.tsv or .csv) according to the mapping table for the detected GNPS workflow version (METABOLOMICS-SNETS, METABOLOMICS-SNETS-V2, FEATURE-BASED-MOLECULAR-NETWORKING for GNPS1; classical_networking_workflow or feature_based_molecular_networking_workflow for GNPS2).: "invoke extraction to identify and rename the workflow-specific files (spectra.mgf, molecular_families.tsv, annotations.tsv, file_mappings.tsv or .csv) according to the mapping table for the detected"
- [other] NPLinker requires GNPS molecular networking data as input.: "NPLinker requires GNPS molecular networking data as input"
- [other] currently accepts data from both GNPS1 (https://gnps.ucsd.edu) and GNPS2 (https://gnps2.org) workflows: "currently accepts data from both GNPS1 (https://gnps.ucsd.edu) and GNPS2 (https://gnps2.org) workflows"
