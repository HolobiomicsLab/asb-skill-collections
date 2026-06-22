---
name: spectrum-pair-retrieval-and-ranking
description: Use when you have a test set of annotated MS/MS spectra with known structural similarity (via molecular fingerprints or InChIKey), and you want to assess how well a spectral similarity measure (learned or classical) retrieves structurally related compound pairs across a full range of thresholds.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - MS2DeepScore
  - Spec2Vec
  - RDKit
  - Python
  - scikit-learn
  - matchms
derived_from:
- doi: 10.1186/s13321-021-00558-4
  title: MS2DeepScore
evidence_spans:
- Our MS2DeepScore Python library offers two types of data generators
- To estimate the uncertainty of a prediction we used Monte-Carlo Dropout ensembles
- recently introduced unsupervised Spec2V
- Unless noted otherwise, we used Tanimoto scores on RDKit [23] Daylight fingerprints (2048 bits) to compute structural similarities.
- Unless noted otherwise, we used Tanimoto scores on RDKit [23] Daylight fingerprints (2048 bits) to compute structural similarities
- Our MS2DeepScore Python library offers two types of data generators, one which iterates over all unique InChIKeys (DataGeneratorAllInchikeys) and one which iterates over all spectra and was used for
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2deepscore_cq
    doi: 10.1186/s13321-021-00558-4
    title: MS2DeepScore
  dedup_kept_from: coll_ms2deepscore_cq
schema_version: 0.2.0
---

# Spectrum pair retrieval and ranking

## Summary

Retrieve and rank all unique spectrum pairs from a spectral library by computing pairwise similarity scores (MS2DeepScore, Spec2Vec, or modified cosine), then evaluate retrieval performance by thresholding similarity scores and comparing precision-recall trade-offs against structural similarity labels (Tanimoto fingerprints). This skill enables benchmarking of spectral similarity measures for their ability to identify structurally related compounds.

## When to use

You have a test set of annotated MS/MS spectra with known structural similarity (via molecular fingerprints or InChIKey), and you want to assess how well a spectral similarity measure (learned or classical) retrieves structurally related compound pairs across a full range of thresholds. Use this when you need precision-recall curves or when comparing multiple similarity measures on the same dataset.

## When NOT to use

- Input spectra lack chemical structure annotations (InChIKey, SMILES, or InChI). Tanimoto labels cannot be computed without molecular fingerprints.
- You need to rank individual query spectra against a library in real time (use single-query retrieval instead).
- Your goal is to optimize hyperparameters of the similarity model itself rather than evaluate a fixed, trained model.

## Inputs

- MS/MS spectrum file (MGF, MSP, mzML, or mzXML format) with ≥3500 spectra
- Metadata: InChIKey or SMILES annotations for all spectra
- Trained spectral similarity model (e.g., MS2DeepScore Siamese network weights) OR classical similarity metric (Spec2Vec, modified cosine)

## Outputs

- Pairwise similarity matrix (N × N, real values in [0, 1])
- Structural similarity labels (N × N Tanimoto scores computed from RDKit fingerprints)
- Precision-recall curves (one per similarity method)
- Summary metrics: AUC, max precision at given recall, max recall at given precision

## How to apply

First, load the test set of spectra and compute all unique spectrum pairs (for N spectra, N*(N-1)/2 pairs). Generate similarity scores for each pair using your chosen spectral similarity method (e.g., MS2DeepScore embeddings via cosine similarity, Spec2Vec, or modified cosine). In parallel, compute structural similarity labels for all pairs using RDKit Daylight fingerprints (2048 bits) and Tanimoto distance, then define high-similarity pairs as those with Tanimoto > 0.6 (or your chosen threshold). For each spectral similarity measure, sweep the score threshold from 0 to 1.0 in steps, and at each threshold record precision (high-similarity pairs retrieved / total pairs selected) and recall (high-similarity pairs retrieved / all high-similarity pairs). Plot precision-recall curves for all methods to visualize trade-offs and identify which method maximizes the area under the curve or achieves the best precision-recall balance for your use case.

## Related tools

