---
name: smiles-string-translation-and-standardization
description: 'Use when you have raw SMILES strings from multiple external database sources (e.g., PubChem, ChEMBL, vendor databases) that need to be integrated into a unified structure registry. Indicators include: (1) raw SMILES table exists at a known interim input path (e.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0154
  tools:
  - R
  - Python
  - smiles.py
  - sanitizing.py
  - Python 3
  - RDKit (implied dependency)
derived_from:
- doi: 10.7554/eLife.70780
  title: lotus
- doi: 10.1007/s00044-016-1764-y
  title: ''
evidence_spans:
- standardizing.R, 1_integrating.R, 1_cleaningOriginal.R, 4_cleaningTaxonomy.R, 5_addingOTL.R
- 1_integrating.R
- 221[[smiles.py]], 260[[3_cleaningAndEnriching/sanitizing.py]]
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lotus
    doi: 10.7554/eLife.70780
    title: lotus
  dedup_kept_from: coll_lotus
schema_version: 0.2.0
---

# SMILES String Translation and Standardization

## Summary

A two-stage transformation that converts raw SMILES strings into standardized, deduplicated structural identifiers through translation and sanitization. This skill is essential in natural products databases where raw SMILES from heterogeneous sources must be normalized to enable consistent structure-organism pair representation and chemical validity verification.

## When to use

Apply this skill when you have raw SMILES strings from multiple external database sources (e.g., PubChem, ChEMBL, vendor databases) that need to be integrated into a unified structure registry. Indicators include: (1) raw SMILES table exists at a known interim input path (e.g., interim/tables/0_original/structure/smiles.tsv.gz), (2) you need to deduplicate structures across the integration, (3) you require chemical validity checks before downstream molecular analysis (e.g., docking, property prediction), or (4) you are building a curated structure-organism reference database.

## When NOT to use

- Input is already a validated, deduplicated structure table with canonical SMILES—skip directly to downstream molecular property or organism annotation steps.
- You need 3D structure coordinates or conformer generation—SMILES alone cannot provide spatial geometry; use specialized tools like RDKit's AllChem.EmbedMolecule or molecular docking software instead.
- Raw input is not in SMILES format but in InChI, MOL, or SDF—apply format conversion before entering this pipeline.

## Inputs

- interim/tables/0_original/structure/smiles.tsv.gz (raw SMILES table with identifiers and source SMILES strings)
- smiles.py (translation and standardization script)
- sanitizing.py (chemical validation and deduplication script)

## Outputs

- interim/tables/1_translated/structure/smiles.tsv.gz (translated and standardized SMILES table)
- interim/tables/1_translated/structure/unique.tsv.gz (deduplicated, validated unique structure table)

## How to apply

Execute a sequential two-file transformation pipeline: (1) Load the raw SMILES table from interim/tables/0_original/structure/smiles.tsv.gz and apply smiles.py to translate and standardise SMILES strings, producing interim/tables/1_translated/structure/smiles.tsv.gz. This step handles SMILES normalization and format conversion. (2) Load the translated SMILES output and apply sanitizing.py to validate chemical structures (removing malformed or chemically impossible entries), deduplicate identical structures, and generate the final standardized unique structure table at interim/tables/1_translated/structure/unique.tsv.gz. The pipeline treats each stage as a deterministic file-to-file transformation; validate intermediate outputs by checking record counts and comparing SMILES canonical forms before and after each step.

## Related tools

- **smiles.py** (Translate and standardize raw SMILES strings from multiple sources into a normalized format) — https://github.com/lotusnprod/lotus-processor
- **sanitizing.py** (Validate chemical structures for chemical feasibility, remove invalid entries, and deduplicate identical structures) — https://github.com/lotusnprod/lotus-processor
- **Python 3** (Runtime environment for executing smiles.py and sanitizing.py scripts)
- **RDKit (implied dependency)** (Chemical informatics library used internally by standardization scripts to parse, validate, and canonicalize SMILES)

## Examples

```
python smiles.py --input interim/tables/0_original/structure/smiles.tsv.gz --output interim/tables/1_translated/structure/smiles.tsv.gz && python sanitizing.py --input interim/tables/1_translated/structure/smiles.tsv.gz --output interim/tables/1_translated/structure/unique.tsv.gz
```

## Evaluation signals

- Record count before and after sanitizing.py: expect loss of records due to invalid structure removal and deduplication; document the number of invalid/duplicate entries discarded.
- SMILES canonical form consistency: verify that identical chemical structures produce identical canonical SMILES before and after the pipeline (e.g., via RDKit Chem.MolToSmiles(Chem.MolFromSmiles(smi), canonical=True)).
- Absence of parsing errors: check that sanitizing.py completes without raising exceptions on translated SMILES—malformed SMILES should be logged and excluded, not crash the pipeline.
- Uniqueness guarantee: confirm that unique.tsv.gz contains no duplicate SMILES entries when sorted; deduplication is complete if cardinality(unique_smiles) < cardinality(translated_smiles).
- Integrity of linked metadata: verify that structure identifiers and organism/reference links are correctly preserved through both transformations (check for orphaned or misaligned rows in the curated output).

## Limitations

- SMILES canonicalization is deterministic but tool-dependent; RDKit and other cheminformatics libraries may produce subtly different canonical forms. Use a single standardization library throughout the pipeline to ensure reproducibility.
- Invalid SMILES strings (e.g., due to typographical errors, rare valence states, or dialect variations from source databases) are discarded during sanitization, potentially losing structure-organism relationships from the raw input.
- The pipeline does not handle stereochemistry explicitly in the dedupe step; if stereoisomers must be distinguished, a post-sanitization stereocounting step (referenced in the LOTUS workflow) is required.
- Performance scales with input size; the LOTUS implementation processes >500,000 unique structures; batch processing or chunking may be needed for very large datasets on resource-constrained systems.

## Evidence

- [methods] smiles.py converts raw SMILES from interim/tables/0_original/structure/smiles.tsv.gz, and sanitizing.py then produces the final standardized unique structure table at interim/tables/1_translated/structure/unique.tsv.gz: "smiles.py converts raw SMILES from interim/tables/0_original/structure/smiles.tsv.gz, and sanitizing.py then produces the final standardized unique structure table at"
- [other] The LOTUS processor applies two consecutive file-to-file transformations: smiles.py converts raw SMILES from interim/tables/0_original/structure/smiles.tsv.gz, and sanitizing.py then produces the final standardized unique structure table: "The LOTUS processor applies two consecutive file-to-file transformations: smiles.py converts raw SMILES from interim/tables/0_original/structure/smiles.tsv.gz, and sanitizing.py then produces the"
- [other] Load raw SMILES table from interim/tables/0_original/structure/smiles.tsv.gz using Python. Execute smiles.py to translate and standardise SMILES strings, generating interim/tables/1_translated/structure/smiles.tsv.gz. Load translated SMILES and apply sanitizing.py to validate chemical structures, remove invalid entries, and deduplicate: "Load raw SMILES table from interim/tables/0_original/structure/smiles.tsv.gz using Python. Execute smiles.py to translate and standardise SMILES strings, generating"
- [methods] 231330 | 153956 (3D|2D) unique curated structures: "231330 | 153956 (3D|2D) unique curated structures"
- [intro] LOTUS provides documented structure-organism pairs to allow more complete understanding of organisms and their chemistry within computational natural products research: "LOTUS provides documented structure-organism pairs to allow more complete understanding of organisms and their chemistry within computational natural products research"
