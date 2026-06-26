---
name: molecular-descriptor-calculation
description: Use when you have raw molecular structures in SMILES or SDF format and
  need to prepare them as input for BitterPredict.m or similar descriptor-based classifiers.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3778
  edam_topics:
  - http://edamontology.org/topic_3314
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3373
  tools:
  - BitterPredict
  - RDKit
  - BitterPredict.m
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jafc.3c09767
  title: bittermass
evidence_spans:
- BitterPredict is a classifier which predicts whether a compound is bitter or not,
  based on its chemical structure.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_bittermass
    doi: 10.1021/acs.jafc.3c09767
    title: bittermass
  dedup_kept_from: coll_bittermass
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jafc.3c09767
  all_source_dois:
  - 10.1021/acs.jafc.3c09767
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-descriptor-calculation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Convert raw molecular structures (SMILES or SDF format) into computed chemical descriptor tables suitable for machine-learning classifiers like BitterPredict. This skill bridges raw chemical representations and descriptor-based prediction by parsing, validating, computing standardized molecular properties, and assembling them into tabular format.

## When to use

You have raw molecular structures in SMILES or SDF format and need to prepare them as input for BitterPredict.m or similar descriptor-based classifiers. The classifier requires pre-computed molecular descriptors organized as rows (molecules) × columns (descriptor features) in CSV or Excel format, and you must construct this descriptor table from structure data.

## When NOT to use

- Input is already a computed descriptor table or CSV/Excel file with descriptors present—skip directly to classifier execution.
- Molecular structures are already validated and descriptors pre-computed—proceed to BitterPredict classification.
- Input is in a non-molecular format (e.g., sequence, image, time-series data) without cheminformatics interpretation.

## Inputs

- SMILES string file or list
- SDF (structure data format) file
- Raw molecular structure representations

## Outputs

- CSV file containing molecular descriptors (molecules × descriptor columns)
- Excel file containing molecular descriptors
- Validated descriptor table with molecule identifiers and feature columns

## How to apply

Load raw molecular structures in SMILES or SDF format and parse them using a cheminformatics parser (e.g., RDKit) to validate syntax and build in-memory molecular objects. Calculate the complete set of molecular descriptors required by BitterPredict.m from each validated structure—this typically includes molecular weight, lipophilicity, topological, and pharmacophoric descriptors organized into functionally coherent subgroups. Assemble the computed descriptors into a structured table with molecules as rows and descriptor columns as specified by BitterPredict.m's input schema. Export the descriptor table to CSV or Excel format compatible with BitterPredict.m input specification. Validate the output by spot-checking descriptor ranges and verifying no missing values exist in the feature matrix.

## Related tools

- **RDKit** (Cheminformatics parser for validating molecular structure syntax, parsing SMILES/SDF, and computing molecular descriptors from validated structures)
- **BitterPredict.m** (Downstream classifier that consumes the descriptor table output by this skill to generate bitter/not-bitter predictions) — https://github.com/Niv-Lab/BitterPredict1

## Evaluation signals

- Output CSV/Excel file has no missing values in any descriptor column and each row corresponds to a unique molecule with a valid identifier.
- Descriptor columns align with BitterPredict.m's input specification as documented in the BitterPredict.m file—verify column names and count match expected schema.
- Descriptor values fall within chemically plausible ranges (e.g., molecular weight > 0, lipophilicity typically −5 to +10, topological descriptors non-negative integers).
- Spot-check 5–10 molecules: manually verify descriptor values are consistent with their chemical structures (e.g., a heavy molecule should have high molecular weight descriptor).
- Input structure file and output descriptor file have the same molecule count and identifiers are preserved in the same order.

## Limitations

- Descriptor calculation depends on the cheminformatics parser's accuracy; invalid or malformed SMILES/SDF entries may fail to parse or produce spurious descriptors.
- The 'complete set of molecular descriptors required by BitterPredict.m' is documented within BitterPredict.m itself; external descriptor specification is not provided in the paper, requiring consultation of the code.
- Descriptor subgroups (molecular weight, lipophilicity, topological, pharmacophoric) are functionally coherent but their exact composition and calculation method are not detailed in the paper.

## Evidence

- [other] Load raw molecular structures in SMILES or SDF format. Parse and validate molecular structure syntax using a cheminformatics parser (e.g., RDKit).: "Load raw molecular structures in SMILES or SDF format. Parse and validate molecular structure syntax using a cheminformatics parser (e.g., RDKit)."
- [other] Calculate the complete set of molecular descriptors required by BitterPredict.m from the validated structures. Assemble descriptors into a structured table with molecules as rows and descriptor columns as required.: "Calculate the complete set of molecular descriptors required by BitterPredict.m from the validated structures. Assemble descriptors into a structured table with molecules as rows and descriptor"
- [other] Export the descriptor table to CSV or Excel format compatible with BitterPredict.m input specification.: "Export the descriptor table to CSV or Excel format compatible with BitterPredict.m input specification."
- [readme] BitterPredict.m gets as input CSV or EXCEL files with required descriptors of molecules: "BitterPredict.m gets as input CSV or EXCEL files with required descriptors of molecules"
- [other] details on descriptor specification and preparation workflow are documented within the BitterPredict.m file itself.: "details on descriptor specification and preparation workflow are documented within the BitterPredict.m file itself."
