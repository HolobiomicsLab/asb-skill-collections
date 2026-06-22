---
name: mass-spectrometry-spectrum-tokenization
description: Use when you have pre-processed MS/MS spectra and need to prepare them for word-embedding-based similarity methods (e.g., Spec2Vec).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0226
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - gensim
  - matchms
  - Numba
  - Pandas
  - spec2vec
  - Word2Vec (gensim)
  - NumPy/Pandas
derived_from:
- doi: 10.1371/journal.pcbi.1008724
  title: Spec2Vec
evidence_spans:
- A Word2Vec [22] model is trained on all documents of a chosen dataset using gensim [37]
- the implementations for the cosine score and the modified cosine score used can be found in the Python package matchms
- the implementations for the cosine score and the modified cosine score used can be found in the Python package matchms [31] (https://github.com/matchms/matchms)
- making extensive use of Numpy [24] and Numba [25]
- by making extensive use of Numpy [24] and Numba [25], the library
- Spec2Vec was optimised by making extensive use of Numpy [24] and Numba [25], the library matching was implemented using Pandas [40]
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

# mass-spectrometry-spectrum-tokenization

## Summary

Convert pre-processed MS/MS spectra into tokenized documents by representing each peak and neutral loss as discrete words, enabling downstream embedding and similarity computation. This is a prerequisite step for learning spectral relationships via Word2Vec-based models like Spec2Vec.

## When to use

Apply this skill when you have pre-processed MS/MS spectra and need to prepare them for word-embedding-based similarity methods (e.g., Spec2Vec). Specifically, use this before training or applying a Word2Vec model to learn relationships between fragment ions and neutral losses, or when you want to represent spectra in a format that captures peak co-occurrence patterns rather than raw intensity profiles.

## When NOT to use

- Input spectra have fewer than 10 fragment peaks — these are below the quality threshold used in Spec2Vec training and will be filtered anyway.
- You are performing similarity scoring on GC-MS data, where neutral losses are typically not measured and Spec2Vec performance has not been validated.
- You need real-time or interactive spectrum annotation — tokenization is a batch preprocessing step, not suitable for live lookups.

## Inputs

- Pre-processed MS/MS spectra (with metadata including precursor m/z)
- Spectrum peak lists (m/z and intensity values)
- Reference Word2Vec model vocabulary (optional, for missing fraction filtering)
- Precursor m/z values for each spectrum

## Outputs

- Tokenized spectrum documents (list of '[redacted-email]' and '[redacted-email]' tokens per spectrum)
- Spectrum identifier to token mapping
- Missing fraction values per spectrum
- Filtered spectrum set (spectra with missing_fraction < 0.05)

## How to apply

For each MS/MS spectrum, represent every peak as a word token using the format '[redacted-email]', where xxx.xx is the m/z value binned to 2 decimal places. Compute neutral losses as precursor m/z minus each peak m/z, keeping only losses in the range 5.0–200.0 Da, and represent each as '[redacted-email]'. Assemble all peak and loss tokens into a single spectrum document. Calculate the missing fraction (the proportion of total peak intensity from peaks/losses not present in the reference Word2Vec vocabulary) and filter out spectra with missing_fraction ≥ 0.05 to ensure sufficient feature overlap with the learned model. Weight each token by the square root of its normalized peak intensity when aggregating into spectrum vectors. Store the resulting tokenized documents and spectrum identifiers for downstream embedding and similarity computations.

## Related tools

- **matchms** (Spectrum import, cleaning, metadata extraction, and tokenization support) — https://github.com/matchms/matchms
- **spec2vec** (Tokenization and spectrum-to-vector conversion using pre-trained Word2Vec embeddings) — https://github.com/iomega/spec2vec
- **Word2Vec (gensim)** (Training embeddings for peak and loss tokens; inference on token sequences)
- **NumPy/Pandas** (Numerical operations for peak intensity normalization and token weighting)

## Examples

```
from spec2vec import SpectrumDocument; from matchms.importing_utils import load_from_mgf; spectra = list(load_from_mgf('spectra.mgf')); spectrum_docs = [SpectrumDocument(spectrum) for spectrum in spectra]; vectors = [spectrum.get_vector() for spectrum in spectrum_docs]
```

## Evaluation signals

- Every spectrum document contains only valid token formats ('peak@' or 'loss@' followed by numeric m/z values to 2 decimal places)
- Neutral loss values fall within the defined range [5.0, 200.0] Da for all loss tokens
- Missing fraction calculation correctly identifies the weighted proportion of spectrum intensity not covered by the Word2Vec vocabulary; verify against ground-truth manual annotation on a small sample
- Filtered spectrum set contains no spectra with missing_fraction ≥ 0.05 and no spectra with fewer than 10 peaks
- Token weights (square root of normalized intensity) are non-negative and sum to ≤ 1.0 per spectrum (after normalization)

## Limitations

- Spec2Vec requires pre-trained Word2Vec models covering the fragment and loss space of the target spectra; models trained on one dataset may have poor feature overlap with spectra from different ionization modes or mass spectrometry platforms, potentially requiring model retraining.
- The method has been validated only on LC-MS spectra in positive ionization mode; GC-MS data are not suitable because neutral losses are usually not measured in GC-MS.
- Tokenization introduces a hard m/z binning at 2 decimal precision, which may lose resolution for very high-mass fragments or spectra acquired at high mass accuracy.
- Spectra with fewer than 10 peaks are automatically excluded, limiting applicability to low-complexity spectra or low-abundance compounds.

## Evidence

- [other] For each spectrum, represent every peak as a word in the form '[redacted-email]' using 2-decimal binning of m/z values. Calculate neutral losses (precursor m/z minus peak m/z) for all losses between 5.0 and 200.0 Da and represent each as '[redacted-email]'.: "For each spectrum, represent every peak as a word in the form '[redacted-email]' using 2-decimal binning of m/z values. Calculate neutral losses (precursor m/z minus peak m/z) for all losses between 5.0"
- [other] Assemble all peak and loss words into a spectrum document. For each spectrum, compute a weighted spectrum vector as the sum of Word2Vec word embeddings, weighted by the square root of normalized peak intensity.: "Assemble all peak and loss words into a spectrum document. For each spectrum, compute a weighted spectrum vector as the sum of Word2Vec word embeddings, weighted by the square root of normalized peak"
- [other] Calculate the missing fraction (proportion of spectrum intensity from unknown peaks/losses not in Word2Vec model); filter out spectra with missing fraction ≥0.05.: "Calculate the missing fraction (proportion of spectrum intensity from unknown peaks/losses not in Word2Vec model); filter out spectra with missing fraction ≥0.05."
- [methods] After processing, spectra are converted to documents. For this, every peak is represented by a word that contains its position up to a defined decimal precision ("[redacted-email]"): "After processing, spectra are converted to documents. For this, every peak is represented by a word that contains its position up to a defined decimal precision ("[redacted-email]")"
- [methods] In addition to all peaks of a spectrum, neutral losses between 5.0 and 200.0 Da were added as "[redacted-email]". Neutral losses are calculated as precursor − peak: "In addition to all peaks of a spectrum, neutral losses between 5.0 and 200.0 Da were added as "[redacted-email]". Neutral losses are calculated as precursor − peak"
- [discussion] In the present work, we have only demonstrated performance on LC-MS data and not yet assessed Spec2Vec for GC-MS data. For GC-MS, neutral losses are usually not measured.: "In the present work, we have only demonstrated performance on LC-MS data and not yet assessed Spec2Vec for GC-MS data. For GC-MS, neutral losses are usually not measured."
- [readme] spec2vec does so for mass fragments and neutral losses in MS/MS spectra. The spectral similarity score is based on spectral embeddings learnt from the fragmental relationships within a large set of spectral data.: "spec2vec does so for mass fragments and neutral losses in MS/MS spectra. The spectral similarity score is based on spectral embeddings learnt from the fragmental relationships within a large set of"
