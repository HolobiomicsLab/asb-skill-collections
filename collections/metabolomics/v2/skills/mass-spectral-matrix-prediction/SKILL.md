---
name: mass-spectral-matrix-prediction
description: Use when you have raw GC-MS data with overlapped peaks in a specific
  retention time region and need to resolve the individual pure mass spectra of all
  components present in that region.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3628
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - PyTorch
  - Python 3
  - conda
  - GCMSFormer
  techniques:
  - GC-MS
  license_tier: open
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectral-matrix-prediction

## Summary

Predict pure mass spectra of all components in overlapped GC-MS peaks using the GCMSFormer Transformer model with orthogonal projection resolution. This skill decomposes a single overlapped mass spectral region into a matrix S of individual component spectra, enabling automated resolution of complex chromatographic mixtures.

## When to use

Apply this skill when you have raw GC-MS data with overlapped peaks in a specific retention time region and need to resolve the individual pure mass spectra of all components present in that region. Use it when standard chromatographic separation is insufficient and you require automated deconvolution of co-eluting compounds.

## When NOT to use

- Input contains baseline-resolved peaks — standard library matching or integration is more appropriate
- GC-MS data quality is poor (low signal-to-noise, fragmented mass spectra) — model was trained on clean, simulated data and may fail on degraded experimental data
- Overlapped region involves >5 co-eluting components — model was trained on overlapped pairs/small mixtures; performance on highly complex overlaps is undocumented

## Inputs

- Raw mass spectral intensities (overlapped peak region)
- Retention time region boundaries (start and end RT)
- GC-MS data file (NetCDF or vendor format)
- Pre-trained GCMSFormer model checkpoint
- Target vocabulary library (tgt_vocab)

## Outputs

- Mass spectral matrix S (components × m/z intensities)
- Number of resolved components (inferred from S)
- Predicted pure mass spectra for each component (CSV or HDF5)
- Optional: concentration distribution matrix C (from least squares fitting)

## How to apply

Load the overlapped peak data (raw mass spectral intensities and retention time boundaries) and preprocess it into the tensor format required by GCMSFormer's Transformer architecture. Apply the pre-trained GCMSFormer model to predict the mass spectral matrix S (dimensions: number of components × m/z values) for all components within the overlapped region using orthogonal projection resolution. Validate the predicted matrix S for chemical plausibility (non-negative intensities, known fragmentation patterns) and save in structured format (CSV or HDF5). The model was trained on 100,000 augmented simulated overlapped peaks and achieved BLEU score of 0.9988, providing high confidence in predictions.

## Related tools

- **GCMSFormer** (Transformer-based neural network model that predicts pure mass spectra from overlapped peaks using orthogonal projection resolution) — https://github.com/zxguocsu/GCMSFormer
- **PyTorch** (Deep learning framework for loading and executing the pre-trained GCMSFormer model) — https://pytorch.org/
- **Python 3** (Runtime environment for data preprocessing, model inference, and post-processing) — https://www.python.org/
- **conda** (Environment manager for installing dependencies and managing PyTorch/Python versions) — https://conda.io/docs/user-guide/install/download.html

## Examples

```
from GCMSFormer.Resolution import Resolution
Resolution(path='/data/gcms/', filename='sample.cdf', model=model, tgt_vacob=tgt_vocab, device='cuda')
```

## Evaluation signals

- Predicted mass spectral matrix S has expected dimensions (number of components × m/z values) and contains non-negative intensities only
- Each predicted pure mass spectrum matches known fragmentation patterns for identified compounds (compare to NIST or in-house library)
- Reconstruction error: least squares fit of predicted S and concentration matrix C to original overlapped spectrum is minimized (residual intensity < 5% of max peak)
- BLEU score or cosine similarity between predicted and reference (if available) mass spectra remains ≥ 0.95
- Number of resolved components is consistent with prior knowledge of the sample (e.g., GC peak count, expected mixture size)

## Limitations

- Model trained only on simulated overlapped peaks in 8:1:1 train/validation/test ratio; generalization to real experimental data with instrumental noise, column bleed, or unusual fragmentation may be limited
- Orthogonal projection resolution assumes linear mixing of mass spectra; non-linear ion suppression or adduct formation will violate this assumption
- Performance is undocumented for overlaps involving >2–3 components or components with highly similar mass spectra
- Requires pre-trained model checkpoint and vocabulary library; retraining on domain-specific data is necessary if resolving novel compound classes

## Evidence

- [readme] GCMSFormer can predict the pure mass spectra of all components in overlapped peaks (mass spectral matrix S), and then use the least squares method to find the concentration distribution matrix C: "GCMSFormer can predict the pure mass spectra of all components in overlapped peaks (mass spectral matrix S), and then use the least squares method to find the concentration distribution matrix C"
- [readme] With the aid of the orthogonal projection resolution method (OPR), GCMSFormer can predict the pure mass spectra of all components in overlapped peaks: "With the aid of the orthogonal projection resolution method (OPR), GCMSFormer can predict the pure mass spectra of all components in overlapped peaks"
- [readme] The GCMSFormer model was trained, validated, and tested with 100,000 augmented simulated overlapped peaks in a ratio of 8:1:1: "The GCMSFormer model was trained, validated, and tested with 100,000 augmented simulated overlapped peaks in a ratio of 8:1:1"
- [readme] its bilingual evaluation understudy (BLEU) on the test set was 0.9988: "its bilingual evaluation understudy (BLEU) on the test set was 0.9988"
- [readme] We proposed the GCMSFormer for resolving the overlapped peaks in complex GC-MS data based on a Transformer model: "We proposed the GCMSFormer for resolving the overlapped peaks in complex GC-MS data based on a Transformer model"
