---
name: chemical-formula-tokenization
description: Use when you have collections of chemical formulae (e.g., from SIRIUS decomposition or subformula labeling) derived from MS/MS spectra and need to feed them into a transformer encoder.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0392
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0209
  - http://edamontology.org/topic_3365
  tools:
  - PyTorch
  - Transformer
  - SIRIUS
  - MIST
  - MIST-CF
  - SCARF
  - MIST-CF formula transformer
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1038/s42256-023-00708-3
  title: MIST (chemical formula transformer)
- doi: 10.1021/acs.jcim.3c01082
  title: ''
evidence_spans:
- github.com/samgoldman97/mist
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mist_chemical_formula_transformer_cq
    doi: 10.1038/s42256-023-00708-3
    title: MIST (chemical formula transformer)
  - build: coll_mistcf_cq
    doi: 10.1021/acs.jcim.3c01082
    title: mistcf
  dedup_kept_from: coll_mist_chemical_formula_transformer_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s42256-023-00708-3
  all_source_dois:
  - 10.1038/s42256-023-00708-3
  - 10.1021/acs.jcim.3c01082
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chemical-formula-tokenization

## Summary

Convert chemical formulae extracted from tandem mass spectrometry data into discrete tokens and learned embeddings for use in transformer-based neural networks. This skill bridges raw chemical notation and neural sequence models by establishing a vocabulary and embedding scheme that preserves chemical semantics.

## When to use

Apply this skill when you have collections of chemical formulae (e.g., from SIRIUS decomposition or subformula labeling) derived from MS/MS spectra and need to feed them into a transformer encoder. Use it specifically when direct embedding of binned spectra is insufficient and you want the model to learn relationships between chemical composition patterns and downstream predictions (e.g., molecular fingerprints or precursor formula ranking).

## When NOT to use

- Input is already a feature matrix or pre-computed fingerprint representation—tokenization is unnecessary.
- You have no chemical formulae available; only raw binned spectra or raw m/z peaks without formula annotation.
- Your application requires human-interpretable chemical features or SMARTS patterns rather than learned latent representations; consider rule-based approaches instead.

## Inputs

- Collection of chemical formulae strings (e.g., 'C6H12O6', 'C10H16N2O2') extracted from MS/MS spectra
- Element vocabulary or atomic number mapping
- Unpaired molecule library or training dataset for vocabulary construction (optional but recommended)

## Outputs

- Tokenized formula sequences (integer token IDs per formula)
- Learned embedding matrix mapping tokens to continuous vectors
- Fixed-dimensional formula representation vectors (via pooling) ready for downstream neural tasks

## How to apply

First, build a vocabulary from the set of unique chemical elements and formula patterns observed in your training dataset. Tokenize each formula by mapping its constituent elements and multiplicities to discrete token IDs. Embed each token using a learned embedding layer (e.g., sinusoidal formula embeddings as described in MIST-CF for improved generalization). Pass the embedded token sequences through a transformer encoder with multi-head self-attention to capture inter-element relationships and formula-level structure. Pool or aggregate the final hidden states (via mean pooling, CLS token, or attention-weighted pooling) to produce a fixed-dimensional representation for downstream tasks. The rationale is that learned formula tokenization allows the transformer to discover which chemical composition patterns are predictive of your target property (e.g., fingerprint or adduct type) in a data-dependent fashion, rather than relying on hand-crafted fragmentation trees.

## Related tools

- **Transformer** (Neural sequence encoder that processes tokenized formula sequences with multi-head self-attention to learn formula-level representations)
- **PyTorch** (Deep learning framework for implementing embedding layers, transformer stacks, and training the formula encoding model)
- **SIRIUS** (Provides the dynamic programming algorithm (SIRIUS decomp) to enumerate candidate chemical formulae for observed MS1 masses before tokenization) — https://bio.informatik.uni-jena.de/software/sirius/
- **MIST** (Reference implementation demonstrating transformer-based chemical formula tokenization and encoding for molecular fingerprint prediction from tandem MS) — https://github.com/samgoldman97/mist
- **MIST-CF** (Extended reference implementation with advances in formula tokenization including sinusoidal embeddings, internal subformula assignment, and multi-adduct handling) — https://github.com/samgoldman97/mist-cf

## Evaluation signals

- Verify that tokenized sequences have uniform or padded lengths compatible with transformer batch processing; all formula tokens map to valid IDs in the learned vocabulary.
- Check that the embedding layer produces dense vectors with consistent dimensionality across all tokens; inspect embedding matrix rank to confirm learning capacity.
- Validate that pooled formula representations are fixed-dimensional and exhibit non-zero variance across the training set (not collapsed to a single point).
- Compare downstream task performance (e.g., fingerprint prediction accuracy, formula ranking AUC) against baselines using raw binned spectra or hand-crafted features; improvement indicates effective formula encoding.
- Conduct ablation: verify that sinusoidal or learned embeddings outperform random or one-hot encoding, and that transformer self-attention is capturing meaningful formula patterns (inspect attention weights for co-occurrence of related elements).

## Limitations

- Vocabulary must be constructed from training data; unseen elements or rare formula patterns in test data may be out-of-vocabulary, requiring fallback tokens or re-tokenization strategies.
- Tokenization assumes formulae are correctly extracted and annotated (e.g., via SIRIUS or MAGMa); errors in upstream formula assignment propagate to the embedding.
- Transformer encoding scales quadratically in formula length (number of elements); very large formulae or very diverse chemical spaces may require memory optimization (e.g., sparse attention or hierarchical pooling).
- The learned formula vocabulary is task- and dataset-specific; models trained on one MS dataset (e.g., NPLIB1) may not generalize well to spectra from different instruments (Orbitrap vs. Q-TOF) without retraining or transfer learning.
- Sinusoidal formula embeddings provide inductive bias for element relationships but require careful hyperparameter tuning; standard learned embeddings may be more flexible for novel chemical spaces.

## Evidence

- [other] Tokenize and embed chemical formulae using a learned vocabulary: "Tokenize and embed chemical formulae using a learned vocabulary."
- [intro] MIST applies a transformer architecture to directly encode and learn to represent collections of chemical formulae: "MIST applies a transformer architecture to directly encode and learn to represent collections of chemical formulae, rather than directly embedding binned spectra"
- [readme] Rather than directly embed binned spectra, MIST applies a transformer architecture to directly encode and learn to represent collections of chemical formula: "Rather than directly embed binned spectra, MIST applies a transformer architecture to directly encode and learn to represent collections of chemical formula"
- [readme] Utilizing sinusoidal *formula* embeddings as developed in our previous work SCARF: "Utilizing sinusoidal *formula* embeddings as developed in our previous work [SCARF](https://arxiv.org/abs/2303.06470)"
- [other] Pass embedded formula sequences through a transformer encoder stack with multi-head self-attention: "Pass embedded formula sequences through a transformer encoder stack with multi-head self-attention."
