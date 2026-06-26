---
name: gnps-data-schema-validation
description: Use when after extracting a GNPS molecular networking job archive using
  GNPSExtractor, before calling npl.load_data().
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - nplinker
  - Python
  - GNPSExtractor
  - GNPS1
  - GNPS2
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1186/s40168-022-01444-3
  title: NPClassScore
evidence_spans:
- It provides the tools [`GNPSDownloader`][nplinker.metabolomics.gnps.GNPSDownloader]
  and [`GNPSExtractor`][nplinker.metabolomics.gnps.GNPSExtractor]
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

# GNPS Data Schema Validation

## Summary

Validate that extracted GNPS molecular networking job archives conform to expected file naming, format, and completeness standards before downstream metabolomics processing. This skill ensures data integrity by confirming all four required files (spectra.mgf, molecular_families.tsv, annotations.tsv, file_mappings) are present and correctly named.

## When to use

After extracting a GNPS molecular networking job archive using GNPSExtractor, before calling npl.load_data(). Trigger when you have renamed and moved extracted files to the gnps directory and need to confirm the extraction completed successfully and produced valid inputs for the NPLinker metabolomics workflow.

## When NOT to use

- Input files have not yet been extracted from the GNPS archive — run GNPSExtractor first.
- Files are in an alternative naming scheme or organization already validated by another tool.
- You are working with pre-downloaded, locally curated GNPS data that has already been validated by the source institution.

## Inputs

- GNPS extraction directory path (gnps/)
- Renamed and relocated GNPS archive files (spectra.mgf, molecular_families.tsv, annotations.tsv, file_mappings.tsv or .csv)

## Outputs

- Validation report confirming presence and format correctness of all four required GNPS files
- Boolean flag or exception indicating readiness for npl.load_data() or load_data failure reason

## How to apply

After the GNPSExtractor step completes and files have been renamed to standard NPLinker names, verify that all four required files are present and accessible in the gnps directory: spectra.mgf (mass spectrometry data), molecular_families.tsv (cluster assignments), annotations.tsv (candidate compounds), and file_mappings.tsv or file_mappings.csv (sample metadata). Check file existence, confirm naming matches the standard schema exactly, and validate that each file is readable and non-empty. This validation gates the subsequent npl.load_data() call and ensures the workflow operates on complete, well-formed metabolomics inputs from either GNPS1 (METABOLOMICS-SNETS, METABOLOMICS-SNETS-V2, FEATURE-BASED-MOLECULAR-NETWORKING) or GNPS2 (classical_networking_workflow, feature_based_molecular_networking_workflow) job types.

## Related tools

- **GNPSExtractor** (Upstream tool that extracts GNPS molecular networking job archives; output of this tool is input to validation) — https://github.com/NPLinker/nplinker
- **nplinker** (Framework that consumes validated GNPS data via npl.load_data(); validation gates this downstream step) — https://github.com/NPLinker/nplinker
- **GNPS1** (Source molecular networking platform; generates job archives in METABOLOMICS-SNETS or FEATURE-BASED-MOLECULAR-NETWORKING workflow types) — https://gnps.ucsd.edu
- **GNPS2** (Updated source molecular networking platform; generates job archives in classical_networking_workflow or feature_based_molecular_networking_workflow types) — https://gnps2.org

## Examples

```
# After GNPSExtractor writes to gnps/, validate schema:
import os; required = ['spectra.mgf', 'molecular_families.tsv', 'annotations.tsv', 'file_mappings.tsv']; present = all(os.path.isfile(f'gnps/{f}') and os.path.getsize(f'gnps/{f}') > 0 for f in required); assert present, 'Missing or empty required GNPS files in gnps/ directory'
```

## Evaluation signals

- All four required files (spectra.mgf, molecular_families.tsv, annotations.tsv, file_mappings.tsv or file_mappings.csv) are present in the gnps directory with exact naming match.
- Each file is readable (not corrupted or truncated) and non-empty (file size > 0 bytes).
- File extensions and formats match expected schema: .mgf for spectra, .tsv for tabular data, .csv as alternative for file_mappings.
- File path resolution confirms gnps directory is accessible and contains no orphaned or duplicate files with alternative names.
- Subsequent npl.load_data() call succeeds without file-not-found or schema errors, indicating validation correctly predicted load readiness.

## Limitations

- Validation confirms file presence and naming only; it does not validate internal data integrity (e.g., whether spectra.mgf contains valid MS/MS records or whether molecular_families.tsv contains expected columns).
- Behavior differs between GNPS1 and GNPS2 job types; validation must account for both classical_networking_workflow (GNPS2) and METABOLOMICS-SNETS (GNPS1) file naming conventions.
- Does not detect incomplete extractions if the archive was only partially decompressed; relies on prior GNPSExtractor success.
- File format validation (e.g., checking for required columns in TSV files) is out of scope; this skill validates schema-level file presence only.

## Evidence

- [other] Rename and move the extracted files to the standard NPLinker names (spectra.mgf, molecular_families.tsv, annotations.tsv, file_mappings.tsv or file_mappings.csv) in the gnps directory.: "Rename and move the extracted files to the standard NPLinker names (spectra.mgf, molecular_families.tsv, annotations.tsv, file_mappings.tsv or file_mappings.csv) in the gnps directory."
- [other] Verify that all four required files are present and accessible in the gnps directory with correct naming and format.: "Verify that all four required files are present and accessible in the gnps directory with correct naming and format."
- [other] GNPSExtractor extracts the archive contents into a designated `gnps` directory for subsequent data loading operations.: "GNPSExtractor extracts the archive contents into a designated `gnps` directory for subsequent data loading operations."
- [other] currently accepts data from both GNPS1 (https://gnps.ucsd.edu) and GNPS2 (https://gnps2.org) workflows: "currently accepts data from both GNPS1 (https://gnps.ucsd.edu) and GNPS2 (https://gnps2.org) workflows"
