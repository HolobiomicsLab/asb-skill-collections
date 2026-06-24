---
name: peak-intensity-normalization-weighted-aggregation
description: Use when when training Word2Vec embeddings on mass spectra represented
  as peak-word documents, and you need to preserve the quantitative intensity relationships
  between fragments without allowing a single dominant peak to overwhelm the learned
  word associations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Spec2Vec
  - matchms
  - gensim
  - RDKit
  - NumPy
  - Numba
  - Pandas
  - scipy
  techniques:
  - LC-MS
  - GC-MS
  license_tier: open
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
- Tanimoto similarity (Jaccard index) based on daylight-like molecular fingerprints,
  version 2020.03.2, 2048 bits, derived using rdkit
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

# peak-intensity-normalization-weighted-aggregation

## Summary

Normalize peak intensities to maximum = 1.0 per spectrum, then apply square-root weighting during spectral embedding aggregation to preserve intensity information while preventing high-intensity peaks from dominating fragment ion relationships in Word2Vec models. This technique is critical for learning balanced spectral embeddings that correlate structure and fragmentation patterns.

## When to use

When training Word2Vec embeddings on mass spectra represented as peak-word documents, and you need to preserve the quantitative intensity relationships between fragments without allowing a single dominant peak to overwhelm the learned word associations. Essential when building Spec2Vec models where fragment intensity encodes chemical relationship information across a large spectral corpus (>90,000 spectra).

## When NOT to use

- Input spectra are already reduced to presence/absence (binary) — intensity information would be lost; use unweighted token occurrence instead.
- Spectra have inconsistent or unreliable intensity calibration across a dataset — normalization artifacts may propagate; validate intensity data first.
- Goal is to match spectra based on exact fragment masses and NOT incorporate intensity relationships into similarity (e.g., traditional cosine score workflows) — use cosine or modified cosine without intensity weighting.

## Inputs

- Mass spectra with annotated peaks (m/z and intensity pairs)
- Precursor m/z values (for neutral loss calculation)
- Cleaned spectral dataset with ≥10 fragment peaks per spectrum
- Peak intensity range [0, 1] after normalization

## Outputs

- Weighted spectral documents ([redacted-email] and [redacted-email] words with √intensity weights)
- Trained Word2Vec model with fragment ion and neutral loss embeddings
- Embedding vectors (typically 100–300 dimensions) encoding learned spectral relationships

## How to apply

For each spectrum: (1) normalize all peak intensities by dividing by the maximum intensity in that spectrum, so the highest peak = 1.0. (2) Convert each peak to a word token in format '[redacted-email]' (2-decimal m/z binning) and neutral losses to '[redacted-email]' tokens. (3) During Word2Vec training (CBOW or Skip-gram), weight each word occurrence by the square-root of the normalized peak intensity (weight = √normalized_intensity). (4) Use gensim's Word2Vec with window_size=500, negative=5, epochs=15–50 to learn embeddings that capture fragmentation relationships balanced across the intensity spectrum. The square-root transformation prevents intensity-based dominance while retaining relative intensity ordering; it serves as a biological/chemical rationale: fragments with higher relative intensity indicate more probable fragmentation pathways, but that relationship is sublinear rather than linear.

## Related tools

- **gensim** (Word2Vec model training with custom intensity-based word weighting for peak and neutral loss embeddings)
- **Spec2Vec** (Spectral similarity scoring using weighted word embeddings derived from normalized and intensity-weighted spectral documents) — https://github.com/iomega/spec2vec
- **matchms** (Spectral data import, metadata cleaning, and peak filtering prior to intensity normalization and document conversion) — https://github.com/matchms/matchms
- **NumPy** (Vectorized intensity normalization and square-root transformation across all spectra)

## Examples

