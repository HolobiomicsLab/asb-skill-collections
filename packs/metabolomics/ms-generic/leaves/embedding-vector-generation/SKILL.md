---
name: embedding-vector-generation
description: Use when when you have tokenized mass spectra (peak-mass and peak-intensity
  pairs from experimental or in-silico libraries such as NIST 2017 or MassBank) and
  need to perform rapid similarity searches or spectrum matching at scale.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3645
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - gensim
  - Python
  - Python 3.7
  - Anaconda
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
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

# embedding-vector-generation

## Summary

Convert raw mass spectra into fixed-length vector representations using Word2vec, enabling efficient similarity-based matching and retrieval in large spectral databases. This skill bridges raw spectral data and downstream machine learning workflows by capturing spectral relationships in dense embedding space.

## When to use

When you have tokenized mass spectra (peak-mass and peak-intensity pairs from experimental or in-silico libraries such as NIST 2017 or MassBank) and need to perform rapid similarity searches or spectrum matching at scale. This skill is essential when building searchable databases of millions of spectra where cosine similarity between known similar spectra must exceed a threshold of 0.7.

## When NOT to use

- Input spectra are already in fixed-length vector form or have been pre-embedded by another method
- Spectral dataset is small (<1000 spectra) where traditional similarity metrics are sufficiently fast
- Embeddings must preserve absolute peak intensities or mass accuracies beyond what Word2vec tokenization can capture

## Inputs

- Tokenized mass spectra (peak-mass and peak-intensity token sequences)
- Mass spectra data from experimental libraries (NIST 2017, MassBank) or in-silico libraries
- Raw peak lists or spectral data files

## Outputs

- Trained Word2vec embedding model (gensim model object)
- Fixed-length embedding vectors for all reference spectra
- Embedding vector database indexed by spectrum identifier

## How to apply

Tokenize all mass spectra from reference libraries into peak-mass and peak-intensity token sequences. Train a Word2vec model using gensim with these tokenized spectra as input sentences, configuring it to learn fixed-length embedding vectors (the gensim Word2vec model learns spectral relationships analogous to semantic relationships in text). Apply the trained model to convert all reference spectra into embedding vectors. Validate embedding quality by computing cosine similarity between pairs of known similar spectra; embeddings are acceptable when similarity scores exceed 0.7. Store the trained Word2vec model and embedding vectors for use in downstream spectrum matching tasks.

## Related tools

- **gensim** (Train Word2vec model on tokenized spectra to learn fixed-length embedding vectors capturing spectral relationships) — https://radimrehurek.com/gensim/
- **Python 3.7** (Primary language for implementing tokenization, model training, and validation workflows)
- **Anaconda** (Environment manager for installing gensim and managing Python 3.7 dependencies) — https://www.anaconda.com/

## Examples

```
from gensim.models import Word2Vec
model = Word2Vec(sentences=tokenized_spectra, vector_size=100, window=5, min_count=1, workers=4)
embeddings = [model.infer_vector(spectrum_tokens) for spectrum_tokens in tokenized_spectra]
```

## Evaluation signals

- Cosine similarity between known similar spectra in embedding space exceeds 0.7 threshold
- Embedding dimension and Word2vec training parameters (e.g., window size, min_count) are documented and reproducible
- Trained model successfully converts all spectra in reference library to vectors without errors
- Embedding vector dimensions match the configured Word2vec output size (e.g., 100 or 200 dimensions)
- Model validation on held-out spectrum pairs shows consistent similarity rankings compared to baseline spectrum matching metrics

## Limitations

- Word2vec tokenization loses absolute intensity information; embeddings capture relative spectral relationships only
- Model performance depends on tokenization strategy and training data composition; different spectral libraries may require retraining
- Installation is currently limited to Windows 64-bit environments (Windows 7, Windows 10 tested)
- Embedding quality validation threshold of 0.7 cosine similarity is heuristic and may require tuning for different molecular classes or ionization methods

## Evidence

- [methods] word2vec_tokenization: "Prepare mass spectra data by tokenizing peaks into peak-mass and peak-intensity tokens from NIST 2017 and MassBank experimental libraries."
- [methods] word2vec_training: "Train a Word2vec model using gensim with the tokenized spectra as input sentences, configured to learn fixed-length embedding vectors that capture spectral relationships."
- [methods] embedding_application: "Apply the trained Word2vec model to convert all spectra in the reference library into fixed-length embedding vectors."
- [methods] embedding_validation: "Validate that embeddings preserve spectral similarity by checking cosine similarity correlations between known similar spectra exceed a threshold of 0.7."
- [intro] fastei_motivation: "FastEI is an ultra-fast and accurate spectrum matching method, proposed to improve accuracy by Word2vec-based spectrum embedding and boost the speed using hierarchical navigable small world graph"
- [readme] installation_deps: "conda install -c conda-forge gensim"
