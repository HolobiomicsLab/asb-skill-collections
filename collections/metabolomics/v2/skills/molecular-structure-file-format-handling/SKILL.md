---
name: molecular-structure-file-format-handling
description: Use when when you have molecular structures in one format (e.g., SMILES
  strings in a spreadsheet or text file) but need to feed them to a tool that accepts
  a different format (e.g., CypReact requires .sdf or .csv with SMILES).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3961
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3314
  tools:
  - CypReact
  license_tier: restricted
  provenance_tier: literature
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

# molecular-structure-file-format-handling

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Convert and prepare molecular structures between standard file formats (.sdf, .csv with SMILES) for input to computational chemistry tools. This skill ensures compatibility between data sources and analysis pipelines that require specific structure representations.

## When to use

When you have molecular structures in one format (e.g., SMILES strings in a spreadsheet or text file) but need to feed them to a tool that accepts a different format (e.g., CypReact requires .sdf or .csv with SMILES). Apply this skill before invoking downstream analysis tools when format mismatch is detected.

## When NOT to use

- Your structures are already in the exact format required by the downstream tool (e.g., .sdf file ready for CypReact) — apply the tool directly instead.
- You are performing format conversion as a primary research goal rather than as a preparation step for subsequent analysis.
- The molecular structures are in specialized proprietary formats not mentioned in tool documentation.

## Inputs

- SMILES strings (comma-delimited)
- CSV file with SMILES column
- SDF (Structure Data Format) file
- Molecular structure list (plain text)

## Outputs

- SDF (Structure Data Format) file
- CSV file with SMILES and metadata
- Formatted molecular structure file compatible with target tool

## How to apply

First, identify the input format of your molecular structures (SMILES text, .sdf binary, CSV spreadsheet). If using .csv input, ensure SMILES strings are present and delimited by commas. If converting to .sdf, verify the structural data is complete and valid. Prepare the file in the target format expected by your downstream tool (for CypReact: either a single .sdf file or a .csv containing SMILES strings separated by commas). Validate the formatted file by checking that all molecular records are intact and parseable before passing to the analysis tool.

## Related tools

- **CypReact** (Downstream tool that consumes formatted molecular structures (.sdf or .csv with SMILES) for CYP reactivity prediction) — github:bitbucket.org__Leon_Ti__cypreact

## Evaluation signals

- Output file exists in the specified format (.sdf or .csv) and is readable by the downstream tool without parse errors.
- All molecular records present in the input are preserved in the output file with no loss or corruption of structural data.
- SMILES strings in CSV format are present and comma-delimited as specified; no malformed entries.
- When the formatted file is passed to CypReact, the tool accepts it without reporting file format errors or incompatibility.
- Spot-check: manually verify 3–5 molecular structures from input and output match in identity and connectivity.

## Limitations

- No changelog or versioning information available for format specifications; format details may change between tool versions.
- CSV input requires well-formed SMILES strings; invalid SMILES syntax will propagate to output and cause downstream tool failures.
- SDF file generation may fail or produce incomplete records if source molecular data lacks stereochemistry or formal charge information.
- Format conversion does not validate chemical or biological plausibility; only structural syntax is verified.

## Evidence

- [intro] Input format specification for CypReact: "The user can either input a .sdf file or a .csv. If the user input a .csv file, it should contains the SMILEs of all molecules and split them with ","."
- [intro] Output format capability: "The user can output a .sdf file or a .csv file."
- [intro] Example command-line invocation with file paths: "java -jar cypreact.jar C:\Users\Desktop\CypReactBundle\ C:\Users\Desktop\BioData\1A2_Test.sdf C:\Users\Desktop\BioData\1A2_Result.sdf 1A2"
