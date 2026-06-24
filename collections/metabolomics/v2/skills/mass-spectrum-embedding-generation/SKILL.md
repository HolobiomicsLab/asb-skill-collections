---
name: mass-spectrum-embedding-generation
description: Use when you have cleaned MS/MS spectra (in formats like .mgf, .msp,
  .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - MS2DeepScore
  - RDKit
  - Python
  - scikit-learn
  - matchms
  - UMAP
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1186/s13321-021-00558-4
  title: MS2DeepScore
evidence_spans:
- Our MS2DeepScore Python library offers two types of data generators
- To estimate the uncertainty of a prediction we used Monte-Carlo Dropout ensembles
- Unless noted otherwise, we used Tanimoto scores on RDKit [23] Daylight fingerprints
  (2048 bits) to compute structural similarities.
- Unless noted otherwise, we used Tanimoto scores on RDKit [23] Daylight fingerprints
  (2048 bits) to compute structural similarities
- Our MS2DeepScore Python library offers two types of data generators, one which iterates
  over all unique InChIKeys (DataGeneratorAllInchikeys) and one which iterates over
  all spectra and was used for
- Using the t-SNE [28] implementation from scikit-learn [29] we computed two-dimensional
  coordinates
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrum-embedding-generation

## Summary

Generate fixed-dimensional vector embeddings from tandem mass spectrometry (MS/MS) spectra using a trained Siamese neural network, enabling downstream chemical similarity scoring and spectral clustering in continuous vector space.

## When to use

You have cleaned MS/MS spectra (in formats like .mgf, .msp, .mzML) and need to convert them into numerical embeddings for: (1) computing structural similarity scores between spectrum pairs via cosine distance or other metrics, (2) visualizing spectra in chemical space using dimensionality reduction (e.g., UMAP, t-SNE), or (3) clustering spectra by chemical structure without access to molecular fingerprints.

## When NOT to use

- You already have reference Tanimoto scores or molecular fingerprints and do not need embedding visualization.
- Input spectra are not cleaned or preprocessed (raw spectra with noise and outlier peaks will degrade embedding quality).
- You require embeddings from spectra in ionization modes significantly different from the training distribution (cross-ionization predictions are supported in MS2DeepScore 2.0+, but earlier versions are mode-specific).

## Inputs

- Collection of cleaned MS/MS spectra (matchms Spectrum objects or mgf/msp file)
- Pre-trained MS2DeepScore model checkpoint (.pt file)
- Spectrum metadata (optional, for ionization mode and precursor m/z if using enhanced model)

## Outputs

- Embedding array: 2D numpy array of shape (n_spectra, 200) containing 200-dimensional vectors
- Per-spectrum embedding vectors suitable for similarity computation and visualization

## How to apply

Load a pre-trained MS2DeepScore model (a Siamese neural network trained on >500,000 annotated MS/MS spectra) and pass your cleaned spectrum collection through the model's embedding layer to produce 200-dimensional vector representations. The model accepts binned spectra (peaks in 10,000 equally-sized bins from 10–1000 m/z with intensities square-root transformed) and outputs one embedding per spectrum. These embeddings can then be compared directly via cosine similarity to obtain predicted Tanimoto scores, or visualized and clustered in the embedding space. The embedding approach is preferred over computing reference Tanimoto scores from RDKit Daylight fingerprints when molecular structures are unavailable or when you want to leverage the model's learned spectral patterns.

## Related tools

- **MS2DeepScore** (Pre-trained Siamese neural network model that produces spectral embeddings from MS/MS spectrum pairs) — https://github.com/matchms/ms2deepscore
- **matchms** (Spectrum data container, filtering, and I/O for loading and cleaning spectra before embedding) — https://github.com/matchms/matchms
- **UMAP** (Dimensionality reduction for visualizing high-dimensional embeddings in 2D/3D chemical space)
- **scikit-learn** (t-SNE implementation for alternative dimensionality reduction and clustering of embeddings)

## Examples

```
from ms2deepscore.models import load_model
from ms2deepscore import MS2DeepScore
model = load_model("ms2deepscore_model.pt")
ms2ds = MS2DeepScore(model)
embeddings = ms2ds.get_embedding_array(cleaned_spectra)
```

## Evaluation signals

- Embedding array shape is (n_spectra, 200) with no NaN or infinite values.
- Cosine similarity between embeddings of spectra from the same compound (same InChIKey) clusters near 1.0; dissimilar spectra cluster near 0.0.
- Predicted Tanimoto scores derived from embeddings (via cosine similarity) have RMSE ≤ 0.15 against reference RDKit Daylight fingerprints on held-out test spectra (3597 spectra of 500 unique InChIKeys).
- UMAP/t-SNE projections of embeddings show coherent spatial grouping of structurally similar compounds.
- Embedding generation completes in <5 minutes for 500–1000 spectra on a standard laptop (no GPU required).

## Limitations

- Model was trained on MS/MS spectra from GNPS, MoNA, MassBank, and MSnLib; performance may degrade on spectra from underrepresented compound classes or ionization methods not well covered in training data.
- Embeddings do not capture explicit molecular structure information; they learn spectral patterns associated with molecular fingerprints, so novel or highly unusual compounds may not be well-represented.
- MS2DeepScore versions prior to 2.0 are ionization-mode-specific; cross-ionization mode predictions require version 2.0 or higher.
- Spectrum metadata such as parent mass and elemental formula were not used during training, so the embeddings rely solely on spectral peak patterns; adding metadata constraints requires model retraining.
- Embeddings are fixed at 200 dimensions; no mechanism to adjust dimensionality without retraining the underlying Siamese network.

## Evidence

- [intro] MS2DeepScore can create mass spectral embeddings that can be used for spectral clustering: "can create mass spectral embeddings that can be used for additional spectral clustering"
- [methods] Siamese network outputs 200-dimensional embeddings for spectrum pairs: "generate N=10 forward passes through the network with dropout rate 0.2 to create an ensemble of 200-dimensional spectral embeddings"
- [results] Embeddings can be used with dimensionality reduction for visualization: "Using the t-SNE [28] implementation from scikit-learn [29] we computed two-dimensional coordinates for all spectra"
- [methods] Embeddings enable downstream structural similarity prediction: "Compute cosine similarity between paired embeddings for each of the 10 ensemble members, yielding 10 structural similarity predictions per spectrum pair"
- [readme] Pre-trained model available for inference without additional training: "This model can be downloaded from [from zenodo here](https://zenodo.org/records/17826815). Only the ms2deepscore_model.pt is needed."
- [methods] Embeddings are extracted after binning and transformation of spectra: "Spectrum peaks were binned in 10,000 equally-sized bins ranging from 10 to 1000 m/z"
- [readme] Expected embedding derivation workflow in README: "ms2ds_model = MS2DeepScore(model)
ms2ds_embeddings = ms2ds_model.get_embedding_array(cleaned_spectra)"
