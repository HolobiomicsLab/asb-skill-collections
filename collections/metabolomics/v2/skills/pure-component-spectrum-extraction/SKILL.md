---
name: pure-component-spectrum-extraction
description: Use when analyzing GC-MS data containing overlapped peaks where two or more components co-elute within the same retention time window, making direct spectral assignment impossible.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
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

# pure-component-spectrum-extraction

## Summary

Extract pure mass spectra of individual components from overlapped GC-MS peaks using the GCMSFormer Transformer model combined with orthogonal projection resolution (OPR). This skill resolves co-eluting compounds in complex chromatographic data by predicting a mass spectral matrix S from which concentration distributions can be derived.

## When to use

Apply this skill when analyzing GC-MS data containing overlapped peaks where two or more components co-elute within the same retention time window, making direct spectral assignment impossible. Use it when you need to recover pure mass spectra for each component and their relative concentration profiles from a single overlapped peak region.

## When NOT to use

- Input contains fully resolved, non-overlapping peaks—use traditional spectral library matching instead
- Mass spectrometry data is from instruments other than GC-MS (e.g., LC-MS, direct infusion MS) without prior validation of model transferability
- Overlapped region contains >10 co-eluting components, as model was trained and validated on complex but finite peak density distributions

## Inputs

- Overlapped GC-MS peak region (raw mass spectral intensities with m/z and intensity values)
- Retention time window defining the overlapped peak boundaries
- Trained GCMSFormer model checkpoint
- Target vocabulary (tgt_vocab) from model training

## Outputs

- Pure mass spectra matrix S (dimensions: number of components × m/z values)
- Predicted pure mass spectrum for each component in the overlapped region
- Structured file (CSV or HDF5) containing resolved spectral matrix

## How to apply

Load raw overlapped peak data (mass spectral intensities and retention time region) and preprocess into PyTorch-compatible tensor format matching the GCMSFormer Transformer architecture. Feed the preprocessed tensor through the trained GCMSFormer model, which applies orthogonal projection resolution to predict the pure mass spectra matrix S (dimensions: number of components × m/z values). Extract and validate the predicted spectral matrix by verifying dimensionality and intensity ranges, then save in structured format (CSV or HDF5). The model has been trained on 100,000 augmented simulated overlapped peaks (8:1:1 train/valid/test split) and achieves a BLEU score of 0.9988, indicating high accuracy in spectral recovery.

## Related tools

- **GCMSFormer** (Transformer neural network model that predicts pure mass spectra matrix S from overlapped GC-MS peaks using orthogonal projection resolution) — https://github.com/zxguocsu/GCMSFormer
- **PyTorch** (Deep learning framework for executing the GCMSFormer model inference) — https://pytorch.org/
- **Python 3** (Programming language for data loading, preprocessing, and postprocessing) — https://www.python.org/
- **conda** (Dependency and environment manager for installing PyTorch and other packages) — https://conda.io/docs/user-guide/install/download.html

## Examples

```
from GCMSFormer.Resolution import Resolution; Resolution(path='./gcms_data/', filename='overlapped_sample.raw', model=trained_model, tgt_vacob=tgt_vocab, device='cuda')
```

## Evaluation signals

- Output mass spectra matrix S has correct dimensions: (number_of_components, number_of_mz_values)
- Predicted mass spectra intensity values fall within physically plausible range (0–100% relative intensity) and sum appropriately per component
- Resolved spectra can be matched to known reference spectra with similarity score (e.g., cosine or BLEU) above the model's training threshold (~0.9988)
- Reconstructed concentration matrix C (via least squares from matrix S) reproduces the original overlapped peak profile when reconvolved with retention time Gaussian
- Predicted pure spectra show expected fragmentations and base peaks consistent with authentic mass spectral library entries for identified compounds

## Limitations

- Model trained exclusively on simulated overlapped peaks; real-world GC-MS data may contain noise, baseline shifts, or peak tailing not represented in training set
- Accuracy degrades when the number of co-eluting components exceeds the complexity range seen during training (100,000 augmented peaks)
- Assumes components in overlapped region follow Gaussian peak shapes; skewed or multi-modal elution profiles may not be resolved correctly
- Requires a pre-trained GCMSFormer checkpoint and target vocabulary; retraining may be necessary for novel instrument types or MS ionization methods

## Evidence

- [readme] GCMSFormer can predict the pure mass spectra of all components in overlapped peaks (mass spectral matrix S), and then use the least squares method to find the concentration distribution matrix C: "GCMSFormer can predict the pure mass spectra of all components in overlapped peaks (mass spectral matrix S), and then use the least squares method to find the concentration distribution matrix C"
- [readme] With the aid of the orthogonal projection resolution method (OPR), GCMSFormer can predict the pure mass spectra: "With the aid of the orthogonal projection resolution method (OPR), GCMSFormer can predict the pure mass spectra"
- [readme] The GCMSFormer model was trained, validated, and tested with 100,000 augmented simulated overlapped peaks in a ratio of 8:1:1, and its bilingual evaluation understudy (BLEU) on the test set was 0.9988: "The GCMSFormer model was trained, validated, and tested with 100,000 augmented simulated overlapped peaks in a ratio of 8:1:1, and its bilingual evaluation understudy (BLEU) on the test set was 0.9988"
- [other] 1. Load the overlapped peak input data (raw mass spectral intensities and retention time region). 2. Preprocess the input into the required tensor format compatible with the GCMSFormer Transformer architecture. 3. Apply the GCMSFormer model to predict the pure mass spectra matrix S for all component peaks within the overlapped region using orthogonal projection resolution. 4. Extract and validate the predicted mass spectral matrix S (dimensions: number of components × m/z values). 5. Save the resolved mass spectra matrix S in a structured format (CSV or HDF5).: "Load the overlapped peak input data (raw mass spectral intensities and retention time region). Preprocess the input into the required tensor format compatible with the GCMSFormer Transformer"
- [readme] We proposed the GCMSFormer for resolving the overlapped peaks in complex GC-MS data based on a Transformer model: "We proposed the GCMSFormer for resolving the overlapped peaks in complex GC-MS data based on a Transformer model"
