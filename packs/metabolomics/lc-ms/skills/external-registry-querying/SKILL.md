---
name: external-registry-querying
description: Use when your project JSON document contains genome identifiers but lacks organism name or taxonomic annotations. The platform needs to auto-populate these fields to enable browsing and cross-linking with public genomic databases. Trigger this skill when you have genome IDs (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_3697
  - http://edamontology.org/topic_3520
  tools:
  - npm
  - redis queue
  - GenBank / NCBI Taxonomy
  - paired-data-form
  techniques:
  - LC-MS
derived_from:
- doi: 10.1038/s41589-020-00724-z
  title: pairedomicsdatapla
evidence_spans:
- make sure the existing tests still work by running ``npm run test`` in `api/` and/or `app/` directory
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pairedomicsdatapla
    doi: 10.1038/s41589-020-00724-z
    title: pairedomicsdatapla
  dedup_kept_from: coll_pairedomicsdatapla
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

# external-registry-querying

## Summary

Query external genome registries (e.g., GenBank, NCBI Taxonomy, IMG) using public genome identifiers to retrieve organism names and other taxonomic metadata, then inject the results into project JSON documents. This enriches paired omics datasets by linking MS/MS mass spectra to curated genomic information.

## When to use

Your project JSON document contains genome identifiers but lacks organism name or taxonomic annotations. The platform needs to auto-populate these fields to enable browsing and cross-linking with public genomic databases. Trigger this skill when you have genome IDs (e.g., from GenBank) but require linked species names or other registry-sourced metadata to complete project metadata.

## When NOT to use

- The genome identifier is malformed, private, or not registered in any public registry — the query will fail and leave the field unpopulated.
- The project JSON already contains complete organism name and taxonomic metadata — re-querying is redundant.
- The external registry is unavailable or rate-limited during the scheduled enrichment window — consider retry logic or manual intervention.

## Inputs

- project JSON document (with genome_identifier field)
- genome identifier(s) (GenBank accession, IMG identifier, or equivalent public ID)

## Outputs

- enriched project JSON document (with organism_name and related taxonomic fields populated)
- validation log (schema compliance report)

## How to apply

Parse the input project JSON document to extract the genome identifier field. Query an external genome registry (e.g., NCBI Taxonomy, IMG, or equivalent) using the genome identifier to retrieve the organism name and any other desired metadata. Inject the retrieved values into the project JSON document as new or updated fields. Validate that the enriched JSON is well-formed, contains both the original genome identifier and the newly populated organism name, and conforms to the project schema. Write the enriched project JSON to the output file. The platform uses a redis queue to schedule these enrichment jobs asynchronously, ensuring scalability.

## Related tools

- **npm** (test runner and build tool for validating enriched JSON and running the task-queue job scheduler) — https://www.npmjs.com
- **redis queue** (job scheduler for asynchronously queuing and executing genome registry lookups)
- **GenBank / NCBI Taxonomy** (external registry API for retrieving organism names and taxonomic information from genome identifiers)
- **paired-data-form** (web application and API that implements project JSON enrichment and provides the JSON schema validation) — https://github.com/iomega/paired-data-form

## Evaluation signals

- The enriched project JSON validates against the app/public/schema.json schema with no errors.
- The organism_name field is populated with a non-empty, non-null string matching a known organism in the external registry.
- The original genome_identifier field remains present and unchanged in the enriched document.
- The enriched document can be stored to disk and retrieved without data loss or corruption.
- The redis queue job completes without timeout or connection errors to the external registry.

## Limitations

- Broken or changed external registry API endpoints (e.g., GNPS task ID links) will cause enrichment to fail silently or return stale data; the platform requires periodic validation of registry URLs.
- Genome identifiers with spaces or special characters may not resolve correctly due to URL encoding issues (GitHub issue #75 noted this limitation).
- Lack of inline field documentation means developers may not know which genome identifier formats are expected or supported; this can lead to malformed enrichment attempts.

## Evidence

- [readme] The scientific species name is fetched from GenBank using the public genome identifiers in the project.: "For example, the scientific species name is fetched from GenBank using the public genome identifiers in the project."
- [other] Query an external genome registry using the genome identifier to retrieve the organism name.: "Query an external genome registry (e.g. NCBI Taxonomy, IMG, or equivalent) using the genome identifier to retrieve the organism name."
- [other] Inject the retrieved organism name into the project JSON document as a new or updated field.: "Inject the retrieved organism name into the project JSON document as a new or updated field."
- [other] Validate that the enriched JSON is well-formed and contains both the original genome identifier and the newly populated organism name.: "Validate that the enriched JSON is well-formed and contains both the original genome identifier and the newly populated organism name."
- [readme] The web service uses a redis queue to schedule jobs to fetch more information about the public identifiers.: "The web service uses a redis queue (v5.0.5) to schedule jobs to fetch more information about the public identifiers and to upload the projects to Zenodo each month."
