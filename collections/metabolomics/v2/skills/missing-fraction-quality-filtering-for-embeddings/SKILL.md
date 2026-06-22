---
name: missing-fraction-quality-filtering-for-embeddings
description: Use when after converting MS/MS spectra to fixed-length vector representations using a pre-trained Word2Vec model (as in Spec2Vec), filter spectra before computing similarity scores to flag those where a large fraction of the observed intensity comes from peaks or neutral losses not present in the.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3520
  tools:
  - gensim
  - matchms
  - Numba
  - Pandas
  - Spec2Vec
  - Word2Vec (gensim)
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

# missing-fraction-quality-filtering-for-embeddings

## Summary

Filter out spectra whose peak and neutral loss composition is poorly represented in a pre-trained Word2Vec embedding model, thereby avoiding unreliable spectral similarity scores for spectra with unknown fragments. This quality gate prevents downstream false positives in spectral matching and molecular networking.

## When to use

After converting MS/MS spectra to fixed-length vector representations using a pre-trained Word2Vec model (as in Spec2Vec), filter spectra before computing similarity scores to flag those where a large fraction of the observed intensity comes from peaks or neutral losses not present in the model's vocabulary. This is especially important when applying a model trained on one dataset (e.g., UniqueInchikey) to spectra from a different experimental source or ionization mode.

## When NOT to use

- When using cosine or modified cosine similarity scores, which do not rely on learned embeddings and are not affected by vocabulary coverage (missing fraction filtering is Spec2Vec-specific).
- When all spectra in your input are from the same dataset used to train the Word2Vec model; retraining on that exact data should eliminate most missing fractions, making this filter redundant.
- When you intentionally want to include out-of-vocabulary spectra for downstream exploration or retraining purposes (e.g., discovering novel fragment types).

## Inputs

- Pre-trained Word2Vec model (gensim format)
- Pre-processed MS/MS spectra (matched to Word2Vec vocabulary as peak@m/z and loss@m/z words)
- Spectrum metadata including precursor m/z and peak intensity array
- Weighted spectrum vectors (computed as sum of Word2Vec embeddings scaled by square-root-normalized peak intensities)

## Outputs

- Filtered spectrum vector set (subset passing missing fraction threshold)
- Spectrum identifiers and their corresponding missing fraction values
- Quality report summarizing count and percentage of spectra removed by missing fraction threshold

## How to apply

For each spectrum converted to a weighted vector embedding, calculate the missing fraction as the sum of intensities of peaks and neutral losses absent from the Word2Vec vocabulary, divided by the total spectrum intensity. Apply a threshold (e.g., <0.05 or <5%) to exclude spectra where the missing fraction exceeds this cutoff. This ensures that the spectrum's embedding captures a representative sample of its fragmentation pattern and reduces the risk of spurious similarity matches driven by unmeasured or out-of-vocabulary fragments. The rationale is that spectra with large missing fractions are poorly constrained by the learned embedding space and should not be trusted for downstream molecular networking or library matching tasks without explicit acknowledgment of this limitation.

## Related tools

- **Spec2Vec** (Implements missing fraction calculation and filtering during spectrum vector computation; provides method to assess coverage of spectrum's intensity by known peaks/losses) — https://github.com/iomega/spec2vec
- **Word2Vec (gensim)** (Provides the learned vocabulary of peak and loss words; missing fraction is calculated by checking which peaks/losses are absent from this vocabulary)
- **matchms** (Provides spectrum import, preprocessing (peak filtering, normalization), and metadata handling prior to missing fraction assessment) — https://github.com/matchms/matchms

## Examples

```
from spec2vec import SpectrumDocument; filtered_spectra = [s for s in spectra if calculate_missing_fraction(s, model) < 0.05]; similarity_scores = spec2vec.score(filtered_spectra, reference_spectra)
```

## Evaluation signals

- Verify that spectra passing the filter have missing fraction values ≤ the specified threshold (e.g., ≤0.05); inspect histogram of missing fractions before and after filtering.
- Check that the fraction of spectra removed is reasonable for the given dataset and model; sudden jumps in removal rate may indicate model–data mismatch.
- Confirm that Spec2Vec similarity scores computed on filtered spectra show stronger correlation with structural similarity (InChIKey matches) compared to unfiltered scores, as reported in the paper.
- Validate that downstream molecular network clustering or library matching results show fewer spurious high-confidence matches (reduced false positive rate) after filtering.
- Ensure that spectrum count and quality report output match the input spectrum count minus the number of filtered spectra.

## Limitations

- Missing fraction filtering is applicable only to learned embedding methods like Spec2Vec; it does not apply to cosine-based scores.
- The threshold value (e.g., <0.05) is heuristic and may require tuning depending on the training data size and feature diversity. Models trained on larger, more diverse datasets may tolerate higher missing fractions.
- If a model is pre-trained on a limited dataset (e.g., LC-MS only), applying it to a different modality (e.g., GC-MS) may result in high missing fractions and many filtered spectra, limiting the method's utility without retraining.
- The method assumes that peak intensities are normalized and that the Word2Vec model was trained on spectra with similar preprocessing; systematic differences in peak intensity calibration between training and query data can distort missing fraction estimates.
- Spectra with very few peaks (e.g., <10 fragments) may have artificially low missing fractions if all observed peaks happen to be in the vocabulary, even though the spectrum carries little information for structural discrimination.

## Evidence

- [methods] By setting a threshold for the missing fraction (e.g. <0.05), returning Spec2Vec similarity scores for spectra far outside the learned peaks (and losses) can be avoided: "By setting a threshold for the missing fraction (e.g. <0.05), returning Spec2Vec similarity scores for spectra far outside the learned peaks (and losses) can be avoided"
- [other] Calculate the missing fraction (proportion of spectrum intensity from unknown peaks/losses not in Word2Vec model); filter out spectra with missing fraction ≥0.05: "Calculate the missing fraction (proportion of spectrum intensity from unknown peaks/losses not in Word2Vec model); filter out spectra with missing fraction ≥0.05"
- [methods] In those instances some words (= peaks) of a given spectra might be unknown to the model. In those instances we can estimate the impact of the missing words by assessing the uncovered weighted part: "In those instances some words (= peaks) of a given spectra might be unknown to the model. In those instances we can estimate the impact of the missing words by assessing the uncovered weighted part"
- [abstract] Spec2Vec is computationally more scalable allowing structural analogue searches in large databases within seconds: "Spec2Vec is computationally more scalable allowing structural analogue searches in large databases within seconds"
- [discussion] one limitation of Spec2Vec as compared to cosine scores is that it needs training data to learn the fragment peak relationships: "one limitation of Spec2Vec as compared to cosine scores is that it needs training data to learn the fragment peak relationships"
