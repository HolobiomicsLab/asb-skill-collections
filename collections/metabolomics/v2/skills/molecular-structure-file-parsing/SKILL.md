---
name: molecular-structure-file-parsing
description: Use when when you have received or downloaded an SDF-formatted compound
  database file and need to verify that it is valid, uncorrupted, and contains the
  expected number of distinct molecular records before using it in metabolomics, cheminformatics,
  or toxicology workflows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3372
  tools:
  - RDKit
  license_tier: restricted
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3389/fchem.2022.908572
  all_source_dois:
  - 10.3389/fchem.2022.908572
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-structure-file-parsing

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Parse and validate SDF-formatted molecular structure files to verify structural integrity, extract compound records, and confirm one-to-one mapping between file entries and unique chemical entities. This skill is essential for quality control of compound databases before downstream analysis.

## When to use

When you have received or downloaded an SDF-formatted compound database file and need to verify that it is valid, uncorrupted, and contains the expected number of distinct molecular records before using it in metabolomics, cheminformatics, or toxicology workflows.

## When NOT to use

- Input file is already in a non-SDF format (e.g., SMILES, CSV, Excel) — use format-specific parsers instead
- Goal is to analyze chemical properties or perform similarity searching — use this skill first for QC, then transition to cheminformatics-specific workflows
- SDF file is known to be valid and has already been successfully parsed in a prior analysis step

## Inputs

- SDF file (Structure Data Format compound database file)

## Outputs

- Validation report documenting file integrity, record count, and parseable structure verification
- Extracted molecular record count
- List of any malformed or invalid records (if applicable)

## How to apply

Use a chemistry toolkit (RDKit) to programmatically open and iterate through the SDF file, validating that each record parses successfully and represents a single, chemically valid molecule. Count the total number of records extracted and cross-reference this against expected counts from documentation or metadata. Generate a validation report that documents: (1) file integrity (whether all records parse without errors), (2) record count, and (3) any malformed or duplicate entries. Success is indicated by zero parse errors, a record count matching known inventory, and confirmation that each entry maps to a single DNA adduct compound.

## Related tools

- **RDKit** (Parse SDF file, validate molecular structure, extract and count records) — https://www.rdkit.org/

## Examples

```
from rdkit import Chem; suppl = Chem.SDMolSupplier('dna_adductomics.sdf'); print(f'Records: {len(suppl)}'); valid = sum(1 for mol in suppl if mol is not None); print(f'Valid: {valid}')
```

## Evaluation signals

- All SDF records parse successfully without errors or exceptions
- Reported record count matches the expected inventory from database documentation
- Each parsed record contains valid molecular structure (nonzero atom count, valid valence)
- No duplicate molecular entries detected (or duplicates are documented if they occur)
- Validation report is generated and contains file path, parse date, record count, and integrity status

## Limitations

- RDKit may silently skip or misparse records with non-standard or archaic SDF extensions; manual spot-checks of complex records are recommended
- Validation confirms structural chemical validity but does not verify that each record is scientifically appropriate or accurate for the intended application (e.g., that a DNA adduct annotation is correct)
- Large SDF files (>100k records) may require optimization (streaming parsing) to avoid memory exhaustion

## Evidence

- [other] Parse the SDF file using RDKit to verify structural validity and extract the number of molecular records.: "Parse the SDF file using RDKit to verify structural validity and extract the number of molecular records."
- [other] Confirm that each record represents a single DNA adduct compound and generate a validation report documenting file integrity, record count, and parseable structure verification.: "Confirm that each record represents a single DNA adduct compound and generate a validation report documenting file integrity, record count, and parseable structure verification."
- [other] An SDF-formatted compound database file is available for download as part of the DNA adductomics database collection.: "An SDF-formatted compound database file is available for download as part of the DNA adductomics database collection."
- [intro] The DNA adduct database in Excel format, Word format, online, compound database in SDF format: "The DNA adduct database in Excel format, Word format, online, compound database in SDF format"
