---
name: natural-product-chemical-representation
description: Use when you have a set of natural product molecules (or suspected natural products) in SMILES, InChI, or SDF format and need a chemical representation suitable for biosynthetic classification, structural screening, or machine learning tasks where standard generic fingerprints (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0291
  edam_topics:
  - http://edamontology.org/topic_3174
  - http://edamontology.org/topic_0209
  - http://edamontology.org/topic_3407
  tools:
  - biosynfoni
  - pip
  - RDKit
  - black
  - pytest
derived_from:
- doi: 10.26434/chemrxiv-2025-cwq74
  title: biosynfoni
evidence_spans:
- biosynfoni
- a biosynformatic molecular fingerprint tailored to natural product chem- and bioinformatic research
- pip install -e .[dev]
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_biosynfoni
    doi: 10.26434/chemrxiv-2025-cwq74
    title: biosynfoni
  dedup_kept_from: coll_biosynfoni
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

# natural-product-chemical-representation

## Summary

Compute biosynfoni fingerprints—a molecular representation tailored specifically for natural product chemistry and bioinformatic analysis—that encode biosynthetic structural features distinct from generic molecular descriptors. Use this skill when you need a feature representation of natural product molecules optimized for downstream biosynthetic class prediction, chemical similarity search, or machine learning on natural product datasets.

## When to use

You have a set of natural product molecules (or suspected natural products) in SMILES, InChI, or SDF format and need a chemical representation suitable for biosynthetic classification, structural screening, or machine learning tasks where standard generic fingerprints (e.g., ECFP) do not capture biosynthetic logic specific to natural product scaffolds and transformations.

## When NOT to use

- Input molecules are synthetic compounds with no natural product ancestry or biosynthetic relevance; consider generic molecular fingerprints (ECFP, MACCS) instead.
- You need real-time fingerprint computation on very large chemical libraries (>1 million molecules) without parallelization infrastructure; biosynfoni may have latency constraints.
- Your downstream task requires human-interpretable chemical features or explicit substructure annotations; biosynfoni fingerprints are latent bit-vectors.

## Inputs

- SMILES strings
- InChI strings
- SDF molecular structures file
- RDKit Mol objects

## Outputs

- biosynfoni count fingerprints (bit-vectors)
- CSV file with molecule IDs and fingerprint vectors
- NumPy .npy array of fingerprints

## How to apply

Install the biosynfoni package via pip (biosynfoni requires Python 3.9+; RDKit is installed as a dependency). Load molecular structures from your dataset using RDKit (Chem.MolFromSmiles, Chem.MolFromInChI, or an SDF supplier). For each molecule, instantiate the Biosynfoni class and extract the .fingerprint attribute, which returns a count-based bit-vector encoding biosynthetic structural motifs. Export fingerprints as a structured output (CSV with molecule IDs and bit-vectors, or NumPy .npy array) for downstream analysis. The fingerprint captures biosynthetic information and biochemical logic tailored to natural products, making it superior to generic molecular fingerprints for natural product-specific tasks.

## Related tools

- **biosynfoni** (Core package for computing molecular fingerprints tailored to natural product chemistry; provides the Biosynfoni class API and command-line interface for fingerprint generation.) — https://github.com/lucinamay/biosynfoni
- **RDKit** (Dependency for molecular structure parsing and manipulation; required to load and represent molecules from SMILES, InChI, or SDF formats before fingerprint computation.)
- **pip** (Package manager for installing biosynfoni and its dependencies in development or production mode.)
- **black** (Code formatter used during development and testing of the biosynfoni package; not required for end-user fingerprint computation but ensures code quality standards.) — https://github.com/psf/black
- **pytest** (Testing framework used in biosynfoni development to verify fingerprint computation correctness and package functionality.)

## Examples

```
from biosynfoni import Biosynfoni
from rdkit import Chem
mol = Chem.MolFromSmiles('CC(=O)Oc1ccccc1C(=O)O')
fp = Biosynfoni(mol).fingerprint
```

## Evaluation signals

- Fingerprints are successfully computed for all input molecules without errors; each molecule yields a single count-based bit-vector of consistent dimensionality.
- Output CSV or NumPy array contains the expected number of fingerprint records matching the number of input molecules, with no missing or null values.
- Fingerprints computed from identical SMILES/InChI strings are byte-identical (deterministic output), indicating stable and reproducible computation.
- Biosynfoni fingerprints demonstrate superior discriminative power for natural product biosynthetic class prediction compared to generic fingerprints (ECFP, MACCS) when evaluated on COCONUT or similar natural product gold standards.
- Fingerprints capture biosynthetic motifs absent in generic descriptors; evidence can be obtained by comparing feature importance or embedding visualizations between biosynfoni and ECFP on a curated natural product benchmark.

## Limitations

- Biosynfoni is optimized specifically for natural products; application to purely synthetic compounds may not yield biochemically meaningful representations.
- No changelog or version history documentation is available, making it difficult to track changes or compatibility across different releases.
- Fingerprint interpretation is latent (bit-level) and not directly human-readable; feature attribution or explainability of individual bits requires additional analysis.
- Computational performance on very large molecular libraries (millions of molecules) is not documented; scaling requirements are unknown.

## Evidence

- [readme] a biosynformatic molecular fingerprint tailored to natural product chem- and bioinformatic research: "a biosynformatic molecular fingerprint tailored to natural product chem- and bioinformatic research"
- [readme] relating to biosynthetic information and biochemical logic: "relating to biosynthetic information and biochemical logic"
- [readme] Biosynfoni requires Python 3.9 or later. RDKit is installed as a dependency when installing Biosynfoni.: "Biosynfoni requires Python 3.9 or later. RDKit is installed as a dependency when installing Biosynfoni."
- [readme] fp = Biosynfoni(mol).fingerprint  # returns biosynfoni's count fingerprint of the molecule: "fp = Biosynfoni(mol).fingerprint  # returns biosynfoni's count fingerprint of the molecule"
- [readme] Write the fingerprints of all molecules in an SDF file to a CSV file: "Write the fingerprints of all molecules in an SDF file to a CSV file"
- [readme] We have used data from the COCONUT natural product database and ZINC compound database.: "We have used data from the COCONUT natural product database and ZINC compound database."
- [other] No changelog found — version history and update documentation absent: "No changelog found — version history and update documentation absent"
