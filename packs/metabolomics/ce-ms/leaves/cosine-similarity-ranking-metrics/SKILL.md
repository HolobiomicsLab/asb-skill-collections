---
name: cosine-similarity-ranking-metrics
description: Use when when you have pre-computed spectral embeddings (vectors) for both query spectra and a reference library, and you need to measure retrieval performance by ranking reference compounds by similarity to each query.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0599
  tools:
  - Python
  - PyTorch
  - CUDA
  - numba
  - SpecEmbedding.utils.model.cosine_similarity
  - SpecEmbedding.utils.model.top_k_indices
  - SpecEmbedding.utils.model.embedding
  - SpecEmbedding.utils.clean.read_raw_spectra
  - SpecEmbedding.trainer.trainer.ModelTester
  - PyTorch 2.6.0 with CUDA 12.4
  techniques:
  - CE-MS
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# cosine-similarity-ranking-metrics

## Summary

Compute pairwise cosine similarity between query and reference MS/MS spectral embeddings, then retrieve top-k candidate indices and calculate hit@k retrieval metrics to evaluate compound identification performance. This skill quantifies how often the correct match appears within the top k retrieved candidates across random query/reference splits.

## When to use

When you have pre-computed spectral embeddings (vectors) for both query spectra and a reference library, and you need to measure retrieval performance by ranking reference compounds by similarity to each query. Specifically, use this skill to validate whether a spectral embedding model generalizes well on curated libraries (e.g., MassBank, MassSpecGym) or to benchmark compound identification accuracy via hit@k metrics across multiple random splits of the data.

## When NOT to use

- When query or reference spectra are not preprocessed to remove malformed or invalid SMILES strings — data quality must be ensured beforehand.
- When you lack pre-computed embeddings and need to train a new model from raw spectra — this skill assumes embeddings are already generated.
- When comparing spectra that were not part of the same training/evaluation split protocol — use the 10-fold query/reference splits from figshare to ensure fair and reproducible evaluation.

## Inputs

- Query MS/MS spectra (MSP format or list of spectrum objects with SMILES/InChI keys)
- Reference MS/MS spectra library (MSP format or list of spectrum objects)
- Pre-trained SpecEmbedding model checkpoint (Tanimoto supervised contrastive learning weights)
- Tokenizer configuration (vocabulary size, augmentation settings)
- Device specification (CPU or CUDA GPU)

## Outputs

- Cosine similarity matrix (query_count × reference_count)
- Top-k candidate indices for each query (query_count × k)
- hit@k metric values (hit@1, hit@5, hit@10 as percentages or fractions)
- Mean and standard deviation of hit@k across random splits

## How to apply

First, load query and reference MS/MS spectra from MSP format files using read_raw_spectra(). Initialize a Tokenizer with vocabulary size 100 and augmentation enabled, then generate embeddings for both sets using the embedding() function with batch size 512 via the ModelTester inference wrapper. Compute the full pairwise cosine similarity matrix between query and reference embeddings using cosine_similarity(). Retrieve top-k candidate indices (k=1, 5, 10) from the similarity scores using top_k_indices(). Finally, calculate hit@k metrics by comparing compound identifiers (e.g., SMILES strings or InChI keys) between matched query and reference pairs across multiple random query/reference splits (typically 10 splits), then report the average and standard deviation of hit rates to quantify retrieval performance and generalization ability.

## Related tools

- **SpecEmbedding.utils.model.cosine_similarity** (Computes pairwise cosine similarity matrix between query and reference embeddings) — https://github.com/sword-nan/SpecEmbedding
- **SpecEmbedding.utils.model.top_k_indices** (Retrieves indices of top-k most similar candidates from cosine similarity scores) — https://github.com/sword-nan/SpecEmbedding
- **SpecEmbedding.utils.model.embedding** (Generates spectral embeddings for query and reference spectra using ModelTester) — https://github.com/sword-nan/SpecEmbedding
- **SpecEmbedding.utils.clean.read_raw_spectra** (Loads MS/MS spectra from MSP format files) — https://github.com/sword-nan/SpecEmbedding
- **SpecEmbedding.trainer.trainer.ModelTester** (Inference wrapper that batches embedding generation with batch size 512 and device management) — https://github.com/sword-nan/SpecEmbedding
- **PyTorch 2.6.0 with CUDA 12.4** (Underlying deep learning framework for embedding computation and similarity calculations)

