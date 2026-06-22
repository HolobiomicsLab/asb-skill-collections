---
name: molecular-geometry-file-parsing
description: Use when when you have a molecular structure in XYZ or similar coordinate format and need to initialize QCxMS2 or related workflows for EI mass spectrum calculation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2427
  edam_topics:
  - http://edamontology.org/topic_0176
  - http://edamontology.org/topic_3314
  tools:
  - QCxMS2
  - xtb
  - ORCA
  - molbar
  - geodesic_interpolate
  - CREST
derived_from:
- doi: 10.1021/jasms.5c00234
  title: QCxMS2
evidence_spans:
- Program package for the quantum mechanical calculation of EI mass spectra using automated reaction network exploration
- '**xtb** (version > 6.7.1 - bleeding edge version)'
- '**orca** (version >= 6.0.0)'
- '**molbar** (version >= 1.1.3)'
- '**geodesic_interpolate** (version'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_qcxms2_cq
    doi: 10.1021/jasms.5c00234
    title: QCxMS2
  dedup_kept_from: coll_qcxms2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.5c00234
  all_source_dois:
  - 10.1021/jasms.5c00234
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-geometry-file-parsing

## Summary

Parse and validate input molecular geometry files (XYZ or equivalent formats) to extract atomic coordinates and connectivity information for downstream quantum mechanical calculations. This skill is essential for initializing automated reaction network exploration pipelines in computational mass spectrometry.

## When to use

When you have a molecular structure in XYZ or similar coordinate format and need to initialize QCxMS2 or related workflows for EI mass spectrum calculation. Trigger this skill at the start of any QCxMS2 pipeline to ensure the input molecular geometry is properly formatted and validated before dispatching to external quantum mechanical programs (xtb, CREST, ORCA).

## When NOT to use

- Input is already a pre-optimized molecular structure with known low-energy conformation and no further geometry validation is needed — proceed directly to reaction network exploration.
- Molecular geometry is incomplete or missing critical atoms; the file should first be completed with a structure builder before parsing.
- Input file is in a format other than XYZ or recognized coordinate format; convert or reformat the file first using external tools.

## Inputs

- XYZ format molecular geometry file
- molecular structure file (coordinate format)
- atomic coordinates (Cartesian or equivalent)
- molecular connectivity information

## Outputs

- parsed and validated molecular geometry object
- extracted atomic coordinates and element identities
- structure representation ready for QCxMS2 initialization
- validation report (coordinates, elements, bond sanity checks)

## How to apply

Begin by reading the input molecular geometry file in XYZ format or equivalent coordinate representation. Validate the file structure: confirm that atomic symbols are recognized, coordinates are numeric and finite, and the geometry represents a valid molecular structure (no NaN values, reasonable bond distances). Extract and store the parsed atomic coordinates and element identities. Pass the validated geometry object to the QCxMS2 driver with reaction network parameters. If validation fails (missing atoms, corrupt coordinates, or unrecognized element symbols), raise an error and request corrected input before proceeding to geometry optimization via xtb or conformer generation via CREST.

## Related tools

- **QCxMS2** (consumes validated geometry; orchestrates full EI mass spectrum calculation pipeline) — https://github.com/grimme-lab/QCxMS2
- **xtb** (receives parsed geometry for fast geometry optimization and conformer generation after parsing) — https://github.com/grimme-lab/xtb
- **CREST** (consumes geometry from parser to explore conformational space in automated ensemble sampling) — https://github.com/crest-lab/crest

## Evaluation signals

- Parsed atomic coordinates match input file values within floating-point tolerance (< 1e-6 Å).
- All element symbols are recognized and map to valid periodic table entries.
- Extracted geometry object successfully instantiates QCxMS2 driver without coordinate validation errors.
- No NaN, infinite, or corrupt coordinate values are present in parsed output.
- Intermolecular distances are chemically reasonable (e.g., no atoms overlapping at < 0.5 Å, standard bond lengths preserved).

## Limitations

- Parser assumes XYZ or equivalent Cartesian coordinate format; non-standard or proprietary geometry formats will fail without prior conversion.
- Validation checks basic structural sanity (numeric coordinates, recognized elements) but do not guarantee chemical reasonableness (e.g., unphysical bond angles or strained ring systems may parse successfully).
- Large molecular structures (>1000 atoms) may incur parsing overhead; performance not characterized in the article.
- Parser does not infer missing explicit hydrogens; input file must include all atoms for complete representation.

## Evidence

- [other] Parse and validate the input molecular geometry file (XYZ or equivalent format).: "Parse and validate the input molecular geometry file (XYZ or equivalent format)."
- [other] Initialize QCxMS2 driver with molecular structure and reaction network parameters.: "Initialize QCxMS2 driver with molecular structure and reaction network parameters."
- [readme] Program package for the quantum mechanical calculation of EI mass spectra using automated reaction network exploration: "Program package for the quantum mechanical calculation of EI mass spectra using automated reaction network exploration"
