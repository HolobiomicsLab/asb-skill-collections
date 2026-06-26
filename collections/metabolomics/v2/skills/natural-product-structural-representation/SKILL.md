---
name: natural-product-structural-representation
description: Use when when you need to represent natural product molecules as numerical
  feature vectors for downstream machine learning (e.g., biosynthetic class prediction),
  comparative analysis, or when standard chemical fingerprints (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3762
  edam_topics:
  - http://edamontology.org/topic_0209
  - http://edamontology.org/topic_3314
  - http://edamontology.org/topic_0154
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# natural-product-structural-representation

## Summary

Generate a biosynformatic molecular fingerprint tailored to natural product chemistry and bioinformatics research. This skill converts molecular structures into fixed-length numerical vectors that encode biosynthetic and chemical logic relevant to natural products.

## When to use

When you need to represent natural product molecules as numerical feature vectors for downstream machine learning (e.g., biosynthetic class prediction), comparative analysis, or when standard chemical fingerprints (e.g., Morgan, ECFP) do not capture biosynthetic features relevant to your research question.

## When NOT to use

- You are working exclusively with synthetic compounds where biosynthetic logic is not relevant; standard cheminformatic fingerprints (Morgan, topological) may suffice.
- Your input molecules are already represented as a feature matrix or precomputed fingerprints; this skill generates new representations, not transforms existing ones.
- Your natural product dataset comes from sources (e.g., ZINC) optimized for synthetic chemistry rather than biosynthetic structure; biosynfoni is trained on COCONUT (natural product database) and may have lower discriminative power on synthetic compound sets.

## Inputs

- SMILES string
- InChI string
- RDKit Mol object
- SDF file (multi-molecule)

## Outputs

- biosynfoni count fingerprint (fixed-length numerical array)
- CSV file with fingerprints (one row per molecule)

## How to apply

Load the biosynfoni package and instantiate a Biosynfoni object with an RDKit molecule object created from a SMILES or InChI string. Call the .fingerprint property to generate a count-based fingerprint—a fixed-length numerical array encoding biosynthetic structural features of the molecule. The fingerprint output is deterministic and dimensionality-consistent across all input molecules. Validate the output by checking that it matches the expected fingerprint array shape and data type. For batch processing (e.g., SDF files), use the command-line interface to write fingerprints to CSV; for programmatic use, iterate over molecule objects and collect fingerprint arrays into a feature matrix suitable for downstream classification or clustering.

## Related tools

- **biosynfoni** (Python package that computes the biosynformatic molecular fingerprint; accepts molecule objects and returns fixed-length count fingerprints encoding biosynthetic features) — https://github.com/lucinamay/biosynfoni
- **RDKit** (Dependency for molecular I/O, SMILES/InChI parsing, and Mol object creation; automatically installed with biosynfoni)
- **black** (Code formatter used in development workflow (optional, for pull request submissions to biosynfoni repository)) — https://github.com/psf/black
- **pytest** (Test runner used to validate fingerprint computation correctness on test molecules)

## Examples

```
from biosynfoni import Biosynfoni
from rdkit import Chem

mol = Chem.MolFromSmiles('CC(C)Cc1ccc(cc1)C(C)C(O)=O')
fp = Biosynfoni(mol).fingerprint
```

## Evaluation signals

- Output fingerprint is a valid numerical array with consistent dimensionality across all input molecules
- Output data type matches expected format (e.g., NumPy array, list of integers or floats)
- pytest tests/ passes without errors, confirming fingerprint computation matches reference implementations
- Fingerprints from the same molecule are identical across repeated runs (determinism check)
- Fingerprints from structurally similar natural products show higher cosine similarity than random pairs, confirming biosynthetic signal

## Limitations

- biosynfoni is optimized for natural products from COCONUT database; performance on synthetic compounds or non-natural scaffolds is not reported.
- Fingerprint dimensionality and feature definitions are fixed; the skill does not support custom feature engineering or parameter tuning.
- Requires valid chemical structure input (SMILES or InChI); malformed strings or molecules with unresolvable stereochemistry will fail silently or raise RDKit exceptions.
- The skill does not perform any molecular validation, standardization, or salts/stereoisomer handling; input quality depends on upstream curation.

## Evidence

- [other] biosynfoni provides a biosynformatic molecular fingerprint tailored to natural product chem- and bioinformatic research.: "biosynfoni provides a biosynformatic molecular fingerprint tailored to natural product chem- and bioinformatic research"
- [readme] Load the biosynfoni package and instantiate; call .fingerprint to return biosynfoni's count fingerprint of the molecule: "from biosynfoni import Biosynfoni
from rdkit import Chem

smi = <SMILES>
mol = Chem.MolFromSmiles(smi)
fp = Biosynfoni(mol).fingerprint"
- [other] Execute the fingerprint function on a test molecule to produce a fixed-length numerical vector representation.: "Execute the fingerprint function on a test molecule to produce a fixed-length numerical vector representation"
- [other] Verify the output is a valid fingerprint array matching the expected dimensionality and data type.: "Verify the output is a valid fingerprint array matching the expected dimensionality and data type"
- [readme] Write the fingerprints of all molecules in an SDF file to a CSV file: "Write the fingerprints of all molecules in an SDF file to a CSV file:

biosynfoni <molecule_supplier.sdf>"
- [other] Run pytest tests/ to validate that all fingerprint computation tests pass successfully.: "Run pytest tests/ to validate that all fingerprint computation tests pass successfully"
- [readme] We have used data from the COCONUT natural product database and ZINC compound database: "We have used data from the COCONUT natural product database"
