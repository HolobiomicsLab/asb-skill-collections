---
name: tautomer-standardization
description: Use when ingesting raw SMILES strings from curated structure inventories where the same chemical may be represented in multiple tautomeric forms (e.g., keto–enol pairs, lactam–lactim forms) across different literature sources or input databases.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3962
  edam_topics:
  - http://edamontology.org/topic_3314
  - http://edamontology.org/topic_0154
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

# tautomer-standardization

## Summary

Standardize molecular structures by canonicalizing SMILES representations to remove tautomeric ambiguities and stereochemical variants, ensuring a single reference form per unique chemical entity. This is critical in natural products databases where raw inputs from multiple sources may represent the same molecule in different tautomeric states.

## When to use

Apply this skill when ingesting raw SMILES strings from curated structure inventories where the same chemical may be represented in multiple tautomeric forms (e.g., keto–enol pairs, lactam–lactim forms) across different literature sources or input databases. Use it as the first normalization step in the structure curation pipeline, before generating 2D or 3D coordinates or performing chemical comparisons.

## When NOT to use

- Input is already a curated structure table with canonical SMILES (re-standardizing introduces no new information and risks data loss if original ambiguities were intentional).
- The research goal requires preservation of specific tautomeric states or protonation variants as distinct chemical entities (e.g., pharmacophore or stereoisomer-specific studies).
- Raw SMILES contain invalid or non-standard chemical notation that fails RDKit parsing; clean and validate before standardization.

## Inputs

- raw SMILES strings (TSV or delimited format)
- chemical identifier or reference pairs (structure-organism or source mappings)
- raw molecular structure representations in variable tautomeric states

## Outputs

- canonical SMILES strings (one per unique chemical entity)
- standardized structure table with tautomer-normalized mappings
- curated structure–organism pair indices with deduplicated chemical identities

## How to apply

Load raw SMILES strings from the interim structure table (interim/tables/0_original/structure/smiles.tsv.gz). Parse each SMILES string into an RDKit molecule object and validate chemical syntax. Apply RDKit's MolToSmiles function with kekulize=False parameter to canonicalize the structure and suppress kekule bond notation, which implicitly resolves tautomeric ambiguities to RDKit's preferred form. The resulting canonical SMILES serves as the unique identifier for that chemical entity, removing stereochemical variant noise from raw inputs. Serialize the canonical SMILES output alongside the original representation for traceability, writing results to the curated structure table (interim/tables/1_translated/structure/smiles.tsv.gz).

## Related tools

- **RDKit** (Core library for parsing SMILES strings, canonicalizing tautomeric forms via MolToSmiles with kekulize=False, and validating chemical syntax)
- **smiles.py** (LOTUS processor module that orchestrates raw SMILES loading, parsing, canonicalization, and output serialization) — https://github.com/lotusnprod/lotus-processor
- **Python 3** (Language runtime for invoking RDKit-based standardization workflows and managing file I/O)

## Examples

```
from rdkit import Chem; smiles_raw = 'C1=CC=C(C=C1)C(=O)C'; mol = Chem.MolFromSmiles(smiles_raw); canonical_smiles = Chem.MolToSmiles(mol, kekuleSmiles=False); print(canonical_smiles)
```

## Evaluation signals

- All output canonical SMILES are valid RDKit-parseable molecules with no syntax errors.
- Tautomeric variants of the same chemical (e.g., keto and enol forms) map to the same canonical SMILES output.
- The canonical SMILES are deterministic: re-running the standardization on the same input produces identical output.
- Serialized output table has 1:1 mapping of unique chemical entities to canonical SMILES (no duplicates within the curated set).
- Traceability is maintained: original raw SMILES are preserved alongside canonical forms, allowing comparison and audit.

## Limitations

- RDKit's canonicalization algorithm applies a single preferred tautomeric form; esoteric or non-standard tautomers may be collapsed to the nearest RDKit-recognized state, potentially losing domain-specific variants.
- Kekulize=False suppresses explicit bond-order indicators but does not resolve all ambiguities in resonance structures or aromaticity edge cases; manual curation of unusual chemotypes may still be required.
- The standardization is deterministic only within a given RDKit version; updates to RDKit's canonicalization rules can change the output for the same input SMILES, requiring re-standardization of historical data.
- Performance scales linearly with the number of SMILES but large datasets (>100k structures) may require batching or parallelization to remain tractable.

## Evidence

- [methods] Canonicalize SMILES using RDKit's MolToSmiles with kekulize=False to standardize tautomeric forms and remove stereochemical ambiguities.: "Canonicalize SMILES using RDKit's MolToSmiles with kekulize=False to standardize tautomeric forms and remove stereochemical ambiguities."
- [methods] Parse each SMILES string into RDKit molecule objects and validate chemical syntax.: "Parse each SMILES string into RDKit molecule objects and validate chemical syntax."
- [methods] The LOTUS processor employs Python with RDKit-based tools (smiles.py, sanitizing.py, stereocounting.py) as part of the 2_curating workflow stage to process and standardize molecular structures, converting raw structures into curated 2D and 3D format representations for the documented structure-organism pairs.: "The LOTUS processor employs Python with RDKit-based tools (smiles.py, sanitizing.py, stereocounting.py) as part of the 2_curating workflow stage to process and standardize molecular structures"
- [intro] *LOTUS* is a comprehensive collection of documented structure-organism pairs.: "*LOTUS* is a comprehensive collection of documented structure-organism pairs."
