---
name: latent-feature-interpretation
description: Use when you have imaging mass spectrometry (IMS) data preprocessed into an h5py-backed feature matrix, and a trained graph-attention autoencoder has already extracted latent low-dimensional peak features.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2238
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - pandas
  - h5py
  - Graph-attention autoencoder
  - scanpy
  - STAGATE
  techniques:
  - MS-imaging
  - ion-mobility-MS
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c06210
  all_source_dois:
  - 10.1021/acs.analchem.4c06210
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# latent-feature-interpretation

## Summary

Interpret and rank latent low-dimensional peak features extracted by a graph-attention autoencoder to identify and select marker ions in imaging mass spectrometry datasets. This skill bridges unsupervised feature learning and interpretable marker-ion discovery by using learned latent representations as a ranking criterion for iterative peak selection.

## When to use

You have imaging mass spectrometry (IMS) data preprocessed into an h5py-backed feature matrix, and a trained graph-attention autoencoder has already extracted latent low-dimensional peak features. You need to transform these abstract latent representations into a ranked, actionable list of marker m/z peaks for downstream analysis, and your stopping criterion is either a target count of markers or plateau in selection informativeness.

## When NOT to use

- The latent features have not yet been extracted; use the graph-attention autoencoder feature-extraction workflow first.
- Your IMS dataset is already a reduced feature table (not raw peak data); marker selection from pre-computed features may not benefit from latent reranking.
- You require deterministic, domain-knowledge-driven marker selection (e.g., known metabolite m/z values); latent-feature ranking is data-driven and may conflict with prior knowledge.

## Inputs

- h5py-backed latent low-dimensional peak features (output from graph-attention autoencoder)
- imaging mass spectrometry m/z dataset (referenced by feature index)
- peak selection criterion specification (e.g., importance metric, variance threshold)
- stopping criterion (target marker count or convergence threshold)

## Outputs

- ranked marker-ion m/z identifier list (CSV file)
- iteration history (peak selection counts and scoring per iteration)
- feature importance or variance rankings

## How to apply

Load the latent low-dimensional peak features output by the graph-attention autoencoder (stored in h5py format). Initialize an empty candidate marker-ion list and set an iteration counter. In each iteration, rank all peaks not yet selected according to their feature importance or variance in latent space, then select the top m/z peaks meeting the criterion. Add newly selected peaks to the marker-ion list and update iteration state. Repeat until a stopping criterion is met (e.g., target number of markers reached, or diminishing returns observed in feature variance or importance). Export the final ranked list of marker-ion m/z identifiers to CSV using pandas. The rationale is that latent features capture nonlinear, graph-structured relationships in peak space that raw intensity alone misses, so sorting peaks by their latent-space informativeness yields more discriminative markers than intensity-only ranking.

## Related tools

- **h5py** (load and access latent low-dimensional peak features stored in HDF5 format)
- **pandas** (rank peaks by latent-space criteria, manage marker-ion lists, and export final ranked m/z identifiers to CSV)
- **Graph-attention autoencoder** (upstream feature extractor that produces latent low-dimensional peak features used as input to this skill) — https://github.com/zhanglabtools/SmartGate
- **scanpy** (optional downstream tool for integration with single-cell or spatial transcriptomics workflows)
- **STAGATE** (optional related spatial analysis framework)

## Evaluation signals

- The final marker-ion list has length equal to or approaching the target number of markers specified; iteration stopped at the intended stopping criterion.
- Marker m/z values are non-redundant and distinct; no duplicate m/z identifiers appear in the ranked output.
- Feature importance or variance scores are monotonically decreasing or plateau as iteration progresses, indicating that peaks selected earlier have higher latent-space informativeness.
- The exported CSV file is valid pandas-readable format with columns for m/z identifier, selection rank, and feature importance/variance score.
- Spot-check: manually verify that a subset of top-ranked marker ions correspond to known or biologically plausible metabolite m/z values in the given tissue or sample type.

## Limitations

- Latent-feature ranking is data-driven and hypothesis-free; selected markers may not align with prior domain knowledge or known metabolite m/z databases.
- The quality of marker selection depends critically on the quality and representativeness of the latent features; poorly trained autoencoders will propagate bias into marker ranking.
- No systematic method is provided in the documentation for choosing the stopping criterion (target marker count or convergence threshold); this remains a user choice that affects downstream analysis.
- The iterative peak-picking process is greedy (peaks are selected independently without considering interactions); feature redundancy among selected markers is not explicitly controlled.

## Evidence

- [other] SmartGate obtains latent low-dimension peak features from a graph-attention autoencoder and applies these features in an iterative automatic peak-picking process to identify marker ions in imaging mass spectrometry datasets.: "SmartGate obtains latent low-dimension peak features from a graph-attention autoencoder and applies these features in an iterative automatic peak-picking process to identify marker ions in imaging"
- [other] In each iteration, apply a peak-selection criterion (e.g., ranked by feature importance or variance in latent space) to identify the top-scoring m/z peaks not yet selected.: "In each iteration, apply a peak-selection criterion (e.g., ranked by feature importance or variance in latent space) to identify the top-scoring m/z peaks not yet selected."
- [readme] SmartGate could get latent low dimension peak features by Graph-attention autoencoder which help us achieve automic peak picking iteratively to find the marker ions.: "SmartGate could get latent low dimension peak features by Graph-attention autoencoder which help us achieve automic peak picking iteratively to find the marker ions."
- [other] Load latent low-dimension peak features extracted by the Graph-attention autoencoder from the preceding feature-extraction step.: "Load latent low-dimension peak features extracted by the Graph-attention autoencoder from the preceding feature-extraction step."
- [other] Repeat steps 3–4 until a stopping criterion is met (e.g., target number of markers reached, or diminishing returns observed).: "Repeat steps 3–4 until a stopping criterion is met (e.g., target number of markers reached, or diminishing returns observed)."
