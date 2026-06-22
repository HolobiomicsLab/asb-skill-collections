---
name: repository-file-enumeration
description: Use when you need to inventory sequence files in a repository's designated directory and cross-reference them against public databases to identify sequences that are unique to the curated archive.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3778
  edam_topics:
  - http://edamontology.org/topic_0219
  tools:
  - Git
  - NCBI GenBank/RefSeq
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

# repository-file-enumeration

## Summary

Systematically list and catalog sequence files stored in a specialized bioinformatics repository directory (e.g., genbanks) to identify which entries lack corresponding public database records. This skill is essential when auditing data provenance and determining the scope of curated sequences not available through standard public archives.

## When to use

Apply this skill when you need to inventory sequence files in a repository's designated directory and cross-reference them against public databases to identify sequences that are unique to the curated archive. Specifically useful when the repository README or documentation indicates that some sequences are intentionally maintained locally because they are absent from NCBI GenBank/RefSeq.

## When NOT to use

- Input is a flat file list already compiled; use this skill only when enumerating from a live repository.
- The repository contains no curated sequences outside public databases; this skill targets repositories that intentionally maintain supplementary archives.
- Accession identifiers are not embedded in repository metadata; this skill depends on parseable structured data.

## Inputs

- GitHub repository URL (e.g., github.com/mibig-secmet/mibig-json)
- Directory path within repository containing sequence files (e.g., genbanks/)
- JSON metadata files with cluster.status and accession fields
- NCBI GenBank/RefSeq database access (API or web interface)

## Outputs

- Enumerated list of sequence files in repository directory
- Parsed metadata records (cluster.status, accession, availability)
- Manifest CSV or JSON with filename, accession, NCBI availability status
- Summary report of sequences absent from NCBI databases

## How to apply

Clone or access the target repository (e.g., mibig-json) and enumerate all files in the designated sequence directory (e.g., genbanks). Parse JSON metadata associated with each file to extract status fields (e.g., cluster.status) and accession identifiers. For each entry, query NCBI GenBank/RefSeq databases using the extracted accessions to determine public availability. Compile results into a structured manifest (CSV or JSON) recording filename, accession, availability status, and any metadata explaining why sequences are unavailable from NCBI. This approach documents the repository's role as a supplementary archive for sequences outside standard public repositories.

## Related tools

- **Git** (Clone and access the remote repository to enumerate and retrieve sequence files from the designated directory) — https://git-scm.com/
- **NCBI GenBank/RefSeq** (Query and cross-reference accession numbers to determine public availability status of each sequence entry) — https://www.ncbi.nlm.nih.gov/genbank/

## Examples

```
git clone https://github.com/mibig-secmet/mibig-json && find mibig-json/genbanks -type f -name '*.json' | while read f; do jq '.cluster.status, .cluster.ncbi_tax_id' "$f"; done > genbanks_manifest.txt
```

## Evaluation signals

- All files in the genbanks directory are enumerated with no missing entries in the final manifest.
- JSON metadata parsing extracts cluster.status and accession fields for 100% of records without errors or null values.
- NCBI GenBank/RefSeq cross-reference queries complete for all accessions; those not found in public databases are flagged as 'absent' or 'unavailable'.
- Manifest CSV/JSON schema is consistent and machine-readable; each row/record contains filename, accession, and status columns.
- Sample spot-checks of manifest entries against NCBI and MIBiG web interfaces confirm accuracy of availability status classification.

## Limitations

- Repository-level changes (additions, deletions, updates) are not tracked; no changelog is available to document version history or reason for file changes.
- NCBI database queries depend on current network availability and may experience latency for bulk accession lookups.
- Sequences may be present in GenBank/RefSeq under alternative accession formats or prefixes not captured by simple string matching.
- Repository metadata schema (cluster.status field) may vary across entries or evolve over time, requiring parsing logic updates.

## Evidence

- [readme] The genbanks directory contains sequence files not available from NCBI: "The `genbanks` directory contains a handful of sequence files that are not available from NCBI's GenBank/RefSeq databases."
- [readme] JSON metadata tracks entry status via cluster.status field: "entry status is now tracked via the `cluster.status` field"
- [other] Workflow for cross-referencing entries against NCBI databases: "For each file, parse the JSON metadata to extract the cluster.status field and GenBank/RefSeq accession information. 4. Cross-reference each entry against NCBI GenBank/RefSeq databases to determine"
- [other] Manifest compilation step for recording results: "Compile a manifest CSV or JSON file recording filename, accession, availability status, and any metadata indicating why the sequence is unavailable from NCBI."
