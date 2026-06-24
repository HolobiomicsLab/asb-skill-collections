---
name: molecular-coordinate-generation-2d3d
description: Use when you have canonicalized SMILES strings from a chemical structure
  database and need both 2D (flat) and 3D (conformer) representations for molecular
  visualization, molecular docking, or structure archival.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0570
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3314
  tools:
  - Python 3
  - RDKit
  - smiles.py
  - sanitizing.py
  - pandas
  license_tier: restricted
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

# molecular-coordinate-generation-2d3d

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Generate and optimize 2D and 3D molecular coordinate representations from canonicalized SMILES strings using RDKit's geometry algorithms and force-field methods. This skill standardizes molecular structure depictions for computational chemistry workflows, enabling downstream docking, visualization, and structure-organism pair curation.

## When to use

Apply this skill when you have canonicalized SMILES strings from a chemical structure database and need both 2D (flat) and 3D (conformer) representations for molecular visualization, molecular docking, or structure archival. Specifically, use it as part of the 2_curating workflow stage after SMILES canonicalization and before storing final curated structure-organism pairs in the LOTUS pipeline.

## When NOT to use

- Input SMILES are not yet canonicalized or validated; perform sanitizing.py and stereocounting.py steps first.
- 3D coordinates are not needed (e.g., for 2D diagram-only use cases); consider generating only 2D coordinates to save computation.
- Input structures contain metal centers or non-standard chemical environments where MMFF94 force-field parameters are unavailable or inappropriate.

## Inputs

- canonicalized SMILES strings (gzipped TSV format)
- RDKit-compatible SMILES encoding with kekulize=False

## Outputs

- 2D coordinate representations (Compute2DCoords output)
- 3D coordinate representations with MMFF94-optimized conformers
- canonical SMILES alongside coordinate serializations (gzipped TSV)

## How to apply

Load canonicalized SMILES from a gzipped TSV file (e.g., interim/tables/0_original/structure/smiles.tsv.gz) using pandas. For each SMILES string, parse it into an RDKit molecule object and validate chemical syntax. Generate 2D coordinates by calling RDKit's Compute2DCoords algorithm to compute a planar layout. Generate 3D coordinates by calling AllChem.EmbedMolecule with distance geometry, then optimize the resulting conformer using MMFF94 force-field minimization to relieve strain. Serialize both the canonical SMILES and the 2D and 3D coordinate sets to an output TSV file (e.g., interim/tables/1_translated/structure/smiles.tsv.gz). The rationale is that 2D coordinates support human-readable depictions and diagram generation, while 3D coordinates with MMFF94 optimization provide chemically reasonable conformers suitable for molecular docking and computational screening.

## Related tools

- **RDKit** (Provides MolToSmiles canonicalization, Compute2DCoords for 2D layout, AllChem.EmbedMolecule for distance geometry 3D generation, and MMFF94 force-field optimization) — http://www.rdkit.org
- **smiles.py** (Python wrapper script that orchestrates SMILES parsing, canonicalization, and 2D/3D coordinate generation as part of the LOTUS 2_curating stage) — https://github.com/lotusnprod/lotus-processor
- **sanitizing.py** (Preceding workflow step that validates and sanitizes raw SMILES before input to coordinate generation) — https://github.com/lotusnprod/lotus-processor
- **pandas** (Loads gzipped TSV files containing raw SMILES strings and writes output coordinate tables)
- **Python 3** (Runtime environment for RDKit and the orchestration pipeline)

## Evaluation signals

- All canonicalized SMILES parse successfully into valid RDKit molecule objects with no syntax errors.
- 2D coordinate sets are non-degenerate (all atoms have distinct x,y positions) and represent valid 2D structure layouts.
- 3D coordinates are generated without distance geometry failures and MMFF94 optimization converges (energies stabilize).
- Output TSV contains expected columns: canonical SMILES, 2D coordinate block, 3D coordinate block, and no rows are missing coordinates.
- Round-trip serialization/deserialization of coordinate sets preserves molecular graph topology and atom ordering.

## Limitations

- MMFF94 force-field parameters are not available for all atom types; molecules with exotic metal centers or unusual coordination states may fail optimization or produce unrealistic geometries.
- Distance geometry can produce multiple distinct 3D conformers for the same molecule; this skill outputs one representative conformer, not an ensemble or the global minimum energy structure.
- Stereochemistry is assumed to be encoded correctly in the input SMILES; if stereochemical ambiguities remain after canonicalization, 3D coordinates may not reflect the intended stereoisomer.
- No changelog available to track updates or bug fixes in the coordinate generation algorithms across workflow versions.

## Evidence

- [other] The LOTUS processor employs Python with RDKit-based tools (smiles.py, sanitizing.py, stereocounting.py) as part of the 2_curating workflow stage to process and standardize molecular structures, converting raw structures into curated 2D and 3D format representations for the documented structure-organism pairs.: "The LOTUS processor employs Python with RDKit-based tools (smiles.py, sanitizing.py, stereocounting.py) as part of the 2_curating workflow stage to process and standardize molecular structures,"
- [other] Parse each SMILES string into RDKit molecule objects and validate chemical syntax. 3. Canonicalize SMILES using RDKit's MolToSmiles with kekulize=False to standardize tautomeric forms and remove stereochemical ambiguities. 4. Generate 2D coordinates via RDKit's Compute2DCoords algorithm. 5. Generate 3D coordinates using RDKit's AllChem.EmbedMolecule with distance geometry, followed by MMFF94 force-field optimization.: "Generate 2D coordinates via RDKit's Compute2DCoords algorithm. 5. Generate 3D coordinates using RDKit's AllChem.EmbedMolecule with distance geometry, followed by MMFF94 force-field optimization."
- [methods] 231330 | 153956 (3D|2D) unique curated structures and 42166 unique organisms: "231330 | 153956 (3D|2D) unique curated structures and 42166 unique organisms"
- [other] Load raw SMILES strings from interim/tables/0_original/structure/smiles.tsv.gz using pandas. 2. Parse each SMILES string into RDKit molecule objects and validate chemical syntax.: "Load raw SMILES strings from interim/tables/0_original/structure/smiles.tsv.gz using pandas. 2. Parse each SMILES string into RDKit molecule objects and validate chemical syntax."
- [other] Serialize both 2D and 3D representations alongside canonical SMILES, storing results to interim/tables/1_translated/structure/smiles.tsv.gz.: "Serialize both 2D and 3D representations alongside canonical SMILES, storing results to interim/tables/1_translated/structure/smiles.tsv.gz."
