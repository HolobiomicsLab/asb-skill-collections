---
name: descriptor-table-assembly
description: Use when when you have calculated molecular descriptors from validated chemical structures and need to prepare them for BitterPredict.m classification. Use this skill after descriptor calculation is complete and before invoking BitterPredict.m for bitter/non-bitter predictions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3750
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3372
  tools:
  - BitterPredict
  - BitterPredict.m
  - RDKit (implied from workflow)
derived_from:
- doi: 10.1021/acs.jafc.3c09767
  title: bittermass
evidence_spans:
- BitterPredict is a classifier which predicts whether a compound is bitter or not, based on its chemical structure.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_bittermass
    doi: 10.1021/acs.jafc.3c09767
    title: bittermass
  dedup_kept_from: coll_bittermass
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jafc.3c09767
  all_source_dois:
  - 10.1021/acs.jafc.3c09767
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# descriptor-table-assembly

## Summary

Assemble pre-computed molecular descriptors into a structured CSV or Excel table formatted for input to BitterPredict classification. This skill bridges descriptor calculation and taste prediction by organizing descriptor columns and molecule rows into the exact input format required by the BitterPredict.m classifier.

## When to use

When you have calculated molecular descriptors from validated chemical structures and need to prepare them for BitterPredict.m classification. Use this skill after descriptor calculation is complete and before invoking BitterPredict.m for bitter/non-bitter predictions.

## When NOT to use

- Input is already a CSV or Excel file in BitterPredict.m-compatible format — skip to classification.
- Descriptor values are missing or null for any molecule — resolve missing descriptors before assembly.
- Raw molecular structures (SMILES/SDF) are provided without pre-computed descriptors — descriptor calculation must occur first.

## Inputs

- Computed molecular descriptors in tabular form (rows = molecules, columns = descriptor values)
- Molecule identifiers or SMILES strings (for row labels)
- Descriptor names or identifiers (for column headers)

## Outputs

- CSV file with molecules as rows and descriptors as columns
- Excel (.xls or .xlsx) file with molecules as rows and descriptors as columns

## How to apply

Take the computed molecular descriptors (one descriptor per column, one molecule per row) and organize them into a structured table. Ensure each molecule has a unique identifier or SMILES representation as a row label, and each calculated descriptor occupies a dedicated column with a descriptive header. Export the complete table to either CSV or Excel (.xls/.xlsx) format compatible with BitterPredict.m input specification. Verify that all molecules have non-null descriptor values and that the column names match the descriptor set expected by BitterPredict.m (as documented in the BitterPredict.m file itself). The table structure is critical because BitterPredict.m reads descriptor columns directly; malformed or missing columns will cause classification failures.

## Related tools

- **BitterPredict.m** (Target classifier that accepts the assembled descriptor table as input for taste prediction; requires exact CSV/Excel format produced by this skill) — https://github.com/Niv-Lab/BitterPredict1
- **RDKit (implied from workflow)** (Cheminformatics parser used upstream to validate molecular structures and calculate descriptors prior to table assembly)

## Evaluation signals

- Table row count equals the number of unique molecules processed.
- Table column count matches the number of descriptors calculated per molecule; no columns are missing or duplicated.
- All descriptor cells contain numeric values; no null, NaN, or text entries are present in descriptor columns.
- CSV/Excel file parses successfully when opened in BitterPredict.m without schema or format errors.
- Column headers are descriptive (e.g. 'MolecularWeight', 'LogP') and do not contain special characters or spaces that conflict with BitterPredict.m parsing.

## Limitations

- The skill does not validate descriptor correctness or ranges — garbage descriptor values will produce uninformative predictions. Descriptor calculation quality is the responsibility of upstream steps.
- BitterPredict.m requires a specific set of molecular descriptors as documented in its source file; assembly does not auto-detect which descriptors are required. If the wrong descriptors are included or omitted, classification will fail or be unreliable.
- Export format compatibility (CSV vs. Excel) depends on BitterPredict.m's parser capabilities, which are documented only 'inside the BitterPredict.m file itself' — consult that file to confirm which format is preferred for your version.

## Evidence

- [other] Assemble descriptors into a structured table with molecules as rows and descriptor columns as required.: "Assemble descriptors into a structured table with molecules as rows and descriptor columns as required."
- [other] Export the descriptor table to CSV or Excel format compatible with BitterPredict.m input specification.: "Export the descriptor table to CSV or Excel format compatible with BitterPredict.m input specification."
- [readme] BitterPredict.m gets as input CSV or EXCEL files with required descriptors of molecules: "BitterPredict.m gets as input CSV or EXCEL files with required descriptors of molecules"
- [readme] Details and examples of how to use the code is avalibale inside bitterPredict.m file.: "Details and examples of how to use the code is avalibale inside bitterPredict.m file."
