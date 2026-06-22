---
name: cyp-isoform-substrate-prediction
description: Use when you have a set of molecular structures (in .sdf or .csv SMILES format) and need to predict which CYP isoforms will metabolize them.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0208
  - http://edamontology.org/topic_3375
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

# cyp-isoform-substrate-prediction

## Summary

Predict cytochrome P450 (CYP) isoform-specific metabolic reactivity for molecular structures using the CypReact command-line tool. This skill enables screening of drug candidates and xenobiotics against single or multiple CYP isoforms to assess metabolic stability and drug–drug interaction potential.

## When to use

Apply this skill when you have a set of molecular structures (in .sdf or .csv SMILES format) and need to predict which CYP isoforms will metabolize them. Use it during early drug discovery to assess metabolic liability, when evaluating potential drug–drug interactions involving CYP enzymes, or when screening xenobiotics for isoform-specific metabolism. It is particularly valuable when you need rapid, batch predictions across one or multiple CYP isoforms (e.g., 1A2, 2A6, 2B6) without running wet-lab assays.

## When NOT to use

- Your input molecules are already experimentally validated with measured Km or Vmax values—use this skill for prediction only, not validation.
- You require quantitative kinetic parameters (Km, Vmax) rather than binary or qualitative reactivity scores—CypReact provides predictive classification, not kinetic modeling.
- Your workflow demands real-time or single-molecule interactive queries rather than batch processing.

## Inputs

- Molecular structures in .sdf (Structure Data File) format
- Molecular structures in .csv format with SMILES strings separated by commas
- CYP isoform identifier(s) as string(s), e.g., '1A2', or comma-separated list '1A2,2A6,2B6'

## Outputs

- Reactivity predictions in .sdf format with isoform-specific scores or metadata
- Reactivity predictions in .csv format with per-molecule, per-isoform predictions

## How to apply

Prepare your input molecular structures in either .sdf format or .csv format with SMILES strings separated by commas. Obtain the CypReact .jar bundle from the documented repository or Google Drive link. Construct a Java command that specifies the bundle path, input molecule file, desired output file path, and one or more CYP isoform identifiers (comma-separated with no spaces for multiple isoforms). Execute the command in the terminal and verify that the output file is generated in the specified format (.sdf or .csv). The CypReact tool will compute reactivity predictions for each input molecule against the nominated isoform(s), allowing comparison of isoform selectivity and metabolic hotspot identification.

## Related tools

- **CypReact** (Command-line tool that executes isoform-specific CYP reactivity prediction on input molecular structures via Java invocation) — https://bitbucket.org/Leon_Ti/cypreact

## Examples

```
java -jar cypreact.jar /path/to/CypReactBundle/ /path/to/molecules.sdf /path/to/results.sdf 1A2,2A6,2B6
```

## Evaluation signals

- Output file is successfully generated at the specified path and is non-empty; .sdf file contains valid structure blocks and .csv file contains header and result rows.
- Output file structure matches the input format (if .sdf input, .sdf output; if .csv input, .csv output) and is readable by standard cheminformatics tools.
- Number of result records equals number of input molecules, indicating all structures were processed without silent failures.
- For multi-isoform predictions, each isoform appears in the output with distinct reactivity scores or predictions for each molecule.
- No error messages or non-zero exit codes reported; exit code = 0 and stderr is empty or contains only informational logs.

## Limitations

- CypReact is a predictive model; predictions must be validated experimentally for high-stakes applications such as regulatory submissions.
- Tool accepts only standardized CYP isoform codes (e.g., 1A2, 2A6, 2B6); non-standard or typo-containing isoform identifiers will result in execution errors or no-result outputs.
- Input molecules must be valid chemical structures (proper SMILES or .sdf format); malformed structures will fail silently or produce undefined predictions.
- Multi-isoform parameter format requires comma-separated isoform codes with no spaces; deviations cause parsing failure.

## Evidence

- [intro] Command-line invocation syntax: "java -jar cypreact.jar [bundle_path] [input.sdf] [output.sdf] 1A2"
- [intro] Input format specification: "The user can either input a .sdf file or a .csv. If the user input a .csv file, it should contains the SMILEs of all molecules and split them with ","."
- [intro] Multi-isoform parameter format: "if the user wants to test his/her molecules on CYP1A2,2A6 and 2B6, he/she can simply replace "1A2" with "1A2,2A6,2B6""
- [intro] Output format flexibility: "The user can output a .sdf file or a .csv file."
- [intro] Repository access: "Alternatively, you can down load the data at google drive with link: https://drive.google.com/drive/folders/1ywvqg6VvmqirU7BY1hMbiLWf4eeQ13zT?usp=sharing"
