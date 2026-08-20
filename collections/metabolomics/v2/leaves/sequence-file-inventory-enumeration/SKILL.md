---
name: sequence-file-inventory-enumeration
description: Use when when you maintain a repository with local sequence files and
  need to determine which sequences are not publicly available in NCBI GenBank/RefSeq
  databases—for example, to distinguish proprietary or supplementary sequence data
  from publicly registered entries, or to create an inventory.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3053
  - http://edamontology.org/topic_0080
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

# sequence-file-inventory-enumeration

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Systematically enumerate and cross-reference sequence files in a local repository (MIBiG's genbanks directory) against NCBI GenBank/RefSeq to identify sequences that are unavailable in public databases. This skill is essential for curating and documenting unique or restricted sequence assets.

## When to use

When you maintain a repository with local sequence files and need to determine which sequences are not publicly available in NCBI GenBank/RefSeq databases—for example, to distinguish proprietary or supplementary sequence data from publicly registered entries, or to create an inventory manifest for data governance.

## When NOT to use

- Input directory contains only already-validated NCBI accessions with no local sequences—use a simple accession lookup instead.
- Sequences are known to be private or restricted by license and you do not need public availability confirmation—enumeration is unnecessary overhead.

## Inputs

- Local sequence file directory (e.g., genbanks directory in MIBiG repository)
- Sequence file metadata (filename, entry identifier, optional NCBI accession)
- NCBI GenBank/RefSeq database (via E-utilities or BLAST index)

## Outputs

- Structured inventory manifest (CSV or JSON format)
- Manifest columns: file path, sequence identifier, GenBank accession, availability status (local-only or public)

## How to apply

Clone or access the target repository (e.g., MIBiG's github.com/mibig-secmet/mibig-json) and list all sequence files in the designated directory (e.g., `genbanks`). For each file, extract its entry identifier and any embedded NCBI accession number. Use NCBI E-utilities or local BLAST to query whether that accession exists in GenBank/RefSeq; if no accession is present or the query returns no hit, flag it as local-only. Compile results into a structured manifest (CSV or JSON) with columns for file path, sequence identifier, GenBank accession (if present), and availability status (local-only or public). The rationale is to create a transparent, machine-readable record of which sequences are unique to the repository versus mirrored from public sources.

## Related tools

- **NCBI E-utilities** (Query NCBI GenBank/RefSeq accession identifiers to determine if a sequence is publicly registered)
- **BLAST** (Local or remote sequence similarity search to cross-reference local sequences against GenBank/RefSeq and confirm accession status)

## Evaluation signals

- Manifest file exists and contains all expected columns (file path, sequence identifier, GenBank accession, availability status).
- No sequence files from the input directory are missing from the manifest; row count equals file count.
- For each row marked 'public', the GenBank accession field is non-empty and validated; for 'local-only' rows, accession is empty or null.
- Spot-check: manually verify 3–5 flagged 'local-only' sequences by querying NCBI directly; no false negatives (sequences marked local but actually public in GenBank).
- Manifest is well-formed JSON or valid CSV with no malformed cells or unexpected null values.

## Limitations

- NCBI E-utilities queries may have rate limits or temporary unavailability; plan for retry logic or fallback to manual spot-checks.
- Sequences without embedded NCBI accessions cannot be definitively cross-referenced unless you perform full BLAST alignment, which is slower and may not always yield a clear match.
- The MIBiG repository maintains only 'a handful' of local sequences, so the inventory may be small and may not justify high automation investment.
- Accession identifiers may be outdated or withdrawn from NCBI; the manifest reflects status at query time only.

## Evidence

- [readme] The `genbanks` directory contains a handful of sequence files that are not available from NCBI's GenBank/RefSeq databases: "The `genbanks` directory contains a handful of sequence files that are not available from NCBI's GenBank/RefSeq databases."
- [other] Scan the genbanks directory, cross-reference against NCBI accession identifiers, and compile results into a structured manifest: "Scan the `genbanks` directory to list all sequence files and their metadata. 3. Cross-reference each file against NCBI GenBank/RefSeq accession identifiers (using NCBI E-utilities or local BLAST) to"
- [other] Output should be CSV or JSON with columns for file path, sequence identifier, GenBank accession, and availability: "Output the manifest as a CSV or JSON file with columns for file path, sequence identifier, GenBank accession, and availability (local-only or public)."
- [other] Tools to use for cross-referencing and validation: "tools: NCBI E-utilities, BLAST"
