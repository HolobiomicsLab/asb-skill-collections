---
name: nmr-spectral-feature-extraction
description: Use when when you have raw or preprocessed 1H NMR spectral tensors from flavor or chemical mixtures and need to generate high-level feature representations that capture both fine-grained local patterns (e.g., peak multiplet structure, coupling constants) and global spectral context (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3382
  - http://edamontology.org/topic_3520
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# nmr-spectral-feature-extraction

## Summary

Extract local and global features from 1H NMR spectra using a hybrid CNN-Transformer architecture that combines convolutional layers for short-range spectral patterns with multi-head Transformer encoders for long-range dependencies. This skill enables accurate feature representation of NMR data for downstream compound identification tasks in mixture analysis.

## When to use

When you have raw or preprocessed 1H NMR spectral tensors from flavor or chemical mixtures and need to generate high-level feature representations that capture both fine-grained local patterns (e.g., peak multiplet structure, coupling constants) and global spectral context (e.g., overall signature changes across the spectrum) for compound matching or classification.

## When NOT to use

- Input spectra are already dimensionally reduced or summarized into feature vectors (e.g., peak lists, integrated regions); the hybrid encoder assumes raw or minimally preprocessed spectral data.
- Your downstream task does not require modeling long-range spectral dependencies (e.g., single-peak detection or trivial threshold classification); CNN-only or simpler methods may suffice.
- Computational resources are severely constrained; multi-head Transformer components add significant memory and latency overhead compared to CNN-only baselines.

## Inputs

- 1H NMR spectral tensor (multi-channel, e.g., shape [batch_size, channels, spectral_length])
- Preprocessed or raw NMR spectral data in tensor format

## Outputs

- Encoded spectral feature representation (tensor) compatible with bi-encoder and cross-encoder
- Unified hybrid encoder module with fused CNN-Transformer outputs

## How to apply

Load 1H NMR spectra as multi-dimensional tensors compatible with PyTorch. Pass spectral data through a CNN feature extractor using convolutional layers to identify local spectral patterns and peak characteristics. Feed the CNN output to a multi-head Transformer encoder block to model global dependencies and long-range spectral relationships. Fuse CNN and Transformer outputs at designated feature fusion points to create unified encoded representations. Verify output tensors are compatible with downstream bi-encoder or cross-encoder heads for compound identification. The hybrid design rationale is that CNNs alone miss long-range correlations while Transformers alone may over-smooth fine spectral detail; the fusion captures both simultaneously.

## Related tools

- **PyTorch** (Deep learning framework for implementing CNN and Transformer encoder layers and managing tensor operations) — https://pytorch.org
- **Python** (Programming language for scripting the hybrid architecture and data pipeline)
- **Anaconda** (Environment manager for installing Python 3.13.2 and PyTorch dependencies) — https://www.anaconda.com/
- **FlavorFormer** (Reference implementation of the complete hybrid CNN-Transformer architecture with bi-encoder and cross-encoder heads) — https://github.com/yfWang01/FlavorFormer

## Examples

```
conda activate FlavorFormer && python -c "import torch; from model import HybridCNNTransformer; encoder = HybridCNNTransformer(); spectra = torch.randn(8, 1, 256); features = encoder(spectra); print(features.shape)"
```

## Evaluation signals

- Output tensor shape and dtype match expected downstream encoder input (verify via model._modules or forward hook inspection)
- CNN sub-module processes local spectral patterns correctly: verify receptive field covers expected peak widths and verify intermediate activations highlight multiplet structure
- Transformer sub-module produces non-zero attention weights across spectral sequence positions (inspect attention matrices from multi-head blocks); all-zero or single-token attention indicates failure
- Fused output representation differs meaningfully from CNN-only or Transformer-only baselines (measure via cosine similarity or reconstruction error on held-out spectra); if outputs collapse to either component alone, fusion is broken
- End-to-end compound identification accuracy on validation mixture spectra meets or exceeds baseline; accuracy drop >5% compared to published FlavorFormer results indicates incorrect architecture instantiation

## Limitations

- Identifying components in mixtures using NMR spectra remains inherently challenging due to peak overlap and concentration variability; the hybrid architecture mitigates but does not eliminate this.
- Performance depends critically on proper input tensor normalization and spectral preprocessing (e.g., baseline correction, phasing); raw or poorly phased spectra degrade both CNN and Transformer feature quality.
- Transformer components require sufficient spectral sequence length to benefit from attention; very short spectra or heavily binned/downsampled inputs reduce attention modeling efficacy.
- Computational cost scales with multi-head attention dimension and spectral length; real-time prediction on resource-constrained devices may require model compression or quantization.

## Evidence

- [intro] hybrid CNN and Transformer architecture that captures both local features and global dependencies from 1H NMR spectra: "FlavorFormer uses a hybrid CNN and Transformer architecture that captures both local features and global dependencies from 1H NMR spectra"
- [other] CNN feature extractor using convolutional layers to capture local patterns; multi-head Transformer encoder to model global dependencies: "1. Define a CNN feature extractor using convolutional layers to capture local patterns in 1H NMR spectra. 2. Implement a multi-head Transformer encoder block to model global dependencies across the"
- [other] Hybrid CNN and Transformer architecture integrated with fusion points and downstream encoder compatibility: "3. Integrate the CNN and Transformer components into a unified hybrid encoder module with appropriate feature fusion points. 4. Verify the module accepts 1H NMR spectral tensors and outputs encoded"
- [readme] Python 3.13.2 and PyTorch 2.7.0+cu118 as implementation tools: "Python 3.13.2 and Pytorch (version 2.7.0+cu118)"
- [intro] Hybrid CNN and Transformer with bi-encoder and cross-encoder for compound identification: "incorporating a hybrid CNN and Transformer architecture to capture both local features and global dependencies from 1H NMR spectra"
