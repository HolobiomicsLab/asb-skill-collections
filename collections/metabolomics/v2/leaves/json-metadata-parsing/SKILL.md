---
name: json-metadata-parsing
description: Use when you have a repository of JSON-formatted scientific annotations
  (e.g., MIBiG curation data) and need to systematically extract structured metadata
  fields (such as cluster.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3071
  - http://edamontology.org/topic_0091
  tools:
  - Git
  - JSON parser (Python json module or equivalent)
  - NCBI Entrez API or local GenBank/RefSeq mirror
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1093/nar/gkz882
  title: MIBiG 2.0
evidence_spans:
- github.com/mibig-secmet/mibig-json
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

# json-metadata-parsing

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Extract and parse metadata from JSON-formatted scientific data files to identify entry status, accession information, and availability flags. This skill enables cross-referencing of JSON annotations against external databases to compile manifests of sequence provenance and curation state.

## When to use

Apply this skill when you have a repository of JSON-formatted scientific annotations (e.g., MIBiG curation data) and need to systematically extract structured metadata fields (such as cluster.status or GenBank/RefSeq accession identifiers) to determine which entries are available in external reference databases or to identify gaps in public availability.

## When NOT to use

- Input JSON files do not contain accession identifiers or status fields needed for cross-referencing.
- The goal is to modify or re-annotate JSON entries rather than extract and inventory metadata.
- JSON data already have been validated against external databases and a manifest already exists.

## Inputs

- JSON annotation files from a curated repository directory (e.g., mibig-json/genbanks/)
- Repository metadata (cluster.status field, GenBank/RefSeq accession identifiers)
- NCBI GenBank/RefSeq database for cross-referencing

## Outputs

- Manifest file (CSV or JSON) with columns: filename, accession, availability_status, metadata_notes
- Set of sequence files not available in NCBI public databases
- Compiled metadata records associating each entry with its curation status

## How to apply

Clone or access the JSON repository and enumerate all JSON files in the target directory. For each file, parse the JSON object and extract the relevant metadata fields (e.g., cluster.status, GenBank accession numbers, RefSeq identifiers). Cross-reference the extracted accessions against NCBI GenBank/RefSeq databases to determine availability status. Compile a manifest (CSV or JSON) recording filename, accession, availability status, and any metadata explaining why the entry is unavailable. The rationale is that JSON metadata fields like cluster.status directly encode curation information that, when systematized, reveals which sequences are curated locally but not deposited in public archives.

## Related tools

- **Git** (Clone or access the mibig-json repository to retrieve JSON annotation files for local parsing) — github.com/mibig-secmet/mibig-json
- **JSON parser (Python json module or equivalent)** (Deserialize JSON annotation objects and iterate over metadata fields such as cluster.status and accession identifiers)
- **NCBI Entrez API or local GenBank/RefSeq mirror** (Cross-reference extracted accessions to determine availability status in public databases)

## Evaluation signals

- All JSON files in the target directory were successfully parsed without deserialization errors.
- Manifest file contains a non-zero number of entries with complete filename, accession, and status columns.
- Cross-reference results are consistent: accessions marked as unavailable in the manifest do not resolve in NCBI GenBank/RefSeq queries.
- Manifest entries corresponding to cluster.status='active' or 'active_cluster' are correctly flagged with their availability status.
- No malformed accession identifiers or missing metadata fields in the output manifest.

## Limitations

- NCBI GenBank/RefSeq databases are updated frequently; availability status is a snapshot and may become stale.
- JSON files may be incomplete or lack accession fields, requiring fallback to other identifiers or manual curation.
- No changelog is available in the mibig-json repository, so version history and changes to metadata schema are not documented.
- Cross-referencing against NCBI requires network access and may be rate-limited.

## Evidence

- [readme] MIBiG curation data structure and status tracking: "This repository tracks the current [MIBiG] annotations in JSON format... entry status is now tracked via the `cluster.status` field."
- [readme] Presence of sequences not in NCBI databases: "The `genbanks` directory contains a handful of sequence files that are not available from NCBI's GenBank/RefSeq databases."
- [other] Cross-reference workflow specification: "For each file, parse the JSON metadata to extract the cluster.status field and GenBank/RefSeq accession information... Cross-reference each entry against NCBI GenBank/RefSeq databases to determine"
- [other] Output manifest structure: "Compile a manifest CSV or JSON file recording filename, accession, availability status, and any metadata indicating why the sequence is unavailable from NCBI."
