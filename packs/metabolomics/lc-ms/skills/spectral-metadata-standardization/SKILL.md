---
name: spectral-metadata-standardization
description: Use when you have mass spectrometry spectra stored across multiple, disparate metabolomics repositories (GNPS, MassBank, MetaboLights, Metabolomics Workbench, ProteoXchange, MS2LDA) and need to retrieve them using a single identifier scheme, or you are publishing spectrum figures and need.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_0091
  tools:
  - GNPS Molecular Networking
  - GNPS Spectral Libraries
  - MassBank
  - MetaboLights
  - Metabolomics Workbench
  - MS2LDA
  - ProteoXchange Repository
  - MetabolomicsSpectrumResolver
  - openNAU
  - MetaQC
  techniques:
  - LC-MS
derived_from:
- doi: 10.1101/2020.05.09.086066
  title: Metabolomics Spectrum Resolver
- doi: 10.21147/j.issn.1000-9604.2023.05.11
  title: ''
evidence_spans:
- GNPS Molecular Networking Clustered Spectra
- GNPS Spectral Libraries
- MassBank Library Spectra
- MetaboLights Dataset Spectra
- Metabolomics Workbench Dataset Spectra
- MS2LDA Reference Motifs
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_matchms
    doi: 10.1186/s13321-024-00878-1
    title: matchms
  - build: coll_metabolomics_spectrum_resolver_cq
    doi: 10.1101/2020.05.09.086066
    title: Metabolomics Spectrum Resolver
  - build: coll_opennau_cq
    doi: 10.21147/j.issn.1000-9604.2023.05.11
    title: OpenNAU
  dedup_kept_from: coll_metabolomics_spectrum_resolver_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2020.05.09.086066
  all_source_dois:
  - 10.1101/2020.05.09.086066
  - 10.21147/j.issn.1000-9604.2023.05.11
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-metadata-standardization

## Summary

Standardize and normalize mass spectrometry spectral metadata across heterogeneous metabolomics repositories by parsing Universal Spectrum Identifiers (USIs) into a unified namespace-to-source mapping and retrieving spectrum data in a standardized JSON format. This skill enables consistent cross-repository spectrum retrieval and embedding for publication and analysis workflows.

## When to use

You have mass spectrometry spectra stored across multiple, disparate metabolomics repositories (GNPS, MassBank, MetaboLights, Metabolomics Workbench, ProteoXchange, MS2LDA) and need to retrieve them using a single identifier scheme, or you are publishing spectrum figures and need embeddable, machine-readable metadata that links to the underlying repository data.

## When NOT to use

- Your spectra are already in a single, proprietary repository format with no need for cross-repository queries or embedding.
- You require real-time spectral data retrieval from sources not yet supported by the USI resolver (the README lists only seven specific types).
- Your use case requires modification of spectral annotations or metadata beyond standard filtering (m/z range, intensity scaling); the resolver is a read-only retrieval and visualization tool.

## Inputs

- Universal Spectrum Identifier (USI) string in mzspec format (e.g., 'mzspec:GNPS:GNPS-LIBRARY:accession:CCMSLIB00005436077')
- Namespace prefix and resource identifier components (e.g., repository type, dataset ID, scan number, accession)

## Outputs

- Standardized JSON spectrum object with m/z array, intensity array, and metadata fields
- Embedded spectrum visualization (SVG, PNG, or QR code) suitable for publication
- Machine-readable spectrum data in JSON, CSV, or ProXI format for downstream analysis

## How to apply

Parse the input USI string to extract its namespace prefix (e.g., 'GNPS', 'MASSBANK', 'MS2LDA') and resource identifier components. Match the namespace against a predefined mapping table to identify the supported source repository and dispatch the retrieval request to the corresponding repository backend API or data access layer. Retrieve and return the spectrum data in a standardized JSON format containing m/z values, intensity values, and associated metadata fields (e.g., compound name, collision energy, precursor m/z). Validate that all required metadata fields are present and that numeric values (m/z, intensity) are within expected ranges. The rationale is that metabolomics repositories have heterogeneous data schemas and access protocols; standardizing on USI format and JSON output enables downstream tools to consume spectral data uniformly without repository-specific parsing logic.

