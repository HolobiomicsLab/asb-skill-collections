---
name: molecular-fingerprint-structural-similarity-tanimoto
description: Use when when evaluating how well mass spectral similarity scores correlate
  with actual chemical structure for annotated spectral pairs (e.g., spectra with
  InChIKey metadata).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3370
  tools:
  - Spec2Vec
  - matchms
  - gensim
  - RDKit
  - NumPy
  - Numba
  - Pandas
  - scipy
  - NumPy / Pandas / SciPy
  techniques:
  - GC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1371/journal.pcbi.1008724
  title: Spec2Vec
evidence_spans:
- we introduce Spec2Vec, a novel spectral similarity score
- spec2vec (https://github.com/iomega/spec2vec). Both packages are freely available
  and can be installed via conda
- the implementations for the cosine score and the modified cosine score used can
  be found in the Python package matchms
- the implementations for the cosine score and the modified cosine score used can
  be found in the Python package matchms [31] (https://github.com/matchms/matchms)
- A Word2Vec [22] model is trained on all documents of a chosen dataset using gensim
  [37]
- Tanimoto similarity (Jaccard index) based on daylight-like molecular fingerprints,
  version 2020.03.2, 2048 bits, derived using rdkit
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: spec2vec_grounded
    doi: 10.1371/journal.pcbi.1008724
    title: Spec2Vec
  dedup_kept_from: spec2vec_grounded
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1008724
  all_source_dois:
  - 10.1371/journal.pcbi.1008724
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Molecular Fingerprint Structural Similarity (Tanimoto)

## Summary

Compute structural similarity between pairs of molecules using daylight-like fingerprints (RDKit, 2048 bits) and Tanimoto/Jaccard distance, enabling quantitative correlation of spectral similarity scores with underlying chemical structure. This skill is essential for benchmarking mass spectral similarity methods against ground-truth structural relationships.

## When to use

When evaluating how well mass spectral similarity scores correlate with actual chemical structure for annotated spectral pairs (e.g., spectra with InChIKey metadata). Use this skill as a gold-standard reference metric when comparing cosine, modified cosine, or embedding-based spectral similarity scores; correlation strength between spectral and structural similarity indicates which scoring method best captures chemical relatedness.

## When NOT to use

- Spectra without InChIKey or SMILES/InChI annotations—Tanimoto computation requires chemical structure identifiers; unannotated spectra cannot be structurally compared.
- GC-MS data or other instrumental modes where structure identity is already known through orthogonal means and spectral method validation is not the goal.
- When the research question is about spectral prediction or library matching rather than benchmarking spectral similarity methods themselves.

## Inputs

- InChIKey annotations for spectra (first 14 characters / planar InChIKeys preferred)
- Spectral similarity score matrices (all-pairs, any method: cosine, modified cosine, Spec2Vec, etc.)
- Canonical SMILES or InChI strings resolvable to RDKit molecule objects

## Outputs

- Mean Tanimoto structural similarity per spectral similarity score percentile (e.g., top 0.1%, top 1%)
- Correlation strength comparison table across spectral similarity methods
- Ranked spectrum pairs with paired spectral and structural similarity scores for error analysis

## How to apply

Generate RDKit daylight-like fingerprints (2048 bits) for all molecules represented in your spectral dataset with InChIKey annotations. Compute pairwise Tanimoto similarity (or Jaccard index) for all spectrum pairs that share valid InChIKey identifiers. Rank spectral similarity scores (from any method—cosine, modified cosine, Spec2Vec) in descending order, then extract the top percentile of pairs (e.g., top 0.1%). Calculate mean structural Tanimoto similarity for each top percentile subset and compare across spectral similarity methods. Higher mean Tanimoto at a given percentile indicates that spectral method's similarity scores more reliably correlate with structural similarity. The rationale: high-scoring spectral pairs should correspond to chemically similar molecules; poor correlation reveals false positives in the spectral method.

## Related tools

- **RDKit** (Generate daylight-like molecular fingerprints (2048 bits) from SMILES/InChI and compute Tanimoto similarity coefficients)
- **matchms** (Compute cosine and modified cosine spectral similarity scores to benchmark against Tanimoto structural similarity) — https://github.com/matchms/matchms
- **Spec2Vec** (Generate embedding-based spectral similarity scores for correlation comparison with Tanimoto structural similarity) — https://github.com/iomega/spec2vec
- **NumPy / Pandas / SciPy** (Rank similarity scores, filter percentiles, compute mean and correlation statistics across method comparisons)

## Examples

```
from rdkit import Chem; from rdkit.Chem import AllChem; import numpy as np; mols = [Chem.MolFromInchi(inchi) for inchi in inchi_list]; fps = [AllChem.GetMorganFingerprintAsBitVect(m, 2, nBits=2048) for m in mols if m]; tanimoto_matrix = np.array([[DataStructs.TanimotoSimilarity(fps[i], fps[j]) for j in range(len(fps))] for i in range(len(fps))]); top_01pct_pairs = np.argsort(spectral_scores.flatten())[-int(0.001*len(spectral_scores.flatten())):]; mean_tanimoto_top = tanimoto_matrix.flatten()[top_01pct_pairs].mean()
```

## Evaluation signals

- Mean Tanimoto structural similarity in top 0.1% spectral pairs is > 0.5 (indicating non-random chemical structure relationships at high similarity scores)
- Spec2Vec mean Tanimoto at top 0.1% is measurably higher than cosine or modified cosine mean Tanimoto at the same percentile, with reported difference and statistical significance
- Correlation curve (percentile vs. mean Tanimoto) is monotonically decreasing for all methods, confirming that lower spectral similarity thresholds correspond to lower structural similarity
- Pearson or Spearman correlation coefficient between spectral and structural similarity is reported for each method, with Spec2Vec showing ≥ ~0.3–0.5 improvement over cosine-based methods
- False positive rate (high spectral similarity but low structural similarity) is lower for Spec2Vec than cosine-based methods when compared at equivalent similarity score thresholds

## Limitations

- Tanimoto is computed only for spectra with InChIKey annotations; spectra lacking chemical identifiers are excluded, potentially biasing benchmarks toward well-annotated (often library) datasets.
- Daylight fingerprints (2048 bits, RDKit) capture 2D structural features but do not account for stereochemistry, 3D conformations, or ion adduct chemistry—two isomeric molecules may appear structurally identical despite different fragmentation behavior.
- Planar InChIKeys (first 14 characters) do not distinguish stereoisomers; if stereochemistry significantly affects fragmentation, true structural diversity may be underestimated and correlation values may be artificially inflated.
- Tanimoto similarity is symmetric and does not distinguish directionality; a spectral method may perform differently when querying A against B vs. B against A in network or library-search contexts.
- The reference Tanimoto metric itself is limited to the UniqueInchikey dataset (12,797 spectra with unique InChIKeys in the referenced work); generalization to larger, more diverse, or GC-MS datasets may not hold without retraining or dataset-specific calibration.

## Evidence

- [methods] Compute structural similarity (Tanimoto/Jaccard) on daylight-like fingerprints (RDKit, 2048 bits) for all spectrum pairs with InChIKey annotations.: "Compute structural similarity (Tanimoto/Jaccard) on daylight-like fingerprints (RDKit, 2048 bits) for all spectrum pairs with InChIKey annotations."
- [other] Spec2Vec similarity scores correlate stronger with structural similarity than cosine or modified cosine scores when evaluated at the top 0.1% of scoring pairs in the UniqueInchikey dataset.: "Spec2Vec similarity scores correlate stronger with structural similarity than cosine or modified cosine scores when evaluated at the top 0.1% of scoring pairs in the UniqueInchikey dataset."
- [results] high Spec2Vec spectrum similarity score correlates stronger with structural similarity than the cosine or modified cosine scores: "high Spec2Vec spectrum similarity score correlates stronger with structural similarity than the cosine or modified cosine scores"
- [results] The poorer correlation between cosine and modified cosine similarity and structural similarity can largely be explained by high false positive rates: "The poorer correlation between cosine and modified cosine similarity and structural similarity can largely be explained by high false positive rates"
- [other] keep only spectra with unique planar InChIKeys (first 14 characters, also termed planar InChIKeys): "keep only spectra with unique planar InChIKeys (first 14 characters, also termed planar InChIKeys)"
- [other] Rank all-pairs similarities by score descending, extract top 0.1% of pairs, and calculate mean Tanimoto similarity for each method: "Rank all-pairs similarities by score descending, extract top 0.1% of pairs, and calculate mean Tanimoto similarity for each method"
