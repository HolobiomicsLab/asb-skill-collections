---
name: compound-ground-truth-matching
description: Use when when you have pre-computed embeddings for query and reference MS/MS spectra, computed their cosine similarity matrix, and need to measure retrieval success by verifying whether the correct compound (identified by SMILES string) appears in the top-1, top-5, or top-10 ranked candidates from.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - PyTorch
  - CUDA
  - numba
  - top_k_indices
  - cosine_similarity
  - read_raw_spectra
  - embedding
derived_from:
- doi: 10.1021/acs.analchem.5c02655
  title: SpecEmbedding
evidence_spans:
- Python：3.12
- PyTorch：2.6.0 + CUDA 12.4
- 该装饰器来自 numba
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_specembedding_cq
    doi: 10.1021/acs.analchem.5c02655
    title: SpecEmbedding
  dedup_kept_from: coll_specembedding_cq
schema_version: 0.2.0
---

# compound-ground-truth-matching

## Summary

Evaluate MS/MS spectral retrieval by checking whether the true compound (ground-truth SMILES) appears in the top-k retrieved reference spectra. This metric quantifies hit@k performance across 10-fold cross-validation splits to measure compound identification accuracy.

## When to use

When you have pre-computed embeddings for query and reference MS/MS spectra, computed their cosine similarity matrix, and need to measure retrieval success by verifying whether the correct compound (identified by SMILES string) appears in the top-1, top-5, or top-10 ranked candidates from a reference spectral library (GNPS, MoNA, MTBLS1572, MassBank, or MassSpecGym).

## When NOT to use

- Input spectra lack ground-truth SMILES or compound annotations — matching cannot be performed.
- Query and reference sets are not strictly separated (e.g., query spectra appear in reference set) — this violates the evaluation design and biases metrics upward.
- You need per-spectrum confidence scores or ranking quality metrics beyond binary hit/miss — use ranking metrics like MRR or NDCG instead.

## Inputs

- cosine similarity matrix (query × reference embeddings)
- query spectra with ground-truth SMILES annotations
- reference spectra with SMILES identifiers
- top-k candidate indices for each query

## Outputs

- hit@k metric (proportion of queries with true compound in top-k)
- hit@k average across 10 splits
- hit@k standard deviation across 10 splits

## How to apply

For each of the 10 query/reference splits, extract the top-k candidate indices (k=1, 5, 10) from the cosine similarity matrix using top_k_indices. For each query spectrum, retrieve its ground-truth SMILES identifier and check whether that compound appears in the top-k retrieved reference spectra. Count hits (matches) and non-hits separately for each k value. Aggregate hit counts across all query spectra within a split to compute hit@k as a proportion. Repeat across all 10 splits and report the mean hit@k and standard deviation. The rationale is that retention of the original MSBERT training set split ensures fair comparison while random test-set splitting measures generalization.

## Related tools

- **top_k_indices** (Extract indices of top-k highest-scoring candidates from cosine similarity matrix for each query spectrum) — https://github.com/sword-nan/SpecEmbedding
- **cosine_similarity** (Compute pairwise cosine similarity scores between query and reference embeddings to rank candidates) — https://github.com/sword-nan/SpecEmbedding
- **read_raw_spectra** (Load query and reference MS/MS spectra from .msp files with SMILES and metadata intact) — https://github.com/sword-nan/SpecEmbedding
- **embedding** (Generate embeddings for query and reference spectra using the pre-trained SpecEmbedding model) — https://github.com/sword-nan/SpecEmbedding

## Examples

```
from SpecEmbedding.utils.model import top_k_indices; indices = top_k_indices(cosine_scores, k=1); hits = sum(1 for i, idx in enumerate(indices[:, 0]) if q_spectra[i].get('smiles') == r_spectra[idx].get('smiles')); hit_at_1 = hits / len(q_spectra)
```

## Evaluation signals

- hit@k values are bounded in [0, 1] and reported separately for k=1, k=5, k=10
- Standard deviation is calculated correctly across exactly 10 independent splits
- hit@k monotonically increases (or stays constant) as k increases (e.g., hit@1 ≤ hit@5 ≤ hit@10)
- Query and reference set splits are confirmed disjoint in each fold (no leakage)
- Ground-truth SMILES in query spectra exactly match identifiers in top-k retrieved reference spectra using string equality

## Limitations

- Performance metric is sensitive to data quality — malformed or invalid SMILES strings must be removed from both query and reference sets beforehand, otherwise false negatives occur.
- Hit@k is a discrete binary metric per query and cannot distinguish near-misses (e.g., correct compound ranked at position k+1).
- Evaluation assumes single best-match per query (one true compound SMILES); multi-target or isomeric scenarios require adaptation.
- On Windows, @njit decorators from numba library may cause numerical errors in cosine similarity computation; decorators should be commented out.
- Cross-validation scheme is asymmetric — training set split is fixed (from MSBERT) while only test sets are randomly split; results are not strictly k-fold cross-validation.

## Evidence

- [other] Calculate hit@k by checking if the true compound (ground truth SMILES) appears in the top-k retrieved references for each query: "Calculate hit@k by checking if the true compound (ground truth SMILES) appears in the top-k retrieved references for each query spectrum."
- [other] Extract top-k candidate indices (k = 1, 5, 10) using top_k_indices for each query spectrum: "Extract top-k candidate indices (k = 1, 5, 10) using top_k_indices for each query spectrum."
- [intro] 10-fold cross-validation splits for evaluation: "we strictly retained the original training set split used by MSBERT and only applied random splitting to the test sets. Final results are reported as the average and standard deviation across the 10"
- [intro] Removal of entries with malformed or invalid SMILES strings: "To further improve data quality, we removed entries with malformed or invalid SMILES strings"
- [other] Aggregate hit@k across all 10 splits and compute mean and standard deviation for each k value: "Aggregate hit@k across all 10 splits and compute mean and standard deviation for each k value."
- [readme] Note for Windows Users: When running on Windows, you may encounter numerical errors during cosine similarity computation: "⚠️ Note for Windows Users: When running on Windows, you may encounter numerical errors during cosine similarity computation. This is caused by @njit decorators from the numba library."
