---
name: smiles-sdf-parsing-validation
description: Use when you have raw molecular structures in SMILES or SDF format that
  will feed into BitterPredict.m or other structure-based classifiers.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2409
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3372
  tools:
  - BitterPredict
  - RDKit
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.jafc.3c09767
  title: bittermass
evidence_spans:
- BitterPredict is a classifier which predicts whether a compound is bitter or not,
  based on its chemical structure.
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

# SMILES/SDF parsing and validation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Parse and validate molecular structure syntax from raw SMILES or SDF format files using a cheminformatics parser (e.g., RDKit) to ensure structural integrity before descriptor calculation. This skill is essential to detect malformed or invalid molecular representations that would fail downstream descriptor computation or classification.

## When to use

Apply this skill when you have raw molecular structures in SMILES or SDF format that will feed into BitterPredict.m or other structure-based classifiers. Use it as the first step in any molecular descriptor pipeline to catch parsing errors, ambiguous stereochemistry, or chemically invalid structures before investing computational resources in descriptor calculation.

## When NOT to use

- Structures are already pre-computed as a numerical descriptor table (CSV/Excel) — validation is needed only on raw structural input.
- Working with already-validated structure sets from a trusted, quality-controlled database where syntax checking has been certified.
- Input is non-molecular data (e.g., spectroscopy or phenotype data) where structure parsing is inapplicable.

## Inputs

- SMILES format files (text-based molecular notation)
- SDF format files (structure data format with 3D coordinates)

## Outputs

- Parsed and validated molecular structure objects
- List of molecules passing syntax and chemical validity checks
- Log or report of rejected structures and failure reasons

## How to apply

Load raw molecular structures from SMILES or SDF files using a cheminformatics parser such as RDKit. Validate the syntax and chemical validity of each parsed structure, recording any that fail to parse or contain unresolvable stereochemical or valence errors. Remove or flag invalid structures and retain only those that parse successfully and satisfy the chemical constraints expected by your downstream descriptor calculator. Document the number and nature of structures rejected during validation to quantify data quality. The validated structure set becomes the input to molecular descriptor calculation in the next workflow step.

## Related tools

- **RDKit** (Cheminformatics parser and validator for SMILES and SDF structures; performs syntax checking and chemical structure representation.)

## Examples

```
from rdkit import Chem; mols = [Chem.MolFromSmiles(smi) for smi in smiles_list]; valid = [m for m in mols if m is not None]; print(f'Parsed {len(valid)}/{len(mols)} structures')
```

## Evaluation signals

- All successfully parsed structures yield valid RDKit molecular objects with no parse exceptions.
- Structures rejected during validation are documented with specific failure codes (e.g., invalid SMILES syntax, unresolvable stereochemistry, violating valence rules).
- The count and percentage of structures passing validation are reported; significant rejection rates (>10%) warrant investigation of input quality.
- Round-trip validation (parse → export → re-parse) produces identical structures, confirming fidelity of the parsing step.
- Downstream descriptor calculator runs without errors on validated structure set, confirming structural objects are suitable for feature computation.

## Limitations

- Parser success does not guarantee chemical reasonableness or biological relevance; valid SMILES may represent unstable or non-existent compounds.
- SDF format parsing depends on correct 3D coordinate formatting; malformed geometry may parse but produce misleading 3D-dependent descriptors.
- SMILES validation alone does not detect tautomeric or protomeric variants; the same chemical entity may be represented in multiple canonical forms.
- No information on BitterPredict.m-specific chemical constraints (e.g., required molecular weight range, allowed element types) is documented in the README; validation may pass structures that later fail descriptor calculation.

## Evidence

- [other] Load raw molecular structures in SMILES or SDF format.: "Load raw molecular structures in SMILES or SDF format."
- [other] Parse and validate molecular structure syntax using a cheminformatics parser (e.g., RDKit).: "Parse and validate molecular structure syntax using a cheminformatics parser (e.g., RDKit)."
- [other] BitterPredict.m accepts CSV or Excel files containing pre-computed molecular descriptors as input, which must be prepared prior to classification.: "BitterPredict.m accepts CSV or Excel files containing pre-computed molecular descriptors as input, which must be prepared prior to classification"
