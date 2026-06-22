---
name: web-application-endpoint-mapping
description: Use when you have a user-submitted spectrum with associated domain context metadata (e.g., selected as 'microbial origin', 'plant tissue', 'food sample') and need to route that spectrum to the appropriate domain-specific MASST application for searching.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - microbeMASST
  - plantMASST
  - tissueMASST
  - microbiomeMASST
  - foodMASST
  - metadataMASST
  - GNPS_MASST
derived_from:
- doi: 10.1038/s41564-023-01575-9
  title: microbemasst
evidence_spans:
- microbeMASST, plantMASST, tissueMASST, microbiomeMASST, and foodMASST
- Aggregated search outputs can be generated and visualized using metadataMASST
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_microbemasst
    doi: 10.1038/s41564-023-01575-9
    title: microbemasst
  dedup_kept_from: coll_microbemasst
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41564-023-01575-9
  all_source_dois:
  - 10.1038/s41564-023-01575-9
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Web Application Endpoint Mapping

## Summary

Route user-submitted mass spectrometry spectra to domain-specific MASST web applications based on parsed domain context (microbial, plant, tissue, microbiome, food, or metadata aggregation). This skill implements conditional dispatch logic that maps spectrum metadata to the correct standalone application endpoint, enabling targeted spectral searching across curated domain-specific databases.

## When to use

Apply this skill when you have a user-submitted spectrum with associated domain context metadata (e.g., selected as 'microbial origin', 'plant tissue', 'food sample') and need to route that spectrum to the appropriate domain-specific MASST application for searching. Use when serving multiple domain-specific applications and need deterministic, metadata-driven routing rather than manual user selection.

## When NOT to use

- Spectrum lacks domain context metadata or user has not selected a domain — routing cannot be performed deterministically without explicit context.
- User needs simultaneous cross-domain searching across all six MASSTs — use batch search via jobs.py instead, which generates outputs for all domainMASSTs in parallel.
- Spectrum is already pre-filtered or curated for a specific domain — endpoint mapping is redundant if destination is already known.

## Inputs

- User-submitted MS/MS spectrum file (.mgf format or USI identifier)
- Spectrum metadata including domain-context field (e.g., sample origin, tissue type, or explicit domain selection)
- Domain-to-endpoint mapping configuration (canonical list of six domainMASSTs and their URLs)

## Outputs

- Routed spectrum submitted to domain-specific MASST web application endpoint
- Routing decision log (domain context extracted, endpoint selected, confirmation of submission)
- Search results from the selected domain-specific MASST (matches.tsv, library.tsv, datasets.tsv, domain-specific HTML/JSON trees)

## How to apply

Parse the user-submitted spectrum file and extract domain-context metadata from the submission (e.g., sample origin, tissue type, or explicit user domain selection). Implement a conditional routing map that associates each domain context value (microbial, plant, tissue, microbiome, food, metadata) with the corresponding MASST application endpoint (e.g., masst.gnps2.org/microbemasst/, masst.gnps2.org/plantmasst/). Validate that the extracted domain context matches one of the six defined domainMASST categories and that the target endpoint is reachable. Route the spectrum to the selected endpoint and log the routing decision for traceability. Test the routing logic with representative spectra from each domain to confirm correct application dispatch and absence of silent routing failures.

## Related tools

- **GNPS_MASST** (Provides the underlying code and web application framework for all six domain-specific MASST standalone applications; implements the web endpoints that receive routed spectra) — https://github.com/mwang87/GNPS_MASST
- **microbeMASST** (Target endpoint for spectra with microbial domain context; searches against microbial metabolite spectral library) — https://masst.gnps2.org/microbemasst/
- **plantMASST** (Target endpoint for spectra with plant domain context; searches against plant metabolite spectral library) — https://masst.gnps2.org/plantmasst/
- **tissueMASST** (Target endpoint for spectra with tissue domain context; searches against tissue metabolite spectral library) — https://masst.gnps2.org/tissuemasst/
- **microbiomeMASST** (Target endpoint for spectra with microbiome domain context; searches against microbiome-derived metabolite spectral library) — https://masst.gnps2.org/microbiomemasst/
- **foodMASST** (Target endpoint for spectra with food domain context; searches against food-derived metabolite spectral library) — https://masst.gnps2.org/foodmasst2/
- **metadataMASST** (Target endpoint for aggregated or cross-domain searches; generates and visualizes aggregated search outputs across all domainMASSTs) — https://masst.gnps2.org/metadatamasst/

## Evaluation signals

- Verify that the extracted domain context matches exactly one of the six defined categories (microbial, plant, tissue, microbiome, food, metadata) and is not null or ambiguous.
- Confirm that the routed spectrum reaches the correct endpoint URL by checking HTTP response code (200 OK) and presence of domain-specific result elements (e.g., _microbe.html for microbeMASST, _plant.json for plantMASST).
- Validate that routing logs record the domain context extracted, the target endpoint selected, and the timestamp of submission; no spectrum should be routed to a mismatched domain.
- Test with representative spectra from each of the six domains and confirm that search results are domain-appropriate (e.g., microbeMASST returns microbial metabolite matches, plantMASST returns plant metabolite matches).
- Verify absence of silent routing failures by confirming that all test spectra produce searchable output (non-empty matches.tsv, library.tsv, or datasets.tsv) within expected latency.

## Limitations

- Routing depends on reliable domain context metadata in user submission; if metadata is missing, malformed, or inconsistent with the six defined domains, routing will fail or require fallback logic (e.g., metadataMASST as catch-all).
- Each domain-specific MASST searches only indexed data from GNPS/MassIVE, Metabolomics Workbench, Metabolights, and NORMAN at the time of submission; routing correctness does not guarantee spectral match coverage, only correct database access.
- Batch routing via jobs.py requires manual parameter configuration (cosine score threshold, m/z tolerance, minimum matching peaks) and may produce partial failures requiring multiple re-runs (as noted in README: 'run jobs.py a couple of times until no new output is generated'); single-spectrum routing does not have this retry requirement but batch workflows do.
- metadataMASST is designed for aggregated/cross-domain results and should not be treated as a domain-specific endpoint; using it as a fallback for unrecognized domain contexts may conflate results across unrelated biological origins.

## Evidence

- [other] Parse user-submitted spectrum metadata and extract the domain-context selection: "Parse user-submitted spectrum metadata and extract the domain-context selection (e.g., microbial, plant, tissue, microbiome, food, or metadata aggregation)."
- [other] Implement conditional routing logic: "Implement conditional routing logic that maps domain context to the corresponding standalone web application endpoint or module."
- [readme] Six domain-specific MASSTs: "This repository contains the code and data for the different domain-specific MASSTs currently under development in the Dorrestein Lab at UC San Diego. This includes microbeMASST, plantMASST,"
- [readme] Standalone web applications endpoints: "Standalone Web Apps: 1. microbeMASST 2. plantMASST 3. tissueMASST 4. microbiomeMASST 5. foodMASST 6. metadataMASST"
- [readme] Aggregated search outputs: "Aggregated search outputs can be generated and visualized using metadataMASST."
- [readme] Spectrum search one at a time: "The code for the different standalone web applications, which allow users to search one spectrum at a time, can be found in GNPS_MASST"
