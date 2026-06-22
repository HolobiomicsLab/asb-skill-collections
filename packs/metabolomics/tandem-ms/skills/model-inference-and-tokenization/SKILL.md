---
name: model-inference-and-tokenization
description: Use when you have MS/MS spectra in .msp format and need to retrieve similar compounds or compute spectral similarities for compound identification. The input spectra should already be cleaned (malformed or invalid SMILES removed), and you have access to a pre-trained SpecEmbedding model checkpoint.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
  tools:
  - Python
  - PyTorch
  - CUDA
  - numba
  - SpecEmbedding.utils.clean.read_raw_spectra
  - SpecEmbedding.data.tokenizer.Tokenizer
  - SpecEmbedding.utils.model.load_tanimoto_supcon_aug_model
  - SpecEmbedding.utils.model.embedding
  - SpecEmbedding.trainer.trainer.ModelTester
  - PyTorch 2.6.0
  techniques:
  - CE-MS
  - tandem-MS
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

# model-inference-and-tokenization

## Summary

Generate vector embeddings for MS/MS spectra by tokenizing m/z intensity pairs with a learned vocabulary, then passing them through a pre-trained deep learning model to produce fixed-dimensional representations. This skill enables efficient similarity-based compound retrieval and structural matching across spectral databases.

## When to use

You have MS/MS spectra in .msp format and need to retrieve similar compounds or compute spectral similarities for compound identification. The input spectra should already be cleaned (malformed or invalid SMILES removed), and you have access to a pre-trained SpecEmbedding model checkpoint. Use this skill when you want to move from raw spectral data to a learned embedding space suitable for cosine similarity ranking or other downstream retrieval tasks.

## When NOT to use

- Input spectra contain invalid or malformed SMILES strings — clean and validate before tokenization.
- You need to train a new model from scratch — this skill uses pre-trained weights only; use the full training pipeline instead.
- Your spectra are in formats other than .msp (e.g., raw binary, mzML without preprocessing) — convert or parse to the expected .msp structure first.

## Inputs

- MS/MS spectra in .msp format (query set)
- MS/MS spectra in .msp format (reference set)
- Pre-trained SpecEmbedding model checkpoint (tanimoto-supcon-aug variant)
- Tokenizer configuration (vocabulary size 100, normalized=true)

## Outputs

- Query embeddings (dense numerical matrix, shape: num_queries × embedding_dim)
- Reference embeddings (dense numerical matrix, shape: num_references × embedding_dim)

## How to apply

Load cleaned query and reference spectra from .msp files using read_raw_spectra(). Initialize a Tokenizer with vocabulary size 100 and normalized flag set to true; this converts m/z intensity pairs into integer token sequences. Load the pre-trained tanimoto-supcon-aug model variant onto your device (CPU or GPU). Call the embedding() function with batch size 512 on both query and reference spectra to generate embeddings. The model uses sinusoidal positional encoding combined with a supervised contrastive learning framework. Check that embeddings are fixed-dimensional vectors suitable for cosine similarity computation. The rationale is that tokenization standardizes variable-length spectra into a fixed vocabulary, and the pre-trained model has learned to project that vocabulary into an embedding space optimized for compound similarity retrieval.

## Related tools

- **SpecEmbedding.utils.clean.read_raw_spectra** (Load MS/MS spectra from .msp files into memory) — https://github.com/sword-nan/SpecEmbedding
- **SpecEmbedding.data.tokenizer.Tokenizer** (Convert m/z intensity pairs into fixed vocabulary integer token sequences with normalization) — https://github.com/sword-nan/SpecEmbedding
- **SpecEmbedding.utils.model.load_tanimoto_supcon_aug_model** (Load the pre-trained tanimoto-supcon-aug model variant onto device) — https://github.com/sword-nan/SpecEmbedding
- **SpecEmbedding.utils.model.embedding** (Generate embeddings for tokenized spectra using the pre-trained model with specified batch size) — https://github.com/sword-nan/SpecEmbedding
- **SpecEmbedding.trainer.trainer.ModelTester** (Wrapper class to manage model inference, device placement, and progress reporting) — https://github.com/sword-nan/SpecEmbedding
- **PyTorch 2.6.0** (Deep learning framework for model loading and GPU/CPU tensor computation)
- **numba** (JIT compilation for fast numerical similarity operations; note: @njit decorators may cause errors on Windows)

