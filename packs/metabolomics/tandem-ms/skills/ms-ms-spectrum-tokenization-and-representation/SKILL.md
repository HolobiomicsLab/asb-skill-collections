---
name: ms-ms-spectrum-tokenization-and-representation
description: Use when when you have raw MS/MS spectra in MSP format (or similar) with m/z–intensity peak pairs and need to prepare them for neural embedding models that require fixed-size discrete token inputs. Applies before generating dense spectral embeddings for retrieval or similarity scoring tasks.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3628
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - PyTorch
  - CUDA
  - numba
  - Tokenizer
  - read_raw_spectra
  - SiameseModel
  techniques:
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

# MS/MS Spectrum Tokenization and Representation

## Summary

Convert MS/MS spectral peak data into discrete token sequences suitable for deep learning models by mapping m/z and intensity values to vocabulary indices. This tokenization step enables supervised contrastive learning and spectral embedding generation for similarity-based compound identification.

## When to use

When you have raw MS/MS spectra in MSP format (or similar) with m/z–intensity peak pairs and need to prepare them for neural embedding models that require fixed-size discrete token inputs. Applies before generating dense spectral embeddings for retrieval or similarity scoring tasks.

## When NOT to use

- Spectra are already pre-tokenized or in pre-computed embedding form
- Input data lacks sufficient peak information or contains malformed m/z–intensity pairs
- You require continuous (non-discretized) spectral representation for direct similarity computation

## Inputs

- Raw MS/MS spectra in MSP format (m/z–intensity peak pairs)
- Vocabulary size parameter (recommended: 100)
- Spectral metadata including SMILES strings for contrastive learning

## Outputs

- Tokenized spectral sequences (discrete integer indices)
- Token embeddings compatible with SiameseModel input

## How to apply

Initialize a Tokenizer with vocabulary size 100 and set the normalized flag to True. For each spectrum, the tokenizer maps m/z and intensity values to discrete tokens within the vocabulary range. This discretization uses sinusoidal positional encoding to preserve spectral order and magnitude relationships. The resulting token sequences serve as input to the SiameseModel architecture during both training with supervised contrastive learning and inference for embedding generation. The normalized flag ensures consistent token ranges across different spectra, which is critical for reproducible supervised learning.

## Related tools

- **Tokenizer** (Discretizes m/z and intensity values into vocabulary indices; manages vocabulary size and normalization for spectral sequences) — https://github.com/sword-nan/SpecEmbedding
- **read_raw_spectra** (Parses raw MSP format spectral files to extract peak data and metadata before tokenization) — https://github.com/sword-nan/SpecEmbedding
- **SiameseModel** (Neural architecture that accepts tokenized sequences and outputs dense embeddings via sinusoidal positional encoding and supervised contrastive learning) — https://github.com/sword-nan/SpecEmbedding
- **PyTorch** (Computational framework for model training and inference on tokenized spectral data)

## Examples

```
tokenizer = Tokenizer(100, True); q = read_raw_spectra('./q.msp'); q_tokens, _ = embedding(tester, tokenizer, 512, q, True)
```

## Evaluation signals

- Verify token indices are within vocabulary range [0, vocabulary_size); no out-of-bounds values
- Confirm all spectra produce consistent token sequence lengths after normalization
- Check that tokenized spectra retain relative m/z ordering and intensity relationships through embedding quality metrics (e.g., hit rate on curated libraries)
- Validate reproducibility across runs with same vocabulary and normalization settings
- Ensure downstream supervised contrastive learning loss converges, indicating tokens preserve discriminative information

## Limitations

- Tokenization uses fixed vocabulary size (100 in SpecEmbedding); very large or very small m/z values may be lossy
- Normalized flag must be consistently applied across training and inference; inconsistent normalization breaks model generalization
- MSP format parsing requires well-formed input; malformed or invalid SMILES strings should be removed upstream
- On Windows, @njit decorators from numba can cause numerical errors during tokenization; users must manually comment out decorators to avoid corruption

## Evidence

- [other] Initialize the Tokenizer with vocabulary size 100 and set the computational device (CPU or GPU).: "Initialize the Tokenizer with vocabulary size 100 and set the computational device (CPU or GPU)."
- [readme] SpecEmbedding is a deep learning model designed specifically for MS/MS spectral embedding. It combines sinusoidal positional encoding with a supervised contrastive learning framework: "SpecEmbedding is a deep learning model designed specifically for MS/MS spectral embedding. It combines sinusoidal positional encoding with a supervised contrastive learning framework"
- [other] Load query and reference spectra from MSP format files using the read_raw_spectra utility.: "Load query and reference spectra from MSP format files using the read_raw_spectra utility."
- [readme] To further improve data quality, we removed entries with malformed or invalid SMILES strings: "To further improve data quality, we removed entries with malformed or invalid SMILES strings"
- [readme] When running on Windows, you may encounter numerical errors during cosine similarity computation. This is caused by @njit decorators from the numba library.: "When running on Windows, you may encounter numerical errors during cosine similarity computation. This is caused by @njit decorators from the numba library."
