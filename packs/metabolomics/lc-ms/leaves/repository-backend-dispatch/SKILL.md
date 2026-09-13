---
name: repository-backend-dispatch
description: Use when when you have a USI string (e.g., 'mzspec:GNPS:TASK-abc123:scan:1943')
  and need to retrieve the underlying spectrum data from its native repository without
  knowing a priori which backend stores it.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - GNPS Molecular Networking
  - ProteoXchange Repository
  - MassBank
  - MetaboLights
  - Metabolomics Workbench
  - MS2LDA
  - GNPS Spectral Libraries
  - MassIVE
  - MetabolomicsSpectrumResolver
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1101/2020.05.09.086066
  title: Metabolomics Spectrum Resolver
evidence_spans:
- GNPS Molecular Networking Clustered Spectra
- ProteoXchange Repository Data
- MassBank Library Spectra
- MetaboLights Dataset Spectra
- Metabolomics Workbench Dataset Spectra
- MS2LDA Reference Motifs
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metabolomics_spectrum_resolver_cq
    doi: 10.1101/2020.05.09.086066
    title: Metabolomics Spectrum Resolver
  dedup_kept_from: coll_metabolomics_spectrum_resolver_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2020.05.09.086066
  all_source_dois:
  - 10.1101/2020.05.09.086066
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Repository Backend Dispatch

## Summary

Route a Uniform Spectrum Identifier (USI) to the correct metabolomics data source backend and retrieve the corresponding spectrum data in standardized format. This skill enables transparent access to seven distinct spectrum repositories (GNPS, MassBank, MetaboLights, Metabolomics Workbench, ProteoXchange, MS2LDA, MassIVE) by parsing the USI namespace and dispatching retrieval to the appropriate repository API.

## When to use

When you have a USI string (e.g., 'mzspec:GNPS:TASK-abc123:scan:1943') and need to retrieve the underlying spectrum data from its native repository without knowing a priori which backend stores it. Use this skill as the first step in any workflow that must resolve, visualize, or analyze spectra identified by USI across heterogeneous data sources.

## When NOT to use

- USI string uses an unsupported or draft namespace prefix not in the resolver's mapping table; resolution will fail.
- Spectrum data is already in-memory or cached from a prior retrieval; re-dispatching adds unnecessary latency.
- Input is a non-USI identifier (e.g., raw accession number, scan ID, or filename without namespace context); first convert to valid USI format.

## Inputs

- USI string (mzspec or mzdata format with namespace and resource identifiers)
- Mapping table of supported USI namespace prefixes to backend APIs
- Repository-specific access credentials or API endpoints (if authentication required)

## Outputs

- JSON spectrum object with m/z array, intensity array, precursor m/z, and metadata fields
- Spectrum data in standardized format (m/z–intensity pairs with auxiliary fields)
- Repository provenance (source repository, accession, scan/file reference)

## How to apply

Parse the input USI string to extract its namespace prefix (e.g., 'GNPS', 'MASSBANK', 'MS2LDA') and resource identifier components (task ID, accession, scan number, filename). Match the namespace against the resolver's supported source mapping table (GNPS Molecular Networking, GNPS Spectral Libraries, ProteoXchange Repository, MassBank, MetaboLights, Metabolomics Workbench, MS2LDA). Dispatch the retrieval request to the corresponding repository backend API or data access layer using the parsed identifiers as query parameters. Retrieve and return the spectrum data in standardized JSON format containing m/z values, intensity values, metadata fields (precursor m/z, retention time, compound name), and provenance information. Validate that returned spectra conform to the expected schema and contain non-empty peak lists before downstream processing.

## Related tools

