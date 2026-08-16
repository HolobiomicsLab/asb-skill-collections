---
name: mibig-metadata-extraction
description: Use when when you need to audit, inventory, or report on the curation
  state of MIBiG entries; when cluster.status values must be validated or aggregated
  for quality control; when building a status index to support data governance or
  release workflows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_3407
  tools:
  - mibig-json repository
  - MIBiG web interface
  license_tier: restricted
derived_from:
- doi: 10.1093/nar/gkz882
  title: MIBiG 2.0
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mibig_2_0_cq
    doi: 10.1093/nar/gkz882
    title: MIBiG 2.0
  dedup_kept_from: coll_mibig_2_0_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/nar/gkz882
  all_source_dois:
  - 10.1093/nar/gkz882
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mibig-metadata-extraction

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Extract and aggregate entry-level metadata from MIBiG JSON files, particularly the cluster.status field, to construct a comprehensive index of curation status across the repository. This skill enables systematic tracking and validation of annotation completeness in the MIBiG secondary metabolite database.

## When to use

When you need to audit, inventory, or report on the curation state of MIBiG entries; when cluster.status values must be validated or aggregated for quality control; when building a status index to support data governance or release workflows.

## When NOT to use

- When only sequence data or GenBank files are needed — use the genbanks directory instead
- When a pre-built, curated status index is already available from MIBiG's public API or web interface
- When cluster.status field semantics or controlled vocabulary are not documented — context required first

## Inputs

- MIBiG JSON file collection (from mibig-json/data directory)
- Entry identifier mappings (filename or internal ID field)

## Outputs

- Structured entry-status index (CSV or JSON format)
- Validation report (parsing completeness, missing status fields)

## How to apply

Clone or download the mibig-json repository from github.com/mibig-secmet/mibig-json and locate the `data` directory. Iterate over all JSON files in the directory, parsing each file to extract the entry identifier (from filename or internal ID field) and the `cluster.status` field value. Aggregate the extracted tuples into a structured index using CSV or JSON format with columns for entry ID and cluster status. Validate that all JSON files have been parsed, that every entry has a status value present, and that status values conform to the expected controlled vocabulary. Manual expert review is recommended to spot-check a sample of entries against the original JSON structure.

## Related tools

- **mibig-json repository** (Source repository containing JSON-formatted MIBiG curation data with cluster.status fields) — https://github.com/mibig-secmet/mibig-json
- **MIBiG web interface** (Reference for validating extracted status values and understanding entry metadata schema) — https://mibig.secondarymetabolites.org/

## Evaluation signals

- All JSON files in the data directory have been successfully parsed with no read errors
- Entry count in output index matches the total number of JSON files in data directory
- Every entry in the index has a non-null cluster.status value
- Status values conform to the expected controlled vocabulary (manually verified against sample entries)
- Index is sortable, searchable, and can be linked back to original JSON files by entry ID

## Limitations

- No changelog is available in the repository to document version history or changes to the cluster.status field semantics
- Manual expert review is required to validate status field values — automated validation alone cannot ensure semantic correctness
- The index will only be as current as the last repository clone/download; updates require re-running the extraction workflow

## Evidence

- [intro] MIBiG curation data is maintained in JSON format with entry status tracked through the `cluster.status` field: "MIBiG curation data in JSON format... entry status is now tracked via the `cluster.status` field"
- [readme] The data directory contains the current MIBiG datasets: "The current datasets for [MIBiG] live in the `data` directory, entry status is now tracked via the `cluster.status` field"
- [other] Extraction workflow steps including cloning, JSON parsing, field extraction, and aggregation: "Clone or download the mibig-json repository from github.com/mibig-secmet/mibig-json. 2. Locate and read all JSON files in the `data` directory. 3. For each JSON file, extract the entry identifier"
- [other] Validation of extraction completeness and status value presence: "Validate that all entries have been parsed and status values are present"
