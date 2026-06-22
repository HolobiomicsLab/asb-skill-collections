---
name: metabolite-database-file-formatting
description: Use when after generating or filtering transformation products using generateTPs() or filter(), when you need to annotate MS/MS spectra using MetFrag and require a database of candidate structures (parent compounds and/or their TPs) in a format MetFrag can read.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3172
  tools:
  - patRoon
  - MetFrag
  - generateTPs (patRoon algorithm)
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1186/s13321-020-00477-w
  title: patRoon
evidence_spans:
- The `generateTPs` function is used to obtain TPs for a particular set of parents.
- componTP <- generateComponents(algorithm = "tp",
- convertToMFDB | Generates a [MetFrag] database for all TPs (and optionally parents, only for TPs with structural information)
- Generates a [MetFrag] database for all TPs
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_patroon_cq
    doi: 10.1186/s13321-020-00477-w
    title: patRoon
  dedup_kept_from: coll_patroon_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-020-00477-w
  all_source_dois:
  - 10.1186/s13321-020-00477-w
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-database-file-formatting

## Summary

Convert transformation product (TP) objects with structural information (SMILES) into MetFrag-compatible CSV database files for MS/MS compound annotation. This skill bridges patRoon's internal TP representation and external spectral matching tools by standardizing compound identifiers and chemical structures.

## When to use

After generating or filtering transformation products using generateTPs() or filter(), when you need to annotate MS/MS spectra using MetFrag and require a database of candidate structures (parent compounds and/or their TPs) in a format MetFrag can read. Typical trigger: you have a TPs object with SMILES structures and want to perform automated compound annotation on experimental features.

## When NOT to use

- TPs object lacks structural information (SMILES) — convertToMFDB requires valid SMILES for all records intended for export.
- You need to annotate spectra using a tool other than MetFrag (e.g., SIRIUS) — use tool-specific export functions instead.
- Input data are already in a different standardized database format (e.g., MassBank, PubChem SDF) — direct conversion or reformatting may be more appropriate than re-exporting TPs.

## Inputs

- TPs object (from generateTPs or filter, containing transformation products with SMILES)
- output file path (string specifying local CSV destination)

## Outputs

- MetFrag-compatible CSV database file (two columns: compound name, SMILES)
- File written to disk, ready for use in MetFrag compound annotation

## How to apply

Load a TPs object containing transformation products and optionally parent compounds, all with valid SMILES strings. Extract parent and TP metadata (compound names and SMILES) using the TPs object accessors (parents() and products()). Call convertToMFDB() with the TPs object and set includeParents=TRUE if parent structures are available; note that parents are only included when structural information exists for the TPs themselves. Format the combined data into a two-column CSV table (compound name and SMILES) matching MetFrag database schema. Write to a local CSV file at the specified output path. Verify the file by checking CSV readability, confirming column headers match MetFrag expectations, and spot-checking SMILES validity for a sample of records.

## Related tools

- **patRoon** (Provides convertToMFDB() function and TPs object model for extraction of parents and products with SMILES) — https://github.com/rickhelmus/patRoon
- **MetFrag** (Target spectral matching and compound annotation tool; requires CSV input in two-column (name, SMILES) format)
- **generateTPs (patRoon algorithm)** (Upstream function to generate TP objects with structural information from BioTransformer, CTS, or library sources) — https://github.com/rickhelmus/patRoon

## Examples

```
convertToMFDB(TPs = TPsFiltered, output = "mfdb_export.csv", includeParents = TRUE)
```

## Evaluation signals

- Output CSV file exists and is readable; check file size and row count are non-zero.
- CSV header row contains exactly two columns ('compound name' and 'SMILES' or equivalent); verify with head() or similar inspection.
- All SMILES strings are valid organic chemistry notation (no truncation, malformed brackets, or illegal characters); spot-check 5–10 random rows.
- When includeParents=TRUE, CSV contains both parent and TP records; row count should equal parents + TPs in the input object.
- File can be successfully loaded into MetFrag without parse errors; confirm via MetFrag's import log or dry-run test.

## Limitations

- Parents are only included in the output CSV when structural information (SMILES) is available for the TPs; if TPs lack SMILES, parent records will not be exported even with includeParents=TRUE.
- The function does not perform SMILES validation or canonicalization; invalid or non-canonical SMILES from the TPs object will be written as-is and may cause downstream MetFrag errors.
- CSV format assumes MetFrag expects exactly two columns; compatibility with other spectral matching tools or database formats is not guaranteed.
- Large TP datasets may produce very large CSV files; no built-in compression or chunking is described.

## Evidence

- [other] convertToMFDB generates a MetFrag-compatible database file for all transformation products (TPs) and optionally includes parent compounds, with the constraint that parents are only included when structural information is available for the TPs.: "convertToMFDB generates a MetFrag-compatible database file for all TPs (and optionally parents, only for TPs with structural information)"
- [other] Workflow requires extracting parent and TP names and SMILES, formatting into a CSV table, and writing to a local file.: "Extract parent names, SMILES, and TP names and SMILES from the TPs object using the products() and parents() accessors. ... Format the combined parent/TP data into a CSV table with columns for"
- [other] Verification involves checking CSV readability and SMILES validity.: "Verify the CSV is readable by MetFrag by checking column presence and SMILES validity."
- [other] The function is part of the TP screening workflow for transformation product annotation.: "Screening for TPs, i.e. chemicals that are formed from a _parent_ chemical by e.g. chemical or biological processes, has broad applications. For this reason, the TP screening related functionality is"