- **GNPS Molecular Networking** (Source backend for GNPS task spectra and clustered spectral data) — https://gnps.ucsd.edu
- **GNPS Spectral Libraries** (Source backend for GNPS library spectrum accessions) — https://gnps.ucsd.edu
- **MassBank** (Source backend for MassBank library spectrum accessions) — https://massbank.eu
- **MetaboLights** (Source backend for MetaboLights dataset spectra by MSV identifier and filename) — https://www.ebi.ac.uk/metabolights
- **Metabolomics Workbench** (Source backend for Metabolomics Workbench dataset spectra by MSV identifier) — https://www.metabolomicsworkbench.org
- **ProteoXchange Repository** (Source backend for proteomics and multi-omics spectrum data via ProteomeXchange identifiers) — http://www.proteomexchange.org
- **MS2LDA** (Source backend for MS2LDA reference motifs and annotations) — https://ms2lda.org
- **MassIVE** (Source backend for MassIVE task and repository spectra (GNPS-integrated)) — https://massive.ucsd.edu
- **MetabolomicsSpectrumResolver** (Reference implementation providing USI parsing, namespace mapping, and backend dispatch logic) — https://github.com/mwang87/MetabolomicsSpectrumResolver

## Evaluation signals

- Returned spectrum JSON conforms to standardized schema (contains 'mz' array, 'intensity' array, 'precursor_mz' number, metadata object)
- Non-empty peak list is returned (mz and intensity arrays have length > 0)
- Metadata fields (compound name, retention time, precursor charge, dataset/file provenance) are populated and match expected type and range
- Dispatch latency is proportional to network round-trip to target repository backend, not to USI parsing or namespace lookup overhead
- Identical USI inputs consistently return identical spectrum data across multiple invocations (idempotency)

## Limitations

- USI identifiers are based on draft specifications ('mzdraft' prefix) and are subject to change; future USI format changes may require resolver updates.
- Resolver supports only seven predefined namespaces; USIs from unlisted repositories (custom databases, newly added sources) cannot be resolved until mapping table is updated.
- Resolution depends on upstream repository availability and API stability; transient outages or breaking changes in repository APIs will cause retrieval failures.
- No built-in retry, caching, or fallback logic; network failures or rate-limiting from target backends are not handled transparently.
- Metadata field coverage varies across source repositories; some backends may return sparse or missing fields (e.g., retention time unavailable in some GNPS tasks or MassBank records).

## Evidence

- [other] The resolver supports seven distinct USI types corresponding to different metabolomics data sources: GNPS Molecular Networking Clustered Spectra, GNPS Spectral Libraries, ProteoXchange Repository Data, MS2LDA Reference Motifs, MassBank Library Spectra, MetaboLights Dataset Spectra, and Metabolomics Workbench Dataset Spectra.: "The resolver supports seven distinct USI types corresponding to different metabolomics data sources: GNPS Molecular Networking Clustered Spectra, GNPS Spectral Libraries, ProteoXchange Repository"
- [other] 1. Parse the input USI to extract its namespace prefix and resource identifier. 2. Match the namespace against a mapping table to identify the supported source repository. 3. Dispatch the retrieval request to the corresponding repository backend API or data access layer. 4. Retrieve and return the spectrum data in a standardized format (e.g., JSON spectrum object with m/z, intensity, metadata fields).: "1. Parse the input USI to extract its namespace prefix and resource identifier. 2. Match the namespace against a mapping table to identify the supported source repository. 3. Dispatch the retrieval"
- [readme] These identifiers are based on draft USI and draft Metabolomics USI identifiers. Thus, they are subject to change, and so for the moment, they will be specified as `mzdraft` instead of `mzspec` in the first block.: "These identifiers are based on draft USI and draft Metabolomics USI identifiers. Thus, they are subject to change"
- [readme] Enable creation of embeddable images in publications that will link out to viewable/interactable spectrum plots. 3rd party embedding for visualization of spectra that exist in repositories (e.g. MassIVE, PRIDE, PeptideAtlas).: "3rd party embedding for visualization of spectra that exist in repositories (e.g. MassIVE, PRIDE, PeptideAtlas)."
