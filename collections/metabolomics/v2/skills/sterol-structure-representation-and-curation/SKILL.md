---
name: sterol-structure-representation-and-curation
description: Use when when you have a collection of N-Me derivatized unsaturated sterol structures from tissue samples or standards that must be fed into MS/MS fragmentation prediction or collision cross section (CCS) prediction workflows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0154
  tools:
  - Python
  - Jupyter Notebook
  - RDKit
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
---

# sterol-structure-representation-and-curation

## Summary

Represent N-Me derived unsaturated sterol lipid structures as SMILES strings or molecular formulas, and curate them for downstream quantum chemistry and MS/MS fragmentation prediction. This skill ensures consistent, machine-readable encoding of sterol isomers and their double-bond positions for automated analysis pipelines.

## When to use

When you have a collection of N-Me derivatized unsaturated sterol structures from tissue samples or standards that must be fed into MS/MS fragmentation prediction or collision cross section (CCS) prediction workflows. Use this skill if your input is a mixture of structural formats (chemical names, drawings, molecular formulas) and you need normalized, queryable representations that preserve double-bond regiochemistry.

## When NOT to use

- Structures are already in validated SMILES format with confirmed double-bond regiochemistry and you are ready to apply MS/MS calculations immediately.
- Input lipids lack C=C bonds or are saturated sterols (the method is documented as theoretically applicable to all molecules with C=C, but testing is limited to unsaturated sterol lipids).
- You are working with non-N-Me derivatized sterol lipids; the fragmentation patterns and workflow are specifically designed for N-Me derivatives.

## Inputs

- Sterol lipid structure identifiers (chemical names, PubChem IDs, or manual drawings)
- N-Me derivatization state annotation
- Double-bond position assignments (e.g., Δ5, Δ7, Δ24)
- Molecular formula or partial structure data

## Outputs

- Curated SMILES string table indexed by lipid identifier
- Molecular formula registry with N-Me and double-bond annotations
- Structured input CSV/JSON file compatible with RDKit-based MS/MS calculation scripts
- Quality report documenting double-bond position recognition by RDKit

## How to apply

Convert input sterol structures to SMILES or molecular formula format, ensuring that N-methyl derivatization and all C=C double-bond positions are explicitly encoded. Load structures into RDKit-compatible data structures within a Python/Jupyter environment. Validate that double-bond positions are recognized and preserved by RDKit's built-in functions, since downstream MS/MS fragmentation relies on accurate position annotation. Organize curated structures into a structured input table (CSV or JSON) with lipid identifiers, SMILES/formula strings, and metadata (tissue source, derivatization state). Export this table for downstream MS/MS calculation and CCS prediction steps.

## Related tools

- **RDKit** (Structure parsing, double-bond position recognition, and SMILES validation for N-Me sterol lipids)
- **Python** (Scripting environment for structure curation and SMILES generation)
- **Jupyter Notebook** (Interactive development and documentation of sterol structure curation workflows) — github.com/Chen-micslab/QCCAssisted4DSterol

## Evaluation signals

- All curated SMILES strings parse without error in RDKit and preserve N-methyl and double-bond annotations.
- Double-bond positions inferred by RDKit match manual annotations or reference standards (100% agreement or documented exceptions).
- Curated structure table has no missing identifiers, SMILES, or derivatization metadata; all rows are complete and non-redundant.
- Exported CSV/JSON can be successfully loaded by downstream MS/MS calculation functions without conversion errors.
- Visual inspection or structural similarity checks confirm that SMILES-encoded isomers are distinct (e.g., Δ5 vs. Δ7 sterols produce different RDKit substructure hashes).

## Limitations

- The method relies on RDKit's built-in double-bond recognition; manually drawn or ambiguous structural inputs may require manual curation before automated processing.
- Testing has been limited to sterol lipids; applicability to other unsaturated lipid classes (e.g., polyunsaturated fatty acyl chains) is theoretical and untested.
- SMILES and molecular formula representations do not encode 3D stereochemistry or ring geometry; structures are treated as 2D graphs, which may lose spatial information relevant to some fragmentation pathways.
- N-Me derivatization must be explicitly represented in the SMILES string; failure to do so will cause downstream MS/MS fragmentation predictions to be incorrect.

## Evidence

- [other] Load input lipid structure data (SMILES or molecular formula) for N-Me derivatized unsaturated sterols.: "Load input lipid structure data (SMILES or molecular formula) for N-Me derivatized unsaturated sterols"
- [readme] The script recognises double bond positions and generates MS/MS based on N-Me fragmentation patterns.: "The script  recognises double bond positions and generates MS/MS based on N-Me fragmentation patterns"
- [readme] Theoretically applicable to all molecules including C=C bond (only test sterol lipids).: "Theoretically applicable to all molecules including C=C bond  (only test sterol lipids)"
- [readme] All functions are implemented in jupyter notebook: "All functions are implemented in jupyter notebook"
- [readme] The script is written on the basis of RDkit's built-in functions.: "The script is written on the basis of RDkit's built-in functions"
