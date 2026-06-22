---
name: chemical-structure-validation-syntax
description: Use when applied immediately after loading raw SMILES strings from external databases or user input during the 2_curating workflow stage, before attempting canonicalization or 2D/3D coordinate generation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3760
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3372
  tools:
  - Python 3
  - RDKit
  - smiles.py
derived_from:
- doi: 10.7554/eLife.70780
  title: lotus
- doi: 10.1007/s00044-016-1764-y
  title: ''
evidence_spans:
- Python scripts for data parsing and transformation
- 221[[smiles.py]]
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lotus_cq
    doi: 10.7554/eLife.70780
    title: lotus
  dedup_kept_from: coll_lotus_cq
schema_version: 0.2.0
---

# Chemical Structure Validation & Syntax Checking

## Summary

Validates raw SMILES strings for correct chemical syntax and parsability using RDKit before downstream processing. This skill ensures that only chemically valid structures enter the curation pipeline, preventing silent failures in canonicalization and coordinate generation.

## When to use

Applied immediately after loading raw SMILES strings from external databases or user input during the 2_curating workflow stage, before attempting canonicalization or 2D/3D coordinate generation. Use this skill when you have ungoverned or heterogeneous SMILES from multiple sources and cannot assume they are well-formed.

## When NOT to use

- Input SMILES have already been validated by a trusted upstream source (e.g., ChEMBL or PubChem curated downloads with integrity checks).
- You are only analyzing structure-activity relationships and do not need 3D coordinates; invalid SMILES may still carry semantic information in some contexts.
- The workflow step is 3_analyzing or later; structure validation should have occurred during 2_curating.

## Inputs

- Raw SMILES strings (TSV or CSV format, e.g., interim/tables/0_original/structure/smiles.tsv.gz)
- Pandas DataFrame or iterable of SMILES strings

## Outputs

- Validated SMILES (subset of input passing syntax checks)
- Rejected SMILES list with error messages
- Boolean validation flags per input record

## How to apply

Parse each SMILES string into an RDKit molecule object using RDKit's SMILES parser and evaluate whether the parse succeeds without exception. Invalid SMILES will fail to create a valid mol object; catch these failures and flag or remove them before proceeding. This is a prerequisite for later steps (canonicalization, stereocounting, coordinate generation) because RDKit requires a valid mol object to compute molecular properties and representations. The rationale is that garbage SMILES early in the pipeline propagate errors throughout the curation, reducing the final yield of usable 2D/3D structure records.

## Related tools

- **RDKit** (Parse and validate SMILES syntax; raise exceptions for malformed input.) — https://www.rdkit.org
- **smiles.py** (LOTUS processor module that wraps RDKit validation as part of structure curation.) — https://github.com/lotusnprod/lotus-processor
- **Python 3** (Runtime environment for RDKit and error handling.)

## Examples

```
from rdkit import Chem; valid_mols = [Chem.MolFromSmiles(smi) for smi in smiles_list]; valid_smiles = [smi for smi, mol in zip(smiles_list, valid_mols) if mol is not None]
```

## Evaluation signals

- Percentage of input SMILES that parse successfully (yield rate); expect >90% for curated sources, <80% for raw databases.
- Absence of downstream RDKit errors during canonicalization and coordinate generation; all records that passed validation should proceed without parse failures.
- Comparison of valid SMILES count to final 2D/3D record count; a large drop suggests late-stage filtering issues unrelated to syntax.
- Manual spot-check of rejected SMILES for known malformations (e.g., mismatched brackets, invalid atom symbols, disconnected fragments).
- Cross-validation: re-parse all 'valid' SMILES in a second pass to confirm consistency.

## Limitations

- RDKit's SMILES parser is permissive and may accept non-standard or ambiguous SMILES that are syntactically valid but chemically nonsensical (e.g., hypervalent atoms). Syntax validation does not guarantee chemical correctness.
- No stereochemical validation at this stage; that is handled separately by stereocounting.py. Invalid stereochemistry (e.g., [C@@H] on a non-stereogenic center) may pass syntax checks.
- Tautomeric and resonance ambiguities are not resolved by syntax checking; canonicalization with RDKit's MolToSmiles(kekulize=False) occurs in a later step.
- SMILES with isotope labels, radical charges, or rare bond types may parse but cause issues in later 3D coordinate generation; syntax validation alone cannot catch these.

## Evidence

- [methods] Parse each SMILES string into RDKit molecule objects and validate chemical syntax.: "Parse each SMILES string into RDKit molecule objects and validate chemical syntax."
- [methods] The LOTUS processor employs Python with RDKit-based tools (smiles.py, sanitizing.py, stereocounting.py) as part of the 2_curating workflow stage to process and standardize molecular structures.: "The LOTUS processor employs Python with RDKit-based tools (smiles.py, sanitizing.py, stereocounting.py) as part of the 2_curating workflow stage to process and standardize molecular structures"
- [methods] Load raw SMILES strings from interim/tables/0_original/structure/smiles.tsv.gz using pandas.: "Load raw SMILES strings from interim/tables/0_original/structure/smiles.tsv.gz using pandas."
