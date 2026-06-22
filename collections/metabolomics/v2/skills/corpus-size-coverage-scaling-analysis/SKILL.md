---
name: corpus-size-coverage-scaling-analysis
description: Use when when deploying a Word2Vec-based spectral similarity model (such as Spec2Vec) on a new mass spectrometry dataset and needing to assess whether the pre-trained model's learned peak embeddings sufficiently represent the peaks in your query spectra.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Spec2Vec
  - matchms
  - gensim
  - NumPy
  - Numba
  - Pandas
  - Word2Vec
  - NumPy, Pandas
derived_from:
- doi: 10.1371/journal.pcbi.1008724
  title: Spec2Vec
evidence_spans:
- we introduce Spec2Vec, a novel spectral similarity score
- spec2vec (https://github.com/iomega/spec2vec). Both packages are freely available and can be installed via conda
- the implementations for the cosine score and the modified cosine score used can be found in the Python package matchms
- the implementations for the cosine score and the modified cosine score used can be found in the Python package matchms [31] (https://github.com/matchms/matchms)
- A Word2Vec [22] model is trained on all documents of a chosen dataset using gensim [37]
- Spec2Vec was optimised by making extensive use of Numpy [24]
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: spec2vec_grounded
    doi: 10.1371/journal.pcbi.1008724
    title: Spec2Vec
  dedup_kept_from: spec2vec_grounded
schema_version: 0.2.0
---

# corpus-size-coverage-scaling-analysis

## Summary

Quantifies how Word2Vec model coverage of spectral features (peaks and neutral losses) scales with increasing training corpus size, using the missing-fraction metric to assess the proportion of spectral peaks with learned embeddings. This skill evaluates whether large pre-trained models achieve sufficient feature coverage (e.g., 97%) to enable reliable Spec2Vec similarity scoring without additional retraining.

## When to use

When deploying a Word2Vec-based spectral similarity model (such as Spec2Vec) on a new mass spectrometry dataset and needing to assess whether the pre-trained model's learned peak embeddings sufficiently represent the peaks in your query spectra. Specifically, when unknown or poorly-represented peaks in the model would compromise similarity score reliability, and you need to decide whether to use the model as-is, retrain on additional data, or establish a missing-fraction threshold for filtering unreliable comparisons.

## When NOT to use

- Input spectra use GC-MS ionization mode or other techniques where neutral losses are not typically measured; the missing-fraction metric will not meaningfully reflect model coverage in such contexts.
- You have already manually retrained a Word2Vec model on your specific dataset; the scaling analysis is most valuable for deciding WHETHER to retrain, not after retraining is complete.
- Your use case does not require per-spectrum filtering or reliability assessment; if you simply need a single similarity score between two spectra, the missing-fraction computation adds overhead without decision-relevant output.

## Inputs

- Mass spectrometry spectra in standardized format (e.g., Spectrum objects from matchms with peak m/z and intensity arrays)
- Pre-trained Word2Vec model with learned embeddings for peak and neutral-loss tokens
- Spectral dataset to assess (e.g., AllPositive dataset with 95,320 positive-mode spectra)

## Outputs

- Per-spectrum missing-fraction values (scalar in [0, 1] per spectrum)
- Aggregated coverage metric (1 − mean missing fraction across all spectra; scalar in [0, 1])
- Coverage-versus-corpus-size curve (plot of coverage on y-axis, training set size on x-axis)
- Optional: filtered spectrum list (spectra passing missing-fraction threshold, e.g., < 0.05)

## How to apply

For each spectrum in your dataset, convert peaks to standardized word tokens (e.g., '[redacted-email]' with 2-decimal m/z binning) and add neutral losses (5.0–200.0 Da) as '[redacted-email]' words. Normalize peak intensities to maximum = 1 per spectrum. Compute the missing fraction for each spectrum as: missing_fraction = 1 − (Σ√w_i for words in trained model) / (Σ√w_i for all words), where w_i is peak intensity. Aggregate missing fractions across all spectra to calculate mean coverage (1 − mean missing fraction). To generate a coverage-versus-corpus-size curve, iteratively subset the dataset (e.g., by adding spectra progressively), retrain a Word2Vec model at each step, and recompute coverage. Plot coverage against effective corpus size to identify plateau points or saturation thresholds. Use the missing-fraction metric as a per-spectrum filter (e.g., discard spectra with missing_fraction > 0.05) to avoid returning unreliable Spec2Vec scores for peaks far outside the learned feature space.

## Related tools

- **Word2Vec** (Trains embeddings of peak and neutral-loss tokens from spectral corpus; pre-trained model is queried to identify which words (peaks/losses) have learned representations)
- **Spec2Vec** (Spectral similarity scoring method that depends on Word2Vec embeddings; missing-fraction metric quantifies coverage of Spec2Vec's feature dependencies) — https://github.com/iomega/spec2vec
- **matchms** (Provides spectrum data structures, peak normalization, and standardized interfaces for loading and processing MS/MS spectra from multiple formats) — https://github.com/matchms/matchms
- **gensim** (Word2Vec implementation used to train or load pre-trained models and query word embeddings)
- **NumPy, Pandas** (Vectorized computation of intensity-weighted sums (√w_i aggregation) and aggregation of per-spectrum missing-fraction values)

## Examples

```
# Load pre-trained Word2Vec model and AllPositive spectra; compute missing fraction for each spectrum
from spec2vec import Spec2Vec
from gensim.models import Word2Vec
import numpy as np

model = Word2Vec.load('model_AllPositive_15epochs.model')
missing_fractions = []
for spectrum in spectra:
    weighted_sum_known = sum([np.sqrt(spectrum.intensity[i]) for i, mz in enumerate(spectrum.mz) if f'peak@{mz:.2f}' in model.wv])
    weighted_sum_all = sum([np.sqrt(i) for i in spectrum.intensity])
    missing_fraction = 1 - (weighted_sum_known / weighted_sum_all) if weighted_sum_all > 0 else 0
    missing_fractions.append(missing_fraction)

coverage = 1 - np.mean(missing_fractions)
print(f'Coverage: {coverage:.2%}')
```

## Evaluation signals

- Coverage metric converges to a plateau as corpus size increases (e.g., asymptotic behavior near 97% for AllPositive at 15 training epochs), indicating saturation of learned features.
- Mean missing fraction across all spectra is consistent with reported coverage (e.g., mean missing_fraction ≈ 0.03 for 97% coverage); verify using: coverage = 1 − mean_missing_fraction.
- Per-spectrum missing-fraction values are in [0, 1] and the distribution reflects the heterogeneity of the dataset (e.g., spectra with common peaks have lower missing fractions than rare ones).
- When filtering spectra by missing_fraction < 0.05, the subset retains >90% of spectra and downstream Spec2Vec similarity scores show improved correlation with structural similarity (as evidenced by reduced false positive rates).
- Coverage-vs-corpus-size curve reproduces known saturation points from reference models (e.g., UniqueInchikey or AllPositive datasets); verify against published benchmarks if available.

## Limitations

- Missing-fraction metric assumes that all peaks and neutral losses are equally informative; it does not account for differential importance of specific fragments for structural discrimination.
- Pre-trained Word2Vec models may not generalize to spectra with rare or novel fragments not present in the training corpus; retraining on new experimental data may still be required for datasets with poor feature overlap, even if overall corpus size is large.
- The metric is specific to LC-MS/MS data; GC-MS spectra typically lack measured neutral losses, so the missing-fraction computation cannot be meaningfully applied to GC-MS without modification.
- Coverage saturation depends heavily on training parameters (e.g., number of Word2Vec epochs); coverage curves derived with different training configurations may not be directly comparable.
- The 2-decimal precision binning ('[redacted-email]') is a design choice; stricter binning (e.g., 1 decimal) increases the number of unique tokens and can lower coverage, while looser binning reduces feature discrimination.

## Evidence

- [other] missing_fraction = 1 − (Σ√w_i for words in model) / (Σ√w_i for all words), where w_i is peak intensity: "compute the missing fraction as: missing_fraction = 1 − (Σ√w_i for words in model) / (Σ√w_i for all words), where w_i is peak intensity"
- [other] coverage = 1 − mean missing fraction across all spectra: "Aggregate missing-fraction statistics across all spectra and compute the proportion of peaks with known word embeddings (coverage = 1 − mean missing fraction)"
- [other] Word2Vec model trained on the AllPositive dataset for 15 iterations achieves approximately 97% peak coverage: "A Word2Vec model trained on the AllPositive dataset for 15 iterations achieves approximately 97% peak coverage, quantified by computing the missing-fraction statistic"
- [other] Vary effective corpus size by progressively adding spectra and recompute coverage at each step to generate a coverage-vs-corpus-size curve: "Vary effective corpus size by progressively adding spectra and recompute coverage at each step to generate a coverage-vs-corpus-size curve"
- [methods] By setting a threshold for the missing fraction (e.g. <0.05), returning Spec2Vec similarity scores for spectra far outside the learned peaks (and losses) can be avoided: "By setting a threshold for the missing fraction (e.g. <0.05), returning Spec2Vec similarity scores for spectra far outside the learned peaks (and losses) can be avoided"
- [other] peak intensities normalized to maximum = 1 for each spectrum: "Normalize peak intensities to maximum = 1 for each spectrum"
- [other] convert peaks to words with format '[redacted-email]' (2-decimal binning) and add neutral losses (5.0–200.0 Da) as '[redacted-email]' words: "convert peaks to words with format '[redacted-email]' (2-decimal binning) and add neutral losses (5.0–200.0 Da) as '[redacted-email]' words"
- [discussion] Spec2Vec requires training data with large fraction of features (fragment ions and losses) present; may require retraining on new experimental spectra not covered in initial training set: "one limitation of Spec2Vec as compared to cosine scores is that it needs training data to learn the fragment peak relationships"
- [discussion] Limited demonstration of Spec2Vec performance restricted to LC-MS data; GC-MS data not demonstrated due to neutral losses usually not being measured: "In the present work, we have only demonstrated performance on LC-MS data and not yet assessed Spec2Vec for GC-MS data. For GC-MS, neutral losses are usually not measured."
