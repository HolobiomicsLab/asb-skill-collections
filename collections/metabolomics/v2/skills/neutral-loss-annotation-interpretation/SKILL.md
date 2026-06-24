---
name: neutral-loss-annotation-interpretation
description: Use when when building Word2Vec or embedding-based spectral similarity
  models where you need to capture fragmentation patterns beyond individual peak positions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3375
  tools:
  - Spec2Vec
  - matchms
  - gensim
  - RDKit
  - NumPy
  - Numba
  - Pandas
  - scipy
  - Word2Vec
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

# Neutral-loss-annotation-interpretation

## Summary

Annotate and interpret neutral losses in MS/MS spectra by calculating mass differences between precursor m/z and observed fragment peaks, then incorporating these losses as features into spectral representations for improved structural relationship learning. This skill enables mass spectrometry-based algorithms to recognize recurring fragmentation patterns that reflect structural chemistry.

## When to use

When building Word2Vec or embedding-based spectral similarity models where you need to capture fragmentation patterns beyond individual peak positions. Apply this skill after peak detection and precursor m/z assignment, especially when working with LC-MS data where neutral losses are regularly measured and carry structural information. Use when the goal is to improve correlation between spectral and structural similarity scores.

## When NOT to use

- GC-MS data: neutral losses are usually not measured in GC-MS, limiting the interpretability and benefit of loss annotation
- Spectra with precursor m/z < 5 Da or > 2000 Da: extreme mass ranges may produce spurious or uninformative neutral loss features
- Data lacking reliable precursor m/z assignment: loss calculation depends critically on accurate precursor annotation; missing or miscalibrated precursor values will corrupt the loss feature space

## Inputs

- Preprocessed spectrum objects with precursor m/z and fragment peak m/z values
- Fragment peak intensity values
- Peak and spectrum metadata (e.g., InChIKey annotations for validation)

## Outputs

- Spectrum documents with peak tokens ('[redacted-email]') and neutral loss tokens ('[redacted-email]')
- Word2Vec model trained on augmented spectrum documents
- Spec2Vec similarity scores incorporating structural relationships learned from neutral loss patterns

## How to apply

For each spectrum, calculate neutral losses as the mass difference between the precursor m/z and each observed fragment peak (precursor − fragment peak). Represent each neutral loss in the 5.0–200.0 Da range as a word token formatted '[redacted-email]' (binning to 2 decimal places for consistency). Append these loss tokens to the spectrum document alongside peak tokens ('[redacted-email]'). This dual representation—peaks and losses—allows Word2Vec to learn co-occurrence patterns: fragments that frequently appear together after the same neutral loss are semantically closer in the embedding space, implicitly encoding structural relationships. The 5.0–200.0 Da threshold excludes trivial losses (< 5 Da) and implausibly large losses, keeping the feature space relevant to common organic chemistry fragmentation (e.g., H₂O = 18.015, CO₂ = 44.009, loss of side chains). Train the Word2Vec model (CBOW, window=500, negative=5) on the augmented spectrum documents so that the model learns which peaks and losses co-occur, thereby capturing structural clues encoded in fragmentation.

## Related tools

- **Word2Vec** (Learns co-occurrence relationships between peak and neutral loss tokens to produce spectrum embeddings that capture structural similarity)
- **Spec2Vec** (Computes spectral similarity scores using learned Word2Vec embeddings that incorporate neutral loss information) — https://github.com/iomega/spec2vec
- **matchms** (Provides spectrum data structures, preprocessing, and validation utilities for neutral loss calculation and loss-annotated document representation) — https://github.com/matchms/matchms
- **gensim** (Implements Word2Vec (CBOW) training on spectrum documents containing loss tokens)

## Examples

```
from matchms import Spectrum; from gensim.models import Word2Vec; spectra = [Spectrum(mz=[100.0, 150.0], intensities=[0.5, 1.0], metadata={'precursor_mz': 200.0}) for ...]; documents = [['peak@100.00', 'peak@150.00', 'loss@100.00', 'loss@50.00'] for spec in spectra]; model = Word2Vec(documents, window=500, sg=0, negative=5, epochs=15)
```

## Evaluation signals

- Verify neutral losses fall within 5.0–200.0 Da range and are correctly calculated as (precursor_m/z − fragment_m/z); spot-check 10–20 spectra against raw data
- Confirm all loss tokens follow '[redacted-email]' format with exactly 2 decimal places and match binned mass values
- Validate that spectra with known fragmentation patterns (e.g., water loss from alcohols, CO₂ loss from carboxylic acids) have corresponding loss tokens present in documents
- Measure Pearson or Spearman correlation between Spec2Vec similarity scores (trained on loss-augmented documents) and structural similarity (Tanimoto/Jaccard on fingerprints) in held-out test set; should show stronger correlation than cosine-based scores (expected improvement visible in top 0.1% pairs)
- Compare Word2Vec embedding neighborhoods: loss tokens should cluster near chemically plausible fragment tokens (e.g., 'loss@18.01' near 'peak@xxx' from water loss products)

## Limitations

- Neutral loss annotation is restricted to LC-MS data; GC-MS does not routinely measure neutral losses, limiting model portability to EI or EI-like ionization
- The approach requires training data with high coverage of fragment and loss features; if applied to experimental spectra or ionization modes not represented in the training set, the Word2Vec model may not have learned meaningful embeddings for novel losses, reducing Spec2Vec performance unless the model is retrained
- Precursor m/z measurement errors directly propagate into loss calculation; miscalibrated instruments or spectra with unknown precursor mass will produce incorrect loss tokens and degrade model quality
- The 5.0–200.0 Da threshold is heuristic and optimized for small-molecule LC-MS; larger molecules, native MS, or targeted applications may require adjusted loss ranges
- Neutral loss tokens are most informative when losses recur across structurally similar molecules; for novel or rare chemical scaffolds absent from training data, loss annotation may not improve structural relationship learning

## Evidence

- [methods] In addition to all peaks of a spectrum, neutral losses between 5.0 and 200.0 Da were added as '[redacted-email]'. Neutral losses are calculated as precursor − peak: "In addition to all peaks of a spectrum, neutral losses between 5.0 and 200.0 Da were added as "[redacted-email]". Neutral losses are calculated as precursor − peak"
- [methods] After processing, spectra are converted to documents. For this, every peak is represented by a word that contains its position up to a defined decimal precision ('[redacted-email]'): "After processing, spectra are converted to documents. For this, every peak is represented by a word that contains its position up to a defined decimal precision ("[redacted-email]")"
- [intro] Adapting Word2Vec, a processing [22], Spec2Vec learns relationships between fragments and neutral losses in mass spectra: "Adapting Word2Vec, a processing [22], Spec2Vec learns relationships between fragments and neutral losses in mass spectra"
- [discussion] we have only demonstrated performance on LC-MS data and not yet assessed Spec2Vec for GC-MS data. For GC-MS, neutral losses are usually not measured.: "we have only demonstrated performance on LC-MS data and not yet assessed Spec2Vec for GC-MS data. For GC-MS, neutral losses are usually not measured."
- [discussion] one limitation of Spec2Vec as compared to cosine scores is that it needs training data to learn the fragment peak relationships: "one limitation of Spec2Vec as compared to cosine scores is that it needs training data to learn the fragment peak relationships"
