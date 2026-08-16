---
name: usi-spectrum-identifier-encoding
description: Use when you have a Universal Spectrum Identifier (USI) string referencing
  a spectrum in a supported metabolomics repository (GNPS, MassBank, MetaboLights,
  Metabolomics Workbench, MassIVE, or MS2LDA) and need to create an embeddable, scannable
  reference for publication or data integration that.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3359
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - QR Code Generation Library
  - USI Resolver and Displayer
  - GNPS Spectral Libraries
  - MassBank
  - MetaboLights
  - Metabolomics Workbench
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1101/2020.05.09.086066
  title: Metabolomics Spectrum Resolver
evidence_spans: []
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

# USI Spectrum Identifier Encoding

## Summary

Encode metabolomics spectrum identifiers (USI) into QR codes that resolve to interactive spectrum visualization endpoints. This enables third-party embedding of spectrum references in publications and repositories via standard URL resolution.

## When to use

You have a Universal Spectrum Identifier (USI) string referencing a spectrum in a supported metabolomics repository (GNPS, MassBank, MetaboLights, Metabolomics Workbench, MassIVE, or MS2LDA) and need to create an embeddable, scannable reference for publication or data integration that links to a viewable/interactive spectrum plot.

## When NOT to use

- USI string is malformed or references an unsupported data source (not GNPS, MassBank, MetaboLights, Metabolomics Workbench, MassIVE, MS2LDA, MOTIFDB, or ProteomeXchange).
- The target spectrum does not exist in the referenced repository or has been deleted/archived.
- You require direct spectrum data export (binary or text) rather than a resolver link; use JSON or CSV endpoints instead.

## Inputs

- USI string (Universal Spectrum Identifier in mzspec or mzdraft format)
- USI source type (GNPS, MassBank, MetaboLights, Metabolomics Workbench, MassIVE, MS2LDA, MOTIFDB, ProteomeXchange)
- Optional output format preference (PNG or SVG)

## Outputs

- QR code image file (PNG or SVG format)
- Resolver URL string (embeddable endpoint)
- Embedded spectrum visualization link

## How to apply

Accept a valid USI string formatted as mzspec:<source>:<dataset>:<index_type>:<index_value> (e.g., mzspec:GNPS:GNPS-LIBRARY:accession:CCMSLIB00005436077). Construct the resolver endpoint URL by appending the USI to the base metabolomics USI resolver (metabolomics-usi.ucsd.edu). Pass this URL to a QR code generation library to produce an image encoding the resolver URL. Return the QR code as PNG or SVG, suitable for embedding in publication figures, supplementary materials, or data repository metadata. Validate the USI format against supported source schemas (MASSBANK, GNPS, MOTIFDB, MassIVE, MetaboLights, Metabolomics Workbench, PXD identifiers) before encoding.

## Related tools

- **QR Code Generation Library** (Encodes resolver URL into a QR code image for third-party embedding)
- **USI Resolver and Displayer** (Resolves USI strings to interactive spectrum visualization endpoints and handles multiple metabolomics data sources) — github.com/mwang87/MetabolomicsSpectrumResolver
- **GNPS Spectral Libraries** (Supported source for USI identifiers (GNPS-LIBRARY accessions))
- **MassBank** (Supported source for USI identifiers (MASSBANK accessions))
- **MetaboLights** (Supported source for USI identifiers (MSV dataset identifiers))
- **Metabolomics Workbench** (Supported source for USI identifiers (MSV dataset identifiers))

## Evaluation signals

- QR code image decodes to a valid resolver URL matching the pattern https://metabolomics-usi.ucsd.edu/spectrum/?usi=<USI_STRING>
- USI string in the encoded URL matches the input USI exactly (no truncation or format corruption)
- QR code can be scanned by standard QR code readers and resolves to a live spectrum visualization page
- Output image format (PNG or SVG) is valid and renders without errors in standard viewers
- The resolver endpoint returns HTTP 200 and displays the requested spectrum when the QR code is scanned or URL is visited directly

## Limitations

- USI identifiers are based on draft specifications (mzdraft prefix) and are subject to change; format stability is not guaranteed.
- The resolver only works for spectra that exist in the supported repositories at the time of QR code generation; deleted or moved spectra will result in broken links.
- Resolver endpoint availability depends on external repository infrastructure (GNPS, MassBank, etc.) and network connectivity.
- QR code size and error correction level may need adjustment for printed vs. digital embedding; no adaptive sizing parameters are documented in the README.

## Evidence

- [readme] Enable creation of embeddable images in publications that will link out to viewable/interactable spectrum plots.: "Enable creation of embeddable images in publications that will link out to viewable/interactable spectrum plots."
- [readme] 3rd party embedding of QR code.: "3rd party embedding of QR code."
- [other] Accept a USI string (dataset identifier, spectrum index, and optional library reference) as input. Construct the resolver URL by appending the USI to the base USI resolver endpoint. Generate a QR code image that encodes this resolver URL using a QR code library. Return the QR code as an embeddable image file (PNG or SVG format) suitable for third-party integration into publications.: "Accept a USI string (dataset identifier, spectrum index, and optional library reference) as input. Construct the resolver URL by appending the USI to the base USI resolver endpoint. Generate a QR"
- [readme] These identifiers are based on draft USI and draft Metabolomics USI identifiers. Thus, they are subject to change, and so for the moment, they will be specified as `mzdraft` instead of `mzspec` in the first block.: "These identifiers are based on draft USI and draft Metabolomics USI identifiers. Thus, they are subject to change, and so for the moment, they will be specified as `mzdraft` instead of `mzspec` in"
- [readme] Supported USI Types: 1. GNPS Molecular Networking Clustered Spectra 2. GNPS Spectral Libraries 3. ProteoXchange Repository Data 4. MS2LDA Reference Motifs 5. MassBank Library Spectra 6. MetaboLights Dataset Spectra 7. Metabolomics Workbench Dataset Spectra: "Supported USI Types: 1. GNPS Molecular Networking Clustered Spectra 2. GNPS Spectral Libraries 3. ProteoXchange Repository Data 4. MS2LDA Reference Motifs 5. MassBank Library Spectra 6. MetaboLights"
