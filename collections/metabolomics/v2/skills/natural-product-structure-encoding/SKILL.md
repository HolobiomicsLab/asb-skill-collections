---
name: natural-product-structure-encoding
description: Use when you have natural product molecules in SMILES, InChI, or SDF
  format and need to convert them into fixed-length numerical feature vectors for
  downstream machine learning tasks (e.g., biosynthetic class prediction, molecular
  similarity analysis, or chemical space exploration).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3674
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3407
  tools:
  - pip
  - biosynfoni
  - RDKit
  - black
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

# natural-product-structure-encoding

## Summary

Encode natural product molecular structures (from SMILES, InChI, or SDF formats) into biosynformatic fingerprint vectors tailored for biosynthetic class prediction and bioinformatic research. This skill converts chemical structure notation into machine-readable count fingerprints that capture biosynthetic information.

## When to use

Apply this skill when you have natural product molecules in SMILES, InChI, or SDF format and need to convert them into fixed-length numerical feature vectors for downstream machine learning tasks (e.g., biosynthetic class prediction, molecular similarity analysis, or chemical space exploration). Use it as a preprocessing step before training or applying biosynthetic classifiers.

## When NOT to use

- Input molecules are already represented as fingerprints or feature vectors (avoid double-encoding)
- Molecules are synthetic compounds or non-natural products outside the domain biosynfoni was trained on (COCONUT and ZINC databases)
- You require fingerprints optimized for 2D similarity search or molecular docking rather than biosynthetic classification

## Inputs

- SMILES string (chemical structure notation)
- InChI string (International Chemical Identifier)
- SDF file (Structure Data File containing multiple molecules)
- RDKit Mol object (parsed molecular structure)

## Outputs

- biosynfoni count fingerprint vector (1D numerical array)
- CSV file with fingerprints for multiple molecules

## How to apply

Install biosynfoni via pip, then load a molecule structure using RDKit's Chem.MolFromSmiles(), Chem.MolFromInchi(), or SDF suppliers. Pass the parsed RDKit molecule object to the Biosynfoni class and access the .fingerprint attribute to obtain the count fingerprint vector. For batch processing, iterate over all molecules in an SDF file and write the resulting fingerprints to CSV. The biosynformatic encoding captures biosynthetic logic encoded into the fingerprint design; verify output by checking fingerprint dimensionality consistency and that all values are non-negative counts.

## Related tools

- **biosynfoni** (Generates biosynformatic molecular fingerprint vectors from natural product structures) — https://github.com/lucinamay/biosynfoni
- **RDKit** (Parses and converts chemical structure formats (SMILES, InChI, SDF) into Mol objects for biosynfoni)
- **pip** (Package manager for installing biosynfoni and dependencies)
- **black** (Code formatter for development workflows (optional for reproducibility)) — https://github.com/psf/black

## Examples

```
from biosynfoni import Biosynfoni
from rdkit import Chem

smi = "CC(=O)Oc1ccccc1C(=O)O"
mol = Chem.MolFromSmiles(smi)
fp = Biosynfoni(mol).fingerprint
```

## Evaluation signals

- Fingerprint vector has consistent dimensionality across all input molecules (no shape mismatches)
- All fingerprint values are non-negative integers (count fingerprint constraint)
- Command-line and Python API produce identical fingerprints for the same molecule
- Batch processing of SDF file produces a CSV with one row per molecule and one column per fingerprint dimension
- Fingerprints can be used as input to a trained biosynthetic class predictor without preprocessing errors

## Limitations

- biosynfoni fingerprints are designed and validated on natural products from COCONUT and ZINC databases; performance on out-of-domain synthetic or highly modified structures is not characterized
- The fingerprint encoding is deterministic but the underlying biosynthetic heuristics are implicit in the fingerprint design and not directly interpretable
- No changelog is publicly available, limiting visibility into API stability or breaking changes across versions
- Python 3.9+ required; RDKit dependency adds system-level C++ compilation requirements on some platforms

## Evidence

- [readme] biosynfoni is a biosynformatic molecular fingerprint tailored to natural product chem- and bioinformatic research: "a biosynformatic molecular fingerprint tailored to natural product chem- and bioinformatic research"
- [other] biosynfoni is implemented as a Python package available on PyPI that provides a biosynformatic molecular fingerprint: "biosynfoni is implemented as a Python package available on PyPI that provides a biosynformatic molecular fingerprint tailored to natural product chemistry and bioinformatic research applications"
- [readme] Convert a SMILES string to a fingerprint via RDKit Mol object and Biosynfoni class: "Convert a SMILES string to a fingerprint: from biosynfoni import Biosynfoni; smi = <SMILES>; mol = Chem.MolFromSmiles(smi); fp = Biosynfoni(mol).fingerprint"
- [readme] Command-line usage for single molecules and batch SDF processing: "Create a fingerprint from an InChI string: biosynfoni <InChI>. Write the fingerprints of all molecules in an SDF file to a CSV file: biosynfoni <molecule_supplier.sdf>"
- [readme] Data sourced from COCONUT and ZINC databases for training: "We have used data from the COCONUT natural product database and ZINC compound database. The parsed data used for the analysis in our manuscript can be downloaded from Zenodo"
- [readme] Installation via pip with development mode support: "To install the package, you can use pip: pip install biosynfoni. Biosynfoni requires Python 3.9 or later. RDKit is installed as a dependency"
