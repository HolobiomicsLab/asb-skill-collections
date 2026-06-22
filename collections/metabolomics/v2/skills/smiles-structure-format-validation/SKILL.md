---
name: smiles-structure-format-validation
description: Use when when you have raw molecular structures in SMILES or .sdf format and need to feed them into CypReact for CYP isoform prediction. Apply this skill before invoking the CypReact command-line tool to avoid runtime failures due to malformed input.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3961
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3474
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jcim.8b00035
  all_source_dois:
  - 10.1021/acs.jcim.8b00035
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# smiles-structure-format-validation

## Summary

Validate and prepare molecular structure input files (SMILES strings or .sdf files) before submission to CypReact for cytochrome P450 metabolite prediction. This skill ensures input data conforms to expected format and encoding requirements.

## When to use

When you have raw molecular structures in SMILES or .sdf format and need to feed them into CypReact for CYP isoform prediction. Apply this skill before invoking the CypReact command-line tool to avoid runtime failures due to malformed input.

## When NOT to use

- Input is already a .sdf or .csv file that has been validated by upstream quality-control processes
- You are only interested in predicted metabolites and do not control the input source — delegate validation to the data provider
- Input contains protein structures or macromolecules; CypReact is designed for small molecule substrates

## Inputs

- SMILES strings (comma-separated in .csv format)
- .sdf file (chemical structure format)
- .csv file (containing SMILES column)

## Outputs

- Validated molecular structure file ready for CypReact input
- SMILES validation report (if applied)

## How to apply

Verify that input molecular structures are provided as either a .sdf file or a .csv file containing SMILES strings. If using .csv format, ensure SMILES strings are comma-delimited within the file. Load the file and validate SMILES syntax (no unexpected characters or encoding errors). Confirm the file path is accessible and readable before passing it to the CypReact invocation. This validation step prevents downstream errors during CYP isoform prediction and ensures consistent output formatting.

## Related tools

- **CypReact** (Tool that consumes validated SMILES/structure input to predict CYP metabolic transformations across multiple isoforms) — github:bitbucket.org__Leon_Ti__cypreact

## Examples

```
# Validate and prepare SMILES input before CypReact invocation
java -jar cypreact.jar C:\Users\Desktop\BioData\molecules.csv C:\Users\Desktop\BioData\1A2_Result.sdf 1A2
```

## Evaluation signals

- SMILES strings parse without error and produce valid chemical graphs
- .sdf or .csv file opens without I/O errors and contains expected column headers or structure records
- CypReact successfully reads the file and completes prediction without format-related exceptions
- Row count and molecule IDs in input file match those in output prediction file (no molecules silently dropped)
- Output file (.sdf or .csv) contains per-molecule predictions in the same order as input

## Limitations

- No built-in changelog or versioning system documented for format compatibility across CypReact releases
- Validation scope is limited to file format and basic syntax; semantic validation (chemical feasibility, tautomerization, stereochemistry) is not addressed
- Large .csv files with thousands of SMILES strings may require streaming or chunked validation to avoid memory overload

## Evidence

- [intro] Input format requirement (SMILES or .sdf): "The user can either input a .sdf file or a .csv. If the user input a .csv file, it should contains the SMILEs of all molecules and split them with ","."
- [intro] CypReact command-line invocation grammar: "java -jar cypreact.jar C:\Users\Desktop\CypReactBundle\ C:\Users\Desktop\BioData\1A2_Test.sdf C:\Users\Desktop\BioData\1A2_Result.sdf 1A2"
- [intro] Output format options: "The user can output a .sdf file or a .csv file."
