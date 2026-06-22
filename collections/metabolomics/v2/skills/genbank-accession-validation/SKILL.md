---
name: genbank-accession-validation
description: Use when you have a collection of sequence files (e.g., in a `genbanks` directory) and need to determine which are publicly available via NCBI and which are maintained locally only. This is critical for repositories like MIBiG that curate sequence data with mixed provenance.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0219
  - http://edamontology.org/topic_0080
  tools:
  - BLAST
  - NCBI E-utilities
derived_from:
- doi: 10.1093/nar/gkac1049
  title: MIBiG 3.0
evidence_spans:
- GenBank/RefSeq databases
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mibig_3_0_cq
    doi: 10.1093/nar/gkac1049
    title: MIBiG 3.0
  dedup_kept_from: coll_mibig_3_0_cq
schema_version: 0.2.0
---

# genbank-accession-validation

## Summary

Validate whether sequence files in a local repository have corresponding entries in NCBI's GenBank/RefSeq databases by cross-referencing accession identifiers. This skill identifies sequences maintained only locally (non-NCBI) and flags their availability status for inventory tracking.

## When to use

Apply this skill when you have a collection of sequence files (e.g., in a `genbanks` directory) and need to determine which are publicly available via NCBI and which are maintained locally only. This is critical for repositories like MIBiG that curate sequence data with mixed provenance.

## When NOT to use

- The sequence files already have a pre-validated NCBI accession and you only need to retrieve metadata (use direct NCBI API fetch instead).
- You are working exclusively with sequences you know are local-only and do not need public availability confirmation.
- The input is a curated GenBank file already downloaded from NCBI (cross-validation is unnecessary).

## Inputs

- Directory path containing sequence files (e.g., `genbanks` directory)
- Sequence file metadata (filenames, embedded identifiers)
- NCBI GenBank/RefSeq accession identifiers (where present in files or metadata)

## Outputs

- Structured manifest (CSV or JSON file) with columns: file path, sequence identifier, GenBank accession, availability flag (local-only or public)
- Inventory of sequences not available from NCBI

## How to apply

First, scan the local sequence directory to extract all filenames and embedded sequence identifiers or accession numbers. For each entry, query NCBI E-utilities or perform a local BLAST search against GenBank/RefSeq to check for a match. Record the result (found in public database or local-only) in a structured manifest. The decision point is whether an NCBI accession identifier is present and resolvable; if the lookup fails or returns no hit, flag the sequence as local-only. Compile all records into a CSV or JSON manifest with columns for file path, sequence identifier, GenBank accession (if present), and availability status.

## Related tools

- **NCBI E-utilities** (Query NCBI GenBank/RefSeq databases to check accession identifier availability and retrieve record status)
- **BLAST** (Perform local sequence alignment against GenBank/RefSeq (or local mirror) to determine if a sequence exists in public databases)

## Evaluation signals

- Manifest file is generated and contains all sequence files from the input directory with no missing rows.
- Each row in the manifest has non-empty values for file path, sequence identifier, and availability flag.
- Spot-check: sequences with known NCBI accessions are marked as 'public'; sequences without accessions or failed NCBI lookups are marked as 'local-only'.
- No duplicate file paths or sequence identifiers in the manifest (uniqueness invariant).
- Cross-validation: requery a sample of 'public' accessions against NCBI E-utilities to confirm they resolve successfully.

## Limitations

- Accession identifiers may be malformed, missing, or embedded inconsistently across sequence file formats, requiring manual curation of edge cases.
- NCBI E-utilities rate limits and network delays may slow validation of large inventories; local BLAST queries require a current GenBank mirror.
- Sequences may be deposited in NCBI but not yet indexed, causing false 'local-only' classifications; periodic re-validation is recommended.
- The skill does not validate sequence content or integrity—only presence/absence in public databases.

## Evidence

- [other] Workflow step for identifying non-NCBI sequences: "The `genbanks` directory contains a handful of sequence files that are not available from NCBI's GenBank/RefSeq databases."
- [other] Research question defining the task: "Which sequence files in the `genbanks` directory are not available from NCBI's GenBank/RefSeq databases?"
- [other] Cross-referencing method: "Cross-reference each file against NCBI GenBank/RefSeq accession identifiers (using NCBI E-utilities or local BLAST) to determine availability status."
- [other] Output format specification: "Output the manifest as a CSV or JSON file with columns for file path, sequence identifier, GenBank accession, and availability (local-only or public)."
