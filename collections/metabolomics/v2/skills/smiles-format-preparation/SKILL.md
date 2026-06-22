---
name: smiles-format-preparation
description: Use when you have molecular structures in raw or unstructured form and need to submit them to CypReact or similar command-line chemistry tools that accept CSV input.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3406
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3314
  tools:
  - CypReact
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
---

# SMILES Format Preparation

## Summary

Prepare molecular structure data in SMILES format as input for computational chemistry workflows, specifically for tools like CypReact that require standardized comma-separated SMILES strings in CSV files. This skill ensures molecular data is correctly formatted to enable downstream reactivity prediction and CYP isoform screening.

## When to use

Use this skill when you have molecular structures in raw or unstructured form and need to submit them to CypReact or similar command-line chemistry tools that accept CSV input. Specifically, apply this skill when your input molecules are not yet organized as comma-delimited SMILES strings, or when converting from alternative formats (.sdf, SMILES lists, structure drawings) to the CSV+SMILES input format required by CypReact.

## When NOT to use

- Input is already provided as a properly formatted CSV file with comma-separated SMILES strings and has been validated.
- You are using an .sdf file directly as input, since CypReact accepts both .sdf and .csv inputs interchangeably; prioritize .sdf if already available to avoid unnecessary format conversion.

## Inputs

- Molecular structures (as .sdf file, structure drawings, or SMILES strings)
- List or set of SMILES strings (unformatted)
- CSV or text file containing SMILES identifiers

## Outputs

- CSV file with comma-separated SMILES strings
- Formatted SMILES input file suitable for CypReact

## How to apply

Obtain or generate SMILES strings for each molecule in your dataset. Organize these SMILES strings into a comma-separated format within a CSV file, with one SMILES string per line (or as specified by your tool's documentation). Verify that each SMILES string is valid and represents the intended molecular structure by spot-checking against the original structure or using a cheminformatics validation tool. Ensure the CSV file is properly formatted with consistent delimiters and no extraneous whitespace that could cause parsing errors during tool execution. The prepared CSV file then serves as the input_molecules parameter for the CypReact command-line invocation.

## Related tools

- **CypReact** (Command-line tool that accepts formatted SMILES-containing CSV files to predict CYP reactivity; this skill prepares input files for CypReact execution.) — github:bitbucket.org__Leon_Ti__cypreact

## Examples

```
# Prepare a CSV file with SMILES strings for CypReact input:
echo 'CC(C)Cc1ccc(cc1)C(C)C(O)=O,c1ccccc1' > molecules.csv && java -jar cypreact.jar /path/to/CypReactBundle molecules.csv output_results.sdf 1A2
```

## Evaluation signals

- The generated CSV file is readable by text editors and contains one or more SMILES strings separated by commas.
- Each SMILES string parses without syntax errors in a cheminformatics library (e.g., RDKit can convert SMILES → molecular graph).
- The CSV file can be successfully passed as the input_molecules parameter to a CypReact command without format-related errors.
- Spot-check: 2–3 SMILES strings correspond to the original chemical structures they represent.
- No extraneous whitespace, trailing delimiters, or encoding issues corrupt the SMILES strings when the file is read by CypReact.

## Limitations

- SMILES format is linear and text-based; stereochemistry and 3D conformations may be ambiguous or lost if not explicitly encoded in the SMILES string.
- No changelog or versioning information available; CypReact tool updates or changes to SMILES parsing rules are not documented, so format compatibility may shift without notice.
- Comma-separated SMILES formatting is specific to CypReact's documented input requirements; other tools may require tab-separated, space-separated, or newline-separated formats.

## Evidence

- [intro] SMILES format specification for CSV input: "If the user input a .csv file, it should contains the SMILEs of all molecules and split them with ","."
- [intro] CypReact accepts both .sdf and .csv file inputs: "The user can either input a .sdf file or a .csv."
- [intro] CSV file is used as primary input for CypReact command: "java -jar cypreact.jar C:\Users\Desktop\CypReactBundle\ C:\Users\Desktop\BioData\1A2_Test.sdf C:\Users\Desktop\BioData\1A2_Result.sdf 1A2"
