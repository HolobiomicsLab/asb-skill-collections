---
name: chemical-structure-integrity-verification
description: Use when you have received or downloaded an SDF-formatted compound database file and need to confirm it is not corrupted, contains the expected number of molecular records, and that each record is structurally valid before using it in compound identification, library matching, or database.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3433
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3407
  tools:
  - RDKit
derived_from:
- doi: 10.3389/fchem.2022.908572
  title: DNA adduct database
evidence_spans:
- compound database in SDF format
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_dna_adduct_database_cq
    doi: 10.3389/fchem.2022.908572
    title: DNA adduct database
  dedup_kept_from: coll_dna_adduct_database_cq
schema_version: 0.2.0
---

# chemical-structure-integrity-verification

## Summary

Validates the structural integrity and parseable format of a chemical compound database file (SDF) by parsing molecular records and confirming each entry represents a single, chemically valid compound. This skill ensures data quality before downstream analysis or integration into metabolomics or adductomics workflows.

## When to use

Apply this skill when you have received or downloaded an SDF-formatted compound database file and need to confirm it is not corrupted, contains the expected number of molecular records, and that each record is structurally valid before using it in compound identification, library matching, or database integration tasks.

## When NOT to use

- Input file is already in a different format (e.g., CSV, JSON, mol2) and no SDF version is available.
- You need to perform compound structure searching or similarity matching; this skill only validates format and integrity, not chemical relationships.
- The database file size exceeds available memory or computational resources for full parsing.

## Inputs

- SDF-formatted compound database file

## Outputs

- Validation report documenting file integrity
- Verified record count
- Parseable structure verification results
- List of invalid or malformed records (if any)

## How to apply

Access and download the SDF file from its source repository. Parse the SDF file using RDKit to enumerate all molecular records and validate their chemical structure representations. Verify that each record parses without errors and represents a single DNA adduct (or target) compound. Generate a validation report that documents file integrity (absence of parse errors), total record count, and confirmation that all structures are chemically sound. Use record count and parse-error frequency as primary success metrics.

## Related tools

- **RDKit** (Parse SDF file, extract molecular records, validate chemical structure representation)

## Examples

```
from rdkit import Chem; suppl = Chem.SDMolSupplier('dna_adductomics_database.sdf'); print(f'Records: {len(suppl)}'); invalid = [i for i, mol in enumerate(suppl) if mol is None]; print(f'Invalid records: {invalid}')
```

## Evaluation signals

- SDF file parses without RDKit errors or warnings on all records
- Record count matches expected or declared number of DNA adduct compounds
- Each record contains a valid molecular structure object (non-null, with valid connectivity)
- No malformed or truncated records in the file
- Validation report is generated and documents all checks and counts

## Limitations

- RDKit validation confirms syntactic and basic chemical validity (e.g., valence, connectivity) but does not verify semantic correctness (whether the structure truly represents the intended biological adduct).
- SDF files may contain metadata or custom fields that RDKit does not parse; integrity verification focuses on molecular structure blocks only.
- Very large SDF files (>1 GB) may exceed available RAM during full parsing; streaming or chunked approaches may be necessary.

## Evidence

- [other] An SDF-formatted compound database file is available for download as part of the DNA adductomics database collection.: "An SDF-formatted compound database file is available for download as part of the DNA adductomics database collection."
- [other] Parse the SDF file using RDKit to verify structural validity and extract the number of molecular records.: "Parse the SDF file using RDKit to verify structural validity and extract the number of molecular records."
- [other] Confirm that each record represents a single DNA adduct compound and generate a validation report documenting file integrity, record count, and parseable structure verification.: "Confirm that each record represents a single DNA adduct compound and generate a validation report documenting file integrity, record count, and parseable structure verification."
- [intro] The DNA adduct database in Excel format, Word format, online, compound database in SDF format: "The DNA adduct database in Excel format, Word format, online, compound database in SDF format"
