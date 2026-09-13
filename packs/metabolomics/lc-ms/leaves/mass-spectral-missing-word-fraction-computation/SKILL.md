---
name: mass-spectral-missing-word-fraction-computation
description: Use when when applying a pre-trained Spec2Vec Word2Vec model to new mass
  spectra (particularly those outside the model's training distribution), you need
  to assess whether peaks and neutral losses in query spectra have been seen during
  model training.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0092
  tools:
  - Spec2Vec
  - matchms
  - gensim
  - NumPy
  - Numba
  - Pandas
  - Word2Vec
  techniques:
  - LC-MS
  - GC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1371/journal.pcbi.1008724
  title: Spec2Vec
evidence_spans:
- we introduce Spec2Vec, a novel spectral similarity score
- spec2vec (https://github.com/iomega/spec2vec). Both packages are freely available
  and can be installed via conda
- the implementations for the cosine score and the modified cosine score used can
  be found in the Python package matchms
- the implementations for the cosine score and the modified cosine score used can
  be found in the Python package matchms [31] (https://github.com/matchms/matchms)
- A Word2Vec [22] model is trained on all documents of a chosen dataset using gensim
  [37]
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

# mass-spectral-missing-word-fraction-computation

## Summary

Quantifies the fraction of peak intensity in a mass spectrum that lacks corresponding word embeddings in a trained Word2Vec model, enabling assessment of model coverage and limiting high-uncertainty similarity scores. This metric is essential for understanding when Spec2Vec embeddings are reliable and when peaks fall outside the learned feature space.

## When to use

When applying a pre-trained Spec2Vec Word2Vec model to new mass spectra (particularly those outside the model's training distribution), you need to assess whether peaks and neutral losses in query spectra have been seen during model training. Use this skill if you want to quantify the risk of unreliable similarity scores due to unknown fragments, or if you need to set a filtering threshold (e.g., 'exclude matches with >5% missing fraction') to avoid returning spurious hits for spectra composed largely of novel peaks.

## When NOT to use

- The input spectra were used to train the Word2Vec model itself; missing fraction will be artificially low and will not reflect real generalization gaps.
- You are comparing spectra only via cosine or modified-cosine similarity (not Spec2Vec); missing fraction is specific to Word2Vec embeddings and not relevant to cosine-based methods.
- The Word2Vec model was trained on GC-MS data and you are analyzing LC-MS spectra (or vice versa); feature overlap will be poor and missing fraction alone does not indicate model appropriateness across MS types.

## Inputs

- mass spectra (matchms Spectrum objects or equivalent with peaks, precursor m/z, and normalized intensities)
- pre-trained Word2Vec model (gensim word2vec.KeyedVectors or model object with known vocabulary)
- model vocabulary (set or dict of known '[redacted-email]' and '[redacted-email]' words)

## Outputs

- missing_fraction per spectrum (float, range [0, 1])
- coverage per spectrum (float, range [0, 1]; 1 − missing_fraction)
- dataset-level missing-fraction statistics (mean, median, distribution)
- filtered spectrum list or boolean mask (if threshold applied)

## How to apply

For each spectrum in your dataset: (1) normalize peak intensities to maximum = 1.0; (2) convert peaks to words in the format '[redacted-email]' (2-decimal m/z binning) and compute neutral losses (precursor − peak, 5.0–200.0 Da range) as '[redacted-email]' words; (3) for each word, check if it exists in the trained Word2Vec model's vocabulary; (4) sum the square-root-transformed intensities (√w_i) of words present in the model, and sum the √w_i of all words in the spectrum; (5) compute missing_fraction = 1 − (Σ√w_i for known words) / (Σ√w_i for all words); (6) aggregate missing fractions across all spectra to derive dataset-level coverage statistics. Use missing_fraction as a filtering criterion: optionally exclude spectra with missing_fraction exceeding a threshold (e.g., <0.05, corresponding to ≥95% coverage) before returning Spec2Vec similarity scores, to avoid returning high-confidence matches for spectra that are largely composed of novel, unseen fragments.

## Related tools

- **Spec2Vec** (Provides the Word2Vec embedding space and similarity scoring framework; missing-word-fraction is used to filter or weight Spec2Vec similarity scores based on embedding coverage) — https://github.com/iomega/spec2vec
- **Word2Vec** (Generates the learned word embeddings for peaks and losses; missing_fraction measures the overlap between spectrum words and Word2Vec's vocabulary)
- **matchms** (Provides data structures (Spectrum objects), peak normalization, neutral-loss computation, and spectral I/O; used to load and preprocess spectra before missing-fraction calculation) — https://github.com/matchms/matchms
- **gensim** (Stores and manages trained Word2Vec models and their vocabularies; provides vocabulary lookup to check word presence)
- **NumPy** (Efficient array operations for computing aggregated statistics (sums, means, distributions) of missing fractions across spectra)

## Examples

```
from spec2vec import Spec2Vec
from matchms.importing import load_from_msp
import numpy as np

spectra = load_from_msp('unknowns.msp')
model = Word2Vec.load('allpositive_15epochs.model')
missing_fractions = []
for spectrum in spectra:
    word_intensities = spectrum.peaks.intensities / spectrum.peaks.intensities.max()
    known_sum = sum(np.sqrt(word_intensities[i]) for word in spectrum_words if word in model.wv.index_to_key)
    all_sum = np.sum(np.sqrt(word_intensities))
    missing_fractions.append(1 - known_sum / all_sum)

print(f'Mean coverage: {1 - np.mean(missing_fractions):.2%}')
```

## Evaluation signals

- Missing-fraction values lie in [0, 1] and sum-of-square-root-transformed-intensities is always ≤ spectrum total √intensity (i.e., known-words sum ≤ all-words sum).
- Spectra used to train the Word2Vec model have missing_fraction = 0.0 or very close to 0.0, while spectra from external datasets show higher missing fractions (>0.05 typical).
- Setting a missing-fraction threshold (e.g., max 0.05) and filtering spectra reduces the tail of low-confidence Spec2Vec matches, as verified by independently computing Spec2Vec similarity on filtered vs. unfiltered data.
- Dataset-level mean missing fraction is consistent with or lower than the framing used in pre-trained model documentation (e.g., 'AllPositive dataset at 15 epochs achieves ~97% coverage' → mean missing_fraction ~0.03).
- Spectra composed entirely of novel peaks not in the Word2Vec vocabulary yield missing_fraction = 1.0; spectra with all peaks in vocabulary yield missing_fraction = 0.0.

## Limitations

- Missing-fraction computation requires a pre-trained Word2Vec model and is specific to the m/z binning precision used during model training (e.g., 2-decimal '[redacted-email]' format); retrained or differently-binned models will yield different missing fractions.
- Missing fraction does not account for the quality or reliability of individual word embeddings; a peak may exist in the model's vocabulary but be poorly embedded if it was rare in the training corpus.
- Large-scale spectra with many novel peaks (missing_fraction > 0.2–0.3) may still yield spurious Spec2Vec hits because the few known peaks can align by chance; missing-fraction thresholding is a necessary but not sufficient filter.
- For GC-MS data, neutral losses are typically not measured and recorded; the neutral-loss component ('[redacted-email]' words) will be absent, potentially inflating missing fractions compared to LC-MS workflows and limiting the applicability of LC-MS trained models.
- The missing-fraction metric assumes square-root transformation of peak intensities; using raw or log-transformed intensities will alter the weighted missing-fraction numerically and require re-validation against published benchmarks.

## Evidence

- [other] missing_fraction = 1 − (Σ√w_i for words in model) / (Σ√w_i for all words), where w_i is peak intensity: "missing_fraction = 1 − (Σ√w_i for words in model) / (Σ√w_i for all words), where w_i is peak intensity"
- [other] For each spectrum, convert peaks to words with format '[redacted-email]' (2-decimal binning) and add neutral losses (5.0–200.0 Da) as '[redacted-email]' words.: "For each spectrum, convert peaks to words with format '[redacted-email]' (2-decimal binning) and add neutral losses (5.0–200.0 Da) as '[redacted-email]' words"
- [methods] By setting a threshold for the missing fraction (e.g. <0.05), returning Spec2Vec similarity scores for spectra far outside the learned peaks (and losses) can be avoided: "By setting a threshold for the missing fraction (e.g. <0.05), returning Spec2Vec similarity scores for spectra far outside the learned peaks (and losses) can be avoided"
- [methods] In those instances some words (= peaks) of a given spectra might be unknown to the model. In those instances we can estimate the impact of the missing words by assessing the uncovered weighted part: "In those instances some words (= peaks) of a given spectra might be unknown to the model. In those instances we can estimate the impact of the missing words by assessing the uncovered weighted part"
- [other] A Word2Vec model trained on the AllPositive dataset for 15 iterations achieves approximately 97% peak coverage, quantified by computing the missing-fraction statistic: "A Word2Vec model trained on the AllPositive dataset for 15 iterations achieves approximately 97% peak coverage, quantified by computing the missing-fraction statistic"
- [other] Normalize peak intensities to maximum = 1 for each spectrum.: "Normalize peak intensities to maximum = 1 for each spectrum"
- [discussion] Spec2Vec requires training data with large fraction of features (fragment ions and losses) present; may require retraining on new experimental spectra not covered in initial training set: "Spec2Vec requires training data with large fraction of features (fragment ions and losses) present; may require retraining on new experimental spectra not covered in initial training set"
- [discussion] For GC-MS, neutral losses are usually not measured.: "For GC-MS, neutral losses are usually not measured."
