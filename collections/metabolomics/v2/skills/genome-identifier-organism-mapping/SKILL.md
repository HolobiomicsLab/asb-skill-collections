---
name: genome-identifier-organism-mapping
description: Use when a paired omics project record contains a genome identifier field
  (e.g., from GenBank) but lacks the corresponding organism name, or when you need
  to validate that genome identifiers in bulk project records can be resolved to authoritative
  taxonomy.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0623
  - http://edamontology.org/topic_0080
  tools:
  - Github
  - NCBI Taxonomy / GenBank
  - redis queue
  - paired-data-form API web service
  techniques:
  - LC-MS
  license_tier: open
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41589-020-00724-z
  all_source_dois:
  - 10.1038/s41589-020-00724-z
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# genome-identifier-organism-mapping

## Summary

Enriches paired omics project records by retrieving and linking organism names to genome identifiers stored in project JSON files. This skill ensures that projects contain both resolvable genome identifiers and their corresponding scientific species names, improving data discoverability and cross-referencing in omics databases.

## When to use

Apply this skill when a paired omics project record contains a genome identifier field (e.g., from GenBank) but lacks the corresponding organism name, or when you need to validate that genome identifiers in bulk project records can be resolved to authoritative taxonomy. Specifically, use it during project ingestion or enrichment workflows where MS/MS mass spectra are being linked with genomic metadata.

## When NOT to use

- The project record already contains a validated organism name field with non-empty value
- The genome identifier is not resolvable against available reference databases (consider manual curation instead)
- The input is not a paired omics project JSON conforming to the platform's JSON schema

## Inputs

- project JSON file with genome_identifier field
- genome identifier string (e.g., GenBank accession)

## Outputs

- enriched project JSON file with organism_name field populated
- validation report indicating successful genome-to-organism resolution

## How to apply

Load the project JSON file and parse the genome identifier field from the project record. Query a public genome reference service (e.g., NCBI GenBank via API or a local genome-to-taxonomy mapping database) to retrieve the scientific organism name corresponding to that identifier. Append or update the organism name field in the project JSON structure. Validate that the enriched record contains both the genome identifier and organism name fields with non-empty values before writing the enriched project JSON to persistent storage. The platform uses a redis queue to schedule these enrichment jobs asynchronously, allowing batch resolution of identifiers without blocking project submission.

## Related tools

- **NCBI Taxonomy / GenBank** (Remote reference service queried to resolve genome identifiers to organism names) — https://www.ncbi.nlm.nih.gov/
- **redis queue** (Asynchronous job scheduler that queues and executes enrichment jobs to fetch organism metadata from public identifiers)
- **paired-data-form API web service** (Web service that orchestrates project JSON storage, retrieval, and enrichment workflows) — https://github.com/iomega/paired-data-form

## Evaluation signals

- Enriched project JSON contains both genome_identifier and organism_name fields with non-empty, non-null values
- organism_name value matches expected scientific nomenclature (e.g., 'Genus species') for the queried genome identifier
- Enrichment round-trip: re-parsing the output JSON yields the same genome identifier and organism name pair without data loss or corruption
- Batch validation: 100% of genome identifiers in a project sample set successfully resolve to organism names (or failures are logged and can be manually reviewed)
- Schema compliance: enriched JSON validates against app/public/schema.json with no schema violations

## Limitations

- Resolution depends on availability and currency of the queried reference database (NCBI GenBank); stale or private genome identifiers may not resolve
- The platform's current implementation does not handle conflicts when the same genome identifier maps to multiple organism names across different reference versions or databases
- Batch enrichment via redis queue is asynchronous; projects submitted before enrichment jobs complete will temporarily lack organism name fields

## Evidence

- [readme] The web service uses a redis queue (v5.0.5) to schedule jobs to fetch more information about the public identifiers and to upload the projects to Zenodo each month. For example, the scientific species name is fetched from GenBank using the public genome identifiers in the project.: "redis queue (v5.0.5) to schedule jobs to fetch more information about the public identifiers ... the scientific species name is fetched from GenBank using the public genome identifiers in the project"
- [other] The platform links MS/MS mass spectra with genome and other metadata including sample preparation, extraction method, and instrumentation method within stored project records.: "platform links MS/MS mass spectra with genome and other metadata including sample preparation, extraction method, and instrumentation method"
- [other] Query a genome database or reference service (e.g., NCBI Taxonomy or local mapping) to retrieve the organism name corresponding to the genome identifier.: "Query a genome database or reference service (e.g., NCBI Taxonomy or local mapping) to retrieve the organism name corresponding to the genome identifier"
- [other] Validate that the enriched record contains both genome identifier and organism name fields with non-empty values.: "Validate that the enriched record contains both genome identifier and organism name fields with non-empty values"
