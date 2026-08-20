---
name: local-sequence-availability-assessment
description: Use when you need to determine which sequence files in a repository like
  MIBiG are unique to that resource and not mirrored in NCBI public databases.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0080
  - http://edamontology.org/topic_3301
  tools:
  - BLAST
  - NCBI E-utilities
  license_tier: restricted
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

# local-sequence-availability-assessment

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Identify and catalog sequence files in a repository's local genbanks directory that are not publicly available in NCBI's GenBank/RefSeq databases. This skill is essential for understanding the scope of non-redundant sequences maintained by secondary metabolite repositories and for tracking curation inventory.

## When to use

Apply this skill when you need to determine which sequence files in a repository like MIBiG are unique to that resource and not mirrored in NCBI public databases. Use it to audit local-only holdings, prioritize curation efforts, or document the added value of a repository's sequence collection beyond public archives.

## When NOT to use

- Input is a single, already-identified sequence: this skill is designed for bulk directory assessment, not validation of individual entries.
- NCBI database access is unavailable or severely rate-limited: the skill requires reliable cross-reference queries; offline or restricted environments will produce incomplete results.
- The goal is to retrieve sequences themselves rather than audit availability: this skill catalogs status, not downloads or extracts the actual sequence data.

## Inputs

- genbanks directory (local repository file tree)
- sequence file metadata (filename, entry identifiers, accession numbers if present)
- NCBI GenBank/RefSeq database (via API or local copy)

## Outputs

- structured manifest (CSV or JSON) with columns: file path, sequence identifier, GenBank accession, local-only status flag
- inventory of non-NCBI sequences with identifiers and metadata

## How to apply

Scan the local genbanks directory to enumerate all sequence files and extract their identifiers and metadata. Cross-reference each file's accession identifier (if present) against NCBI GenBank/RefSeq using NCBI E-utilities API queries or local BLAST searches to test for public availability. For files without explicit accessions, attempt sequence similarity matching via BLAST to infer whether the sequence exists in public databases under a different identifier. Compile results into a structured manifest (CSV or JSON) recording the file path, sequence identifier, GenBank accession status, and a binary local-only flag. Evaluate correctness by confirming that files flagged as local-only return no hits in NCBI queries and that accession cross-references are current.

## Related tools

- **NCBI E-utilities** (Query NCBI GenBank/RefSeq accession databases to determine public availability of sequence identifiers)
- **BLAST** (Perform sequence similarity searches to infer public availability status for sequences without explicit accessions)

## Evaluation signals

- Manifest completeness: all files in the genbanks directory are listed with non-null file path, sequence identifier, and local-only flag.
- Accession validation: files flagged with a GenBank accession number are confirmed to resolve in NCBI E-utilities queries; files without accessions show zero BLAST hits in public databases.
- No false negatives: spot-check a sample of files flagged as local-only by independent NCBI search to confirm they are genuinely absent from public archives.
- Schema consistency: output CSV/JSON conforms to declared column structure with proper data types (e.g., boolean for local-only flag).
- Reproducibility: re-running the workflow on the same genbanks directory snapshot produces identical manifest output.

## Limitations

- Accession-based queries assume file metadata includes valid NCBI identifiers; poorly annotated or legacy entries may lack accessions, requiring fallback to BLAST and increasing runtime.
- BLAST sequence similarity matching is probabilistic and may miss distant homologs or sequences that have been heavily edited since deposition in NCBI; results are only as sensitive as the search parameters (e.g., e-value threshold).
- NCBI databases are dynamic: accessions may be deprecated, merged, or withdrawn; a sequence flagged as local-only at time T1 may later appear in NCBI, requiring periodic re-assessment.
- The README indicates 'a handful' of local-only sequences in MIBiG; this skill is most useful for larger or rapidly evolving repositories where manual audit is infeasible.

## Evidence

- [readme] The `genbanks` directory contains a handful of sequence files that are not available from NCBI's GenBank/RefSeq databases.: "The `genbanks` directory contains a handful of sequence files that are not available from NCBI's GenBank/RefSeq databases."
- [other] Cross-reference each file against NCBI GenBank/RefSeq accession identifiers (using NCBI E-utilities or local BLAST) to determine availability status.: "Cross-reference each file against NCBI GenBank/RefSeq accession identifiers (using NCBI E-utilities or local BLAST) to determine availability status."
- [other] Compile results into a structured manifest recording filename, entry identifier, accession (if present), and local-only status flag.: "Compile results into a structured manifest recording filename, entry identifier, accession (if present), and local-only status flag."
- [other] Output the manifest as a CSV or JSON file with columns for file path, sequence identifier, GenBank accession, and availability (local-only or public).: "Output the manifest as a CSV or JSON file with columns for file path, sequence identifier, GenBank accession, and availability (local-only or public)."
- [readme] entry status is now tracked via the `cluster.status` field: "entry status is now tracked via the `cluster.status` field"
