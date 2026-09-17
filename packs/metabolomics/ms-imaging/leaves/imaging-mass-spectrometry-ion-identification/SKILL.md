---
name: imaging-mass-spectrometry-ion-identification
description: Use when you have imaging mass spectrometry data from spatial metabolomics
  experiments and need to reduce the high-dimensional peak space to a ranked set of
  marker ions for downstream spatial analysis (e.g., tissue region annotation or biomarker
  discovery).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3801
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - pandas
  - h5py
  - Graph-attention autoencoder
  - scanpy
  techniques:
  - MS-imaging
  - ion-mobility-MS
  license_tier: restricted
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# imaging-mass-spectrometry-ion-identification

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Automatically select marker ions from imaging mass spectrometry (IMS) datasets by iteratively ranking m/z peaks according to latent features learned by a graph-attention autoencoder. This skill identifies the most discriminative ions for spatial metabolomics analysis without manual curation.

## When to use

Apply this skill when you have imaging mass spectrometry data from spatial metabolomics experiments and need to reduce the high-dimensional peak space to a ranked set of marker ions for downstream spatial analysis (e.g., tissue region annotation or biomarker discovery). Use it after graph-attention autoencoder feature extraction has produced latent low-dimension peak representations, and you want to avoid exhaustive manual peak selection.

## When NOT to use

- Input peak features have not yet been reduced to latent space by a graph-attention autoencoder—run feature extraction first.
- You have already manually curated a set of marker ions or have a priori biological knowledge of target peaks; manual/knowledge-driven selection may be more appropriate.
- IMS dataset is not spatial or lacks spatial context; this skill is designed for spatial metabolomics, not bulk mass spectrometry.

## Inputs

- latent peak feature matrix (HDF5 format from graph-attention autoencoder)
- original imaging mass spectrometry peak data (m/z values and intensities)
- target marker count or stopping threshold (integer or float)

## Outputs

- ranked CSV file of marker-ion m/z identifiers with selection order
- marker-ion feature importance or ranking scores

## How to apply

Load the latent low-dimension peak features (typically in HDF5 format) extracted by the preceding graph-attention autoencoder step. Initialize an empty marker-ion list and iteration counter. In each iteration, rank all peaks not yet selected by a criterion (e.g., feature importance, variance in latent space, or reconstruction contribution). Select the top m/z peaks scoring highest under this criterion and add them to the marker-ion list. Repeat until a stopping criterion is met—either a target number of markers is reached, or diminishing returns in ranking scores are observed. Export the final ranked list of m/z identifiers to a CSV file for downstream spatial analysis.

## Related tools

- **Graph-attention autoencoder** (Extracts latent low-dimension peak features from imaging mass spectrometry data; feeds feature representations to the peak-picking loop) — https://github.com/zhanglabtools/SmartGate
- **h5py** (Loads and reads latent peak feature matrices stored in HDF5 format)
- **pandas** (Manipulates peak rankings, marker-ion lists, and exports final m/z selections to CSV)
- **scanpy** (Optional: supports downstream spatial analysis and visualization of marker-ion contributions to tissue regions)

## Evaluation signals

- Output CSV contains m/z values in ascending or descending order with no duplicates and matches the target marker count or stopping criterion.
- Ranking scores (feature importance or variance) are monotonically decreasing across iterations, confirming diminishing returns.
- Selected marker ions have been validated against biological ground truth (known biomarkers or tissue-specific metabolites) or show strong spatial correlation with tissue regions in downstream analysis.
- Latent feature dimensionality is consistent with the input HDF5 file schema; no missing or malformed values in the feature matrix.
- Reproducibility: re-running the peak-picking loop with identical feature matrix and parameters produces identical marker-ion rank order.

## Limitations

- Performance depends critically on the quality and interpretability of latent features from the upstream graph-attention autoencoder; poor feature learning will produce suboptimal marker selection.
- Stopping criteria (target marker count, diminishing-returns threshold) are user-specified; no principled automatic threshold is provided in the article.
- No explicit guidance on how to select peak-ranking criterion (importance vs. variance); choice may affect reproducibility and biological relevance of selected ions.
- Skill is demonstrated on spatial metabolomics; generalization to other IMS modalities (e.g., imaging mass cytometry, MALDI-TOF) is not discussed.

## Evidence

- [readme] SmartGate could get latent low dimension peak features by Graph-attention autoencoder which help us achieve automic peak picking iteratively to find the marker ions: "SmartGate could get latent low dimension peak features by Graph-attention autoencoder which help us achieve automic peak picking iteratively to find the marker ions"
- [other] SmartGate obtains latent low-dimension peak features from a graph-attention autoencoder and applies these features in an iterative automatic peak-picking process to identify marker ions in imaging mass spectrometry datasets: "SmartGate obtains latent low-dimension peak features from a graph-attention autoencoder and applies these features in an iterative automatic peak-picking process to identify marker ions in imaging"
- [other] Load latent low-dimension peak features extracted by the Graph-attention autoencoder from the preceding feature-extraction step. Initialize an empty candidate marker-ion list and set iteration counter to zero. In each iteration, apply a peak-selection criterion (e.g., ranked by feature importance or variance in latent space) to identify the top-scoring m/z peaks not yet selected. Add newly selected peaks to the marker-ion list and update iteration state. Repeat steps 3–4 until a stopping criterion is met (e.g., target number of markers reached, or diminishing returns observed). Export the final ranked list of marker-ion m/z identifiers to a CSV file: "Load latent low-dimension peak features extracted by the Graph-attention autoencoder from the preceding feature-extraction step. Initialize an empty candidate marker-ion list and set iteration"
- [readme] spatial metabolomics by introducing an iterative graph attention auto-encoder method SmartGate: "spatial metabolomics by introducing an iterative graph attention auto-encoder method SmartGate"
