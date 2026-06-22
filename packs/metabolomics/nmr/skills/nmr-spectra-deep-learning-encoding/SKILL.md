---
name: nmr-spectra-deep-learning-encoding
description: Use when when you have preprocessed 1H NMR spectral data from flavor mixtures or similar compound identification tasks, and you need to identify which compounds are present.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3801
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - Anaconda
  - PyTorch
  - FlavorFormer
  techniques:
  - NMR
derived_from:
- doi: 10.1016/j.microc.2025.115372
  title: FlavorFormer
evidence_spans:
- Python 3.13.2 and Pytorch (version 2.7.0+cu118)
- Install [Anaconda](https://www.anaconda.com/).
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_flavorformer_cq
    doi: 10.1016/j.microc.2025.115372
    title: FlavorFormer
  dedup_kept_from: coll_flavorformer_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1016/j.microc.2025.115372
  all_source_dois:
  - 10.1016/j.microc.2025.115372
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# nmr-spectra-deep-learning-encoding

## Summary

A hybrid CNN-Transformer deep learning approach that combines bi-encoder and cross-encoder architectures with fusion pooling and weighted loss to encode and identify compounds in 1H NMR spectra. This skill addresses the challenge of accurately distinguishing mixture components in NMR data by jointly modeling spectral representations and compound reference embeddings.

## When to use

When you have preprocessed 1H NMR spectral data from flavor mixtures or similar compound identification tasks, and you need to identify which compounds are present. Use this skill when you have labeled training data pairing spectra with known compound identities, and standard spectral matching or simpler classifiers fail to capture the complex relationships between spectral features and multiple possible compounds in a mixture.

## When NOT to use

- Input spectra are not preprocessed or normalized; raw instrument output typically requires baseline correction, peak alignment, and intensity scaling before encoding.
- Unlabeled or very sparsely labeled training data; the weighted loss and bi-encoder/cross-encoder fusion require sufficient supervised compound-spectrum pairs to learn meaningful encodings.
- Single-compound or known-mixture scenarios where classical peak-matching or simpler distance-based methods already achieve acceptable accuracy; this skill introduces significant computational overhead.

## Inputs

- Preprocessed 1H NMR spectral data (vectorized or image-like tensors)
- Compound reference embeddings or labels
- Training dataset with spectrum-compound label pairs
- Test set of unlabeled or held-out spectra

## Outputs

- Trained model checkpoint with learned CNN-Transformer hybrid backbone
- Compound identification predictions (compound ID or probability rankings per spectrum)
- Compound identification accuracy metric
- Ranking metrics (e.g., mean reciprocal rank, NDCG)
- Performance report with evaluation results

## How to apply

Initialize a hybrid CNN-Transformer backbone to extract both local spectral features (via convolutions) and global long-range dependencies (via Transformer attention) from 1H NMR inputs. Build two parallel branches: (1) a bi-encoder that independently encodes spectra and reference compound embeddings, then fuses their CNN and Transformer outputs via fusion pooling; (2) a cross-encoder that jointly processes spectrum-compound pairs to refine relevance scores. Combine logits from both branches using a weighted loss function that balances bi-encoder and cross-encoder contributions. Train end-to-end with backpropagation on the labeled compound-spectrum pairs, then evaluate compound identification accuracy and ranking metrics on held-out test spectra. The weighted loss allows the model to leverage the complementary strengths of independent (bi-encoder) and joint (cross-encoder) processing strategies.

## Related tools

- **PyTorch** (Deep learning framework used to implement the hybrid CNN-Transformer backbone, bi-encoder and cross-encoder branches, fusion pooling layers, and weighted loss training loop)
- **Python** (Primary programming language for implementing the encoding pipeline, data loading, model training, and evaluation)
- **Anaconda** (Environment and package manager for installing Python 3.13.2, PyTorch 2.7.0+cu118, and other dependencies) — https://www.anaconda.com/
- **FlavorFormer** (Reference implementation of the complete bi-encoder/cross-encoder compound identification architecture with fusion pooling and weighted loss) — https://github.com/yfWang01/FlavorFormer

## Examples

```
cd FlavorFormer && conda env create -f environment.yml && conda activate FlavorFormer && jupyter notebook demo.ipynb
```

## Evaluation signals

- Compound identification accuracy on held-out test set improves beyond baseline single-encoder models or classical spectral matching methods
- Both bi-encoder and cross-encoder branches contribute meaningfully to final predictions (inspect learned weights in weighted loss; ablate each branch and verify performance drop)
- Fusion pooling successfully combines CNN local features and Transformer global dependencies (visualize attention patterns and CNN feature maps; verify they capture distinct aspects of spectra)
- Ranking metrics (e.g., mean reciprocal rank, NDCG@k) confirm that correct compounds are ranked near the top of predicted lists, not just present in the top-1 prediction
- Model generalizes to held-out test spectra; compare training and validation loss curves for signs of overfitting; cross-validate on multiple train/test splits if dataset size permits

## Limitations

- Requires sufficient labeled training data pairing spectra with compound identities; performance degrades with sparse or noisy labels.
- Assumes 1H NMR spectral format and preprocessing; method may require retuning or retraining if applied to other NMR modalities (e.g., 13C, 2D NMR) or vastly different chemical domains.
- Computational cost is higher than simpler classifiers due to dual-branch architecture, CNN + Transformer inference, and fusion pooling; inference latency may be prohibitive for real-time high-throughput screening.
- Model interpretability is limited; understanding which spectral regions and compound properties drive predictions requires additional analysis (e.g., attention visualization, saliency maps).

## Evidence

- [intro] incorporating a hybrid CNN and Transformer architecture to capture both local features and global dependencies from 1H NMR spectra: "incorporating a hybrid CNN and Transformer architecture to capture both local features and global dependencies from 1H NMR spectra"
- [intro] leverages a combination of a bi-encoder and cross-encoder, a fusion pooling strategy, and a weighted loss function to identify compounds correctly: "leverages a combination of a bi-encoder and cross-encoder, a fusion pooling strategy, and a weighted loss function to identify compounds correctly"
- [other] Build a bi-encoder branch that encodes spectra and compound reference embeddings independently, using fusion pooling to combine CNN and Transformer outputs. Build a cross-encoder branch that jointly processes spectrum-compound pairs to refine relevance scoring.: "Build a bi-encoder branch that encodes spectra and compound reference embeddings independently, using fusion pooling to combine CNN and Transformer outputs. Build a cross-encoder branch that jointly"
- [other] Combine bi-encoder and cross-encoder logits using the weighted loss function (balancing both encoder contributions) and train end-to-end with backpropagation.: "Combine bi-encoder and cross-encoder logits using the weighted loss function (balancing both encoder contributions) and train end-to-end with backpropagation."
- [other] Validate on held-out test set, compute compound identification accuracy and ranking metrics, and save trained model checkpoint and performance report.: "Validate on held-out test set, compute compound identification accuracy and ranking metrics, and save trained model checkpoint and performance report."
- [readme] Python 3.13.2 and Pytorch (version 2.7.0+cu118): "Python 3.13.2 and Pytorch (version 2.7.0+cu118)"
