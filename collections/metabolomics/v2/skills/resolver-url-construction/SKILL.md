---
name: resolver-url-construction
description: Use when when you have a USI string (comprising dataset identifier, spectrum index, and optional library reference) and need to generate a stable, machine-readable link that resolves to interactive spectrum visualization or programmatic access.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0337
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - QR Code Generation Library
  - GNPS Molecular Networking
  - MassBank
  - MetaboLights
  - Metabolomics Workbench
  - ProteomeXchange Repository
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# resolver-url-construction

## Summary

Construct resolver URLs that encode Unified Spectrum Identifiers (USIs) for metabolomics data, enabling standardized linking to spectrum data across distributed repositories. This skill transforms a structured USI string into a resolvable HTTP endpoint that third-party systems can embed in publications or data pipelines.

## When to use

When you have a USI string (comprising dataset identifier, spectrum index, and optional library reference) and need to generate a stable, machine-readable link that resolves to interactive spectrum visualization or programmatic access. Use this skill when publishing results that reference spectra in GNPS, MassBank, MetaboLights, Metabolomics Workbench, or ProteomeXchange, or when building automated pipelines that must reference spectra by persistent identifier.

## When NOT to use

- If the spectrum data is stored in a non-standard format or repository not supported by the USI standard (only GNPS, MassBank, MetaboLights, Metabolomics Workbench, ProteomeXchange, MS2LDA, and MOTIFDB are supported).
- If you need to modify or transform the underlying spectrum data itself; this skill only constructs links, it does not manipulate spectra.
- If you are working with draft USI identifiers using the `mzdraft` prefix and require stable, production-grade URLs (the article warns that draft identifiers are subject to change).

## Inputs

- USI string (e.g., 'mzspec:GNPS:GNPS-LIBRARY:accession:CCMSLIB00005436077')
- Base resolver endpoint URL (e.g., 'https://metabolomics-usi.ucsd.edu/spectrum/?usi=')
- Optional query parameters (mz_min, mz_max, width, height, plot_title)

## Outputs

- Resolver URL suitable for HTTP GET request
- Embedded spectrum visualization link for publications
- Machine-readable USI reference endpoint

## How to apply

Accept the USI as input—for example, `mzspec:GNPS:GNPS-LIBRARY:accession:CCMSLIB00005436077` or `mzspec:MASSBANK::accession:SM858102`. Append the entire USI string to the base resolver endpoint (e.g., `https://metabolomics-usi.ucsd.edu/spectrum/?usi=`). The resolver accepts multiple USI formats (GNPS tasks, GNPS libraries, MassBank accessions, MetaboLights/Metabolomics Workbench datasets, ProteomeXchange repositories, MS2LDA motifs). Validate the USI format against the documented schema for your source type before construction. Return the complete URL as the resolver endpoint; this URL can then be embedded in publications, QR codes, or passed to downstream visualization or JSON/CSV export endpoints. The resolver supports optional query parameters for filtering (e.g., `mz_min`, `mz_max`) and rendering (e.g., `width`, `height`, `plot_title`).

## Related tools

- **QR Code Generation Library** (Encodes the constructed resolver URL into a QR code image (PNG or SVG) for embedding in publications)
- **GNPS Molecular Networking** (Source repository for clustered spectra referenced by USI)
- **MassBank** (Source library spectra referenced by USI accession)
- **MetaboLights** (Source dataset spectra referenced by USI dataset identifier)
- **Metabolomics Workbench** (Source dataset spectra referenced by USI dataset identifier)
- **ProteomeXchange Repository** (Source proteomics spectra referenced by USI PXD identifier)

## Examples

```
https://metabolomics-usi.ucsd.edu/spectrum/?usi=mzspec:GNPS:GNPS-LIBRARY:accession:CCMSLIB00005436077
```

## Evaluation signals

- The constructed URL follows the pattern `<base_endpoint>?usi=<USI_string>` and is resolvable via HTTP GET.
- The USI string component is preserved exactly as input (no URL-encoding corruption or truncation).
- When the URL is accessed, it returns a valid spectrum visualization (SVG, PNG, or JSON) or HTTP 200 with appropriate spectrum metadata.
- The resolved endpoint matches the documented USI format for the source type (e.g., GNPS library accessions contain 'CCMSLIB', MassBank accessions contain 'SM' or 'AU' prefix).
- Optional query parameters (if provided) are correctly appended and honored by the resolver (e.g., `mz_min` and `mz_max` filter the mass range in the visualization).

## Limitations

- Draft USI identifiers use the `mzdraft` prefix instead of `mzspec` and are subject to change; the article warns these are not yet stable.
- Only USI types for supported repositories (GNPS, MassBank, MetaboLights, Metabolomics Workbench, ProteomeXchange, MS2LDA, MOTIFDB) can be resolved; arbitrary spectrum identifiers cannot be constructed.
- The resolver does not validate the existence of the spectrum before returning the URL; a malformed or non-existent USI will construct a valid URL that may fail at resolution time.
- No changelog is documented for the resolver tool, so breaking changes to USI format or endpoint behavior may not be announced.

## Evidence

- [other] 1. Accept a USI string (dataset identifier, spectrum index, and optional library reference) as input. 2. Construct the resolver URL by appending the USI to the base USI resolver endpoint.: "Accept a USI string (dataset identifier, spectrum index, and optional library reference) as input. 2. Construct the resolver URL by appending the USI to the base USI resolver endpoint."
- [intro] 3rd party embedding of QR code that encode USI/spectrum references: "3rd party embedding of QR code"
- [intro] Enable creation of embeddable images in publications that will link out to viewable/interactable spectrum plots.: "Enable creation of embeddable images in publications that will link out to viewable/interactable spectrum plots."
- [readme] Supported USI Types: 1. GNPS Molecular Networking Clustered Spectra 2. GNPS Spectral Libraries 3. ProteoXchange Repository Data 4. MS2LDA Reference Motifs 5. MassBank Library Spectra 6. MetaboLights Dataset Spectra 7. Metabolomics Workbench Dataset Spectra: "Supported USI Types: 1. GNPS Molecular Networking Clustered Spectra 2. GNPS Spectral Libraries 3. ProteoXchange Repository Data 4. MS2LDA Reference Motifs 5. MassBank Library Spectra 6. MetaboLights"
- [readme] These identifiers are based on draft USI and draft Metabolomics USI identifiers. Thus, they are subject to change, and so for the moment, they will be specified as `mzdraft` instead of `mzspec`: "These identifiers are based on draft USI and draft Metabolomics USI identifiers. Thus, they are subject to change, and so for the moment, they will be specified as `mzdraft` instead of `mzspec`"
