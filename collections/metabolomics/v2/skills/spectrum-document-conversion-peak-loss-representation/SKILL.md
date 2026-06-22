---
name: spectrum-document-conversion-peak-loss-representation
description: Use when when preparing MS/MS spectral data for training word-embedding models (Word2Vec, Skip-gram, CBOW) that will learn relationships between fragment ions and neutral losses.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Spec2Vec
  - matchms
  - gensim
  - RDKit
  - NumPy
  - Numba
  - Pandas
  - scipy
  - gensim (Word2Vec, CBOW, Skip-gram)
  - NumPy, Pandas, SciPy
  techniques:
  - GC-MS
derived_from:
- doi: 10.1371/journal.pcbi.1008724
  title: Spec2Vec
evidence_spans:
- we introduce Spec2Vec, a novel spectral similarity score
- spec2vec (https://github.com/iomega/spec2vec). Both packages are freely available and can be installed via conda
- the implementations for the cosine score and the modified cosine score used can be found in the Python package matchms
- the implementations for the cosine score and the modified cosine score used can be found in the Python package matchms [31] (https://github.com/matchms/matchms)
- A Word2Vec [22] model is trained on all documents of a chosen dataset using gensim [37]
- Tanimoto similarity (Jaccard index) based on daylight-like molecular fingerprints, version 2020.03.2, 2048 bits, derived using rdkit
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectrum-document-conversion-peak-loss-representation

## Summary

Convert mass spectra into text-like documents by representing fragment peaks and neutral losses as discrete words, enabling natural language processing algorithms (e.g., Word2Vec) to learn spectral embeddings. This representation bridges MS/MS spectra and NLP by treating peaks and losses as vocabulary units whose co-occurrence patterns encode structural relationships.

## When to use

When preparing MS/MS spectral data for training word-embedding models (Word2Vec, Skip-gram, CBOW) that will learn relationships between fragment ions and neutral losses. Use this skill prior to training spectral embedding models or computing similarity scores based on learned spectral vectors, particularly when the goal is to correlate spectral similarity with chemical structure.

## When NOT to use

- Input spectra have fewer than 10 fragment peaks or precursor m/z is unknown or unreliable — document representation will be too sparse or invalid for meaningful embedding training.
- Analyzing GC-MS data in which neutral losses are typically not measured or detected — the [redacted-email] component of the representation will be absent or uninformative.
- Goal is real-time or batch similarity scoring without training embeddings — use cosine or modified cosine scores directly instead.

## Inputs

- mass spectra (MS/MS) with fragment peak m/z and intensity values
- precursor m/z (for neutral loss calculation)
- spectrum count and peak counts (for filtering decisions)

## Outputs

- spectrum documents (lists or sequences of '[redacted-email]' and '[redacted-email]' tokens, optionally weighted by intensity)
- text corpus ready for Word2Vec or embedding model training

## How to apply

For each spectrum in your dataset: (1) extract all fragment peaks and represent each as a word token '[redacted-email]' using the m/z ratio binned to 2 decimal places; (2) calculate neutral losses as differences (precursor_m/z − peak_m/z) for losses in the range 5.0–200.0 Da and represent each as '[redacted-email]'; (3) weight each peak token by its normalized intensity (with square-root intensity weighting applied); (4) filter peaks according to parent mass scaling (retain up to max_peaks = 0.5 × parent_mass) to reduce noise and focus on informative fragments; (5) assemble all peak and loss tokens (weighted by intensity) into an ordered sequence to form a single 'document' for that spectrum. This document representation preserves the distributional structure of fragmentation and is then passed to Word2Vec or similar embedding models to learn latent relationships between fragments.

## Related tools

- **gensim (Word2Vec, CBOW, Skip-gram)** (trains word embeddings on the peak and loss token sequences to learn latent relationships between fragments and neutral losses across a large corpus of spectrum documents) — https://github.com/RaRe-Technologies/gensim
- **Spec2Vec** (uses the trained word embeddings from spectrum documents to compute spectral similarity scores via cosine distance between weighted document vectors) — https://github.com/iomega/spec2vec
- **matchms** (provides spectrum I/O, metadata cleaning, and filtering utilities to prepare raw spectra before document conversion) — https://github.com/matchms/matchms
- **NumPy, Pandas, SciPy** (handle numerical operations for intensity normalization, weighting, peak filtering, and vectorization of spectrum documents)

## Examples

```
from matchms import Spectrum; import numpy as np
spectra_docs = []
for spec in spectra:
    peaks = [(m_z, intensity) for m_z, intensity in spec.peaks]
    tokens = [f'peak@{round(m_z, 2)}' for m_z, intensity in peaks if m_z <= 0.5 * spec.precursor_mz]
    losses = [f'loss@{round(spec.precursor_mz - m_z, 2)}' for m_z, _ in peaks if 5.0 <= spec.precursor_mz - m_z <= 200.0]
    spectrum_doc = tokens + losses
    spectra_docs.append(spectrum_doc)
```

## Evaluation signals

- Each spectrum document contains at least one 'peak@' token (and ideally multiple) and zero or more 'loss@' tokens; documents are not empty or malformed.
- Peak tokens use consistent decimal precision (2 decimals); all m/z values fall within the expected analytical range (0–1000 m/z).
- Intensity-weighted peak tokens sum to the expected total normalized intensity (or close to it, accounting for peak filtering and normalization steps).
- Number of retained peaks per spectrum respects the scaling constraint max_peaks = 0.5 × parent_mass; no spectrum document exceeds this limit.
- Neutral loss calculations are valid: each loss is in the range [5.0, 200.0] Da and equals (precursor_m/z − peak_m/z) within rounding error.

## Limitations

- Spec2Vec embeddings are sensitive to the training corpus: models trained on one dataset (e.g., UniqueInchiKey) may not generalize well to spectra with fragments or losses not represented in the training set; retraining may be needed for experimental data with novel fragmentation patterns.
- Document representation discards peak order and absolute m/z information beyond binned tokens, potentially losing fine-grained mass calibration nuances.
- GC-MS spectra cannot be effectively represented using neutral loss tokens, since neutral losses are typically not measured in GC-MS workflows.
- The choice of decimal precision (2 decimals), peak mass scaling factor (0.5 × parent_mass), and neutral loss range (5–200 Da) are heuristic and may require tuning for different instrument types or metabolite classes.
- Rare fragments (high m/z, low abundance) that appear in only a few spectra may receive poor embeddings or be ignored due to peak filtering; this can bias similarity scores for structural analogues with atypical fragmentation.

## Evidence

- [methods] After processing, spectra are converted to documents. For this, every peak is represented by a word that contains its position up to a defined decimal precision ('[redacted-email]'): "After processing, spectra are converted to documents. For this, every peak is represented by a word that contains its position up to a defined decimal precision ("[redacted-email]")"
- [methods] In addition to all peaks of a spectrum, neutral losses between 5.0 and 200.0 Da were added as '[redacted-email]'. Neutral losses are calculated as precursor − peak: "In addition to all peaks of a spectrum, neutral losses between 5.0 and 200.0 Da were added as "[redacted-email]". Neutral losses are calculated as precursor − peak"
- [other] convert all spectra to documents by representing peaks as '[redacted-email]' words (binning 2 decimals) and adding neutral losses (5.0–200.0 Da) as '[redacted-email]' words: "convert all spectra to documents by representing peaks as '[redacted-email]' words (binning 2 decimals) and adding neutral losses (5.0–200.0 Da) as '[redacted-email]' words"
- [other] compute all-pairs spectrum vector similarities using weighted sum of word embeddings (weight = normalized intensity, sqrt applied): "compute all-pairs spectrum vector similarities using weighted sum of word embeddings (weight = normalized intensity, sqrt applied)"
- [methods] the maximum number of kept peaks per spectrum was set to scale linearly with the estimated parent mass: max(n_peaks) = 0.5 × parentmass: "the maximum number of kept peaks per spectrum was set to scale linearly with the estimated parent mass: max(n_peaks) = 0.5 × parentmass"
- [discussion] one limitation of Spec2Vec as compared to cosine scores is that it needs training data to learn the fragment peak relationships: "one limitation of Spec2Vec as compared to cosine scores is that it needs training data to learn the fragment peak relationships"
- [discussion] For GC-MS, neutral losses are usually not measured.: "For GC-MS, neutral losses are usually not measured."