- **MS2DeepScore** (Compute deep-learned spectral similarity scores via Siamese network embeddings and cosine distance) — https://github.com/matchms/ms2deepscore
- **Spec2Vec** (Compute unsupervised spectral similarity scores for baseline comparison)
- **RDKit** (Generate Daylight fingerprints (2048 bits) and compute Tanimoto structural similarity labels)
- **matchms** (Clean, normalize, and parse spectrum metadata; provide Spectrum objects for processing) — https://github.com/matchms/matchms
- **scikit-learn** (Compute precision-recall metrics and plot curves)
- **Python** (Orchestrate pair generation, similarity computation, threshold sweeps, and curve plotting)

## Examples

```
from ms2deepscore.models import load_model; from ms2deepscore import MS2DeepScore; model = load_model('ms2deepscore_model.pt'); ms2ds = MS2DeepScore(model); embeddings = ms2ds.get_embedding_array(spectra); import numpy as np; similarity_matrix = np.dot(embeddings, embeddings.T); from sklearn.metrics import precision_recall_curve; precision, recall, _ = precision_recall_curve(tanimoto_labels.flatten(), similarity_matrix.flatten())
```

## Evaluation signals

- Total number of unique spectrum pairs computed equals N*(N-1)/2 for N test spectra (e.g., 6,485,401 pairs for 3,601 spectra).
- Similarity scores are in the range [0, 1] with no NaN or infinite values; Tanimoto labels are also in [0, 1].
- Precision-recall curves are monotonically decreasing (or non-increasing): as the similarity threshold lowers and more pairs are selected, recall increases but precision decreases.
- Precision-recall curves for superior methods (e.g., MS2DeepScore) lie to the upper-right of inferior baselines (e.g., modified cosine), demonstrating better precision-recall trade-off.
- At a fixed high-similarity threshold (e.g., Tanimoto > 0.6), the method correctly identifies ≥80% of true positive pairs (indicating recall) while minimizing false positives (indicating precision).

## Limitations

- Computational cost grows as O(N²) for N spectra; for 3,601 spectra, ~6.5M pairs must be computed, requiring hours to days depending on hardware.
- Precision-recall evaluation depends critically on the structural similarity label (Tanimoto threshold = 0.6); if this threshold is misaligned with your application's definition of 'related,' results may not generalize.
- MS2DeepScore and other learned models may exhibit poor performance on spectra from ionization modes or mass ranges not present in training data.
- The test set must contain sufficient diversity and balanced representation of high and low structural similarity pairs; skewed datasets yield misleading precision-recall curves.
- Spectrum metadata (parent mass, adduct, elemental formula) are not used in MS2DeepScore training, potentially limiting interpretability for metadata-rich applications.

## Evidence

- [methods] Computed all 6,485,401 unique spectrum pairs: "Load the test set of 3601 spectra and compute all 6,485,401 unique spectrum pairs."
- [methods] Generate similarity scores via MS2DeepScore embeddings and cosine similarity: "Generate MS2DeepScore embeddings for each spectrum using the trained Siamese base network and compute cosine similarity scores."
- [methods] Structural labels computed with RDKit Daylight fingerprints: "Calculate Tanimoto structural similarity labels for all pairs using RDKit Daylight fingerprints (2048 bits)."
- [methods] Threshold sweep from 0 to 1.0 to compute precision and recall at each threshold: "For each spectral similarity measure, vary the similarity threshold from 0 to 1.0 and compute precision (high-similarity pairs retrieved / total pairs selected) and recall (high-similarity pairs"
- [other] MS2DeepScore outperforms baselines across full precision-recall range: "MS2DeepScore outperforms both modified Cosine and Spec2Vec across the full precision-recall range for identifying structurally related compounds, achieving notably better precision/recall"
- [methods] Precision-recall curves enable comparison of spectral similarity measures: "Generate precision-recall curves for all three methods and compare the trade-offs reported in Figure 4."
- [readme] README: compute MS2DeepScore similarities and embeddings from spectra: "To compute the similarities between spectra of your choice you can run the code below. There is a small example dataset available in the folder "./tests/resources/pesticides_processed.mgf"."
