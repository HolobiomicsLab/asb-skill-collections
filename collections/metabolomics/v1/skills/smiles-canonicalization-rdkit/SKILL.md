---
name: smiles-canonicalization-rdkit
description: Use when when preprocessing raw SMILES strings from external chemistry databases (e.g., CCSBase, METLIN-CCS, or custom compound libraries) that may contain multiple valid but non-canonical notations for the same molecular structure.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3314
  - http://edamontology.org/topic_0154
  tools:
  - manual expert review
  - RDKit
  - enveda/ccs-prediction training pipeline
derived_from:
- doi: 10.1186/s13321-024-00899-w
  title: mol2ccs
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mol2ccs
    doi: 10.1186/s13321-024-00899-w
    title: mol2ccs
  dedup_kept_from: coll_mol2ccs
schema_version: 0.2.0
---

# SMILES canonicalization with RDKit

## Summary

Standardize SMILES string representations of chemical structures using RDKit to ensure structural consistency before converting to graph representations for machine learning. This step eliminates notation variants and ambiguities that could otherwise produce different graph features from chemically identical molecules.

## When to use

When preprocessing raw SMILES strings from external chemistry databases (e.g., CCSBase, METLIN-CCS, or custom compound libraries) that may contain multiple valid but non-canonical notations for the same molecular structure. Apply this before constructing molecular graphs for GNN input to ensure that identical chemicals always produce identical feature tensors regardless of how they were originally notated.

## When NOT to use

- SMILES strings are already known to be canonicalized or from a single standardized source.
- The analysis requires preservation of the original notation (e.g., for notation bias studies).
- Input is not in SMILES format (e.g., InChI, molecular formula, or structure image).

## Inputs

- Raw SMILES strings (CSV, Excel, or Parquet column)
- Column name or file path specifying the SMILES field
- Optional: molecular validity threshold or error handling strategy

## Outputs

- Canonical SMILES strings (one per molecule)
- Validity log or report (fraction parsed successfully, rejected SMILES)

## How to apply

Load raw SMILES strings from the input dataset (typically a CSV, Excel, or Parquet file with a designated SMILES column). For each SMILES string, use RDKit's canonicalization function to convert it to a unique, standardized form that represents the same molecular structure unambiguously. Verify that canonicalization does not reject the input (i.e., RDKit successfully parses it as a valid molecule); invalid SMILES should be logged and filtered. The canonicalized SMILES output becomes the input for the next step (molecular graph construction). This preprocessing ensures that downstream graph representations and GNN predictions are deterministic and comparable across different data sources or notational variations.

## Related tools

- **RDKit** (Canonicalize SMILES strings and parse molecular structure to ensure validity) — https://github.com/rdkit/rdkit
- **enveda/ccs-prediction training pipeline** (Applies canonicalization within the data preprocessing notebooks before graph construction) — https://github.com/enveda/ccs-prediction

## Examples

```
from rdkit import Chem; canonical_smiles = Chem.MolToSmiles(Chem.MolFromSmiles('CCO'))
```

## Evaluation signals

- All input SMILES strings are successfully parsed by RDKit; log parsing errors and rejection rate.
- Canonical SMILES are deterministic: running canonicalization twice on the same input produces identical output.
- Equivalent molecules notated differently (e.g., CCO vs OCC for ethanol) map to the same canonical form.
- Canonical SMILES are valid input to downstream molecular graph construction (no errors in bond/atom feature extraction).
- Canonical SMILES are shorter or equal in length to originals (canonical form removes redundant notation).

## Limitations

- RDKit's canonicalization may fail on unusual or malformed SMILES; invalid structures must be filtered before graph construction.
- Canonicalization does not validate chemical plausibility or detect stereoisomers; stereochemistry must be explicitly encoded in SMILES.
- Different RDKit versions may produce slightly different canonical forms; reproducibility requires fixing the RDKit version.
- Very large SMILES strings or highly complex structures may be slow to canonicalize; performance depends on molecular complexity.

## Evidence

- [other] Canonicalize SMILES using RDKit to ensure structural consistency.: "Canonicalize SMILES using RDKit to ensure structural consistency."
- [readme] Each user should download the raw database (as excel/csv) and read them in the two notebooks for each database located at https://github.com/enveda/ccs-prediction/tree/main/notebooks/data_processing.: "Each user should download the raw database (as excel/csv) and read them in the two notebooks for each database"
- [other] Convert each canonical SMILES to a molecular graph representation with atom and bond features.: "Convert each canonical SMILES to a molecular graph representation with atom and bond features."
