---
name: manifest-generation-and-documentation
description: Use when you need to audit a bioinformatics repository (such as MIBiG) to determine which sequence files are maintained locally but lack public accessions in NCBI GenBank/RefSeq. Use this to support curation workflows, data provenance tracking, or to identify candidate sequences for public release.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3071
  - http://edamontology.org/topic_0091
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

# Reconstruct the non-NCBI sequence inventory from the genbanks directory

## Summary

Generate a structured inventory manifest of sequence files held in a repository's local `genbanks` directory that are not available from NCBI's GenBank/RefSeq databases. This skill reconciles local file metadata with public sequence databases to identify and document sequences unique to the repository.

## When to use

Apply this skill when you need to audit a bioinformatics repository (such as MIBiG) to determine which sequence files are maintained locally but lack public accessions in NCBI GenBank/RefSeq. Use this to support curation workflows, data provenance tracking, or to identify candidate sequences for public release.

## When NOT to use

- Input sequence files are already linked to public NCBI accessions and no audit of local-only sequences is needed.
- The genbanks directory does not exist or is empty in the target repository.
- NCBI E-utilities or BLAST access is unavailable and cross-referencing cannot be performed.

## Inputs

- MIBiG repository cloned from github.com/mibig-secmet/mibig-json
- genbanks directory containing sequence files
- NCBI GenBank/RefSeq database (via E-utilities or BLAST)

## Outputs

- Structured manifest (CSV or JSON) with columns: file path, sequence identifier, GenBank accession, availability status (local-only or public)

## How to apply

Clone or access the target repository and enumerate all files in the `genbanks` directory, extracting sequence identifiers and any embedded NCBI accession numbers. For each file, cross-reference the accession against NCBI GenBank/RefSeq using NCBI E-utilities or local BLAST searches to establish availability status. Files with valid public accessions are marked as publicly available; files with no matching accession or accession lookup failures are flagged as local-only. Compile the results into a structured manifest (CSV or JSON) recording filename, entry identifier, accession (if present), and a local-only status flag. This reconciliation approach ensures completeness and helps distinguish curated or proprietary sequences from those already in the public domain.

## Related tools

- **NCBI E-utilities** (Query NCBI GenBank/RefSeq databases to verify accession availability and retrieve sequence metadata for cross-referencing)
- **BLAST** (Perform local sequence similarity searches to determine whether sequences are present in NCBI GenBank/RefSeq or are unique to the local genbanks directory)

## Evaluation signals

- Manifest file is generated and contains all expected columns: file path, sequence identifier, GenBank accession, and availability flag.
- All files in the genbanks directory are represented in the manifest with no missing entries.
- Accession lookups return consistent results when spot-checked against NCBI's online interfaces or local BLAST databases.
- Local-only sequences have blank or 'N/A' accession fields, while public sequences carry valid NCBI accessions and availability = 'public'.
- Manifest can be parsed as valid CSV/JSON and round-trips without data loss.

## Limitations

- Some sequence files in the genbanks directory may lack embedded accession identifiers, requiring sequence-level similarity searches (BLAST) which may be computationally expensive or ambiguous for highly similar or fragmented sequences.
- NCBI E-utilities queries may timeout or rate-limit if the number of accessions is very large; batch queries or delays may be necessary.
- Sequences that are novel or significantly divergent from public databases may not be detected as local-only without full de novo assembly or annotation.
- No changelog is available in the repository documentation to track historical changes to the genbanks directory, limiting provenance tracking.

## Evidence

- [readme] The `genbanks` directory contains a handful of sequence files that are not available from NCBI's GenBank/RefSeq databases.: "The `genbanks` directory contains a handful of sequence files that are not available from NCBI's GenBank/RefSeq databases"
- [other] Cross-reference each file against NCBI GenBank/RefSeq accession identifiers (using NCBI E-utilities or local BLAST) to determine availability status.: "Cross-reference each file against NCBI GenBank/RefSeq accession identifiers (using NCBI E-utilities or local BLAST) to determine availability status"
- [other] Compile results into a structured manifest recording filename, entry identifier, accession (if present), and local-only status flag.: "Compile results into a structured manifest recording filename, entry identifier, accession (if present), and local-only status flag"
- [other] Output the manifest as a CSV or JSON file with columns for file path, sequence identifier, GenBank accession, and availability (local-only or public).: "Output the manifest as a CSV or JSON file with columns for file path, sequence identifier, GenBank accession, and availability (local-only or public)"
