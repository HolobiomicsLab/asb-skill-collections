---
name: word2vec-embedding-training-mass-spectrometry
description: Use when you have a large collection of preprocessed MS/MS spectra (typically >10,000 spectra) with diverse chemical structures and you need to learn embeddings that capture fragmentation patterns and neutral loss relationships.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Spec2Vec
  - Word2Vec
  - matchms
  - gensim
  - RDKit
  - NumPy
  - Numba
  - Pandas
  - scipy
  - NumPy / Pandas
  techniques:
  - LC-MS
  - GC-MS
derived_from:
- doi: 10.1371/journal.pcbi.1008724
  title: Spec2Vec
- doi: 10.5281/zenodo.3978054
  title: ''
evidence_spans:
- we introduce Spec2Vec, a novel spectral similarity score
- spec2vec (https://github.com/iomega/spec2vec). Both packages are freely available and can be installed via conda
- inspired by a natural language processing algorithm—Word2Vec
- A Word2Vec [22] model is trained on all documents of a chosen dataset using gensim [37]
- the implementations for the cosine score and the modified cosine score used can be found in the Python package matchms
- the implementations for the cosine score and the modified cosine score used can be found in the Python package matchms [31] (https://github.com/matchms/matchms)
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
  - 10.5281/zenodo.3978054
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# word2vec-embedding-training-mass-spectrometry

## Summary

Train Word2Vec embeddings on mass spectrometry spectral data represented as documents, where peaks and neutral losses are encoded as words, to learn fragment-relationship representations that enable improved spectral similarity scoring. This skill is foundational for Spec2Vec and produces learned embeddings that capture structural relationships between spectral fragments.

## When to use

Apply this skill when you have a large collection of preprocessed MS/MS spectra (typically >10,000 spectra) with diverse chemical structures and you need to learn embeddings that capture fragmentation patterns and neutral loss relationships. Use it as a prerequisite for Spec2Vec similarity scoring when cosine-based methods show weak correlation with structural similarity, or when library matching must scale to hundreds of thousands of spectra.

## When NOT to use

- Input spectra contain <10 peaks per spectrum on average or insufficient diversity in fragment patterns; insufficient training data reduces embedding quality.
- GC-MS data where neutral losses are not measured; Spec2Vec has not been validated on GC-MS and retraining on GC data has not been demonstrated.
- Pre-existing Word2Vec models already cover your fragment ion space adequately; retraining adds computational cost with diminishing return if feature overlap is high.

## Inputs

- Collection of preprocessed MS/MS spectra (mzML, mzXML, msp, or MGF format)
- Spectral metadata (precursor m/z, parent mass, retention time if available)
- InChIKey annotations (recommended for validation and quality control)

## Outputs

- Trained Word2Vec model (gensim model object, serializable)
- Word embeddings for fragment peaks and neutral losses (dense vectors, dimension typically 100–300)
- Spectrum documents (text format, one spectrum per line)

## How to apply

Convert all spectra in your dataset to text documents by representing each peak as '[redacted-email]' (binning m/z to 2 decimal places) and adding neutral losses as '[redacted-email]' words (calculated from precursor − peak, range 5.0–200.0 Da). Train a Word2Vec model using CBOW architecture with window-size 500, negative sampling (negative=5), and 15–50 epochs on the spectrum documents. To improve model robustness, apply filtering before training: remove spectra with <10 peaks and m/z outside [0, 1000], and limit peaks per spectrum to 0.5 × parent_mass to reduce noise. Store the trained model for later use in Spec2Vec similarity computations; pre-trained models on large datasets (e.g., UniqueInchikey, AllPositive) can be retrieved from Zenodo to avoid retraining if your experimental scope overlaps.

## Related tools

- **Word2Vec** (Core embedding algorithm; implemented via gensim library for training CBOW models on spectral documents) — https://radimrehurek.com/gensim/
- **gensim** (Python library providing Word2Vec implementation (CBOW) and model serialization; used to train and manage embeddings) — https://github.com/RajaRajeswariAP/gensim
- **matchms** (Provides spectrum loading, preprocessing (peak filtering, metadata validation), and format conversion (mzML, msp, MGF) prior to document creation) — https://github.com/matchms/matchms
- **Spec2Vec** (Downstream consumer of trained Word2Vec models; uses embeddings to compute spectral similarity scores based on learned fragment relationships) — https://github.com/iomega/spec2vec
- **NumPy / Pandas** (Utilities for spectrum document creation, filtering, and neutral loss calculation)

## Examples

```
from gensim.models import Word2Vec
from matchms.importing_utils import load_from_msp
import pandas as pd

# Load and preprocess spectra
spectra = [s for s in load_from_msp('spectra.msp') if len(s.peaks) >= 10]

# Convert to spectrum documents
spectrum_docs = []
for spec in spectra:
    words = [f'peak@{mz:.2f}' for mz, intensity in spec.peaks]
    precursor = spec.precursor_mz
    for mz, _ in spec.peaks:
        loss = precursor - mz
        if 5.0 <= loss <= 200.0:
            words.append(f'loss@{loss:.2f}')
    spectrum_docs.append(words)

# Train Word2Vec model
model = Word2Vec(spectrum_docs, window=500, negative=5, epochs=30, min_count=1, workers=4)
model.save('word2vec_model.model')
```

## Evaluation signals

- Model convergence: training loss decreases monotonically over epochs; loss trajectory should stabilize by epoch 15–30.
- Embedding quality: word embeddings for fragments with similar chemical properties (e.g., loss@18 for H2O, loss@44 for CO2) show high cosine similarity in embedding space (>0.5).
- Downstream Spec2Vec correlation: when used in Spec2Vec similarity scoring, top 0.1% of spectral pairs show higher mean Tanimoto structural similarity (as measured on RDKit fingerprints, 2048 bits) compared to cosine or modified cosine scores.
- Coverage: >95% of peaks and losses in test spectra are present in the trained model's vocabulary; missing-fraction threshold <0.05 for the majority of spectra.
- Model file integrity: serialized model loads without errors and produces identical embeddings on re-run with same input data.

## Limitations

- Spec2Vec requires training data with large fraction of features (fragment ions and losses) present; models trained on one dataset may require retraining when applied to experimental data with insufficient feature overlap (e.g., new instrument types, ionization methods).
- Unknown peaks not represented in trained Word2Vec model reduce similarity score accuracy; impact can be assessed via missing-fraction thresholding but cannot be fully eliminated without retraining.
- Limited to LC-MS spectra; performance on GC-MS data has not been validated and is not recommended due to absence of neutral loss measurements in typical GC-MS workflows.
- Training time and memory grow with dataset size and number of epochs; very large spectra collections (>500k spectra) may require distributed training or downsampling.
- Model pre-training on a large spectra dataset reduces but does not eliminate the need for retraining when applying to data with fundamentally different fragmentation characteristics.

## Evidence

- [methods] Convert all spectra to documents by representing peaks as '[redacted-email]' words (binning 2 decimals) and adding neutral losses (5.0–200.0 Da) as '[redacted-email]' words.: "After processing, spectra are converted to documents. For this, every peak is represented by a word that contains its position up to a defined decimal precision ("[redacted-email]"). In addition to all"
- [methods] Train Word2Vec models using CBOW with window-size 500, negative sampling (negative=5), 15–50 epochs.: "train from scratch using CBOW with window-size 500, negative sampling (negative=5), 15–50 epochs on spectrum documents"
- [methods] Filter spectra before training: remove those with <10 peaks, m/z outside [0, 1000]; limit peaks per spectrum to 0.5 × parent_mass.: "We removed all peaks with m/z ratios outside the range [0, 1000] and discarded all spectra with less than 10 peaks. the maximum number of kept peaks per spectrum was set to scale linearly with the"
- [methods] Pre-trained Word2Vec models can be downloaded from Zenodo and applied without retraining when feature overlap is sufficient.: "The two most important trained Word2Vec models used in this work can be downloaded from https://doi.org/10.5281/zenodo.3978054 (trained on UniqueInchikey dataset)"
- [discussion] Model retraining may be needed when applying to data with insufficient feature overlap not covered in initial training set.: "one limitation of Spec2Vec as compared to cosine scores is that it needs training data to learn the fragment peak relationships; however, since this not necessarily needs to be library spectra and in"
- [discussion] Spec2Vec performance has only been demonstrated on LC-MS data and not on GC-MS due to absent neutral loss measurements.: "In the present work, we have only demonstrated performance on LC-MS data and not yet assessed Spec2Vec for GC-MS data. For GC-MS, neutral losses are usually not measured."
- [readme] Word2Vec learns relationships between words in sentences; Spec2Vec does so for mass fragments and neutral losses in MS/MS spectra.: "**spec2vec** is a novel spectral similarity score inspired by a natural language processing algorithm -- Word2Vec. Where Word2Vec learns relationships between words in sentences, **spec2vec** does so"
