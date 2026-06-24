---
name: tanimoto-similarity-pairwise-calculation
description: Use when you have a collection of molecular fingerprint vectors (such
  as biosynfoni count fingerprints) and need to measure structural similarity between
  all pairs of molecules.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0154
  tools:
  - biosynfoni
  - pip
  - RDKit
  license_tier: open
derived_from:
- doi: 10.26434/chemrxiv-2025-cwq74
  title: biosynfoni
evidence_spans:
- biosynfoni
- a biosynformatic molecular fingerprint tailored to natural product chem- and bioinformatic
  research
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

# tanimoto-similarity-pairwise-calculation

## Summary

Compute pairwise Tanimoto similarity coefficients across a collection of molecular fingerprint vectors to characterize structural similarity patterns. This skill quantifies how similar pairs of fingerprints are, enabling downstream analysis of fingerprint sparsity and structural diversity in molecular datasets.

## When to use

Apply this skill when you have a collection of molecular fingerprint vectors (such as biosynfoni count fingerprints) and need to measure structural similarity between all pairs of molecules. Use it to generate a pairwise similarity matrix that reveals clustering tendencies, redundancy, or diversity in your fingerprint dataset.

## When NOT to use

- Fingerprints have not yet been computed or are missing for some molecules in the dataset
- You need per-bit similarity or local feature matching rather than global fingerprint similarity
- Input vectors are not molecular fingerprints (e.g., raw chemical descriptors without fingerprint encoding)

## Inputs

- collection of molecular fingerprint vectors (e.g., biosynfoni count fingerprints or binary fingerprints)
- fingerprint vector matrix or array (samples × bits)

## Outputs

- pairwise Tanimoto similarity matrix (samples × samples)
- summary statistics table (mean, median, standard deviation of similarity scores)
- distribution plot of pairwise Tanimoto similarity coefficients

## How to apply

Load all fingerprint vectors from your dataset (e.g., from the Zenodo biosynfoni deposit or local biosynfoni-generated fingerprints). Compute Tanimoto similarity coefficients for every pair of fingerprint vectors in the collection—this metric ranges from 0 (completely dissimilar) to 1 (identical). Calculate summary statistics on the resulting similarity scores (mean, median, standard deviation) and generate distribution plots (histogram or density) to visualize the shape and range of pairwise similarities. The Tanimoto coefficient is appropriate for count fingerprints and binary fingerprints alike; verify that your summary statistics table contains all coefficients with no missing values and that the distribution plot displays expected shapes consistent with your dataset's structural diversity.

## Related tools

- **biosynfoni** (generates molecular fingerprint vectors (count fingerprints) that serve as input to pairwise similarity calculation) — https://github.com/lucinamay/biosynfoni
- **RDKit** (provides molecular fingerprint generation and similarity metric implementations (installed as dependency of biosynfoni))
- **pip** (package manager for installing biosynfoni and its dependencies)

## Examples

```
from biosynfoni import Biosynfoni
from rdkit import Chem
import numpy as np
from scipy.spatial.distance import pdist

fingerprints = [Biosynfoni(Chem.MolFromSmiles(smi)).fingerprint for smi in smiles_list]
similarities = 1 - pdist(fingerprints, metric='jaccard')
similarity_matrix = np.mean(similarities)
```

## Evaluation signals

- Pairwise Tanimoto similarity matrix has shape (N, N) where N equals the number of fingerprints, with all values in the range [0, 1]
- Summary statistics table contains mean, median, and standard deviation of all pairwise similarities with no missing values
- Distribution plot of Tanimoto similarity values shows expected shape (e.g., right-skewed or normal depending on dataset diversity)
- Diagonal of the similarity matrix equals 1.0 (each fingerprint is identical to itself)
- Similarity matrix is symmetric (similarity of fingerprint A to B equals similarity of B to A)

## Limitations

- Tanimoto similarity is sensitive to fingerprint bit-frequency and sparsity characteristics; dense fingerprints may yield high baseline similarities
- Computational cost scales as O(N²) for N fingerprints; large datasets (>100k molecules) may require approximate or batch-based methods
- Tanimoto coefficient treats all bit positions equally and does not account for chemical domain knowledge about feature importance

## Evidence

- [other] Compute pairwise Tanimoto similarity coefficients for all fingerprint vector pairs.: "Compute pairwise Tanimoto similarity coefficients for all fingerprint vector pairs."
- [other] biosynfoni is a molecular fingerprint resource designed for natural product chemistry and bioinformatic research, providing a dataset suitable for statistical characterization of fingerprint properties.: "biosynfoni is a molecular fingerprint resource designed for natural product chemistry and bioinformatic research"
- [other] Generate summary statistics table including mean, median, and standard deviation of bit-frequencies, sparsity, and similarity scores.: "Generate summary statistics table including mean, median, and standard deviation of bit-frequencies, sparsity, and similarity scores."
- [other] Create distribution plots (histogram/density) for bit-frequencies, sparsity values, and pairwise Tanimoto similarity.: "Create distribution plots (histogram/density) for bit-frequencies, sparsity values, and pairwise Tanimoto similarity."
- [readme] a biosynformatic molecular fingerprint tailored to natural product chem- and bioinformatic research: "a biosynformatic molecular fingerprint tailored to natural product chem- and bioinformatic research"
