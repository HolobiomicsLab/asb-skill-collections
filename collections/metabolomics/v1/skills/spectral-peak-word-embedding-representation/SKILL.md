---
name: spectral-peak-word-embedding-representation
description: Use when when you have MS/MS spectra (LC-MS or equivalent positive ionization mode data) that you intend to embed using Word2Vec or similar distributional semantic models, or when you need to prepare spectral data for training similarity models that learn peak co-occurrence patterns rather than.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3473
  tools:
  - Spec2Vec
  - matchms
  - gensim
  - NumPy
  - Numba
  - Pandas
  - spec2vec
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
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: spec2vec_grounded
    doi: 10.1371/journal.pcbi.1008724
    title: Spec2Vec
  dedup_kept_from: spec2vec_grounded
schema_version: 0.2.0
---

# spectral-peak-word-embedding-representation

## Summary

Convert mass spectrometry fragment peaks and neutral losses into word tokens suitable for Word2Vec embedding, enabling learned representation of fragmental relationships. This representation bridges spectral data and natural language processing to capture structural similarity patterns in MS/MS spectra.

## When to use

When you have MS/MS spectra (LC-MS or equivalent positive ionization mode data) that you intend to embed using Word2Vec or similar distributional semantic models, or when you need to prepare spectral data for training similarity models that learn peak co-occurrence patterns rather than relying on cosine-based peak matching alone.

## When NOT to use

- Input spectra contain fewer than 10 fragment peaks (filter these before tokenization)
- Data is GC-MS where neutral losses are not reliably measured; Spec2Vec was only demonstrated on LC-MS
- You require deterministic, directly interpretable peak alignment (cosine or modified cosine scores are more transparent)

## Inputs

- MS/MS spectra (mzML, mzXML, msp, MGF, or JSON format)
- Normalized spectrum object with peaks (m/z, intensity pairs) and precursor m/z
- Peak intensity matrix (relative intensities normalized to [0, 1] range)

## Outputs

- Spectrum-as-document representation (list of peak and loss word tokens per spectrum)
- Ordered token sequence suitable for Word2Vec gensim.models.Word2Vec input
- Peak vocabulary with token-to-m/z mapping for later embedding lookups

## How to apply

For each spectrum, normalize peak intensities to a maximum of 1.0. Convert each peak to a word token using the format 'peak@xxx.xx' (binned to 2 decimal places in m/z space). Add neutral loss words by computing precursor m/z minus each peak m/z, retaining only losses in the range 5.0–200.0 Da, formatted as 'loss@xxx.xx'. Filter peaks by intensity (relative intensity ≥ 0.01 of max) and by parent mass scaling (retain at most 0.5 × parent_mass peaks per spectrum). This tokenization transforms each spectrum into a 'document' (ordered sequence of words) that preserves both fragmental identity and neutral loss patterns, which Word2Vec then learns as a co-occurrence space. The binning precision and mass range cutoffs are justified to balance model generalization against sparsity.

## Related tools

- **matchms** (Provides spectral data structures, I/O loaders (mzML, MGF, msp), peak filtering, and intensity normalization functions used to prepare spectra before tokenization) — https://github.com/matchms/matchms
- **gensim** (Implements Word2Vec model training and word embedding lookups on the tokenized peak and loss sequences)
- **spec2vec** (Wraps this tokenization workflow and applies trained Word2Vec embeddings to compute spectral similarity scores based on learned peak relationships) — https://github.com/iomega/spec2vec
- **NumPy** (Used for intensity normalization and numerical operations on peak arrays)
- **Numba** (Provides JIT-compiled functions for fast computation of missing-fraction statistics and embedding aggregations across large spectra collections)

## Examples

