---
name: csv-format-validation
description: Use when when you have a .csv file intended as input to CypReact containing SMILES strings and need to verify it meets the required comma-separated format specification and that each SMILES string is syntactically valid before processing molecules through CYP isoform testing.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3314
  - http://edamontology.org/topic_0154
  tools:
  - CypReact
  - RDKit
  - pandas
derived_from:
- doi: 10.1021/acs.jcim.8b00035
  title: CypReact
evidence_spans: []
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

# CSV format validation

## Summary

Validates that comma-separated SMILES input files (.csv) conform to CypReact's required format and contain syntactically correct molecular structure representations. This skill ensures molecules can be successfully ingested before running CYP isoform reactivity predictions.

## When to use

When you have a .csv file intended as input to CypReact containing SMILES strings and need to verify it meets the required comma-separated format specification and that each SMILES string is syntactically valid before processing molecules through CYP isoform testing.

## When NOT to use

- Input is already a .sdf file (use direct .sdf input to CypReact instead)
- SMILES strings are already validated and formatted in a structured database or data object
- Molecules are in a different format not requiring CSV parsing (e.g., InChI, molecular name lists)

## Inputs

- .csv file containing SMILES strings separated by commas
- raw SMILES string sequences

## Outputs

- validated .csv file with deduplicated, syntactically correct SMILES
- validated .json file with structured molecule records and metadata
- validation report documenting SMILES correctness and format compliance

## How to apply

Load the .csv file using a CSV parser (e.g., pandas) and extract all SMILES strings. Validate each SMILES string for syntactic correctness using RDKit or an equivalent molecular structure validator to confirm it represents a valid chemical structure. Check that molecules are comma-separated as required by CypReact's specification. Deduplicate the molecule list to remove redundant entries. Format the validated molecule list as a structured data object (DataFrame or JSON) compatible with CypReact input specifications. Write the parsed and validated molecule list to an output file (CSV or JSON) with validated SMILES and metadata fields.

## Related tools

- **CypReact** (Target tool that ingests and processes the validated CSV-formatted SMILES input for CYP isoform reactivity prediction) — github:bitbucket.org__Leon_Ti__cypreact
- **RDKit** (Molecular structure validator used to verify syntactic correctness of each SMILES string)
- **pandas** (CSV parser and data structure tool for loading, deduplicating, and formatting molecule lists)

## Examples

```
import pandas as pd
from rdkit import Chem

df = pd.read_csv('molecules.csv')
valid_smiles = [s for s in df['SMILES'] if Chem.MolFromSmiles(s) is not None]
valid_df = pd.DataFrame({'SMILES': list(set(valid_smiles))})
valid_df.to_csv('validated_molecules.csv', index=False)
```

## Evaluation signals

- All SMILES strings parse successfully without RDKit errors or syntax exceptions
- Output .csv/.json contains deduplicated molecule list with no empty or malformed SMILES entries
- File structure matches CypReact input specification (comma-separated format with valid metadata fields)
- Validated output can be successfully loaded by CypReact without pre-processing errors
- Comparison of input vs. output record counts shows deduplication was applied and all remaining SMILES are valid

## Limitations

- Validation only confirms syntactic SMILES correctness; does not verify chemical feasibility or drug-likeness
- Large CSV files may require chunked or streaming parsing to avoid memory exhaustion
- Deduplication is exact-match only; stereoisomers or different canonical forms are not detected as duplicates
- No changelog documented for CypReact format version changes; format specification may drift between releases

## Evidence

- [intro] csv_format_requirement: "If the user input a .csv file, it should contains the SMILEs of all molecules and split them with ","."
- [other] validation_and_parsing_workflow: "Validate each SMILES string for syntactic correctness using RDKit or equivalent molecular structure validator. Extract and deduplicate the molecule list. Format the parsed molecule list as a"
- [intro] output_format_specification: "The user can output a .sdf file or a .csv file."
- [intro] csv_input_alternative: "The user can either input a .sdf file or a .csv. If the user input a .csv file, it should contains the SMILEs of all molecules and split them with ","."
