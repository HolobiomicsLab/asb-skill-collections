---
name: bond-connectivity-prediction
description: Use when you have predicted or partially assembled molecular fragments (as token sequences or substructure embeddings) and need to determine which atoms are bonded to which—that is, when the formula (atom inventory) is known or predicted but the connectivity graph is uncertain.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0276
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3474
  tools:
  - PyTorch
  - Transformer (architecture)
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# bond-connectivity-prediction

## Summary

Predict molecular bond connectivity (graph structure) from spectroscopic or fragmentary inputs using transformer-based link prediction on molecular graphs. This skill recovers the missing edges and atom adjacencies in a partial or inferred molecular structure.

## When to use

Apply this skill when you have predicted or partially assembled molecular fragments (as token sequences or substructure embeddings) and need to determine which atoms are bonded to which—that is, when the formula (atom inventory) is known or predicted but the connectivity graph is uncertain. This is the typical downstream task after fragment assembly or when NMR spectra yield atom counts but not bond topology.

## When NOT to use

- Input is a complete, validated molecular structure with all bonds already specified—no prediction is needed.
- Only atom formula (elemental composition) is required and bond topology is not of interest.
- Molecules exceed 19 heavy atoms; the model in the source article is only validated up to this limit.

## Inputs

- Fragment token sequences (encoded substructures or predicted fragments)
- Adjacency matrices or bond-type tensors (ground truth for training)
- Atom embeddings or fragment embeddings (from prior assembly or encoding step)
- Molecular graphs with known atom positions and partial or missing edges

## Outputs

- Predicted adjacency matrix (binary or multi-class per bond type)
- Bond connectivity accuracy metrics (edge-level precision, recall, F1)
- Predicted molecular graph with inferred bond topology
- Per-atom bond predictions or edge scores for uncertainty quantification

## How to apply

Encode predicted substructures or molecular fragments as token sequences and represent target structures as adjacency matrices. Implement a transformer encoder-decoder architecture with multi-head self-attention and cross-attention layers to map fragment embeddings to a bond prediction space. Train the model end-to-end using supervised link prediction loss on the molecular graph (treating bond prediction as a binary classification task for each potential atom pair). At inference, compute predicted bond adjacency by thresholding the model's link prediction scores (or by taking the argmax over bond-type classes if distinguishing single/double/triple bonds). Validate by comparing predicted connectivity to ground-truth adjacency matrices using edge-level accuracy, precision, recall, or F1 score on the test set.

## Related tools

- **PyTorch** (Deep learning framework for implementing transformer encoder-decoder with attention mechanisms and supervised loss training for link prediction)
- **Transformer (architecture)** (Encoder-decoder architecture with multi-head self-attention and cross-attention layers to map fragment embeddings to bond adjacency predictions)

## Evaluation signals

- Edge-level accuracy: fraction of predicted bonds (true positives + true negatives) matching ground truth adjacency matrix on held-out test set.
- Link prediction F1 score: harmonic mean of precision and recall for predicted bonds, treating each atom pair as a binary classification.
- Valence validation: check that predicted bonds satisfy standard valence rules for the inferred atoms (e.g., carbon valence ≤ 4).
- Connectivity consistency: verify that predicted graph is a connected component (or expected number of components) and contains no isolated atoms given the predicted formula.
- Comparison to ground truth: visualize or diff predicted and ground-truth molecular graphs to identify systematic errors (e.g., ring closure mismatches).

## Limitations

- Effectiveness is demonstrated only for molecules with up to 19 heavy (non-hydrogen) atoms; performance on larger molecules is not reported.
- Model assumes fragment token sequences are already available or accurately predicted; errors in fragment assembly propagate to bond prediction.
- Transformer training requires paired fragment-to-adjacency data; availability and quality of training datasets for diverse chemical spaces may be limiting.
- Bond-type distinction (single/double/triple) is treated as multi-class prediction; performance per bond type is not separately reported in the source article.

## Evidence

- [intro] Transformer for bond prediction: "a transformer architecture can be constructed to efficiently solve the task, traditionally performed by chemists, of assembling large numbers of molecular fragments into molecular"
- [other] Bond connectivity as link prediction task: "bond connectivity prediction (link prediction on molecular graph)"
- [other] End-to-end supervised training on adjacency matrices: "Train the transformer end-to-end using supervised loss on formula prediction (classification) and bond connectivity prediction (link prediction on molecular graph)"
- [other] Validation on held-out test molecules: "Validate the trained model on held-out test molecules by comparing predicted formula and connectivity to ground truth, computing accuracy metrics for both outputs"
- [intro] Scope: up to 19 heavy atoms: "We demonstrate the effectiveness of this framework on molecules with up to 19 heavy (non-hydrogen) atoms"
