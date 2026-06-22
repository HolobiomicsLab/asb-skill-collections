---
name: conditional-routing-logic
description: Use when you have received a USI string (formatted as mzspec:<namespace>:<resource>:<identifier_type>:<identifier>) and need to retrieve the corresponding mass spectrum data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3282
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - GNPS Molecular Networking
  - MassBank
  - MetaboLights
  - Metabolomics Workbench
  - MS2LDA
  - GNPS Spectral Libraries
  - ProteoXchange Repository
  - MetabolomicsSpectrumResolver
derived_from:
- doi: 10.1101/2020.05.09.086066
  title: Metabolomics Spectrum Resolver
evidence_spans:
- GNPS Molecular Networking Clustered Spectra
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Conditional Routing Logic

## Summary

Route a Universal Spectrum Identifier (USI) to the correct metabolomics data source backend by parsing its namespace prefix and matching it against a repository mapping table. This skill enables transparent retrieval of spectrum data from heterogeneous sources (GNPS, MassBank, MetaboLights, Metabolomics Workbench, ProteoXchange, MS2LDA) through a unified interface.

## When to use

You have received a USI string (formatted as mzspec:<namespace>:<resource>:<identifier_type>:<identifier>) and need to retrieve the corresponding mass spectrum data. Use this skill when the source repository is unknown or variable, and you must dispatch the request to the correct backend without manual intervention.

## When NOT to use

- Input is already a parsed spectrum object or raw mass spectrometry data file (e.g., mzML, mzXML) — use data loading/parsing instead.
- The USI namespace is not in the supported list (GNPS, MASSBANK, MS2LDA, MOTIFDB, MassIVE, PXD, MetaboLights, Metabolomics Workbench) — routing will fail; confirm source support first.
- You need to retrieve multiple spectra in bulk — consider batch routing or direct repository API access for performance.

## Inputs

- USI string (mzspec:<namespace>:<resource>:<identifier_type>:<identifier>)
- USI namespace-to-repository mapping table
- Connection credentials or API endpoints for each supported repository

## Outputs

- Spectrum object (JSON format with m/z values, intensities, and metadata)
- HTTP response with spectrum data or error status code

## How to apply

Parse the input USI to extract the namespace prefix (the second colon-delimited field, e.g., 'GNPS', 'MASSBANK', 'MS2LDA'). Match this namespace against a maintained mapping table of supported sources to identify the target repository. Construct and dispatch a retrieval request to that repository's backend API or data access layer, using the resource identifier and identifier type from the USI. Retrieve the spectrum data in standardized format (JSON spectrum object with m/z array, intensity array, and metadata fields). The resolver supports seven distinct namespaces; if the namespace is not in the mapping table, the resolver should fail gracefully with an unsupported source error.

## Related tools

- **GNPS Molecular Networking** (Data source for clustered spectra from networking analysis tasks; dispatched via GNPS namespace in USI) — https://gnps.ucsd.edu
- **GNPS Spectral Libraries** (Data source for library spectra; dispatched via GNPS-LIBRARY namespace in USI) — https://gnps.ucsd.edu
- **MassBank** (Data source for reference mass spectra library; dispatched via MASSBANK namespace in USI) — https://massbank.eu
- **MetaboLights** (Data source for metabolomics dataset spectra; dispatched via MSV identifier in USI) — https://www.ebi.ac.uk/metabolights
- **Metabolomics Workbench** (Data source for metabolomics repository spectra; dispatched via MSV identifier in USI) — https://www.metabolomicsworkbench.org
- **ProteoXchange Repository** (Data source for proteomics and cross-domain mass spec data; dispatched via PXD namespace in USI) — http://www.proteomexchange.org
- **MS2LDA** (Data source for reference motifs; dispatched via MS2LDA or MOTIFDB namespace in USI)
- **MetabolomicsSpectrumResolver** (Primary implementation of conditional routing logic; orchestrates dispatch to all seven sources) — https://github.com/mwang87/MetabolomicsSpectrumResolver

## Examples

```
curl 'https://metabolomics-usi.ucsd.edu/json/?usi=mzspec:MASSBANK::accession:SM858102' | jq '.spectrum'
```

## Evaluation signals

- The namespace extracted from the USI matches one of the seven supported sources and is present in the mapping table.
- The resolver successfully dispatches the request to the correct repository backend without timeouts or authentication errors.
- The returned spectrum object contains required fields: m/z array, intensity array, and at least one metadata field (e.g., precursor m/z, charge state, retention time).
- Round-trip test: parsing a known USI (e.g., 'mzspec:MASSBANK::accession:SM858102') produces spectrum data with non-empty peak lists.
- Namespace mismatch or unsupported prefix results in a predictable error response (HTTP 4xx or explicit unsupported source message), not silent failure or null return.

## Limitations

- USI identifiers are based on draft metabolomics USI standard and may change; identifiers currently use 'mzdraft' prefix instead of 'mzspec' in some contexts, requiring version management.
- Resolver supports only seven discrete sources; repositories not in the mapping (e.g., custom institutional repositories) cannot be resolved.
- Network latency and availability of individual repository backends directly affect resolution time; no caching or fallback mechanisms are mentioned.
- Complex USI patterns (e.g., file-scoped vs. collection-scoped GNPS tasks) require distinct parsing logic; edge cases may not be handled in all dispatchers.

## Evidence

- [other] Parse the input USI to extract its namespace prefix and resource identifier: "Parse the input USI to extract its namespace prefix and resource identifier."
- [other] The resolver supports seven distinct USI types corresponding to different metabolomics data sources: "The resolver supports seven distinct USI types corresponding to different metabolomics data sources: GNPS Molecular Networking Clustered Spectra, GNPS Spectral Libraries, ProteoXchange Repository"
- [other] Match the namespace against a mapping table to identify the supported source repository: "Match the namespace against a mapping table to identify the supported source repository."
- [other] Dispatch the retrieval request to the corresponding repository backend API or data access layer: "Dispatch the retrieval request to the corresponding repository backend API or data access layer."
- [other] Retrieve and return the spectrum data in a standardized format (e.g., JSON spectrum object with m/z, intensity, metadata fields): "Retrieve and return the spectrum data in a standardized format (e.g., JSON spectrum object with m/z, intensity, metadata fields)."
- [readme] These identifiers are based on draft USI and draft Metabolomics USI identifiers. Thus, they are subject to change: "These identifiers are based on draft USI and draft Metabolomics USI identifiers. Thus, they are subject to change, and so for the moment, they will be specified as `mzdraft` instead of `mzspec`."
- [readme] Enable creation of embeddable images in publications that will link out to viewable/interactable spectrum plots: "Enable creation of embeddable images in publications that will link out to viewable/interactable spectrum plots."
