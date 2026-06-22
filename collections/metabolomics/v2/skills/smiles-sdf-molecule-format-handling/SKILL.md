---
name: smiles-sdf-molecule-format-handling
description: Use when when you have molecular structures in SMILES or SDF format that need to be passed to CyProduct for metabolite prediction, or when you need to switch between string-based and file-based molecular representations for compatibility with different CYP450 enzyme prediction workflows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3961
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0202
  tools:
  - BioTransformerAPI
  - CyProduct
  - Java
derived_from:
- doi: 10.1021/acs.jcim.1c00144
  title: CyProduct
evidence_spans:
- there is a class called BioTransformerAPI in the jar file
- Please download the CyProduct.jar to run the tool
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cyproduct_cq
    doi: 10.1021/acs.jcim.1c00144
    title: CyProduct
  dedup_kept_from: coll_cyproduct_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jcim.1c00144
  all_source_dois:
  - 10.1021/acs.jcim.1c00144
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# SMILES/SDF molecule format handling

## Summary

Prepare and validate molecular input data for CYP450 metabolite prediction by converting between SMILES strings and SDF file formats, and ensuring correct syntax conventions. This skill is essential for feeding query molecules into the BioTransformerAPI and command-line CyProduct tools.

## When to use

When you have molecular structures in SMILES or SDF format that need to be passed to CyProduct for metabolite prediction, or when you need to switch between string-based and file-based molecular representations for compatibility with different CYP450 enzyme prediction workflows.

## When NOT to use

- Input molecules are already in a non-standard format or lack stereochemical information required for accurate CYP450 prediction
- The SDF file path contains spaces or special characters that would break command-line argument parsing without proper escaping
- Enzyme names are provided with the 'CYP' prefix (e.g., 'CYP1A2'), which will cause parsing errors in the BioTransformerAPI

## Inputs

- SMILES string (formatted as SMILES=yourSmilesString)
- SDF file path (path to a .sdf file containing one or more molecular structures)
- CYP450 enzyme list (comma-separated without CYP prefix, e.g. 1A2,3A4,2C9)

## Outputs

- Predicted metabolite structures and properties (output to specified folder path)
- Metabolite prediction results (SDF or tabular format in OutputFolderPath)
- Scoring metadata (Score = (prob-threshold)/(1-threshold) per metabolite site of metabolism)

## How to apply

Identify your input molecule source (SMILES string or SDF file path). If using SMILES, wrap it in the format SMILES=yourSmilesString to ensure correct parsing by CyProduct. If using an SDF file, provide the direct file path without the SMILES= prefix. Validate that enzyme names are specified without the 'CYP' prefix (e.g., use '1A2' not 'CYP1A2'). Pass the formatted molecule and enzyme list to either the command-line tool or the BioTransformerAPI static functions. Verify that the output folder exists and is writable, then capture the predicted metabolite results in the specified OutputFolderPath.

## Related tools

- **CyProduct** (Command-line tool that accepts SMILES strings or SDF file paths and outputs predicted metabolites for specified CYP450 enzymes) — https://github.com/Le0nT1/CyProduct
- **BioTransformerAPI** (Java class within CyProduct.jar that provides static functions accepting molecules in SMILES/SDF format and CYP450 enzyme lists to programmatically predict metabolites) — https://github.com/Le0nT1/CyProduct
- **Java** (Runtime environment for executing CyProduct.jar and calling BioTransformerAPI static functions)

## Examples

```
java -jar CyProduct.jar "SMILES=CC(=O)Nc1ccc(O)cc1" 1A2,2A6,2B6,2C8,2C9,2C19,2D6,2E1,3A4 /path/to/output/
```

## Evaluation signals

- SMILES-formatted input parses without syntax errors and produces non-empty metabolite predictions
- SDF file path resolves correctly and all molecules in the file are processed without I/O errors
- Enzyme list is correctly parsed (no 'CYP' prefix present in input) and metabolites are predicted for all specified enzymes
- OutputFolderPath contains generated result files and results contain valid metabolite structures with associated scoring metadata
- Comparison of results between SMILES string input and equivalent SDF file input for the same molecule yields identical metabolite predictions

## Limitations

- SMILES strings must follow strict format convention (SMILES=yourSmilesString); omitting the prefix or using incorrect syntax will cause parsing failure
- SDF files are expected to contain valid molblock structures; malformed or corrupted SDF entries will be skipped or cause the tool to fail
- Enzyme names must omit the 'CYP' prefix; providing 'CYP1A2' instead of '1A2' will result in the enzyme not being recognized
- No version history or changelog is available, making it difficult to track compatibility across different CyProduct releases

## Evidence

- [readme] SMILES string format specification: "The QueryMolecule can be either a SMILES string or the path to a sdf file. Note that if the QueryMolecule is a SMILES string, it should use format:SMILES=yourSmilesString."
- [readme] SDF file path handling: "The QueryMolecule can be either a SMILES string or the path to a sdf file."
- [readme] Enzyme naming convention (no CYP prefix): "Please note that when you use the CyProduct tool or its API, please input enzyme without "CYP". For example, please use 1A2 other than CYP1A2 in both cases."
- [readme] Multiple enzyme support in SDF: "If the enzyme list contains more than one enzyme, CyProduct will predict the metabolites for all of them."
- [readme] Output destination specification: "The OutputFoldPath is the path to the folder where you want to store the predicted results."
- [readme] BioTransformerAPI molecule input flexibility: "It provides two static functions that take one molecule (or molecules), a list of cyp450 enzymes and a boolean variable useCypReact as input, and predict the corresponding metabolites."
