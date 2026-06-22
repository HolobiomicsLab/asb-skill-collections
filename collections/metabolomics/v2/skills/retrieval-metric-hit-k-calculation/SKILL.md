---
name: retrieval-metric-hit-k-calculation
description: Use when when you have generated embeddings for query and reference MS/MS spectra, computed a cosine similarity matrix between them, and need to evaluate how often the correct compound appears in the top-1, top-5, or top-10 retrieved candidates.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3814
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - PyTorch
  - CUDA
  - numba
  - SpecEmbedding
  - cosine_similarity (SpecEmbedding.utils.model)
  - top_k_indices (SpecEmbedding.utils.model)
  - read_raw_spectra (SpecEmbedding.utils.clean)
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c02655
  all_source_dois:
  - 10.1021/acs.analchem.5c02655
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# retrieval-metric-hit-k-calculation

## Summary

Compute hit@k retrieval performance metrics by checking whether the ground-truth compound (identified by SMILES) appears in the top-k most similar reference spectra for each query, then aggregate across multiple evaluation splits to report mean and standard deviation. This skill quantifies compound identification accuracy in MS/MS spectral retrieval workflows.

## When to use

When you have generated embeddings for query and reference MS/MS spectra, computed a cosine similarity matrix between them, and need to evaluate how often the correct compound appears in the top-1, top-5, or top-10 retrieved candidates. Use this skill when ground-truth SMILES annotations are available for query spectra and you are reporting performance across multiple random train/test splits (e.g., 10-fold cross-validation) to quantify both average retrieval accuracy and its variability.

## When NOT to use

- Query spectra lack ground-truth SMILES annotations or compound identifiers — hit@k requires a definitive ground truth to validate retrieval correctness.
- No multiple evaluation splits are available or splits were not created independently — this skill is designed to quantify and report variability across random partitions; a single evaluation split cannot yield a standard deviation.
- Similarity scores have not yet been computed or top-k ranking indices are unavailable — this skill assumes embeddings and rankings are already in hand; it does not generate them.

## Inputs

- query MS/MS spectra (loaded as spectral objects with SMILES annotations)
- reference MS/MS spectra (loaded as spectral objects with SMILES annotations)
- query embeddings (vector matrix, shape [num_queries, embedding_dim])
- reference embeddings (vector matrix, shape [num_references, embedding_dim])
- cosine similarity matrix (shape [num_queries, num_references], float values in [-1, 1])

## Outputs

- hit@k rate per split (float, typically [0, 1])
- mean hit@k across all splits (float)
- standard deviation of hit@k across splits (float)
- per-query hit@k binary indicators (binary matrix, shape [num_queries, num_splits])

## How to apply

