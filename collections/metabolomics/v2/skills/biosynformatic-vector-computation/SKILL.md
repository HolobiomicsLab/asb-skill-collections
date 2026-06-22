---
name: biosynformatic-vector-computation
description: Use when you have a natural product molecule structure in SMILES, InChI, or SDF format and need to convert it into a fixed-length numerical vector representation (fingerprint) that preserves biosynthetic and chemical information for machine learning, similarity searching, or class prediction tasks.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0292
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3391
  tools:
  - pip
  - biosynfoni
  - RDKit
  - black
  - pytest
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

# biosynformatic-vector-computation

## Summary

Encode natural product molecular structures into biosynformatic fingerprint vectors—count-based representations that capture biosynthetic logic and chemical features tailored to natural product chemistry. Use this skill when you need a machine-readable molecular descriptor optimized for downstream biosynthetic class prediction or chemical similarity analysis.

## When to use

You have a natural product molecule structure in SMILES, InChI, or SDF format and need to convert it into a fixed-length numerical vector representation (fingerprint) that preserves biosynthetic and chemical information for machine learning, similarity searching, or class prediction tasks.

## When NOT to use

- Input is a raw molecular formula (e.g., 'C6H12O6') without structural connectivity information—requires 2D or 3D structure.
- Target is synthetic (non-natural) compound chemistry where biosynthetic feature encoding is not informative.
- Fingerprint output is already available and you need dimension reduction or alternative encodings instead.

## Inputs

- SMILES string
- InChI string
- SDF file (molecule supplier)
- RDKit Mol object

## Outputs

- biosynformatic count fingerprint vector
- numerical array representation of molecular features

## How to apply

Install biosynfoni from PyPI (requires Python 3.9+; RDKit installs automatically as a dependency). Parse the input molecule structure using RDKit's Chem.MolFromSmiles(), Chem.MolFromInChI(), or Chem.SDMolSupplier() depending on input format. Instantiate the Biosynfoni class with the parsed molecule object and extract the .fingerprint attribute, which returns a count-based fingerprint vector. The fingerprint encodes biosynthetic and chemical features specific to natural product structures. Validate the output by confirming the fingerprint is a non-empty numerical vector suitable for downstream analysis (e.g., classifier input, similarity computation).

## Related tools

- **biosynfoni** (Primary package implementing biosynformatic fingerprint encoding; provides Biosynfoni class and CLI for SMILES/InChI/SDF input conversion to count fingerprints) — https://github.com/lucinamay/biosynfoni
- **RDKit** (Dependency for parsing and handling molecular structures (SMILES, InChI, SDF); installed automatically with biosynfoni)
- **black** (Code formatting tool used in biosynfoni development; recommended for code quality in reproduction or extension work) — https://github.com/psf/black
- **pytest** (Testing framework for validating fingerprint computations and package correctness)

## Examples

```
from biosynfoni import Biosynfoni
from rdkit import Chem
mol = Chem.MolFromSmiles('CC(=O)Oc1ccccc1C(=O)O')
fp = Biosynfoni(mol).fingerprint
```

## Evaluation signals

- Output fingerprint is a non-empty numerical vector (count-based format) with consistent dimensionality across multiple molecules
- Fingerprint can be serialized to CSV or compared between structurally similar molecules with expected similarity metrics
- Fingerprint successfully ingests into downstream biosynthetic class predictors (e.g., trained classifiers from Zenodo 14791239) without shape/type errors
- Molecules with identical SMILES produce identical fingerprints across multiple runs (determinism check)
- Command-line invocation (e.g., `biosynfoni <SMILES>`) produces human-readable or machine-parseable output without errors

## Limitations

- Requires valid, parseable input structures; malformed SMILES, InChI, or corrupted SDF files will cause failures.
- Fingerprint is optimized for natural products; application to synthetic or non-organic molecules may produce less informative encodings.
- No built-in dimensionality reduction or feature weighting; downstream analysis must handle high-dimensional or sparse vectors.
- Large SDF files require sequential processing; memory constraints may apply for very large molecular datasets.

## Evidence

- [readme] biosynfoni is a biosynformatic molecular fingerprint tailored to natural product chem- and bioinformatic research: "a biosynformatic molecular fingerprint tailored to natural product chem- and bioinformatic research"
- [readme] Python package API usage to load molecules and compute fingerprints: "from biosynfoni import Biosynfoni
from rdkit import Chem

smi = <SMILES>
mol = Chem.MolFromSmiles(smi)
fp = Biosynfoni(mol).fingerprint"
- [readme] Multiple input format support via CLI and API: "Write the fingerprints of all molecules in an SDF file to a CSV file:

biosynfoni <molecule_supplier.sdf>"
- [readme] Package availability and installation: "biosynfoni is implemented as a Python package available on PyPI that provides a biosynformatic molecular fingerprint"
- [readme] Python version and dependency requirement: "Biosynfoni requires Python 3.9 or later. RDKit is installed as a dependency when installing Biosynfoni."
