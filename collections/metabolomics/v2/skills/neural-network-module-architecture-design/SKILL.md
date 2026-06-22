---
name: neural-network-module-architecture-design
description: Use when when building an end-to-end deep learning model that must predict multiple correlated peptide properties (charge, isotope count, retention time) simultaneously from mass spectrometry data, and you need a principled way to merge learned representations from separate task-specific branches.
license: CC-BY-4.0
metadata:
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - PyTorch
  - IsoFusion
derived_from:
- doi: 10.26599/bdma.2024.9020059
  title: IsoFusion
evidence_spans:
- _No usage/docs found._
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_isofusion_cq
    doi: 10.26599/bdma.2024.9020059
    title: IsoFusion
  dedup_kept_from: coll_isofusion_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.26599/bdma.2024.9020059
  all_source_dois:
  - 10.26599/bdma.2024.9020059
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# neural-network-module-architecture-design

## Summary

Design and implement a multi-branch neural network fusion module that integrates feature tensors from independent prediction tasks (isotope, charge, retention time) into a unified representation. This skill is essential for multi-task learning architectures where auxiliary tasks must contribute learned features to improve main task performance through joint optimization.

## When to use

When building an end-to-end deep learning model that must predict multiple correlated peptide properties (charge, isotope count, retention time) simultaneously from mass spectrometry data, and you need a principled way to merge learned representations from separate task-specific branches so that gradient signals from all tasks can jointly optimize shared feature extraction.

## When NOT to use

- When auxiliary tasks are not expected to share or benefit from feature fusion (e.g., completely independent prediction problems with no causal or informational coupling).
- When input feature tensors are already a single unified representation rather than separate task-specific branches.

## Inputs

- Feature tensor from isotope prediction branch (shape: [batch_size, isotope_feature_dim])
- Feature tensor from charge prediction branch (shape: [batch_size, charge_feature_dim])
- Feature tensor from retention-time prediction branch (shape: [batch_size, rt_feature_dim])

## Outputs

- Unified fused feature representation (shape: [batch_size, fused_feature_dim])
- Multi-task learning gradients flowing back to each branch

## How to apply

Define a FuseBlock module architecture in PyTorch that accepts three separate feature tensors (one per prediction branch: isotope, charge, retention-time). Concatenate or apply learned weighted combination across the three feature dimensions to produce an intermediate fused tensor. Pass the fused tensor through a series of fully connected layers to produce a unified feature representation. Critically, ensure that the backpropagation path from the fused representation flows bidirectionally back to each branch's feature tensor so that gradients from all task losses propagate through the fusion layer. Validate output shape consistency and verify gradient flow during backpropagation by inspecting gradient norms at each branch.

## Related tools

- **PyTorch** (Deep learning framework used to implement the FuseBlock module, fully connected layers, and gradient backpropagation for multi-task learning.)
- **IsoFusion** (End-to-end peptide feature detection model that implements FuseBlock as a core architectural component for integrating charge, isotope, and retention-time predictions.) — https://github.com/xfcui/IsoFusion

## Examples

```
In PyTorch: `fused = FuseBlock(isotope_features, charge_features, rt_features)` where each input is shape `[batch_size, dim]`; then compute combined loss as `loss = main_task_loss(pred, target) + 0.1 * isotope_aux_loss + 0.1 * charge_aux_loss + 0.1 * rt_aux_loss` and backpropagate with `loss.backward()`.
```

## Evaluation signals

- Output tensor shape matches expected fused feature dimensionality (e.g., concatenation of three 64-dim branches produces 192-dim intermediate, then reduces to 128-dim after FC layers).
- Gradient norm is non-zero and finite at each branch input during backpropagation (verify using `tensor.grad` inspection after loss.backward()).
- All three branch gradients are non-zero simultaneously, confirming multi-task learning signal propagation is active.
- Main task performance improves when auxiliary task losses are included in the combined loss function, demonstrating that feature fusion enables auxiliary tasks to enhance main task learning.
- Ablation test: removing one branch's input or freezing its gradients produces measurable degradation in main task performance, confirming interdependency.

## Limitations

- The design assumes all three branches have compatible feature representations; significant dimension mismatch may require learned projection layers before concatenation.
- The ratio of auxiliary task loss weights to main task loss must be tuned; inappropriate weighting can cause auxiliary tasks to dominate and degrade main task performance.
- No quantitative guidance is provided in the article on choice of intermediate FC layer sizes or activation functions for the fusion block.

## Evidence

- [other] FuseBlock component designed to integrate features from different dimensions: "FuseBlock component designed to integrate features from different dimensions as part of its novel end-to-end architecture for peptide feature detection"
- [readme] Multi-task learning auxiliary task contribution: "Using the multi-task learning to predict charge, number of isotopes and retention time simultaneously, the auxiliary task can help improve the learning performance of the main task"
- [other] Feature fusion implementation steps: "Implement dimension-wise feature fusion using concatenation or learned weighted combination across the three feature dimensions. Apply a series of fully connected layers to produce a unified fused"
- [other] Gradient flow validation requirement: "Integrate gradient flow from the fused representation back to each feature dimension branch to enable multi-task learning signal propagation. Validate the module outputs expected shape and verify"
- [readme] End-to-end model prediction targets: "our model is an end-to-end model that can predict charge, number of isotopes and retention time directly from the mass spectrum"
