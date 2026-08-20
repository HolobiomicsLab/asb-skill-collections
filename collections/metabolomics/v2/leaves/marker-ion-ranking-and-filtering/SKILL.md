---
name: marker-ion-ranking-and-filtering
description: Use when you have extracted latent low-dimensional peak features from
  imaging mass spectrometry (IMS) data using a graph-attention autoencoder and need
  to identify a ranked subset of marker ions that represent spatial metabolomic patterns.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - pandas
  - h5py
  - Graph-attention autoencoder
  - scanpy
  techniques:
  - MS-imaging
  - ion-mobility-MS
  license_tier: restricted
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

# marker-ion-ranking-and-filtering

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Iteratively rank and select marker ions from imaging mass spectrometry data using latent low-dimensional peak features learned by a graph-attention autoencoder, stopping when a target number of markers is reached or diminishing returns are observed. This skill transforms learned feature representations into an ordered list of biologically or chemically significant m/z peaks for downstream analysis.

## When to use

You have extracted latent low-dimensional peak features from imaging mass spectrometry (IMS) data using a graph-attention autoencoder and need to identify a ranked subset of marker ions that best represent spatial metabolomic patterns. Use this skill when your goal is to reduce dimensionality from hundreds or thousands of m/z peaks to a manageable, interpretable set of biomarker candidates ranked by importance or variance in latent space.

## When NOT to use

- Latent features have not yet been extracted by a graph-attention autoencoder or equivalent dimensionality-reduction model; use the feature-extraction step first.
- Raw imaging mass spectrometry peak data is provided without prior feature learning; this skill operates on learned representations, not raw m/z intensities.
- Input is already a pre-curated, manually validated set of marker ions; this skill is for automated discovery and ranking, not validation of known markers.

## Inputs

- latent low-dimensional peak features (HDF5 .h5 file or NumPy array from graph-attention autoencoder)
- m/z identifiers or peak indices corresponding to the latent features
- target number of marker ions (integer parameter)
- ranking criterion (e.g., 'variance', 'importance_score', or custom scoring function)

## Outputs

- ranked list of marker-ion m/z identifiers (CSV or tabular format)
- ranked scores or importance weights for each selected marker ion
- iteration history / convergence log (optional)

## How to apply

Load the latent low-dimensional peak features (typically stored in HDF5 or NumPy format) output by the graph-attention autoencoder. Initialize an empty marker-ion list and iteration counter. In each iteration, apply a ranking criterion—such as feature importance scores or variance across latent dimensions—to identify the top m/z peaks not yet selected. Add newly selected peaks to the marker list and increment the iteration counter. Repeat until a stopping criterion is satisfied: either the target number of markers is reached, or a diminishing-returns threshold is detected (e.g., marginal gain in variance explained falls below a threshold). Export the final ranked list of m/z identifiers and their scores to a CSV file for validation and downstream use.

## Related tools

- **pandas** (handle and export ranked marker-ion list to CSV; manage iteration state and scoring DataFrames)
- **h5py** (load latent low-dimensional peak features from HDF5 files output by graph-attention autoencoder)
- **Graph-attention autoencoder** (upstream feature extractor that produces the latent low-dimensional peak representations used for ranking) — https://github.com/zhanglabtools/SmartGate
- **scanpy** (general single-cell and spatial omics analysis framework integrated with SmartGate for downstream marker validation)

## Evaluation signals

- Ranked list is exported as valid CSV with m/z identifiers, iteration count, and importance scores; no missing or malformed rows.
- Number of selected markers equals or approaches the target threshold (or stopping criterion is documented and justified).
- Ranking scores are monotonically decreasing or non-increasing across iterations, indicating consistent application of selection criterion.
- Selected m/z peaks show biological or chemical relevance (e.g., known metabolite masses or spatial co-localization patterns) when validated against reference databases or imaging data.
- Diminishing-returns stopping criterion is verifiable: marginal gain in variance or importance between successive iterations falls below the predefined threshold.

## Limitations

- Skill is entirely dependent on the quality of latent features learned by the upstream graph-attention autoencoder; poor feature learning will produce uninformative marker rankings.
- No guidance is provided in the source material on how to set the target number of markers or the diminishing-returns threshold; these are data- and application-dependent hyperparameters.
- Stopping criterion (target number or diminishing returns) must be chosen a priori; the paper does not describe adaptive or data-driven stopping strategies.
- Ranking is based solely on latent-space statistics (variance, importance); biological validation or cross-validation against experimental metadata is external to this skill.

## Evidence

- [other] SmartGate obtains latent low-dimension peak features from a graph-attention autoencoder and applies these features in an iterative automatic peak-picking process to identify marker ions in imaging mass spectrometry datasets.: "SmartGate obtains latent low-dimension peak features from a graph-attention autoencoder and applies these features in an iterative automatic peak-picking process to identify marker ions"
- [other] In each iteration, apply a peak-selection criterion (e.g., ranked by feature importance or variance in latent space) to identify the top-scoring m/z peaks not yet selected.: "apply a peak-selection criterion (e.g., ranked by feature importance or variance in latent space) to identify the top-scoring m/z peaks not yet selected"
- [other] Repeat steps 3–4 until a stopping criterion is met (e.g., target number of markers reached, or diminishing returns observed).: "until a stopping criterion is met (e.g., target number of markers reached, or diminishing returns observed)"
- [other] Export the final ranked list of marker-ion m/z identifiers to a CSV file.: "Export the final ranked list of marker-ion m/z identifiers to a CSV file"
- [readme] SmartGate could get latent low dimension peak features by Graph-attention autoencoder which help us achieve automic peak picking iteratively to find the marker ions.: "latent low dimension peak features by Graph-attention autoencoder which help us achieve automic peak picking iteratively to find the marker ions"
