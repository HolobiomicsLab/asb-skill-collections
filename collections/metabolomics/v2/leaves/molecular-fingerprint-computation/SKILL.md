---
name: molecular-fingerprint-computation
description: Use when you have natural product molecules (or compounds from natural
  product-like databases such as COCONUT or ZINC) in structural format (SMILES, InChI,
  or SDF file) and need a fingerprint representation optimized for biosynthetic-class
  prediction, structural clustering, or bioinformatic feature.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0564
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_2275
  tools:
  - biosynfoni
  - pip
  - RDKit
  - black
  - pytest
  - PubChemPy
  - Python
  - SIRIUS
  - MetFrag
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.26434/chemrxiv-2025-cwq74
  title: biosynfoni
- doi: 10.1186/s13321-023-00695-y
  title: ''
- doi: 10.1186/s12859-023-05149-8
  title: ''
evidence_spans:
- biosynfoni
- a biosynformatic molecular fingerprint tailored to natural product chem- and bioinformatic
  research
- pip install -e .[dev]
- Final candidate selection is done in Python using RDKit and PubChemPy
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_biosynfoni
    doi: 10.26434/chemrxiv-2025-cwq74
    title: biosynfoni
  - build: coll_maw_cq
    doi: 10.1186/s13321-023-00695-y
    title: MAW
  - build: coll_pickaxe_cq
    doi: 10.1186/s12859-023-05149-8
    title: Pickaxe
  dedup_kept_from: coll_biosynfoni
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.26434/chemrxiv-2025-cwq74
  all_source_dois:
  - 10.26434/chemrxiv-2025-cwq74
  - 10.1186/s13321-023-00695-y
  - 10.1186/s12859-023-05149-8
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-fingerprint-computation

## Summary

Compute biosynfoni fingerprints—a biosynformatic molecular representation tailored for natural product chemistry—from molecular structures (SMILES, InChI, or SDF) to generate bit-vector or count fingerprints suitable for downstream bioinformatic analysis and biosynthetic class prediction.

## When to use

Apply this skill when you have natural product molecules (or compounds from natural product-like databases such as COCONUT or ZINC) in structural format (SMILES, InChI, or SDF file) and need a fingerprint representation optimized for biosynthetic-class prediction, structural clustering, or bioinformatic feature extraction rather than generic chemical similarity.

## When NOT to use

- Input molecules are non-natural-product synthetics where generic molecular descriptors (Morgan fingerprints, ECFP) are expected to perform equally well or better.
- You require real-time or ultra-low-latency fingerprint computation on streaming data; biosynfoni involves RDKit dependency overhead.
- Your downstream task is docking or 3D shape-based screening where 2D fingerprints are insufficient.

## Inputs

- SMILES strings (individual or batch)
- InChI strings
- SDF file (molecular structure records)
- RDKit Mol objects

## Outputs

- Biosynfoni count fingerprints (numeric vectors)
- Biosynfoni bit-vector fingerprints
- CSV file with molecule IDs and fingerprint vectors
- NumPy .npy array (fingerprint matrix)

## How to apply

Install the biosynfoni package via pip (pip install biosynfoni), then load molecular structures using RDKit (Chem.MolFromSmiles or from an SDF file). For each molecule, instantiate the Biosynfoni class and extract the .fingerprint attribute, which returns either a count fingerprint or bit-vector representation. Batch processing is supported via the command-line tool for SDF inputs. The fingerprints encode biosynthetic information and biochemical logic specific to natural products, making them more discriminative than generic molecular fingerprints for downstream classification tasks. Export results as CSV (with molecule IDs and fingerprint vectors) or NumPy arrays (.npy) for further analysis.

## Related tools

- **biosynfoni** (Core package that computes biosynformatic fingerprints from molecular structures and provides command-line and Python API interfaces.) — https://github.com/lucinamay/biosynfoni
- **RDKit** (Dependency for parsing and manipulating molecular structures (SMILES, InChI, SDF); installed automatically with biosynfoni.)
- **pip** (Package installer used to install biosynfoni and its dependencies.)
- **black** (Code formatter for ensuring consistent style in development workflows; recommended for contributors.) — https://github.com/psf/black
- **pytest** (Testing framework for validating fingerprint computation correctness during development.)

## Examples

```
from biosynfoni import Biosynfoni
from rdkit import Chem
mol = Chem.MolFromSmiles('CC(=O)Oc1ccccc1C(=O)O')
fp = Biosynfoni(mol).fingerprint
```

## Evaluation signals

- Fingerprints are non-empty numeric vectors with expected dimensionality (consistent across molecules of a batch).
- CSV export contains all input molecule IDs paired with corresponding fingerprint vectors with no missing values.
- Fingerprints computed from identical molecules (via identical SMILES) are identical across runs (deterministic).
- Downstream biosynthetic class predictions using the fingerprints show improved accuracy over baseline fingerprints on the COCONUT or ZINC datasets (as reported in the biosynfoni publication).
- NumPy array export can be loaded and reshaped to (n_molecules × fingerprint_dim) without errors.

## Limitations

- Biosynfoni requires Python 3.9 or later and RDKit as a hard dependency; installation may be system-dependent.
- The fingerprint representation is optimized for natural products; its performance on non-natural-product molecules or highly synthetic scaffolds is not established.
- No changelog or version history is provided in the repository, limiting traceability of updates and breaking changes.
- Command-line tool behavior on malformed SMILES or InChI strings is not documented; invalid input handling should be tested.

## Evidence

- [readme] a biosynformatic molecular fingerprint tailored to natural product chem- and bioinformatic research: "a biosynformatic molecular fingerprint tailored to natural product chem- and bioinformatic research"
- [other] Install the package, load molecular structures, compute fingerprints using the biosynfoni API, and export as CSV or NumPy arrays: "Install the package in development mode using pip install -e .[dev] from the project root. Load molecular structures from the sample dataset (format and path to be specified by user). Compute"
- [readme] Convert a SMILES string to a fingerprint via Biosynfoni class: "from biosynfoni import Biosynfoni
from rdkit import Chem

smi = <SMILES>
mol = Chem.MolFromSmiles(smi)
fp = Biosynfoni(mol).fingerprint  # returns biosynfoni's count fingerprint of the molecule"
- [readme] biosynfoni fingerprints encode biosynthetic information and biochemical logic: "relating to biosynthetic information and biochemical logic.
as a concatenation of  biosynthetic and bioinformatics, it was coined
during the creation of `BioSynFoni`."
- [readme] Command-line support for batch SDF processing and export: "Write the fingerprints of all molecules in an SDF file to a CSV file:

```bash
biosynfoni <molecule_supplier.sdf>
```"
- [readme] RDKit is installed as a dependency when installing Biosynfoni: "Biosynfoni requires Python 3.9 or later. RDKit is installed as a dependency when installing Biosynfoni."
- [readme] Data sourced from COCONUT and ZINC databases for manuscript validation: "We have used data from the COCONUT natural product database and ZINC compound database. The parsed data used for the analysis in our manuscript can be downloaded from Zenodo"
