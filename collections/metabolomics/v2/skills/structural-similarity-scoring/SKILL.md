---
name: structural-similarity-scoring
description: Use when when you have a collection of mass spectra with annotated chemical structures (SMILES/InChI) and need to generate structural similarity labels to train or validate a model that predicts molecular similarity from spectral pairs.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3627
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3375
  tools:
  - RDKit
  - matchms
  - Python
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1186/s13321-021-00558-4
  title: MS2DeepScore
evidence_spans:
- Unless noted otherwise, we used Tanimoto scores on RDKit [23] Daylight fingerprints (2048 bits) to compute structural similarities.
- Unless noted otherwise, we used Tanimoto scores on RDKit [23] Daylight fingerprints (2048 bits) to compute structural similarities
- Metadata was cleaned and checked using matchms [18] version 0.8.2, which included cleaning compound names, extracting adduct information from the given metadata, moving metadata to consistent fields
- For each pair of molecular fingerprints Tanimoto scores were calculated, indicating the structural similarity of that pair. (as implemented in matchms [18])
- Our MS2DeepScore Python library offers two types of data generators, one which iterates over all unique InChIKeys (DataGeneratorAllInchikeys) and one which iterates over all spectra and was used for
- Our MS2DeepScore Python library offers two types of data generators
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_biotransformer_3_0_cq
    doi: 10.1093/nar/gkac408
    title: BioTransformer 3.0
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Structural Similarity Scoring

## Summary

Compute pairwise Tanimoto structural-similarity scores between molecular structures using RDKit Daylight fingerprints, generating a label matrix for training deep learning models on tandem mass spectra. This skill quantifies structural similarity as ground-truth targets for predicting chemical relationships from MS/MS spectral data.

## When to use

When you have a collection of mass spectra with annotated chemical structures (SMILES/InChI) and need to generate structural similarity labels to train or validate a model that predicts molecular similarity from spectral pairs. Specifically, use this when preparing training targets for a neural network that must learn to infer Tanimoto scores or other structural similarity metrics directly from MS/MS spectra without pre-computing fingerprints at inference time.

## When NOT to use

- When input spectra lack chemical structure annotations (SMILES/InChI/InChIKey); fingerprints cannot be generated without molecular structures.
- When the goal is to compute spectral similarity directly (cosine similarity, modified cosine, etc.); structural similarity and spectral similarity are orthogonal metrics.
- When stereoisomerism must be preserved as distinct; InChIKey notation (14-character form) disregards stereoisomerism, collapsing stereoisomers into one key.

## Inputs

- Cleaned MS/MS spectra dataset (matchms Spectrum objects or equivalent metadata table)
- InChIKey annotations (14-character strings, one per spectrum or unique molecule)
- SMILES or InChI chemical structure strings (at least one per unique InChIKey)

## Outputs

- Tanimoto similarity score matrix (N × N symmetric float array, where N = number of unique InChIKeys)
- RDKit Daylight fingerprint collection (2048-bit binary vectors per unique InChIKey)
- Structured label data with (InChIKey_1, InChIKey_2, Tanimoto_score) tuples for model training

## How to apply

Load the cleaned MS/MS spectra dataset with InChIKey and SMILES/InChI annotations. For each unique 14-character InChIKey, extract the most common InChI annotation (handling cases where multiple InChI strings map to the same InChIKey). Generate 2048-bit RDKit Daylight fingerprints for each unique InChIKey using matchms and RDKit. Compute pairwise Tanimoto similarity scores between all fingerprint pairs to produce a symmetric N×N label matrix, where N is the number of unique InChIKeys. Store this matrix as the training target, ensuring balanced sampling across similarity ranges during downstream model training to avoid bias toward high or low similarity regions.

## Related tools

- **RDKit** (Generates 2048-bit Daylight fingerprints from SMILES/InChI and computes pairwise Tanimoto similarity scores between fingerprints)
- **matchms** (Cleans and standardizes MS/MS spectrum metadata; extracts InChI/SMILES and provides data structures for coupling spectral data with chemical annotations) — https://github.com/matchms/matchms

## Examples

```
from rdkit import Chem; from rdkit.Chem import AllChem; import numpy as np; fps = [AllChem.GetMorganFingerprintAsBitVect(Chem.MolFromSmiles(smiles), 2, nBits=2048) for smiles in smiles_list]; similarity_matrix = np.array([[DataStructs.TanimotoSimilarity(fps[i], fps[j]) for j in range(len(fps))] for i in range(len(fps))])
```

