---
name: cross-dataset-generalization-assessment
description: Use when you have a pre-trained MS/MS spectral embedding model evaluated on one or more source datasets (GNPS, MoNA, MTBLS1572) and need to verify that it performs well on independent, high-quality curated spectral libraries to claim robustness.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0092
  tools:
  - Python
  - PyTorch
  - CUDA
  - numba
  - load_tanimoto_supcon_aug_model
  - read_raw_spectra
  - Tokenizer
  - ModelTester
  - embedding
  - cosine_similarity
  - top_k_indices
  - CUDA 12.4
  techniques:
  - LC-MS
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

# cross-dataset-generalization-assessment

## Summary

Evaluate whether a trained spectral embedding model maintains strong retrieval performance when applied to curated external spectral libraries (MassBank, MassSpecGym) that differ in data provenance and quality from the training set. This assesses model robustness and generalizability beyond the primary training cohort.

## When to use

You have a pre-trained MS/MS spectral embedding model evaluated on one or more source datasets (GNPS, MoNA, MTBLS1572) and need to verify that it performs well on independent, high-quality curated spectral libraries to claim robustness. This is essential before deployment or publication of a general-purpose compound identification tool.

## When NOT to use

- The model has not yet been trained or validated on the primary training datasets (GNPS, MoNA, MTBLS1572); establish baseline performance first.
- The external spectral library contains spectra with malformed or invalid SMILES strings that have not been cleaned; apply data quality filtering before evaluation.
- You are testing model performance on the same dataset used for training or hyperparameter tuning; use only held-out test splits or independent external data.

## Inputs

- Pre-trained SpecEmbedding model checkpoint (Tanimoto supervised contrastive learning weights)
- Query spectra in MSP format from external curated library (e.g., MassBank or MassSpecGym)
- Reference spectra in MSP format from the same external library
- Compound identifiers or SMILES strings associated with each spectrum
- Tokenizer configuration (vocabulary size, augmentation settings)

## Outputs

- Hit@k metrics (hit@1, hit@5, hit@10) for the external library
- Mean and standard deviation of hit@k across multiple random query/reference splits
- Cosine similarity score matrix (query × reference dimension)
- Top-k candidate indices for each query spectrum
- Performance comparison table vs. training-set baseline results

## How to apply

Load the pre-trained model checkpoint (e.g., Tanimoto supervised contrastive learning model with sinusoidal positional encoding) and initialize a ModelTester inference wrapper. Load query and reference spectra from the external curated library in MSP format using read_raw_spectra(). Initialize a Tokenizer with vocabulary size 100 and augmentation enabled. Generate embeddings for both query and reference spectral sets using the embedding() function with batch size 512. Compute pairwise cosine similarity scores between query and reference embeddings. Retrieve top-k candidate indices (k=1, 5, 10) and calculate hit@k metrics by counting matches between query and reference compound identifiers. Report hit@k scores and standard deviations; performance is considered consistent with training set results if scores fall within the reported ranges or show no significant degradation, validating generalization on high-quality spectra.

## Related tools

- **load_tanimoto_supcon_aug_model** (Load pre-trained SpecEmbedding checkpoint with supervised contrastive learning and sinusoidal positional encoding) — https://github.com/sword-nan/SpecEmbedding
- **read_raw_spectra** (Parse and load MSP-format spectral library files into memory for query and reference sets) — https://github.com/sword-nan/SpecEmbedding
- **Tokenizer** (Initialize vocabulary (size 100) and augmentation settings for spectrum tokenization during embedding) — https://github.com/sword-nan/SpecEmbedding
- **ModelTester** (Wrapper for model inference on batches of tokenized spectra to produce embeddings) — https://github.com/sword-nan/SpecEmbedding
- **embedding** (Generate dense embeddings for query and reference spectra with batch size 512 using ModelTester) — https://github.com/sword-nan/SpecEmbedding
- **cosine_similarity** (Compute pairwise cosine similarity matrix between query and reference embeddings) — https://github.com/sword-nan/SpecEmbedding
- **top_k_indices** (Extract top-k candidate reference indices for each query spectrum from similarity scores) — https://github.com/sword-nan/SpecEmbedding
- **PyTorch** (Deep learning framework for loading and running inference on the trained model)
- **CUDA 12.4** (GPU acceleration for embedding computation on large spectral sets)

