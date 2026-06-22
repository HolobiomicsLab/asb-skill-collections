---
name: project-metadata-integration
description: Use when a paired omics project record contains a genome identifier (e.g., GenBank accession) but lacks the corresponding organism name field, and you need to populate that metadata field to enable full text search, sample tracking, or project validation before archival to Zenodo.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_0080
  - http://edamontology.org/topic_3520
  tools:
  - Github
  - redis queue
  - GenBank / NCBI Taxonomy
derived_from:
- doi: 10.1038/s41589-020-00724-z
  title: pairedomicsdatapla
evidence_spans:
- pull request (https://help.github.com/articles/about-pull-requests/)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pairedomicsdatapla_cq
    doi: 10.1038/s41589-020-00724-z
    title: pairedomicsdatapla
  dedup_kept_from: coll_pairedomicsdatapla_cq
schema_version: 0.2.0
---

# project-metadata-integration

## Summary

Enrich paired omics project records by fetching and integrating organism name information from public genome identifiers, linking MS/MS mass spectra with taxonomic metadata. This ensures complete traceability of both genomic and proteomic data within stored project JSON records.

## When to use

A paired omics project record contains a genome identifier (e.g., GenBank accession) but lacks the corresponding organism name field, and you need to populate that metadata field to enable full text search, sample tracking, or project validation before archival to Zenodo.

## When NOT to use

- The project record already contains a populated organism name field.
- The genome identifier is invalid, deprecated, or not resolvable via available genome reference services.
- The project does not contain genomic data or a genome identifier field.

## Inputs

- Project JSON file containing genome identifier field
- Genome identifier (e.g., GenBank accession number)

## Outputs

- Enriched project JSON file with populated organism name field
- Updated project record with both genome identifier and organism name

## How to apply

Load the project JSON file and parse the genome identifier field from the project record. Query a public genome database service (e.g., NCBI Taxonomy or GenBank) or consult a locally maintained genome-to-organism mapping to retrieve the scientific species name corresponding to that identifier. Append or update the organism name field in the project JSON structure. Validate that the enriched record contains both genome identifier and organism name fields with non-empty values. Write the enriched project JSON to the output file. This workflow is performed asynchronously by the platform's redis queue during project submission to ensure timely retrieval without blocking user interaction.

## Related tools

- **redis queue** (Schedules asynchronous jobs to fetch organism name information from GenBank using public genome identifiers in project records)
- **GenBank / NCBI Taxonomy** (Public genome database service queried to retrieve organism name corresponding to genome identifier)
- **Github** (Version control and contribution workflow for modifications to enrichment logic and schema validation) — https://github.com/iomega/paired-data-form

## Evaluation signals

- Both genome identifier and organism name fields are non-empty in the enriched project JSON record
- The organism name matches the expected taxonomy for the provided genome identifier (spot-check against NCBI Taxonomy)
- The enriched project record passes JSON schema validation against the platform's defined schema
- No duplicate or partial genome identifiers remain unresolved after the enrichment job completes
- The organism name field is indexed and searchable via the platform's full text search functionality

## Limitations

- Enrichment depends on availability and accuracy of external genome reference services (NCBI, GenBank); service outages or stale data may cause retrieval failures.
- Ambiguous or non-standard genome identifiers (e.g., malformed accessions, legacy identifiers) may not resolve to an organism name.
- The redis queue processes jobs asynchronously; enrichment may be delayed, requiring monitoring of job completion status.
- Multi-organism projects or metagenomic samples with multiple genome identifiers require separate enrichment steps per identifier.

## Evidence

- [other] Parse the genome identifier field from the project record. Query a genome database or reference service (e.g., NCBI Taxonomy or local mapping) to retrieve the organism name corresponding to the genome identifier.: "Parse the genome identifier field from the project record. Query a genome database or reference service (e.g., NCBI Taxonomy or local mapping) to retrieve the organism name"
- [readme] The web service uses a redis queue (v5.0.5) to schedule jobs to fetch more information about the public identifiers and to upload the projects to Zenodo each month. For example, the scientific species name is fetched from GenBank using the public genome identifiers in the project.: "The web service uses a redis queue (v5.0.5) to schedule jobs to fetch more information about the public identifiers. For example, the scientific species name is fetched from GenBank using the public"
- [intro] Links MS/MS mass spectra with genome, sample preparation, extraction method and instrumentation method: "Links MS/MS mass spectra with genome, sample preparation, extraction method and instrumentation method"
- [other] Validate that the enriched record contains both genome identifier and organism name fields with non-empty values.: "Validate that the enriched record contains both genome identifier and organism name fields with non-empty values."
