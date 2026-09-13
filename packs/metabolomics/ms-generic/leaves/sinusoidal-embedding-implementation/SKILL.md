---
name: sinusoidal-embedding-implementation
description: Use when building a transformer-based neural network for chemical formula
  ranking or classification from mass spectrometry spectra, and you need to encode
  categorical chemical formulas (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3365
  edam_topics:
  - http://edamontology.org/topic_0218
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3407
  tools:
  - MIST
  - SCARF
  - MIST-CF
  - SIRIUS
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jcim.3c01082
  title: mistcf
evidence_spans:
- an extension of MIST for annotating MS1 precursor masses from MS/MS data
- Utilizing sinusoidal formula embeddings as developed in our previous work SCARF
- MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum
  using an end-to-end energy based modeling approach
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mistcf
    doi: 10.1021/acs.jcim.3c01082
    title: mistcf
  dedup_kept_from: coll_mistcf
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

# Sinusoidal Embedding Implementation

## Summary

Implement sinusoidal formula embeddings to convert chemical formulas into fixed-dimensional continuous vector representations using trigonometric positional encoding. This technique, developed in SCARF and adopted in MIST-CF, enables neural network models to learn chemical structure patterns from mass spectrometry data.

## When to use

Use this skill when building a transformer-based neural network for chemical formula ranking or classification from mass spectrometry spectra, and you need to encode categorical chemical formulas (e.g., C6H12O6, C3H7NO2) into learnable continuous embeddings that preserve formula structure semantics for downstream transformer layers.

## When NOT to use

- Input is already a pre-computed feature matrix or fingerprint representation; sinusoidal embedding is a raw formula encoding step, not a post-hoc transformation.
- Your model does not use a transformer architecture; sinusoidal embeddings are most effective as positional encodings for attention-based layers.
- Formula strings are malformed or contain unsupported elements; verify chemical formula validity before embedding.

## Inputs

- Chemical formula strings (e.g., 'C6H12O6', 'C3H7NO2', 'C8H10N4O2')
- Embedding dimensionality parameter (integer)
- Batch of formula candidates from SIRIUS decomposition or enumeration

## Outputs

- Embedding vectors of shape (batch_size, embedding_dim)
- Validation results confirming numerical range and dimensionality
- Structured output file containing embedding vectors and metadata

## How to apply

Instantiate a sinusoidal embedding layer with a configured embedding dimensionality parameter (commonly used in MIST-CF transformer architecture). For each input chemical formula, invoke the forward pass to produce embedding vectors. The layer applies sinusoidal positional encoding based on the formula's elemental composition or sequence, similar to positional embeddings in transformer architectures. Verify that output embedding vectors match the configured embedding dimension and fall within the expected numerical range (typically [-1, 1] for sinusoidal embeddings). Validate reproducibility by comparing produced embeddings against reference outputs from the SCARF or MIST-CF codebase using numerical tolerance (e.g., L2 distance < 1e-6).

## Related tools

- **MIST-CF** (Adopts sinusoidal formula embeddings as a core component of its chemical formula transformer architecture for de novo mass spectrometry annotation) — https://github.com/samgoldman97/mist-cf
- **SCARF** (Original work that developed and published sinusoidal formula embedding technique; serves as methodological foundation) — https://arxiv.org/abs/2303.06470
- **SIRIUS** (Provides dynamic programming algorithm (SIRIUS decomp) to enumerate candidate chemical formulas for a given MS1 mass; output formulas are fed into sinusoidal embedding layer) — https://bio.informatik.uni-jena.de/software/sirius/

## Examples

```
from mist_cf.models import FormulaEmbeddingLayer; embedder = FormulaEmbeddingLayer(embedding_dim=256); formulas = ['C6H12O6', 'C3H7NO2', 'C8H10N4O2']; embeddings = embedder(formulas); assert embeddings.shape == (3, 256) and embeddings.min() >= -1.0 and embeddings.max() <= 1.0
```

## Evaluation signals

- Embedding vector dimensionality matches the configured embedding_dim parameter (e.g., shape (batch_size, 256))
- All embedding values are bounded within expected range, typically [-1, 1] for sinusoidal functions
- L2 distance between reproduced embeddings and reference outputs from MIST-CF repository is below numerical tolerance threshold (< 1e-6)
- Embeddings for identical formulas are deterministic and reproducible across multiple forward passes
- Embeddings for different formulas produce distinct vectors with meaningful cosine similarity patterns (chemically similar formulas have higher similarity)

## Limitations

- Sinusoidal embeddings are specifically designed for transformer architectures; may not transfer well to other model types without adaptation.
- Implementation details (dimensionality, encoding scheme, maximum formula length) must match SCARF/MIST-CF specifications for reproducibility; custom hyperparameter tuning is not discussed in the paper.
- Only positive-mode mass spectrometry is currently supported in MIST-CF; adaptation to negative-mode or neutral-loss formula embeddings requires separate implementation.
- Formula enumeration relies on SIRIUS decomposition algorithm; embedding quality depends on upstream candidate generation and may fail for atypical or novel chemical structures.

## Evidence

- [other] MIST-CF incorporates sinusoidal formula embeddings, a technique developed in prior work (SCARF), as an advance to the chemical formula transformer architecture: "MIST-CF incorporates sinusoidal formula embeddings, a technique developed in prior work (SCARF), as an advance to the chemical formula transformer architecture for improved representation of chemical"
- [other] Instantiate the sinusoidal embedding layer with its configured dimensionality and invoke the forward pass on each formula to produce embedding vectors: "Instantiate the sinusoidal embedding layer with its configured dimensionality and invoke the forward pass on each formula to produce embedding vectors."
- [other] Verify all embedding values fall within the expected numerical range (typically [-1, 1] for sinusoidal embeddings): "Verify all embedding values fall within the expected numerical range (typically [-1, 1] for sinusoidal embeddings)."
- [other] Compare produced embeddings against reference outputs from the MIST-CF repository using numerical tolerance (e.g., L2 distance < 1e-6) to confirm reproducibility: "Compare produced embeddings against reference outputs from the MIST-CF repository using numerical tolerance (e.g., L2 distance < 1e-6) to confirm reproducibility."
- [readme] Utilizing sinusoidal *formula* embeddings as developed in our previous work SCARF: "Utilizing sinusoidal *formula* embeddings as developed in our previous work SCARF"
- [intro] MIST-CF adopts a formula transformer neural network architecture and learns in a data dependent fashion instead of computing fragmentation trees: "MIST-CF adopts a formula transformer neural network architecture and learns in a data dependent fashion instead of computing fragmentation trees"