For each of the k evaluation splits (e.g., 10 random query/reference partitions), (1) load the query spectra and corresponding reference library; (2) generate embeddings using the trained model (e.g., SpecEmbedding's tanimoto-supcon-aug variant); (3) compute the cosine similarity matrix between query and reference embeddings; (4) extract the top-k indices (k = 1, 5, 10) for each query using argmax or similar ranking; (5) check if the reference spectrum at each top-k position has the same SMILES (ground-truth compound) as the query; (6) record hit@k as a binary indicator (1 if match, 0 otherwise) for each query; (7) aggregate across all queries in the split to compute the hit@k rate (fraction of queries with correct match in top-k); (8) repeat for all k splits and compute mean hit@k and standard deviation. The rationale is that averaging across splits accounts for variance due to the train/test split randomization, yielding a more robust estimate of retrieval performance.

## Related tools

- **SpecEmbedding** (Pre-trained deep learning model that generates embeddings for MS/MS spectra; embeddings are fed into hit@k calculation.) — https://github.com/sword-nan/SpecEmbedding
- **cosine_similarity (SpecEmbedding.utils.model)** (Computes cosine similarity matrix between query and reference embeddings; output feeds directly into top-k ranking step.) — https://github.com/sword-nan/SpecEmbedding
- **top_k_indices (SpecEmbedding.utils.model)** (Extracts indices of top-k most similar reference spectra for each query; required to identify which references are ranked highest.) — https://github.com/sword-nan/SpecEmbedding
- **read_raw_spectra (SpecEmbedding.utils.clean)** (Loads query and reference spectra from .msp files, preserving SMILES annotations needed for ground-truth matching.) — https://github.com/sword-nan/SpecEmbedding
- **PyTorch** (Underlying deep learning framework for embedding generation; CUDA 12.4 enables GPU acceleration.)

## Examples

```
```python
from SpecEmbedding.utils.model import embedding, cosine_similarity, load_tanimoto_supcon_aug_model, top_k_indices
from SpecEmbedding.utils.clean import read_raw_spectra
from SpecEmbedding.trainer.trainer import ModelTester
from SpecEmbedding.data.tokenizer import Tokenizer
import numpy as np

q_spectra = read_raw_spectra('./q.msp')
r_spectra = read_raw_spectra('./r.msp')
tokenizer = Tokenizer(100, True)
device = 'cpu'
model = load_tanimoto_supcon_aug_model(device)
tester = ModelTester(model, device, False)
q, _ = embedding(tester, tokenizer, 512, q_spectra, False)
r, _ = embedding(tester, tokenizer, 512, r_spectra, False)
cosine_scores = cosine_similarity(q, r)
indices_top1 = top_k_indices(cosine_scores, 1)
hits = [r_spectra[indices_top1[i, 0]]['smiles'] == q_spectra[i]['smiles'] for i in range(len(q_spectra))]
hit_rate = np.mean(hits)
```
```

## Evaluation signals

- Hit@k values must lie in [0, 1] for each split and each k value; any value outside this range indicates a logic error.
- Mean hit@k should be ≥ highest individual split hit@k (if aggregating across all queries) or ≤ (due to randomness); verify that the mean is computed correctly from split-wise rates.
- Standard deviation should be > 0 if splits differ in composition; a standard deviation of 0 suggests all splits yielded identical results, which may indicate splits were not truly independent or random.
- Verify that ground-truth SMILES from query spectra match correctly with reference SMILES; spot-check a subset of hits to ensure the matching logic is sound (e.g., both are canonicalized or both are raw strings).
- Compare hit@1 ≥ hit@5 ≥ hit@10; hit@k should be non-decreasing in k because a larger top-k window includes all lower-k results.

## Limitations

- Hit@k assumes a single ground-truth compound per query; if a query spectrum matches multiple distinct SMILES in the reference library (e.g., isomers, duplicates), hit@k will only count as a hit if one specific SMILES is designated as ground truth.
- SMILES canonicalization and string matching are case-sensitive; inconsistent SMILES formatting (e.g., canonical vs. non-canonical, whitespace differences) will cause valid matches to be scored as misses. Ensure both query and reference SMILES are preprocessed identically.
- On Windows systems, @njit decorators from numba in the cosine_similarity function may introduce numerical errors; the README recommends commenting out these decorators when running on Windows to avoid spurious ranking artifacts.
- Hit@k does not distinguish between retrieval rank; a hit at rank 2 and rank 100 are scored equally. Consider reporting precision@k, rank correlation, or ranked metrics (e.g., MRR) if rank order is important.
- Assumes embeddings are already computed; if the embedding model is misconfigured, poorly trained, or not appropriate for the reference library (e.g., trained only on GNPS but applied to MassBank), hit@k will reflect embedding quality rather than retrieval method quality.

## Evidence

- [other] Calculate hit@k by checking if the true compound (ground truth SMILES) appears in the top-k retrieved references for each query spectrum.: "Calculate hit@k by checking if the true compound (ground truth SMILES) appears in the top-k retrieved references for each query spectrum."
- [other] Extract top-k candidate indices (k = 1, 5, 10) using top_k_indices for each query spectrum.: "Extract top-k candidate indices (k = 1, 5, 10) using top_k_indices for each query spectrum."
- [other] Aggregate hit@k across all 10 splits and compute mean and standard deviation for each k value.: "Aggregate hit@k across all 10 splits and compute mean and standard deviation for each k value."
- [readme] we strictly retained the original training set split used by MSBERT and only applied random splitting to the test sets. Final results are reported as the average and standard deviation across the 10: "we strictly retained the original training set split used by MSBERT and only applied random splitting to the test sets. Final results are reported as the average and standard deviation across the 10"
- [other] Compute the cosine similarity matrix between query and reference embeddings using cosine_similarity.: "Compute the cosine similarity matrix between query and reference embeddings using cosine_similarity."
- [readme] When running on Windows, you may encounter numerical errors during cosine similarity computation. This is caused by @njit decorators from the numba library.: "When running on Windows, you may encounter numerical errors during cosine similarity computation. This is caused by @njit decorators from the numba library."
