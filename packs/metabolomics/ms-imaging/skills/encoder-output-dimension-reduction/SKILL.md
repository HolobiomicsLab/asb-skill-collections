---
name: encoder-output-dimension-reduction
description: 'Use when you have 512-dimensional representation vectors output from paired ResNet18 encoders processing augmented ion images, and you need to: (1) introduce an intermediate projection space to enable contrastive loss optimization without trivial/collapsed solutions, (2) further compress learned.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
  tools:
  - ResNet18
  - UMAP
  - PyTorch
  - kornia
  techniques:
  - MS-imaging
derived_from:
- doi: 10.1021/acs.analchem.3c05002
  title: deepion
evidence_spans:
- Two augmented images are propagated through a pair of ResNet18-based encoders
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_deepion
    doi: 10.1021/acs.analchem.3c05002
    title: deepion
  dedup_kept_from: coll_deepion
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c05002
  all_source_dois:
  - 10.1021/acs.analchem.3c05002
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Encoder Output Dimension Reduction

## Summary

Reduce high-dimensional encoder representations (512-dim vectors from ResNet18) to lower-dimensional spaces suitable for downstream analysis, contrastive learning, or final task-specific embeddings. This skill is essential for avoiding representation collapse during self-supervised learning and for producing interpretable, compact ion image representations in mass spectrometry imaging.

## When to use

Apply this skill when you have 512-dimensional representation vectors output from paired ResNet18 encoders processing augmented ion images, and you need to: (1) introduce an intermediate projection space to enable contrastive loss optimization without trivial/collapsed solutions, (2) further compress learned representations into a final low-dimensional embedding (e.g., 20-dim) for downstream co-localization or isotope ion analysis, or (3) prevent feature collapse during self-supervised learning of mass spectrometry ion images in COL or ISO modes.

## When NOT to use

- Input is already a low-dimensional feature table or final embedding; further reduction may lose task-relevant information.
- No augmentation strategy is available for the input ion images; contrastive learning requires paired augmented views to be meaningful.
- The downstream analysis requires interpretability of individual dimensions; aggressive dimensionality reduction may obscure feature semantics.

## Inputs

- 512-dimensional representation vectors from paired ResNet18 encoders
- Augmented ion image pairs (two augmentations per original ion image)
- Ion image matrix data with shape [X*Y, P] (pixels × ions)
- Ion peak list data with shape [P, 1]

## Outputs

- Projection space vectors (intermediate dimensionality, optimized for contrastive learning)
- Prediction module outputs (asymmetric projections used in loss computation)
- Final 20-dimensional ion image representation vectors for downstream analysis
- Contrastive loss values (scalar, optimized during training)

## How to apply

The skill is applied in two sequential stages. First, apply a Projection module to transform the 512-dimensional encoder outputs into a lower-dimensional projection space optimized for contrastive learning; follow this with a Prediction module that applies an asymmetric transformation to the projected vectors, introducing the necessary asymmetry to avoid trivial/collapsed solutions during optimization. Compute contrastive loss between the projections (or predictions) of augmented image pairs, maximizing similarity for the same ion image while minimizing similarity across different images. Second, after contrastive pre-training, apply a Dimensionality Reduction module (e.g., UMAP) to further reduce the projection space to a final 20-dimensional vector suitable for downstream tasks such as co-localized ion searching or isotope discovery. The contrastive loss incorporates a stop-gradient operation to prevent gradient flow and further mitigate collapse.

## Related tools

- **ResNet18** (Encoder backbone that outputs 512-dimensional representation vectors from augmented ion images; weights are either frozen or jointly optimized during contrastive pre-training.)
- **UMAP** (Dimensionality reduction algorithm applied in the final Dimensionality Reduction module to compress learned representations to 20-dimensional vectors.)
- **PyTorch** (Deep learning framework for implementing Projection and Prediction modules, contrastive loss computation, and backpropagation.)
- **kornia** (Computer vision library (mentioned in requirements) used for image augmentation operations and transformation pipelines.)

## Examples

```
python run.py --input_Matrix .../DATASET/Pos_brain_data_matrix.txt --input_PeakList .../DATASET/Pos_brain_data_peak.csv --input_shape 198 422 --mode COL --ion_mode positive --num 5 --output_file Pos_COL_result
```

## Evaluation signals

- Contrastive loss converges and decreases over training epochs, indicating successful optimization of the projection/prediction modules.
- Similarity between projections/predictions of augmented pairs from the same ion image is significantly higher than across different images (e.g., cosine similarity > 0.9 within-image, < 0.3 cross-image).
- Final 20-dimensional representations produce well-separated clusters in visualization (t-SNE or UMAP) corresponding to distinct ion populations or co-localization groups.
- Downstream tasks (co-localized ion searching with 'num' parameter, isotope ion discovery) show improved accuracy or recall compared to using raw 512-dim or non-reduced representations.
- No representation collapse (all dimensions active, feature variance across the batch is non-trivial); verify by checking that encoder outputs do not converge to a constant vector.

## Limitations

- Projection and Prediction module architectures and hyperparameters are not explicitly detailed in the README; practitioners must infer or implement based on standard self-supervised learning best practices (e.g., hidden layer sizes, activation functions).
- The skill requires paired augmented images; augmentation strategies differ between COL mode (color jitter, filtering, Poisson noise, random missing value) and ISO mode (additional intensity-dependent missing value), so mode selection must precede dimension reduction.
- Stop-gradient operation and contrastive loss design are critical to prevent collapse; incomplete or incorrect implementation of these components may result in meaningless low-dimensional representations.
- UMAP and other downstream dimensionality reduction steps may introduce hyperparameter sensitivity; no guidance is provided on neighbor count, min_dist, or metric choice for ion image data.

## Evidence

- [readme] Two augmented images are propagated through a pair of ResNet18-based encoders that shared parameters, then output two 512-dimensional representation vectors: "Two augmented images are propagated through a pair of ResNet18-based encoders that shared parameters, then output two 512-dimensional representation vectors"
- [readme] Projection module and Prediction module are used to avoid collapsing solutions during the optimization process of maximizing the similarity between two augmentations from a same image: "Projection module and Prediction module are used to avoid collapsing solutions during the optimization process of maximizing the similarity between two augmentations from a same image"
- [readme] A contrastive loss is employed to maximize similarity with a stop-gradient operation to prevent collapsing during training: "A contrastive loss is employed to maximize similarity with a stop-gradient operation to prevent collapsing during training"
- [readme] Dimensionality Reduction module. This module is applied to further reduce the dimensionality of ion image representation to a 20-dimensional vector O for downstream tasks.: "Dimensionality Reduction module. This module is applied to further reduce the dimensionality of ion image representation to a 20-dimensional vector O for downstream tasks"
- [other] The Projection and Prediction modules process the 512-dimensional representation vectors output by the ResNet18-based encoders to avoid collapsing solutions while optimizing for maximized similarity between augmentations of the same ion image using contrastive loss.: "The Projection and Prediction modules process the 512-dimensional representation vectors output by the ResNet18-based encoders to avoid collapsing solutions while optimizing for maximized similarity"