## Examples

```
from SpecEmbedding.utils.model import embedding, cosine_similarity, top_k_indices, load_tanimoto_supcon_aug_model
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
indices = top_k_indices(cosine_scores, 10)
```

## Evaluation signals

- Cosine similarity scores fall within [−1, 1] range and exhibit reasonable distribution (not all near 0 or 1).
- hit@k values increase monotonically with k (hit@1 ≤ hit@5 ≤ hit@10).
- Mean and standard deviation of hit@k across 10 random splits match or fall within the reported performance ranges from the article's benchmark results on MassBank and MassSpecGym.
- Top-1 candidate compound identifiers (SMILES, InChI keys) match ground-truth query identifiers for a statistically meaningful fraction of queries (hit@1 typically ≥ 70–80% on curated libraries).
- Results are reproducible across runs using the same fixed query/reference split indices from figshare.

## Limitations

- On Windows systems, @njit decorators from the numba library may cause numerical errors during cosine similarity computation; workaround is to comment out all @njit decorators in the code.
- Performance depends critically on data quality — entries with malformed or invalid SMILES strings must be removed beforehand; model was validated only on cleaned subsets of GNPS, MoNA, MTBLS1572, MassBank, and MassSpecGym.
- Results are specific to the Tanimoto supervised contrastive learning checkpoint and sinusoidal positional encoding; other SpecEmbedding variants or model architectures may produce different rankings.
- Evaluation assumes compound identifiers (SMILES, InChI keys) are present and correctly matched between query and reference sets; missing or corrupted identifiers will inflate or deflate hit@k metrics.

## Evidence

- [methods] Compute pairwise cosine similarity scores between query and reference embeddings using cosine_similarity().: "Compute pairwise cosine similarity scores between query and reference embeddings using cosine_similarity()"
- [methods] Retrieve top-k candidate indices (k=1, 5, 10) from similarity scores using top_k_indices().: "Retrieve top-k candidate indices (k=1, 5, 10) from similarity scores using top_k_indices()"
- [methods] Calculate hit@k metrics by counting matches between query and reference compound identifiers across 10 random query/reference splits: "Calculate hit@k metrics by counting matches between query and reference compound identifiers across 10 random query/reference splits from figshare"
- [methods] Verify hit@k scores and standard deviations match or fall within reported performance ranges demonstrating consistent generalization on high-quality curated spectra.: "Verification: Verify hit@k scores and standard deviations match or fall within reported performance ranges demonstrating consistent generalization on high-quality curated spectra"
- [methods] Generate embeddings for query and reference spectra using the embedding() function with batch size 512 and ModelTester inference wrapper.: "Generate spectral embeddings for query and reference sets using the embedding() function with batch size 512 and ModelTester inference wrapper"
- [intro] SpecEmbedding achieved consistently strong performance on MassBank and MassSpecGym, two curated spectral libraries.: "SpecEmbedding achieved consistently strong performance on these datasets as well"
- [intro] we strictly retained the original training set split used by MSBERT and only applied random splitting to the test sets. Final results are reported as the average and standard deviation across the 10: "we strictly retained the original training set split used by MSBERT and only applied random splitting to the test sets. Final results are reported as the average and standard deviation across the 10"
- [readme] Compute the cosine similarity matrix between query and reference spectra: "# Compute the cosine similarity matrix
cosine_scores = cosine_similarity(q, r)"
- [readme] Retrieve the indices of the top-1 candidates: "# Retrieve the indices of the top-1 candidates
indices = top_k_indices(cosine_scores, 1)"
