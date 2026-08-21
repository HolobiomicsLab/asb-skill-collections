---
name: smiles-string-preparation
description: Use when you have a target molecule (e.g., acetaminophen, a drug candidate,
  or a xenobiotic) whose structure you need to encode for metabolite prediction, reaction
  rule matching, or other structure-based cheminformatics workflow.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0360
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_2258
  tools:
  - CyProduct
  - Java
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jcim.1c00144
  title: CyProduct
evidence_spans:
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# SMILES String Preparation for Molecular Input

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Format a molecule's SMILES representation as a queryable input string for computational chemistry tools that predict metabolites or other molecular properties. This skill ensures the SMILES notation is syntactically correct and wrapped in the tool-specific format required by command-line or API invocation.

## When to use

You have a target molecule (e.g., acetaminophen, a drug candidate, or a xenobiotic) whose structure you need to encode for metabolite prediction, reaction rule matching, or other structure-based cheminformatics workflow. The downstream tool accepts SMILES input and requires explicit format specification to distinguish a SMILES string from a file path.

## When NOT to use

- Input is already a file path to an SDF or structure file — use the file path directly without SMILES= prefix instead.
- The tool accepts either SMILES or SDF indifferently without explicit format tagging — check tool documentation to avoid redundant formatting.

## Inputs

- Molecular structure (as InChI, common name, or SMILES notation)
- Canonical or semi-canonical SMILES string

## Outputs

- Formatted SMILES query string (e.g., SMILES=CC(=O)Nc1ccc(O)cc1)
- Validated SMILES input ready for metabolite prediction or structure-based cheminformatics workflow

## How to apply

Obtain or derive the canonical or semi-canonical SMILES string for your molecule (e.g., CC(=O)Nc1ccc(O)cc1 for acetaminophen). If the tool requires explicit labeling (as CyProduct does), prepend the SMILES with the format prefix SMILES= to disambiguate it from a file path input. Validate that the SMILES string is chemically valid by checking it parses without syntax errors and represents the intended molecular structure. Pass the formatted string (e.g., SMILES=CC(=O)Nc1ccc(O)cc1) as the QueryMolecule parameter to the command-line tool or API.

## Related tools

- **CyProduct** (Accepts SMILES string as QueryMolecule parameter for metabolite prediction across specified CYP450 enzymes) — https://github.com/Le0nT1/CyProduct
- **Java** (Runtime environment for executing CyProduct.jar with SMILES input and command-line parameters)

## Examples

```
java -jar CyProduct.jar SMILES=CC(=O)Nc1ccc(O)cc1 1A2,2A6,2B6,2C8,2C9,2C19,2D6,2E1,3A4 /path/to/output
```

## Evaluation signals

- SMILES string parses without syntax errors in a cheminformatics toolkit (RDKit, CDK, etc.)
- Formatted input (e.g., SMILES=...) is accepted by the tool without malformed-input errors
- Tool successfully generates output (predicted metabolites, reaction matches) without rejecting the input as invalid
- SMILES notation correctly represents the intended molecular structure (manual visual inspection or comparison against a reference SDF)
- Output metabolites or results are consistent with expectations for the query molecule and enzyme/reaction set used

## Limitations

- SMILES strings are not unique — different SMILES can represent the same molecule; canonical or semi-canonical forms are recommended but tool behavior may vary.
- The SMILES= prefix format is tool-specific to CyProduct; other tools may require different input syntax or no prefix at all.
- Complex or unusual molecules (e.g., salts, charged species, stereoisomers with mixed or undefined stereochemistry) may not parse correctly or may generate ambiguous results.
- No validation that the SMILES represents a chemically realistic or drug-like molecule — syntactic validity does not imply biological relevance.

## Evidence

- [readme] QueryMolecule input format specification: "The QueryMolecule can be either a SMILES string or the path to a sdf file. Note that if the QueryMolecule is a SMILES string, it should use format:SMILES=yourSmilesString."
- [other] Concrete SMILES example for acetaminophen: "1. Prepare the acetaminophen SMILES string (CC(=O)Nc1ccc(O)cc1) as the query molecule input."
- [readme] Command-line invocation with SMILES input: "java -jar CyProduct.jar CC(=O)Nc1ccc(O)cc1 1A2,2A6,2B6,2C8,2C9,2C19,2D6,2E1,3A4 E:\Users\cyproduct\"
- [readme] Enzyme format specification: "Please note that when you use the CyProduct tool or its API, please input enzyme without "CYP". For example, please use 1A2 other than CYP1A2 in both cases."
