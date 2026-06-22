---
name: cypreact-input-format-compliance
description: Use when you have a collection of molecular structures intended for CypReact-based CYP isoform metabolism prediction and need to verify the input file conforms to CypReact's expected format (comma-separated SMILES in .csv or SDF molecular structure files) before submission to the tool.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_3172
  tools:
  - CypReact
  - RDKit
  - pandas
derived_from:
- doi: 10.1021/acs.jcim.8b00035
  title: CypReact
evidence_spans:
- 'To run the CypReact tool, the user should use command in the terminal as: ->java -jar "PathOfCypReactBundle"'
- java -jar "PathOfCypReactBundle"
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cypreact_cq
    doi: 10.1021/acs.jcim.8b00035
    title: CypReact
  dedup_kept_from: coll_cypreact_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jcim.8b00035
  all_source_dois:
  - 10.1021/acs.jcim.8b00035
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# cypreact-input-format-compliance

## Summary

Validate and parse molecular structure input files (.csv or .sdf) to meet CypReact's format specifications before cytochrome P450 metabolism prediction. This skill ensures SMILES strings are syntactically correct, properly delimited, and deduplicated to avoid processing failures.

## When to use

You have a collection of molecular structures intended for CypReact-based CYP isoform metabolism prediction and need to verify the input file conforms to CypReact's expected format (comma-separated SMILES in .csv or SDF molecular structure files) before submission to the tool.

## When NOT to use

- Input molecules are already in a vendor-specific binary format not convertible to SMILES or SDF without loss of stereochemistry or 3D information.
- The analysis goal does not require CYP isoform-specific metabolism prediction; alternative ADME tools may be more appropriate.
- Input SMILES or SDF records contain non-standard valence or undefined atom types that RDKit cannot canonicalize or sanitize.

## Inputs

- CSV file with comma-separated SMILES strings
- SDF file containing molecular structures
- Raw molecular structure list (unvalidated)

## Outputs

- Validated CSV file with deduplicated SMILES and metadata
- Validated SDF file with confirmed molecular records
- Structured data object (DataFrame or JSON) compatible with CypReact input specifications

## How to apply

Load the input .csv or .sdf file using a molecular parser (e.g., pandas for CSV, RDKit for molecular validation). If CSV format is used, verify that SMILES strings are comma-separated; if SDF format, confirm molecular records are properly structured. Validate each SMILES string for syntactic correctness using RDKit or equivalent validator. Extract and deduplicate the molecule list to remove redundant structures. Format the parsed molecules as a structured object (DataFrame or JSON) that matches CypReact's input schema. Write the validated output to a new CSV or SDF file with metadata fields intact and pass this to CypReact via the command-line invocation specifying the input file path and desired CYP isoforms.

## Related tools

- **CypReact** (Executes cytochrome P450 metabolism prediction on validated molecular input files; outputs metabolism sites and products for specified isoforms) — github:bitbucket.org__Leon_Ti__cypreact
- **RDKit** (Validates SMILES string syntax and sanitizes molecular structures during parsing and deduplication)
- **pandas** (Loads and structures CSV files containing comma-separated SMILES strings into memory-efficient DataFrame objects)

## Examples

```
java -jar cypreact.jar /path/to/CypReactBundle /path/to/validated_molecules.csv /path/to/output_result.csv 1A2,2A6,2B6
```

## Evaluation signals

- All SMILES strings in the validated output pass RDKit sanitization without errors or warnings.
- Deduplicated molecule count is equal to or less than the input count; no valid structures are lost.
- CSV output file has consistent column structure (e.g., SMILES, ID, metadata fields) with no null or malformed rows.
- CypReact command executes without file format errors when passed the validated output file and a valid CYP isoform identifier (e.g., '1A2', '2A6', '2B6').
- Output .sdf or .csv from CypReact contains predictions for all input molecules with no missing entries corresponding to valid input records.

## Limitations

- CypReact accepts only .csv (comma-separated SMILES) or .sdf molecular file formats; other formats (MOL2, PDB, MOL) must be converted first.
- SMILES strings with undefined stereochemistry or non-standard notation may pass syntactic validation but produce unexpected metabolism predictions.
- Large-scale deduplication (>100k molecules) may require memory-efficient streaming approaches not detailed in the CypReact documentation.
- No changelog is available; parsing behavior or format requirements may change between CypReact versions without explicit notice.

## Evidence

- [intro] CSV format requirement: "If the user input a .csv file, it should contains the SMILEs of all molecules and split them with ","."
- [other] Multi-step workflow for input preparation: "Load the CSV file containing SMILES strings separated by commas using a CSV parser (e.g., pandas). 2. Validate each SMILES string for syntactic correctness using RDKit or equivalent molecular"
- [intro] SDF file support: "The user can either input a .sdf file or a .csv."
- [intro] Output format flexibility: "The user can output a .sdf file or a .csv file."
- [intro] CypReact command invocation: "java -jar cypreact.jar C:\Users\Desktop\CypReactBundle\ C:\Users\Desktop\BioData\1A2_Test.sdf C:\Users\Desktop\BioData\1A2_Result.sdf 1A2"