```
from matchms import Spectrum; from spec2vec import Spec2VecParallel; import gensim; spectra = [Spectrum(mz=np.array([100.1, 200.2, 300.3]), intensities=np.array([0.5, 1.0, 0.3]), metadata={'precursor_mz': 400.4})]; documents = [[f'peak@{mz:.2f}' for mz in s.mz] + [f'loss@{(s.metadata["precursor_mz"] - mz):.2f}' for mz in s.mz if 5.0 <= (s.metadata["precursor_mz"] - mz) <= 200.0] for s in spectra]; model = gensim.models.Word2Vec(documents, window=10, min_count=1, epochs=15)
```

## Evaluation signals

- Every spectrum in the tokenized corpus contains at least 1 peak word token (spectra with <10 original peaks are filtered out; retained spectra should have ≥1 token after binning and filtering)
- Peak word vocabulary size grows monotonically with the number of unique m/z values in the input dataset; no negative vocabulary counts
- Missing-fraction metric (1 − Σ√w_i for known words / Σ√w_i for all words) computed on the held-out test set reaches ≈97% coverage when the Word2Vec model is trained on a large corpus (e.g., AllPositive dataset, 95,320 spectra, 15 epochs)
- Each loss word token falls strictly in the range 5.0–200.0 Da; losses outside this range are absent from the output
- Peak intensity normalization is correctly applied: max intensity per spectrum equals 1.0, all others ≤ 1.0; relative peak filtering (intensity < 0.01) removes the expected proportion of low-intensity peaks

## Limitations

- GC-MS data are not supported; neutral losses are typically not measured in GC-MS, reducing the utility of this tokenization scheme (only LC-MS demonstrated)
- Tokenization binning to 2 decimal places (m/z precision) may lose fine structural detail and may merge nearby peaks; alternative binning strategies are not explored in the article
- Unknown peaks (word tokens) not present in the trained Word2Vec model are excluded from similarity computation; this requires a model trained on a representative corpus; retraining may be necessary for experimental data with insufficient feature overlap to the training set
- Spectra with fewer than 10 fragment peaks are filtered before tokenization, discarding potentially informative low-complexity spectra
- No guidance provided on optimal loss-mass range (5.0–200.0 Da) selection for datasets with unusual precursor mass distributions

## Evidence

- [methods] After processing, spectra are converted to documents. For this, every peak is represented by a word that contains its position up to a defined decimal precision ("peak@xxx.xx"): "After processing, spectra are converted to documents. For this, every peak is represented by a word that contains its position up to a defined decimal precision ("peak@xxx.xx")"
- [methods] In addition to all peaks of a spectrum, neutral losses between 5.0 and 200.0 Da were added as "loss@xxx.xx". Neutral losses are calculated as precursor − peak: "In addition to all peaks of a spectrum, neutral losses between 5.0 and 200.0 Da were added as "loss@xxx.xx". Neutral losses are calculated as precursor − peak"
- [other] For each spectrum, convert peaks to words with format 'peak@xxx.xx' (2-decimal binning) and add neutral losses (5.0–200.0 Da) as 'loss@xxx.xx' words. Normalize peak intensities to maximum = 1 for each spectrum.: "For each spectrum, convert peaks to words with format 'peak@xxx.xx' (2-decimal binning) and add neutral losses (5.0–200.0 Da) as 'loss@xxx.xx' words. Normalize peak intensities to maximum = 1 for"
- [methods] the maximum number of kept peaks per spectrum was set to scale linearly with the estimated parent mass: max(n_peaks) = 0.5 × parentmass: "the maximum number of kept peaks per spectrum was set to scale linearly with the estimated parent mass: max(n_peaks) = 0.5 × parentmass"
- [methods] For both the cosine and modified cosine score calculations we ignored all peaks with relative intensities <0.01 compared to the highest intensity peak: "For both the cosine and modified cosine score calculations we ignored all peaks with relative intensities <0.01 compared to the highest intensity peak"
- [readme] Spec2Vec does so for mass fragments and neutral losses in MS/MS spectra. The spectral similarity score is based on spectral embeddings learnt from the fragmental relationships within a large set of spectral data.: "Spec2Vec does so for mass fragments and neutral losses in MS/MS spectra. The spectral similarity score is based on spectral embeddings learnt from the fragmental relationships within a large set of"
