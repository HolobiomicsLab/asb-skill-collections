---
name: word2vec-vocabulary-matching-and-unknown-peak-handling
description: Use when converting MS/MS spectra into Spec2Vec embeddings using a pre-trained Word2Vec model that was trained on reference data (e.g., a subset of GNPS or MassBank).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3628
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - Word2Vec
  - gensim
  - matchms
  - Numba
  - Pandas
  - Word2Vec (gensim)
  - spec2vec
  - Numpy, Pandas
  techniques:
  - LC-MS
  - GC-MS
derived_from:
- doi: 10.1371/journal.pcbi.1008724
  title: Spec2Vec
evidence_spans:
- inspired by a natural language processing algorithm—Word2Vec
- A Word2Vec [22] model is trained on all documents of a chosen dataset using gensim [37]
- the implementations for the cosine score and the modified cosine score used can be found in the Python package matchms
- the implementations for the cosine score and the modified cosine score used can be found in the Python package matchms [31] (https://github.com/matchms/matchms)
- making extensive use of Numpy [24] and Numba [25]
- by making extensive use of Numpy [24] and Numba [25], the library
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

# Word2Vec Vocabulary Matching and Unknown Peak Handling

## Summary

This skill detects and quantifies spectral peaks and neutral losses that fall outside a trained Word2Vec model's vocabulary, then filters spectra to exclude those with excessive unknown features. By computing a 'missing fraction' (the proportion of total spectral intensity from unmapped peaks/losses), this approach ensures that only spectra with sufficient feature overlap are scored, avoiding unreliable Spec2Vec similarity estimates on out-of-distribution data.

## When to use

Apply this skill when converting MS/MS spectra into Spec2Vec embeddings using a pre-trained Word2Vec model that was trained on reference data (e.g., a subset of GNPS or MassBank). You must use it whenever your query or library spectra may contain fragment ions or neutral losses not seen during Word2Vec training—particularly when working with novel chemical structures, different ionization modes, or instrumental platforms that were not well-represented in the training corpus.

## When NOT to use

- Input spectra were already used to train the Word2Vec model (risk of data leakage and inflated coverage statistics)
- You require similarity scores for spectra with fragmentation patterns substantially different from training data (e.g., GC-MS data when model was trained only on LC-MS; the method will filter out most or all spectra)
- You are working with cosine or modified cosine similarity (those methods do not depend on vocabulary matching and should not be filtered by this skill)

## Inputs

- Pre-processed MS/MS spectrum collection (matchms Spectrum objects or equivalent, with precursor m/z and normalized peak intensity)
- Pre-trained Word2Vec model (gensim model file, trained on reference spectra)

## Outputs

- Filtered spectrum set (same format as input, with low-coverage spectra removed)
- Missing fraction value per spectrum (float in [0, 1])
- Spectrum vectors computed only from known Word2Vec vocabulary (vector per spectrum)

## How to apply

For each spectrum in your dataset: (1) Convert all peak m/z values to words ('[redacted-email]' with 2-decimal precision) and compute neutral losses (precursor m/z minus each peak m/z, for losses between 5.0–200.0 Da) as words ('[redacted-email]'). (2) Query the trained Word2Vec model to identify which peaks and losses are present in its vocabulary and which are unknown. (3) Sum the intensity-weighted components (√intensity × embedding) for all known words; sum the √intensity for all unknown words. (4) Calculate missing fraction = (sum of unknown intensities) / (sum of all intensities). (5) Filter out spectra where missing fraction ≥ 0.05 (or your chosen threshold). (6) For retained spectra, compute Spec2Vec similarity only on the known vocabulary subset. This filtering step prevents high-confidence but potentially spurious similarity scores on spectra far outside the model's training distribution.

## Related tools

- **Word2Vec (gensim)** (Trained embedding model that provides word (peak/loss) vectors; queried to identify in-vocabulary and unknown spectrum features)
- **spec2vec** (Orchestrates spectrum-to-document conversion, vocabulary lookup, and missing fraction calculation; filters spectra before scoring) — https://github.com/iomega/spec2vec
- **matchms** (Loads, pre-processes, and normalizes MS/MS spectra; provides Spectrum object interface for peak and metadata access) — https://github.com/matchms/matchms
- **Numpy, Pandas** (Numerical aggregation and filtering of intensity sums and missing fractions)

## Evaluation signals

- All retained spectra have missing_fraction < threshold (e.g., < 0.05); check histogram of missing fractions across dataset
- Spectrum vectors are non-zero and have expected dimensionality (equal to Word2Vec embedding size); verify shape and non-null counts
- Filtered spectrum count and total intensity coverage are reasonable (e.g., 90–95% of spectra and intensity retained if threshold is 0.05); compare pre- and post-filter summary statistics
- Spec2Vec similarity scores on filtered spectra show stronger correlation with structural similarity (InChIKey-based ground truth) than unfiltered spectra; compute Kendall τ or ROC-AUC vs. structural ground truth
- Spectra with high missing fractions (e.g., > 0.1) are reproducibly excluded; verify via manual inspection of removed spectrum metadata

## Limitations

- Method is sensitive to the choice of missing_fraction threshold (0.05 recommended in the paper, but lower thresholds remove more spectra, higher thresholds allow noisier embeddings). No principled way to set this threshold without domain knowledge or validation data.
- If the Word2Vec model is trained on a narrow or biased subset of spectra (e.g., only alkaloid structures), the method may over-filter spectra from underrepresented chemical classes, leading to missing similarity matches.
- Unknown peaks not in the model contribute zero vector to the final embedding, effectively losing chemical information. Spectra with many unknown features (but missing_fraction < threshold) will have lower-quality embeddings.
- Method is demonstrated only on LC-MS positive ionization mode data. GC-MS and negative ionization modes were not assessed; neutral losses are often unmeasured in GC-MS, making the method inapplicable without retraining on GC-MS-specific models.
- Requires retraining or at minimum re-assessment of missing_fraction when applied to experimental spectra from instruments or chemical spaces substantially different from the training corpus.

## Evidence

- [methods] In those instances some words (= peaks) of a given spectra might be unknown to the model. In those instances we can estimate the impact of the missing words by assessing the uncovered weighted part: "In those instances some words (= peaks) of a given spectra might be unknown to the model. In those instances we can estimate the impact of the missing words by assessing the uncovered weighted part"
- [methods] By setting a threshold for the missing fraction (e.g. <0.05), returning Spec2Vec similarity scores for spectra far outside the learned peaks (and losses) can be avoided: "By setting a threshold for the missing fraction (e.g. <0.05), returning Spec2Vec similarity scores for spectra far outside the learned peaks (and losses) can be avoided"
- [other] Calculate neutral losses (precursor m/z minus peak m/z) for all losses between 5.0 and 200.0 Da and represent each as '[redacted-email]': "Calculate neutral losses (precursor m/z minus peak m/z) for all losses between 5.0 and 200.0 Da and represent each as '[redacted-email]'"
- [other] For each spectrum, compute a weighted spectrum vector as the sum of Word2Vec word embeddings, weighted by the square root of normalized peak intensity: "For each spectrum, compute a weighted spectrum vector as the sum of Word2Vec word embeddings, weighted by the square root of normalized peak intensity"
- [discussion] one limitation of Spec2Vec as compared to cosine scores is that it needs training data to learn the fragment peak relationships: "one limitation of Spec2Vec as compared to cosine scores is that it needs training data to learn the fragment peak relationships"
- [discussion] In the present work, we have only demonstrated performance on LC-MS data and not yet assessed Spec2Vec for GC-MS data. For GC-MS, neutral losses are usually not measured.: "In the present work, we have only demonstrated performance on LC-MS data and not yet assessed Spec2Vec for GC-MS data. For GC-MS, neutral losses are usually not measured."
