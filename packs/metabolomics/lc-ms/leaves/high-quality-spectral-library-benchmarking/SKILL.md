---
name: high-quality-spectral-library-benchmarking
description: Use when you have a pre-trained MS/MS spectral embedding model and need to validate that it achieves strong and consistent retrieval performance on curated spectral libraries that represent real-world data quality standards.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - PyTorch
  - CUDA
  - numba
  - SpecEmbedding
  - ModelTester
  - Tokenizer
  - SpecEmbedding-Comparison
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# high-quality-spectral-library-benchmarking

## Summary

Evaluate MS/MS spectral embedding model performance on curated, high-quality spectral libraries (MassBank and MassSpecGym) using hit@k retrieval metrics computed across multiple random query/reference splits. This skill assesses model robustness and generalization on spectral data with minimal quality artifacts.

## When to use

You have a pre-trained MS/MS spectral embedding model and need to validate that it achieves strong and consistent retrieval performance on curated spectral libraries that represent real-world data quality standards. This is particularly important when the model was trained on larger, noisier datasets (e.g., GNPS, MoNA) and you want to verify generalization to high-quality references before deployment or publication.

## When NOT to use

- If spectral data contains malformed or invalid SMILES strings—these must be removed beforehand via data cleaning steps
- If you are evaluating on training data or using the original training/test splits from MSBERT—only apply random splitting to test sets to avoid data leakage
- If your model was not trained with supervised contrastive learning or sinusoidal positional encoding—the reported baseline performance may not be representative

## Inputs

- Pre-trained SpecEmbedding model checkpoint (Tanimoto supervised contrastive learning variant)
- Query spectra in MSP format
- Reference spectra in MSP format (from MassBank or MassSpecGym)
- 10 random query/reference split definitions (from figshare)
- Tokenizer configuration (vocabulary size 100, augmentation enabled)

## Outputs

- hit@k metrics (k=1, 5, 10) per split
- Mean and standard deviation of hit@k across 10 splits
- Cosine similarity score matrix (query × reference)
- Top-k candidate indices per query spectrum

## How to apply

Load the pre-trained SpecEmbedding model checkpoint (using Tanimoto supervised contrastive learning with sinusoidal positional encoding) and initialize a Tokenizer with vocabulary size 100 and augmentation enabled. Load query and reference spectra in MSP format from MassBank or MassSpecGym using read_raw_spectra(). Generate spectral embeddings using the embedding() function with batch size 512 and ModelTester inference wrapper. Compute pairwise cosine similarity scores between query and reference embeddings, then retrieve top-k candidate indices (k=1, 5, 10) using top_k_indices(). Calculate hit@k metrics by counting matches between query and reference compound identifiers. Repeat this evaluation across 10 random query/reference splits (available on figshare) and report both average hit@k scores and standard deviations. Compare results against reported performance ranges to confirm consistent generalization on high-quality spectra.

## Related tools

- **SpecEmbedding** (Pre-trained deep learning model for MS/MS spectral embedding with sinusoidal positional encoding and supervised contrastive learning checkpoint) — https://github.com/sword-nan/SpecEmbedding
- **ModelTester** (Inference wrapper for generating spectral embeddings in batch mode with optional progress bar) — https://github.com/sword-nan/SpecEmbedding
- **Tokenizer** (Converts raw spectral peaks into token sequences (vocabulary size 100) with augmentation for model input) — https://github.com/sword-nan/SpecEmbedding
- **SpecEmbedding-Comparison** (Evaluation framework and benchmarking scripts for computing hit@k metrics and comparison with baseline methods) — https://github.com/sword-nan/SpecEmbedding-Comparison

## Examples