## Examples

```
q = read_raw_spectra('./MassBank.msp'); r = read_raw_spectra('./MassBank.msp'); model = load_tanimoto_supcon_aug_model('cpu'); tester = ModelTester(model, 'cpu', True); tokenizer = Tokenizer(100, True); q_emb, _ = embedding(tester, tokenizer, 512, q, True); r_emb, _ = embedding(tester, tokenizer, 512, r, True); scores = cosine_similarity(q_emb, r_emb); indices = top_k_indices(scores, 5); print(f'hit@5: {sum(indices[:, 0] < len(r)) / len(q)}')
```

## Evaluation signals

- Hit@k scores for external library fall within or exceed the reported performance range from training-set evaluation (e.g., hit@1, hit@5, hit@10 scores match reported baselines within ±2–3%).
- Standard deviations across 10 random query/reference splits remain low and similar in magnitude to training-set variance, indicating stable performance.
- Mean hit@k scores show no statistically significant degradation compared to training dataset results, validating generalization.
- Cosine similarity score distribution remains well-calibrated (e.g., correct matches cluster at high similarity, incorrect matches at lower similarity) across the external library.
- Compound identifiers retrieved via top-k matching agree with ground-truth SMILES or external identifier mappings for a high fraction of queries.

## Limitations

- Performance on external libraries depends critically on data quality; MassBank and MassSpecGym are curated, high-quality libraries; performance may degrade on noisier or lower-resolution spectra not represented in training or curation workflows.
- The skill uses 10-fold random query/reference splits for evaluation; results are stochastic and should be reported with standard deviations; reproducibility requires fixing random seeds and version control of data splits.
- On Windows systems, the @njit decorators from numba in the cosine_similarity function can cause numerical errors during computation; these must be commented out or replaced with non-numba implementations for reliable results.
- Hit@k metrics only capture retrieval rank; they do not distinguish between near-miss candidates (high cosine similarity but incorrect identity) and true negatives, limiting diagnostic insight into failure modes.
- Generalization assessment assumes the model has been trained on GNPS, MoNA, or MTBLS1572 with MSBERT preprocessing; models trained on other datasets or preprocessing pipelines may show different generalization behavior.

## Evidence

- [intro] we additionally tested MassBank and MassSpecGym, two curated spectral libraries. SpecEmbedding achieved consistently strong performance on these datasets as well.: "we additionally tested MassBank and MassSpecGym, two curated spectral libraries. SpecEmbedding achieved consistently strong performance on these datasets as well"
- [readme] To assess the model's robustness and generalizability on high-quality data, we additionally tested MassBank and MassSpecGym, two curated spectral libraries.: "To assess the model's robustness and generalizability on high-quality data, we additionally tested MassBank and MassSpecGym, two curated spectral libraries"
- [readme] Final results are reported as the average and standard deviation across the 10 splits.: "Final results are reported as the average and standard deviation across the 10 splits"
- [methods] Generate spectral embeddings for query and reference sets using the embedding() function with batch size 512 and ModelTester inference wrapper. 5. Compute pairwise cosine similarity scores between query and reference embeddings using cosine_similarity().: "Generate spectral embeddings for query and reference sets using the embedding() function with batch size 512 and ModelTester inference wrapper"
- [methods] Calculate hit@k metrics by counting matches between query and reference compound identifiers across 10 random query/reference splits from figshare.: "Calculate hit@k metrics by counting matches between query and reference compound identifiers across 10 random query/reference splits"
- [readme] When running on Windows, you may encounter numerical errors during cosine similarity computation. This is caused by @njit decorators from the numba library.: "When running on Windows, you may encounter numerical errors during cosine similarity computation. This is caused by @njit decorators from the numba library"
