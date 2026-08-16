---
name: dimensionality-reduction-t-sne
description: Use when you have computed high-dimensional embeddings (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3935
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3372
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

# dimensionality-reduction-t-sne

## Summary

Apply t-SNE (t-distributed Stochastic Neighbor Embedding) to project high-dimensional spectral embeddings into 2D space for visual inspection of chemical clustering and validation that learned representations preserve chemically meaningful structure.

## When to use

You have computed high-dimensional embeddings (e.g., 200-dimensional spectral vectors from a neural network base) and need to verify that molecules of the same chemical class or superclass cluster together visually, or when you want to generate a 2D scatter plot colored by chemical annotation to assess whether the embedding space encodes chemical similarity.

## When NOT to use

- Embeddings are already known to be poor quality or untrainable; t-SNE will faithfully project garbage data but will not validate quality.
- No chemical annotations or ground-truth labels are available; t-SNE is useful for supervised or semi-supervised quality checks but cannot assess clustering without reference classes.
- You need quantitative clustering metrics (silhouette score, Davies–Bouldin index, etc.); t-SNE visualization is qualitative and should be paired with formal metrics if rigor is required.

## Inputs

- High-dimensional spectral embeddings (200-dimensional vectors, one per spectrum)
- Test set spectra (MS/MS mass spectra in standardized format)
- Chemical class annotations (ClassyFire superclass/subclass labels mapped by InChIKey)

## Outputs

- 2D t-SNE coordinate array (one (x, y) pair per spectrum)
- Scatter plot visualization with t-SNE coordinates colored by chemical class
- Qualitative assessment of embedding quality (whether chemical similarity is preserved)

## How to apply

Load the pre-trained MS2DeepScore model and compute 200-dimensional spectral embeddings for your test spectra using the base network component. Apply t-SNE dimensionality reduction using scikit-learn with metric='cosine' (to preserve cosine distances in the high-dimensional space), perplexity=100 (balancing local and global structure), learning_rate=200, and iterations=1000 to generate 2D coordinates. Retrieve ClassyFire chemical annotations (superclass or subclass) for all spectra by InChIKey lookup. Generate a scatter plot with t-SNE x/y coordinates as axes and color points by chemical superclass or subclass. Visually inspect the resulting plot: consistent clustering of same-class compounds validates that the 200-dimensional embeddings capture chemically meaningful molecular features beyond spectral noise.

## Related tools

- **MS2DeepScore** (Compute 200-dimensional spectral embeddings from test spectra via base network component) — https://github.com/matchms/ms2deepscore
- **scikit-learn** (Provides t-SNE implementation with configurable metric, perplexity, learning rate, and iteration parameters)
- **matchms** (Handles spectrum data loading and metadata cleaning prior to embedding computation) — https://github.com/matchms/matchms

## Examples

```
from ms2deepscore.models import load_model
from sklearn.manifold import TSNE
import numpy as np

model = load_model('ms2deepscore_model.pt')
embeddings = model.get_embedding_array(test_spectra)  # shape: (3601, 200)
tsne = TSNE(n_components=2, metric='cosine', perplexity=100, learning_rate=200, n_iter=1000)
coords_2d = tsne.fit_transform(embeddings)
# coords_2d is (3601, 2); color by ClassyFire superclass and plot
```

## Evaluation signals

- Spectra from the same ClassyFire chemical superclass form visually distinct, well-separated clusters in the 2D scatter plot.
- Clustering structure persists at finer resolution (chemical subclass) without fragmentation into spurious islands.
- No major misclassifications: spectra from different superclasses are not intermixed within cluster cores.
- t-SNE convergence: training loss plateaus within the specified 1000 iterations, indicating stable 2D projection.
- Reproducibility check: re-running t-SNE with the same seed produces identical coordinate assignments and cluster layouts.

## Limitations

- t-SNE is a stochastic algorithm; results depend on random initialization and hyperparameter choice (perplexity, learning_rate). Small seed changes can alter cluster appearance, though overall structure should be preserved.
- t-SNE may create artificial structure in sparse or uniformly distributed embeddings; visually tight clusters do not automatically confirm embedding quality without quantitative metrics.
- Computational cost scales poorly for very large datasets (e.g., >10,000 spectra) and may require subsampling or alternative methods (e.g., UMAP).
- The visualization is sensitive to perplexity setting; values too small or too large can obscure true clustering or create over-fragmentation. Perplexity=100 is tuned for ~3,600 spectra but may require adjustment for other dataset sizes.

## Evidence

- [other] Molecules of the same chemical superclass consistently cluster together in t-SNE visualizations of MS2DeepScore embeddings, and this pattern holds at finer resolution for chemical subclasses: "Molecules of the same chemical superclass consistently cluster together in t-SNE visualizations of MS2DeepScore embeddings, and this pattern holds at finer resolution for chemical subclasses,"
- [other] Apply t-SNE dimensionality reduction with metric='cosine', perplexity=100, learning_rate=200, and iterations=1000 to generate 2D coordinates: "Apply t-SNE dimensionality reduction (scikit-learn implementation) with settings: metric='cosine', perplexity=100, learning_rate=200, iterations=1000 to generate 2D coordinates."
- [other] Compute 200-dimensional spectral embeddings for all 3,601 test-set spectra using the base network component: "Compute 200-dimensional spectral embeddings for all 3,601 test-set spectra using the base network component."
- [other] Retrieve or map ClassyFire chemical superclass annotations for all test-set InChIKeys: "Retrieve or map ClassyFire chemical superclass annotations for all test-set InChIKeys."
- [methods] Using the t-SNE implementation from scikit-learn we computed two-dimensional coordinates: "Using the t-SNE [28] implementation from scikit-learn [29] we computed two-dimensional coordinates"
- [readme] To calculate chemical similarity scores, MS2DeepScore first calculates an embedding (vector) representing each spectrum. This intermediate product can also be used to visualize spectra in 'chemical space' by using a dimensionality reduction technique, like UMAP.: "To calculate chemical similarity scores, MS2DeepScore first calculates an embedding (vector) representing each spectrum. This intermediate product can also be used to visualize spectra in "chemical"