## Related tools

- **GNPS Molecular Networking** (Source repository for clustered spectra accessed via USI namespace 'GNPS')
- **GNPS Spectral Libraries** (Source repository for library spectra accessed via USI namespace 'GNPS' with 'GNPS-LIBRARY' identifier)
- **MassBank** (Source repository for library spectra accessed via USI namespace 'MASSBANK')
- **MetaboLights** (Source repository for dataset spectra accessed via MetaboLights MSV identifiers)
- **Metabolomics Workbench** (Source repository for dataset spectra accessed via Metabolomics Workbench MSV identifiers)
- **ProteoXchange Repository** (Source repository for proteomics data accessed via USI namespace 'PXD')
- **MS2LDA** (Source repository for reference motifs accessed via USI namespace 'MS2LDA')
- **MetabolomicsSpectrumResolver** (Reference implementation of USI parsing, namespace-to-source dispatch, and spectrum retrieval workflow) — https://github.com/mwang87/MetabolomicsSpectrumResolver

## Examples

```
curl 'https://metabolomics-usi.ucsd.edu/json/?usi=mzspec:GNPS:GNPS-LIBRARY:accession:CCMSLIB00005436077'
```

## Evaluation signals

- USI parse succeeds: input USI string is split into namespace prefix, resource identifier, and scan/accession components without error.
- Namespace mapping succeeds: the extracted namespace prefix is matched to a supported repository and the correct backend API endpoint is identified.
- Spectrum retrieval succeeds: the backend API returns a spectrum record with non-null m/z and intensity arrays of equal length.
- JSON output schema is valid: returned spectrum object contains required fields (m/z, intensity, metadata) and numeric arrays conform to expected ranges (m/z > 0, intensity ≥ 0).
- Embeddable visualization renders: SVG, PNG, or QR code output is generated and can be embedded in HTML/Markdown documents without malformation.

## Limitations

- Only seven USI namespace types are supported (GNPS, MASSBANK, MOTIFDB, MS2LDA, MetaboLights, Metabolomics Workbench, ProteoXchange); queries for unmapped repositories will fail.
- The USI format specification is currently draft ('mzdraft' prefix) and subject to change, creating potential fragility for long-term data linking.
- Backend repository availability and API stability are not guaranteed; network timeouts or API changes will cause retrieval failures.
- Metadata completeness varies by repository and source; standardized JSON output may contain null or missing fields for optional metadata (e.g., collision energy, compound name).

## Evidence

- [other] The resolver supports seven distinct USI types corresponding to different metabolomics data sources: GNPS Molecular Networking Clustered Spectra, GNPS Spectral Libraries, ProteoXchange Repository Data, MS2LDA Reference Motifs, MassBank Library Spectra, MetaboLights Dataset Spectra, and Metabolomics Workbench Dataset Spectra.: "The resolver supports seven distinct USI types corresponding to different metabolomics data sources: GNPS Molecular Networking Clustered Spectra, GNPS Spectral Libraries, ProteoXchange Repository"
- [other] Parse the input USI to extract its namespace prefix and resource identifier. Match the namespace against a mapping table to identify the supported source repository. Dispatch the retrieval request to the corresponding repository backend API or data access layer. Retrieve and return the spectrum data in a standardized format (e.g., JSON spectrum object with m/z, intensity, metadata fields).: "Parse the input USI to extract its namespace prefix and resource identifier. Match the namespace against a mapping table to identify the supported source repository. Dispatch the retrieval request to"
- [readme] Enable creation of embeddable images in publications that will link out to viewable/interactable spectrum plots.: "Enable creation of embeddable images in publications that will link out to viewable/interactable spectrum plots."
- [readme] These identifiers are based on draft USI and draft Metabolomics USI identifiers. Thus, they are subject to change, and so for the moment, they will be specified as `mzdraft` instead of `mzspec` in the first block.: "These identifiers are based on draft USI and draft Metabolomics USI identifiers. Thus, they are subject to change"
