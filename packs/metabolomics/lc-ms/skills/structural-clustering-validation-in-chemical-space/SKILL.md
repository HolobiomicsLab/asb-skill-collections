---
name: structural-clustering-validation-in-chemical-space
description: Use when you have trained or loaded a deep learning model that produces high-dimensional spectral embeddings (e.g., 200-dimensional vectors from MS2DeepScore base network) and need to validate that these embeddings capture chemical structure information rather than learning spurious patterns.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3745
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0154
  tools:
  - matchms
  - MS2DeepScore
  - scikit-learn
  - Python
  - RDKit
  techniques:
  - LC-MS
derived_from:
- doi: 10.1186/s13321-021-00558-4
  title: MS2DeepScore
evidence_spans:
- Metadata was cleaned and checked using matchms [18] version 0.8.2, which included cleaning compound names
- MS2DeepScore to predict structural similarity scores for spe
- we used the MS2DeepScore base network (Fig. 1) to compute the 200-dimensional spectral embeddings for all 3601 spectra in the test set
- Using the t-SNE [28] implementation from scikit-learn [29]
- Using the t-SNE [28] implementation from scikit-learn [29] we computed two-dimensional coordinates
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Structural clustering validation in chemical space

## Summary

Validate that learned molecular embeddings encode chemically meaningful information by applying dimensionality reduction to spectral embeddings and verifying that compounds cluster by chemical class. This skill confirms whether an embedding space preserves structural relationships needed for similarity prediction and molecular family discovery.

## When to use

You have trained or loaded a deep learning model that produces high-dimensional spectral embeddings (e.g., 200-dimensional vectors from MS2DeepScore base network) and need to validate that these embeddings capture chemical structure information rather than learning spurious patterns. Apply this skill when classification by chemical superclass or subclass is expected and must be visually confirmed before using embeddings for downstream applications like similarity scoring or database retrieval.

## When NOT to use

- Input embeddings are known to be uninformative (e.g., random initialization or untrained network) — clustering validation will fail trivially.
- Test set contains fewer than ~100 spectra or fewer than 5–10 unique chemical classes — t-SNE may produce misleading patterns with insufficient data.
- Chemical class annotations are incomplete or unreliable — comparison will be meaningless without ground truth.
- Goal is only to compute similarity scores or retrieve spectral matches without concern for interpretability — this skill is validation-focused, not a production similarity measure.

## Inputs

- Trained embedding model (e.g., MS2DeepScore base network)
- Test-set MS/MS spectra (3,600+ spectra recommended)
- InChIKey-to-spectrum mapping or compound metadata
- ClassyFire chemical class annotations

## Outputs

- 2D t-SNE coordinate matrix for test-set embeddings
- Scatter plot colored by chemical superclass/subclass
- Visual clustering assessment report

## How to apply

Load the trained embedding model and compute 200-dimensional spectral embeddings for a test set of spectra (e.g., 3,601 spectra from 500 unique chemical structures). Apply t-SNE dimensionality reduction with cosine distance metric (scikit-learn implementation; recommended settings: perplexity=100, learning_rate=200, iterations=1000) to generate 2D coordinates. Retrieve ClassyFire chemical superclass or subclass annotations for all test-set compounds via InChIKey mapping. Generate a scatter plot coloring points by chemical class and visually inspect for tight clustering of same-class compounds and separation between different classes. Use consistent visual inspection criteria: compounds of the same superclass should form visible clusters, and finer subclass distinctions should be resolvable when zooming or refining annotations.

## Related tools

- **MS2DeepScore** (Trained Siamese neural network that produces 200-dimensional spectral embeddings via its base network component) — https://github.com/matchms/ms2deepscore
- **scikit-learn** (Provides t-SNE implementation for 2D dimensionality reduction of embeddings with cosine metric support)
- **matchms** (Spectrum data loading, cleaning, and metadata management (InChIKey extraction and standardization)) — https://github.com/matchms/matchms
- **RDKit** (Optional: InChI parsing and chemical structure validation via InChIKey)

## Examples

```
from ms2deepscore.models import load_model
from sklearn.manifold import TSNE
import numpy as np

model = load_model('ms2deepscore_model.pt')
embeddings = model.get_embedding_array(test_spectra)  # 3601 x 200
tsne = TSNE(n_components=2, metric='cosine', perplexity=100, learning_rate=200, n_iter=1000, random_state=42)
coords_2d = tsne.fit_transform(embeddings)
# Plot coords_2d colored by ClassyFire superclass labels
```

## Evaluation signals

- Visual inspection: compounds with identical ClassyFire superclass should form a contiguous cluster in the 2D scatter plot with minimal overlap from other classes
- Silhouette score or Davies-Bouldin index on t-SNE coordinates grouped by chemical class — higher silhouette or lower DB index indicates tighter, more separated clusters
- Purity metric: measure the fraction of spectra in each cluster whose chemical class matches the majority class label; purity >0.8 indicates strong clustering
- Class-wise cluster compactness: verify that intra-class distances in t-SNE space are significantly smaller than inter-class distances (e.g., median within-class distance <20% of median between-class distance)
- Reproduction of known chemical families: confirm that compounds from well-characterized chemical families (e.g., alkaloids, lipids, phenolics) form visually distinct, expected groupings

## Limitations

- t-SNE results are stochastic and sensitive to hyperparameters (perplexity, learning_rate); different runs may produce different layouts. Use fixed random seed for reproducibility.
- t-SNE distorts global structure; local clustering may be accurate while inter-cluster relationships are not preserved. UMAP may be more reliable for assessing global separation.
- ClassyFire annotations may be incomplete or incorrect for some spectra, introducing noise. Validate annotation quality independently.
- Validation is visual and subjective; no single quantitative threshold definitively proves embeddings are 'good.' Combine with downstream task performance (e.g., similarity prediction accuracy) for full assessment.
- The method does not guarantee that embeddings are optimal for all downstream tasks; good clustering by chemical class does not imply good performance on fine-grained similarity tasks or cross-ionization-mode prediction.

## Evidence

- [other] research_question: "Do the 200-dimensional spectral embeddings learned by MS2DeepScore encode chemically meaningful information that enables molecules of the same chemical class to cluster together in low-dimensional"
- [other] finding: "Molecules of the same chemical superclass consistently cluster together in t-SNE visualizations of MS2DeepScore embeddings, and this pattern holds at finer resolution for chemical subclasses,"
- [other] method_summary: "Compute 200-dimensional spectral embeddings for all 3,601 test-set spectra using the base network component. Apply t-SNE dimensionality reduction (scikit-learn implementation) with settings:"
- [other] annotation_integration: "Retrieve or map ClassyFire chemical superclass annotations for all test-set InChIKeys. Generate a scatter plot with t-SNE coordinates coloured by ClassyFire superclass and verify visual clustering of"
- [readme] embedding_extraction: "To calculate chemical similarity scores, MS2DeepScore first calculates an embedding (vector) representing each spectrum. This intermediate product can also be used to visualize spectra in "chemical"
- [methods] tsne_parameters: "Using the t-SNE [28] implementation from scikit-learn [29] we computed two-dimensional coordinates"
