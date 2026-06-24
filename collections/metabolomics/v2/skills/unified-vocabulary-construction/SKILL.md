---
name: unified-vocabulary-construction
description: Use when when you have parallel mass spectra and molecular structure
  data (e.g., CANOPUS or MassSpecGym datasets) and aim to train a single encoder-decoder
  model (e.g., BART) that must handle both modalities as input and output tokens.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0154
  tools:
  - BART
  - MS-BART
  techniques:
  - mass-spectrometry
  license_tier: restricted
derived_from:
- doi: 10.48550/arxiv.2510.20615
  title: MS-BART
evidence_spans:
- MS-BART is the first to leverage language model for mass spectra structure elucidation
  by introducing a unified vocabulary
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# unified-vocabulary-construction

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Construct a unified token vocabulary that merges mass spectral features (m/z values, intensities) and molecular structure tokens (SMILES or graph representations) into a single coherent set for end-to-end sequence modeling. This enables a single language model to process both spectral and structural data with consistent tokenization.

## When to use

When you have parallel mass spectra and molecular structure data (e.g., CANOPUS or MassSpecGym datasets) and aim to train a single encoder-decoder model (e.g., BART) that must handle both modalities as input and output tokens. Use this skill when naive separate vocabularies would prevent bidirectional alignment or when you need to encode spectra-to-molecule or molecule-to-spectra tasks within one model.

## When NOT to use

- Input data are already tokenized or pre-encoded in a fixed external vocabulary — use this skill only when you need to design a new unified vocabulary from raw spectra and structures.
- Spectral and molecular data are processed independently and will never be jointly modeled — separate vocabularies are simpler and more efficient.
- You require cross-lingual or cross-domain vocabulary sharing beyond mass spectrometry and chemistry — this skill is specific to MS-structure alignment tasks.

## Inputs

- Mass spectral data (m/z values and intensities from experimental or simulated spectra)
- Molecular structure data (SMILES strings or molecular graph representations)
- Typical data ranges and chemical complexity parameters
- Representative sample of spectra and molecules for validation

## Outputs

- Unified token vocabulary (token ID assignments)
- Bidirectional mapping dictionary (raw data ↔ token IDs)
- Vocabulary summary report (token counts, coverage metrics, special token assignments)

## How to apply

First, define separate token vocabularies for mass spectral peaks (discretizing m/z values and intensity ranges typical to your data domain) and molecular structures (SMILES tokens or graph node/edge symbols). Merge these vocabularies into a unified token set, assigning unique token IDs to each spectral feature and structural element while preserving special tokens (BOS, EOS, PAD, UNK). Create a bidirectional mapping dictionary between raw data and token IDs for efficient encode/decode. Validate by encoding representative spectra and molecules from your dataset, checking that all data types tokenize correctly, no token ID collisions occur, and coverage spans your entire data domain. Document vocabulary statistics (total token count, spectral vs. structural token split, special token assignments) and coverage metrics to ensure the vocabulary is suitable for downstream pretraining and fine-tuning.

## Related tools

- **BART** (Encoder-decoder language model backbone that ingests the unified vocabulary for pretraining and fine-tuning on mass spectra and molecular structure tasks)
- **MS-BART** (Reference implementation demonstrating unified vocabulary construction and application to mass spectra structure elucidation) — https://github.com/OpenDFM/MS-BART

## Examples

```
python preprocess/generate_pretrain_data.py && python preprocess/generate_canopus_and_lables.py
```

## Evaluation signals

- All mass spectral m/z values and intensities in the validation set tokenize without out-of-vocabulary (OOV) errors.
- All SMILES characters and molecular graph tokens in the validation set tokenize without OOV errors; no token ID collisions between spectral and structural vocabularies.
- Vocabulary coverage metrics show ≥99% of the training/validation data domain is represented; histogram of token frequencies shows no unexpected gaps.
- Round-trip encode-decode test: raw spectra and molecules can be recovered exactly (or within tolerance for numerical features like m/z) after tokenization and detokenization.
- Vocabulary summary report documents total token count, spectral token count, structural token count, special token assignments, and per-modality coverage statistics.

## Limitations

- Vocabulary design requires domain knowledge of typical m/z ranges and intensity distributions; poor choice of discretization can lead to information loss or excessive token expansion.
- The unified vocabulary may not generalize well to mass spectra from different instrumental platforms or chemical domains not represented in the training set used to design vocabularies.
- Bidirectional mapping must handle ties or near-collisions in continuous m/z values; rounding or binning strategies can introduce systematic biases.
- No changelog or versioning signal was found in the repository, making it unclear how vocabulary updates or retraining are managed if new data modalities are added.

## Evidence

- [other] MS-BART introduces a unified vocabulary as a core mechanism to enable end-to-end pretraining, fine-tuning, and alignment of mass spectra and molecular structures within a language model framework.: "MS-BART introduces a unified vocabulary as a core mechanism to enable end-to-end pretraining, fine-tuning, and alignment of mass spectra and molecular structures within a language model framework."
- [other] Define token vocabularies for mass spectral peaks (m/z values and intensities) and molecular structures (SMILES strings or graph tokens) based on typical data ranges and chemical complexity.: "Define token vocabularies for mass spectral peaks (m/z values and intensities) and molecular structures (SMILES strings or graph tokens) based on typical data ranges and chemical complexity."
- [other] Merge the two vocabularies into a unified token set, assigning unique token IDs to spectral features and structural elements while preserving special tokens (BOS, EOS, PAD, UNK).: "Merge the two vocabularies into a unified token set, assigning unique token IDs to spectral features and structural elements while preserving special tokens (BOS, EOS, PAD, UNK)."
- [other] Validate the vocabulary by encoding representative mass spectra and molecular structures to verify all data types tokenize correctly, no token collisions occur, and coverage of the data domain is complete.: "Validate the vocabulary by encoding representative mass spectra and molecular structures to verify all data types tokenize correctly, no token collisions occur, and coverage of the data domain is"
- [intro] MS-BART is the first to leverage language model for mass spectra structure elucidation by introducing a unified vocabulary and enabling end-to-end pretraining, fine-tuning, and alignment.: "MS-BART is the first to leverage language model for mass spectra structure elucidation by introducing a unified vocabulary and enabling end-to-end pretraining, fine-tuning, and alignment."
