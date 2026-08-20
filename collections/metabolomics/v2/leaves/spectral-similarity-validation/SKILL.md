---
name: spectral-similarity-validation
description: Use when after training a Word2vec model on tokenized mass spectra and
  converting reference spectra into fixed-length embedding vectors, use this skill
  to confirm that the embedding space preserves spectral similarity before deploying
  it for spectrum matching.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - gensim
  - Python
  - scikit-learn or scipy
  license_tier: open
derived_from:
- doi: 10.1038/s41467-023-39279-7
  title: FastEI
evidence_spans:
- conda install -c conda-forge gensim
- Anaconda for Python 3.7
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_fastei_cq
    doi: 10.1038/s41467-023-39279-7
    title: FastEI
  dedup_kept_from: coll_fastei_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-023-39279-7
  all_source_dois:
  - 10.1038/s41467-023-39279-7
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-similarity-validation

## Summary

Validate that spectrum embeddings preserve spectral similarity by computing cosine similarity between known similar spectra and verifying they exceed a predefined threshold. This quality-control step ensures that the embedding representation captures meaningful spectral relationships necessary for accurate spectrum matching.

## When to use

After training a Word2vec model on tokenized mass spectra and converting reference spectra into fixed-length embedding vectors, use this skill to confirm that the embedding space preserves spectral similarity before deploying it for spectrum matching. Apply it when you need confidence that similar spectra cluster together in the embedded space with measurable correlation.

## When NOT to use

- Input spectra are not yet tokenized into peak-mass and peak-intensity tokens; run tokenization first.
- You have not yet trained a Word2vec model on your spectral corpus; validation requires trained embeddings.
- No ground-truth labels or known similar spectrum pairs are available to establish validation baselines.

## Inputs

- trained Word2vec model (gensim format)
- reference library spectra (tokenized as peak-mass and peak-intensity pairs)
- set of known similar spectrum pairs with ground-truth labels

## Outputs

- cosine similarity scores for spectrum pairs
- validation report (pass/fail against 0.7 threshold)
- aggregate similarity metric (mean, median, or percentile)

## How to apply

Compute cosine similarity between embedding vectors of known similar spectrum pairs (e.g., replicates or authentic matches from NIST 2017 or MassBank). Aggregate similarity scores across the validation set and check that the mean or median correlation coefficient exceeds a threshold of 0.7. This threshold guards against embeddings that fail to capture spectral relationships. If validation fails, retrain the Word2vec model with adjusted parameters (e.g., embedding dimension, window size, or training epochs) and repeat validation. The rationale is that Word2vec embeddings trained on peak tokens should encode spectral proximity; cosine similarity in this space should correlate with true spectral similarity.

## Related tools

- **gensim** (trains Word2vec model on tokenized spectra and provides methods to retrieve embedding vectors for cosine similarity computation) — https://github.com/RaRe-Technologies/gensim
- **Python** (runtime environment for executing cosine similarity calculations and validation workflow)
- **scikit-learn or scipy** (compute cosine similarity between embedding vectors (e.g., sklearn.metrics.pairwise.cosine_similarity or scipy.spatial.distance.cosine))

## Examples

```
from gensim.models import Word2Vec
from scipy.spatial.distance import cosine
model = Word2Vec.load('references_word2vec.model')
vec1, vec2 = model.wv['peak_m100_i500'], model.wv['peak_m100_i498']
sim = 1 - cosine(vec1, vec2)
print(f'Cosine similarity: {sim:.3f}'); assert sim >= 0.7, 'Validation failed'
```

## Evaluation signals

- Mean or median cosine similarity of known similar spectrum pairs ≥ 0.7 (threshold from FastEI design).
- Cosine similarity distribution for similar pairs is significantly higher than for dissimilar pairs (e.g., ROC AUC > 0.9 when classifying similar vs. dissimilar).
- No embedding vectors contain NaN or infinite values; all similarities fall in the range [−1, 1].
- Validation passes consistently across multiple random subsets of known similar pairs, indicating robust embedding quality.
- Embeddings for physically similar spectra (e.g., same compound, different collision energy) show higher cosine similarity than those for unrelated compounds.

## Limitations

- Validation accuracy depends on the quality and representativeness of known similar spectrum pairs; sparse or noisy ground-truth labels reduce signal.
- The 0.7 cosine similarity threshold is specific to FastEI's design on NIST 2017 and MassBank libraries; threshold may need adjustment for in-silico or specialized spectral collections.
- Cosine similarity does not capture all aspects of spectral match quality (e.g., peak alignment, intensity ranking); it is a proxy for embedding quality, not a full spectrum matching metric.
- Validation only assesses embedding preservation of similarity; it does not guarantee downstream spectrum matching accuracy or identify failure modes in the HNSW search index.

## Evidence

- [other] Validate that embeddings preserve spectral similarity by checking cosine similarity correlations between known similar spectra exceed a threshold of 0.7.: "Validate that embeddings preserve spectral similarity by checking cosine similarity correlations between known similar spectra exceed a threshold of 0.7."
- [other] FastEI implements Word2vec-based spectrum embedding as a mechanism to improve accuracy in spectrum matching by converting spectra into embedded vector representations using gensim.: "FastEI implements Word2vec-based spectrum embedding as a mechanism to improve accuracy in spectrum matching by converting spectra into embedded vector representations using gensim."
- [other] Prepare mass spectra data by tokenizing peaks into peak-mass and peak-intensity tokens from NIST 2017 and MassBank experimental libraries.: "Prepare mass spectra data by tokenizing peaks into peak-mass and peak-intensity tokens from NIST 2017 and MassBank experimental libraries."
- [other] Apply the trained Word2vec model to convert all spectra in the reference library into fixed-length embedding vectors.: "Apply the trained Word2vec model to convert all spectra in the reference library into fixed-length embedding vectors."
- [readme] FastEI is an ultra-fast and accurate spectrum matching method, proposed to improve accuracy by Word2vec-based spectrum embedding and boost the speed using hierarchical navigable small world graph: "FastEI is an ultra-fast and accurate spectrum matching method, proposed to improve accuracy by Word2vec-based spectrum embedding and boost the speed using hierarchical navigable small world graph"
