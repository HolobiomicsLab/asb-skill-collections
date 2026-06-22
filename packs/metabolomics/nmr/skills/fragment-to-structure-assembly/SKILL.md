---
name: fragment-to-structure-assembly
description: Use when when you have spectroscopic measurements (1D ¹H or ¹³C NMR) that have been decomposed into predicted substructures or fragments, and you need to reconstruct the full molecular formula and connectivity graph.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3379
  tools:
  - PyTorch
  - Transformer (multi-head self-attention and cross-attention architecture)
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# fragment-to-structure-assembly

## Summary

Use a transformer encoder-decoder architecture to assemble predicted molecular fragments (encoded as token sequences) into complete molecular structures by jointly predicting molecular formula and bond connectivity. This skill maps fragment embeddings to structure space via multi-head attention, enabling rapid structure elucidation from spectroscopic data.

## When to use

When you have spectroscopic measurements (1D ¹H or ¹³C NMR) that have been decomposed into predicted substructures or fragments, and you need to reconstruct the full molecular formula and connectivity graph. The input must be a set of fragment tokens with corresponding embedding representations and a target output space defined as (molecular formula vector, adjacency matrix). This is the appropriate step after fragment prediction and before final structure validation.

## When NOT to use

- When molecular fragments are not available or cannot be reliably predicted from input spectra; use end-to-end spectrum-to-structure models instead.
- When dealing with molecules larger than 19 heavy atoms, as the model was validated only on this scope.
- When the target structure cannot be represented as a single connected molecular graph (e.g., multi-component mixtures or salts with distinct ions).

## Inputs

- Fragment token sequences (predicted substructures encoded as integer or categorical tokens)
- Fragment embedding vectors (output from a prior fragment prediction or encoding module)
- Target molecular formula vectors (element counts and formal charges as dense vectors or one-hot encodings)
- Target adjacency matrices (bond connectivity as NxN matrices, where N is the number of atoms)

## Outputs

- Predicted molecular formula vector (element composition and formal charge prediction)
- Predicted adjacency matrix (bond connectivity graph)
- Accuracy metric for formula prediction (classification accuracy or F1 score per element)
- Accuracy metric for connectivity prediction (graph-level or edge-level classification metrics)
- Trained transformer model weights

## How to apply

Encode predicted molecular fragments as token sequences and prepare target structures as both formula vectors (e.g., one-hot or continuous representations of element counts) and adjacency matrices representing bond connectivity. Implement a transformer encoder-decoder with multi-head self-attention to process fragment embeddings and cross-attention layers to map those embeddings into the structure prediction space. Train end-to-end using supervised loss: a classification loss for formula prediction (predicting element counts and charges) and a link-prediction loss on the molecular graph for bond connectivity (e.g., binary cross-entropy on adjacency matrix edges). Validate on held-out test molecules by computing separate accuracy metrics for formula prediction and connectivity prediction; compare predicted adjacency matrices and formulae to ground truth using graph edit distance or Tanimoto similarity for connectivity and exact-match or Levenshtein distance for formula. The model is effective for molecules up to 19 heavy atoms; effectiveness degrades beyond this scope.

## Related tools

- **PyTorch** (Deep learning framework for implementing the transformer encoder-decoder architecture, training the model with supervised loss, and performing inference on held-out test molecules.)
- **Transformer (multi-head self-attention and cross-attention architecture)** (Core neural architecture for mapping fragment embeddings to structure space via learned attention mechanisms over fragments and cross-attention to output structure tokens.)

## Evaluation signals

- Formula prediction accuracy: percentage of test molecules where predicted element composition and formal charge exactly match ground truth.
- Connectivity prediction accuracy: edge-level or graph-level classification metrics on adjacency matrix predictions (e.g., true positive rate, precision, recall for bond existence).
- Adjacency matrix schema validation: confirm predicted matrices are symmetric, have appropriate atom counts matching formula predictions, and contain only valid bond orders.
- Comparison of predicted and ground-truth molecular graphs: compute graph edit distance or canonical SMILES Tanimoto similarity to ensure predicted connectivity is chemically feasible.
- Separation of loss signals: validate that formula loss and connectivity loss both decrease during training and that they do not trade off adversarially at convergence.

## Limitations

- Effectiveness demonstrated only for molecules with up to 19 heavy (non-hydrogen) atoms; scalability to larger molecules is unvalidated.
- Model assumes fragments are correctly predicted prior to assembly; propagates errors from upstream fragment prediction step.
- Requires paired training data of fragment token sequences and ground-truth molecular structures (formula and adjacency matrices), which may be expensive to generate for novel compound classes.
- Does not explicitly model stereochemistry or 3D spatial information; outputs are 2D connectivity only.

## Evidence

- [intro] transformer_architecture_for_assembly: "we show how a transformer architecture can be constructed to efficiently solve the task, traditionally performed by chemists, of assembling large numbers of molecular fragments into molecular"
- [other] fragment_to_structure_training_workflow: "Prepare fragment-to-structure training dataset by encoding predicted substructures as token sequences and target structures as adjacency matrices and formula vectors"
- [other] encoder_decoder_with_attention: "Implement transformer encoder-decoder architecture with multi-head self-attention and cross-attention layers to map fragment embeddings to structure space"
- [other] supervised_loss_formula_and_connectivity: "Train the transformer end-to-end using supervised loss on formula prediction (classification) and bond connectivity prediction (link prediction on molecular graph)"
- [other] validation_on_test_molecules: "Validate the trained model on held-out test molecules by comparing predicted formula and connectivity to ground truth, computing accuracy metrics for both outputs"
- [intro] scope_heavy_atoms: "We demonstrate the effectiveness of this framework on molecules with up to 19 heavy (non-hydrogen) atoms"
