---
name: structure-file-format-conversion
description: Use when you have raw structure input from diverse external databases
  (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0335
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3372
  tools:
  - Python 3
  - RDKit
  - smiles.py
  - sanitizing.py
  - pandas
  license_tier: restricted
  provenance_tier: literature
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.7554/eLife.70780
  all_source_dois:
  - 10.7554/eLife.70780
  - 10.1007/s00044-016-1764-y
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Structure file format conversion

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Convert raw molecular structure representations (SMILES strings, SDF files, mol blocks) into standardized canonical and dimensional coordinate formats (2D/3D SMILES, mol files) using RDKit-based parsing and serialization. This skill is essential during the curation stage to ensure consistent structure representation across heterogeneous source databases before downstream computational chemistry tasks.

## When to use

Apply this skill when you have raw structure input from diverse external databases (e.g., ChEMBL, PubChem, Wikidata) that exists in mixed or non-canonical formats and you need to generate normalized, reproducible 2D and 3D coordinate representations for structure-organism pair curation, validation, or molecular docking workflows.

## When NOT to use

- Input structures are already in a validated, canonical format from a single trusted source and no dimensional coordinates are required.
- Structures contain novel or non-standard chemical entities (e.g., heavy metals, organometallics, or undefined R-groups) that RDKit cannot sanitize without manual curation.
- The downstream analysis does not require 3D conformations or canonical standardization (e.g., simple similarity searching on raw SMILES).

## Inputs

- Raw SMILES strings (TSV/CSV format, gzip-compressed)
- Mol block files or SDF structures from external databases
- Structure-organism pair tables with heterogeneous source formats

## Outputs

- Canonical SMILES strings (kekulized=False)
- 2D coordinate representations (Compute2DCoords output)
- 3D coordinate representations (MMFF94-optimized conformers)
- Serialized structure records (TSV format, gzip-compressed) with standardized fields

## How to apply

Load raw SMILES strings or structure files using pandas and parse them into RDKit molecule objects, validating chemical syntax. Canonicalize each structure using RDKit's MolToSmiles with kekulize=False to remove stereochemical ambiguities and standardize tautomeric forms. Generate 2D coordinates via RDKit's Compute2DCoords algorithm for visualization and structure validation. Generate 3D coordinates using RDKit's AllChem.EmbedMolecule with distance geometry followed by MMFF94 force-field optimization to produce energetically plausible conformations. Serialize canonical SMILES alongside both 2D and 3D coordinate representations to tab-separated output files, retaining traceability to source structure identifiers. Validate output by checking that all structures round-trip correctly through RDKit and that coordinate sets are non-degenerate.

## Related tools

- **RDKit** (Parsing SMILES into molecule objects, canonicalization, 2D/3D coordinate generation, molecule sanitization and validation)
- **smiles.py** (LOTUS processor script that orchestrates SMILES parsing and standardization) — https://github.com/lotusnprod/lotus-processor
- **sanitizing.py** (Companion script to smiles.py that validates and cleans molecular structures during curation) — https://github.com/lotusnprod/lotus-processor
- **Python 3** (Runtime environment for RDKit-based conversion pipeline)
- **pandas** (Loading and serializing raw SMILES tables from TSV/CSV files)

## Examples

```
python scripts/smiles.py --input interim/tables/0_original/structure/smiles.tsv.gz --output interim/tables/1_translated/structure/smiles.tsv.gz --kekulize False --generate-2d --generate-3d --force-field mmff94
```

## Evaluation signals

- All input SMILES strings successfully parse into RDKit molecule objects without syntax errors; no structures are lost during parsing.
- Canonical SMILES output is invariant under repeated round-trip through RDKit (MolToSmiles → MolFromSmiles → MolToSmiles produces identical strings).
- 2D and 3D coordinate sets are non-degenerate: each molecule has >0 heavy atoms with distinct atomic positions; 3D coordinates reflect MMFF94 energy minimization (no strained/colliding atoms).
- Output file schema matches expected format: TSV with columns for original identifier, canonical SMILES, 2D coordinates, 3D coordinates, and source database link.
- File size and record count of output matches input; no structures silently dropped; gzip compression reduces file size by ≥70% relative to uncompressed TSV.

## Limitations

- RDKit sanitization may fail on structures with non-standard valency, exotic formal charges, or metal coordination; such structures require manual intervention or alternative chemistry toolkits.
- 2D coordinate generation via Compute2DCoords may produce overlapping or hard-to-interpret layouts for highly symmetric or cage-like molecules; visual inspection is recommended.
- 3D coordinate generation via EmbedMolecule is non-deterministic and stochastic; MMFF94 optimization may fail to converge for very large molecules or those with unusual ring systems; multiple conformer sampling may be needed.
- Kekulization and tautomeric standardization via MolToSmiles(kekulize=False) may lose stereochemical information if input SMILES lack explicit stereochemistry markers; output should be validated against source databases.
- Conversion assumes input structures are organic molecules; inorganic compounds, salts, or mixtures may not convert correctly and should be filtered before processing.

## Evidence

- [other] The LOTUS processor employs Python with RDKit-based tools (smiles.py, sanitizing.py, stereocounting.py) as part of the 2_curating workflow stage to process and standardize molecular structures, converting raw structures into curated 2D and 3D format representations for the documented structure-organism pairs.: "LOTUS processor employs Python with RDKit-based tools (smiles.py, sanitizing.py, stereocounting.py) as part of the 2_curating workflow stage to process and standardize molecular structures,"
- [other] Load raw SMILES strings from interim/tables/0_original/structure/smiles.tsv.gz using pandas. Parse each SMILES string into RDKit molecule objects and validate chemical syntax. Canonicalize SMILES using RDKit's MolToSmiles with kekulize=False to standardize tautomeric forms and remove stereochemical ambiguities. Generate 2D coordinates via RDKit's Compute2DCoords algorithm. Generate 3D coordinates using RDKit's AllChem.EmbedMolecule with distance geometry, followed by MMFF94 force-field optimization.: "Parse each SMILES string into RDKit molecule objects and validate chemical syntax. Canonicalize SMILES using RDKit's MolToSmiles with kekulize=False to standardize tautomeric forms. Generate 2D"
- [other] Serialize both 2D and 3D representations alongside canonical SMILES, storing results to interim/tables/1_translated/structure/smiles.tsv.gz.: "Serialize both 2D and 3D representations alongside canonical SMILES, storing results to interim/tables/1_translated/structure/smiles.tsv.gz"
- [methods] 231330 | 153956 (3D|2D) unique curated structures and 42166 unique organisms: "231330 | 153956 (3D|2D) unique curated structures and 42166 unique organisms"
- [methods] Data originates from 31 initial open databases: "originating from 31 initial open databases"