```
from SpecEmbedding.utils.model import embedding, cosine_similarity, load_tanimoto_supcon_aug_model, top_k_indices
from SpecEmbedding.utils.clean import read_raw_spectra
from SpecEmbedding.trainer.trainer import ModelTester
from SpecEmbedding.data.tokenizer import Tokenizer
q_spectra = read_raw_spectra('./q.msp')
r_spectra = read_raw_spectra('./r.msp')
tokenizer = Tokenizer(100, True)
model = load_tanimoto_supcon_aug_model('cpu')
tester = ModelTester(model, 'cpu', False)
q_emb, _ = embedding(tester, tokenizer, 512, q_spectra, False)
r_emb, _ = embedding(tester, tokenizer, 512, r_spectra, False)
cosine_scores = cosine_similarity(q_emb, r_emb)
indices = top_k_indices(cosine_scores, 1)
```

## Evaluation signals

- hit@k scores (especially hit@1, hit@5, hit@10) fall within or exceed the reported performance ranges for MassBank and MassSpecGym
- Standard deviations across 10 random splits are consistent with published ranges, indicating stable and reproducible retrieval performance
- Cosine similarity scores between matching query and reference spectra are substantially higher than non-matching pairs
- Top-k candidate indices correctly identify compound identifiers that match the query spectrum's reference compound
- Performance on curated libraries (MassBank, MassSpecGym) is comparable to or better than performance on noisier training datasets (GNPS, MoNA), confirming generalization

## Limitations

- Evaluation relies on compound identifier matching; spectral variations of the same compound may not be captured if SMILES or compound ID fields are missing or inconsistent
- Performance is sensitive to data quality—spectra with malformed or invalid SMILES strings must be removed beforehand; results do not generalize to uncleaned spectral data
- Windows users may encounter numerical errors during cosine similarity computation due to @njit decorators from numba; requires commenting out decorators to run
- Hit@k metrics assume a single correct reference compound per query; isomers or structural analogs will be counted as false negatives
- Results are specific to the Tanimoto supervised contrastive learning checkpoint; other model variants or training procedures may yield different performance

## Evidence

- [readme] We additionally tested MassBank and MassSpecGym, two curated spectral libraries. SpecEmbedding achieved consistently strong performance on these datasets as well.: "We additionally tested MassBank and MassSpecGym, two curated spectral libraries. SpecEmbedding achieved consistently strong performance on these datasets as well."
- [methods] Calculate hit@k metrics by counting matches between query and reference compound identifiers across 10 random query/reference splits from figshare.: "Calculate hit@k metrics by counting matches between query and reference compound identifiers across 10 random query/reference splits"
- [methods] Retrieve top-k candidate indices (k=1, 5, 10) from similarity scores using top_k_indices().: "Retrieve top-k candidate indices (k=1, 5, 10) from similarity scores using top_k_indices()."
- [methods] Verification: Verify hit@k scores and standard deviations match or fall within reported performance ranges demonstrating consistent generalization on high-quality curated spectra.: "Verify hit@k scores and standard deviations match or fall within reported performance ranges demonstrating consistent generalization on high-quality curated spectra"
- [readme] All cleaned data, along with the preprocessing scripts and 10-fold query/reference splits used for evaluation, are available on figshare: "All cleaned data, along with the preprocessing scripts and 10-fold query/reference splits used for evaluation, are available on figshare"
- [methods] Generate spectral embeddings for query and reference sets using the embedding() function with batch size 512 and ModelTester inference wrapper.: "Generate spectral embeddings for query and reference sets using the embedding() function with batch size 512 and ModelTester inference wrapper"
- [methods] Initialize Tokenizer with vocabulary size 100 and augmentation enabled.: "Initialize Tokenizer with vocabulary size 100 and augmentation enabled."
- [methods] Load pre-trained SpecEmbedding model using the Tanimoto supervised contrastive learning checkpoint with sinusoidal positional encoding via load_tanimoto_supcon_aug_model().: "Load pre-trained SpecEmbedding model using the Tanimoto supervised contrastive learning checkpoint with sinusoidal positional encoding"
