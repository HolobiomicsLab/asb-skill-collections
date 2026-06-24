---
name: molecular-structure-validation
description: Use when ingesting SMILES strings from CSV or other bulk molecular input
  files before passing them to structure-based prediction tools.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3346
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3373
  tools:
  - RDKit
  - pandas
  - CypReact
  license_tier: restricted
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

# molecular-structure-validation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Validates syntactic correctness and structural integrity of SMILES strings prior to computational chemistry analysis. This skill ensures only well-formed molecular representations enter downstream processing pipelines like CypReact, preventing parsing errors and invalid predictions.

## When to use

Apply this skill when ingesting SMILES strings from CSV or other bulk molecular input files before passing them to structure-based prediction tools. Validation is required whenever molecule data originates from external sources or user-supplied input, or when deduplication and data quality assessment are prerequisites for CYP isoform metabolite prediction workflows.

## When NOT to use

- SMILES strings are already validated and sourced from a trusted, curated molecular database with documented quality control.
- Input is pre-formatted as an SDF file with embedded 3D coordinates; use SDF parsing and validation instead.
- Molecules are represented in formats other than SMILES (e.g., InChI, molecular name) without prior conversion to SMILES.

## Inputs

- CSV file containing SMILES strings separated by commas
- Individual SMILES string (string)

## Outputs

- Validated and deduplicated molecule list (CSV file)
- Validated and deduplicated molecule list (JSON structured object)
- Validation report with pass/fail status per molecule

## How to apply

Load the CSV file containing comma-separated SMILES strings using a CSV parser such as pandas. For each SMILES string, invoke a molecular structure validator (RDKit or equivalent) to verify syntactic correctness and confirm the string can be converted to a valid molecular object. Flag or reject SMILES that fail to parse or produce invalid molecular graphs. Extract and deduplicate the resulting molecule list to remove redundant entries. Format the validated, deduplicated molecule list as a structured data object (DataFrame or JSON) with validated SMILES strings and metadata fields (e.g., original row index, validation status). Write the output to a CSV or JSON file compatible with downstream tools like CypReact.

## Related tools

- **RDKit** (Validates SMILES string syntactic correctness and converts strings to molecular structure objects for structural validation)
- **pandas** (Loads and parses CSV files containing comma-separated SMILES strings; organizes validated output into DataFrames)
- **CypReact** (Accepts validated and formatted SMILES input as CSV or SDF files for CYP isoform metabolite prediction) — github:bitbucket.org__Leon_Ti__cypreact

## Examples

```
import pandas as pd; from rdkit import Chem; df = pd.read_csv('molecules.csv'); df['valid_smiles'] = [Chem.MolToSmiles(Chem.MolFromSmiles(s)) if Chem.MolFromSmiles(s) else None for s in df['smiles']]; df_valid = df.dropna(subset=['valid_smiles']).drop_duplicates(subset=['valid_smiles']); df_valid.to_csv('validated_molecules.csv', index=False)
```

## Evaluation signals

- All SMILES strings in the output parse successfully without exceptions when re-ingested by RDKit or equivalent validator.
- Each validated SMILES produces a valid molecular object with atomic and bond information intact; no null or undefined molecular graphs.
- Deduplicated molecule count is ≤ input count; duplicate SMILES are removed exactly once with no false negatives.
- Output CSV/JSON schema matches the expected format (columns: original_smiles, validated_smiles, validation_status, deduplication_flag).
- All molecules in the validated output file are compatible with CypReact input specifications (parseable by CypReact without file format errors).

## Limitations

- Validation does not verify chemical plausibility or biological relevance; syntactically correct SMILES may represent unstable or non-existent compounds.
- SMILES canonicalization differences may cause false duplicate detection if isomeric variants are represented with different SMILES strings.
- RDKit and equivalent validators may have edge-case differences in SMILES parsing; behavior is tool-dependent.
- Validation does not assess the appropriateness of molecules for CYP metabolism prediction (e.g., molecular weight, logP thresholds specific to CypReact are not enforced).

## Evidence

- [other] Validate each SMILES string for syntactic correctness using RDKit or equivalent molecular structure validator.: "Validate each SMILES string for syntactic correctness using RDKit or equivalent molecular structure validator."
- [intro] CSV file format and parsing requirements for CypReact input: "If the user input a .csv file, it should contains the SMILEs of all molecules and split them with ","."
- [other] Deduplication and structured output formatting: "Extract and deduplicate the molecule list. 4. Format the parsed molecule list as a structured data object (DataFrame or JSON) compatible with CypReact input specifications."
- [intro] Output file requirements: "The user can output a .sdf file or a .csv file."
