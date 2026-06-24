---
name: publication-image-asset-preparation
description: Use when you have resolved a USI string pointing to a spectrum in a supported
  repository (GNPS, MassBank, MassIVE, MetaboLights, Metabolomics Workbench, ProteoXchange,
  or MS2LDA) and need to embed a publication-ready visualization or machine-readable
  reference that preserves the spectrum's.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
  tools:
  - QR Code Generation Library
  - GNPS Molecular Networking
  - MassBank
  - MassIVE
  - MetaboLights
  - Metabolomics Workbench
  - MetabolomicsSpectrumResolver
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

# Publication-Image-Asset-Preparation

## Summary

Generate embeddable spectrum visualization images (PNG/SVG) and QR codes from Universal Spectrum Identifiers (USI) that encode references to metabolomics spectral data, enabling direct linking from publications to interactive spectrum viewers in remote repositories.

## When to use

You have resolved a USI string pointing to a spectrum in a supported repository (GNPS, MassBank, MassIVE, MetaboLights, Metabolomics Workbench, ProteoXchange, or MS2LDA) and need to embed a publication-ready visualization or machine-readable reference that preserves the spectrum's persistent identity and links readers to an interactive viewer.

## When NOT to use

- The spectrum identifier is not a valid USI or does not conform to supported metabolomics USI patterns (mzspec/mzdraft prefixed formats from GNPS, MassBank, MassIVE, MetaboLights, Metabolomics Workbench, ProteoXchange, or MS2LDA).
- The target spectrum exists in a repository not supported by the resolver (only GNPS Molecular Networking, GNPS Spectral Libraries, ProteoXchange, MassBank, MetaboLights, Metabolomics Workbench, and MS2LDA are currently supported).
- You need interactive filtering or quantitative analysis of spectral features rather than a static publication image — use the resolver's interactive web interface instead.

## Inputs

- Universal Spectrum Identifier (USI) string (e.g., mzspec:GNPS:TASK-c95481f0c53d42e78a61bf899e9f9adb-spectra/specs_ms.mgf:scan:1943)
- Optional rendering parameters: m/z range (mz_min, mz_max), intensity scaling (max_intensity), annotation settings (annotate_peaks, annotate_precision, annotation_rotation), peak filtering threshold (annotate_threshold), grid visibility, plot title

## Outputs

- SVG spectrum plot image (vector format, resolution-independent)
- PNG spectrum plot image (raster format)
- QR code image (PNG or SVG) encoding resolver URL
- JSON metadata endpoint response
- CSV export of spectrum peaks
- ProXI v0.1 spectra API response

## How to apply

