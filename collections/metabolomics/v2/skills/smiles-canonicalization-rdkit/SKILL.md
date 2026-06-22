---
name: smiles-canonicalization-rdkit
description: Use when when processing raw SMILES strings from external databases or user input that may contain non-canonical tautomeric forms, variable stereochemical notation, or redundant representations of the same chemical structure.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3929
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3314
  tools:
  - Python 3
  - RDKit
  - pandas
  - manual expert review
  - enveda/ccs-prediction training pipeline
derived_from:
- doi: 10.7554/eLife.70780
  title: lotus
- doi: 10.1007/s00044-016-1764-y
  title: ''
- doi: 10.1186/s13321-024-00899-w
  title: ''
evidence_spans:
- Python scripts for data parsing and transformation
- 221[[smiles.py]]
- smiles.py uses RDKit for SMILES parsing and coordinate generation
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lotus_cq
    doi: 10.7554/eLife.70780
    title: lotus
  - build: coll_mol2ccs
    doi: 10.1186/s13321-024-00899-w
    title: mol2ccs
  dedup_kept_from: coll_lotus_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.7554/eLife.70780
  all_source_dois:
  - 10.7554/eLife.70780
  - 10.1007/s00044-016-1764-y
  - 10.1186/s13321-024-00899-w
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# SMILES Canonicalization via RDKit

## Summary

Standardize raw SMILES strings into canonical form using RDKit's MolToSmiles function, removing stereochemical ambiguities and tautomeric variations to ensure consistent molecular representation across structure curation pipelines.

## When to use

When processing raw SMILES strings from external databases or user input that may contain non-canonical tautomeric forms, variable stereochemical notation, or redundant representations of the same chemical structure. Apply this skill during the structure standardization phase of natural products curation workflows to ensure all structures in the downstream 2D/3D coordinate generation and database deposition steps are normalized.

## When NOT to use

- Input structures are already validated as canonical (e.g., from a trusted vendor SMILES list or pre-curated database with documented canonicalization protocol).
- Stereochemistry must be preserved exactly as input (e.g., for diastereomer-specific bioactivity studies); canonicalization will lose original stereochemical intent if the raw SMILES used non-standard notation.
- SMILES strings represent polymers, mixtures, or organometallic complexes where RDKit parsing may fail or produce unexpected canonical forms; manual curation is required.

## Inputs

- raw SMILES strings (from tsv.gz file, comma- or tab-delimited)
- RDKit-compatible molecular structure data
- structure-organism pair metadata with raw SMILES identifiers

## Outputs

- canonical SMILES strings (standardized, kekulized with aromaticity preserved)
- curated structure dataset with canonical SMILES and traceability to raw input
- validation log (parse errors, failed canonicalizations)
- tsv.gz file with canonical SMILES and associated molecular metadata

## How to apply

Parse each raw SMILES string into an RDKit molecule object and validate chemical syntax; if parsing fails, log the invalid SMILES for manual review. Call RDKit's MolToSmiles function with kekulize=False to canonicalize the structure, standardizing tautomeric forms and removing stereochemical ambiguities. Serialize the canonical SMILES output alongside the original raw SMILES for traceability. Store both forms in the curated structure dataset (e.g., interim/tables/1_translated/structure/smiles.tsv.gz). The kekulize=False parameter preserves aromaticity notation, which is critical for consistent downstream coordinate generation and structure comparison.

## Related tools

- **RDKit** (Performs SMILES parsing, validation, and canonicalization via MolToSmiles with kekulize parameter control)
- **Python 3** (Scripting language (smiles.py) that orchestrates RDKit canonicalization workflow and file I/O) — https://github.com/lotusnprod/lotus-processor
- **pandas** (Loads raw SMILES strings from interim/tables/0_original/structure/smiles.tsv.gz and writes canonical output) — https://github.com/lotusnprod/lotus-processor

## Examples

```
from rdkit import Chem; raw_smiles = 'C1=CC=C(C=C1)O'; mol = Chem.MolFromSmiles(raw_smiles); canonical_smiles = Chem.MolToSmiles(mol, kekuleSmiles=False); print(canonical_smiles)
```

## Evaluation signals

- All output canonical SMILES parse successfully into RDKit molecule objects with no errors.
- Canonical SMILES are stable under re-canonicalization (applying MolToSmiles again yields identical output).
- Tautomeric forms of the same structure (e.g., keto vs. enol) map to a single canonical SMILES.
- Original and canonical SMILES represent the same molecular graph (validated via InChIKey comparison or Tanimoto similarity on fingerprints).
- No structural information is lost: atom count, bond count, and formal charges match between input and canonical output.

## Limitations

- RDKit may fail to parse or canonicalize highly unusual or non-standard SMILES notation; invalid inputs must be manually curated or excluded.
- Canonicalization with kekulize=False assumes aromaticity perception is unambiguous; some ambiguous aromatic systems may produce inconsistent canonical forms across RDKit versions.
- Stereochemistry is removed or simplified by canonicalization; if stereospecific bioactivity data exist, the link between raw stereochemistry and canonical form must be documented separately.
- Large-scale canonicalization (>100k structures) may be I/O or memory-bound; batch processing and checkpointing are recommended.
- No changelog documented for the LOTUS processor—version-specific canonicalization behavior changes are not tracked, making reproducibility across releases uncertain.

## Evidence

- [methods] Canonicalization method and output format: "Canonicalize SMILES using RDKit's MolToSmiles with kekulize=False to standardize tautomeric forms and remove stereochemical ambiguities."
- [methods] Input file and parsing workflow: "Load raw SMILES strings from interim/tables/0_original/structure/smiles.tsv.gz using pandas. Parse each SMILES string into RDKit molecule objects and validate chemical syntax."
- [methods] Output file and dataset integration: "Serialize both 2D and 3D representations alongside canonical SMILES, storing results to interim/tables/1_translated/structure/smiles.tsv.gz."
- [methods] Tool ecosystem and role in curation pipeline: "The LOTUS processor employs Python with RDKit-based tools (smiles.py, sanitizing.py, stereocounting.py) as part of the 2_curating workflow stage"
- [methods] Broader curation context and dataset scale: "231330 | 153956 (3D|2D) unique curated structures and 42166 unique organisms"
