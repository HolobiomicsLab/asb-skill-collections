---
name: cheminformatic-feature-representation
description: Use when when you have natural product structures in SMILES, InChI, or
  SDF format and need to convert them into numerical feature vectors for downstream
  tasks such as biosynthetic class prediction, molecular similarity analysis, or machine
  learning-based natural product classification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0337
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0601
  tools:
  - pip
  - biosynfoni
  - RDKit
  - black
  - pytest
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.26434/chemrxiv-2025-cwq74
  title: biosynfoni
evidence_spans:
- pip install -e .[dev]
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_biosynfoni_2_cq
    doi: 10.26434/chemrxiv-2025-cwq74
    title: biosynfoni
  dedup_kept_from: coll_biosynfoni_2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.26434/chemrxiv-2025-cwq74
  all_source_dois:
  - 10.26434/chemrxiv-2025-cwq74
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# cheminformatic-feature-representation

## Summary

Convert natural product molecule structures (SMILES, InChI, or SDF) into biosynformatic molecular fingerprint vector representations that encode biosynthetic information for machine learning and structural analysis. This skill bridges molecular chemistry and bioinformatic data representation for natural product research.

## When to use

When you have natural product structures in SMILES, InChI, or SDF format and need to convert them into numerical feature vectors for downstream tasks such as biosynthetic class prediction, molecular similarity analysis, or machine learning-based natural product classification. Apply this skill before training predictive models or conducting comparative analyses that require fixed-dimensional molecular representations.

## When NOT to use

- Input molecules are synthetic chemicals from non-biological sources where biosynthetic pathway information is not relevant.
- You require generic molecular fingerprints (e.g., Morgan, MACCS keys) optimized for small-molecule screening rather than natural product-specific features.
- Your input is already in pre-computed fingerprint or feature vector format — skip directly to downstream modeling.

## Inputs

- SMILES string (molecular structure notation)
- InChI string (molecular structure notation)
- SDF file (multi-molecule structure file)
- RDKit Mol object

## Outputs

- biosynfoni count fingerprint vector (numerical array)
- CSV file of fingerprints (for batch processing)
- Biosynthetic feature encoding

## How to apply

Install biosynfoni from PyPI and load your natural product molecule structure using RDKit's Chem.MolFromSmiles(), Chem.MolFromInchi(), or SDF suppliers. Call the Biosynfoni class on the RDKit molecule object and access the .fingerprint attribute to obtain a count-based biosynformatic fingerprint vector. The fingerprint encodes biosynthetic structural features tailored to natural products rather than generic molecular features. For batch processing of SDF files, use the command-line tool to write fingerprints directly to CSV. Validate output by confirming fingerprint vector dimensionality and checking that count values reflect the presence and multiplicity of biosynthetic motifs in your molecules.

## Related tools

- **biosynfoni** (Python package that computes the biosynformatic molecular fingerprint vector from molecule objects) — https://github.com/lucinamay/biosynfoni
- **RDKit** (Cheminformatics library used to parse and manipulate SMILES, InChI, and SDF molecule structures before fingerprinting)
- **black** (Code formatter for development and contribution workflows) — https://github.com/psf/black
- **pytest** (Testing framework for validating fingerprint computation correctness)

## Examples

```
from biosynfoni import Biosynfoni
from rdkit import Chem
mol = Chem.MolFromSmiles('CC(=O)Oc1ccccc1C(=O)O')
fp = Biosynfoni(mol).fingerprint
```

## Evaluation signals

- Fingerprint vector has consistent dimensionality across all input molecules (no missing or ragged outputs).
- Fingerprint count values are non-negative integers reflecting the multiplicity of biosynthetic motifs.
- Structurally similar natural products yield similar fingerprint vectors (visual inspection via cosine similarity or clustering validation).
- Batch SDF processing completes without errors and output CSV dimensions match the number of input molecules and expected fingerprint features.
- Command-line and Python API invocations produce identical fingerprints for the same input molecule.

## Limitations

- Fingerprint is optimized for natural products and may not generalize well to synthetic chemicals or non-biological molecules.
- Requires RDKit to be installed as a dependency; molecules with ambiguous or invalid SMILES/InChI will fail to parse.
- No changelog is maintained in the repository, limiting traceability of feature changes across versions.
- Fingerprint interpretation requires domain knowledge of biosynthetic pathways and natural product chemistry to extract actionable insights.

## Evidence

- [readme] biosynfoni is a biosynformatic molecular fingerprint tailored to natural product chem- and bioinformatic research: "a biosynformatic molecular fingerprint tailored to natural product chem- and bioinformatic research"
- [readme] Biosynfoni requires Python 3.9 or later. RDKit is installed as a dependency when installing Biosynfoni.: "Biosynfoni requires Python 3.9 or later. RDKit is installed as a dependency when installing Biosynfoni."
- [readme] Convert a SMILES string to a fingerprint: from biosynfoni import Biosynfoni; from rdkit import Chem; smi = <SMILES>; mol = Chem.MolFromSmiles(smi); fp = Biosynfoni(mol).fingerprint: "Convert a SMILES string to a fingerprint: from biosynfoni import Biosynfoni from rdkit import Chem smi = <SMILES> mol = Chem.MolFromSmiles(smi) fp = Biosynfoni(mol).fingerprint"
- [other] Load a natural-product molecule structure from SMILES or SDF input using the biosynfoni API. Compute the biosynformatic molecular fingerprint vector encoding via the biosynfoni fingerprint function.: "Load a natural-product molecule structure from SMILES or SDF input using the biosynfoni API. Compute the biosynformatic molecular fingerprint vector encoding via the biosynfoni fingerprint function."
- [readme] Write the fingerprints of all molecules in an SDF file to a CSV file: biosynfoni <molecule_supplier.sdf>: "Write the fingerprints of all molecules in an SDF file to a CSV file: biosynfoni <molecule_supplier.sdf>"