Parse the USI string into its constituent parts: repository identifier, dataset/collection identifier, file reference (if applicable), and spectrum index. Construct a resolver URL by appending the USI to the base metabolomics USI resolver endpoint (https://metabolomics-usi.ucsd.edu/). For visual embeddings, request SVG or PNG output via the /svg/ or /png/ endpoints, optionally specifying display parameters (m/z range, intensity scaling, annotation precision, grid visibility, peak selection, title). For QR code output, invoke the /qrcode/ endpoint to generate a compact, embeddable image encoding the resolver URL. Validate that the USI format matches the supported patterns (e.g., mzspec:GNPS:TASK-<id>-<file>:scan:<n>, mzspec:MASSBANK::accession:<acc>) before rendering, as draft metabolomics USI identifiers may use 'mzdraft' prefix during standardization phases.

## Related tools

- **QR Code Generation Library** (Encodes resolver URLs into embeddable QR codes for publication asset preparation)
- **GNPS Molecular Networking** (Source repository for clustered spectra accessible via USI resolution)
- **MassBank** (Source repository for library reference spectra accessible via USI resolution)
- **MassIVE** (Source repository for mass spectrometry datasets accessible via USI resolution)
- **MetaboLights** (Source repository for metabolomics datasets accessible via USI resolution)
- **Metabolomics Workbench** (Source repository for metabolomics datasets accessible via USI resolution)
- **MetabolomicsSpectrumResolver** (Core resolver service that generates spectrum visualizations and QR codes from USI strings) — https://github.com/mwang87/MetabolomicsSpectrumResolver

## Examples

```
curl 'https://metabolomics-usi.ucsd.edu/svg/?usi=mzspec:GNPS:TASK-c95481f0c53d42e78a61bf899e9f9adb-spectra/specs_ms.mgf:scan:1943&mz_min=550&mz_max=800&width=4&height=4' > spectrum.svg
```

## Evaluation signals

- Output image renders without errors and contains recognizable mass spectrum visualization with m/z values on x-axis and intensity on y-axis.
- QR code, when scanned, resolves to the correct spectrum viewer at the metabolomics USI resolver endpoint (https://metabolomics-usi.ucsd.edu/spectrum/?usi=<input_usi>).
- SVG output preserves vector format (viewBox attribute present, paths rather than raster data) suitable for publication scaling; PNG output has appropriate resolution (dimensions and DPI match specification).
- Rendering parameters (mz_min, mz_max, annotate_peaks, max_intensity, grid visibility, title) are correctly reflected in the generated image.
- Peak annotations (if requested via annotate_peaks parameter) match the specified m/z values and precision level (annotate_precision).

## Limitations

- USI standard for metabolomics is currently in draft status (identifiers prefixed 'mzdraft' rather than 'mzspec' during standardization); format may change, breaking backward compatibility with pre-standardization identifiers.
- Resolver functionality depends on ongoing availability and correct configuration of remote data repositories (GNPS, MassBank, MassIVE, MetaboLights, Metabolomics Workbench, ProteoXchange, MS2LDA); repository downtime or API changes will disable resolution.
- QR code rendering is suitable for publication but contingent on persistent availability of the resolver URL endpoint; if the resolver service is moved or deprecated, QR codes in archived publications may become invalid.
- Mirror match visualization (comparing two spectra side-by-side) requires two valid USI strings; asymmetric or invalid USI pairs will fail rendering.

## Evidence

- [intro] Enable creation of embeddable images in publications that will link out to viewable/interactable spectrum plots.: "Enable creation of embeddable images in publications that will link out to viewable/interactable spectrum plots."
- [other] The tool achieves 3rd-party embedding of QR codes as one of its core objectives, allowing external systems to embed QR codes that reference USI identifiers from supported metabolomics data sources.: "The tool achieves 3rd-party embedding of QR codes as one of its core objectives, allowing external systems to embed QR codes that reference USI identifiers from supported metabolomics data sources."
- [other] Accept a USI string (dataset identifier, spectrum index, and optional library reference) as input. Construct the resolver URL by appending the USI to the base USI resolver endpoint. Generate a QR code image that encodes this resolver URL using a QR code library. Return the QR code as an embeddable image file (PNG or SVG format).: "Accept a USI string (dataset identifier, spectrum index, and optional library reference) as input. Construct the resolver URL by appending the USI to the base USI resolver endpoint. Generate a QR"
- [readme] Vanilla Rendering, Small Figure, Mass Range Filtering, Zoom Intensity, No Grid, No Peak Annotations, Custom Peak Annotations, Less Decimal Places, Rotate Labels, Decrease Label Minimum Intensity: "Vanilla Rendering, Small Figure, Mass Range Filtering, Zoom Intensity, No Grid, No Peak Annotations, Custom Peak Annotations, Less Decimal Places, Rotate Labels, Decrease Label Minimum Intensity"
- [readme] These identifiers are based on draft USI and draft Metabolomics USI identifiers. Thus, they are subject to change, and so for the moment, they will be specified as `mzdraft` instead of `mzspec` in the first block.: "These identifiers are based on draft USI and draft Metabolomics USI identifiers. Thus, they are subject to change, and so for the moment, they will be specified as `mzdraft` instead of `mzspec`"
- [readme] URL Endpoints: /png/, /svg/, /json/, /proxi/v0.1/spectra, /csv/, /qrcode/, /spectrum/, /mirror/, /svg/mirror, /png/mirror: "URL Endpoints: /png/, /svg/, /json/, /proxi/v0.1/spectra, /csv/, /qrcode/, /spectrum/, /mirror/, /svg/mirror, /png/mirror"
