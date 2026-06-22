---
name: json-record-enrichment
description: Use when when a project JSON record contains a resolvable public identifier (genome accession, biosynthetic gene cluster ID, etc.) but lacks the corresponding human-readable or standardized metadata field (organism name, cluster description).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3283
  edam_topics:
  - http://edamontology.org/topic_0622
  - http://edamontology.org/topic_3697
  tools:
  - Github
  - redis queue
  - GenBank / NCBI Taxonomy
  - Node.js / npm
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# json-record-enrichment

## Summary

Enrich JSON project records by fetching and integrating external metadata (e.g., organism names) linked to public identifiers (e.g., genome accessions). This skill is essential for paired omics platforms that store heterogeneous experimental metadata and need to standardize and cross-reference records with authoritative databases.

## When to use

When a project JSON record contains a resolvable public identifier (genome accession, biosynthetic gene cluster ID, etc.) but lacks the corresponding human-readable or standardized metadata field (organism name, cluster description). Typical triggers: ingestion of new projects into the platform, batch validation workflows, or scheduled reconciliation jobs that need to populate missing fields before public release or search indexing.

## When NOT to use

- The public identifier is missing, malformed, or does not resolve to any reference database entry.
- The target metadata field is already populated with a non-empty, validated value.
- The reference service is unavailable or has rate-limiting restrictions that would block enrichment in a time-critical workflow.

## Inputs

- Project JSON record with genome identifier field
- Public identifier (e.g., GenBank genome accession, NCBI Taxonomy ID)
- JSON schema definition (app/public/schema.json)

## Outputs

- Enriched project JSON record with organism name field populated
- Validated project record conforming to JSON schema

## How to apply

Load the project JSON file and parse the public identifier field (e.g., genome identifier). Query an authoritative reference service (e.g., NCBI Taxonomy, GenBank, or a local lookup table) to retrieve the corresponding metadata value. Append or update the target field (e.g., organism name) in the project record. Validate that both the source identifier and enriched field contain non-empty values and conform to the project JSON schema. Write the enriched record back to the output file. The platform uses a redis queue to schedule these enrichment jobs asynchronously, allowing batch processing without blocking project submission.

## Related tools

- **redis queue** (Schedules and orchestrates asynchronous enrichment jobs to fetch metadata from public identifiers without blocking project submission.)
- **GenBank / NCBI Taxonomy** (Reference service queried to retrieve organism names and other taxonomic metadata from genome identifiers.)
- **Node.js / npm** (Runtime and package manager for running enrichment jobs in the API web service.) — https://github.com/iomega/paired-data-form

## Evaluation signals

- Both source identifier and enriched field are present and non-empty in the output JSON record.
- Output record validates against the JSON schema (app/public/schema.json) with no missing required fields.
- Organism name (or other enriched field) matches the expected value from the reference database when manually verified.
- Enrichment job completes without errors and logs successful retrieval and update actions.
- Enriched records appear in full-text search index and can be discovered by their newly populated metadata fields.

## Limitations

- Enrichment depends on external reference service availability and accuracy; if the service is offline or contains incorrect mappings, enriched data will be incomplete or incorrect.
- Public identifiers must be resolvable and properly formatted; malformed or deprecated accessions will fail enrichment silently or with error logs.
- Batch enrichment can be slow if reference services have rate limits or if the job queue has high latency; prioritization of high-value identifiers may be needed.
- The platform enriches only those identifiers explicitly mapped in the schema and configured in the enrichment job definitions; other potential metadata sources are not automatically integrated.

## Evidence

- [readme] The web service uses a redis queue (v5.0.5) to schedule jobs to fetch more information about the public identifiers and to upload the projects to Zenodo each month. For example, the scientific species name is fetched from GenBank using the public genome identifiers in the project.: "redis queue (v5.0.5) to schedule jobs to fetch more information about the public identifiers... the scientific species name is fetched from GenBank using the public genome identifiers"
- [other] 1. Load the project JSON file containing the genome identifier. 2. Parse the genome identifier field from the project record. 3. Query a genome database or reference service (e.g., NCBI Taxonomy or local mapping) to retrieve the organism name corresponding to the genome identifier. 4. Append or update the organism name field in the project JSON record. 5. Validate that the enriched record contains both genome identifier and organism name fields with non-empty values. 6. Write the enriched project JSON to the output file.: "Load the project JSON file containing the genome identifier... Query a genome database or reference service... Append or update the organism name field... Validate that the enriched record contains"
- [readme] The JSON schema (app/public/schema.json) describes the format of an project.: "The JSON schema (app/public/schema.json) describes the format of an project"
- [other] The platform links MS/MS mass spectra with genome and other metadata including sample preparation, extraction method, and instrumentation method within stored project records.: "platform links MS/MS mass spectra with genome and other metadata including sample preparation, extraction method, and instrumentation method"
