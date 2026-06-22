---
name: cross-domain-token-mapping
description: Use when when building a unified sequence model (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_0599
  - http://edamontology.org/topic_3372
  tools:
  - BART
derived_from:
- doi: 10.48550/arxiv.2510.20615
  title: MS-BART
evidence_spans:
- MS-BART is the first to leverage language model for mass spectra structure elucidation by introducing a unified vocabulary
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

# cross-domain-token-mapping

## Summary

Construct a unified token vocabulary that bridges mass spectra and molecular structures, enabling a single language model to jointly encode and decode both spectral peak data (m/z values, intensities) and chemical structures (SMILES or graph tokens). This skill is essential for end-to-end pretraining and fine-tuning in multimodal chemistry models.

## When to use

When building a unified sequence model (e.g., BART, transformer) that must process both mass spectrometry data and molecular structures as parallel modalities, and you need to ensure that spectral tokens and structural tokens can be embedded and decoded from a single shared latent space without collision or information loss.

## When NOT to use

- Input modalities are already pre-tokenized in separate vocabularies and will not be jointly modeled in a single encoder/decoder—use separate vocabularies instead.
- Your downstream task requires modality-specific token spaces with intentional separation (e.g., to preserve spectral-only or structure-only interpretability).
- Token collision is acceptable or desired for dimensionality reduction; unified vocabulary is designed to preserve modality distinction.

## Inputs

- mass spectral peak lists (m/z values paired with intensities)
- molecular structure representations (SMILES strings or molecular graphs)
- typical data ranges and chemical complexity distributions
- raw spectral and structural datasets for validation

## Outputs

- unified token vocabulary (set of unique token IDs)
- bidirectional token mapping dictionary (raw data ↔ token ID)
- vocabulary statistics report (total tokens, spectral/structural token counts, special token assignments)
- vocabulary coverage metrics (domain completeness validation)

## How to apply

First, define separate token vocabularies for mass spectral peaks (m/z values and intensities normalized to typical data ranges) and molecular structures (SMILES strings tokenized or graph-based tokens representing chemical complexity). Merge these vocabularies into a single token set, assigning unique token IDs to each spectral feature and structural element while preserving special tokens (BOS, EOS, PAD, UNK). Create a bidirectional mapping dictionary for efficient encoding/decoding of raw spectral and structural data. Validate the unified vocabulary by encoding representative mass spectra and molecular structures to verify all data types tokenize without collisions and coverage spans the full data domain. Generate a coverage report documenting total token count, spectral token count, structural token count, special token assignments, and domain coverage metrics to confirm vocabulary completeness.

## Related tools

- **BART** (Sequence-to-sequence denoising autoencoder framework used to embed and jointly model unified token vocabularies from both mass spectra and molecules) — github.com/OpenDFM/MS-BART

## Evaluation signals

- All mass spectral peaks (m/z and intensity pairs) and molecular structures encode without raising UNK (unknown) token errors, indicating complete domain coverage.
- Bidirectional mapping dictionary round-trips correctly: raw data → tokens → raw data with no information loss or ambiguity.
- No token ID collisions detected between spectral and structural features; each token uniquely maps to exactly one data element.
- Vocabulary coverage report shows >95% of held-out validation spectra and molecules tokenize using the unified vocabulary without truncation.
- Special tokens (BOS, EOS, PAD, UNK) are preserved and correctly assigned, enabling proper sequence framing in the language model.

## Limitations

- Unified vocabulary size grows with the union of spectral and structural token spaces; large vocabularies may increase memory overhead and training time in downstream models.
- Vocabulary is domain-specific to the training data distribution; transfer to mass spectra or molecules from different instruments, ionization methods, or chemical scaffolds may require revalidation or vocabulary expansion.
- No explicit mechanism described for handling rare or out-of-distribution spectral peaks or novel chemical scaffolds not represented in the vocabulary construction data.

## Evidence

- [other] Define token vocabularies for mass spectral peaks (m/z values and intensities) and molecular structures (SMILES strings or graph tokens) based on typical data ranges and chemical complexity.: "Define token vocabularies for mass spectral peaks (m/z values and intensities) and molecular structures (SMILES strings or graph tokens) based on typical data ranges and chemical complexity."
- [other] Merge the two vocabularies into a unified token set, assigning unique token IDs to spectral features and structural elements while preserving special tokens (BOS, EOS, PAD, UNK).: "Merge the two vocabularies into a unified token set, assigning unique token IDs to spectral features and structural elements while preserving special tokens (BOS, EOS, PAD, UNK)."
- [other] Validate the vocabulary by encoding representative mass spectra and molecular structures to verify all data types tokenize correctly, no token collisions occur, and coverage of the data domain is complete.: "Validate the vocabulary by encoding representative mass spectra and molecular structures to verify all data types tokenize correctly, no token collisions occur, and coverage of the data domain is"
- [intro] MS-BART is the first to leverage language model for mass spectra structure elucidation by introducing a unified vocabulary and enabling end-to-end pretraining, fine-tuning, and alignment.: "MS-BART is the first to leverage language model for mass spectra structure elucidation by introducing a unified vocabulary and enabling end-to-end pretraining, fine-tuning, and alignment."
- [other] Create a bidirectional mapping dictionary between raw spectral/structural data and token IDs for efficient encoding/decoding.: "Create a bidirectional mapping dictionary between raw spectral/structural data and token IDs for efficient encoding/decoding."
