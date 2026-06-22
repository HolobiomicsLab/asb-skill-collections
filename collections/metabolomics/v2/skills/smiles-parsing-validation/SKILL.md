---
name: smiles-parsing-validation
description: Use when when you have a dataset of molecular structures encoded as SMILES strings that will be processed downstream (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3762
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3172
  tools:
  - RDKit
  - HassounLab/BAM
derived_from:
- doi: 10.1021/acs.analchem.4c01565
  title: bam
evidence_spans:
- standard library for parsing and manipulating SMILES and chemical structures
- HassounLab/BAM
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_bam
    doi: 10.1021/acs.analchem.4c01565
    title: bam
  dedup_kept_from: coll_bam
schema_version: 0.2.0
---

# SMILES Parsing and Validation

## Summary

Parse and validate SMILES strings using RDKit to ensure chemical validity before applying biotransformation rules or other molecular transformations. This is a prerequisite quality-control step for untargeted metabolomics workflows where input structures must be chemically sound.

## When to use

When you have a dataset of molecular structures encoded as SMILES strings that will be processed downstream (e.g., by biotransformation rule engines, molecular networking, or structure annotation pipelines) and you need to filter out malformed or chemically invalid entries before proceeding.

## When NOT to use

- Input is already a pre-validated or curated structure database (e.g., ChEBI, PubChem standardized structures).
- You need 3D spatial information or conformers; RDKit parsing produces 2D graphs only.
- Input structures are in formats other than SMILES (e.g., InChI, MOL, SDF) without prior conversion.

## Inputs

- CSV file or dataset containing molecular identifiers and SMILES strings
- List of SMILES strings in canonical or non-canonical form

## Outputs

- Validated SMILES strings (canonical form)
- Validated RDKit molecular objects (mol objects)
- Rejection log containing original SMILES that failed validation
- Deduplicated structure index mapping original to canonical SMILES

## How to apply

Load each SMILES string from the input dataset (CSV or list format) and parse it using RDKit's canonical SMILES parser. For each parsed structure, validate chemical validity by checking that the molecular graph is chemically sensible (proper valence, atom types, bonding). Deduplicate any canonicalized SMILES that map to the same molecular structure. Retain only SMILES strings that parse without errors and pass RDKit's validation checks. Log or report the identifiers and original SMILES of any structures that fail validation, as these will be excluded from downstream biotransformation or annotation steps. This ensures that only valid chemical structures are propagated to rule application engines.

## Related tools

- **RDKit** (SMILES parser and molecular validity checker; used to parse, canonicalize, and validate chemical structures before biotransformation rule application) — https://www.rdkit.org/
- **HassounLab/BAM** (Biotransformation-based annotation pipeline that requires validated SMILES as input for molecular structure discovery) — https://github.com/HassounLab/BAM

## Examples

```
from rdkit import Chem; smiles_list = ['CC(=O)O', 'c1ccccc1']; valid_mols = [Chem.MolFromSmiles(s) for s in smiles_list if Chem.MolFromSmiles(s) is not None]; valid_canonical = [Chem.MolToSmiles(m) for m in valid_mols]
```

## Evaluation signals

- All output SMILES strings are valid RDKit mol objects with no parse errors or warnings.
- Canonicalized SMILES are deterministic and reproducible (same input → same canonical output across runs).
- Rejection count and reason codes are tracked; any rejected entries are documented with original SMILES for manual review.
- No chemical valence errors, disconnected atoms, or invalid bond orders in validated structures.
- Downstream biotransformation rule application succeeds without structure-parsing errors on the validated SMILES set.

## Limitations

- RDKit SMILES parsing assumes 2D molecular graphs; stereochemistry encoding in SMILES may be ambiguous or lost if not properly canonicalized.
- Some non-standard or highly unusual SMILES notations (e.g., chemically valid but rare forms) may fail validation despite being technically correct.
- Validation does not check for biological or metabolic plausibility; a chemically valid structure may still be unrealistic or unmeasurable in a given organism.

## Evidence

- [other] Load input molecular structures in SMILES format from the provided dataset. Parse and validate each SMILES string using RDKit to ensure chemical validity.: "Load input molecular structures in SMILES format from the provided dataset. Parse and validate each SMILES string using RDKit to ensure chemical validity."
- [readme] The desired reaction dataset of interest needs to be specified. We have used KEGG and RetroRules as examples. metabolites_list = csv file of metabolites and their structures (represented by SMILES) that are included in the reaction dataset: "metabolites_list = csv file of metabolites and their structures (represented by SMILES) that are included in the reaction dataset"
- [other] Collect and deduplicate the transformed structures, maintaining parent–product relationships.: "Collect and deduplicate the transformed structures, maintaining parent–product relationships."
