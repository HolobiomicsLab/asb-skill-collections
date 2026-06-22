---
name: mass-spectral-data-augmentation
description: Use when when you have limited real GC-MS overlapped peak data but need thousands of labeled examples to train a deep learning model for mass spectral deconvolution.
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

# mass-spectral-data-augmentation

## Summary

Generate synthetic overlapped GC-MS peak datasets through controlled augmentation to create large-scale training corpora for machine learning models. This skill transforms limited real mass spectra into thousands of realistic simulated overlapped peaks suitable for training Transformer models on spectral deconvolution tasks.

## When to use

When you have limited real GC-MS overlapped peak data but need thousands of labeled examples to train a deep learning model for mass spectral deconvolution. Use this skill when the bottleneck is training data size rather than model architecture, and when you can parameterize the overlapped peak generation process (component count, intensity ratios, spectral similarity).

## When NOT to use

- Input is already a large, well-characterized real GC-MS overlapped peak dataset (>10,000 samples); augmentation may introduce artificial patterns that conflict with real spectral variability.
- Application requires the model to generalize to completely different sample matrices or instrument types not represented in the augmentation parameters; synthetic data may not capture sufficient domain variance.
- Augmentation parameters are unknown or cannot be reliably estimated from domain knowledge; incorrect parameterization will produce unrealistic training data that degrades model performance.

## Inputs

- Data augmentation parameters object (peak count range, component diversity, overlap intensity distributions)
- Optional: reference pure mass spectra library or chemical database to seed augmentation

## Outputs

- TRAIN set: 80,000 augmented simulated overlapped peak samples (or proportional to 8:1:1 split)
- VALID set: 10,000 augmented simulated overlapped peak samples
- TEST set: 10,000 augmented simulated overlapped peak samples
- tgt_vocab: target vocabulary (encoding of all possible m/z values and intensity levels)

## How to apply

Use the GCMSFormer `gen_datasets()` function with data augmentation parameters to generate synthetic overlapped peaks. The function creates realistic simulated peaks by combining pure mass spectra at varying intensity levels and retention times. Generate a target vocabulary (tgt_vocab) from the augmented dataset to represent all possible mass-to-charge ratios and intensities. Partition the generated dataset into train/validation/test sets (commonly 8:1:1 ratio) before model training. The augmentation parameters control the number of component peaks per sample, intensity distributions, and spectral overlap characteristics—tune these to match your application domain (e.g., essential oil analysis, pharmaceutical compounds). Validation that augmentation is effective comes from downstream model BLEU score on held-out test peaks.

## Related tools

- **GCMSFormer** (Host framework containing gen_datasets() function for mass spectral data augmentation and model training pipeline) — https://github.com/zxguocsu/GCMSFormer
- **PyTorch** (Underlying deep learning framework for model training and tensor operations on augmented datasets) — https://pytorch.org/
- **conda** (Environment manager to install and isolate GCMSFormer and PyTorch dependencies) — https://conda.io/docs/user-guide/install/download.html

## Examples

```
TRAIN, VALID, TEST, tgt_vocab = gen_datasets(para)
```

## Evaluation signals

- Augmented dataset size matches specification: 100,000 total samples with 8:1:1 train/valid/test partition (80k/10k/10k)
- tgt_vocab is non-empty and contains encodings for all m/z values and intensity levels present in augmented peaks
- Downstream GCMSFormer model trained on augmented data achieves BLEU ≥ 0.99 on held-out test set (benchmark: 0.9988)
- Augmented peak samples are valid and parseable: no NaN/inf values, m/z ranges are physically realistic (e.g., 50–500 m/z for small molecules), intensity sums per sample are non-zero
- Augmented data distribution matches domain assumptions: overlapped peaks contain 2–5 components with realistic intensity ratios, no degenerate single-component samples

## Limitations

- Augmented data is synthetic and may not capture all artifacts of real GC-MS instruments (baseline drift, noise profiles, column bleed, detector saturation).
- Augmentation quality depends critically on the choice of parameters (component count, overlap intensity distributions); poorly chosen parameters will produce unrealistic training data.
- Model trained exclusively on augmented data may overfit to synthetic patterns and exhibit poor generalization to real overlapped peaks from different sample matrices or instruments not covered by the augmentation.
- No explicit guidance provided in README for selecting or tuning augmentation parameters; users must rely on domain knowledge or empirical validation.

## Evidence

- [readme] The overlapped peak dataset for training, validating and testing the GCMSFormer model is obtained using the gen_datasets functions.: "The overlapped peak dataset for training, validating and testing the GCMSFormer model is obtained using the [gen_datasets](https://github.com/zxguocsu/GCMSFormer/blob/master/GCMSFormer/da.py#L240)"
- [readme] The GCMSFormer model was trained, validated, and tested with 100,000 augmented simulated overlapped peaks in a ratio of 8:1:1, and its bilingual evaluation understudy (BLEU) on the test set was 0.9988.: "The GCMSFormer model was trained, validated, and tested with 100,000 augmented simulated overlapped peaks in a ratio of 8:1:1, and its bilingual evaluation understudy (BLEU) on the test set was"
- [intro] We proposed the GCMSFormer for resolving the overlapped peaks in complex GC-MS data based on a Transformer model.: "We proposed the GCMSFormer for resolving the overlapped peaks in complex GC-MS data based on a Transformer model."
- [readme] TRAIN, VALID, TEST, tgt_vacob = gen_datasets(para): "TRAIN, VALID, TEST, tgt_vacob = gen_datasets(para)"
