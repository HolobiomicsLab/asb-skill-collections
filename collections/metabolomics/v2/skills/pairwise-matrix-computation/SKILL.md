---
name: pairwise-matrix-computation
description: Use when when you have a cleaned MS/MS dataset with chemical structure
  annotations (SMILES, InChI, or InChIKey) and need to generate ground-truth structural
  similarity labels for training a deep learning model.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_1812
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_0593
  tools:
  - RDKit
  - matchms
  - Python
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

# pairwise-matrix-computation

## Summary

Compute a symmetric matrix of pairwise similarity scores (Tanimoto) between all molecular fingerprints derived from annotated MS/MS spectra, serving as ground-truth structural similarity labels for model training. This is essential when you need quantitative measures of molecular structural relatedness across a large set of unique chemical structures.

## When to use

When you have a cleaned MS/MS dataset with chemical structure annotations (SMILES, InChI, or InChIKey) and need to generate ground-truth structural similarity labels for training a deep learning model. Specifically, when you must compute all pairwise comparisons between unique molecular structures to create a complete N×N similarity matrix where N is the number of unique InChIKeys in your dataset.

## When NOT to use

- When you only have a few dozen structures and do not need a complete all-pairs matrix — iterative pairwise scoring may be more efficient
- When input structures lack chemical annotation (no SMILES, InChI, or InChIKey) — fingerprint generation requires valid molecular structure encoding
- When you need to compare spectra across different ionization modes and structural similarity alone is insufficient — this skill does not account for ionization effects or mass spectral properties

## Inputs

- Cleaned MS/MS spectra dataset with InChIKey and SMILES/InChI annotations
- Set of unique InChIKeys (14-character identifiers)
- SMILES or InChI strings corresponding to each InChIKey

## Outputs

- Symmetric N×N Tanimoto similarity score matrix (numpy array or saved file)
- RDKit Daylight fingerprints (2048 bits) for each unique InChIKey

## How to apply

First, extract the most common InChI for each unique 14-character InChIKey (handling cases where multiple InChI annotations exist for the same key). Generate RDKit Daylight fingerprints (2048 bits) for each unique InChIKey using the matchms and RDKit libraries. Then compute Tanimoto similarity scores between all pairs of molecular fingerprints across the entire set of unique InChIKeys using RDKit's built-in Tanimoto implementation. Finally, construct and save the resulting N×N symmetric matrix (where N = number of unique InChIKeys) as the structural similarity label matrix. The choice of Daylight fingerprints with 2048 bits is motivated by their proven effectiveness for structural similarity quantification in metabolomics workflows.

## Related tools

- **RDKit** (Generate Daylight fingerprints (2048 bits) from SMILES/InChI and compute Tanimoto similarity scores between all fingerprint pairs)
- **matchms** (Provide data structures and utilities for working with MS/MS spectral metadata and facilitate fingerprint generation workflow) — https://github.com/matchms/matchms
- **Python** (Orchestrate the full workflow including data loading, fingerprint generation, pairwise computation, and matrix serialization)

## Examples

```
from rdkit import Chem
from rdkit.Chem import AllChem
import numpy as np

smiles_list = [smiles for inchikey, smiles in unique_structures]
fps = [AllChem.GetMorganFingerprintAsBitVect(Chem.MolFromSmiles(smi), 2, nBits=2048) for smi in smiles_list]
tanimoto_matrix = np.array([[DataStructs.TanimotoSimilarity(fps[i], fps[j]) for j in range(len(fps))] for i in range(len(fps))])
np.save('tanimoto_similarity_matrix.npy', tanimoto_matrix)
```

## Evaluation signals

- Output matrix dimensions match N×N where N equals the count of unique InChIKeys in the input dataset (e.g., 15,062 × 15,062)
- Matrix is symmetric: score[i,j] == score[j,i] for all pairs, and diagonal values are 1.0 (self-similarity)
- All matrix values fall within the valid Tanimoto range [0.0, 1.0] with no NaN or infinite entries
- Fingerprint generation completes for 100% of unique InChIKeys without errors or skipped structures
- Spot-check pairwise scores by verifying known structurally similar molecules (same InChIKey or close chemical analogues) have scores near 1.0, while unrelated structures score near 0.0

## Limitations

- Tanimoto similarity based on Daylight fingerprints may not capture all relevant structural features (e.g., stereoisomerism is disregarded by InChIKey comparison; 3D geometry is not encoded)
- Computational complexity is O(N²) where N is the number of unique InChIKeys, making this approach memory-intensive for very large datasets (>100,000 unique structures)
- If multiple InChI strings map to the same 14-character InChIKey, only the most common InChI is retained; information from alternative annotations is lost
- The method does not handle spectra lacking chemical structure annotation; those records are excluded from matrix computation entirely

## Evidence

- [other] From annotated structures (SMILES/InChI) in the cleaned dataset, RDKit Daylight fingerprints (2048 bits) are generated per unique InChIKey, and pairwise Tanimoto scores are computed between all fingerprint pairs to quantify structural similarity as training targets.: "RDKit Daylight fingerprints (2048 bits) are generated per unique InChIKey, and pairwise Tanimoto scores are computed between all fingerprint pairs to quantify structural similarity as training targets"
- [other] Extract the most common InChI for each unique 14-character InChIKey (handling cases where multiple InChI annotations exist for the same InChIKey). Generate RDKit Daylight fingerprints (2048 bits) for each unique InChIKey using matchms and RDKit. Compute pairwise Tanimoto similarity scores between all molecular fingerprints across the 15,062 unique InChIKeys using RDKit. Construct and save the 15,062 × 15,062 Tanimoto score matrix as the structural similarity label matrix for model training.: "Extract the most common InChI for each unique 14-character InChIKey (handling cases where multiple InChI annotations exist for the same InChIKey). Generate RDKit Daylight fingerprints (2048 bits) for"
- [methods] Unless noted otherwise, we used Tanimoto scores on RDKit Daylight fingerprints (2048 bits) to compute structural similarities: "we used Tanimoto scores on RDKit Daylight fingerprints (2048 bits) to compute structural similarities"
- [results] The dataset contains 15,062 different molecules (disregarding stereoisomerism): "The dataset contains 15,062 different molecules (disregarding stereoisomerism)"
- [methods] For every unique 14-character InChIKey the most common InChI was selected (if different InChI existed) and used to generate a molecular fingerprint. For each pair of molecular fingerprints Tanimoto: "For every unique 14-character InChIKey the most common InChI was selected (if different InChI existed) and used to generate a molecular fingerprint"
