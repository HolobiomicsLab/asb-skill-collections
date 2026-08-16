---
name: positional-encoding-implementation
description: Use when you need to feed discrete chemical formula representations (e.g.,
  'C6H12O6') into a neural network that requires continuous vector inputs, particularly
  when adopting a transformer architecture for formula ranking or property prediction
  tasks.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3314
  - http://edamontology.org/topic_0091
  tools:
  - SCARF
  - MIST-CF formula transformer
  license_tier: open
derived_from:
- doi: 10.1021/acs.jcim.3c01082
  title: mistcf
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mistcf_cq
    doi: 10.1021/acs.jcim.3c01082
    title: mistcf
  dedup_kept_from: coll_mistcf_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jcim.3c01082
  all_source_dois:
  - 10.1021/acs.jcim.3c01082
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Positional Encoding Implementation

## Summary

Implement sinusoidal positional encodings to convert discrete chemical formula strings into fixed-length continuous embedding vectors for neural network input. This technique, developed in SCARF, enables transformer architectures to process chemical formulae by mapping element counts and positions to orthogonal sinusoidal basis functions.

## When to use

Use this skill when you need to feed discrete chemical formula representations (e.g., 'C6H12O6') into a neural network that requires continuous vector inputs, particularly when adopting a transformer architecture for formula ranking or property prediction tasks. Sinusoidal encoding is especially valuable when formula diversity is high and you need position-invariant, orthogonal representations.

## When NOT to use

- Input is already a pre-computed continuous embedding or feature vector—skip re-encoding.
- The downstream task does not use transformer or attention-based architectures; simpler one-hot or fingerprint encodings may suffice.
- Formula strings are already standardized as fixed-size tensors in your pipeline; avoid redundant re-encoding.

## Inputs

- Discrete chemical formula strings (e.g., 'C6H12O6')
- Reference dataset of chemical formulae (for dimensionality validation)
- Sinusoidal encoding hyperparameters (dimensionality, frequency scales)

## Outputs

- Fixed-length embedding vectors (continuous representations of formulae)
- Embedding output table with sample formulae and their vectors
- Validation report on embedding orthogonality and dimensionality coverage

## How to apply

Define a sinusoidal positional encoding scheme that applies sine and cosine functions to element counts and their positions within the formula string. Implement an encoder that parses discrete chemical formula strings, extracts element symbols and counts, and maps them to fixed-length embedding vectors using the sinusoidal basis functions at different frequency scales. Validate that embeddings maintain orthogonality across distinct formulae and that the output dimensionality is sufficient to capture the diversity of formulae in your reference dataset. Generate an embedding output table showing sample input formulae paired with their vector representations to enable manual inspection and verification of encoding quality.

## Related tools

- **SCARF** (Prior work that developed the sinusoidal formula embedding technique adopted by MIST-CF) — https://arxiv.org/abs/2303.06470
- **MIST-CF formula transformer** (Neural network architecture that consumes sinusoidal formula embeddings as input) — https://github.com/samgoldman97/mist-cf

## Evaluation signals

- Embedding vectors are fixed-length and dimensionally consistent across all input formulae.
- Orthogonality test: dot products between embeddings of distinct formulae are near zero; cosine similarity is low for chemically dissimilar compounds.
- Coverage validation: embedding dimensionality is sufficient to represent the full diversity of formulae in the reference dataset without saturation.
- Manual inspection: sample embedding output table shows visually distinct vector patterns for chemically diverse formulae (e.g., organic vs. inorganic, high vs. low atomic mass).
- Downstream performance: transformer model trained on sinusoidal embeddings achieves baseline or improved formula ranking accuracy vs. alternative encoding schemes.

## Limitations

- Sinusoidal encoding is position-dependent; order of elements in the formula string affects the embedding. Canonicalization of formula strings is recommended for consistency.
- Fixed-length embedding dimensionality may not scale efficiently to very large or highly diverse formula spaces; empirical validation on your dataset is essential.
- The technique is most effective within transformer architectures; effectiveness with other neural network types (e.g., simple feedforward networks) has not been characterized in the article.
- Only positive mode adduct types are supported in the current MIST-CF implementation; negative mode or other ionization modes require architectural extension.

## Evidence

- [readme] Utilizing sinusoidal *formula* embeddings as developed in our previous work [SCARF]: "Utilizing sinusoidal *formula* embeddings as developed in our previous work [SCARF]"
- [other] Define the sinusoidal positional encoding scheme for chemical formulae (sine and cosine functions applied to element counts and positions): "Define the sinusoidal positional encoding scheme for chemical formulae (sine and cosine functions applied to element counts and positions)."
- [other] Implement encoder that maps discrete chemical formula strings to fixed-length embedding vectors using the sinusoidal basis: "Implement encoder that maps discrete chemical formula strings (e.g., 'C6H12O6') to fixed-length embedding vectors using the sinusoidal basis."
- [other] Validate embedding orthogonality and dimensionality against formula diversity in a reference dataset: "Validate embedding orthogonality and dimensionality against formula diversity in a reference dataset."
- [other] Generate embedding output table showing sample formulae and their corresponding vector representations for inspection: "Generate embedding output table showing sample formulae and their corresponding vector representations for inspection."
- [intro] MIST-CF adopts a formula transformer neural network architecture: "MIST-CF adopts a formula transformer neural network architecture and learns in a data dependent fashion"
