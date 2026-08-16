---
name: quantum-chemistry-structure-preparation
description: Use when when you have a collection of N-Me derived unsaturated sterol
  lipid identifiers or structures and need to generate predicted collision cross section
  (CCS) values for LC-IM-MS/MS analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0335
  edam_topics:
  - http://edamontology.org/topic_3314
  - http://edamontology.org/topic_3372
  tools:
  - Python
  - Jupyter Notebook
  - RDKit
  techniques:
  - LC-MS
  - ion-mobility-MS
  license_tier: restricted
derived_from:
- doi: 10.1002/anie.202507483
  title: NA
evidence_spans:
- collection of Python scripts
- All functions are implemented in jupyter notebook
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_na_cq
    doi: 10.1002/anie.202507483
    title: NA
  dedup_kept_from: coll_na_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1002/anie.202507483
  all_source_dois:
  - 10.1002/anie.202507483
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# quantum-chemistry-structure-preparation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Preparation of structural input data (SMILES or molecular geometry files) for N-Me derived unsaturated sterol lipids prior to quantum chemistry calculations. This upstream step ensures molecular representations are standardized and computationally compatible for CCS prediction via 3D conformational and electronic structure modeling.

## When to use

When you have a collection of N-Me derived unsaturated sterol lipid identifiers or structures and need to generate predicted collision cross section (CCS) values for LC-IM-MS/MS analysis. Specifically, use this skill as the first step of the QCC-assisted CCS prediction workflow, before executing quantum chemistry calculations and machine-learning CCS model inference.

## When NOT to use

- Structures are already in a validated, standardized format and have passed consistency checks.
- You are working with saturated (non-unsaturated) sterol lipids; the workflow is specifically designed for N-Me derived unsaturated variants.
- You are beginning at a later stage (e.g., you already have computed quantum chemistry features or CCS predictions) and do not need to re-prepare structural inputs.

## Inputs

- N-Me derived unsaturated sterol lipid identifiers (list or table)
- SMILES strings or molecular geometry files (PDB, MOL2, XYZ) for each lipid
- structural isomer classification or annotation (e.g., double-bond position)

## Outputs

- standardized structural input dataset indexed by lipid identifier
- metadata table linking lipid ID, SMILES/geometry file, and isomer class
- validated molecular structures ready for quantum chemistry input

## How to apply

Collect or enumerate all N-Me derived unsaturated sterol lipid structures in your analysis set, then convert each to a machine-readable structural representation—either SMILES strings (for simplicity) or 3D molecular geometry files (PDB, MOL2, or XYZ format for fidelity). Validate structural formats for consistency (e.g., all SMILES are canonical, all geometry files contain valid atomic coordinates and connectivity). Index each prepared structure by a unique lipid identifier and structural isomer class (e.g., position of double bonds). This preparation ensures that downstream quantum chemistry solvers receive well-formed, unambiguous molecular input and that predicted CCS values can be reliably traced back to their source lipid.

## Related tools

- **RDKit** (Molecular structure parsing, SMILES canonicalization, and 3D coordinate generation for N-Me derived sterol lipids)
- **Python** (Script language for automated batch preparation of structural data and metadata indexing)
- **Jupyter Notebook** (Interactive environment for exploratory structure validation and preparation workflow implementation) — https://github.com/Chen-micslab/QCCAssisted4DSterol

## Evaluation signals

- All SMILES strings are parseable by RDKit and round-trip to the same canonical form.
- All molecular geometry files contain valid atomic coordinates with no missing or duplicate atoms.
- Each lipid identifier maps to exactly one structure and one isomer class; no duplicates or orphaned entries.
- Structural representations preserve double-bond positions and N-Me substituent patterns as documented.
- Downstream quantum chemistry calculations accept all prepared structures without parsing errors.

## Limitations

- The workflow is tested and documented only for N-Me derived unsaturated sterol lipids; applicability to other lipid classes or non-methylated variants is not confirmed.
- SMILES representation alone may not capture all stereochemical information; 3D geometry files are recommended for high-fidelity conformational input.
- Preparation does not validate against experimental or reference CCS standards; validation occurs only after quantum chemistry and CCS prediction steps.

## Evidence

- [other] 1. Prepare structural input data for N-Me derived unsaturated sterol lipids (SMILES or molecular geometry files).: "Prepare structural input data for N-Me derived unsaturated sterol lipids (SMILES or molecular geometry files)"
- [readme] The script is written on the basis of RDkit's built-in functions.: "The script is written on the basis of RDkit's built-in functions"
- [other] Compile predicted CCS values into a tabular dataset indexed by lipid identifier and structural isomer class.: "Compile predicted CCS values into a tabular dataset indexed by lipid identifier and structural isomer class"
- [readme] All functions are implemented in jupyter notebook: "All functions are implemented in jupyter notebook"