```
import numpy as np; from gensim.models import Word2Vec; spectra_docs = [['peak@145.50', 'loss@18.01', 'peak@203.75'] for s in spectra]; weights = [[np.sqrt(0.8), np.sqrt(0.6), np.sqrt(1.0)]] * len(spectra_docs); model = Word2Vec(sentences=spectra_docs, window=500, negative=5, epochs=15); similarities = [np.dot(model.wv['peak@145.50'], model.wv['peak@203.75']) for _ in range(1)]
```

## Evaluation signals

- Verify all normalized intensities fall in [0.0, 1.0] with maximum intensity per spectrum = 1.0 (exact equality check).
- Confirm weighted word tokens are generated in correct format '[redacted-email]' (or '[redacted-email]') with weights = √(normalized_intensity) in [0.0, 1.0].
- Check that trained Word2Vec model embeddings capture expected fragmentation relationships: high-intensity fragments should co-occur more frequently in low-dimensional space than low-intensity fragments, and neutral losses should cluster with their corresponding peak m/z values.
- Validate that Spec2Vec similarity scores computed from intensity-weighted embeddings show stronger correlation with structural Tanimoto similarity (≥0.5 Spearman rho at top 0.1% scoring pairs) compared to unweighted or cosine-only baselines.
- Confirm missing-fraction metric (uncovered weighted intensity) is <0.05 threshold, indicating >95% of peak intensity in spectra is represented by words with known embeddings in the trained model.

## Limitations

- Spec2Vec requires training data with sufficient feature coverage (fragments and neutral losses); if a spectrum contains peaks far outside the learned vocabulary, missing-fraction will increase and similarity scores become unreliable (mitigation: apply missing-fraction threshold <0.05 or retrain model on new experimental batches).
- Square-root weighting assumes sublinear relationship between peak intensity and fragmentation importance; this may not hold uniformly across all compound classes or ionization conditions — validation on domain-specific datasets recommended.
- Normalization by maximum intensity per spectrum can be unstable if spectra have very low signal-to-noise or contain single dominant peaks (e.g., molecular ion); pre-filtering spectra for minimum peak count (≥10) and noise filtering is essential.
- Word2Vec CBOW with intensity weights is not demonstrated for GC-MS data where neutral losses are not reliably measured; the method is validated only on LC-MS positive ionization mode.
- Model generalization suffers if training corpus m/z range, resolution, or instrument type differs substantially from query spectra (e.g., training on high-resolution Orbitrap but querying low-resolution ion trap).

## Evidence

- [methods] Normalize peak intensities to maximum = 1 for each spectrum: "Normalize peak intensities to maximum = 1 for each spectrum."
- [methods] Weighted sum of word embeddings with weight = normalized intensity, sqrt applied: "weighted sum of word embeddings (weight = normalized intensity, sqrt applied)"
- [methods] Peaks represented as words in [redacted-email] format with neutral losses as [redacted-email]: "every peak is represented by a word that contains its position up to a defined decimal precision ("[redacted-email]"). In addition to all peaks of a spectrum, neutral losses between 5.0 and 200.0 Da were"
- [methods] Word2Vec CBOW training with window-size 500, negative=5, 15-50 epochs: "train from scratch using CBOW with window-size 500, negative sampling (negative=5), 15–50 epochs on spectrum documents"
- [methods] Missing-fraction threshold <0.05 filters spectra outside learned vocabulary: "By setting a threshold for the missing fraction (e.g. <0.05), returning Spec2Vec similarity scores for spectra far outside the learned peaks (and losses) can be avoided"
- [methods] Missing-fraction = 1 − (Σ√w_i for words in model) / (Σ√w_i for all words): "missing_fraction = 1 − (Σ√w_i for words in model) / (Σ√w_i for all words), where w_i is peak intensity"
- [readme] Word2Vec learns fragment relationships inspired by natural language processing: "Spec2Vec is a novel spectral similarity score inspired by a natural language processing algorithm -- Word2Vec. Where Word2Vec learns relationships between words in sentences, spec2vec does so for"
