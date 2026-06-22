---
name: spectral-vector-normalization-by-intensity
description: Use when when converting pre-processed MS/MS spectra into fixed-length vector representations using Word2Vec embeddings for Spec2Vec similarity scoring. Specifically, apply this skill after you have represented individual peaks and neutral losses as words ('[redacted-email]', 'loss@xxx.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
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
  - tandem-MS
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

# spectral-vector-normalization-by-intensity

## Summary

Normalize fragment ion intensities in MS/MS spectra before converting them to document vectors for Word2Vec embedding. This intensity weighting ensures that the spectral embedding reflects the relative importance of fragment peaks and improves the fidelity of spectral similarity scoring based on learned structural relationships.

## When to use

When converting pre-processed MS/MS spectra into fixed-length vector representations using Word2Vec embeddings for Spec2Vec similarity scoring. Specifically, apply this skill after you have represented individual peaks and neutral losses as words ('[redacted-email]', '[redacted-email]') and are ready to aggregate their embeddings into a single spectrum vector; intensity normalization is essential to weight common fragments appropriately and avoid over-representation of low-abundance noise peaks.

## When NOT to use

- When input spectra have fewer than 10 fragment peaks—these should be filtered before vector normalization
- When comparing spectra across different ionization modes or instrumental platforms without retraining the Word2Vec model on data with sufficient feature overlap
- When applying to GC-MS data where neutral losses are typically not measured and Word2Vec models have not been trained on GC-MS fragmentation patterns

## Inputs

- Pre-processed MS/MS spectrum with peak m/z and intensity values
- Precursor m/z (for neutral loss calculation)
- Trained Word2Vec model with peak and loss embeddings
- Peak representation words ('[redacted-email]') and loss representation words ('[redacted-email]')

## Outputs

- Fixed-length spectrum vector (weighted sum of Word2Vec embeddings)
- Missing fraction estimate (proportion of spectrum intensity from unknown peaks/losses)
- Filtered spectrum indicator (boolean: true if missing fraction < 0.05)

## How to apply

For each peak in a spectrum, normalize its intensity by dividing by the maximum intensity in that spectrum, then apply the square root of this normalized intensity as the weight when summing Word2Vec word embeddings. The square root transformation prevents extremely intense peaks from dominating the vector sum while still preserving the relative intensity hierarchy. Filter out spectra with high missing fractions (proportion of total spectrum intensity from peaks/losses not found in the trained Word2Vec model; threshold ≥0.05) to avoid low-quality embeddings. This weighted aggregation produces a single spectrum vector where both fragment identity (via embeddings) and relative abundance (via intensity weights) contribute to the final representation suitable for efficient similarity comparisons.

## Related tools

- **Word2Vec** (provides pre-trained embeddings for peak and loss words that are weighted and aggregated by normalized intensities)
- **gensim** (library containing Word2Vec model implementation and word embedding lookups)
- **spec2vec** (implements the weighted spectrum vector aggregation step using intensity-normalized embeddings) — https://github.com/iomega/spec2vec
- **matchms** (provides utilities for spectrum preprocessing, peak filtering, and metadata handling before vector normalization) — https://github.com/matchms/matchms
- **Numpy** (efficient array operations for intensity normalization and vector aggregation)

## Examples

```
from spec2vec import SpectrumDocument; import gensim; model = gensim.models.Word2Vec.load('pretrained_model.w2v'); documents = [SpectrumDocument(spectrum=s, intensity_weighting_power=0.5) for s in spectra]; spectrum_vectors = [model.infer_vector(doc.words, epochs=10) for doc in documents]
```

## Evaluation signals

- Verify that spectrum vectors have consistent dimensionality matching the Word2Vec embedding size (e.g., 100 or 300 dimensions)
- Check that normalized intensities fall in the range [0, 1] before taking square root, producing weights in [0, 1]
- Confirm that spectra with missing fraction ≥0.05 are excluded from downstream similarity calculations
- Validate that resulting spectrum vectors preserve the relative abundance relationships by comparing vector magnitude changes with original peak intensity distributions
- Ensure that the sum of weighted embeddings is numerically stable and does not produce NaN or infinite values

## Limitations

- Requires a pre-trained Word2Vec model; if the model was trained on a different spectrum dataset or ionization mode with limited feature overlap, some peaks may be unknown, reducing vector quality.
- The square root intensity weighting is empirically motivated but the paper does not provide ablation studies comparing alternative weighting schemes (e.g., linear, log, or no weighting).
- Not suitable for GC-MS data where neutral losses are typically not measured; the method is validated only on LC-MS/MS spectra.
- Missing fraction threshold (0.05) is a fixed cutoff; spectra near this boundary may have borderline reliability and could benefit from dataset-specific tuning.
- The method assumes that peak intensity relative to the maximum is a reliable proxy for fragment abundance; this may not hold for all instrumental conditions or sample preparation methods.

## Evidence

- [methods] weighted spectrum vector as the sum of Word2Vec word embeddings, weighted by the square root of normalized peak intensity: "compute a weighted spectrum vector as the sum of Word2Vec word embeddings, weighted by the square root of normalized peak intensity"
- [methods] missing fraction (proportion of spectrum intensity from unknown peaks/losses not in Word2Vec model): "Calculate the missing fraction (proportion of spectrum intensity from unknown peaks/losses not in Word2Vec model); filter out spectra with missing fraction ≥0.05"
- [methods] Spec2Vec converts spectra into documents by representing each peak as a word and neutral losses between 5.0–200.0 Da, then computes vectors as weighted sums: "For each spectrum, compute a weighted spectrum vector as the sum of Word2Vec word embeddings, weighted by the square root of normalized peak intensity"
- [methods] Word2Vec model provides embeddings that Spec2Vec aggregates into spectrum vectors: "Assemble all peak and loss words into a spectrum document. 5. For each spectrum, compute a weighted spectrum vector as the sum of Word2Vec word embeddings"
- [methods] setting a threshold for the missing fraction can avoid returning Spec2Vec similarity scores for spectra far outside the learned peaks and losses: "By setting a threshold for the missing fraction (e.g. <0.05), returning Spec2Vec similarity scores for spectra far outside the learned peaks (and losses) can be avoided"
