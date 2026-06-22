---
name: cross-split-metric-aggregation
description: 'Use when when you have a pre-trained model and need to report stable, generalizable performance on a fixed training set with multiple held-out test splits. Specifically: when you have 10 (or n) random query/reference splits on the same dataset (e.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3745
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - PyTorch
  - CUDA
  - numba
  - SpecEmbedding
  - Tokenizer
  - cosine_similarity
  - ModelTester
  - top_k_indices
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.5c02655
  title: SpecEmbedding
- doi: 10.6084/m9.figshare.28876751.v2
  title: ''
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c02655
  all_source_dois:
  - 10.1021/acs.analchem.5c02655
  - 10.6084/m9.figshare.28876751.v2
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# cross-split-metric-aggregation

## Summary

Compute and aggregate retrieval performance metrics (hit@k) across multiple independent train/test splits to obtain robust mean and standard deviation estimates. This skill enables reproducible, split-independent evaluation of spectral embedding models on benchmark datasets.

## When to use

When you have a pre-trained model and need to report stable, generalizable performance on a fixed training set with multiple held-out test splits. Specifically: when you have 10 (or n) random query/reference splits on the same dataset (e.g., GNPS, MoNA, MTBLS1572), and you want to report average hit@k and standard deviation rather than a single-split result that may be sensitive to the random split choice.

## When NOT to use

- Input is a single train/test split with no replicates — use single-split evaluation instead.
- You are training a new model and need per-epoch validation metrics — use cross-validation during training.
- Query or reference sets contain entries with malformed or invalid SMILES — apply data cleaning first.

## Inputs

- n pre-computed query/reference splits (MS/MS spectra in .msp format)
- pre-trained SpecEmbedding model (tanimoto-supcon-aug variant)
- Tokenizer (vocabulary size 100, normalized flag)
- query spectra array
- reference spectra array
- ground-truth SMILES annotations

## Outputs

- hit@k scores per split (k=1, 5, 10)
- aggregated hit@k mean across n splits
- aggregated hit@k standard deviation across n splits
- cosine similarity matrix (query × reference)

## How to apply

Load each of the n pre-computed splits (query and reference spectra). For each split: (1) generate embeddings using the pre-trained model with consistent tokenizer settings (vocabulary size 100, normalized=true); (2) compute the cosine similarity matrix between query and reference embeddings; (3) extract top-k indices (k=1, 5, 10) for each query; (4) calculate hit@k by checking if the ground-truth SMILES appears in the top-k retrieved references. After processing all splits, aggregate hit@k scores across splits and compute mean and standard deviation for each k value. Critically, retain the original training set split and apply random splitting only to test sets to ensure fair comparison with prior work (e.g., MSBERT).

## Related tools

- **SpecEmbedding** (Pre-trained deep learning model that generates MS/MS spectral embeddings using sinusoidal positional encoding and supervised contrastive learning; loaded via load_tanimoto_supcon_aug_model()) — https://github.com/sword-nan/SpecEmbedding
- **Tokenizer** (Converts MS/MS spectra into token sequences for model input; initialized with vocabulary size 100 and normalized flag true) — https://github.com/sword-nan/SpecEmbedding
- **cosine_similarity** (Computes pairwise cosine similarity matrix between query and reference embeddings to rank retrieval candidates) — https://github.com/sword-nan/SpecEmbedding
- **ModelTester** (Orchestrates embedding generation and evaluation; wraps the model and tokenizer for batch processing) — https://github.com/sword-nan/SpecEmbedding
- **top_k_indices** (Extracts indices of top-k most similar reference spectra from cosine similarity matrix for each query) — https://github.com/sword-nan/SpecEmbedding
- **PyTorch** (Deep learning framework for model inference; version 2.6.0 with CUDA 12.4)

## Examples

```
from SpecEmbedding.utils.model import embedding, cosine_similarity, load_tanimoto_supcon_aug_model, top_k_indices
from SpecEmbedding.utils.clean import read_raw_spectra
from SpecEmbedding.trainer.trainer import ModelTester
from SpecEmbedding.data.tokenizer import Tokenizer
import numpy as np
hits = []
for split_id in range(10):
    q = read_raw_spectra(f'./split_{split_id}/q.msp')
    r = read_raw_spectra(f'./split_{split_id}/r.msp')
    tokenizer = Tokenizer(100, True)
    model = load_tanimoto_supcon_aug_model('cpu')
    tester = ModelTester(model, 'cpu', False)
    q_emb, _ = embedding(tester, tokenizer, 512, q, False)
    r_emb, _ = embedding(tester, tokenizer, 512, r, False)
    scores = cosine_similarity(q_emb, r_emb)
    indices = top_k_indices(scores, 1)
    hit = sum(1 for i, idx in enumerate(indices[:, 0]) if q[i]['smiles'] == r[idx]['smiles']) / len(q)
    hits.append(hit)
print(f'hit@1: {np.mean(hits):.4f} ± {np.std(hits):.4f}')
```

## Evaluation signals

- Verify that hit@k mean and standard deviation are computed across exactly n splits with no missing or duplicate splits.
- Confirm that hit@k values for each k (1, 5, 10) are in the range [0, 1] and that hit@1 ≤ hit@5 ≤ hit@10 (monotonicity).
- Check that standard deviation is non-negative and reflects split-to-split variability; low SD suggests stable performance across splits.
- Validate that the original training set split was retained and only test sets were randomly re-split (compare against MSBERT's original split if available).
- Ensure ground-truth compound matching uses exact SMILES string comparison from top-k retrieved references.

## Limitations

- Windows users may encounter numerical errors during cosine similarity computation due to @njit decorators from numba; workaround is to comment out all @njit decorators.
- The skill assumes pre-computed splits are available; generating new splits requires separate infrastructure for reproducible random partitioning.
- Performance metrics depend critically on data quality (malformed SMILES removed); if source data is uncleaned, results may be unreliable.
- Batch size (512) and device (CPU/GPU) choice may affect memory usage and runtime but should not affect final metric values.

## Evidence

- [other] Load the pre-computed 10 query/reference splits from figshare: "Load the pre-computed 10 query/reference splits from figshare (https://doi.org/10.6084/m9.figshare.28876751.v2)."
- [other] Calculate hit@k by checking if the true compound (ground truth SMILES) appears in the top-k retrieved references: "Calculate hit@k by checking if the true compound (ground truth SMILES) appears in the top-k retrieved references for each query spectrum."
- [other] Aggregate hit@k across all 10 splits and compute mean and standard deviation: "Aggregate hit@k across all 10 splits and compute mean and standard deviation for each k value."
- [readme] Strictly retained the original training set split used by MSBERT and only applied random splitting to the test sets: "we strictly retained the original training set split used by MSBERT and only applied random splitting to the test sets. Final results are reported as the average and standard deviation across the 10"
- [other] Initialize the Tokenizer with vocabulary size 100 and normalized flag true: "Initialize the Tokenizer with vocabulary size 100 and normalized flag true."
- [other] Compute cosine similarity matrix between query and reference embeddings using cosine_similarity: "Compute cosine similarity matrix between query and reference embeddings using cosine_similarity."
- [other] Extract top-k candidate indices (k = 1, 5, 10) using top_k_indices for each query spectrum: "Extract top-k candidate indices (k = 1, 5, 10) using top_k_indices for each query spectrum."
