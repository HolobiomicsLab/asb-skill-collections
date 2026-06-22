---
name: qr-code-generation-and-embedding
description: Use when you need to publish metabolomics spectra in static media (PDF, print, supplementary tables) and want readers or automated systems to access the corresponding interactive spectrum visualization without manual lookup.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3359
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - GNPS Molecular Networking
  - MassBank
  - MetaboLights
  - Metabolomics Workbench
  - QR Code Generation Library
  - MetabolomicsSpectrumResolver
  techniques:
  - LC-MS
derived_from:
- doi: 10.1101/2020.05.09.086066
  title: Metabolomics Spectrum Resolver
evidence_spans:
- GNPS Molecular Networking Clustered Spectra
- MassBank Library Spectra
- MetaboLights Dataset Spectra
- Metabolomics Workbench Dataset Spectra
- 3rd party embedding of QR code
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

# QR code generation and embedding

## Summary

Generate QR codes that encode Universal Spectrum Identifiers (USIs) pointing to metabolomics spectrum data, enabling third-party embedding of machine-readable references into publications and supplementary materials. This skill bridges static publication media with interactive spectrum visualization by encoding resolver URLs that dereference to specific spectra across metabolomics repositories.

## When to use

Use this skill when you need to publish metabolomics spectra in static media (PDF, print, supplementary tables) and want readers or automated systems to access the corresponding interactive spectrum visualization without manual lookup. Specifically when you have resolved USI identifiers from supported sources (GNPS, MassBank, MetaboLights, Metabolomics Workbench, ProteoXchange, MS2LDA) and need to embed machine-readable spectrum references that link directly to the resolver endpoint.

## When NOT to use

- Input USI is unresolved or malformed (does not conform to mzspec/mzdata syntax for a supported source)
- Target audience lacks QR code scanning capability or the publication medium cannot embed raster/vector images
- The spectrum data source is not supported by the resolver (outside GNPS, MassBank, MetaboLights, Metabolomics Workbench, ProteoXchange, MS2LDA)

## Inputs

- Universal Spectrum Identifier (USI) string (fully qualified, e.g., mzspec:SOURCE:dataset:index:scan_number)
- Base resolver endpoint URL (e.g., https://metabolomics-usi.ucsd.edu/spectrum/)
- Target format preference (PNG or SVG)

## Outputs

- QR code image file (PNG or SVG format)
- Embeddable QR code suitable for publication or supplementary material
- Encoded resolver URL within the QR code

## How to apply

Accept a fully qualified USI string as input (e.g., 'mzspec:GNPS:GNPS-LIBRARY:accession:CCMSLIB00005436077' or 'mzspec:MASSBANK::accession:SM858102'). Construct the resolver URL by appending the USI to the base MetabolomicsSpectrumResolver endpoint (e.g., 'https://metabolomics-usi.ucsd.edu/spectrum/?usi=[USI]'). Pass this resolver URL to a QR code generation library (e.g., pyqrcode or qrcode Python packages) to encode the full URL as a 2D barcode. Generate the QR code output in a publication-compatible format (PNG or SVG). Embed the resulting QR code image as a figure, table cell, or supplementary element alongside the spectrum metadata or caption. Verify that scanning the QR code or copying the embedded resolver URL successfully redirects to the interactive spectrum viewer.

## Related tools

- **MetabolomicsSpectrumResolver** (Resolves USI identifiers to spectrum data and provides the base resolver endpoint that QR codes encode) — https://github.com/mwang87/MetabolomicsSpectrumResolver
- **QR Code Generation Library** (Encodes the resolver URL as a 2D barcode in PNG or SVG format)
- **GNPS Molecular Networking** (Source repository for clustered spectra USI references)
- **MassBank** (Source repository for library spectra USI references)
- **MetaboLights** (Source repository for dataset spectra USI references)
- **Metabolomics Workbench** (Source repository for dataset spectra USI references)

## Examples

```
https://metabolomics-usi.ucsd.edu/qrcode/?usi=mzspec:GNPS:GNPS-LIBRARY:accession:CCMSLIB00005436077
```

## Evaluation signals

- QR code image is valid and scannable by standard QR readers
- Scanning the QR code or manually extracting and visiting the encoded URL successfully resolves to the MetabolomicsSpectrumResolver endpoint with the correct USI parameter
- The resolver endpoint returns a valid spectrum visualization or metadata for the encoded USI
- QR code output format matches the requested type (PNG or SVG) and is embeddable in the target publication/medium
- The encoded USI string is preserved exactly (no truncation, corruption, or character encoding errors) in the QR code URL

## Limitations

- USI identifiers are based on draft USI and draft Metabolomics USI standards and are subject to change; currently designated as 'mzdraft' instead of 'mzspec' in some contexts
- QR code generation and embedding success depends on compatibility of the target publication format with image embedding (e.g., some legacy PDF or plain text formats may not support QR visualization)
- End-user access to the interactive spectrum visualization requires network connectivity and access to the MetabolomicsSpectrumResolver service; offline readers cannot follow the embedded link

## Evidence

- [other] The tool achieves 3rd-party embedding of QR codes as one of its core objectives, allowing external systems to embed QR codes that reference USI identifiers from supported metabolomics data sources.: "The tool achieves 3rd-party embedding of QR codes as one of its core objectives, allowing external systems to embed QR codes that reference USI identifiers from supported metabolomics data sources."
- [other] Accept a USI string (dataset identifier, spectrum index, and optional library reference) as input. Construct the resolver URL by appending the USI to the base USI resolver endpoint. Generate a QR code image that encodes this resolver URL using a QR code library. Return the QR code as an embeddable image file (PNG or SVG format) suitable for third-party integration into publications.: "Accept a USI string (dataset identifier, spectrum index, and optional library reference) as input. Construct the resolver URL by appending the USI to the base USI resolver endpoint. Generate a QR"
- [intro] 3rd party embedding of QR code.: "3rd party embedding of QR code."
- [readme] These identifiers are based on draft USI and draft Metabolomics USI identifiers. Thus, they are subject to change, and so for the moment, they will be specified as `mzdraft` instead of `mzspec` in the first block.: "These identifiers are based on draft USI and draft Metabolomics USI identifiers. Thus, they are subject to change, and so for the moment, they will be specified as `mzdraft` instead of `mzspec` in"
