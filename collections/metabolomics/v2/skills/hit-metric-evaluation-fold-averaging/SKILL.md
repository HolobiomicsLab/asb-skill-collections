---
name: hit-metric-evaluation-fold-averaging
description: Use when when you have a trained MS/MS spectral embedding model and need
  to measure compound identification accuracy on a held-out test set, but want to
  mitigate sensitivity to a single random train/test split. Use this skill if the
  original training set split is fixed (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - Python
  - PyTorch
  - ModelTester
  - Tokenizer
  - cosine_similarity function
  - top_k_indices function
  - SpecEmbedding-Comparison
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.5c02655
  title: SpecEmbedding
evidence_spans:
- Python：3.12
- PyTorch：2.6.0 + CUDA 12.4
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c02655
  all_source_dois:
  - 10.1021/acs.analchem.5c02655
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# hit-metric-evaluation-fold-averaging

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Evaluate spectral retrieval model performance using hit-rate metrics (e.g., top-1 hit rate) computed independently across 10 random query/reference test-set partitions, then aggregate results as mean and standard deviation to characterize model robustness and generalization.

## When to use

When you have a trained MS/MS spectral embedding model and need to measure compound identification accuracy on a held-out test set, but want to mitigate sensitivity to a single random train/test split. Use this skill if the original training set split is fixed (e.g., from MSBERT) and you can only randomize within the test partition to create multiple evaluation folds.

## When NOT to use

- Training set has not been locked; you plan to re-randomize the entire dataset (use stratified k-fold cross-validation instead).
- You have no ground-truth compound identity for query spectra; hit-rate metric requires known labels.
- Test set is too small (<50 samples total) to meaningfully subdivide into 10 folds without severe sparsity.

## Inputs

- Pre-trained SpecEmbedding model (PyTorch checkpoint)
- Test-set spectra in .msp format (GNPS, MoNA, or MTBLS1572)
- Tokenizer instance (configured for MS/MS spectral tokens)
- Fixed random seeds or seed list for 10 fold generations

## Outputs

- Hit-rate metric per fold (list of 10 floats, range [0, 1])
- Mean hit rate across 10 folds
- Standard deviation of hit rate across 10 folds
- Fold-level metadata (partition index, split seed, sample counts, top-k indices)

## How to apply

First, load the pre-trained model and the fixed test set (with training set partition locked). Generate 10 distinct random splits of the test set, each producing a separate query and reference subset (e.g., 50/50 or 80/20); record the random seed and split ratio for each fold for reproducibility. For each fold, compute query embeddings using the tokenizer and model, generate reference embeddings, compute the cosine similarity matrix between all query–reference pairs, and record the top-k hit counts (e.g., whether the true compound appears in the top-1 retrieval for each query). After all 10 folds complete, calculate the hit rate (hit count / total queries) for each fold, then report the mean hit rate and standard deviation across the 10 folds. This approach isolates evaluation variance from training variance and provides a confidence interval on retrieval performance.

## Related tools

- **ModelTester** (Orchestrates embedding generation and cosine similarity computation for query and reference spectra across a fold) — https://github.com/sword-nan/SpecEmbedding
- **Tokenizer** (Converts raw MS/MS spectral m/z and intensity pairs into model-compatible token sequences) — https://github.com/sword-nan/SpecEmbedding
- **cosine_similarity function** (Computes pairwise cosine similarity matrix between query and reference embeddings for each fold) — https://github.com/sword-nan/SpecEmbedding
- **top_k_indices function** (Retrieves ranked indices of top-k most similar reference spectra for each query spectrum) — https://github.com/sword-nan/SpecEmbedding
- **SpecEmbedding-Comparison** (Reference repository containing hit-rate metric computation and evaluation harness for 10-fold averaging) — https://github.com/sword-nan/SpecEmbedding-Comparison

## Examples

```
from SpecEmbedding.utils.model import embedding, cosine_similarity, top_k_indices, load_tanimoto_supcon_aug_model
from SpecEmbedding.utils.clean import read_raw_spectra
from SpecEmbedding.trainer.trainer import ModelTester
from SpecEmbedding.data.tokenizer import Tokenizer
import numpy as np
q = read_raw_spectra('./fold_1_query.msp')
r = read_raw_spectra('./fold_1_reference.msp')
tokenizer = Tokenizer(100, True)
model = load_tanimoto_supcon_aug_model('cpu')
tester = ModelTester(model, 'cpu', False)
q_emb, _ = embedding(tester, tokenizer, 512, q, False)
r_emb, _ = embedding(tester, tokenizer, 512, r, False)
sim = cosine_similarity(q_emb, r_emb)
hits = (top_k_indices(sim, 1)[:, 0] == np.arange(len(q))).sum()
hit_rate = hits / len(q)
print(f'Fold 1 hit rate: {hit_rate:.4f}')
```

## Evaluation signals

- All 10 folds must be mutually exclusive within the test set (no query spectrum appears in multiple folds' reference sets; verify by set intersection check).
- Standard deviation across 10 folds should be ≤ 10 % of mean hit rate; larger variance suggests instability or insufficient fold size.
- Mean hit rate must be in range [0, 1]; per-fold hit rates are non-negative integers divided by fold size.
- Metadata for each fold must record split seed, query/reference sample counts, and total matches; verify counts sum to test-set size.
- No test-set spectrum should appear in the training set (verify by SMILES/ID deduplication between locked training partition and all 10 test folds).

## Limitations

- Requires the original MSBERT training/test split to be strictly preserved; if training set boundaries shift, results are not comparable to prior benchmarks.
- Hit-rate metric alone does not distinguish between near-miss (ranked 2–5) and far-miss (ranked >100) retrievals; consider complementary metrics (e.g., mean reciprocal rank, nDCG) for finer resolution.
- Random splitting of test set assumes uniform distribution of compound classes; if test set is heavily imbalanced (e.g., one family dominates), fold-level hit rates may vary widely and standard deviation may be inflated.
- On Windows systems, numba @njit decorators in cosine_similarity and related functions may produce numerical errors; users must comment out @njit decorators or use Linux/WSL for reliable computation.

## Evidence

- [other] The evaluation methodology retains the original training set split from MSBERT while applying random splitting only to test sets, generating 10 distinct query/reference partitions for evaluation and reporting results as average and standard deviation across the 10 splits.: "we strictly retained the original training set split used by MSBERT and only applied random splitting to the test sets. Final results are reported as the average and standard deviation across the 10"
- [methods] The workflow involves loading pre-cleaned spectral data with original MSBERT training/test split, extracting only the test partition, randomly re-partitioning it 10 times into query/reference pairs, storing each partition separately with metadata, and validating mutual exclusivity and training/test separation.: "Load the pre-cleaned spectral data (GNPS, MoNA, MTBLS1572) with the original MSBERT training/test split already applied. Extract only the test partition and confirm training split is held fixed."
- [intro] All cleaned data and the 10-fold query/reference splits are available on figshare with preprocessing scripts and reproducibility metadata.: "All cleaned data, along with the preprocessing scripts and 10-fold query/reference splits used for evaluation, are available on figshare"
- [readme] Demonstrates the concrete workflow of loading spectra, initializing tokenizer and device, loading model, generating embeddings for query and reference spectra, computing cosine similarity matrix, and retrieving top-k candidate indices.: "Load query and reference spectra; Initialize tokenizer and device; Define the SiameseModel architecture; Initialize the ModelTester; Generate embeddings for query and reference spectra; Compute the"
- [readme] Windows users may encounter numerical errors during cosine similarity computation due to numba @njit decorators; the fix is to comment out all @njit decorators.: "When running on Windows, you may encounter numerical errors during cosine similarity computation. This is caused by @njit decorators from the numba library. You can fix it by commenting out all @njit"
