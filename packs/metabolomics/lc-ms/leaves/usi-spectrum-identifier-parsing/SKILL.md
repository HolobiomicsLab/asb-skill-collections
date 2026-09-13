---
name: usi-spectrum-identifier-parsing
description: Use when when you have a USI string (e.g., mzspec:MTBLS1124:QC07.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - GNPS LCMS Visualization Dashboard
  - MetaboLights REST API
  - MassIVE Repository API
  - GNPS Task Resolver
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41592-021-01339-5
  title: GNPS Dashboard
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_gnps_dashboard_cq
    doi: 10.1038/s41592-021-01339-5
    title: GNPS Dashboard
  dedup_kept_from: coll_gnps_dashboard_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41592-021-01339-5
  all_source_dois:
  - 10.1038/s41592-021-01339-5
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# USI Spectrum Identifier Parsing

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Parse Universal Spectrum Identifiers (USIs) to extract repository accession codes and file identifiers, enabling programmatic resolution and retrieval of mass spectrometry data from public repositories like GNPS, MassIVE, and MetaboLights. This skill is essential for automating data discovery and visualization workflows across heterogeneous mass spectrometry data sources.

## When to use

When you have a USI string (e.g., mzspec:MTBLS1124:QC07.mzML or mzspec:MSV000084951:AH22) and need to retrieve the corresponding raw mass spectrometry file from a remote repository, or when you are building a data pipeline that ingests USI-formatted dataset references from documentation, web services, or user input.

## When NOT to use

- Input is already a local file path or downloaded mzML/mzXML file; use spectrum loading instead.
- USI refers to a private or restricted-access dataset for which you lack credentials.
- Target repository API is unavailable or has changed the USI format specification.

## Inputs

- USI string (e.g., mzspec:MTBLS1124:QC07.mzML)
- Repository accession identifier (e.g., MTBLS1124, MSV000084951)
- File identifier or path within repository (e.g., QC07.mzML, AH22)

## Outputs

- Parsed repository prefix (string: MTBLS, MSV, GNPS, etc.)
- Parsed accession code (string)
- Parsed file identifier or path (string)
- Remote download URL (for the resolved file)
- File manifest or metadata (from repository API)

## How to apply

Parse the USI string using the standardized mzspec format to extract three components: the repository prefix (e.g., MTBLS, MSV, GNPS), the repository-specific accession identifier, and the file path or identifier. Use the parsed accession to query the appropriate repository's REST API or download service (MetaboLights REST API for MTBLS, MassIVE for MSV, GNPS task resolver for GNPS) to retrieve the file manifest and locate the target file. Validate that the file format matches the USI specification (mzML, mzXML, etc.) before initiating download. The rationale is that USIs provide a machine-readable, repository-agnostic mechanism for data citation and programmatic access; parsing them enables dynamic resolution across multiple public archives without hardcoding repository-specific URLs.

## Related tools

- **GNPS LCMS Visualization Dashboard** (Provides documentation and live examples of supported USI formats across multiple repositories (GNPS, MassIVE, MetaboLights); used as reference for valid USI structure and resolution) — https://github.com/Wang-Bioinformatics-Lab/GNPS_LCMSDashboard
- **MetaboLights REST API** (Queried using parsed MTBLS accession to retrieve file manifest and metadata for MetaboLights datasets)
- **MassIVE Repository API** (Queried using parsed MSV accession to retrieve file listings and download URLs for MassIVE datasets)
- **GNPS Task Resolver** (Resolves GNPS-prefixed USIs (e.g., mzspec:GNPS:TASK-*) to retrieve analysis task outputs and intermediate data files)

## Evaluation signals

- Parser successfully extracts repository prefix, accession, and file identifier without error; output matches expected regex pattern for each component.
- Parsed accession resolves to a valid repository API endpoint that returns a 200 HTTP response.
- File identifier from parsed USI is found in the file manifest returned by the repository API.
- Remote URL constructed from parsed components is valid and returns the correct file type (mzML, mzXML, etc.) when downloaded.
- Resolved file can be validated against the mzML or mzXML schema, confirming correct data format and integrity.

## Limitations

- USI specification is repository-specific; parsing logic must be implemented separately for each repository prefix (MTBLS, MSV, GNPS) due to different accession formats and API structures.
- Repository APIs may be subject to rate limiting or may require authentication; no fallback is specified if the primary repository is unavailable.
- File paths containing special characters or non-ASCII characters may cause parsing ambiguities; USI spec compliance for such edge cases is not addressed in the article.
- USIs referencing deleted or moved datasets may return 404 or stale metadata; no validation of dataset currency is performed during parsing.

## Evidence

- [other] Parse the USI string mzspec:MTBLS1124:QC07.mzML to extract the MetaboLights accession (MTBLS1124) and file identifier (QC07.mzML).: "Parse the USI string mzspec:MTBLS1124:QC07.mzML to extract the MetaboLights accession (MTBLS1124) and file identifier (QC07.mzML)."
- [other] Query the MetaboLights REST API or download service using accession MTBLS1124 to retrieve the file manifest and locate QC07.mzML.: "Query the MetaboLights REST API or download service using accession MTBLS1124 to retrieve the file manifest and locate QC07.mzML."
- [other] GNPS LCMS Visualization Dashboard documentation lists mzspec:MTBLS1124:QC07.mzML as an example MetaboLights public dataset source, indicating this USI format is supported for dataset retrieval and visualization.: "GNPS LCMS Visualization Dashboard documentation lists mzspec:MTBLS1124:QC07.mzML as an example MetaboLights public dataset source"
- [readme] Since we utilize a USI to find datasets, there are a limited number of locations we can grab data from.: "Since we utilize a USI to find datasets, there are a limited number of locations we can grab data from."
- [readme] Update the code in download.py, specifically in _resolve_usi_remotelink to implement how to get the remote URL for your new USI.: "Update the code in download.py, specifically in _resolve_usi_remotelink to implement how to get the remote URL for your new USI."
