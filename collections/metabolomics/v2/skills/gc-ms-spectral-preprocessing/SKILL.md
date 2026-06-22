---
name: gc-ms-spectral-preprocessing
description: Use when you have raw GC-MS data files containing overlapped peaks (unresolved components with coeluting retention times) and need to predict pure mass spectra for each individual component using a Transformer-based model.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
  tools:
  - PyTorch
  - Python 3
  - conda
  - GCMSFormer
derived_from:
- doi: 10.1021/acs.analchem.3c05772
  title: GCMSFormer
evidence_spans:
- '[pytorch](https://pytorch.org/)'
- '[python3](https://www.python.org/)'
- We recommend to use [conda](https://conda.io/docs/user-guide/install/download.html)
- We recommend to use [conda](https://conda.io/docs/user-guide/install/download.html).
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_gcmsformer_cq
    doi: 10.1021/acs.analchem.3c05772
    title: GCMSFormer
  dedup_kept_from: coll_gcmsformer_cq
schema_version: 0.2.0
---

# GC-MS spectral preprocessing

## Summary

Preprocessing of raw GC-MS overlapped peak data into tensor format compatible with Transformer-based architectures for mass spectral deconvolution. This step prepares raw mass spectral intensities and retention time regions for input to neural network models like GCMSFormer.

## When to use

You have raw GC-MS data files containing overlapped peaks (unresolved components with coeluting retention times) and need to predict pure mass spectra for each individual component using a Transformer-based model. Apply this skill when raw mass spectral intensities and retention time region data must be converted into the specific tensor format required by GCMSFormer or similar deep learning architectures.

## When NOT to use

- Input is already resolved into pure component spectra (preprocessing is redundant)
- Data lacks retention time information or contains only isolated, non-overlapped peaks
- Input data format is incompatible with Transformer tensor requirements and cannot be reliably reshaped

## Inputs

- Raw GC-MS data file (e.g., NetCDF or proprietary GC-MS format)
- Mass spectral intensities (m/z and intensity pairs)
- Retention time region boundaries defining overlapped peak window
- Model architecture configuration (tensor shape specifications)

## Outputs

- Preprocessed tensor in GCMSFormer-compatible format
- Normalized mass spectral intensity matrix ready for neural network input
- Metadata mapping (original indices, retention time annotations)

## How to apply

Load the overlapped peak input data containing raw mass spectral intensities (m/z values and their corresponding intensity values) along with the retention time region boundaries. Transform these raw inputs into a tensor format compatible with the GCMSFormer Transformer architecture, ensuring proper dimensionality and normalization. The preprocessed tensor is then fed into the GCMSFormer model, which uses orthogonal projection resolution (OPR) to predict the pure mass spectra matrix S (dimensions: number of components × m/z values). Validate that the output tensor matches the expected shape and that intensity values are normalized appropriately for the model's input specifications.

## Related tools

- **PyTorch** (Tensor creation, normalization, and data structure management for Transformer input) — https://pytorch.org/
- **Python 3** (Language runtime for data loading and preprocessing scripts) — https://www.python.org/
- **conda** (Environment and dependency management for reproducible preprocessing pipeline) — https://conda.io/docs/user-guide/install/download.html
- **GCMSFormer** (Downstream Transformer model that consumes preprocessed tensors to predict pure mass spectra) — https://github.com/zxguocsu/GCMSFormer

## Examples

```
```python
from GCMSFormer.Resolution import Resolution
from GCMSFormer.GCMSformer import train_model
import torch

# After preprocessing input data into tensor format:
Resolution(path='./data/', filename='essential_oil.cdf', model=model, tgt_vacob=tgt_vacob, device='cuda')
```
```

## Evaluation signals

- Preprocessed tensor shape matches expected GCMSFormer input dimensions (verified against model.input_shape or environment.yml specifications)
- Mass spectral intensity values are normalized and within expected numerical range (e.g., [0, 1] or z-score normalized)
- No NaN or infinity values present in preprocessed tensor
- Retention time metadata is correctly preserved and maps back to original data indices
- Model accepts preprocessed tensor without shape/dtype errors during GCMSFormer.predict() call

## Limitations

- Preprocessing assumes overlapped peaks fall within a single contiguous retention time window; multiple disjoint peak regions require separate preprocessing passes
- GCMSFormer model was trained on 100,000 simulated overlapped peaks; real GC-MS data with significantly different peak distributions or noise characteristics may require retraining or augmentation-aware preprocessing
- Tensor format and normalization scheme are tightly coupled to GCMSFormer architecture; preprocessing code must be updated if model input specifications change

## Evidence

- [other] Load the overlapped peak input data (raw mass spectral intensities and retention time region). Preprocess the input into the required tensor format compatible with the GCMSFormer Transformer architecture.: "Load the overlapped peak input data (raw mass spectral intensities and retention time region). Preprocess the input into the required tensor format compatible with the GCMSFormer Transformer"
- [readme] GCMSFormer can predict the pure mass spectra of all components in overlapped peaks (mass spectral matrix S), and then use the least squares method to find the concentration distribution matrix C: "GCMSFormer can predict the pure mass spectra of all components in overlapped peaks (mass spectral matrix S), and then use the least squares method to find the concentration distribution matrix C"
- [readme] The GCMSFormer model was trained, validated, and tested with 100,000 augmented simulated overlapped peaks in a ratio of 8:1:1: "The GCMSFormer model was trained, validated, and tested with 100,000 augmented simulated overlapped peaks in a ratio of 8:1:1"
- [readme] We recommend to use conda. - python3 - pytorch: "We recommend to use conda. - python3 - pytorch"
- [other] Extract and validate the predicted mass spectral matrix S (dimensions: number of components × m/z values).: "Extract and validate the predicted mass spectral matrix S (dimensions: number of components × m/z values)."
