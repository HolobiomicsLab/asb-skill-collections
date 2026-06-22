---
name: multi-source-spectrum-retrieval
description: Use when when you have a Universal Spectrum Identifier (USI) string or collection of USI strings and need to programmatically retrieve the corresponding mass spectrometry spectrum data from one of seven supported repositories (GNPS Molecular Networking, GNPS Spectral Libraries, ProteoXchange.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3172
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

# multi-source-spectrum-retrieval

## Summary

Resolve metabolomics mass spectrometry identifiers (USIs) to retrieve spectrum data from heterogeneous public repositories by parsing the namespace prefix, routing to the correct backend API, and returning standardized spectrum objects. Use this skill when you need to fetch raw or annotated spectra from multiple metabolomics or proteomics data sources using a unified identifier scheme.

## When to use

When you have a Universal Spectrum Identifier (USI) string or collection of USI strings and need to programmatically retrieve the corresponding mass spectrometry spectrum data from one of seven supported repositories (GNPS Molecular Networking, GNPS Spectral Libraries, ProteoXchange, MassBank, MetaboLights, Metabolomics Workbench, or MS2LDA) for downstream analysis, visualization, or publication embedding.

## When NOT to use

- Input USI namespace is not one of the seven supported types (GNPS, MASSBANK, PXD, MS2LDA, MOTIFDB, MetaboLights MSV, Metabolomics Workbench MSV); resolver will fail or return null.
- Spectrum data is already locally cached or embedded in memory; retrieval would be redundant network I/O.
- USI format is malformed or uses an older draft identifier scheme (mzdraft) that is no longer synchronized with the resolver's current mapping table.

## Inputs

- Universal Spectrum Identifier (USI) string conforming to mzspec or mzdata draft format (e.g., 'mzspec:GNPS:GNPS-LIBRARY:accession:CCMSLIB00005436077')
- Optional query parameters: mz_min, mz_max, max_intensity, annotate_peaks, plot_title

## Outputs

- JSON spectrum object with m/z array, intensity array, and metadata fields (accession, compound name, molecular weight, adduct, source repository)
- SVG or PNG rendered spectrum image (if /svg/ or /png/ endpoint used)
- CSV export of spectrum peaks (if /csv/ endpoint used)
- QR code linking to spectrum (if /qrcode/ endpoint used)

## How to apply

Parse the input USI by extracting its namespace prefix (the segment immediately after 'mzspec:' or 'mzdata:', e.g., 'GNPS', 'MASSBANK', 'PXD', 'MSV') and matching it against the resolver's internal mapping table to identify the target repository. Route the retrieval request to the corresponding repository backend API or data access layer with the resource identifier and accessor fields (e.g., accession, scan number, filename). The resolver standardizes output to a JSON spectrum object containing m/z values, intensity pairs, and metadata fields (compound name, molecular weight, adduct information where available). Query parameters (e.g., mz_min, mz_max, max_intensity) can filter or zoom the spectrum before return. Verify successful retrieval by checking that the returned object contains non-empty m/z and intensity arrays and expected metadata keys for the source repository.

## Related tools

- **GNPS Molecular Networking** (Source repository for clustered spectra from network analysis tasks; resolver dispatches requests using task ID and scan number.) — https://gnps.ucsd.edu
- **GNPS Spectral Libraries** (Source repository for reference spectral library entries; resolver queries by library accession identifier.) — https://gnps.ucsd.edu
- **ProteoXchange Repository** (Source repository for proteomics and metabolomics raw spectra; resolver uses PXD dataset and filename identifiers.) — http://proteomecentral.proteomexchange.org
- **MassBank** (Source repository for curated mass spectra library; resolver retrieves spectra by MassBank accession code.) — https://massbank.eu
- **MetaboLights** (Source repository for metabolomics study datasets; resolver accesses spectra via MSV identifier and scan number.) — https://www.ebi.ac.uk/metabolights
- **Metabolomics Workbench** (Source repository for metabolomics project data; resolver retrieves spectra via MSV identifier and scan number.) — https://www.metabolomicsworkbench.org
- **MS2LDA** (Source repository for reference motif spectral patterns; resolver queries by task ID and accession.) — https://ms2lda.org
- **MetabolomicsSpectrumResolver** (The resolver implementation itself; orchestrates USI parsing, routing, and standardized return formatting.) — https://github.com/mwang87/MetabolomicsSpectrumResolver

## Examples

```
curl 'https://metabolomics-usi.ucsd.edu/json/?usi=mzspec:MASSBANK::accession:SM858102' | jq '.spectrum | {mz: .[].mz, intensity: .[].intensity}'
```

## Evaluation signals

- Returned JSON object contains non-empty 'm/z' and 'intensity' arrays with numeric values; lengths match.
- Metadata fields (accession, compound name, source repository) are present and non-null in the returned spectrum object.
- USI namespace prefix correctly maps to expected source repository; e.g., 'MASSBANK' prefix retrieves from MassBank, 'GNPS-LIBRARY' from GNPS Libraries.
- Filtered spectra (via mz_min, mz_max, max_intensity parameters) show only peaks within the specified ranges; no out-of-range m/z or intensity values remain.
- HTTP response status is 200 (success) for valid USI; 4xx error for malformed or unsupported namespace; backend latency is consistent with source repository API response time.

## Limitations

- USI identifiers are based on draft standards (prefixed with 'mzdraft' rather than final 'mzspec') and are subject to change; forward compatibility is not guaranteed.
- Resolver supports only seven predefined source repositories; USIs from other metabolomics or proteomics databases cannot be resolved.
- Network latency depends on backend repository API responsiveness; retrieval may timeout or fail if source repository is temporarily unavailable.
- Spectrum metadata completeness varies by source (e.g., MassBank provides curated annotations, while raw datasets may lack compound information); standardized output cannot guarantee all fields are populated.
- Large batch retrievals are not optimized; recommended for single or small numbers of spectra per request; high-throughput access should use native repository APIs.

## Evidence

- [other] The resolver supports seven distinct USI types corresponding to different metabolomics data sources: GNPS Molecular Networking Clustered Spectra, GNPS Spectral Libraries, ProteoXchange Repository Data, MS2LDA Reference Motifs, MassBank Library Spectra, MetaboLights Dataset Spectra, and Metabolomics Workbench Dataset Spectra.: "The resolver supports seven distinct USI types corresponding to different metabolomics data sources: GNPS Molecular Networking Clustered Spectra, GNPS Spectral Libraries, ProteoXchange Repository"
- [other] 1. Parse the input USI to extract its namespace prefix and resource identifier. 2. Match the namespace against a mapping table to identify the supported source repository. 3. Dispatch the retrieval request to the corresponding repository backend API or data access layer. 4. Retrieve and return the spectrum data in a standardized format (e.g., JSON spectrum object with m/z, intensity, metadata fields).: "Parse the input USI to extract its namespace prefix and resource identifier. 2. Match the namespace against a mapping table to identify the supported source repository. 3. Dispatch the retrieval"
- [readme] Enable creation of embeddable images in publications that will link out to viewable/interactable spectrum plots. 3rd party embedding for visualization of spectra that exist in repositories (e.g. MassIVE, PRIDE, PeptideAtlas).: "Enable creation of embeddable images in publications that will link out to viewable/interactable spectrum plots. 3rd party embedding for visualization of spectra that exist in repositories"
- [readme] These identifiers are based on draft USI and draft Metabolomics USI identifiers. Thus, they are subject to change, and so for the moment, they will be specified as `mzdraft` instead of `mzspec` in the first block.: "These identifiers are based on draft USI and draft Metabolomics USI identifiers. Thus, they are subject to change, and so for the moment, they will be specified as `mzdraft` instead of `mzspec`"
- [readme] Supported USI Types: 1. GNPS Molecular Networking Clustered Spectra 2. GNPS Spectral Libraries 3. ProteoXchange Repository Data 4. MS2LDA Reference Motifs 5. MassBank Library Spectra 6. MetaboLights Dataset Spectra 7. Metabolomics Workbench Dataset Spectra: "Supported USI Types: 1. GNPS Molecular Networking Clustered Spectra 2. GNPS Spectral Libraries 3. ProteoXchange Repository Data 4. MS2LDA Reference Motifs 5. MassBank Library Spectra 6. MetaboLights"
