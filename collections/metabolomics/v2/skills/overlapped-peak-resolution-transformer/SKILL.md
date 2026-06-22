---
name: overlapped-peak-resolution-transformer
description: Use when when GC-MS chromatograms contain overlapped or co-eluting peaks in a retention time region and you need to recover the individual pure mass spectra and relative abundances of each component without manual peak picking or external standards.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
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

# overlapped-peak-resolution-transformer

## Summary

Resolve overlapped peaks in complex GC-MS data by predicting pure mass spectra of all components using a Transformer model (GCMSFormer) in conjunction with orthogonal projection resolution (OPR) and least squares fitting. This skill deconvolutes mass spectral matrix S and concentration distribution matrix C from raw overlapped peak regions.

## When to use

When GC-MS chromatograms contain overlapped or co-eluting peaks in a retention time region and you need to recover the individual pure mass spectra and relative abundances of each component without manual peak picking or external standards.

## When NOT to use

- Input peaks are already baseline-resolved and do not exhibit significant co-elution — use simpler peak detection methods instead.
- GC-MS data format is not compatible with model input preprocessing (e.g., missing m/z or intensity arrays).
- The number of overlapped components exceeds the training distribution (model trained on 100,000 augmented overlapped peaks with specific overlap patterns and component counts).

## Inputs

- overlapped peak region (raw mass spectral intensities and retention time boundaries)
- GC-MS data file (e.g., NetCDF or vendor format)
- pre-trained GCMSFormer model checkpoint
- target vocabulary (tgt_vocab) from model training

## Outputs

- pure mass spectral matrix S (components × m/z values)
- concentration distribution matrix C (components × retention time or sample × components)
- resolved mass spectra in CSV or HDF5 format

## How to apply

Load overlapped peak input data (raw mass spectral intensities and retention time region), preprocess into tensor format compatible with the GCMSFormer Transformer architecture, apply the pre-trained GCMSFormer model to predict the pure mass spectra matrix S (dimensions: number of components × m/z values) using orthogonal projection resolution, then apply the least squares method to solve for the concentration distribution matrix C that best explains the observed overlapped intensities. Extract and validate the resolved mass spectral matrix S by checking matrix dimensions, intensity ranges, and consistency with known mass spectral libraries before saving in CSV or HDF5 format.

## Related tools

- **GCMSFormer** (Transformer-based neural network model that predicts pure mass spectra from overlapped peak regions using orthogonal projection resolution) — https://github.com/zxguocsu/GCMSFormer
- **PyTorch** (Deep learning framework for loading, running, and deploying the GCMSFormer model) — https://pytorch.org/
- **Python 3** (Programming language for data preprocessing, model inference, and post-processing of resolved spectra) — https://www.python.org/
- **conda** (Environment manager for reproducible installation of all required packages and dependencies) — https://conda.io/docs/user-guide/install/download.html

## Examples

```
from GCMSFormer.Resolution import Resolution
Resolution(path='./gc_ms_data/', filename='essential_oil.cdf', model=model, tgt_vocab=tgt_vocab, device='cuda')
```

## Evaluation signals

- Predicted mass spectral matrix S has correct dimensions (number_of_components × number_of_mz_values) and all intensity values are non-negative.
- BLEU score on held-out test data is ≥ 0.998 (article reports 0.9988), indicating high fidelity of predicted pure mass spectra.
- Reconstructed overlapped peak profile (S × C^T) closely matches the observed raw mass spectral intensities across the retention time region (e.g., root mean square error below noise floor).
- Resolved mass spectra can be matched to known standards or library entries with cosine similarity or spectral dot product scores above a threshold (e.g., > 0.7).
- Sum of concentration matrix C across all components equals 1.0 (or close, within numerical precision), confirming proper normalization and mass balance.

## Limitations

- Model was trained on 100,000 augmented simulated overlapped peaks in 8:1:1 train/validation/test ratio; performance on real, untrained peak overlap patterns or edge cases (e.g., >5 co-eluting components, extreme intensity ratios) is not reported.
- The method assumes components have known or learnable mass spectral patterns; completely novel or highly unusual mass spectra may not be resolved accurately.
- Least squares solving of concentration matrix C can be ill-conditioned if mass spectra are highly similar or m/z resolution is insufficient to distinguish components.
- No explicit handling of background noise, baseline variation, or non-linear detector response is described in the workflow.

## Evidence

- [readme] With the aid of the orthogonal projection resolution method (OPR), GCMSFormer can predict the pure mass spectra of all components in overlapped peaks (mass spectral matrix S), and then use the least squares method to find the concentration distribution matrix C.: "With the aid of the orthogonal projection resolution method (OPR), GCMSFormer can predict the pure mass spectra of all components in overlapped peaks (mass spectral matrix S), and then use the least"
- [readme] The GCMSFormer model was trained, validated, and tested with 100,000 augmented simulated overlapped peaks in a ratio of 8:1:1, and its bilingual evaluation understudy (BLEU) on the test set was 0.9988.: "The GCMSFormer model was trained, validated, and tested with 100,000 augmented simulated overlapped peaks in a ratio of 8:1:1, and its bilingual evaluation understudy (BLEU) on the test set was 0.9988"
- [other] Preprocess the input into the required tensor format compatible with the GCMSFormer Transformer architecture.: "Preprocess the input into the required tensor format compatible with the GCMSFormer Transformer architecture"
- [other] Extract and validate the predicted mass spectral matrix S (dimensions: number of components × m/z values).: "Extract and validate the predicted mass spectral matrix S (dimensions: number of components × m/z values)"
- [other] Save the resolved mass spectra matrix S in a structured format (CSV or HDF5).: "Save the resolved mass spectra matrix S in a structured format (CSV or HDF5)"
- [readme] Automatic Resolution of GC-MS data files by using the [Resolution](https://github.com/zxguocsu/GCMSFormer/blob/master/GCMSFormer/Resolution.py#L51) function.: "Automatic Resolution of GC-MS data files by using the [Resolution] function"
