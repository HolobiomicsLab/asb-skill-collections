---
name: word-embedding-aggregation-for-spectral-data
description: Use when when you have pre-processed MS/MS spectra and a pre-trained
  Word2Vec model, and need to compute fast, scalable similarity scores for library
  matching or molecular networking that correlate better with structural similarity
  than cosine-based methods.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - gensim
  - matchms
  - Numba
  - Pandas
  - Word2Vec
  - spec2vec
  - Numpy
  techniques:
  - LC-MS
  - GC-MS
  license_tier: open
derived_from:
- doi: 10.1371/journal.pcbi.1008724
  title: Spec2Vec
evidence_spans:
- A Word2Vec [22] model is trained on all documents of a chosen dataset using gensim
  [37]
- the implementations for the cosine score and the modified cosine score used can
  be found in the Python package matchms
- the implementations for the cosine score and the modified cosine score used can
  be found in the Python package matchms [31] (https://github.com/matchms/matchms)
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

# word-embedding-aggregation-for-spectral-data

## Summary

Convert MS/MS spectra into fixed-length vector representations by aggregating pre-trained Word2Vec embeddings of fragment peaks and neutral losses, weighted by normalized peak intensity. This enables efficient similarity comparisons and structural analogue searches in large spectral databases.

## When to use

When you have pre-processed MS/MS spectra and a pre-trained Word2Vec model, and need to compute fast, scalable similarity scores for library matching or molecular networking that correlate better with structural similarity than cosine-based methods. Use this skill when cosine-based scores underperform on spectra of molecules with high structural similarity but differing in multiple locations.

## When NOT to use

- GC-MS data, where neutral losses are usually not measured and the method has not been demonstrated
- Spectra with missing fractions ≥ 0.05, as similarity scores cannot be reliably computed for spectra far outside the learned feature space
- New experimental spectra with insufficient feature overlap to the training set without first retraining the Word2Vec model on data covering those features

## Inputs

- pre-processed MS/MS spectra (mzML, mzXML, msp, MGF, or JSON format)
- pre-trained Word2Vec model (trained on reference spectral dataset)
- precursor m/z values
- peak m/z values and relative intensities

## Outputs

- spectrum vectors (fixed-length arrays of embedding values, one per spectrum)
- spectrum identifiers and corresponding vector components (CSV or HDF5 format)
- missing fraction values for quality control

## How to apply

For each spectrum, represent every peak as a word in the form '[redacted-email]' using 2-decimal m/z binning, then compute neutral losses (precursor m/z minus peak m/z) for all losses between 5.0–200.0 Da and represent each as '[redacted-email]'. Assemble all peak and loss words into a spectrum document. Compute the weighted spectrum vector as the sum of Word2Vec word embeddings for all peaks and losses, where each embedding is weighted by the square root of normalized peak intensity. Calculate the missing fraction (proportion of spectrum intensity from unknown peaks/losses not in the Word2Vec model) and filter out spectra with missing fraction ≥ 0.05 to avoid returning similarity scores for spectra far outside the learned feature space.

## Related tools

- **Word2Vec** (Pre-trained word embedding model that learns relationships between fragment peaks and neutral losses; provides the vector representations for each '[redacted-email]' and '[redacted-email]' word that are aggregated into spectrum vectors)
- **gensim** (Library for loading and querying the pre-trained Word2Vec model to retrieve embeddings for individual peaks and losses)
- **matchms** (Python package for importing, pre-processing, and cleaning MS/MS spectra from multiple formats (mzML, mzXML, msp, MGF, JSON) before vector aggregation) — https://github.com/matchms/matchms
- **spec2vec** (Reference implementation that applies the word-embedding-aggregation method to compute spectral similarity scores from spectrum vectors) — https://github.com/iomega/spec2vec
- **Numpy** (Numerical computing library used for vector operations and weighted aggregation of embeddings)
- **Pandas** (Data manipulation library for organizing spectrum identifiers and vector components in tabular format (CSV output))

## Evaluation signals

- All spectrum vectors are fixed-length arrays with dimensionality matching the Word2Vec embedding dimension (typically 300)
- Missing fraction calculated for each spectrum should be < 0.05 for included spectra; spectra with missing fraction ≥ 0.05 are correctly filtered
- Spectrum vectors have magnitude-squared values consistent with weighted aggregation of normalized peak intensities (not all zeros or NaN)
- Resulting Spec2Vec similarity scores correlate stronger with structural similarity (quantified by Tanimoto fingerprint similarity) than cosine or modified cosine scores
- Vector output file (CSV or HDF5) contains one row per spectrum with spectrum identifier and complete vector components; no missing or truncated rows

## Limitations

- Requires a pre-trained Word2Vec model; if the model does not cover a large fraction of the fragment peaks and losses in new experimental data, additional retraining may be necessary
- Not demonstrated on GC-MS data due to neutral losses usually not being measured in GC-MS
- Spectra with fewer than 10 fragment peaks should be filtered beforehand, as the method requires sufficient fragmentation information
- Peaks with m/z ratios outside [0, 1000] and peaks with relative intensities < 0.01 of the highest peak should be removed during pre-processing to avoid spurious words
- The method is limited to LC-MS data; performance on other ionization modes or instrument types not yet assessed

## Evidence

- [other] spectrum is then represented as a low-dimensional vector calculated as the weighted sum of all its fragment and loss vectors from a trained Word2Vec model: "the spectrum is then represented as a low-dimensional vector calculated as the weighted sum of all its fragment and loss vectors from a trained Word2Vec model"
- [other] For each spectrum, compute a weighted spectrum vector as the sum of Word2Vec word embeddings, weighted by the square root of normalized peak intensity: "For each spectrum, compute a weighted spectrum vector as the sum of Word2Vec word embeddings, weighted by the square root of normalized peak intensity"
- [other] For each spectrum, represent every peak as a word in the form '[redacted-email]' using 2-decimal binning of m/z values. Calculate neutral losses (precursor m/z minus peak m/z) for all losses between 5.0 and 200.0 Da: "For each spectrum, represent every peak as a word in the form '[redacted-email]' using 2-decimal binning of m/z values. 3. Calculate neutral losses (precursor m/z minus peak m/z) for all losses between"
- [methods] By setting a threshold for the missing fraction (e.g. <0.05), returning Spec2Vec similarity scores for spectra far outside the learned peaks (and losses) can be avoided: "By setting a threshold for the missing fraction (e.g. <0.05), returning Spec2Vec similarity scores for spectra far outside the learned peaks (and losses) can be avoided"
- [methods] the spectrum is converted to a document. For this, every peak is represented by a word that contains its position up to a defined decimal precision ('[redacted-email]'). In addition to all peaks of a spectrum, neutral losses between 5.0 and 200.0 Da were added as '[redacted-email]': "every peak is represented by a word that contains its position up to a defined decimal precision ('[redacted-email]'). In addition to all peaks of a spectrum, neutral losses between 5.0 and 200.0 Da were"
- [discussion] one limitation of Spec2Vec as compared to cosine scores is that it needs training data to learn the fragment peak relationships; however, since this not necessarily needs to be library spectra and in: "one limitation of Spec2Vec as compared to cosine scores is that it needs training data to learn the fragment peak relationships"
- [discussion] For many cases, we expect that a model pre-trained on a large spectra dataset will cover a large enough fraction of the features to work well without the need for additional re-training: "a model pre-trained on a large spectra dataset will cover a large enough fraction of the features to work well without the need for additional re-training"
- [discussion] In the present work, we have only demonstrated performance on LC-MS data and not yet assessed Spec2Vec for GC-MS data. For GC-MS, neutral losses are usually not measured.: "we have only demonstrated performance on LC-MS data and not yet assessed Spec2Vec for GC-MS data. For GC-MS, neutral losses are usually not measured"
