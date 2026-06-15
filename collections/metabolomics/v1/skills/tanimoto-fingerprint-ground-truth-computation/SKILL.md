---
name: tanimoto-fingerprint-ground-truth-computation
description: Use when when preparing paired MS/MS spectra for training or validation of a siamese neural network model, and you have chemical structure annotations (InChI, SMILES, or InChIKey) for each spectrum but lack pre-computed structural similarity labels.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0564
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0209
  tools:
  - MS2DeepScore
  - RDKit
  - Python
  - matchms
  - pubchempy
derived_from:
- doi: 10.1186/s13321-021-00558-4
  title: MS2DeepScore
evidence_spans:
- MS2DeepScore to predict structural similarity scores for spe
- we used the MS2DeepScore base network (Fig. 1) to compute the 200-dimensional spectral embeddings for all 3601 spectra in the test set
- we used Tanimoto scores on RDKit [23] Daylight fingerprints (2048 bits) to compute structural similarities
- Our MS2DeepScore Python library offers two types of data generators
- Our MS2DeepScore Python library
- Metadata was cleaned and checked using matchms [18] version 0.8.2, which included cleaning compound names
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2deepscore
    doi: 10.1186/s13321-021-00558-4
    title: MS2DeepScore
  dedup_kept_from: coll_ms2deepscore
schema_version: 0.2.0
---

# tanimoto-fingerprint-ground-truth-computation

## Summary

Compute Tanimoto structural similarity scores from pairs of molecular fingerprints derived from chemical structure annotations (InChI/SMILES), producing ground-truth labels for training and evaluating mass spectra similarity models. This is essential when building supervised learning systems that predict structural similarity directly from MS/MS spectral data without explicit fingerprint computation.

## When to use

When preparing paired MS/MS spectra for training or validation of a siamese neural network model, and you have chemical structure annotations (InChI, SMILES, or InChIKey) for each spectrum but lack pre-computed structural similarity labels. Use this skill to generate the ground-truth Tanimoto scores that will supervise the model's learning.

## When NOT to use

- Spectra lack chemical structure annotations (InChI, SMILES, or InChIKey); alternative unsupervised similarity measures (e.g., Spec2Vec, cosine similarity on spectral embeddings) should be used instead.
- You are predicting unknown compound structures from spectra; Tanimoto scores require reference structures and cannot be computed de novo.
- Your task is to measure spectral similarity directly without structural context; use classical spectral similarity metrics (modified cosine, neutral loss) instead.

## Inputs

- MS/MS spectrum metadata containing InChI, SMILES, or InChIKey annotations
- List of spectrum objects with assigned unique InChIKeys
- Cleaned and standardized InChI strings (one canonical per InChIKey)

## Outputs

- Ground-truth Tanimoto similarity scores (float, range 0–1) for spectrum pairs
- Paired spectrum indices with associated Tanimoto labels
- Binned pair sampling distribution for downstream model training

## How to apply

For each unique 14-character InChIKey in your dataset, select the most common InChI annotation and generate a 2048-bit RDKit Daylight molecular fingerprint. For every pair of spectra (typically created through stratified random pairing binned by similarity score range), compute the Tanimoto similarity between their corresponding fingerprints. This produces a continuous ground-truth label (0 to 1 range) for each spectrum pair. The pairing strategy should use balanced sampling across similarity bins to avoid skewed training distributions toward either high or low similarity pairs.

## Related tools

- **RDKit** (Generate 2048-bit Daylight molecular fingerprints from InChI/SMILES structures for Tanimoto computation) — https://www.rdkit.org/
- **matchms** (Clean, normalize, and manage MS/MS spectrum metadata (InChI, SMILES, InChIKey extraction and standardization)) — https://github.com/matchms/matchms
- **pubchempy** (Automated lookup and retrieval of missing InChI or SMILES annotations from PubChem for spectra lacking structure information) — https://pubchem.ncbi.nlm.nih.gov/

## Examples

```
from rdkit import Chem; from rdkit.Chem import AllChem; from rdkit import DataStructs; fp1 = AllChem.GetMorganFingerprintAsBitVect(Chem.MolFromInchi(inchi1), 2, nBits=2048); fp2 = AllChem.GetMorganFingerprintAsBitVect(Chem.MolFromInchi(inchi2), 2, nBits=2048); tanimoto = DataStructs.TanimotoSimilarity(fp1, fp2)
```

## Evaluation signals

- Verify that all spectrum pairs have Tanimoto scores in the range [0, 1] with no NaN or infinite values.
- Check that the distribution of Tanimoto scores across bins (e.g., 0–0.1, 0.1–0.2, …, 0.9–1.0) is balanced or follows the intended sampling strategy, avoiding large gaps or under-represented bins.
- Confirm that the number of spectrum pairs matches the expected total from the pairing strategy (e.g., n unique InChIKeys, stratified sampling with replacement).
- Validate that all InChIKeys map to exactly one canonical InChI and that the same InChI pair always produces identical Tanimoto scores across runs (reproducibility check).
- Spot-check 10–20 pairs by independently recalculating their Tanimoto scores using the same RDKit fingerprints and comparing results for numerical agreement (≤ 1e-6 relative error).

## Limitations

- Tanimoto scores depend on the quality and uniqueness of structure annotations; missing, incorrect, or duplicated InChI/SMILES will introduce errors or label noise. The article notes that 'for every unique 14-character InChIKey the most common InChI was selected', which reduces but does not eliminate ambiguity in cases of multiple InChI entries per key.
- The 2048-bit Daylight fingerprint is a fixed-size representation and may lose fine structural detail for very large or complex molecules; different fingerprint types (e.g., ECFP, TTT) would produce different Tanimoto scores and model training dynamics.
- Balanced pair sampling is crucial but non-trivial; if bins are not representative of the actual compound structure space or if the sampling strategy is skewed, the resulting ground truth may bias the model toward certain similarity ranges and degrade performance on undersampled regions.
- Computation is quadratic in the number of unique structures (O(n²) pairs); datasets with >100,000 spectra or >15,000 unique molecules require efficient pair generation and storage strategies.

## Evidence

- [methods] For every unique 14-character InChIKey the most common InChI was selected and used to generate a molecular fingerprint. For each pair of molecular fingerprints Tanimoto scores were calculated: "For every unique 14-character InChIKey the most common InChI was selected and used to generate a molecular fingerprint. For each pair of molecular fingerprints Tanimoto scores were calculated,"
- [methods] we used Tanimoto scores on RDKit Daylight fingerprints (2048 bits) to compute structural similarities: "we used Tanimoto scores on RDKit Daylight fingerprints (2048 bits) to compute structural similarities"
- [methods] each spectrum was then matched to a random other spectrum, with the condition that the resulting corresponding InChiKey pair had a structural similarity label falling into a randomly chosen bin: "each spectrum was then matched to a random other spectrum, with the condition that the resulting corresponding InChiKey pair had a structural similarity label falling into a randomly chosen bin,"
- [methods] The set of 15,062 InChIKeys was split into a training (n = 14,062), validation (n = 500), and test set (n = 500): "The set of 15,062 InChIKeys was split into a training (n = 14,062), validation (n = 500), and test set (n = 500)"
- [results] validation set (3597 spectra of 500 unique InChIKeys)... test set (3601 spectra of 500 unique InChIKeys): "validation set (3597 spectra of 500 unique InChIKeys)... test set (3601 spectra of 500 unique InChIKeys)"
