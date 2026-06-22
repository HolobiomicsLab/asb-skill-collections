---
name: word-embedding-based-spectrum-representation
description: Use when when comparing large numbers of MS/MS spectra against spectral libraries or in molecular networking, particularly when molecules differ by multiple structural modifications and cosine-based scores produce excessive false positives.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3678
  tools:
  - matchms
  - gensim
  - Numba
  - Pandas
  - scipy
  - Spec2Vec
  - Word2Vec (gensim)
  - Numpy, Scipy, Pandas
  techniques:
  - GC-MS
derived_from:
- doi: 10.1371/journal.pcbi.1008724
  title: Spec2Vec
evidence_spans:
- the implementations for the cosine score and the modified cosine score used can be found in the Python package matchms
- the implementations for the cosine score and the modified cosine score used can be found in the Python package matchms [31] (https://github.com/matchms/matchms)
- A Word2Vec [22] model is trained on all documents of a chosen dataset using gensim [37]
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# word-embedding-based-spectrum-representation

## Summary

Convert mass spectra into document-like representations where peaks and neutral losses are encoded as learned word embeddings, enabling structural similarity inference through natural language processing models such as Word2Vec. This approach yields superior true-positive-to-false-positive ratios compared to cosine-based spectral similarity during library matching.

## When to use

When comparing large numbers of MS/MS spectra against spectral libraries or in molecular networking, particularly when molecules differ by multiple structural modifications and cosine-based scores produce excessive false positives. Apply when you have access to a large, chemically diverse training corpus (e.g., ≥76,000 spectra) to train or retrain Word2Vec embeddings on fragment ion and neutral loss vocabularies specific to your experimental context (e.g., positive or negative ionization mode).

## When NOT to use

- If input spectra are from GC-MS; Spec2Vec relies on neutral losses which are usually not measured in GC-MS data.
- If you have only a small dataset (<10,000 spectra) with limited chemical diversity and no access to a large pretrained model; Word2Vec requires substantial training data to learn robust embeddings.
- If spectra contain fragments and losses far outside those represented in the training set and you cannot or will not retrain the model; unknown peaks will inflate the missing-fraction threshold and reduce reliability.

## Inputs

- MS/MS spectra in standard formats (mzML, mzXML, msp, MGF, JSON)
- Spectrum metadata (precursor m/z, parent mass, ionization mode)
- InChIKey annotations or other chemical structure ground truth (for evaluation)
- Trained Word2Vec model or large training corpus of spectra for Word2Vec fitting

## Outputs

- Spectrum documents (text files with peak and neutral loss tokens)
- Trained Word2Vec embedding model (gensim format)
- Spec2Vec similarity score matrix (sparse or dense format)
- Receiver-operator-characteristic curves and true-positive/false-positive rates
- Library matches ranked by Spec2Vec similarity with confidence scores

## How to apply

Convert each processed spectrum into a text document by representing each peak as '[redacted-email]' (m/z to defined decimal precision) and adding neutral losses as '[redacted-email]' (calculated as precursor − peak for losses between 5.0 and 200.0 Da). Train a Word2Vec model (or use a pretrained model) on a large set of such documents to learn embeddings that capture co-occurrence relationships between fragments and losses across structurally similar compounds. Apply parent-mass-scaled peak filtering (max_peaks = 0.5 × parent mass) before embedding to reduce noise and computational cost. Compute Spec2Vec similarity scores by comparing the learned embeddings of query and library spectra; this yields scores that correlate more strongly with structural similarity than cosine or modified cosine. Use a missing-fraction threshold (e.g., <0.05) to flag spectra with unknown peaks outside the learned vocabulary. Evaluate performance using receiver-operator-characteristic curves and true-positive/false-positive rates on a held-out test set with known InChIKey ground truth (first 14 characters / planar structure).

## Related tools

- **Spec2Vec** (Compute spectral similarity scores based on learned Word2Vec embeddings of peaks and neutral losses) — https://github.com/iomega/spec2vec
- **Word2Vec (gensim)** (Train embeddings of fragment ions and neutral losses to capture fragmentation relationships)
- **matchms** (Import, filter, and process mass spectra; compute cosine and modified cosine similarity for comparison) — https://github.com/matchms/matchms
- **Numpy, Scipy, Pandas** (Numerical operations, similarity matrix computation, and data frame handling)
- **Numba** (JIT compilation of similarity score computations for performance optimization)

## Examples

```
from spec2vec import Spec2Vec; from gensim.models import Word2Vec; model = Word2Vec.load('word2vec_model.model'); spec2vec = Spec2Vec(model); scores = spec2vec.pair_iterator(query_spectrum, library_spectra)
```

## Evaluation signals

- Spec2Vec similarity scores should correlate more strongly with structural similarity (measured via InChIKey planar structure matches) than cosine or modified cosine scores, visible as higher R² in correlation plots.
- True-positive rate at a fixed false-positive rate threshold should exceed that of cosine/modified cosine; ROC curves should show Spec2Vec with larger area-under-curve (AUC ≥ 0.88 reported in Huber et al. 2021).
- Missing-fraction estimates (uncovered weighted part of spectra with unknown peaks) should remain below the set threshold (e.g., <0.05) for the majority of test spectra, indicating sufficient vocabulary overlap with the trained model.
- Rank-order of library hits should place true-positive matches (same planar InChIKey) higher than false positives when sorting by descending Spec2Vec similarity.
- Reproducibility check: similarity score matrices computed from the same spectra and model should be identical (bit-for-bit); pre-trained models from Zenodo should be loadable and produce consistent scores.

## Limitations

- Spec2Vec requires training data and may underperform on spectral features (peaks or losses) not well-represented in the training set; retraining on new experimental conditions is often necessary.
- Not yet validated on GC-MS data, as neutral losses are typically not measured in GC-MS workflows.
- Model pre-training on a large dataset reduces but does not eliminate the need for retraining when applying to data with significantly different ionization modes or instrumental parameters.
- Unknown peaks not present in the trained Word2Vec vocabulary cannot be directly embedded; missing-fraction estimates provide only indirect uncertainty quantification.
- Computational cost of Word2Vec training scales with corpus size and vector dimensionality; model inference is faster than training but slower than simple cosine similarity for very large databases.

## Evidence

- [methods] After processing, spectra are converted to documents. For this, every peak is represented by a word that contains its position up to a defined decimal precision ("[redacted-email]"): "After processing, spectra are converted to documents. For this, every peak is represented by a word that contains its position up to a defined decimal precision ('[redacted-email]')"
- [methods] In addition to all peaks of a spectrum, neutral losses between 5.0 and 200.0 Da were added as "[redacted-email]". Neutral losses are calculated as precursor − peak: "In addition to all peaks of a spectrum, neutral losses between 5.0 and 200.0 Da were added as '[redacted-email]'. Neutral losses are calculated as precursor − peak"
- [abstract] Spec2Vec scores correlate better with structural similarity than cosine-based scores: "Spec2Vec scores correlate better with structural similarity than cosine-based scores"
- [results] high Spec2Vec spectrum similarity score correlates stronger with structural similarity than the cosine or modified cosine scores: "high Spec2Vec spectrum similarity score correlates stronger with structural similarity than the cosine or modified cosine scores"
- [methods] the maximum number of kept peaks per spectrum was set to scale linearly with the estimated parent mass: max(n_peaks) = 0.5 × parentmass: "the maximum number of kept peaks per spectrum was set to scale linearly with the estimated parent mass: max(n_peaks) = 0.5 × parentmass"
- [methods] In those instances some words (= peaks) of a given spectra might be unknown to the model. In those instances we can estimate the impact of the missing words by assessing the uncovered weighted part: "In those instances some words (= peaks) of a given spectra might be unknown to the model. In those instances we can estimate the impact of the missing words by assessing the uncovered weighted part"
- [intro] Spec2Vec is a novel spectral similarity score based upon learnt embeddings of spectra. Instead inspired by the success of algorithms from the field of natural language: "Spec2Vec is a novel spectral similarity score based upon learnt embeddings of spectra"
- [discussion] For GC-MS, neutral losses are usually not measured.: "For GC-MS, neutral losses are usually not measured."
- [readme] Where Word2Vec learns relationships between words in sentences, **spec2vec** does so for mass fragments and neutral losses in MS/MS spectra.: "Where Word2Vec learns relationships between words in sentences, spec2vec does so for mass fragments and neutral losses in MS/MS spectra."
- [abstract] Spec2Vec is computationally more scalable allowing structural analogue searches in large databases within seconds: "Spec2Vec is computationally more scalable allowing structural analogue searches in large databases within seconds"
