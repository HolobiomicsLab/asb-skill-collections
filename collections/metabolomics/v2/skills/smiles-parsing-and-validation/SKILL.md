---
name: smiles-parsing-and-validation
description: Use when you have SMILES strings for candidate novel psychoactive substance structures and need to convert them into a machine-readable molecular representation before computing descriptors, generating mass spectra, or calculating chemical fingerprints.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3929
  edam_topics:
  - http://edamontology.org/topic_0176
  - http://edamontology.org/topic_3314
  tools:
  - RDKit
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1021/acs.analchem.3c05019
  title: ps2ms
evidence_spans:
- jhhung/PS2MS
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ps2ms
    doi: 10.1021/acs.analchem.3c05019
    title: ps2ms
  dedup_kept_from: coll_ps2ms
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c05019
  all_source_dois:
  - 10.1021/acs.analchem.3c05019
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# SMILES Parsing and Validation

## Summary

Convert SMILES strings representing chemical structures into validated canonical molecule objects using RDKit, ensuring structural correctness before downstream feature encoding. This is a foundational step in computational chemistry workflows where chemical identity must be unambiguously resolved before mass spectrum prediction or fingerprint generation.

## When to use

You have SMILES strings for candidate novel psychoactive substance structures and need to convert them into a machine-readable molecular representation before computing descriptors, generating mass spectra, or calculating chemical fingerprints. Apply this skill whenever raw chemical identity data (SMILES format) must be validated and standardized prior to deep learning feature extraction or similarity matching.

## When NOT to use

- SMILES strings have already been validated and canonicalized in an upstream step.
- Input is a pre-built RDKit molecule object or molecular graph structure (no parsing needed).
- Chemical structures are represented in other formats (InChI, MOL, PDB) that do not require SMILES-specific parsing.

## Inputs

- SMILES strings (from file, list, or database)
- RDKit molecular toolkit

## Outputs

- Validated canonical SMILES strings
- RDKit molecule objects (Mol type)
- Log of failed/invalid SMILES (optional)

## How to apply

Load SMILES strings from an input file (e.g., CSV, text list, or database). Use RDKit's SMILES parser to generate canonical molecule objects, which simultaneously validates syntax and resolves aromaticity. Canonicalization ensures that different SMILES representations of the same molecule (e.g., 'c1ccccc1' vs. '[c]1[c][c][c][c][c]1' for benzene) map to a single standard form, preventing duplicate entries in synthetic NPS databases. Reject any SMILES that fail to parse (RDKit returns None), and log these as invalid structures. For valid molecules, retain the canonical SMILES and the parsed molecule object for subsequent steps (descriptor extraction, fingerprint computation, or mass spectrum prediction). The rationale is that canonical SMILES ensures consistency across the synthetic database enumeration and mass spectrometry matching pipeline, reducing false positives in NPS identification.

## Related tools

- **RDKit** (Parses and validates SMILES strings into canonical molecule objects; extracts molecular descriptors and structural features (atom types, bond connectivity, graph topology) required by PS2MS architecture) — https://www.rdkit.org/docs/Install.html

## Evaluation signals

- All input SMILES either successfully parse and return a valid RDKit Mol object, or are logged as parse failures with the original SMILES string.
- Canonical SMILES are deterministic: running the same input twice produces identical canonical SMILES strings.
- Different SMILES representations of the same molecule (e.g., reordered atoms, different aromaticity notation) resolve to the same canonical SMILES.
- Parsed molecule objects contain consistent structural properties: molecular formula, atom count, bond count, and formal charge match expectations for the input structure.
- No silent failures: molecules that chemically violate valence rules or contain unsupported atoms are rejected with clear error messages, not silently passed through.

## Limitations

- RDKit's SMILES parser may not recognize non-standard or obsolete SMILES notation; custom preprocessing may be required for unusual chemical representations.
- Canonicalization can be computationally expensive for very large synthetic databases with millions of enumerated derivatives; batch processing or caching is recommended.
- SMILES strings do not encode 3D stereochemistry or conformational properties; 2D graph topology alone cannot distinguish all relevant isomers (e.g., some tautomers).
- The README specifies that RDKit must be 'build from the source and install python package from conda', indicating potential build complexity or version-specific dependencies.

## Evidence

- [other] Parse and validate SMILES using RDKit molecular toolkit to generate canonical molecule objects.: "Parse and validate SMILES using RDKit molecular toolkit to generate canonical molecule objects."
- [readme] RDKit is required and must be built from source and installed via conda for compatibility with the enumeration and deep learning steps.: "[rdkit](https://www.rdkit.org/docs/Install.html)
  - build the c++ code from the source and install python package from conda"
- [other] Extracted features include atom types, bond connectivity, and graph topology required by the PS2MS architecture.: "Extract molecular descriptors and structural features (atom types, bond connectivity, graph topology) required by PS2MS architecture."
- [readme] PS2MS builds a synthetic NPS database by enumerating possible derivatives based on core structure, requiring structural validation of input SMILES.: "PS2MS builds a synthetic NPS database by enumerating possible derivatives based on the core structure of a preselected illicit drug."
