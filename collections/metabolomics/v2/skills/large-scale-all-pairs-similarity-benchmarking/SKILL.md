---
name: large-scale-all-pairs-similarity-benchmarking
description: Use when you have multiple competing spectral similarity scoring methods (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3625
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Spec2Vec
  - matchms
  - gensim
  - RDKit
  - NumPy
  - Numba
  - Pandas
  - scipy
  - Word2Vec (gensim)
  - NumPy, Pandas, SciPy
derived_from:
- doi: 10.1371/journal.pcbi.1008724
  title: Spec2Vec
evidence_spans:
- we introduce Spec2Vec, a novel spectral similarity score
- spec2vec (https://github.com/iomega/spec2vec). Both packages are freely available and can be installed via conda
- the implementations for the cosine score and the modified cosine score used can be found in the Python package matchms
- the implementations for the cosine score and the modified cosine score used can be found in the Python package matchms [31] (https://github.com/matchms/matchms)
- A Word2Vec [22] model is trained on all documents of a chosen dataset using gensim [37]
- Tanimoto similarity (Jaccard index) based on daylight-like molecular fingerprints, version 2020.03.2, 2048 bits, derived using rdkit
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
---

# large-scale-all-pairs-similarity-benchmarking

## Summary

Systematically compute all-pairs similarity scores across multiple methods (Spec2Vec, cosine, modified cosine) on large MS/MS spectral datasets, then correlate the resulting similarity matrices with ground-truth structural similarity (Tanimoto fingerprint distance) to benchmark and compare method performance at aggregate levels (e.g., top 0.1% of pairs).

## When to use

You have multiple competing spectral similarity scoring methods (e.g., traditional cosine vs. learnt embeddings), want to rank them by how well they correlate with known chemical structure similarity across a substantial corpus of spectra (typically >10,000 spectra with unique structures), and need quantitative evidence of whether one method systematically outperforms another before deploying it in production molecular networking or library matching workflows.

## When NOT to use

- You have fewer than ~5,000 spectra with unique structures; sampling bias and statistical noise will dominate, making aggregate percentile slicing unreliable.
- Your spectra are GC-MS without neutral loss measurements; Spec2Vec was demonstrated only on LC-MS and neutral losses are a key feature—retraining or domain adaptation would be needed.
- You only want to compare two spectra or a small query set; use pairwise similarity directly without benchmarking infrastructure.
- You lack InChIKey or structural ground truth for the majority of your spectra; the correlation cannot be computed and the benchmarking goal is defeated.

## Inputs

- MS/MS spectra from large library (e.g., GNPS ALL_GNPS, 95,000+ spectra)
- InChIKey annotations (planar, first 14 characters)
- Precursor m/z and fragment peak data (m/z, relative intensity)
- Neutral loss metadata (optional, computed from precursor − peak)
- Pre-trained or trainable Word2Vec model (gensim CBOW architecture)
- Molecular structures or SMILES strings (for RDKit fingerprint generation)

## Outputs

- All-pairs Spec2Vec similarity score matrix (sparse or dense)
- All-pairs cosine similarity score matrix
- All-pairs modified cosine similarity score matrix
- All-pairs structural similarity matrix (Tanimoto/Jaccard on fingerprints)
- Comparison table: mean structural similarity in top 0.1% (or other percentile) for each scoring method
- Correlation coefficient or rank-correlation plot (e.g., Spearman ρ) between spectral and structural similarity per method

## How to apply

First, load pre-processed spectral datasets (e.g., AllPositive or UniqueInchikey subsets from GNPS) and filter to spectra with ≥10 fragment peaks, InChIKey annotations, and m/z in range [0, 1000]. Then, for each similarity method: (1) for Spec2Vec, train or retrieve a pre-trained Word2Vec model (CBOW, window 500, negative=5, 15–50 epochs), convert each spectrum to a document (peaks as '[redacted-email]' words, neutral losses 5–200 Da as '[redacted-email]'), compute cosine similarity between weighted word embeddings (weights = sqrt-normalized intensities), filter by parent mass scaling (max_peaks = 0.5 × parent_mass) and missing-fraction threshold (<0.05); (2) for cosine and modified cosine, remove peaks with relative intensity <0.01 of highest peak and compute via matchms (modified cosine also matches peaks shifted by precursor m/z difference). Next, compute all-pairs similarity score matrices for all spectra. In parallel, calculate structural similarity (Tanimoto or Jaccard) on RDKit daylight-like fingerprints (2048 bits) for all spectrum pairs with InChIKey annotations. Finally, rank all-pairs similarity scores by value descending, slice out the top percentile (e.g., top 0.1%), and calculate mean structural similarity for pairs in each top percentile; output comparison table showing correlation strength by method. The method's validity depends on whether the highest-scoring pairs by each method also exhibit high structural similarity—a strong correlation indicates the method learned or captured genuine chemical relationships.

## Related tools

- **Spec2Vec** (Primary learnt spectral similarity method; computes spectrum embeddings via Word2Vec and returns cosine distance between weighted peak/loss vectors) — https://github.com/iomega/spec2vec
- **matchms** (Spectrum data loading, filtering, metadata cleaning, and baseline cosine/modified cosine similarity computation) — https://github.com/matchms/matchms
- **Word2Vec (gensim)** (CBOW model training on spectrum documents to learn fragment ion and neutral loss embeddings)
- **RDKit** (Generate 2048-bit daylight-like molecular fingerprints from InChIKeys or SMILES for ground-truth structural similarity (Tanimoto) calculation)
- **NumPy, Pandas, SciPy** (Matrix operations, all-pairs similarity storage, ranking, correlation statistics (e.g., Spearman, Pearson))

## Examples

```
from matchms import Spectrum; from spec2vec import Spec2Vec, model_from_file; import numpy as np; spec2vec = Spec2Vec(model_from_file('path_to_model')); scores = [spec2vec.pair(spec1, spec2) for spec1, spec2 in all_pairs]; top_indices = np.argsort(scores)[-int(0.001*len(scores)):]; mean_tanimoto = np.mean([structural_sim[i] for i in top_indices])
```

## Evaluation signals

- Correlation coefficient (Spearman ρ or Pearson r) between method's top-percentile spectral similarity and structural similarity is higher for the proposed method (Spec2Vec) than baseline methods (cosine, modified cosine); threshold typically ρ > 0.6–0.7 for strong correlation.
- Sensitivity and specificity at the top 0.1% percentile: proposed method retrieves pairs with higher mean Tanimoto structural similarity (e.g., >0.5–0.6) than baselines; false positive rate (pairs scoring high in spectral similarity but low in structural) is lower.
- Ranked percentile slices are monotonically related to structural similarity across methods; i.e., top 0.01% > top 0.1% > top 1% in mean Tanimoto for the proposed method, indicating genuine learning of structure.
- Reproducibility: all-pairs score matrices computed independently on subset and full dataset yield identical top-percentile rankings (within numerical precision), indicating stability.
- No zero-division or NaN values in similarity matrices; all spectra with ≥10 peaks and InChIKey pass filtering and contribute valid pairs.

## Limitations

- Spec2Vec requires pre-training on a large, representative corpus of spectra; unknown fragment peaks or neutral losses not present in the training set will be assigned zero embeddings or estimated via a missing-fraction threshold, potentially degrading similarity for spectra with novel features. Retraining may be necessary for datasets with low feature overlap.
- Performance demonstrated only on LC-MS data with neutral loss information; GC-MS, where neutral losses are typically not measured, was not benchmarked and may require model retraining or feature engineering.
- The method assumes all spectra in the benchmarking set are correctly annotated with InChIKeys; mislabeled or ambiguous structural assignments will introduce noise into the ground-truth correlation and bias benchmarking results.
- All-pairs computation scales as O(n²) in memory and time; for >100,000 spectra, sparse data structures or batching is necessary to avoid memory exhaustion.
- Cosine-based methods exhibit high false positive rates when molecules have high spectral similarity but differ in multiple structural locations; this limitation is inherent to the method, not the benchmarking workflow, but should be noted when interpreting low correlations.

## Evidence

- [abstract] Spec2Vec scores correlate better with structural similarity than cosine-based scores: "Spec2Vec scores correlate better with structural similarity than cosine-based scores"
- [results] High Spec2Vec spectrum similarity score correlates stronger with structural similarity than cosine or modified cosine scores: "high Spec2Vec spectrum similarity score correlates stronger with structural similarity than the cosine or modified cosine scores"
- [other] Top 0.1% percentile filtering applied to benchmark spectral similarity methods: "Rank all-pairs similarities by score descending, extract top 0.1% of pairs, and calculate mean Tanimoto similarity for each method"
- [methods] Spec2Vec similarity computation via weighted word embeddings and cosine distance: "compute all-pairs spectrum vector similarities using weighted sum of word embeddings (weight = normalized intensity, sqrt applied), then cosine distance"
- [methods] Spectrum document representation with peaks and neutral losses as words: "every peak is represented by a word that contains its position up to a defined decimal precision ("[redacted-email]"). In addition to all peaks of a spectrum, neutral losses between 5.0 and 200.0 Da were"
- [other] Structural similarity computed via RDKit fingerprint Tanimoto distance: "Compute structural similarity (Tanimoto/Jaccard) on daylight-like fingerprints (RDKit, 2048 bits) for all spectrum pairs with InChIKey annotations"
- [methods] Word2Vec model architecture and training parameters: "train from scratch using CBOW with window-size 500, negative sampling (negative=5), 15–50 epochs on spectrum documents"
- [methods] matchms library provides cosine and modified cosine score implementations: "the implementations for the cosine score and the modified cosine score used can be found in the Python package matchms"
- [discussion] Spec2Vec performance limitation on GC-MS data: "we have only demonstrated performance on LC-MS data and not yet assessed Spec2Vec for GC-MS data. For GC-MS, neutral losses are usually not measured"
- [discussion] Training data requirement and potential retraining need for Spec2Vec: "one limitation of Spec2Vec as compared to cosine scores is that it needs training data to learn the fragment peak relationships; however, since this not necessarily needs to be library spectra"
