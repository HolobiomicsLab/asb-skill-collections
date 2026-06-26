---
name: ncbi-database-cross-referencing
description: Use when you have a collection of sequence files (e.g., GenBank format
  files in a repository directory) and need to determine which ones lack corresponding
  entries in NCBI's GenBank or RefSeq databases.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0080
  - http://edamontology.org/topic_3053
  tools:
  - NCBI E-utilities
  - BLAST
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1093/nar/gkac1049
  title: MIBiG 3.0
evidence_spans:
- NCBI's GenBank/RefSeq databases
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/nar/gkac1049
  all_source_dois:
  - 10.1093/nar/gkac1049
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ncbi-database-cross-referencing

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Cross-reference local sequence files against NCBI GenBank/RefSeq accession identifiers to determine which sequences are unavailable from public databases. This skill identifies locally-curated sequences not yet deposited in NCBI, critical for inventory management and data provenance tracking in sequence repositories.

## When to use

You have a collection of sequence files (e.g., GenBank format files in a repository directory) and need to determine which ones lack corresponding entries in NCBI's GenBank or RefSeq databases. This is particularly relevant when maintaining curated sequence repositories that may include novel or unpublished sequences not yet submitted to NCBI.

## When NOT to use

- Input sequences are already known to be NCBI-deposited (accessions already verified)
- No network access to NCBI or local BLAST database available for querying
- Sequence files lack identifiers or metadata necessary to perform accession lookup

## Inputs

- Directory of sequence files (GenBank format or similar)
- Sequence identifiers and embedded accession numbers
- NCBI GenBank/RefSeq database (accessed via E-utilities or BLAST)

## Outputs

- Structured manifest (CSV or JSON) with columns: file path, sequence identifier, GenBank accession, availability status (local-only or public)
- Inventory of sequences not available from NCBI

## How to apply

Scan the local sequence directory to extract all sequence identifiers and any embedded NCBI accession numbers. For each sequence, query NCBI GenBank/RefSeq using E-utilities (programmatic access via API) or perform local BLAST alignment against downloaded NCBI reference sequences to determine public availability. Records that return no match or no valid accession identifier are flagged as local-only. Compile cross-reference results into a structured manifest with columns tracking filename, sequence identifier, GenBank accession (if present), and local-only status flag. This manifest serves as both an inventory and a record of which sequences require future submission to NCBI.

## Related tools

- **NCBI E-utilities** (Programmatic querying of GenBank/RefSeq accession identifiers to check public availability)
- **BLAST** (Local or remote similarity search to cross-reference sequences against NCBI reference databases)

## Evaluation signals

- All sequence files in the directory have been assigned either a GenBank accession or a local-only flag
- Cross-reference results are reproducible: re-querying the same files yields consistent accession matches or non-matches
- Manifest schema is valid (all required columns present, no malformed entries)
- Accession numbers returned match the format and length expected for GenBank identifiers (e.g., alphanumeric prefix + numeric suffix)
- Spot-check: known public sequences are correctly matched to their NCBI accessions; known local sequences are correctly flagged

## Limitations

- Sequences lacking embedded accession numbers or identifiers cannot be reliably cross-referenced; manual curation may be required
- NCBI databases are continuously updated; a sequence marked local-only today may appear in GenBank after future submissions
- BLAST or E-utilities query results depend on sequence similarity threshold and query parameters; borderline matches may yield false positives or false negatives
- The `genbanks` directory in MIBiG contains 'a handful' of local-only sequences, suggesting the inventory is small and curated, but scale and maintenance burden were not quantified

## Evidence

- [other] Which sequence files in the `genbanks` directory are not available from NCBI's GenBank/RefSeq databases?: "Which sequence files in the `genbanks` directory are not available from NCBI's GenBank/RefSeq databases?"
- [other] The MIBiG repository maintains a `genbanks` directory containing sequence files that are not available from NCBI's GenBank/RefSeq databases.: "The MIBiG repository maintains a `genbanks` directory containing sequence files that are not available from NCBI's GenBank/RefSeq databases."
- [other] Scan the `genbanks` directory to list all sequence files and their metadata. Cross-reference each file against NCBI GenBank/RefSeq accession identifiers (using NCBI E-utilities or local BLAST) to determine availability status.: "Scan the `genbanks` directory to list all sequence files and their metadata. Cross-reference each file against NCBI GenBank/RefSeq accession identifiers (using NCBI E-utilities or local BLAST) to"
- [other] Output the manifest as a CSV or JSON file with columns for file path, sequence identifier, GenBank accession, and availability (local-only or public).: "Output the manifest as a CSV or JSON file with columns for file path, sequence identifier, GenBank accession, and availability (local-only or public)."
- [readme] The `genbanks` directory contains a handful of sequence files that are not available from NCBI's GenBank/RefSeq databases.: "The `genbanks` directory contains a handful of sequence files that are not available from NCBI's GenBank/RefSeq databases."
