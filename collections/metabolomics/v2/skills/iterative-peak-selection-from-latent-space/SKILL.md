---
name: iterative-peak-selection-from-latent-space
description: Use when you have latent low-dimension peak features extracted by a Graph-attention autoencoder from imaging mass spectrometry (IMS) datasets, and you need to automatically identify a ranked subset of marker ions without manual inspection.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - pandas
  - h5py
  - Graph-attention autoencoder
  - scanpy
  - STAGATE
derived_from:
- doi: 10.1021/acs.analchem.4c06210
  title: SMART
evidence_spans:
- pandas
- h5py
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_smartgate_cq
    doi: 10.1021/acs.analchem.4c06210
    title: SMART
  dedup_kept_from: coll_smartgate_cq
schema_version: 0.2.0
---

# iterative-peak-selection-from-latent-space

## Summary

Iteratively select marker ions from imaging mass spectrometry data by ranking and filtering m/z peaks according to their importance or variance in a learned latent feature space. This skill automates the identification of diagnostic peaks when a graph-attention autoencoder has already extracted low-dimensional peak representations.

## When to use

You have latent low-dimension peak features extracted by a Graph-attention autoencoder from imaging mass spectrometry (IMS) datasets, and you need to automatically identify a ranked subset of marker ions without manual inspection. Use this skill when you want to avoid bias in peak selection and require reproducible, data-driven identification of the most informative m/z peaks for spatial metabolomics analysis.

## When NOT to use

- Input latent features are not derived from an autoencoder—use standard univariate peak-picking methods (e.g., signal-to-noise ratio thresholding) instead.
- You require unsupervised peak picking without prior feature extraction—apply classical peak detection algorithms directly to raw mass spectrometry profiles.
- The imaging mass spectrometry dataset lacks spatial structure or has very sparse peak distributions that do not benefit from learned representations.

## Inputs

- latent low-dimension peak features (HDF5 or NumPy array from Graph-attention autoencoder)
- peak metadata (m/z values, iteration count, selection thresholds)
- stopping criterion parameters (target marker count or importance threshold)

## Outputs

- ranked list of marker-ion m/z identifiers (CSV file)
- iteration history and feature importance scores per peak
- final marker-ion selection with metadata

## How to apply

Initialize an empty candidate marker-ion list and set an iteration counter to zero. Load the latent low-dimension peak features from the preceding autoencoder step (typically stored in HDF5 format). In each iteration, apply a peak-selection criterion—such as ranking by feature importance scores or variance in latent space—to identify the top-scoring m/z peaks not yet selected. Add the newly identified peaks to the marker-ion list and update the iteration state. Repeat until a stopping criterion is met (e.g., target number of markers reached, or diminishing returns in feature importance observed). The rationale is that iterative selection prevents redundancy: each successive peak adds complementary information in latent space, ensuring diversity of the final marker set. Export the final ranked list of marker-ion m/z identifiers to a CSV file for downstream analysis.

## Related tools

- **Graph-attention autoencoder** (Extracts latent low-dimension peak features from imaging mass spectrometry datasets prior to peak selection) — https://github.com/zhanglabtools/SmartGate
- **h5py** (Loads and manipulates HDF5-formatted latent feature arrays and peak metadata)
- **pandas** (Manages peak rankings, iteration history, and exports final marker-ion list to CSV)
- **scanpy** (Supports data handling and integration with spatial omics workflows)
- **STAGATE** (Provides spatial graph-attention mechanisms underlying the autoencoder feature extraction)

## Evaluation signals

- Final marker-ion list is ranked by feature importance or variance and is monotonically decreasing in score across iterations.
- No m/z peak appears more than once in the final marker-ion list (uniqueness invariant).
- Stopping criterion is met: either the target number of markers is reached or feature importance scores drop below a pre-specified threshold.
- CSV output contains valid m/z identifiers, iteration counts, and importance scores with no missing or NaN values.
- Marker-ion m/z values are physically plausible (within the expected mass range for the instrument and sample chemistry).

## Limitations

- Performance depends critically on the quality of the upstream Graph-attention autoencoder; poor latent features will yield uninformative marker ions.
- No built-in validation that selected markers are genuinely discriminative for the biological or chemical question at hand; post-hoc validation (e.g., cross-dataset testing, annotation) is recommended.
- Stopping criteria are heuristic (target count or importance threshold); no principled statistical test is provided to determine the optimal number of markers.
- The method assumes that high variance or importance in latent space correlates with biological relevance; this assumption may fail if the autoencoder learns artifacts or spatial noise.

## Evidence

- [other] Load latent low-dimension peak features extracted by the Graph-attention autoencoder from the preceding feature-extraction step: "Load latent low-dimension peak features extracted by the Graph-attention autoencoder from the preceding feature-extraction step."
- [other] In each iteration, apply a peak-selection criterion (e.g., ranked by feature importance or variance in latent space) to identify the top-scoring m/z peaks not yet selected: "In each iteration, apply a peak-selection criterion (e.g., ranked by feature importance or variance in latent space) to identify the top-scoring m/z peaks not yet selected."
- [other] Repeat steps 3–4 until a stopping criterion is met (e.g., target number of markers reached, or diminishing returns observed): "Repeat steps 3–4 until a stopping criterion is met (e.g., target number of markers reached, or diminishing returns observed)."
- [readme] SmartGate could get latent low dimension peak features by Graph-attention autoencoder which help us achieve automic peak picking iteratively to find the marker ions: "SmartGate could get latent low dimension peak features by Graph-attention autoencoder which help us achieve automic peak picking iteratively to find the marker ions."
- [other] Export the final ranked list of marker-ion m/z identifiers to a CSV file: "Export the final ranked list of marker-ion m/z identifiers to a CSV file."
