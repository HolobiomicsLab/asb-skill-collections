---
name: sequence-availability-assessment
description: Use when you maintain or curate a specialized sequence repository (such as MIBiG) and need to identify which sequences in your local genbanks directory are not publicly available via NCBI GenBank/RefSeq databases.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3071
  - http://edamontology.org/topic_0080
  tools:
  - Git
  - NCBI GenBank/RefSeq API
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

# sequence-availability-assessment

## Summary

Cross-reference sequence files stored in a specialized repository's genbanks directory against NCBI GenBank/RefSeq to identify sequences absent from public databases. This skill is essential when determining data provenance and identifying sequences maintained only in specialized repositories.

## When to use

Apply this skill when you maintain or curate a specialized sequence repository (such as MIBiG) and need to identify which sequences in your local genbanks directory are not publicly available via NCBI GenBank/RefSeq databases. Use it to audit data completeness, document sequences of research significance that lack NCBI availability, and generate manifests of non-redundant sequence holdings.

## When NOT to use

- If your input sequences are already confirmed to originate from NCBI GenBank/RefSeq — no need to re-validate availability.
- If you lack accession identifiers or structured metadata linking sequences to GenBank/RefSeq identifiers — the cross-reference step will fail.
- If your genbanks directory contains only sequences you have already validated as NCBI-sourced.

## Inputs

- genbanks directory containing sequence files from a specialized repository
- JSON metadata files with cluster.status field and GenBank/RefSeq accession information
- NCBI GenBank/RefSeq database (via API or web access)

## Outputs

- Manifest CSV or JSON file with columns: filename, accession, availability_status, metadata_notes
- List of sequence files not available from NCBI public databases
- Audit report of non-redundant sequence holdings

## How to apply

Clone or access the repository (e.g., mibig-json from GitHub) and enumerate all sequence files in the genbanks directory. For each file, parse associated JSON metadata to extract the cluster.status field and GenBank/RefSeq accession identifiers. Cross-reference each accession against NCBI GenBank/RefSeq databases via API or web lookup to determine availability status. Compile results into a structured manifest (CSV or JSON) recording filename, accession, availability status, and metadata indicating why sequences remain unavailable from NCBI. The decision point is cluster.status: entries with status 'active' or similar indicate curated sequences requiring validation.

## Related tools

- **Git** (Clone or access the mibig-json repository to retrieve genbanks directory and JSON metadata) — github.com/mibig-secmet/mibig-json
- **NCBI GenBank/RefSeq API** (Query GenBank/RefSeq databases to determine accession availability status)

## Examples

```
git clone https://github.com/mibig-secmet/mibig-json && ls -la mibig-json/genbanks/ | grep -E '\.gb|\.gbk' | awk '{print $NF}' | head -10
```

## Evaluation signals

- All files in genbanks directory have been processed and assigned an availability status (available or unavailable).
- Accessions marked as unavailable are manually spot-checked against NCBI web interface to confirm status.
- Manifest file contains no null/missing values in key fields (filename, accession, availability_status).
- JSON metadata cluster.status field aligns with availability assessment (e.g., 'active' entries in genbanks should show rationale for non-NCBI status).
- Row count in manifest matches total number of sequence files processed from genbanks directory.

## Limitations

- NCBI availability status can change over time; manifest is a point-in-time snapshot and requires periodic re-validation.
- Accession identifiers must be present and correctly formatted in JSON metadata; missing or malformed accessions will produce incomplete results.
- Cross-reference relies on NCBI API availability and rate limits; large-scale audits may require batching and delays.
- No changelog is maintained in the repository; version history and documentation of changes to genbanks directory are unavailable, making it difficult to track which sequences were added or modified.

## Evidence

- [readme] genbanks directory contains sequence files not available from NCBI: "The `genbanks` directory contains a handful of sequence files that are not available from NCBI's GenBank/RefSeq databases."
- [readme] cluster.status field tracks entry status in JSON metadata: "entry status is now tracked via the `cluster.status` field"
- [other] Workflow requires cross-referencing entries against NCBI databases: "Cross-reference each entry against NCBI GenBank/RefSeq databases to determine availability status."
- [other] Output is a structured manifest with availability and metadata: "Compile a manifest CSV or JSON file recording filename, accession, availability status, and any metadata indicating why the sequence is unavailable from NCBI."
