---
name: embedding-space-visualization-and-interpretation
description: Use when after training or loading a pre-trained deep learning model
  that produces high-dimensional embeddings (e.g., 200-dimensional vectors from MS2DeepScore).
  Use this skill when you have a set of spectra with known chemical class annotations
  (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3935
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3361
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

# embedding-space-visualization-and-interpretation

## Summary

Apply dimensionality reduction (t-SNE) to high-dimensional spectral embeddings learned by deep neural networks to visualize chemical structure relationships in low-dimensional space and validate that embeddings encode chemically meaningful features. This skill confirms that learned embeddings cluster compounds of the same chemical superclass together, validating the representational capacity of the model.

## When to use

After training or loading a pre-trained deep learning model that produces high-dimensional embeddings (e.g., 200-dimensional vectors from MS2DeepScore). Use this skill when you have a set of spectra with known chemical class annotations (e.g., ClassyFire superclasses) and want to verify that the learned embeddings capture chemically meaningful structure—i.e., whether unsupervised dimensionality reduction reveals visual clustering by chemical class.

## When NOT to use

- Embeddings are already known to be poorly trained or do not capture chemical structure (e.g., random or trivial embeddings); use other validation approaches first.
- Test set lacks chemical structure annotations (InChIKey, SMILES, or ClassyFire labels); clustering interpretation will be impossible.
- Input spectra are from a single chemical class or are not diverse enough; clustering patterns will not be interpretable.

## Inputs

- trained MS2DeepScore model (or other deep learning model producing spectral embeddings)
- MS/MS spectra dataset (test set, typically 3,500–10,000 spectra)
- chemical structure annotations as InChIKey or ClassyFire chemical superclass labels

## Outputs

- 2D t-SNE coordinate array (numpy array with shape [n_spectra, 2])
- scatter plot visualization with points colored by chemical superclass
- visual confirmation of chemical clustering in embedding space

## How to apply

Load the trained model and compute 200-dimensional spectral embeddings for all test-set spectra using the base network component. Apply t-SNE dimensionality reduction using scikit-learn with metric='cosine', perplexity=100, learning_rate=200, and iterations=1000 to generate 2D coordinates. Retrieve or map ClassyFire chemical superclass annotations for all spectra (via InChIKey lookup). Generate a scatter plot with t-SNE coordinates colored by chemical superclass and visually inspect whether compounds of the same superclass cluster together. If visual clustering is strong and consistent at both superclass and finer subclass resolution, the embeddings are encoding chemically meaningful features.

## Related tools

- **MS2DeepScore** (provides the trained Siamese neural network and base network for computing 200-dimensional spectral embeddings from MS/MS spectra) — https://github.com/matchms/ms2deepscore
- **scikit-learn** (implements t-SNE dimensionality reduction algorithm to project 200D embeddings into 2D coordinates)
- **RDKit** (used to retrieve and process chemical structure information (InChI, SMILES) from InChIKey annotations for mapping ClassyFire superclasses)
- **matchms** (provides spectrum data handling and filtering utilities; may be used for metadata cleanup and InChIKey retrieval) — https://github.com/matchms/matchms

## Examples

```
from ms2deepscore.models import load_model; from sklearn.manifold import TSNE; model = load_model('ms2deepscore_model.pt'); embeddings = model.get_embeddings(test_spectra); tsne = TSNE(metric='cosine', perplexity=100, learning_rate=200, n_iter=1000); coords_2d = tsne.fit_transform(embeddings); import matplotlib.pyplot as plt; plt.scatter(coords_2d[:, 0], coords_2d[:, 1], c=chemical_class_labels); plt.show()
```

## Evaluation signals

- Visual inspection: compounds annotated with the same ClassyFire chemical superclass form tight, well-separated clusters in the t-SNE scatter plot.
- Consistency across granularity: clustering pattern holds at both coarse (superclass) and fine (subclass) resolution levels of chemical classification.
- Separation metrics: compute silhouette score or Davies-Bouldin index on t-SNE coordinates grouped by chemical class; positive silhouette scores and low Davies-Bouldin index indicate good clustering.
- Cross-class proximity: verify that spectra from different chemical superclasses occupy distinct regions of the t-SNE space, with minimal overlap.
- Reproducibility: re-running t-SNE with the same hyperparameters (perplexity, learning_rate, iterations) on the same embeddings produces visually similar cluster patterns (t-SNE is stochastic, but large-scale structure should be stable).

## Limitations

- t-SNE is a stochastic algorithm; different random seeds may produce variations in 2D layout, though large-scale clustering structure should be consistent. Results are sensitive to hyperparameter choices (perplexity, learning_rate, iterations).
- t-SNE visualization is primarily qualitative and not suitable for rigorous quantitative distance inference; distances in 2D space do not necessarily reflect distances in 200D embedding space.
- Clustering interpretation requires high-quality chemical structure annotations; missing or incorrect InChIKey/ClassyFire labels will produce confusing or misleading patterns.
- The embedding space may cluster compounds by features other than chemical class (e.g., instrument type, ionization mode, sample preparation); visual clustering by superclass does not exclude other driving factors.
- Computational cost grows with dataset size; t-SNE on very large test sets (>10,000 spectra) may become slow; alternative methods (UMAP) are faster but were not used in the original study.

## Evidence

- [other] Do the 200-dimensional spectral embeddings learned by MS2DeepScore encode chemically meaningful information that enables molecules of the same chemical class to cluster together in low-dimensional space?: "research_question from task_005"
- [other] Molecules of the same chemical superclass consistently cluster together in t-SNE visualizations of MS2DeepScore embeddings, and this pattern holds at finer resolution for chemical subclasses, confirming that embeddings contain chemically meaningful molecular features.: "finding from task_005"
- [other] Compute 200-dimensional spectral embeddings for all 3,601 test-set spectra using the base network component. Apply t-SNE dimensionality reduction (scikit-learn implementation) with settings: metric='cosine', perplexity=100, learning_rate=200, iterations=1000 to generate 2D coordinates. Retrieve or map ClassyFire chemical superclass annotations for all test-set InChIKeys. Generate a scatter plot with t-SNE coordinates coloured by ClassyFire superclass and verify visual clustering of same-class compounds.: "workflow from task_005"
- [methods] we used the MS2DeepScore base network (Fig. 1) to compute the 200-dimensional spectral embeddings for all 3601 spectra in the test set. Using the t-SNE [28] implementation from scikit-learn [29]: "extraction of methodology for computing embeddings and applying t-SNE"
- [intro] MS2DeepScore can detect compounds of high structural similarity and create mass spectral embeddings for spectral clustering: "justification for embedding utility in chemical clustering"
- [readme] To calculate chemical similarity scores, MS2DeepScore first calculates an embedding (vector) representing each spectrum. This intermediate product can also be used to visualize spectra in "chemical space" by using a dimensionality reduction technique, like UMAP.: "explanation of embedding use for visualization in chemical space"
- [readme] The [tutorial](https://github.com/matchms/ms2deepscore/blob/main/notebooks/MS2DeepScore_tutorial.ipynb) shows how to use these embeddings to create an interactive UMAP with overlaying smiles.: "reference to practical visualization approaches using embeddings"
