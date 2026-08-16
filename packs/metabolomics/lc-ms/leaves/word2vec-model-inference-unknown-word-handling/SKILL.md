---
name: word2vec-model-inference-unknown-word-handling
description: Use when when applying a pre-trained Word2Vec model to mass spectra at inference time (e.g., library matching or molecular networking), especially when the query spectra may contain fragment peaks or neutral losses not represented in the model's training vocabulary.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
  tools:
  - Spec2Vec
  - Word2Vec
  - matchms
  - gensim
  - NumPy
  - Numba
  - Pandas
  techniques:
  - LC-MS
  - GC-MS
derived_from:
- doi: 10.1371/journal.pcbi.1008724
  title: Spec2Vec
evidence_spans:
- we introduce Spec2Vec, a novel spectral similarity score
- spec2vec (https://github.com/iomega/spec2vec). Both packages are freely available and can be installed via conda
- inspired by a natural language processing algorithm—Word2Vec
- A Word2Vec [22] model is trained on all documents of a chosen dataset using gensim [37]
- the implementations for the cosine score and the modified cosine score used can be found in the Python package matchms
- the implementations for the cosine score and the modified cosine score used can be found in the Python package matchms [31] (https://github.com/matchms/matchms)
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1008724
  all_source_dois:
  - 10.1371/journal.pcbi.1008724
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# word2vec-model-inference-unknown-word-handling

## Summary

Quantify and handle unknown peaks (words) in mass spectra that fall outside a trained Word2Vec model's vocabulary during similarity inference. This skill estimates the weighted fraction of spectral intensity represented by out-of-vocabulary peaks and applies a missing-fraction threshold to avoid spurious Spec2Vec similarity scores on spectra with insufficient feature coverage.

## When to use

When applying a pre-trained Word2Vec model to mass spectra at inference time (e.g., library matching or molecular networking), especially when the query spectra may contain fragment peaks or neutral losses not represented in the model's training vocabulary. This is critical when the training corpus is small or covers a limited chemical space, or when new experimental data contains peaks arising from rare fragmentation patterns or instrumentation-specific artifacts.

## When NOT to use

- Input spectra are already de novo fragmentation patterns or synthetic data with no m/z-based word representation.
- The Word2Vec model was trained on the same spectra now being scored; in this case, unknown words should be rare by design and missing-fraction filtering may be overly aggressive.
- The downstream task does not require filtering by learned-feature coverage (e.g., purely empirical cosine-based similarity scores that do not depend on word embeddings).

## Inputs

- pre-trained Word2Vec model (gensim format or compatible)
- mass spectra (as matchms Spectrum objects or records with peak m/z and intensity arrays)
- precursor m/z and parent mass for each spectrum
- missing-fraction threshold (float, e.g., 0.05)

## Outputs

- missing-fraction value per spectrum (float, 0 to 1)
- binary classification (pass/fail) based on threshold
- coverage metric (1 − mean missing fraction) aggregated across dataset
- filtered subset of spectra meeting coverage threshold

## How to apply

For each spectrum at inference, convert peaks to words (format '[redacted-email]' with 2-decimal m/z binning) and neutral losses ('[redacted-email]', 5.0–200.0 Da range). Normalize peak intensities to maximum = 1 per spectrum. Compute the missing fraction as: missing_fraction = 1 − (Σ√w_i for words present in model vocabulary) / (Σ√w_i for all words), where w_i is peak intensity. The numerator sums square-root intensities of known words; the denominator sums square-root intensities across all words in the spectrum. Apply a configurable threshold (e.g., missing_fraction < 0.05) to filter spectra with insufficient learned peak coverage before computing or reporting Spec2Vec scores. This prevents the model from making predictions on spectra where the majority of intensity comes from unknown peaks. The square-root weighting emphasizes stronger peaks while down-weighting noise.

## Related tools

- **gensim** (loads and queries pre-trained Word2Vec model for vocabulary membership and word embeddings)
- **matchms** (loads, parses, and standardizes mass spectra; provides peak and metadata access) — https://github.com/matchms/matchms
- **Spec2Vec** (applies learned spectral embeddings derived from Word2Vec; missing-fraction filtering prevents scoring on under-covered spectra) — https://github.com/iomega/spec2vec
- **NumPy** (vectorized computation of missing-fraction statistics and aggregate coverage metrics)

## Examples

```
from gensim.models import Word2Vec
from matchms.importing_utils import load_from_msp
import numpy as np

model = Word2Vec.load('allpositive_15epochs.model')
spectra = load_from_msp('query_spectra.msp')

for spectrum in spectra:
    peaks_words = [f'peak@{mz:.2f}' for mz in spectrum.peaks.mz]
    losses_words = [f'loss@{spectrum.precursor_mz - mz:.2f}' for mz in spectrum.peaks.mz if 5.0 <= spectrum.precursor_mz - mz <= 200.0]
    all_words = peaks_words + losses_words
    intensities = spectrum.peaks.intensities / spectrum.peaks.intensities.max()
    
    intensity_dict = dict(zip(peaks_words + losses_words, intensities))
    known_intensity_sum = sum(np.sqrt(intensity_dict[w]) for w in all_words if w in model.wv.key_to_index)
    total_intensity_sum = sum(np.sqrt(intensity_dict[w]) for w in all_words)
    
    missing_frac = 1.0 - (known_intensity_sum / total_intensity_sum) if total_intensity_sum > 0 else 0.0
    if missing_frac < 0.05:
        print(f'{spectrum.metadata["spectrum_id"]}: coverage={1-missing_frac:.3f}')
```

## Evaluation signals

- Missing-fraction values lie in [0, 1] and are monotonically decreasing with increasing training corpus size.
- Spectra with no unknown peaks have missing_fraction = 0; spectra with all peaks unknown have missing_fraction → 1.
- Coverage (1 − mean missing_fraction) at 15 training epochs on AllPositive dataset reaches ≥ 0.97 (97% threshold).
- Applying missing-fraction threshold (e.g., < 0.05) removes the high false-positive rate in Spec2Vec similarity for under-covered spectra, measurable by correlation with structural similarity (InChIKey) compared to unfiltered results.
- Threshold behavior is reproducible across independent subsamples of the dataset; coverage curve converges smoothly as training corpus size increases.

## Limitations

- The missing-fraction metric depends on the square-root weighting scheme; alternative intensity weightings (linear, log) may yield different results and require empirical validation.
- Model pre-training on a large spectra dataset reduces but does not eliminate the need for retraining when applied to data with insufficient feature overlap in novel experimental contexts (e.g., new instrument types, collision energy regimes, or chemical classes not well represented in training).
- Neutral losses are only reliably measured in LC-MS and not typically present in GC-MS; the skill is limited to LC-MS workflows and may not generalize to other ionization or separation techniques.
- The skill assumes a uniform 2-decimal m/z binning precision. Spectra with very high or low parent mass may require adaptive binning or peak-filtering strategies (e.g., max_peaks = 0.5 × parent_mass) to avoid vocabulary explosion or sparsity.

## Evidence

- [methods] In those instances some words (= peaks) of a given spectra might be unknown to the model. In those instances we can estimate the impact of the missing words by assessing the uncovered weighted part: "In those instances some words (= peaks) of a given spectra might be unknown to the model. In those instances we can estimate the impact of the missing words by assessing the uncovered weighted part"
- [other] missing_fraction = 1 − (Σ√w_i for words in model) / (Σ√w_i for all words), where w_i is peak intensity: "missing_fraction = 1 − (Σ√w_i for words in model) / (Σ√w_i for all words), where w_i is peak intensity"
- [methods] By setting a threshold for the missing fraction (e.g. <0.05), returning Spec2Vec similarity scores for spectra far outside the learned peaks (and losses) can be avoided: "By setting a threshold for the missing fraction (e.g. <0.05), returning Spec2Vec similarity scores for spectra far outside the learned peaks (and losses) can be avoided"
- [other] For each spectrum, convert peaks to words with format '[redacted-email]' (2-decimal binning) and add neutral losses (5.0–200.0 Da) as '[redacted-email]' words. Normalize peak intensities to maximum = 1 for each spectrum.: "For each spectrum, convert peaks to words with format '[redacted-email]' (2-decimal binning) and add neutral losses (5.0–200.0 Da) as '[redacted-email]' words. Normalize peak intensities to maximum = 1 for"
- [discussion] one limitation of Spec2Vec as compared to cosine scores is that it needs training data to learn the fragment peak relationships; however, since this not necessarily needs to be library spectra and in: "one limitation of Spec2Vec as compared to cosine scores is that it needs training data to learn the fragment peak relationships; however, since this not necessarily needs to be library spectra"
- [discussion] For many cases, we expect that a model pre-trained on a large spectra dataset will cover a large enough fraction of the features to work well without the need for additional re-training: "For many cases, we expect that a model pre-trained on a large spectra dataset will cover a large enough fraction of the features to work well without the need for additional re-training"
- [discussion] In the present work, we have only demonstrated performance on LC-MS data and not yet assessed Spec2Vec for GC-MS data. For GC-MS, neutral losses are usually not measured.: "In the present work, we have only demonstrated performance on LC-MS data and not yet assessed Spec2Vec for GC-MS data. For GC-MS, neutral losses are usually not measured."
