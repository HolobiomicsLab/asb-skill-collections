---
name: orthogonal-projection-deconvolution
description: Use when you have overlapped peak regions in GC-MS chromatography data (multiple components eluting within the same retention time window) and need to recover the pure mass spectra of each component and their relative concentrations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3520
  tools:
  - PyTorch
  - Python 3
  - conda
  - GCMSFormer
  techniques:
  - GC-MS
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c05772
  all_source_dois:
  - 10.1021/acs.analchem.3c05772
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# orthogonal-projection-deconvolution

## Summary

Resolve overlapped peaks in GC-MS data by using orthogonal projection resolution (OPR) in conjunction with a Transformer model (GCMSFormer) to predict pure mass spectra matrices, then apply least squares fitting to extract component concentration distributions. This skill enables automated deconvolution of complex, co-eluting chromatographic signals into individual component spectra.

## When to use

Apply this skill when you have overlapped peak regions in GC-MS chromatography data (multiple components eluting within the same retention time window) and need to recover the pure mass spectra of each component and their relative concentrations. Typical trigger: raw mass spectral intensities and retention time regions showing multiple unresolved peaks in a single region.

## When NOT to use

- Input data already consists of fully resolved, baseline-separated peaks — OPR is designed for overlapped signals, not single-peak deconvolution.
- Mass spectrometry data is from a non-chromatographic source or lacks temporal (retention time) dimension — OPR/GCMSFormer targets GC-MS specifically.
- The number of overlapped components exceeds the training distribution of the GCMSFormer model (trained on up to ~8–10 typical component mixtures) — model may not generalize reliably.

## Inputs

- Overlapped peak region: raw mass spectral intensities (2D array: m/z × time points)
- Retention time region boundaries (start, end)
- Pre-trained GCMSFormer model checkpoint
- Target vocabulary (tgt_vocab) library

## Outputs

- Pure mass spectra matrix S (components × m/z values)
- Concentration distribution matrix C (components × time points)
- Resolved mass spectra in CSV or HDF5 format

## How to apply

Load overlapped peak data (raw mass spectral intensities and retention time region) and preprocess into tensor format compatible with the GCMSFormer Transformer architecture. Apply the pre-trained GCMSFormer model to predict the pure mass spectra matrix S (dimensions: number of components × m/z values) for all component peaks within the overlapped region using orthogonal projection resolution. The model leverages OPR to isolate each component's spectral signature from the convolved mixture. Extract and validate the predicted mass spectral matrix S, then apply the least squares method to solve for the concentration distribution matrix C. Save both resolved matrices in structured format (CSV or HDF5) for downstream analysis.

## Related tools

- **GCMSFormer** (Transformer-based neural network model that predicts pure mass spectra matrices S from overlapped peaks using orthogonal projection resolution) — https://github.com/zxguocsu/GCMSFormer
- **PyTorch** (Deep learning framework for training, validating, and executing the GCMSFormer model) — https://pytorch.org/
- **Python 3** (Programming language for orchestrating data preprocessing, model inference, and matrix I/O) — https://www.python.org/
- **conda** (Environment manager for reproducible package installation and dependency resolution) — https://conda.io/docs/user-guide/install/download.html

## Examples

```
from GCMSFormer.Resolution import Resolution; Resolution(path='./data', filename='sample.ms', model=trained_model, tgt_vacob=vocab, device='cuda')
```

## Evaluation signals

- Predicted mass spectra matrix S has correct dimensions (number of components × m/z values) and all intensities are non-negative.
- Concentration matrix C sums across all components to approximate the total overlapped peak intensity at each time point (least squares reconstruction error < threshold).
- BLEU score on resolved spectra vs. held-out reference spectra should approach the reported test BLEU of 0.9988, indicating high spectral fidelity.
- Individual resolved mass spectra match known reference spectra (if available) with cosine similarity > 0.95.
- Chromatographic retention times of resolved components fall within the input retention time window and do not exceed model training range (~100 m/z, ~20 time points per peak).

## Limitations

- Model was trained exclusively on simulated, augmented overlapped peaks (100,000 examples, 8:1:1 train/valid/test split); real environmental or biological samples may exhibit spectral noise, background interference, or isotope patterns not captured in training distribution.
- GCMSFormer predictions depend on the quality of the pre-trained checkpoint; model performance degrades if the input overlapped region deviates significantly from training conditions (e.g., very noisy, extreme m/z ranges, or >10 co-eluting components).
- Least squares fitting for concentration matrix C assumes linear mixing and homogeneous peak shapes; non-linear peak distortions or severe tailing may reduce accuracy.
- Orthogonal projection resolution is sensitive to the choice of initial spectral estimates and may fail if components have highly similar mass spectra (low orthogonality).

## Evidence

- [readme] With the aid of the orthogonal projection resolution method (OPR), GCMSFormer can predict the pure mass spectra of all components in overlapped peaks (mass spectral matrix S), and then use the least squares method to find the concentration distribution matrix C.: "With the aid of the orthogonal projection resolution method (OPR), GCMSFormer can predict the pure mass spectra of all components in overlapped peaks (mass spectral matrix S), and then use the least"
- [readme] We proposed the GCMSFormer for resolving the overlapped peaks in complex GC-MS data based on a Transformer model.: "We proposed the GCMSFormer for resolving the overlapped peaks in complex GC-MS data based on a Transformer model."
- [readme] The GCMSFormer model was trained, validated, and tested with 100,000 augmented simulated overlapped peaks in a ratio of 8:1:1: "The GCMSFormer model was trained, validated, and tested with 100,000 augmented simulated overlapped peaks in a ratio of 8:1:1"
- [readme] its bilingual evaluation understudy (BLEU) on the test set was 0.9988: "its bilingual evaluation understudy (BLEU) on the test set was 0.9988"
- [other] Load the overlapped peak input data (raw mass spectral intensities and retention time region). Preprocess the input into the required tensor format compatible with the GCMSFormer Transformer architecture. Apply the GCMSFormer model to predict the pure mass spectra matrix S for all component peaks within the overlapped region using orthogonal projection resolution.: "Load the overlapped peak input data (raw mass spectral intensities and retention time region). Preprocess the input into the required tensor format compatible with the GCMSFormer Transformer"
