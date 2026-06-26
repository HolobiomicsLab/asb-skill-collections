---
name: tensor-embedding-design
description: Use when when you need to represent discrete chemical formulae (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0292
  edam_topics:
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_0080
  tools:
  - SCARF
  - SIRIUS decomp
  license_tier: open
  provenance_tier: literature
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

# Tensor Embedding Design

## Summary

Design and implement sinusoidal formula embeddings to encode discrete chemical formulae as fixed-length dense vectors for neural network input. This technique encodes structural information (element identities and counts) using sine and cosine basis functions, enabling transformer architectures to process chemical composition in a learnable, position-independent manner.

## When to use

When you need to represent discrete chemical formulae (e.g., 'C6H12O6', 'C2H5OH') as continuous input vectors for neural network architectures such as transformers or energy-based models, and you want embeddings that preserve compositional structure and scale predictably with formula complexity.

## When NOT to use

- Input is already a pre-computed or learned feature table (e.g., from a pretrained molecular fingerprinting model) — use the existing embeddings directly.
- Formula representation is continuous or real-valued rather than discrete (e.g., concentrations, fractions) — sinusoidal encoding assumes discrete element identities and counts.
- Your model architecture does not require fixed-length vector input (e.g., if using graph neural networks on explicit molecular graphs) — alternative molecular representations may be more natural.

## Inputs

- Chemical formula strings (e.g., 'C6H12O6', SMILES-like or Hill notation)
- Element count dictionary or parsed formula representation
- Reference dataset of diverse chemical formulae (for validation)
- Target embedding dimensionality (d)

## Outputs

- Sinusoidal formula embedding matrix (N_formulae × d dense vectors)
- Embedding orthogonality validation report
- Sample formula-to-vector reference table
- Encoder function for inference on new formulae

## How to apply

Define a sinusoidal positional encoding scheme that applies sine and cosine functions to element counts and positions within the formula. Implement an encoder that maps discrete chemical formula strings to fixed-length embedding vectors by computing sinusoidal basis values for each element and concatenating them. Validate the embedding quality by checking orthogonality properties across diverse formulae in your reference dataset and confirming that the dimensionality accommodates the range of formula complexities you expect. Generate an embedding reference table showing sample input formulae and their corresponding vector representations to enable visual inspection and debugging. This approach derives from prior work on SCARF and is adopted in MIST-CF because it provides a data-independent, deterministic encoding that does not require learned parameters while maintaining compositional information.

## Related tools

- **SCARF** (Prior work that developed the sinusoidal formula embedding technique adapted in MIST-CF) — https://arxiv.org/abs/2303.06470
- **SIRIUS decomp** (Used upstream to enumerate candidate chemical formulae from observed MS1 masses before embedding) — https://bio.informatik.uni-jena.de/software/sirius/

## Evaluation signals

- Embedding orthogonality: Compute pairwise cosine similarities between embeddings of distinct formulae; expect most similarities to be close to zero (within ±0.1) for formulae with different elemental composition.
- Dimensionality sufficiency: Verify that the embedding dimension is large enough to represent the diversity of formulae in your dataset without saturation (check rank of embedding matrix vs. dimension).
- Consistency check: Re-encoding the same formula string multiple times should produce identical vectors (deterministic properties).
- Scaling test: Confirm that embedding norms scale predictably with formula size (total atom count) across your dataset range.
- Visual inspection: Review the reference table of sample formulae and vectors to spot anomalies (e.g., chemically similar formulae with unexpectedly distant embeddings).

## Limitations

- Sinusoidal embeddings are deterministic and do not learn task-specific representations; they encode only compositional structure, not chemical reactivity, bioactivity, or spectroscopic properties.
- Currently only supports positive mode ionization; negative mode and multiply charged adducts are not yet handled by the MIST-CF implementation.
- Embedding dimensionality must be chosen a priori; there is no adaptive mechanism to scale with formula diversity.
- The scheme assumes standard elemental symbols; non-standard isotopes or exotic elements may require manual extension.

## Evidence

- [readme] SCARF sinusoidal embeddings are the basis of formula encoding: "Utilizing sinusoidal *formula* embeddings as developed in our previous work [SCARF]"
- [other] The workflow for implementing sinusoidal embeddings from the task card: "1. Define the sinusoidal positional encoding scheme for chemical formulae (sine and cosine functions applied to element counts and positions). 2. Implement encoder that maps discrete chemical formula"
- [other] MIST-CF uses sinusoidal formula embeddings for the formula transformer: "MIST-CF uses sinusoidal formula embeddings, a technique developed in prior work on SCARF, to encode chemical formulae for input to the formula transformer neural network architecture."
- [other] Validation approach for embeddings: "Validate embedding orthogonality and dimensionality against formula diversity in a reference dataset."
