---
name: mass-spectrum-binning-and-vectorization
description: Use when when preparing MS/MS spectra for neural network training or inference, particularly when you need to feed variable-length spectra into a Siamese network or embedding model that requires fixed-dimensional input.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - matchms
  - pubchempy
  - RDKit
  - Python
  - Python (NumPy/SciPy)
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1186/s13321-021-00558-4
  title: MS2DeepScore
evidence_spans:
- Metadata was cleaned and checked using matchms [18] version 0.8.2, which included cleaning compound names, extracting adduct information from the given metadata, moving metadata to consistent fields
- For each pair of molecular fingerprints Tanimoto scores were calculated, indicating the structural similarity of that pair. (as implemented in matchms [18])
- We then ran an automated search against PubChem [42] using pubchempy [43] for spectra which still missed InChI or SMILES annotations.
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-021-00558-4
  all_source_dois:
  - 10.1186/s13321-021-00558-4
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrum-binning-and-vectorization

## Summary

Convert raw tandem mass spectra into fixed-size numerical vectors by binning peaks into equally-sized m/z intervals and applying intensity transformations. This standardizes spectral representation for machine learning while preserving chemical information relevant to structural similarity prediction.

## When to use

When preparing MS/MS spectra for neural network training or inference, particularly when you need to feed variable-length spectra into a Siamese network or embedding model that requires fixed-dimensional input. Essential when converting from heterogeneous spectrum formats (varying number of peaks, different m/z ranges) into a uniform numerical representation suitable for deep learning.

## When NOT to use

- When spectra require retention of exact peak positions or high-resolution m/z precision (binning loses sub-bin localization)
- If input spectra are already in fragment ion fingerprint or molecular descriptor format
- When the mass range of interest falls outside 10–1000 m/z (e.g., very high m/z or low m/z specialized analyses)

## Inputs

- MS/MS spectra (matchms Spectrum objects or MGF/MSP files)
- Cleaned spectrum metadata including peak lists with m/z and intensity values
- Training dataset specification (to identify bins to retain)

## Outputs

- Fixed-size spectral vectors (1D numpy arrays, 10,000 or ~9,948 dimensions)
- Binned spectrum peak intensity arrays with square-root transformation applied
- Bin index mapping (10–1000 m/z → bin indices)

## How to apply

Bin spectrum peaks into 10,000 equally-sized bins spanning the 10–1000 m/z mass range, selecting the maximum intensity when multiple peaks fall in the same bin. Apply square root transformation to peak intensities to avoid overweighting high-intensity peaks. Remove bins not represented in the training dataset (typically reducing from 10,000 to ~9,948 retained bins). The resulting spectrum is represented as a vector of bin intensities. Use this vectorized representation directly as input to neural network models without computing fingerprints or metadata features (parent mass, formula) separately, as the model learns to extract structural information directly from the binned intensities.

## Related tools

- **matchms** (Load, clean, and standardize spectrum metadata and peak lists prior to binning; provide Spectrum objects as input to vectorization) — https://github.com/matchms/matchms
- **RDKit** (Compute molecular fingerprints and Tanimoto similarity scores as reference labels for training; not used in the binning itself but used post-vectorization for label generation)
- **Python (NumPy/SciPy)** (Perform binning operations, intensity transformations, and vector construction)

## Examples

```
from matchms.importing_utils import load_from_mgf; from matchms.Pipeline import Pipeline, create_workflow; from matchms.filtering.default_pipelines import DEFAULT_FILTERS; pipeline = Pipeline(create_workflow(query_filters=DEFAULT_FILTERS)); spectra = list(load_from_mgf('spectra.mgf')); cleaned = [pipeline.apply_filters(s) for s in spectra]; import numpy as np; vectorized = np.array([spectrum_to_binned_vector(s, bins=10000, mz_min=10, mz_max=1000) for s in cleaned])
```

## Evaluation signals

- Output vectors are exactly 10,000 (or 9,948 if bins not in training data are removed) dimensions with no NaN or infinite values
- Peak intensities fall in [0, 1] range after square-root transformation, with no negative values
- For a given spectrum, the number of non-zero bins matches the count of unique m/z regions containing peaks
- Spectra with identical peak content and intensities produce identical vectorized outputs (deterministic)
- Downstream neural network accepts the vectorized spectra without shape mismatch errors and trains without NaN loss

## Limitations

- Binning resolution of 0.09 m/z per bin (1000 m/z / 10,000 bins) may lose high-resolution structural detail in crowded spectral regions; not suitable for resolving isotope fine structure
- Square root transformation compresses high-intensity peaks; may underrepresent dominant diagnostic ions
- Fixed m/z range (10–1000 Da) excludes very low m/z fragments and high-mass neutral losses; unsuitable for specialized applications requiring extended mass range
- Loss of peak metadata such as annotation strings or scan provenance; vectorization is lossy with respect to original spectrum objects

## Evidence

- [methods] Spectrum peaks were binned in 10,000 equally-sized bins ranging from 10 to 1000 m/z: "Spectrum peaks were binned in 10,000 equally-sized bins ranging from 10 to 1000 m/z"
- [methods] Peak intensities were square root transformed to avoid a too strong focus on the highest intensity peaks only: "Peak intensities were square root transformed to avoid a too strong focus on the highest intensity peaks only"
- [other] Remove bins not represented in training data (9948 of 10,000 bins retained) and output cleaned spectral vectors and metadata: "Remove bins not represented in training data (9948 of 10,000 bins retained) and output cleaned spectral vectors and metadata"
- [results] the neural network was not trained on any spectrum metadata such as parent mass and elemental formula: "the neural network was not trained on any spectrum metadata such as parent mass and elemental formula"
- [other] selecting the maximum intensity when multiple peaks occupy one bin: "selecting maximum intensity per bin when multiple peaks occupy one bin"
