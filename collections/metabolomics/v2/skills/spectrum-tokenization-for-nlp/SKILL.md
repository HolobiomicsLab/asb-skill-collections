---
name: spectrum-tokenization-for-nlp
description: Use when when you have raw mass spectra from experimental libraries (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3937
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - gensim
  - Python
  - Python 3.7
  techniques:
  - mass-spectrometry
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

# spectrum-tokenization-for-nlp

## Summary

Convert mass spectra into discrete token sequences (peak-mass and peak-intensity tokens) to enable natural language processing techniques like Word2vec to learn fixed-length vector embeddings that capture spectral relationships. This preprocessing step bridges spectroscopy data and NLP-based similarity learning.

## When to use

When you have raw mass spectra from experimental libraries (e.g., NIST 2017, MassBank) and need to train an embedding model to improve spectrum matching accuracy by representing spectra as fixed-length vectors that preserve spectral similarity relationships with cosine similarity correlations exceeding 0.7.

## When NOT to use

- Spectra are already represented as fixed-length numeric feature vectors (e.g., from direct intensity binning or principal component analysis)—tokenization adds no value.
- Peak lists are corrupted, missing intensity information, or contain fewer than ~10 informative peaks per spectrum—insufficient signal for robust token sequences.
- The goal is real-time single-spectrum search without offline embedding; preprocessing and model training overhead is unjustified.

## Inputs

- Raw mass spectra from experimental libraries (NIST 2017, MassBank)
- Peak mass values and intensities for each spectrum
- Reference library of annotated spectra

## Outputs

- Tokenized spectrum sequences (peak-mass and peak-intensity tokens per spectrum)
- Word2vec trained embedding model (gensim model object)
- Fixed-length embedding vectors for all reference spectra
- Validated cosine similarity matrix (≥0.7 threshold for known similar pairs)

## How to apply

Tokenize each mass spectrum by converting peaks into parallel sequences of peak-mass tokens and peak-intensity tokens. Treat each spectrum as a 'sentence' where tokens are ordered by mass/intensity relationships. Feed these tokenized spectra as input to a Word2vec model (via gensim) trained with default or tuned embedding dimensions. The resulting embeddings encode spectral similarity in vector space, enabling fast cosine similarity lookups. Validate that known similar spectra yield cosine similarity ≥ 0.7 to confirm embeddings preserve spectral relationships.

## Related tools

- **gensim** (Train Word2vec embedding model on tokenized spectrum sequences to learn fixed-length vector representations capturing spectral similarity) — https://github.com/RaRe-Technologies/gensim
- **Python 3.7** (Runtime environment for tokenization scripts and gensim model training)

## Examples

```
from gensim.models import Word2Vec
tokenized_spectra = [["peak_mass_100", "peak_intensity_500"], ["peak_mass_150", "peak_intensity_300"]]
model = Word2Vec(sentences=tokenized_spectra, vector_size=100, window=5, min_count=1)
embeddings = [model.infer_vector(tokens) for tokens in tokenized_spectra]
```

## Evaluation signals

- Tokenized spectra form valid input to gensim Word2vec (each spectrum tokenized into ≥1 token sequence, no null or malformed entries)
- Resulting embeddings have consistent dimensionality (fixed-length vectors per spectrum)
- Cosine similarity between known similar spectra (from reference annotations) exceeds 0.7 threshold, confirming preservation of spectral relationships
- Embedding model converges during training (loss decreases over epochs, no divergence)
- Random dissimilar spectra yield cosine similarity <0.7, demonstrating discriminative power

## Limitations

- Tokenization quality depends on peak detection accuracy upstream; noisy or incomplete peak lists degrade embedding quality.
- Word2vec requires sufficient spectral diversity and volume (millions of spectra in FastEI) to learn generalizable embeddings; small libraries may overfit.
- Threshold of 0.7 for cosine similarity validation is empirically chosen for FastEI and may require adjustment for other spectroscopy domains or mass spectrometry instruments.
- Only supports Windows 64-bit systems (FastEI-GUI binary), limiting deployment flexibility for non-Windows environments without development-version setup.

## Evidence

- [other] Prepare mass spectra data by tokenizing peaks into peak-mass and peak-intensity tokens from NIST 2017 and MassBank experimental libraries.: "Prepare mass spectra data by tokenizing peaks into peak-mass and peak-intensity tokens from NIST 2017 and MassBank experimental libraries."
- [other] Train a Word2vec model using gensim with the tokenized spectra as input sentences, configured to learn fixed-length embedding vectors that capture spectral relationships.: "Train a Word2vec model using gensim with the tokenized spectra as input sentences, configured to learn fixed-length embedding vectors that capture spectral relationships."
- [other] Validate that embeddings preserve spectral similarity by checking cosine similarity correlations between known similar spectra exceed a threshold of 0.7.: "Validate that embeddings preserve spectral similarity by checking cosine similarity correlations between known similar spectra exceed a threshold of 0.7."
- [readme] FastEI is an ultra-fast and accurate spectrum matching method, proposed to improve accuracy by Word2vec-based spectrum embedding: "FastEI is an ultra-fast and accurate spectrum matching method, proposed to improve accuracy by Word2vec-based spectrum embedding"
- [readme] conda install -c conda-forge gensim: "conda install -c conda-forge gensim"
