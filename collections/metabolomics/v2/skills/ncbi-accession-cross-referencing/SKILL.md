---
name: ncbi-accession-cross-referencing
description: Use when you have parsed a collection of sequence files with associated GenBank/RefSeq accession identifiers (typically from JSON metadata fields like cluster.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3071
  - http://edamontology.org/topic_0080
  tools:
  - Git
  - NCBI Entrez API
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
---

# ncbi-accession-cross-referencing

## Summary

Cross-reference sequence file accessions extracted from JSON metadata against NCBI GenBank/RefSeq databases to determine availability status and identify sequences maintained locally but absent from public repositories. This skill surfaces sequences of interest that may be curated, restricted, or otherwise unavailable through standard NCBI channels.

## When to use

Apply this skill when you have parsed a collection of sequence files with associated GenBank/RefSeq accession identifiers (typically from JSON metadata fields like cluster.status or accession records) and need to determine which entries are actually available in public NCBI databases versus which are maintained only locally in a repository's genbanks directory.

## When NOT to use

- Input accessions are not GenBank/RefSeq format or are incomplete (missing NCBI-standard identifiers).
- You only need to verify that sequences exist locally; public availability status is not relevant to your analysis.
- The genbanks directory contains non-sequence files or files without associated accession metadata.

## Inputs

- MIBiG JSON metadata files with cluster.status and accession fields
- genbanks directory listing (filenames and associated accessions)
- NCBI GenBank/RefSeq public database (accessed via API or web query)

## Outputs

- Manifest CSV or JSON file with columns: filename, accession, availability_status (found/not_found), metadata_rationale
- Inventory of sequences absent from NCBI GenBank/RefSeq
- Mapping of local sequence files to their public availability status

## How to apply

Extract GenBank/RefSeq accession numbers from the JSON metadata (particularly the cluster.status field) for each sequence file in the target directory. For each accession, query the NCBI GenBank/RefSeq databases using their public APIs or web interface to verify availability. Record the availability status (found/not found), any associated metadata indicating why a sequence is absent from NCBI (e.g., curation status, restricted access, or local-only maintenance), and compile results into a structured manifest (CSV or JSON) with columns for filename, accession, availability status, and rationale. This cross-referencing reveals gaps between local curation and public sequence repositories.

## Related tools

- **Git** (Clone and access the mibig-json repository to obtain the genbanks directory and JSON metadata files) — github.com/mibig-secmet/mibig-json
- **NCBI Entrez API** (Query GenBank/RefSeq databases to verify accession availability and retrieve metadata)

## Evaluation signals

- Manifest file is valid CSV/JSON with all required columns (filename, accession, availability_status, metadata_rationale) and no missing entries.
- All accessions are correctly formatted as NCBI identifiers (e.g., NC_*, NZ_*, or GenBank accession patterns).
- Spot-check: manually verify a sample of 'not_found' accessions against the NCBI web interface to confirm they are genuinely absent from public databases.
- Cross-referencing is complete: every sequence file in the genbanks directory with an associated accession appears exactly once in the manifest.
- Metadata rationale field is populated consistently; entries marked 'not_found' should include a reason (e.g., curation status, local-only).

## Limitations

- NCBI GenBank/RefSeq databases are continuously updated; accessions may become available or deprecated over time, so results are a snapshot at the time of query.
- Accession format variations or parsing errors in JSON metadata may lead to false 'not_found' results if identifiers are malformed or incomplete.
- The genbanks directory README indicates it contains 'a handful' of sequences; this skill is designed for small to moderate collections and may require rate-limiting or caching if applied to very large repositories.
- No changelog is maintained for the mibig-json repository, so it is difficult to track when sequences were added or removed from the genbanks directory.

## Evidence

- [abstract] workflow_step_1: "For each file, parse the JSON metadata to extract the cluster.status field and GenBank/RefSeq accession information."
- [abstract] workflow_step_2: "Cross-reference each entry against NCBI GenBank/RefSeq databases to determine availability status."
- [abstract] workflow_step_3: "Compile a manifest CSV or JSON file recording filename, accession, availability status, and any metadata indicating why the sequence is unavailable from NCBI."
- [readme] finding_rationale: "The `genbanks` directory contains a handful of sequence files that are not available from NCBI's GenBank/RefSeq databases."
- [readme] metadata_structure: "entry status is now tracked via the `cluster.status` field"
