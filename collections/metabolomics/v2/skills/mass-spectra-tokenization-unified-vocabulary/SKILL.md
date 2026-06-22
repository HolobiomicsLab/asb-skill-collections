---
name: mass-spectra-tokenization-unified-vocabulary
description: Use when when you have paired mass spectra and molecular structure data and need to train a unified model for structure elucidation. Use this skill at the data preparation stage before pretraining, when you want both modalities to share representational capacity rather than operate in isolation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2429
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  tools:
  - PyTorch
  - Hugging Face Transformers
derived_from:
- doi: 10.48550/arxiv.2510.20615
  title: MS-BART
evidence_spans:
- github.com/OpenDFM/MS-BART
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms_bart_cq
    doi: 10.48550/arxiv.2510.20615
    title: MS-BART
  dedup_kept_from: coll_ms_bart_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.48550/arxiv.2510.20615
  all_source_dois:
  - 10.48550/arxiv.2510.20615
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectra-tokenization-unified-vocabulary

## Summary

Tokenize mass spectra and molecular structures using a unified vocabulary that enables joint end-to-end pretraining, fine-tuning, and alignment in a single sequence-to-sequence model. This skill bridges spectroscopy and chemistry by converting both modalities into a shared token space, eliminating the need for separate encoders.

## When to use

When you have paired mass spectra and molecular structure data and need to train a unified model for structure elucidation. Use this skill at the data preparation stage before pretraining, when you want both modalities to share representational capacity rather than operate in isolation. Specifically, apply it when you have raw spectra-molecule pairs and need to convert them into token sequences compatible with a seq2seq architecture.

## When NOT to use

- Input spectra and molecules are already pre-tokenized or embedded in a learned representation; tokenization is a data preparation step and does not apply to downstream inference.
- You are using a modality-specific architecture (e.g., separate spectrometry encoder and molecular encoder) and do not intend to share vocabulary; use modality-specific tokenization instead.
- The target model does not support concatenated input sequences (e.g., it requires strict separation of spectra and molecule inputs); this skill assumes a unified seq2seq input format.

## Inputs

- Mass spectra datasets (m/z, intensity pairs or mgf format)
- Molecular structure data (SMILES strings, canonical representations, or molecular graphs)
- Unified MS-BART vocabulary definition (token-to-ID mapping)

## Outputs

- Tokenized spectra (sequence of integer token IDs)
- Tokenized molecular structures (sequence of integer token IDs)
- Concatenated spectra-molecule token sequences ready for seq2seq input

## How to apply

Load mass spectra and molecular structure datasets in parallel. Define or load the unified MS-BART vocabulary that encodes both modality types. Tokenize spectra (e.g., m/z and intensity values) and molecular structures (e.g., SMILES or molecule graphs) separately using modality-specific tokenization rules, then concatenate the resulting token sequences. The unified vocabulary ensures that both token streams are machine-readable by the same encoder, enabling the pretraining objective to operate on concatenated spectra-molecule sequences without modality-specific preprocessing branches. Validate token distributions and verify that tokenization is lossless or acceptably compressed relative to the original data.

## Related tools

- **PyTorch** (Implements tensor operations and data loading for tokenized sequences during training)
- **Hugging Face Transformers** (Provides seq2seq model architecture (e.g., BART) that accepts concatenated tokenized input and manages vocabulary encoding/decoding)

## Examples

```
python preprocess/generate_pretrain_data.py && python preprocess/split_pretrain_dataset.py
```

## Evaluation signals

- Token sequences for spectra and molecules have consistent length distributions and fall within vocabulary size bounds (no out-of-vocabulary tokens).
- Concatenated sequences can be successfully loaded into the seq2seq model without shape or dtype errors.
- Loss curves during pretraining converge smoothly and loss checkpoint files are saved correctly, indicating the model is learning from unified token representations.
- Tokenization is reversible or lossy compression is quantified (e.g., Tanimoto similarity > 0.5 for deduplicated pretrain data as noted in the README).
- Vocabulary coverage: verify that all unique spectra tokens and molecular tokens from the training set are present in the unified vocabulary with no unmapped tokens.

## Limitations

- Unified vocabulary design is not detailed in the provided materials; vocabulary size, coverage, and modality balance are not explicitly specified, which may affect tokenization efficiency for one modality over another.
- No ablation study is provided comparing unified vs. separate tokenization; relative benefit for end-to-end learning is inferred from overall model performance rather than isolated tokenization impact.
- Preprocessing steps (generate_pretrain_data.py, etc.) are mentioned in the README but their implementation details are not provided, so tokenization logic may vary from the description depending on actual code.
- The article does not discuss failure modes for edge cases such as low-intensity or high-mass spectra, or unusual molecular structures that might produce rare tokens.

## Evidence

- [intro] MS-BART is the first to leverage language model for mass spectra structure elucidation by introducing a unified vocabulary and enabling end-to-end pretraining, fine-tuning, and alignment.: "MS-BART introduces a unified vocabulary that enables end-to-end pretraining, fine-tuning, and alignment as its core training mechanism for joint mass spectra and molecular structure modeling."
- [other] The workflow explicitly requires tokenizing both modalities with the unified MS-BART vocabulary before pretraining.: "Load mass spectra and molecular structure datasets, tokenizing both modalities using the unified MS-BART vocabulary."
- [other] Concatenation of spectra and molecule tokens is the input format to the seq2seq pretraining objective.: "Execute end-to-end pretraining stage using a sequence-to-sequence architecture with the pretraining objective on concatenated spectra-molecule token sequences."
- [other] Validation includes checking that tokenization and model checkpointing succeed.: "Validate training convergence by logging loss metrics at each stage and verify model checkpoint files are saved correctly."
- [readme] The README specifies preprocessing scripts that prepare data including tokenization.: "Pretrain dataset generation and split 10000 for validation to choose the best model for finetune and alignment"
