---
name: molecular-graph-encoder-decoder-training
description: Use when when you have a training dataset of NMR spectra-derived molecular
  fragments encoded as token sequences, and you need to predict both the molecular
  formula and complete bond connectivity of unknown molecules.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0154
  tools:
  - PyTorch
  - Transformer (architecture)
  techniques:
  - NMR
  license_tier: open
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

# molecular-graph-encoder-decoder-training

## Summary

Train a transformer encoder-decoder architecture to map molecular fragment embeddings to complete molecular structures by predicting both molecular formula (via classification) and bond connectivity (via link prediction on molecular graphs). This skill enables automated assembly of fragmented spectroscopic data into chemically valid structures.

## When to use

When you have a training dataset of NMR spectra-derived molecular fragments encoded as token sequences, and you need to predict both the molecular formula and complete bond connectivity of unknown molecules. Apply this skill when traditional fragment-assembly approaches are insufficient for high-throughput structure elucidation from spectroscopic data on molecules with up to 19 heavy atoms.

## When NOT to use

- Molecules with more than 19 heavy (non-hydrogen) atoms — framework effectiveness is only demonstrated up to this size
- When you already have complete molecular structures (not fragments) — the skill is designed to assemble fragments, not refine complete structures
- When input spectra are multidimensional (2D NMR or higher) rather than 1D spectra — the model is trained on 1D ¹H and/or ¹³C NMR inputs

## Inputs

- fragment-to-structure training dataset (fragment token sequences paired with target structures)
- encoded predicted substructures (token sequences)
- target molecular structures (adjacency matrices and formula vectors)
- held-out test set (fragment sequences with ground-truth formula and connectivity)

## Outputs

- trained transformer encoder-decoder model weights
- predicted molecular formula (classification output)
- predicted bond connectivity (link prediction output on molecular graph)
- validation accuracy metrics for formula and connectivity separately

## How to apply

Prepare a training dataset by encoding predicted substructures as token sequences and target structures as adjacency matrices and formula vectors. Implement a transformer encoder-decoder with multi-head self-attention and cross-attention layers to map fragment embeddings to structure space. Train end-to-end using supervised loss on formula prediction (classification task) and bond connectivity prediction (link prediction on the molecular graph). Validate on held-out test molecules by computing separate accuracy metrics for formula and connectivity predictions. The model learns to reconstruct complete molecular structures from fragmented inputs through joint optimization of both tasks.

## Related tools

- **PyTorch** (Deep learning framework used to implement and train the transformer encoder-decoder architecture with multi-head attention layers)
- **Transformer (architecture)** (Core neural architecture providing encoder-decoder with multi-head self-attention and cross-attention for mapping fragment embeddings to molecular structure space)

## Evaluation signals

- Formula prediction accuracy: percentage of test molecules where predicted molecular formula exactly matches ground truth
- Bond connectivity accuracy: percentage of test molecules where predicted adjacency matrix exactly matches ground truth molecular graph
- Schema validation: all predicted adjacency matrices are symmetric and contain valid bond orders; all predicted formulas satisfy valency constraints
- Separate metric reporting: formula and connectivity accuracies are computed independently and reported as distinct values
- Convergence: supervised loss on both tasks decreases monotonically during training and plateaus on validation data

## Limitations

- Framework is only validated on molecules with up to 19 heavy atoms; performance on larger molecules is unknown
- Requires end-to-end labeled training data with both fragment token sequences and ground-truth adjacency matrices and formula vectors
- Model assumes fragments are derived from 1D ¹H and/or ¹³C NMR spectra; applicability to other spectroscopic modalities is not established

## Evidence

- [other] Fragment-to-structure dataset preparation and encoding: "Prepare fragment-to-structure training dataset by encoding predicted substructures as token sequences and target structures as adjacency matrices and formula vectors"
- [intro] Transformer architecture with attention mechanisms: "a transformer architecture can be constructed to efficiently solve the task, traditionally performed by chemists, of assembling large numbers of molecular fragments into molecular"
- [other] Dual loss formulation for formula and connectivity: "Train the transformer end-to-end using supervised loss on formula prediction (classification) and bond connectivity prediction (link prediction on molecular graph)"
- [other] Validation methodology with separate accuracy metrics: "Validate the trained model on held-out test molecules by comparing predicted formula and connectivity to ground truth, computing accuracy metrics for both outputs separately"
- [intro] Scope: molecules up to 19 heavy atoms: "We demonstrate the effectiveness of this framework on molecules with up to 19 heavy (non-hydrogen) atoms"