## Examples

```
from SpecEmbedding.utils.model import embedding, load_tanimoto_supcon_aug_model
from SpecEmbedding.utils.clean import read_raw_spectra
from SpecEmbedding.trainer.trainer import ModelTester
from SpecEmbedding.data.tokenizer import Tokenizer
q = read_raw_spectra('./q.msp')
r = read_raw_spectra('./r.msp')
tokenizer = Tokenizer(100, True)
device = 'cpu'
model = load_tanimoto_supcon_aug_model(device)
tester = ModelTester(model, device, True)
q_emb, _ = embedding(tester, tokenizer, 512, q, True)
r_emb, _ = embedding(tester, tokenizer, 512, r, True)
```

## Evaluation signals

- Embeddings have consistent dimensionality across all spectra (verify shape of output matrix is [num_spectra, embedding_dim])
- Embedding values are normalized or at least bounded within expected range (e.g., no NaN or infinity values)
- Tokenized spectra have no out-of-vocabulary indices; all m/z intensity pairs map to integers in [0, vocab_size=100]
- Downstream cosine similarity matrix is symmetric and has values in [-1, 1] (or [0, 1] for normalized embeddings)
- Hit@k metrics computed from retrieved neighbors match published benchmarks on GNPS/MoNA/MTBLS1572 (e.g., hit@1, hit@5, hit@10 within reported mean ± standard deviation across 10 splits)

## Limitations

- Windows users may encounter numerical errors during cosine similarity computation due to @njit decorators from numba; workaround is to comment out all @njit decorators in the code.
- The model is trained only on GNPS, MoNA, and MTBLS1572 datasets initially preprocessed by MSBERT; performance on out-of-distribution spectra or from different instruments/protocols is not guaranteed.
- Tokenizer vocabulary size is fixed at 100; spectra with extremely high or low m/z values or unusual intensity distributions may not tokenize optimally.
- The pre-trained model is optimized for tanimoto similarity and supervised contrastive learning; other similarity metrics or loss functions may require retraining.

## Evidence

- [other] Load query and reference MS/MS spectra using read_raw_spectra from the SpecEmbedding.utils.clean module.: "Load query and reference MS/MS spectra using read_raw_spectra from the SpecEmbedding.utils.clean module"
- [other] Initialize the Tokenizer with vocabulary size 100 and normalized flag true.: "Initialize the Tokenizer with vocabulary size 100 and normalized flag true"
- [other] Load the pre-trained SpecEmbedding model (tanimoto-supcon-aug variant) using load_tanimoto_supcon_aug_model onto device (CPU or GPU).: "Load the pre-trained SpecEmbedding model (tanimoto-supcon-aug variant) using load_tanimoto_supcon_aug_model onto device (CPU or GPU)"
- [other] Generate embeddings for query spectra and reference spectra using the embedding function with batch size 512.: "Generate embeddings for query spectra and reference spectra using the embedding function with batch size 512"
- [intro] SpecEmbedding combines sinusoidal positional encoding with a supervised contrastive learning framework to improve performance in compound identification and structural similarity retrieval tasks: "SpecEmbedding combines sinusoidal positional encoding with a supervised contrastive learning framework to improve"
- [readme] When running on Windows, you may encounter numerical errors during cosine similarity computation. This is caused by @njit decorators from the numba library. You can fix it by commenting out all @njit decorators in the code.: "When running on Windows, you may encounter numerical errors during cosine similarity computation. This is caused by @njit decorators from the numba library"
