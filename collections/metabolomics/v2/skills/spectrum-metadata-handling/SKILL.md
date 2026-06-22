---
name: spectrum-metadata-handling
description: Use when when you have a USI (Universal Spectrum Identifier) string referencing a spectrum in a public metabolomics repository (GNPS Molecular Networking, GNPS Spectral Libraries, MassBank, MetaboLights, Metabolomics Workbench, MS2LDA, or ProteoXchange) and need to extract its raw spectral data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - GNPS Molecular Networking
  - MassBank
  - MetaboLights
  - Metabolomics Workbench
  - MetabolomicsSpectrumResolver
  - MS2LDA
derived_from:
- doi: 10.1101/2020.05.09.086066
  title: Metabolomics Spectrum Resolver
evidence_spans:
- GNPS Molecular Networking Clustered Spectra
- MassBank Library Spectra
- MetaboLights Dataset Spectra
- Metabolomics Workbench Dataset Spectra
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

# spectrum-metadata-handling

## Summary

Resolve Universal Spectrum Identifiers (USIs) from heterogeneous metabolomics repositories (GNPS, MassBank, MetaboLights, etc.) and extract their underlying m/z, intensity, and annotation metadata to enable downstream visualization and publication embedding. This skill bridges repository-specific formats into a unified metadata schema suitable for embeddable spectrum rendering.

## When to use

When you have a USI (Universal Spectrum Identifier) string referencing a spectrum in a public metabolomics repository (GNPS Molecular Networking, GNPS Spectral Libraries, MassBank, MetaboLights, Metabolomics Workbench, MS2LDA, or ProteoXchange) and need to extract its raw spectral data (peak m/z values, intensities, metadata) in order to render, annotate, or embed the spectrum in a publication or interactive viewer.

## When NOT to use

- The USI references a source repository not yet supported by MetabolomicsSpectrumResolver (only GNPS, MassBank, MetaboLights, Metabolomics Workbench, MS2LDA, and ProteoXchange are supported).
- You already have the raw spectrum data (m/z and intensity arrays) in hand and do not need to retrieve it from a remote repository.
- The USI string is malformed or the spectrum accession no longer exists in the source repository.

## Inputs

- USI string (e.g., 'mzspec:GNPS:TASK-c95481f0c53d42e78a61bf899e9f9adb-spectra/specs_ms.mgf:scan:1943')
- Repository identifier and accession within the USI (GNPS task ID, MassBank accession, MSV ID, etc.)

## Outputs

- Resolved spectrum JSON object (m/z array, intensity array, metadata fields)
- Peak list with optional annotations (m/z, intensity, fragment assignment)
- Spectrum metadata (precursor m/z, collision energy, compound name, source repository)

## How to apply

Parse the USI string to identify the source repository and spectrum accession. Submit the USI to the MetabolomicsSpectrumResolver's resolution endpoint (e.g., `/json/` or `/proxi/`) to retrieve the resolved spectrum object containing m/z array, intensity array, and associated metadata (e.g., precursor m/z, collision energy, compound name). Extract the peak list and metadata into a standardized format (JSON, CSV, or Python dict). Validate that all required fields (m/z, intensity, accession) are present and non-empty. Use these resolved data for downstream rendering (SVG/PNG), annotation, or filtering (e.g., mass range selection via `mz_min`/`mz_max` parameters).

## Related tools

- **MetabolomicsSpectrumResolver** (Primary resolver that ingests USI strings and returns structured spectrum metadata and peak lists from supported repositories) — https://github.com/mwang87/MetabolomicsSpectrumResolver
- **GNPS Molecular Networking** (Source repository for clustered spectra accessed via USI)
- **MassBank** (Source repository for library spectra accessed via USI)
- **MetaboLights** (Source repository for metabolomics dataset spectra accessed via USI)
- **Metabolomics Workbench** (Source repository for metabolomics dataset spectra accessed via USI)
- **MS2LDA** (Source repository for reference motifs accessed via USI)

## Examples

```
curl 'https://metabolomics-usi.ucsd.edu/json/?usi=mzspec:GNPS:TASK-c95481f0c53d42e78a61bf899e9f9adb-spectra/specs_ms.mgf:scan:1943'
```

## Evaluation signals

- Resolved spectrum object contains non-empty m/z array and intensity array of equal length.
- USI accession identifier in resolved metadata matches the input USI string.
- Precursor m/z, if present, falls within typical mass range for the ionization mode (e.g., 50–2000 m/z).
- Peak annotations (if requested) align to m/z values within tolerance; annotation m/z values are present in the resolved peak list.
- Source repository field in metadata matches one of the seven supported repositories (GNPS, MassBank, MetaboLights, Metabolomics Workbench, MS2LDA, ProteoXchange, or MassIVE/GNPS).

## Limitations

- USI identifiers are currently specified as 'mzdraft' rather than the finalized 'mzspec' standard, indicating the format is subject to change.
- Only seven source repositories are supported; USIs from other repositories will fail resolution.
- Metadata completeness varies by source repository; some spectra may lack collision energy, compound name, or other optional fields.
- No changelog is provided, so version stability and backward compatibility of USI formats cannot be verified.

## Evidence

- [readme] Supported USI Types: 1. GNPS Molecular Networking Clustered Spectra 2. GNPS Spectral Libraries 3. ProteoXchange Repository Data 4. MS2LDA Reference Motifs 5. MassBank Library Spectra 6. MetaboLights Dataset Spectra 7. Metabolomics Workbench Dataset Spectra: "Supported USI Types: 1. GNPS Molecular Networking Clustered Spectra 2. GNPS Spectral Libraries 3. ProteoXchange Repository Data 4. MS2LDA Reference Motifs 5. MassBank Library Spectra 6. MetaboLights"
- [other] The tool achieves embeddable image creation by resolving USI identifiers from supported sources (GNPS Molecular Networking, GNPS Spectral Libraries, ProteoXchange, MS2LDA, MassBank, MetaboLights, and Metabolomics Workbench) and generating linked visual outputs for publication integration.: "resolving USI identifiers from supported sources (GNPS Molecular Networking, GNPS Spectral Libraries, ProteoXchange, MS2LDA, MassBank, MetaboLights, and Metabolomics Workbench)"
- [other] Load the resolved spectrum data (m/z values, intensities, metadata) from the USI resolver output.: "Load the resolved spectrum data (m/z values, intensities, metadata) from the USI resolver output."
- [readme] These identifiers are based on draft USI and draft Metabolomics USI identifiers. Thus, they are subject to change, and so for the moment, they will be specified as `mzdraft` instead of `mzspec` in the first block.: "These identifiers are based on draft USI and draft Metabolomics USI identifiers. Thus, they are subject to change"
- [readme] URL Endpoints: 1. /png/ 2. /svg/ 3. /json/ 4. /proxi/v0.1/spectra 5. /csv/ 6. /qrcode/ 7. /spectrum/ 8. /mirror/ 9. /svg/mirror 10. /png/mirror: "URL Endpoints: 1. /png/ 2. /svg/ 3. /json/ 4. /proxi/v0.1/spectra 5. /csv/"
