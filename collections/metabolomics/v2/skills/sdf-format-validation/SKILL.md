---
name: sdf-format-validation
description: Use when when you have downloaded an SDF-formatted compound database file (such as from the DNA adductomics database) and need to verify that the file is not corrupted, that each record represents a single valid chemical structure, and to obtain a record count before proceeding to structure-based.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3314
  - http://edamontology.org/topic_0154
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3389/fchem.2022.908572
  all_source_dois:
  - 10.3389/fchem.2022.908572
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# sdf-format-validation

## Summary

Validate the structural integrity and parseable format of an SDF (Structure Data Format) compound database file, confirming one entry per compound and extracting metadata for database quality assurance. This skill ensures that downloaded or deposited SDF files are suitable for downstream cheminformatics analysis.

## When to use

When you have downloaded an SDF-formatted compound database file (such as from the DNA adductomics database) and need to verify that the file is not corrupted, that each record represents a single valid chemical structure, and to obtain a record count before proceeding to structure-based queries or molecular property calculations.

## When NOT to use

- The SDF file has already been validated by the source repository and you are only performing structure similarity or property-based queries (validation is redundant).
- You are working with a different chemical structure format (e.g., MOL, SMILES, InChI) and do not need SDF-specific parsing.

## Inputs

- SDF file (Structure Data Format compound database)

## Outputs

- Validation report (count of total records, count of parseable vs. unparseable records, file integrity status)
- Parsed molecular objects (RDKit Mol objects for valid compounds)

## How to apply

Download the SDF file to local storage, then parse it using RDKit's SDF reader to iterate through all molecular records. For each record, verify that the structure data is chemically valid and that the molecule can be successfully deserialized. Count the total number of records and cross-reference against expected compound counts from database documentation. Generate a validation report documenting file integrity (parse success rate), total record count, and any records that failed to parse. Use RDKit's sanitization checks to catch invalid valence states or connectivity errors.

## Related tools

- **RDKit** (Parse SDF file to verify structural validity, extract molecular records, and perform sanitization checks on chemical structures)

## Examples

```
from rdkit import Chem; suppl = Chem.SDMolSupplier('dna_adductomics_database.sdf'); valid_count = sum(1 for mol in suppl if mol is not None); print(f'Total records: {len(suppl)}, Valid molecules: {valid_count}')
```

## Evaluation signals

- SDF file is successfully parsed without fatal I/O errors or format exceptions
- All molecular records can be deserialized into valid RDKit Mol objects with no valence or connectivity errors
- Extracted record count matches the expected number of DNA adduct compounds in the database (from documentation or metadata)
- Validation report shows 100% or near-100% parse success rate; any failed records are flagged with specific error reasons
- Each parsed record contains valid atom/bond topology and satisfies chemical valence rules

## Limitations

- RDKit sanitization may fail on non-standard or highly unusual chemical structures that are nevertheless valid; false negatives are possible.
- The SDF file format does not guarantee uniqueness of compounds across records; validation detects format integrity but not semantic duplication.
- Very large SDF files may consume significant memory during parsing; consider streaming or chunked parsing for databases with millions of records.

## Evidence

- [other] Access the nexs-metabolomics GitLab repository and locate the SDF format compound database file: "Access the nexs-metabolomics GitLab repository (gitlab.com/nexs-metabolomics/projects/dna_adductomics_database) and locate the SDF format compound database file."
- [other] Parse using RDKit to verify structural validity: "Parse the SDF file using RDKit to verify structural validity and extract the number of molecular records."
- [other] Generate validation report documenting file integrity and record count: "generate a validation report documenting file integrity, record count, and parseable structure verification."
- [intro] DNA adductomics database available in multiple formats including SDF: "The following files are available: [Excel format, Word format, online, SDF format, experimental fragments online, predicted fragments online, collection of Excel file, online databases, CFM-ID]"
- [other] Each record represents a single DNA adduct compound: "Confirm that each record represents a single DNA adduct compound and generate a validation report"
