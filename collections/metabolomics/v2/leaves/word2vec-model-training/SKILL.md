---
name: word2vec-model-training
description: Use when when you have a collection of mass spectra (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3465
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - gensim
  - Python
  - Python 3.7
  - Anaconda
  techniques:
  - mass-spectrometry
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

# word2vec-model-training

## Summary

Train a Word2vec embedding model on tokenized mass spectra to convert variable-length spectra into fixed-length vector representations that preserve spectral similarity relationships. This enables accurate spectrum matching by embedding spectra into a continuous vector space where similar spectra cluster together.

## When to use

When you have a collection of mass spectra (e.g., from NIST 2017 or MassBank) that need to be converted into fixed-length numerical vectors for similarity-based matching or retrieval, and you want to preserve spectral relationships such that cosine similarity between embedding vectors correlates with actual spectral similarity.

## When NOT to use

- Spectra are already in fixed-length vector form or pre-computed embeddings are available
- Reference spectral library is very small (<100 spectra), making statistical training of Word2vec unreliable
- Real-time or single-spectrum embedding is required without prior model training

## Inputs

- Collection of mass spectra (raw peak lists with mass and intensity values)
- Tokenized spectra (peak-mass and peak-intensity tokens derived from raw spectra)
- Reference spectral library (e.g., NIST 2017, MassBank experimental libraries)

## Outputs

- Trained Word2vec model (gensim model file)
- Fixed-length spectrum embedding vectors (one vector per spectrum in the library)
- Validation report with cosine similarity scores between known similar spectra

## How to apply

First, tokenize all mass spectra by decomposing each spectrum into peak-mass and peak-intensity tokens, treating each spectrum as a sentence of tokens. Train a Word2vec model using gensim with these tokenized spectra as input, configuring it to learn fixed-length embedding vectors (the paper does not specify vector dimensionality, but Word2vec typically uses 100–300 dimensions). Apply the trained model to convert all reference spectra into embeddings. Validate that embeddings preserve spectral relationships by computing cosine similarity between known similar spectra and confirming the similarity exceeds a threshold of 0.7, indicating the embeddings have captured meaningful spectral structure.

## Related tools

- **gensim** (Trains Word2vec model on tokenized spectra and applies the trained model to convert spectra into fixed-length embedding vectors) — https://github.com/RaRe-Technologies/gensim
- **Python 3.7** (Execution environment for running gensim and the FastEI workflow)
- **Anaconda** (Package and environment manager for installing gensim and dependencies) — https://www.anaconda.com/

## Examples

```
from gensim.models import Word2Vec; tokenized_spectra = [['peak_100_0.5', 'peak_150_1.2', ...], ...]; model = Word2Vec(sentences=tokenized_spectra, vector_size=100, window=5, min_count=1, workers=4); embeddings = [model.infer_vector(spectrum) for spectrum in tokenized_spectra]
```

## Evaluation signals

- Cosine similarity between embedding vectors of known similar spectra exceeds 0.7 threshold
- Trained model file successfully persists and can be reloaded for inference on new spectra
- All spectra in reference library are converted to embedding vectors of consistent dimensionality
- Embedding vectors are numeric, finite (no NaN or Inf), and normalized or scaled appropriately for similarity computation
- Qualitative inspection: dissimilar spectra have cosine similarity below 0.7, confirming separation in embedding space

## Limitations

- Tokenization strategy (peak-mass and peak-intensity tokens) is not detailed; token granularity and normalization affect model quality but are not fully specified
- Vector dimensionality and other Word2vec hyperparameters (window size, minimum count, iterations) are not documented in the article or README
- Model quality depends on reference library size and diversity; very small or biased spectral libraries may produce poor embeddings
- Validation threshold of 0.7 is empirically chosen; no justification or sensitivity analysis is provided
- Installation and deployment are documented only for Windows 64-bit; cross-platform applicability is unclear

## Evidence

- [other] Prepare mass spectra data by tokenizing peaks into peak-mass and peak-intensity tokens from NIST 2017 and MassBank experimental libraries: "Prepare mass spectra data by tokenizing peaks into peak-mass and peak-intensity tokens from NIST 2017 and MassBank experimental libraries."
- [other] Train a Word2vec model using gensim with the tokenized spectra as input sentences, configured to learn fixed-length embedding vectors that capture spectral relationships: "Train a Word2vec model using gensim with the tokenized spectra as input sentences, configured to learn fixed-length embedding vectors that capture spectral relationships."
- [other] Apply the trained Word2vec model to convert all spectra in the reference library into fixed-length embedding vectors: "Apply the trained Word2vec model to convert all spectra in the reference library into fixed-length embedding vectors."
- [other] Validate that embeddings preserve spectral similarity by checking cosine similarity correlations between known similar spectra exceed a threshold of 0.7: "Validate that embeddings preserve spectral similarity by checking cosine similarity correlations between known similar spectra exceed a threshold of 0.7."
- [readme] FastEI is an ultra-fast and accurate spectrum matching method, proposed to improve accuracy by Word2vec-based spectrum embedding: "FastEI is an ultra-fast and accurate spectrum matching method, proposed to improve accuracy by Word2vec-based spectrum embedding"
