---
name: spectral-embedding-extraction-from-neural-networks
description: Use when you have a set of preprocessed MS/MS spectra (binned to 10,000
  m/z bins with intensities square-root transformed) and a trained MS2DeepScore Siamese
  neural network model, and you need to compute 200-dimensional spectral embeddings
  for dimensionality reduction, clustering, or chemical space.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - matchms
  - MS2DeepScore
  - scikit-learn
  - Python
  - RDKit
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1186/s13321-021-00558-4
  title: MS2DeepScore
evidence_spans:
- Metadata was cleaned and checked using matchms [18] version 0.8.2, which included
  cleaning compound names
- MS2DeepScore to predict structural similarity scores for spe
- we used the MS2DeepScore base network (Fig. 1) to compute the 200-dimensional spectral
  embeddings for all 3601 spectra in the test set
- Using the t-SNE [28] implementation from scikit-learn [29]
- Using the t-SNE [28] implementation from scikit-learn [29] we computed two-dimensional
  coordinates
- Our MS2DeepScore Python library offers two types of data generators
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2deepscore
    doi: 10.1186/s13321-021-00558-4
    title: MS2DeepScore
  dedup_kept_from: coll_ms2deepscore
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

# spectral-embedding-extraction-from-neural-networks

## Summary

Extract fixed-dimensional dense vector representations (embeddings) from MS/MS spectra using a trained Siamese neural network's base network component. These embeddings encode learned chemically meaningful features and enable downstream tasks such as spectral clustering, visualization, and structural similarity prediction without requiring explicit molecular fingerprint computation.

## When to use

You have a set of preprocessed MS/MS spectra (binned to 10,000 m/z bins with intensities square-root transformed) and a trained MS2DeepScore Siamese neural network model, and you need to compute 200-dimensional spectral embeddings for dimensionality reduction, clustering, or chemical space visualization. Use this skill when you want to move beyond pairwise similarity scores to obtain a dense representation suitable for t-SNE, UMAP, or other manifold learning methods.

## When NOT to use

- Spectra have not been preprocessed or binned; the base network expects input in the fixed 10,000-bin format used during training.
- You need pairwise similarity scores directly; use the full Siamese network's distance head instead of just the base network embeddings.
- You are working with spectra from ionization modes or chemical classes not well represented in the GNPS training data (model generalization may be poor).

## Inputs

- Set of preprocessed MS/MS spectra (binned to 10,000 m/z bins, intensities square-root transformed, peaks < 0.1% of max removed)
- Trained MS2DeepScore Siamese neural network model (base network component)

## Outputs

- 200-dimensional spectral embeddings (numpy array of shape (n_spectra, 200))
- 2D coordinates from t-SNE or UMAP reduction (for visualization)
- Clustering assignments by chemical superclass or subclass (when labels are available)

## How to apply

Load the pretrained MS2DeepScore base network (the first component of the Siamese architecture) and apply it to binned spectra to generate 200-dimensional embeddings. The base network is a convolutional neural network that learns to extract chemically meaningful features directly from binned peak intensities. Pass all test or query spectra through the base network in batch mode to obtain an embedding matrix of shape (n_spectra, 200). The resulting embeddings can then be visualized using t-SNE (with metric='cosine', perplexity=100, learning_rate=200, iterations=1000) to confirm that molecules of the same chemical superclass cluster together, or fed into UMAP for interactive visualization.

## Related tools

- **MS2DeepScore** (Siamese neural network model whose base network component is used to compute spectral embeddings from preprocessed spectra) — https://github.com/matchms/ms2deepscore
- **matchms** (Used to load, clean, filter, and preprocess spectra into the 10,000-bin format required by the base network) — https://github.com/matchms/matchms
- **scikit-learn** (Provides t-SNE implementation for dimensionality reduction and visualization of embeddings) — https://scikit-learn.org
- **Python** (Programming language and runtime for loading the model, computing embeddings, and orchestrating downstream analyses)

## Examples

```
from ms2deepscore.models import load_model
from ms2deepscore import MS2DeepScore

model = load_model("ms2deepscore_model.pt")
ms2ds = MS2DeepScore(model)
embeddings = ms2ds.get_embedding_array(cleaned_spectra)
```

## Evaluation signals

- Embedding array has shape (n_spectra, 200) with no NaN or inf values
- Molecules sharing the same ClassyFire chemical superclass visually cluster together in t-SNE scatter plots (perplexity=100, metric='cosine')
- Clustering pattern holds at finer resolution (chemical subclasses) as well as superclass level
- Embeddings are computed from all test-set spectra (3,601 in the reference) without loss or truncation
- Cosine distance between embeddings of structurally similar compounds (Tanimoto ≥ 0.6) is consistently lower than between unrelated compounds

## Limitations

- The base network was trained on GNPS spectra binned to 10,000 m/z bins; spectra in different formats or mass ranges may require re-binning.
- Embeddings encode chemical structure information but cannot distinguish between spectra from different ionization modes or adducts without additional metadata.
- t-SNE visualization is sensitive to hyperparameter choice (perplexity, learning rate); results may differ with different settings.
- Model generalization to chemical classes underrepresented in the training data (109,734 spectra across 15,062 molecules) is not characterized in the article.
- The 200-dimensional embedding is a lossy compression; information about minor peaks or rare spectral patterns may be discarded.

## Evidence

- [methods] we used the MS2DeepScore base network (Fig. 1) to compute the 200-dimensional spectral embeddings for all 3601 spectra in the test set: "we used the MS2DeepScore base network (Fig. 1) to compute the 200-dimensional spectral embeddings for all 3601 spectra in the test set"
- [other] Molecules of the same chemical superclass consistently cluster together in t-SNE visualizations of MS2DeepScore embeddings, and this pattern holds at finer resolution for chemical subclasses: "Molecules of the same chemical superclass consistently cluster together in t-SNE visualizations of MS2DeepScore embeddings, and this pattern holds at finer resolution for chemical subclasses"
- [methods] Using the t-SNE [28] implementation from scikit-learn [29] we computed two-dimensional coordinates: "Using the t-SNE [28] implementation from scikit-learn [29] we computed two-dimensional coordinates"
- [readme] To calculate chemical similarity scores, MS2DeepScore first calculates an embedding (vector) representing each spectrum. This intermediate product can also be used to visualize spectra in "chemical space" by using a dimensionality reduction technique, like UMAP.: "To calculate chemical similarity scores, MS2DeepScore first calculates an embedding (vector) representing each spectrum. This intermediate product can also be used to visualize spectra in "chemical"
- [other] Apply t-SNE dimensionality reduction (scikit-learn implementation) with settings: metric='cosine', perplexity=100, learning_rate=200, iterations=1000: "Apply t-SNE dimensionality reduction (scikit-learn implementation) with settings: metric='cosine', perplexity=100, learning_rate=200, iterations=1000"
- [methods] Peak intensities were square root transformed to avoid a too strong focus on the highest intensity peaks only: "Peak intensities were square root transformed to avoid a too strong focus on the highest intensity peaks only"
- [methods] Spectrum peaks were binned in 10,000 equally-sized bins ranging from 10 to 1000 m/z: "Spectrum peaks were binned in 10,000 equally-sized bins ranging from 10 to 1000 m/z"
