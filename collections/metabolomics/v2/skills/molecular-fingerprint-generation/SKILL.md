---
name: molecular-fingerprint-generation
description: Use when when you have annotated chemical structures (SMILES or InChI
  strings) from a curated MS/MS dataset and need to compute pairwise structural similarity
  scores (Tanimoto or other metrics) as training labels, or when preparing molecular
  representations for comparison against mass spectral data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3627
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3172
  tools:
  - RDKit
  - matchms
  - Python
  - MS2DeepScore
  - Spec2Vec
  - scikit-learn
  - pubchempy
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1186/s13321-021-00558-4
  title: MS2DeepScore
evidence_spans:
- Unless noted otherwise, we used Tanimoto scores on RDKit [23] Daylight fingerprints
  (2048 bits) to compute structural similarities.
- Unless noted otherwise, we used Tanimoto scores on RDKit [23] Daylight fingerprints
  (2048 bits) to compute structural similarities
- Metadata was cleaned and checked using matchms [18] version 0.8.2, which included
  cleaning compound names, extracting adduct information from the given metadata,
  moving metadata to consistent fields
- For each pair of molecular fingerprints Tanimoto scores were calculated, indicating
  the structural similarity of that pair. (as implemented in matchms [18])
- Our MS2DeepScore Python library offers two types of data generators, one which iterates
  over all unique InChIKeys (DataGeneratorAllInchikeys) and one which iterates over
  all spectra and was used for
- Our MS2DeepScore Python library offers two types of data generators
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_biosynfoni_2_cq
    doi: 10.26434/chemrxiv-2025-cwq74
    title: biosynfoni
  - build: coll_biosynfoni_cq
    doi: 10.26434/chemrxiv-2025-cwq74
    title: biosynfoni
  - build: coll_deepmass_cq
    doi: 10.1101/2024.05.30.596727v2
    title: DeepMASS
  - build: coll_ms2deepscore_cq
    doi: 10.1186/s13321-021-00558-4
    title: MS2DeepScore
  dedup_kept_from: coll_ms2deepscore_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-021-00558-4
  all_source_dois:
  - 10.1186/s13321-021-00558-4
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-fingerprint-generation

## Summary

Generate binary molecular fingerprints from chemical structures (SMILES/InChI) using RDKit Daylight algorithm to encode structural features for downstream similarity computation and machine learning tasks.

## When to use

When you have annotated chemical structures (SMILES or InChI strings) from a curated MS/MS dataset and need to compute pairwise structural similarity scores (Tanimoto or other metrics) as training labels, or when preparing molecular representations for comparison against mass spectral data.

## When NOT to use

- Input structures are already pre-computed fingerprints or embeddings (skip directly to similarity scoring).
- Only unannotated spectra are available without chemical structure data (fingerprints cannot be generated de novo from mass spectral peaks alone).
- Non-standard or stereoisomerically ambiguous InChI strings that do not map to a single canonical structure (handle curation first).

## Inputs

- InChIKey (14-character identifiers, unique per molecular structure)
- InChI or SMILES strings (chemical structure representations)
- Annotated MS/MS spectra dataset with metadata mappings

## Outputs

- RDKit Daylight fingerprints (2048-bit binary vectors, one per unique InChIKey)
- Fingerprint index/lookup table (InChIKey → fingerprint)
- Fingerprint matrix ready for pairwise similarity computation

## How to apply

For each unique 14-character InChIKey in your annotated dataset, extract the most common InChI (if multiple InChI annotations exist for the same InChIKey) and generate a 2048-bit RDKit Daylight fingerprint using matchms and RDKit. Each fingerprint encodes structural features as a binary vector. Store fingerprints indexed by InChIKey for efficient pairwise comparison. The 2048-bit representation balances chemical feature discrimination with computational tractability for subsequent similarity scoring across large molecular libraries (e.g., 15,062 unique molecules).

## Related tools

- **RDKit** (Generates Daylight fingerprints (2048 bits) from InChI/SMILES structures; core algorithm for binary molecular representation) — https://www.rdkit.org/
- **matchms** (Wraps RDKit fingerprint generation and manages InChIKey/SMILES/InChI metadata extraction and standardization from MS/MS spectra annotations) — https://github.com/matchms/matchms
- **pubchempy** (Automated PubChem lookup to retrieve missing InChI or SMILES annotations for spectra before fingerprint generation) — https://pubchem.ncbi.nlm.nih.gov/

## Examples

```
from rdkit import Chem
from rdkit.Chem import AllChem
fp = AllChem.GetMorganFingerprintAsBitVect(Chem.MolFromInchi(inchi_string), radius=2, nBits=2048)
```

## Evaluation signals

- All 15,062 unique InChIKeys yield exactly one canonical fingerprint (no duplicates or missing values).
- Fingerprints are binary vectors of length 2048 with no NaN or null entries.
- Pairwise Tanimoto similarity scores computed from fingerprints fall within [0, 1] range and show expected chemical similarity patterns (e.g., structurally identical compounds yield Tanimoto = 1.0).
- Fingerprint generation completes without RDKit structure parsing errors; any failures are logged and traceable to malformed InChI/SMILES input.
- Fingerprint matrix dimensions are 15,062 × 2048 (or smaller if subset of unique InChIKeys); matrix is sparse (binary representation).

## Limitations

- Daylight fingerprints encode 2D molecular structure only; stereochemical information is discarded (disregarding stereoisomerism as noted in the article).
- Fingerprint quality depends on input SMILES/InChI curation; invalid or ambiguous structures fail silently or produce uninformative fingerprints.
- 2048-bit resolution is a fixed hyperparameter; different fingerprint lengths or algorithms (e.g., Morgan, ECFP) may be more suitable for specific molecular scaffolds but are not explored here.
- Computational cost scales quadratically with the number of unique molecules during pairwise Tanimoto computation (O(n²) for n InChIKeys).
- Fingerprints do not preserve intensity or fragmentation patterns from MS/MS spectra; only structural features are encoded.

## Evidence

- [methods] For every unique 14-character InChIKey the most common InChI was selected (if different InChI existed) and used to generate a molecular fingerprint.: "For every unique 14-character InChIKey the most common InChI was selected (if different InChI existed) and used to generate a molecular fingerprint."
- [other] RDKit Daylight fingerprints (2048 bits) are generated per unique InChIKey, and pairwise Tanimoto scores are computed between all fingerprint pairs to quantify structural similarity as training targets.: "RDKit Daylight fingerprints (2048 bits) are generated per unique InChIKey, and pairwise Tanimoto scores are computed between all fingerprint pairs to quantify structural similarity as training"
- [methods] Unless noted otherwise, we used Tanimoto scores on RDKit Daylight fingerprints (2048 bits) to compute structural similarities: "Unless noted otherwise, we used Tanimoto scores on RDKit Daylight fingerprints (2048 bits) to compute structural similarities"
- [other] Generate RDKit Daylight fingerprints (2048 bits) for each unique InChIKey using matchms and RDKit.: "Generate RDKit Daylight fingerprints (2048 bits) for each unique InChIKey using matchms and RDKit."
- [results] The dataset contains 15,062 different molecules (disregarding stereoisomerism): "The dataset contains 15,062 different molecules (disregarding stereoisomerism)"
