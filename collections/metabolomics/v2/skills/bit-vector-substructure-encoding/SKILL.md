---
name: bit-vector-substructure-encoding
description: Use when you need to represent natural product molecules as fixed-length bit vectors for downstream machine learning (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0292
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3474
  tools:
  - biosynfoni
  - pip
  - RDKit
  - black
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# bit-vector-substructure-encoding

## Summary

Compute a biosynfoni bit-vector molecular fingerprint that encodes biosynthetic substructural information from chemical structure input. This specialized fingerprint representation is designed for natural product classification and bioinformatic analysis where traditional fingerprints may not capture domain-specific biosynthetic features.

## When to use

Apply this skill when you need to represent natural product molecules as fixed-length bit vectors for downstream machine learning (e.g., biosynthetic class prediction), or when comparing chemical similarity within natural product chemistry and you want fingerprints sensitive to biosynthetic logic rather than generic molecular properties.

## When NOT to use

- Input molecules are synthetic compounds not related to natural product chemistry; standard fingerprints (Morgan, ECFP) are more generalizable.
- Fingerprints are already computed or the molecule representation is already a pre-computed feature vector.
- Analysis requires atom or bond-level explanations of molecular differences; bit vectors are not interpretable at that granularity.

## Inputs

- SMILES string
- InChI string
- RDKit Mol object
- SDF file (multi-molecule)

## Outputs

- Biosynfoni count fingerprint (bit vector)
- CSV file with molecule IDs and bit vectors
- NumPy .npy array of fingerprints

## How to apply

Load the molecule structure as an RDKit Mol object from SMILES, InChI, or SDF input. Instantiate a Biosynfoni object and call its fingerprint property to generate a count-based bit vector encoding biosynthetic substructures. The fingerprint represents the presence and abundance of biosynthetically relevant molecular fragments. Export the resulting bit vectors (one per molecule) as a structured format (CSV with molecule IDs and bit positions, or NumPy array) for use in downstream classifiers or similarity analyses. The fingerprint design is specifically trained on natural product chemistry patterns from databases like COCONUT, making it more informative than generic Morgan or ECFP fingerprints for this domain.

## Related tools

- **biosynfoni** (Core package that computes the bit-vector fingerprint representation from molecular structures) — https://github.com/lucinamay/biosynfoni
- **RDKit** (Chemistry toolkit dependency for loading and parsing molecular structures (SMILES, InChI, SDF))
- **pip** (Package installer to deploy biosynfoni and its dependencies)
- **black** (Code formatter for development workflows (optional, for code quality during implementation)) — https://github.com/psf/black

## Examples

```
from biosynfoni import Biosynfoni
from rdkit import Chem
mol = Chem.MolFromSmiles('CC(C)Cc1ccc(cc1)C(C)C(=O)O')
fp = Biosynfoni(mol).fingerprint
```

## Evaluation signals

- Fingerprint output is a valid bit vector (NumPy array or structured CSV) with length consistent across all molecules in the batch.
- Fingerprints computed from identical molecules are bitwise identical (deterministic output).
- Fingerprints can be successfully ingested by downstream biosynthetic class predictors without shape or type errors.
- CSV export includes all molecule IDs and corresponding bit vectors with no missing values.
- Command-line invocation (e.g., `biosynfoni molecule.sdf`) produces output file without errors and completes in expected runtime.

## Limitations

- Biosynfoni fingerprints are optimized for natural product molecules; performance on synthetic compounds or out-of-domain chemistry is not established.
- The fingerprint design is tied to biosynthetic patterns learned from COCONUT and related natural product databases; coverage of rare or exotic scaffolds may be limited.
- No changelog or version history documented in the repository, making it difficult to track breaking changes or improvements across releases.
- Bit-vector representation is not human-interpretable; users cannot easily identify which substructures contributed to specific fingerprint positions.

## Evidence

- [other] Biosynfoni is a biosynformatic molecular fingerprint tailored to natural product chemistry and bioinformatic research applications.: "a biosynformatic molecular fingerprint designed specifically for natural product chemistry and bioinformatic research applications"
- [other] The skill computes fingerprints using the biosynfoni package API by loading molecules and exporting structured bit vectors.: "Load molecular structures from the sample dataset (format and path to be specified by user). 3. Compute biosynfoni fingerprints for each molecule using the biosynfoni package API. 4. Export"
- [readme] The package supports multiple input formats and command-line usage for batch fingerprint computation.: "Convert a SMILES string to a fingerprint... Create a fingerprint from an InChI string... Write the fingerprints of all molecules in an SDF file to a CSV file"
- [readme] Fingerprints are designed for downstream biosynthetic class prediction on natural products.: "We have trained a biosynthetic class predictor on `biosynfoni` fingerprints"
- [readme] The fingerprint is grounded in natural product chemistry training data from established databases.: "We have used data from the [COCONUT](https://coconut.naturalproducts.net) natural product database and [ZINC](https://zinc.docking.org) compound database"