## Evaluation signals

- Tanimoto score matrix is symmetric (score[i,j] == score[j,i]) and diagonal entries equal 1.0 (perfect self-similarity)
- All Tanimoto scores fall in the valid range [0.0, 1.0]; no NaN, Inf, or out-of-range values
- Matrix dimensions are N × N where N equals the count of unique InChIKeys in the dataset; verify no molecules were dropped during InChIKey aggregation
- Histogram of Tanimoto scores shows roughly balanced representation across bins (0.0–0.1, 0.1–0.2, …, 0.9–1.0) to confirm the label matrix spans chemical diversity and avoids degenerate clustering around one similarity value
- Spot-check: manually verify a few high-similarity pairs (score > 0.8) and low-similarity pairs (score < 0.2) by inspecting SMILES structures; similar molecules should have structurally recognizable overlap or differences

## Limitations

- InChIKey collapsing: the 14-character InChIKey disregards stereoisomerism, so cis/trans isomers and enantiomers are merged into a single key; if stereoisomeric discrimination is critical, use the full InChI key or structure-level metadata instead.
- Fingerprint resolution: 2048-bit Daylight fingerprints may not capture subtle structural distinctions relevant to some chemical classes (e.g., very large macrocycles, inorganics); consider higher bit-depths or alternative fingerprinting schemes for specialized datasets.
- Missing structures: spectra without SMILES or InChI annotations are excluded, potentially biasing the training set toward well-characterized compounds; the article reports 109,734 spectra in training but 210,407 total spectra retrieved, indicating ~48% of spectra were discarded due to missing annotations.
- Annotation ambiguity: multiple different InChI strings can theoretically map to the same InChIKey (though rare); the workflow selects the most common InChI, but this choice may introduce silent conflicts in edge cases.
- Computational cost: computing all pairwise Tanimoto scores scales as O(N²) and becomes memory-intensive for datasets with >100,000 unique molecules; the article's 15,062 unique InChIKeys produce a ~114 MB matrix at float32 precision.

## Evidence

- [methods] For every unique 14-character InChIKey the most common InChI was selected (if different InChI existed) and used to generate a molecular fingerprint. For each pair of molecular fingerprints Tanimoto: "For every unique 14-character InChIKey the most common InChI was selected (if different InChI existed) and used to generate a molecular fingerprint. For each pair of molecular fingerprints Tanimoto"
- [other] RDKit Daylight fingerprints (2048 bits) are generated per unique InChIKey, and pairwise Tanimoto scores are computed between all fingerprint pairs: "RDKit Daylight fingerprints (2048 bits) are generated per unique InChIKey, and pairwise Tanimoto scores are computed between all fingerprint pairs to quantify structural similarity as training targets"
- [methods] Unless noted otherwise, we used Tanimoto scores on RDKit [23] Daylight fingerprints (2048 bits) to compute structural similarities: "Unless noted otherwise, we used Tanimoto scores on RDKit [23] Daylight fingerprints (2048 bits) to compute structural similarities"
- [other] Load the cleaned and annotated MS/MS spectra dataset (109,734 spectra, 184,698 with InChIKey and SMILES/InChI) from GNPS. Extract the most common InChI for each unique 14-character InChIKey: "Load the cleaned and annotated MS/MS spectra dataset (109,734 spectra, 184,698 with InChIKey and SMILES/InChI) from GNPS. Extract the most common InChI for each unique 14-character InChIKey"
- [other] Construct and save the 15,062 × 15,062 Tanimoto score matrix as the structural similarity label matrix for model training: "Construct and save the 15,062 × 15,062 Tanimoto score matrix as the structural similarity label matrix for model training"
- [methods] Metadata was cleaned and checked using matchms [18] version 0.8.2, which included cleaning compound names, extracting adduct information from the given metadata, moving metadata to consistent fields: "Metadata was cleaned and checked using matchms [18] version 0.8.2, which included cleaning compound names, extracting adduct information"
- [results] The resulting training data set contains chemical structure annotations for 109,734 spectra… The dataset contains 15,062 different molecules (disregarding stereoisomerism): "The dataset contains 15,062 different molecules (disregarding stereoisomerism)"
