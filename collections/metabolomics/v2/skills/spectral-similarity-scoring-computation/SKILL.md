---
name: spectral-similarity-scoring-computation
description: Use when you have a query spectrum (or set of query spectra) and need to rank candidate library spectra by their likelihood of sharing the same chemical structure.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3674
  tools:
  - Spec2Vec
  - matchms
  - gensim
  - RDKit
  - NumPy
  - Numba
  - Pandas
  - scipy
  - Word2Vec (gensim)
  - NumPy, Pandas, SciPy, Numba
  techniques:
  - LC-MS
  - GC-MS
  - tandem-MS
derived_from:
- doi: 10.1371/journal.pcbi.1008724
  title: Spec2Vec
evidence_spans:
- we introduce Spec2Vec, a novel spectral similarity score
- spec2vec (https://github.com/iomega/spec2vec). Both packages are freely available and can be installed via conda
- the implementations for the cosine score and the modified cosine score used can be found in the Python package matchms
- the implementations for the cosine score and the modified cosine score used can be found in the Python package matchms [31] (https://github.com/matchms/matchms)
- A Word2Vec [22] model is trained on all documents of a chosen dataset using gensim [37]
- Tanimoto similarity (Jaccard index) based on daylight-like molecular fingerprints, version 2020.03.2, 2048 bits, derived using rdkit
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

# Spectral Similarity Scoring Computation

## Summary

Compute pairwise similarity scores between mass spectra using cosine, modified cosine, or Spec2Vec methods to rank spectral matches by structural similarity. This skill is essential for library matching, molecular networking, and metabolite identification workflows where similarity thresholds determine which spectra are considered structurally related.

## When to use

Apply this skill when you have a query spectrum (or set of query spectra) and need to rank candidate library spectra by their likelihood of sharing the same chemical structure. Use it as a pre-filtering step before expensive in-silico fragmentation calculations, or when building molecular networks where edges represent high-confidence spectral similarity. The choice of method (cosine vs. Spec2Vec) depends on whether you have a trained Word2Vec model available and whether the spectral pairs are expected to have high structural similarity with multiple local chemical modifications.

## When NOT to use

- Do not apply to GC-MS data when using Spec2Vec with neutral loss features, as neutral losses are usually not measured in GC-MS and will leave unknown peaks in the model.
- Do not expect reliable performance from a pre-trained Spec2Vec model when querying spectra with fragmentations far outside the learned peaks and losses (mitigated by missing-fraction threshold, but retraining may be necessary).
- Do not use cosine or modified cosine scoring if your structural pairs are expected to differ in multiple local chemical modifications; Spec2Vec correlates substantially better with structural similarity in such cases.

## Inputs

- Query mass spectrum or spectra (with precursor m/z, peaks with m/z and intensity)
- Library of reference mass spectra (with InChIKey annotations for validation)
- Pre-trained Word2Vec model (required for Spec2Vec; optional for cosine methods)
- Spectrum metadata: parent mass, ionization mode (positive/negative)

## Outputs

- Pairwise similarity score matrix (all-vs-all or sparse format)
- Ranked list of library matches per query spectrum (sorted by similarity score descending)
- True-positive rate, false-positive rate, and receiver-operator-characteristic (ROC) curves per method
- Classification of hits as true positives or false positives (when InChIKey ground truth available)

## How to apply

First, ensure spectra are pre-processed: remove peaks with m/z outside [0, 1000], discard spectra with fewer than 10 peaks, and remove spectra without InChIKey annotation. For cosine and modified cosine scoring, filter peaks by ignoring those with relative intensities <0.01 compared to the highest intensity peak. For Spec2Vec, apply parent-mass-scaled peak filtering (max_peaks = 0.5 × parent_mass) and set a missing-fraction threshold (e.g., <0.05). Pre-select potentially matching spectra using precursor m/z matching with 1 ppm tolerance to reduce computation. Compute similarity scores using your chosen method: cosine similarity with tolerance 0.005 and minimum matching peaks ≥ 6; modified cosine with tolerance 0.005 and minimum matching peaks ≥ 10; or Spec2Vec using a pre-trained Word2Vec model (weighted sum of word embeddings with normalized intensity weights, sqrt applied). Rank query spectra against library by score descending. Classify hits as true positives (matching InChIKey within first 14 characters / planar structure) or false positives to evaluate performance.

## Related tools

- **matchms** (Implements cosine and modified cosine similarity score computation; handles spectrum I/O, peak filtering, and metadata cleaning.) — https://github.com/matchms/matchms
- **Spec2Vec** (Implements spectral similarity scoring via learned Word2Vec embeddings of spectrum documents (peaks and neutral losses).) — https://github.com/iomega/spec2vec
- **Word2Vec (gensim)** (Learns distributed embeddings of spectrum fragments and neutral losses; required for Spec2Vec similarity computation.)
- **RDKit** (Computes structural similarity via Tanimoto/Jaccard distance on daylight-like fingerprints (2048 bits) for ground-truth evaluation.)
- **NumPy, Pandas, SciPy, Numba** (Efficient numerical computation, data manipulation, and parallelization of pairwise similarity calculations.)

## Examples

```
from matchms import Spectrum; from matchms.similarity import CosineGreedy, ModifiedCosine; from spec2vec import SpectrumDocument, Spec2Vec; spec2vec_sim = Spec2Vec(model=model); query_results = []; for spec in library: sim_score = spec2vec_sim.pair(SpectrumDocument(query_spectrum), SpectrumDocument(spec)); query_results.append((spec, sim_score)); query_results.sort(key=lambda x: x[1], reverse=True)
```

## Evaluation signals

- For cosine/modified cosine methods: verify that minimum matching peak thresholds are applied (min_match ≥ 6 or 10) and that peak filtering (intensity <0.01) reduces false positives without discarding structurally meaningful fragments.
- For Spec2Vec: confirm that the trained Word2Vec model is loaded correctly and that missing-fraction thresholds prevent scores for spectra with insufficient peak coverage (e.g., missing_fraction > 0.05).
- Compute correlation between similarity scores and structural similarity (Tanimoto on RDKit fingerprints) across all spectrum pairs; Spec2Vec should show higher correlation than cosine methods, especially at top 0.1% of ranking pairs.
- Calculate receiver-operator-characteristic (ROC) curves and area-under-curve (AUC) when ground-truth InChIKey labels are available; Spec2Vec should achieve >80% true-positive rate at low false-positive rates.
- Verify that pre-selected spectra (via precursor m/z matching at 1 ppm tolerance) reduce computation time without systematically removing true positive matches.

## Limitations

- Spec2Vec requires a trained Word2Vec model on spectral data; performance degrades when querying spectra with fragments or neutral losses not well-represented in the training set. Pre-training on large datasets (e.g., AllPositive or UniqueInchiKeys) reduces but does not eliminate the need for retraining on new experimental spectra.
- LC-MS data only: Spec2Vec incorporation of neutral losses (5.0–200.0 Da) is demonstrated only for LC-MS; GC-MS data lacks measurable neutral losses and has not been validated.
- Cosine and modified cosine scores often underperform (high false positive rates) when comparing spectra of molecules with high structural similarity but differing in multiple locations; modified cosine partially addresses this but Spec2Vec is substantially better.
- Unknown peaks in the Spec2Vec model (not present in training Word2Vec vocabulary) reduce the weighted similarity contribution and cannot be recovered without model retraining; mitigation by missing-fraction threshold may increase false negatives.
- All-vs-all similarity computation scales quadratically with the number of spectra; sparse matrix storage and pre-selection funnels (e.g., precursor m/z matching) are required for large libraries.

## Evidence

- [abstract] Spec2Vec similarity scores correlate better with structural similarity than cosine-based scores: "Spec2Vec scores correlate better with structural similarity than cosine-based scores"
- [methods] Spectrum document representation via peaks and neutral losses for Word2Vec training: "every peak is represented by a word that contains its position up to a defined decimal precision ('[redacted-email]'). In addition to all peaks of a spectrum, neutral losses between 5.0 and 200.0 Da were"
- [methods] Peak filtering criteria for Spec2Vec: "the maximum number of kept peaks per spectrum was set to scale linearly with the estimated parent mass: max(n_peaks) = 0.5 × parentmass"
- [methods] Peak filtering criteria for cosine and modified cosine scoring: "For both the cosine and modified cosine score calculations we ignored all peaks with relative intensities <0.01 compared to the highest intensity peak"
- [results] Pre-selection via precursor m/z matching: "potentially matching spectra were pre-selected based on precursor-m/z matches (tolerance = 1ppm)"
- [results] Minimum matching peaks threshold and ROC curve evaluation: "ignoring scores based on fewer than min_match matching peak ks (here: min_match = 10)"
- [results] High false positive rates in cosine-based methods: "The poorer correlation between cosine and modified cosine similarity and structural similarity can largely be explained by high false positive rates"
- [discussion] Spec2Vec limitation in GC-MS data: "In the present work, we have only demonstrated performance on LC-MS data and not yet assessed Spec2Vec for GC-MS data. For GC-MS, neutral losses are usually not measured."
- [discussion] Retraining requirement when feature coverage is insufficient: "one limitation of Spec2Vec as compared to cosine scores is that it needs training data to learn the fragment peak relationships; however, since this not necessarily needs to be library spectra"
- [methods] Missing fraction threshold to avoid unknown peaks: "By setting a threshold for the missing fraction (e.g. <0.05), returning Spec2Vec similarity scores for spectra far outside the learned peaks (and losses) can be avoided"
- [methods] matchms enables cosine and modified cosine scoring: "the implementations for the cosine score and the modified cosine score used can be found in the Python package matchms"
- [discussion] Spec2Vec use case as pre-selection funnel: "This makes it particularly suited to act as a pre-selection funnel for selecting promising candidates for further exploration using computationally more expensive approaches"
