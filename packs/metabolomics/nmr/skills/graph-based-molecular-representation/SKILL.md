---
name: graph-based-molecular-representation
description: Use when when you have 1D NMR spectra (¹H and/or ¹³C) as input and need to predict complete molecular structure (both molecular formula and bond connectivity) for molecules with up to 19 heavy atoms.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0337
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3315
  tools:
  - PyTorch
  - Transformer (architecture)
  techniques:
  - NMR
derived_from:
- doi: 10.1021/acscentsci.4c01132
  title: NMR2Struct
evidence_spans:
- transformer architecture
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nmr2struct_cq
    doi: 10.1021/acscentsci.4c01132
    title: NMR2Struct
  dedup_kept_from: coll_nmr2struct_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acscentsci.4c01132
  all_source_dois:
  - 10.1021/acscentsci.4c01132
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# graph-based-molecular-representation

## Summary

Represent molecular structures as graphs with atoms as nodes and bonds as edges, enabling transformer and neural network architectures to learn structure-from-spectra mappings. This representation decouples molecular connectivity and formula prediction into discrete, learnable tasks suitable for end-to-end neural training.

## When to use

When you have 1D NMR spectra (¹H and/or ¹³C) as input and need to predict complete molecular structure (both molecular formula and bond connectivity) for molecules with up to 19 heavy atoms. Use this skill when you want to train a neural model that treats formula prediction and bond connectivity as separate supervised learning tasks that can be jointly optimized.

## When NOT to use

- Input spectra contain molecules with >19 heavy atoms — the framework's demonstrated scope does not extend beyond this
- You require 2D NMR spectra or other spectral modalities — this skill is designed specifically for 1D ¹H and/or ¹³C NMR
- Your goal is to predict only molecular formula without connectivity, or vice versa — the skill's value derives from joint graph-based representation and multitask learning

## Inputs

- fragment token sequences (encoded predicted substructures from spectra)
- molecular structure ground truth (adjacency matrices and formula vectors)
- 1D NMR spectra (¹H and/or ¹³C)

## Outputs

- predicted adjacency matrix (molecular graph connectivity)
- predicted molecular formula vector
- validation accuracy for connectivity prediction
- validation accuracy for formula prediction

## How to apply

Encode target molecular structures as both adjacency matrices (capturing bond connectivity as a graph link-prediction task) and formula vectors (capturing atomic composition as a classification task). Prepare a training dataset by pairing fragment token sequences (derived from predicted substructures) with these dual representations. Train a transformer encoder-decoder architecture with multi-head self-attention and cross-attention layers to map spectra-derived fragment embeddings into this graph space. Use supervised loss on both formula classification and graph connectivity prediction, optimizing jointly. Validate on held-out test molecules by comparing predicted adjacency matrices and formula vectors to ground truth using separate accuracy metrics for each output.

## Related tools

- **PyTorch** (deep learning framework for implementing transformer encoder-decoder and training end-to-end model with supervised loss on adjacency matrices and formula vectors)
- **Transformer (architecture)** (encoder-decoder backbone with multi-head self-attention and cross-attention layers to map fragment embeddings to molecular graph space)

## Evaluation signals

- Predicted adjacency matrices match ground truth bond connectivity with reported accuracy metric across test molecules
- Predicted formula vectors match ground truth molecular formulas with separate reported accuracy metric
- Model successfully reconstructs molecular graphs for held-out test molecules with both connectivity and formula predictions verified independently
- Training/validation loss converges for both formula classification and link prediction tasks during joint optimization
- Predicted structures contain only chemically valid bonds and atom counts consistent with input spectra

## Limitations

- Framework is demonstrated only on molecules with up to 19 heavy (non-hydrogen) atoms; scalability to larger molecules is not validated
- Accuracy of structure prediction depends critically on quality of predicted substructures fed as fragments; errors in fragment prediction propagate to final structure
- Graph-based representation assumes standard valency rules; unusual bonding or charged species may not be handled correctly

## Evidence

- [other] task_001 workflow step 1: "Prepare fragment-to-structure training dataset by encoding predicted substructures as token sequences and target structures as adjacency matrices and formula vectors."
- [other] task_001 workflow step 2: "Implement transformer encoder-decoder architecture with multi-head self-attention and cross-attention layers to map fragment embeddings to structure space."
- [other] task_001 workflow step 3: "Train the transformer end-to-end using supervised loss on formula prediction (classification) and bond connectivity prediction (link prediction on molecular graph)."
- [intro] article intro finding 2: "we show how a transformer architecture can be constructed to efficiently solve the task, traditionally performed by chemists, of assembling large numbers of molecular fragments into molecular"
- [intro] article intro scope: "We demonstrate the effectiveness of this framework on molecules with up to 19 heavy (non-hydrogen) atoms"
