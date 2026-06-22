---
name: taxonomy-database-querying
description: Use when a paired omics project record contains a genome identifier (e.g., from GenBank or NCBI) but lacks the corresponding organism scientific name.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3095
  edam_topics:
  - http://edamontology.org/topic_0637
  - http://edamontology.org/topic_3697
  tools:
  - Github
  - NCBI Taxonomy database
  - Redis queue
  - GenBank
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

# taxonomy-database-querying

## Summary

Query a taxonomic database or reference service (e.g., NCBI Taxonomy) to retrieve organism scientific names from genome identifiers, enabling enrichment of omics project records with standardized taxonomic metadata.

## When to use

A paired omics project record contains a genome identifier (e.g., from GenBank or NCBI) but lacks the corresponding organism scientific name. This skill is needed when enriching project JSON records to link MS/MS mass spectra with complete genomic and organism metadata before storage or publication.

## When NOT to use

- The project record already contains a populated organism name field
- The genome identifier is invalid, malformed, or does not exist in any available reference database
- The organism name must be manually curated or verified by domain experts rather than automatically retrieved

## Inputs

- Project JSON file containing a genome identifier field
- Genome identifier string (e.g., NCBI RefSeq accession)

## Outputs

- Enriched project JSON record with organism name field populated
- Validated project record with both genome identifier and organism name

## How to apply

Parse the genome identifier field from the project JSON record. Query a genome database or reference service (e.g., NCBI Taxonomy or a local genome-to-organism mapping table) using the identifier as the lookup key. Retrieve the organism scientific name from the service response. Append or update the organism name field in the project JSON record. Validate that the enriched record contains both the genome identifier and organism name fields with non-empty values. Write the enriched project JSON to the output file or storage system.

## Related tools

- **NCBI Taxonomy database** (Reference service queried to retrieve organism scientific names from genome identifiers)
- **Redis queue** (Schedules asynchronous jobs to fetch organism names from public identifiers in projects)
- **GenBank** (Source of genome identifiers and organism name mappings)

## Evaluation signals

- The enriched project JSON contains a non-empty organism name field that corresponds to the genome identifier
- Schema validation confirms both genome identifier and organism name fields are present and populated
- The organism name retrieved matches expected taxonomy nomenclature (e.g., binomial Genus species format)
- No null, empty, or placeholder values remain in the organism name field after enrichment
- Round-trip verification: re-querying the database with the retrieved organism name returns the same genome identifier

## Limitations

- Genome identifiers must be valid and exist in the queried reference service; invalid or retired identifiers will fail lookup
- Database service availability and query latency may affect enrichment speed; the platform uses an asynchronous redis queue to mitigate this
- Organism name formats vary across databases; normalization or curation may be needed for consistency across projects
- Some genome identifiers may map to multiple or ambiguous organism names if the reference database contains duplicates or strain-level variants

## Evidence

- [other] The platform links MS/MS mass spectra with genome and other metadata including sample preparation, extraction method, and instrumentation method within stored project records.: "The platform links MS/MS mass spectra with genome and other metadata including sample preparation, extraction method, and instrumentation method within stored project records."
- [other] Query a genome database or reference service (e.g., NCBI Taxonomy or local mapping) to retrieve the organism name corresponding to the genome identifier.: "Query a genome database or reference service (e.g., NCBI Taxonomy or local mapping) to retrieve the organism name corresponding to the genome identifier."
- [readme] The web service uses a redis queue (v5.0.5) to schedule jobs to fetch more information about the public identifiers and to upload the projects to Zenodo each month. For example, the scientific species name is fetched from GenBank using the public genome identifiers in the project.: "The web service uses a redis queue (v5.0.5) to schedule jobs to fetch more information about the public identifiers. For example, the scientific species name is fetched from GenBank using the public"
- [other] Validate that the enriched record contains both genome identifier and organism name fields with non-empty values.: "Validate that the enriched record contains both genome identifier and organism name fields with non-empty values."
