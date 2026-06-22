---
name: biosynformatic-descriptor-computation
description: Use when when you have a natural product structure (as a molecule object, SMILES string, or InChI string) and need to generate a biosynformatic descriptor for downstream machine learning tasks such as biosynthetic class prediction, structure-activity correlation, or natural product database.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0564
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_2258
  tools:
  - pip
  - biosynfoni
  - RDKit
  - pytest
  - black
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
  - build: coll_biosynfoni_cq
    doi: 10.26434/chemrxiv-2025-cwq74
    title: biosynfoni
  dedup_kept_from: coll_biosynfoni_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.26434/chemrxiv-2025-cwq74
  all_source_dois:
  - 10.26434/chemrxiv-2025-cwq74
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# biosynformatic-descriptor-computation

## Summary

Compute biosynformatic molecular fingerprints—fixed-length numerical vector representations tailored to natural product structure—from molecule objects using the biosynfoni package. This skill converts chemical structures into machine-readable descriptors suitable for biosynthetic class prediction and natural product cheminformatics research.

## When to use

When you have a natural product structure (as a molecule object, SMILES string, or InChI string) and need to generate a biosynformatic descriptor for downstream machine learning tasks such as biosynthetic class prediction, structure-activity correlation, or natural product database annotation. Apply this skill when standard molecular fingerprints are insufficient for capturing biosynthetic logic relevant to secondary metabolites.

## When NOT to use

- Input is already a pre-computed feature table or descriptor matrix; use this skill only on raw chemical structures.
- Goal is general-purpose molecular fingerprinting (e.g., Tanimoto similarity, scaffold diversity) unrelated to biosynthetic classification or natural product cheminformatics; consider standard RDKit fingerprints (ECFP, MACCS) instead.
- Molecule structures are invalid, ambiguous, or cannot be parsed by RDKit; validate input with Chem.MolFromSmiles() returning non-None before applying this skill.

## Inputs

- SMILES string (canonical or non-canonical)
- InChI string
- SDF file (molecular structure supplier)
- RDKit molecule object (Mol)

## Outputs

- biosynfoni count fingerprint (fixed-length numerical vector)
- fingerprint array (integer or float dtype)
- CSV file of fingerprints (from SDF batch processing)

## How to apply

Install biosynfoni from PyPI (pip install biosynfoni) or from the development repository (pip install -e .[dev]) if contributing. Parse your structure into an RDKit molecule object using Chem.MolFromSmiles() or Chem.MolFromInChI(). Instantiate a Biosynfoni object with the molecule and call the .fingerprint property to retrieve a count fingerprint—a fixed-length numerical vector. Verify output dimensionality and data type match expected specifications (e.g., integer or float array of consistent length). Use pytest tests/ to validate fingerprint computation correctness if modifying the package, and format any code contributions with black before submission.

## Related tools

- **biosynfoni** (Computes biosynformatic molecular fingerprints from molecule objects; core tool for this skill) — https://github.com/lucinamay/biosynfoni
- **RDKit** (Parses SMILES/InChI strings into molecule objects required as input to biosynfoni)
- **pytest** (Validates fingerprint computation correctness and implementation integrity before deployment)
- **black** (Code formatter for maintaining style consistency in biosynfoni contributions) — https://github.com/psf/black

## Examples

```
from biosynfoni import Biosynfoni
from rdkit import Chem

mol = Chem.MolFromSmiles('CC(C)Cc1ccc(cc1)C(C)C(O)=O')
fp = Biosynfoni(mol).fingerprint
```

## Evaluation signals

- Output fingerprint array has expected fixed dimensionality (compare to documented fingerprint size in biosynfoni documentation).
- Fingerprint data type is consistent with specification (integer counts or floats); no NaN or infinite values.
- All pytest tests in tests/ pass without errors or warnings, confirming fingerprint computation logic is correct.
- Fingerprint for the same molecule is deterministic and reproducible across repeated calls.
- Fingerprints from semantically equivalent structures (e.g., different SMILES representations of the same molecule) are identical or very similar in Tanimoto distance.

## Limitations

- biosynfoni is specialized for natural products and biosynthetic classification; fingerprints may not generalize well to synthetic drug-like compounds or other chemical spaces.
- Requires valid, parseable chemical structures; malformed or ambiguous SMILES/InChI strings will fail silently or produce invalid fingerprints.
- Fingerprint interpretation is tied to the biosynthetic class predictor training data (COCONUT and ZINC databases); performance on novel chemical scaffolds not represented in training may be limited.
- Python 3.9+ and RDKit (installed as a dependency) are required; some computational environments may have constraints on dependency installation.

## Evidence

- [other] biosynfoni provides a biosynformatic molecular fingerprint tailored to natural product chem- and bioinformatic research.: "biosynfoni provides a biosynformatic molecular fingerprint tailored to natural product chem- and bioinformatic research"
- [other] Fingerprint computation returns fixed-length numerical vector: "Execute the fingerprint function on a test molecule to produce a fixed-length numerical vector representation"
- [readme] Installation and RDKit dependency: "Biosynfoni requires Python 3.9 or later. RDKit is installed as a dependency when installing Biosynfoni."
- [readme] Python API usage via Biosynfoni class: "from biosynfoni import Biosynfoni
from rdkit import Chem

smi = <SMILES>
mol = Chem.MolFromSmiles(smi)
fp = Biosynfoni(mol).fingerprint"
- [other] Validation via pytest: "Run pytest tests/ to validate that all fingerprint computation tests pass successfully"
- [other] Code formatting requirement: "Please use `black` to format your code before submitting a pull request"
- [readme] Training data sourcing: "We have used data from the COCONUT natural product database and ZINC compound database"
