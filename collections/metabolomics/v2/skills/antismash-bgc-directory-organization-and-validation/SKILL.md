---
name: antismash-bgc-directory-organization-and-validation
description: Use when when preparing genomic data for NPLinker analysis and you have AntiSMASH BGC predictions that need to be validated and organized into NPLinker's standardized directory layout.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_3053
  - http://edamontology.org/topic_0102
  tools:
  - nplinker
  - Python
  - AntiSMASH
  - MIBiG
  - Dynaconf
derived_from:
- doi: 10.1101/2024.10.11.617756
  title: NPLinker
evidence_spans:
- NPLinker is a python framework for data mining microbial natural products
- GNPSDownloader, GNPSExtractor
- Python version ≥3.11
- antismash directory contains a collection of AntiSMASH BGC data
- mibig directory contains the MIBiG metadata
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

# antismash-bgc-directory-organization-and-validation

## Summary

Validates and organizes AntiSMASH biosynthetic gene cluster (BGC) output directories for integration into NPLinker's data preparation pipeline. This skill ensures that AntiSMASH results conform to expected directory structure and content requirements before downstream metabolomics-genomics linkage analysis.

## When to use

When preparing genomic data for NPLinker analysis and you have AntiSMASH BGC predictions that need to be validated and organized into NPLinker's standardized directory layout. Specifically, apply this skill after running AntiSMASH and before invoking NPLinker's DatasetLoader, or when working in PODP mode where AntiSMASH data may require download and extraction.

## When NOT to use

- If you are working with pre-computed AntiSMASH results that are already integrated into an NPLinker project and do not require re-validation or reorganization.
- If your workflow does not involve linking genomic and metabolomic data, or you are not using NPLinker as the downstream analysis framework.
- If AntiSMASH has not yet been run on your genomic samples and you need to execute AntiSMASH first (this skill validates existing results, not run prediction).

## Inputs

- Dynaconf configuration file (nplinker.toml)
- Operating mode indicator (local or PODP)
- Antismash directory path (for local mode) or project metadata (for PODP mode)
- Optional: remote antismash archive URL or PODP project ID

## Outputs

- Validated antismash directory with organized BGC data files
- Configuration state with antismash path and validation status
- Error message (if validation fails and retries exhausted)

## How to apply

Check the Dynaconf configuration (nplinker.toml) to determine the operating mode (local or PODP). For local mode, verify that the antismash directory exists at the configured path; if missing, raise a data validation error. For PODP mode, if the antismash directory is missing or invalid, download and extract the AntiSMASH data automatically, with up to 2 retries on validation failure. Validate the directory contents to ensure they follow the expected AntiSMASH output structure. The skill succeeds when a validated antismash directory with properly organized BGC data files is ready for consumption by NPLinker's DatasetLoader.

## Related tools

- **nplinker** (Framework that consumes the validated and organized AntiSMASH directory as input for metabolomics-genomics data integration) — https://github.com/NPLinker/nplinker
- **AntiSMASH** (BGC prediction tool whose output directory is being validated and organized by this skill)
- **Dynaconf** (Configuration management system used to specify mode (local vs. PODP) and data paths for validation logic)

## Examples

```
From task_001, step 5 summarizes the AntiSMASH validation: in local mode, check if antismash directory exists; in PODP mode, download and extract if missing/invalid with up to 2 retries. This is performed within NPLinker's DatasetArranger initialization before DatasetLoader consumes the prepared data.
```

## Evaluation signals

- For local mode: antismash directory path exists on the filesystem and contains valid AntiSMASH output files (e.g., GBK or JSON BGC predictions).
- For PODP mode: antismash data is successfully downloaded and extracted; directory structure matches expected layout after extraction.
- Validation passes without raising ConfigurationError or DataValidationError, and the antismash directory path is recorded in the DatasetArranger state.
- If retries are triggered (PODP mode with invalid data), exactly 2 retry attempts are performed before failing or succeeding.
- The validated antismash directory can be successfully ingested by NPLinker's DatasetLoader without missing or malformed BGC data files.

## Limitations

- For local mode, this skill assumes the user has already run AntiSMASH and placed results in the configured directory; it does not execute AntiSMASH itself.
- PODP mode depends on network connectivity and the availability of remote PODP repositories; download failures cannot be recovered without manual intervention after 2 retries.
- The skill validates directory structure and presence but does not deeply inspect individual BGC files for biological correctness or completeness of gene cluster annotations.
- If both local and PODP configurations are malformed or missing, the skill will raise an error and halt; there is no fallback mode.

## Evidence

- [other] antismash directory contains a collection of AntiSMASH BGC data: "antismash directory contains a collection of AntiSMASH BGC data"
- [other] For AntiSMASH data: if in local mode and directory missing, raise an error; if in podp mode and invalid, download and extract (retry up to 2 times).: "For AntiSMASH data: if in local mode and directory missing, raise an error; if in podp mode and invalid, download and extract (retry up to 2 times)."
- [other] Check Dynaconf config validation; if it fails, raise a configuration error.: "Check Dynaconf config validation; if it fails, raise a configuration error."
- [other] Return a validated arrangement of all input directories and configuration ready for DatasetLoader consumption.: "Return a validated arrangement of all input directories and configuration ready for DatasetLoader consumption."
