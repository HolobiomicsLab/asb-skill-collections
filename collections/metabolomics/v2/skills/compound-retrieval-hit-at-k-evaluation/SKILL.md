---
name: compound-retrieval-hit-at-k-evaluation
description: Use when when you have generated spectral embeddings for a query set and a reference spectral library, computed pairwise cosine similarity scores between them, and need to quantify retrieval performance across ranked candidates (top-1, top-5, top-10).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - PyTorch
  - CUDA
  - numba
  - SpecEmbedding
  - SpecEmbedding-Comparison
  - ModelTester
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

# compound-retrieval-hit-at-k-evaluation

## Summary

Evaluates MS/MS spectral retrieval models by computing hit@k metrics—the proportion of queries whose true compound is ranked within the top-k retrieved candidates—across multiple random query/reference splits to assess consistency and generalization on curated or large-scale spectral libraries.

## When to use

When you have generated spectral embeddings for a query set and a reference spectral library, computed pairwise cosine similarity scores between them, and need to quantify retrieval performance across ranked candidates (top-1, top-5, top-10). Particularly valuable for assessing model generalization on high-quality curated spectra (MassBank, MassSpecGym) or validating consistency across multiple random splits of training/test data.

## When NOT to use

- When query and reference sets share overlapping compounds—this violates the assumption of independent test samples and inflates hit@k scores artificially.
- When embeddings have not been validated for quality (e.g., embeddings are zero vectors or contain NaN); compute a sanity check (e.g., cosine similarity range, embedding norms) first.
- When compound identifiers are not reliably aligned or normalized across query and reference sets; data cleaning and SMILES validation must precede evaluation.

## Inputs

- query embeddings (tensor, shape [n_queries, embedding_dim])
- reference embeddings (tensor, shape [n_references, embedding_dim])
- query compound identifiers (list/array of strings or integers)
- reference compound identifiers (list/array of strings or integers)
- cosine similarity matrix (tensor, shape [n_queries, n_references])
- k values for retrieval depth (list of integers, e.g. [1, 5, 10])

## Outputs

- hit@k scores (float, per k; range [0, 1])
- mean hit@k across splits (float per k)
- standard deviation of hit@k across splits (float per k)
- per-query match status (boolean array, length n_queries)
- top-k candidate indices per query (integer array, shape [n_queries, k])

## How to apply

After computing cosine similarity scores between query and reference embeddings, retrieve the indices of top-k most similar reference spectra using top_k_indices(). For each query spectrum, check whether its true compound identifier matches any of the k retrieved reference compounds. Count matches to compute hit@k (fraction of queries with a match in top-k). Repeat this evaluation across 10 random query/reference splits (or as specified in your dataset), reporting the mean hit@k and standard deviation to quantify robustness. The rationale is that hit@k aggregates retrieval success across multiple splits, revealing whether the model generalizes consistently rather than depending on a particular data partition.

## Related tools

- **SpecEmbedding** (Generates spectral embeddings and computes cosine similarity for retrieval evaluation) — https://github.com/sword-nan/SpecEmbedding
- **SpecEmbedding-Comparison** (Provides detailed evaluation metrics and benchmark results for hit@k and other retrieval metrics) — https://github.com/sword-nan/SpecEmbedding-Comparison
- **PyTorch** (Tensor operations and cosine similarity computation)
- **ModelTester** (Inference wrapper for generating embeddings with batching (batch size 512)) — https://github.com/sword-nan/SpecEmbedding

## Examples

```
indices = top_k_indices(cosine_scores, k=1); matches = [r_spectra[idx].get('smiles') == q_spectra[i].get('smiles') for i, idx in enumerate(indices[:, 0])]; hit_at_1 = sum(matches) / len(matches); print(f'hit@1: {hit_at_1:.3f}')
```

## Evaluation signals

- Hit@k scores fall within reported performance ranges for the model and dataset (e.g., hit@1 > 0.7 for high-quality curated libraries).
- Standard deviation across 10 splits is small (< 0.05), indicating stable and consistent generalization.
- Hit@1 < hit@5 < hit@10 (monotonically increasing with k), demonstrating that larger candidate sets retrieve more true matches.
- Compound identifiers in top-k matches are verified to be distinct from query identifiers (no self-matches).
- Mean and std align with or fall within 95% confidence intervals of previously reported baselines on the same dataset.

## Limitations

- Hit@k assumes a single ground truth per query; if a query compound has multiple valid spectral matches in the reference set, only one match may be counted, potentially underestimating true retrieval success.
- Performance depends critically on data quality and SMILES string validity; malformed or invalid SMILES must be removed beforehand, or false negatives will inflate miss rates.
- Evaluation is sensitive to compound identifier normalization; inconsistent or duplicate identifiers across query/reference splits can produce misleading results.
- On Windows systems, the @njit decorator from numba used in cosine similarity computation may introduce numerical errors; workaround is to comment out @njit decorators.

## Evidence

- [other] Calculate hit@k metrics by counting matches between query and reference compound identifiers across 10 random query/reference splits: "Calculate hit@k metrics by counting matches between query and reference compound identifiers across 10 random query/reference splits from figshare."
- [other] Retrieve top-k candidate indices (k=1, 5, 10) from similarity scores using top_k_indices(): "Retrieve top-k candidate indices (k=1, 5, 10) from similarity scores using top_k_indices()."
- [readme] Final results are reported as the average and standard deviation across the 10 splits: "Final results are reported as the average and standard deviation across the 10 splits."
- [intro] SpecEmbedding achieved consistently strong performance on MassBank and MassSpecGym, two curated spectral libraries.: "SpecEmbedding achieved consistently strong performance on MassBank and MassSpecGym, two curated spectral libraries."
- [readme] To further improve data quality, we removed entries with malformed or invalid SMILES strings: "To further improve data quality, we removed entries with malformed or invalid SMILES strings."
- [readme] When running on Windows, you may encounter numerical errors during cosine similarity computation. This is caused by @njit decorators from the numba library.: "When running on Windows, you may encounter numerical errors during cosine similarity computation. This is caused by @njit decorators from the numba library."
