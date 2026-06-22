---
name: organism-metadata-retrieval
description: Use when when a project JSON document contains genome identifiers but lacks corresponding organism name annotations, and you need to link MS/MS mass spectra with genomic context for downstream biosynthetic gene cluster or chemical ecology analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_0080
  tools:
  - npm
  - redis queue
  - paired-data-form platform
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# organism-metadata-retrieval

## Summary

Enrich project JSON documents by querying external genome registries (e.g., NCBI Taxonomy, IMG) to fetch organism names corresponding to genome identifiers, then inject the retrieved metadata back into the project record. This skill enables integration of genomic information with mass spectrometry data in paired omics workflows.

## When to use

When a project JSON document contains genome identifiers but lacks corresponding organism name annotations, and you need to link MS/MS mass spectra with genomic context for downstream biosynthetic gene cluster or chemical ecology analysis.

## When NOT to use

- When the project JSON already contains organism name annotations from manual curation or prior enrichment.
- When genome identifiers are malformed, non-existent, or from private/proprietary databases not accessible to public registries.
- When the external registry API is unavailable or rate-limited, unless a fallback or retry mechanism with exponential backoff is implemented.

## Inputs

- Project JSON document with genome identifier field
- Genome identifier (from GenBank or equivalent public registry)

## Outputs

- Enriched project JSON document with organism name field populated
- Well-formed JSON with both original genome identifier and organism name

## How to apply

Parse the input project JSON document to extract the genome identifier field. Query an external genome registry (e.g., NCBI Taxonomy or IMG) using the genome identifier to retrieve the organism name. Inject the retrieved organism name into the project JSON document as a new or updated field. Validate that the enriched JSON is well-formed and contains both the original genome identifier and the newly populated organism name. Write the enriched project JSON to the output file. The enrichment is typically scheduled via a redis queue task, allowing asynchronous batch processing across multiple project records.

## Related tools

- **npm** (Build and test framework for running project enrichment scripts and validating JSON transformation in api/ and app/ directories) — https://www.npmjs.com/
- **redis queue** (Job scheduling system for asynchronous enrichment tasks; fetches organism names from GenBank using public genome identifiers)
- **paired-data-form platform** (Web application and API service that stores project JSON documents and orchestrates genome-to-organism metadata enrichment via task queue) — https://github.com/iomega/paired-data-form

## Evaluation signals

- Enriched JSON is valid against the schema (app/public/schema.json)
- Original genome identifier field remains present and unchanged in output
- Newly populated organism name field contains non-empty, non-null string value
- No malformed or truncated fields introduced during JSON serialization
- Organism name retrieved matches expected nomenclature for the queried genome identifier (manual spot-check against GenBank entry)

## Limitations

- External registry availability and API rate limits may cause enrichment failures or delays; no fallback mechanism is documented for missing or unresolvable genome identifiers.
- Broken or outdated links to external registries (e.g., GNPS task identifier links noted as broken in issue #81) may prevent validation of linked data.
- No documented specification of field descriptions and requirements for organism name format, encoding, or required length, limiting schema validation rigor.

## Evidence

- [readme] The web service uses a redis queue (v5.0.5) to schedule jobs to fetch more information about the public identifiers and to upload the projects to Zenodo each month. For example, the scientific species name is fetched from GenBank using the public genome identifiers in the project.: "redis queue (v5.0.5) to schedule jobs to fetch more information about the public identifiers... the scientific species name is fetched from GenBank using the public genome identifiers in the project"
- [intro] The platform links MS/MS mass spectra with genome, sample preparation, extraction method and instrumentation method: "Links MS/MS mass spectra with genome, sample preparation, extraction method and instrumentation method"
- [other] 1. Parse the input project JSON document to extract the genome identifier field. 2. Query an external genome registry (e.g. NCBI Taxonomy, IMG, or equivalent) using the genome identifier to retrieve the organism name. 3. Inject the retrieved organism name into the project JSON document as a new or updated field. 4. Validate that the enriched JSON is well-formed and contains both the original genome identifier and the newly populated organism name. 5. Write the enriched project JSON to the output file.: "Parse the input project JSON document to extract the genome identifier field. 2. Query an external genome registry (e.g. NCBI Taxonomy, IMG, or equivalent) using the genome identifier to retrieve the"
- [other] make sure the existing tests still work by running ``npm run test`` in `api/` and/or `app/` directory: "npm run test in `api/` and/or `app/` directory"
