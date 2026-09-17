---
name: mass-spectrometry-library-matching
description: Use when when you have an unknown MS/MS spectrum (with ≥10 peaks, precursor
  m/z, and at least 5 fragment ions) and need to identify it by comparing against
  a curated spectral library with annotated InChIKeys or chemical structures.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3647
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3172
  tools:
  - matchms
  - gensim
  - Numba
  - Pandas
  - scipy
  - Spec2Vec
  - Word2Vec (gensim)
  - NumPy, SciPy
  techniques:
  - LC-MS
  - GC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1371/journal.pcbi.1008724
  title: Spec2Vec
evidence_spans:
- the implementations for the cosine score and the modified cosine score used can
  be found in the Python package matchms
- the implementations for the cosine score and the modified cosine score used can
  be found in the Python package matchms [31] (https://github.com/matchms/matchms)
- A Word2Vec [22] model is trained on all documents of a chosen dataset using gensim
  [37]
- making extensive use of Numpy [24] and Numba [25]
- by making extensive use of Numpy [24] and Numba [25], the library
- Spec2Vec was optimised by making extensive use of Numpy [24] and Numba [25], the
  library matching was implemented using Pandas [40]
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

# mass-spectrometry-library-matching

## Summary

Library matching is the task of ranking unknown MS/MS spectra against a spectral database to identify chemical structures. This skill applies similarity scoring (cosine, modified cosine, or Spec2Vec) to assign candidate compounds ranked by score, controlled by threshold and minimum-peak-count criteria.

## When to use

When you have an unknown MS/MS spectrum (with ≥10 peaks, precursor m/z, and at least 5 fragment ions) and need to identify it by comparing against a curated spectral library with annotated InChIKeys or chemical structures. Use this skill when library-based annotation is preferred over in-silico prediction, or when you need to benchmark or validate the true-positive and false-positive rates of spectral similarity methods.

## When NOT to use

- Input spectra have fewer than 10 fragment peaks after filtering; insufficient spectral information for reliable matching.
- Library is primarily GC-MS data; Spec2Vec was only demonstrated on LC-MS where neutral losses are reliably measured.
- Query spectra contain fragment ions (m/z values) with poor feature overlap to the Word2Vec training set; Spec2Vec may require retraining on new experimental data.
- Unknown precursor m/z is unavailable; cannot pre-select candidates using 1 ppm mass tolerance.

## Inputs

- Unknown MS/MS spectrum (with metadata: precursor m/z, charge state, ionization mode)
- Spectral library with ≥1000 reference spectra (InChIKey annotated, mzML/mzXML/mgf/msp format)
- Pre-trained Word2Vec model (if using Spec2Vec scoring)
- Similarity scoring method selection: cosine, modified cosine, or Spec2Vec

## Outputs

- Ranked list of candidate library spectra with similarity scores (descending order)
- Classification of each hit as true positive or false positive (based on InChIKey match)
- Receiver-operator-characteristic curve (true-positive rate vs. false-positive rate)
- Performance metrics: area-under-curve, accuracy at selected thresholds

## How to apply

Prepare the unknown spectrum and library spectra by removing peaks with m/z outside [0, 1000] and discarding spectra with fewer than 10 peaks. For cosine or modified cosine scoring, filter peaks with relative intensity <0.01 of the highest peak and require ≥6 matching peaks (cosine) or ≥10 matching peaks (modified cosine) with m/z tolerance 0.005. For Spec2Vec, convert each spectrum into a document of peak words (format: '[redacted-email]') and neutral losses ('[redacted-email]', for masses 5.0–200.0 Da), then apply the learned Word2Vec model. Pre-select candidate matches using precursor m/z matching with 1 ppm tolerance to reduce search space. Rank library spectra by descending similarity score. Classify hits as true positives if the InChIKey matches the query within the first 14 characters (planar structure); otherwise classify as false positives. Report true-positive rate, false-positive rate, and area-under-curve at each score threshold to construct receiver-operator-characteristic curves.

## Related tools

- **matchms** (Provides cosine and modified cosine similarity scoring implementations, spectrum I/O, peak filtering, and metadata validation) — https://github.com/matchms/matchms
- **Spec2Vec** (Computes learned spectral embeddings via Word2Vec to generate similarity scores that correlate better with structural similarity than cosine-based methods) — https://github.com/iomega/spec2vec
- **Word2Vec (gensim)** (Trains and loads the embedding model that maps peaks and neutral losses to learned vector representations for Spec2Vec scoring)
- **Pandas** (Manages spectral metadata (InChIKey, m/z, intensity), formats rankings, and computes performance metrics)
- **NumPy, SciPy** (Performs similarity matrix computation, ROC curve generation, and area-under-curve calculation)

## Examples

```
from matchms.importing import load_from_mgf
from matchms.processing import default_filters
from matchms.similarity import CosineGreedy, ModifiedCosine
from spec2vec import Spec2Vec
from gensim.models import Word2Vec

# Load and process library spectra
library = [default_filters(s) for s in load_from_mgf('library.mgf')]
query = default_filters(load_from_mgf('unknown.mgf')[0])

# Load pre-trained Word2Vec model
model = Word2Vec.load('word2vec_model.bin')
spec2vec = Spec2Vec(model=model)

# Compute scores and rank
scores = [spec2vec.pair(query, lib_spec) for lib_spec in library]
rankings = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
print(f'Top match: library[{rankings[0][0]}] with score {rankings[0][1]:.3f}')
```

## Evaluation signals

- Output ranking list contains only library spectra with valid similarity scores (≥0.0, ≤1.0 for cosine-based methods); no NaN or negative scores.
- Pre-selected candidate set size is consistent with 1 ppm precursor m/z tolerance; if N library spectra match the unknown m/z within 1 ppm, only those N candidates should have computed scores.
- True-positive and false-positive classifications are consistent with InChIKey matching rule: planar InChIKey (first 14 characters) match → true positive; mismatch → false positive.
- ROC curve monotonically increases: true-positive rate is non-decreasing as false-positive rate increases across score thresholds.
- Spec2Vec area-under-curve (≤0.88 on AllPositive dataset) exceeds cosine and modified cosine area-under-curve values, confirming improved structural correlation.
- Minimum-peak-count constraint is enforced: no match with fewer than specified peaks (6 for cosine, 10 for modified cosine) is scored or ranked.

## Limitations

- Spec2Vec requires a Word2Vec model pre-trained on a large spectral dataset with substantial feature overlap to the query spectra; unknown peaks outside the training set will reduce score reliability, and retraining on domain-specific data may be necessary.
- Cosine and modified cosine methods exhibit high false-positive rates when comparing spectra of molecules with high structural similarity but differing in multiple locations, reducing utility for analogue searching.
- Spec2Vec performance has only been validated on LC-MS data with reliable neutral loss measurement; GC-MS data (where neutral losses are typically absent) has not been assessed.
- Library matching is fundamentally limited by database completeness: compounds absent from the reference library cannot be identified, even with perfect scoring.
- The 1 ppm precursor m/z tolerance for candidate pre-selection assumes high-resolution mass spectrometry; lower-resolution instruments may have insufficient selectivity.

## Evidence

- [other] Spec2Vec resulted in a notably better true/false positive ratio at all thresholds compared to cosine and modified cosine scores during library matching, achieving up to 88% accuracy and higher retrieval rates.: "Spec2Vec resulted in a notably better true/false positive ratio at all thresholds compared to cosine and modified cosine scores during library matching, achieving up to 88% accuracy"
- [other] For cosine and modified cosine scoring, apply peak filtering by ignoring peaks with relative intensities <0.01; for Spec2Vec, apply parent-mass-scaled peak filtering (max_peaks = 0.5 × parentmass).: "For cosine and modified cosine scoring, apply peak filtering by ignoring peaks with relative intensities <0.01 compared to the highest intensity peak; for Spec2Vec, apply parent-mass-scaled peak"
- [other] Pre-select potentially matching spectra using precursor m/z matching with 1 ppm tolerance.: "Pre-select potentially matching spectra using precursor m/z matching with 1 ppm tolerance"
- [other] Compute similarity scores: apply cosine similarity with tolerance 0.005 and minimum matching peaks = 6; apply modified cosine with tolerance 0.005 and minimum matching peaks = 10; apply Spec2Vec similarity using both the 15-epoch and 50-epoch Word2Vec models.: "Compute similarity scores: apply cosine similarity with tolerance 0.005 and minimum matching peaks = 6; apply modified cosine with tolerance 0.005 and minimum matching peaks = 10"
- [other] For each similarity method, rank query spectra against library and classify hits as true positives (matching InChIKey within first 14 characters / planar structure) or false positives (non-matching structure) to construct receiver-operator-characteristic curves.: "For each similarity method, rank query spectra against library and classify hits as true positives (matching InChIKey within first 14 characters / planar structure) or false positives (non-matching"
- [results] high Spec2Vec spectrum similarity score correlates stronger with structural similarity than the cosine or modified cosine scores: "high Spec2Vec spectrum similarity score correlates stronger with structural similarity than the cosine or modified cosine scores"
- [readme] Matchms is a versatile open-source Python package developed for importing, processing, cleaning, and comparing mass spectrometry data (MS/MS).: "Matchms is a versatile open-source Python package developed for importing, processing, cleaning, and comparing mass spectrometry data (MS/MS)"
- [methods] the maximum number of kept peaks per spectrum was set to scale linearly with the estimated parent mass: max(n_peaks) = 0.5 × parentmass: "the maximum number of kept peaks per spectrum was set to scale linearly with the estimated parent mass: max(n_peaks) = 0.5 × parentmass"
- [discussion] In the present work, we have only demonstrated performance on LC-MS data and not yet assessed Spec2Vec for GC-MS data. For GC-MS, neutral losses are usually not measured.: "In the present work, we have only demonstrated performance on LC-MS data and not yet assessed Spec2Vec for GC-MS data. For GC-MS, neutral losses are usually not measured."
- [discussion] one limitation of Spec2Vec as compared to cosine scores is that it needs training data to learn the fragment peak relationships: "one limitation of Spec2Vec as compared to cosine scores is that it needs training data to learn the fragment peak relationships"
