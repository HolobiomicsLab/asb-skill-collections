---
name: cosine-similarity-matrix-computation
description: Use when after generating normalized dense embeddings for both query and reference MS/MS spectra using a pre-trained model like SpecEmbedding.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3791
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - PyTorch
  - CUDA
  - numba
  - SpecEmbedding embedding function
  - cosine_similarity function
  - top_k_indices function
  - PyTorch 2.6.0
  - CUDA 12.4
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

# cosine-similarity-matrix-computation

## Summary

Compute pairwise cosine similarity scores between query and reference MS/MS spectral embeddings to rank candidate compounds by retrieval relevance. This skill is essential for spectral library search workflows where dense embeddings from deep learning models must be converted into similarity-ranked retrieval results.

## When to use

Apply this skill after generating normalized dense embeddings for both query and reference MS/MS spectra using a pre-trained model like SpecEmbedding. Use it when you need to rank reference compounds by similarity to a query spectrum, or when evaluating retrieval performance metrics (hit@k) across spectral datasets (GNPS, MoNA, MTBLS1572, MassBank, MassSpecGym).

## When NOT to use

- Query or reference embeddings are not normalized (cosine similarity assumes unit-norm vectors; use L2 normalization or set normalized=True in the embedding function first)
- Embeddings are not dense vectors (e.g., sparse features or bag-of-words representations are inappropriate for cosine similarity in this context)
- You need to retrieve compounds by exact mass or molecular formula match rather than spectral similarity (this skill is for learned embedding similarity, not structural metadata matching)

## Inputs

- query spectral embeddings (NumPy array, shape [n_queries, embedding_dim], normalized)
- reference spectral embeddings (NumPy array, shape [n_references, embedding_dim], normalized)
- pre-trained SpecEmbedding model (tanimoto-supcon-aug variant)

## Outputs

- cosine similarity matrix (NumPy array, shape [n_queries, n_references])
- similarity scores (float values in range [−1, 1], typically [0, 1] for normalized embeddings)

## How to apply

Initialize the pre-trained SpecEmbedding model (tanimoto-supcon-aug variant) and a Tokenizer with vocabulary size 100 and normalized flag set to True. Generate normalized dense embeddings for query and reference spectra using the embedding function with batch size 512. Pass the resulting query and reference embedding matrices to the cosine_similarity function, which computes the pairwise cosine similarity matrix. The output is a 2D array where rows correspond to queries, columns to references, and each cell contains the cosine similarity score. Store this matrix as a NumPy array or CSV for downstream ranking or metric computation (e.g., extracting top-k indices for hit@k calculation).

## Related tools

- **SpecEmbedding embedding function** (Generates normalized dense embeddings for query and reference spectra; output is input to cosine_similarity) — https://github.com/sword-nan/SpecEmbedding
- **cosine_similarity function** (Core similarity computation; computes pairwise cosine similarity between query and reference embeddings) — https://github.com/sword-nan/SpecEmbedding
- **top_k_indices function** (Extracts top-k candidate indices from the cosine similarity matrix for retrieval ranking and hit@k evaluation) — https://github.com/sword-nan/SpecEmbedding
- **PyTorch 2.6.0** (Deep learning framework for loading and running the pre-trained SpecEmbedding model)
- **CUDA 12.4** (GPU acceleration for embedding and similarity computation on large-scale spectral datasets)

## Examples

```
from SpecEmbedding.utils.model import embedding, cosine_similarity, load_tanimoto_supcon_aug_model
from SpecEmbedding.utils.clean import read_raw_spectra
from SpecEmbedding.trainer.trainer import ModelTester
from SpecEmbedding.data.tokenizer import Tokenizer
q = read_raw_spectra('./q.msp')
r = read_raw_spectra('./r.msp')
tokenizer = Tokenizer(100, True)
model = load_tanimoto_supcon_aug_model('cpu')
tester = ModelTester(model, 'cpu', True)
q_emb, _ = embedding(tester, tokenizer, 512, q, True)
r_emb, _ = embedding(tester, tokenizer, 512, r, True)
cosine_scores = cosine_similarity(q_emb, r_emb)
```

## Evaluation signals

- Similarity matrix shape is [n_queries, n_references] and all values are in the range [0, 1] (for normalized embeddings)
- Diagonal or near-diagonal entries in within-dataset similarity matrices are higher than off-diagonal entries, indicating intra-compound clustering
- Top-k retrieval rankings contain the correct compound (ground truth SMILES) within the top k positions; hit@k metric is computed correctly across 10-fold splits
- hit@k values and standard deviations match published benchmarks on GNPS, MoNA, and MTBLS1572 when using the same model variant and data splits
- Cosine similarity scores are numerically stable (no NaN or Inf values) across all 10 dataset splits and all k values (1, 5, 10)

## Limitations

- Numerical errors may occur on Windows due to @njit decorators from the numba library; commenting out decorators is required for correct computation on Windows
- Cosine similarity assumes unit-norm (L2-normalized) embeddings; if embeddings are not normalized by the embedding function, the matrix will be incorrect
- Performance and generalizability are limited to spectral data similar in quality and composition to GNPS, MoNA, MTBLS1572, MassBank, and MassSpecGym; out-of-distribution spectra may yield lower retrieval accuracy
- The pre-trained tanimoto-supcon-aug model is fixed; no fine-tuning or domain adaptation is performed during similarity computation, so transfer to novel compound classes is limited

## Evidence

- [other] Generate dense embeddings for query spectra using the embedding function with batch size 512 and normalized flag True. Generate dense embeddings for reference spectra using the same embedding function parameters. Compute the cosine similarity matrix between query and reference embeddings using cosine_similarity function.: "Generate dense embeddings for query spectra using the embedding function with batch size 512 and normalized flag True. Generate dense embeddings for reference spectra using the same embedding"
- [other] Load the pre-trained SpecEmbedding model (tanimoto-supcon-aug variant) using load_tanimoto_supcon_aug_model onto device (CPU or GPU).: "Load the pre-trained SpecEmbedding model (tanimoto-supcon-aug variant) using load_tanimoto_supcon_aug_model onto device (CPU or GPU)."
- [other] Initialize the Tokenizer with vocabulary size 100 and normalized flag true.: "Initialize the Tokenizer with vocabulary size 100 and normalized flag true."
- [other] SpecEmbedding generates embeddings for query and reference spectra using a deep learning model with sinusoidal positional encoding and supervised contrastive learning, then computes a cosine similarity matrix between them for retrieval scoring.: "SpecEmbedding generates embeddings for query and reference spectra using a deep learning model with sinusoidal positional encoding and supervised contrastive learning, then computes a cosine"
- [readme] When running on Windows, you may encounter numerical errors during cosine similarity computation. This is caused by @njit decorators from the numba library. You can fix it by commenting out all @njit decorators in the code.: "When running on Windows, you may encounter numerical errors during cosine similarity computation. This is caused by @njit decorators from the numba library."
- [readme] Compute the cosine similarity matrix
q, _ = embedding(tester, tokenizer, 512, q, True)
r, _ = embedding(tester, tokenizer, 512, r, True)
cosine_scores = cosine_similarity(q, r): "Compute the cosine similarity matrix between query and reference embeddings using cosine_similarity(q, r)"
