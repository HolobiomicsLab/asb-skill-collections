---
name: peak-mass-intensity-feature-encoding
description: Use when you have raw mass spectra (e.g., from NIST 2017 or MassBank) and need to prepare them for Word2vec embedding or other token-based neural models. Use it as a preprocessing step before training spectral embedding models, especially when scale and accuracy of spectrum matching are priorities.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - gensim
  - Python
  - Python 3.7
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peak-mass-intensity-feature-encoding

## Summary

Converts raw mass spectra into discrete token pairs (peak-mass and peak-intensity tokens) to enable downstream neural embedding and similarity matching. This tokenization step standardizes spectral representations for Word2vec-based embedding in high-throughput spectrum matching workflows.

## When to use

Apply this skill when you have raw mass spectra (e.g., from NIST 2017 or MassBank) and need to prepare them for Word2vec embedding or other token-based neural models. Use it as a preprocessing step before training spectral embedding models, especially when scale and accuracy of spectrum matching are priorities.

## When NOT to use

- Spectra are already represented as fixed-length vectors or dense feature matrices; tokenization would be redundant.
- Your downstream model does not benefit from sequence-based representations (e.g., if you are using direct kernel methods or simple dot-product similarity).
- Peak-level noise or baseline subtraction has not been performed; raw, uncleaned spectra may produce uninformative tokens.

## Inputs

- Raw mass spectra (e.g., from NIST 2017 or MassBank experimental libraries)
- Peak m/z values and intensity measurements per spectrum

## Outputs

- Tokenized spectra: sequences of peak-mass and peak-intensity token pairs
- Token vocabulary: discrete bins for mass and intensity ranges

## How to apply

Extract peak mass-to-charge ratios (m/z) and their corresponding intensities from each mass spectrum in your reference library. Tokenize each peak as a pair of discrete tokens—one representing the peak-mass bin and one representing the peak-intensity magnitude. Aggregate all tokenized peaks from a single spectrum into a sequence (analogous to a sentence in NLP) that preserves the spectral structure. These sequences become the input training data for Word2vec models trained with gensim, configured to learn fixed-length embedding vectors that capture spectral relationships. Validation follows by checking that cosine similarity between known similar spectra exceeds a threshold of 0.7.

## Related tools

- **gensim** (Word2vec model training on tokenized spectra sequences to learn fixed-length embedding vectors)
- **Python 3.7** (Runtime environment for tokenization, token sequence assembly, and model training)

## Evaluation signals

- Token vocabulary size and frequency distribution are reasonable (no extreme sparsity or collapse to a few dominant tokens).
- Tokenized sequences maintain spectrum-level uniqueness: known similar spectra produce similar token sequences.
- Post-embedding cosine similarity between known spectral pairs exceeds the 0.7 threshold, confirming that embeddings preserve spectral relationship structure.
- No information loss in the token representation: round-trip conversion (spectrum → tokens → embedding) preserves rank order of similarity judgments.

## Limitations

- Tokenization introduces quantization loss: fine-grained mass and intensity information is binned into discrete tokens, potentially losing precision in boundary regions.
- Token vocabulary design (bin size, granularity) is not detailed in the source material; optimal tokenization parameters may be task- and library-dependent.
- FastEI installation currently supports Windows 64-bit only (Windows 7, Windows 10), limiting portability of the full system.
- The article does not provide explicit guidance on handling spectra with missing or sparse peaks, or on standardizing peak intensity normalization before tokenization.

## Evidence

- [other] Prepare mass spectra data by tokenizing peaks into peak-mass and peak-intensity tokens from NIST 2017 and MassBank experimental libraries.: "Prepare mass spectra data by tokenizing peaks into peak-mass and peak-intensity tokens from NIST 2017 and MassBank experimental libraries."
- [other] Train a Word2vec model using gensim with the tokenized spectra as input sentences, configured to learn fixed-length embedding vectors that capture spectral relationships.: "Train a Word2vec model using gensim with the tokenized spectra as input sentences, configured to learn fixed-length embedding vectors that capture spectral relationships."
- [other] Validate that embeddings preserve spectral similarity by checking cosine similarity correlations between known similar spectra exceed a threshold of 0.7.: "Validate that embeddings preserve spectral similarity by checking cosine similarity correlations between known similar spectra exceed a threshold of 0.7."
- [other] FastEI implements Word2vec-based spectrum embedding as a mechanism to improve accuracy in spectrum matching by converting spectra into embedded vector representations using gensim.: "FastEI implements Word2vec-based spectrum embedding as a mechanism to improve accuracy in spectrum matching by converting spectra into embedded vector representations using gensim."
- [readme] experimental libraries (e.g., NIST 2017 and MassBank libraries): "experimental libraries (e.g., NIST 2017 and MassBank libraries)"
