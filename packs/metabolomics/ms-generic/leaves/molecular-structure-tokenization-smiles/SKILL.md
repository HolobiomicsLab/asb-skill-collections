---
name: molecular-structure-tokenization-smiles
description: Use when when you have molecular structures encoded as SMILES strings and need to incorporate them into a multi-modal language model (such as BART) that also processes mass spectra.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3762
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3172
  tools:
  - BART
  techniques:
  - mass-spectrometry
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Molecular Structure Tokenization (SMILES)

## Summary

Convert molecular structures represented as SMILES strings into discrete tokens for integration into a unified vocabulary alongside mass spectral tokens. This enables end-to-end neural modeling of both molecular structures and their corresponding mass spectra within a single sequence-to-sequence framework.

## When to use

When you have molecular structures encoded as SMILES strings and need to incorporate them into a multi-modal language model (such as BART) that also processes mass spectra. This is essential when building a unified vocabulary for joint MS and molecular structure modeling, particularly for structure elucidation tasks where spectral-molecular alignment requires token-level interoperability.

## When NOT to use

- Input molecules are already represented as atom/bond adjacency matrices or graph objects — use graph-based encoders instead of SMILES tokenization.
- You need to preserve continuous molecular descriptors or 3D structural information — SMILES tokenization discards stereochemistry detail and conformational diversity.
- Vocabulary size is severely constrained (e.g., < 100 tokens total) — SMILES coverage will suffer and collision risk increases.

## Inputs

- SMILES strings (chemical structure notation)
- molecular structure dataset (in text or CSV format with SMILES column)
- chemical complexity range specifications (e.g., max molecular weight, atom count limits)

## Outputs

- unified token vocabulary (merged spectral + structural tokens with unique IDs)
- bidirectional token mapping dictionary (SMILES element ↔ token ID)
- vocabulary statistics report (total structural tokens, coverage metrics, token assignments)
- encoded molecular token sequences (ready for BART pretraining/fine-tuning)

## How to apply

Define a token vocabulary for molecular structures by parsing SMILES strings into chemical graph tokens (atoms, bonds, rings, branches, aromaticity markers). Assign unique token IDs to each SMILES element, ensuring no collision with spectral tokens (m/z, intensity) or special tokens (BOS, EOS, PAD, UNK). Create a bidirectional mapping dictionary between raw SMILES data and token IDs for efficient encode/decode. Validate by tokenizing representative molecules from your dataset to verify complete domain coverage, correct handling of chemical notation (e.g., aromatic rings, stereochemistry), and absence of out-of-vocabulary tokens. Generate a vocabulary statistics report documenting structural token count, coverage metrics, and representative tokenization examples.

## Related tools

- **BART** (sequence-to-sequence neural encoder-decoder framework that accepts unified token vocabularies for end-to-end pretraining, fine-tuning, and cross-modal alignment of molecular structures and mass spectra) — https://github.com/OpenDFM/MS-BART

## Evaluation signals

- All SMILES strings in the representative validation set tokenize successfully with zero out-of-vocabulary tokens and no token ID collisions with spectral tokens.
- Token ID mappings are bidirectional and invertible: encoding a SMILES → tokens → decoding reproduces the original SMILES or a chemically equivalent canonical form.
- Vocabulary statistics report confirms structural token count + spectral token count + special tokens equals total vocabulary size with no gaps.
- Coverage metrics show ≥95% of unique SMILES elements in the dataset are represented in the vocabulary.
- BART model successfully ingests the merged vocabulary and processes minibatches of tokenized spectra and molecules during pretraining without dimension mismatches or embedding errors.

## Limitations

- SMILES tokenization does not preserve stereochemistry or 3D conformation information; enantiomers and conformational isomers may collapse to the same token sequence.
- Out-of-vocabulary SMILES elements (unusual bond types, exotic atoms, formal charges not seen in training) will cause tokenization failure; preprocessing and vocabulary expansion may be required.
- Vocabulary size grows with chemical diversity; datasets spanning synthetic chemistry, natural products, and drug-like compounds may require significantly larger vocabularies, increasing memory and training time.
- Token boundaries in SMILES (e.g., multi-character symbols like 'Cl', 'Br', branching parentheses) must be handled carefully to avoid ambiguous segmentation.

## Evidence

- [other] Define token vocabularies for mass spectral peaks (m/z values and intensities) and molecular structures (SMILES strings or graph tokens): "Define token vocabularies for mass spectral peaks (m/z values and intensities) and molecular structures (SMILES strings or graph tokens) based on typical data ranges and chemical complexity."
- [other] Merge the two vocabularies into a unified token set, assigning unique token IDs to spectral features and structural elements while preserving special tokens: "Merge the two vocabularies into a unified token set, assigning unique token IDs to spectral features and structural elements while preserving special tokens (BOS, EOS, PAD, UNK)."
- [other] Create a bidirectional mapping dictionary between raw spectral/structural data and token IDs for efficient encoding/decoding: "Create a bidirectional mapping dictionary between raw spectral/structural data and token IDs for efficient encoding/decoding."
- [other] Validate the vocabulary by encoding representative mass spectra and molecular structures to verify all data types tokenize correctly, no token collisions occur, and coverage of the data domain is complete.: "Validate the vocabulary by encoding representative mass spectra and molecular structures to verify all data types tokenize correctly, no token collisions occur, and coverage of the data domain is"
- [intro] MS-BART is the first to leverage language model for mass spectra structure elucidation by introducing a unified vocabulary and enabling end-to-end pretraining, fine-tuning, and alignment.: "MS-BART is the first to leverage language model for mass spectra structure elucidation by introducing a unified vocabulary and enabling end-to-end pretraining, fine-tuning, and alignment."
