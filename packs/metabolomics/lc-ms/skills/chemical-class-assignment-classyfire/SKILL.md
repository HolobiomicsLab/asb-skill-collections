---
name: chemical-class-assignment-classyfire
description: Use when you have computed low-dimensional embeddings (e.g., t-SNE coordinates) or clusterings of mass spectra and need to validate that the learned representation space organizes molecules by chemical taxonomy.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3520
  tools:
  - matchms
  - MS2DeepScore
  - scikit-learn
  - Python
  - RDKit
  - ClassyFire
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

# chemical-class-assignment-classyfire

## Summary

Retrieve or map ClassyFire chemical superclass and subclass annotations for molecular structures (via InChIKey) to enable chemically meaningful stratification and validation of spectral embeddings or clustering results. This skill verifies that learned representations capture true chemical structure relationships by confirming class-level coherence in dimensionality-reduced visualizations.

## When to use

You have computed low-dimensional embeddings (e.g., t-SNE coordinates) or clusterings of mass spectra and need to validate that the learned representation space organizes molecules by chemical taxonomy. Use this skill when you want to move beyond numerical similarity metrics and ask: 'Do spectra of the same chemical superclass or subclass co-locate in the embedding space?'

## When NOT to use

- Your spectra lack InChIKey metadata or reliable chemical structure annotations—ClassyFire mapping requires unambiguous molecular identifiers.
- You are interested only in spectral similarity (fragment ion matching) and not in the chemical structural meaning of the learned embeddings.
- Your embedding dimensionality is very high (>50) and you have not yet applied dimensionality reduction; visualizing 200-dim embeddings directly without t-SNE/UMAP obscures class-level patterns.

## Inputs

- 200-dimensional spectral embeddings (e.g., base network activations from MS2DeepScore)
- 2D coordinates from dimensionality reduction (e.g., t-SNE output with cosine metric, perplexity=100, learning_rate=200, iterations=1000)
- Spectrum metadata including InChIKey identifiers (or SMILES/InChI for chemical lookup)
- Test-set spectra (e.g., 3,601 spectra from 500 unique InChIKeys)

## Outputs

- Scatter plot or visualization with 2D embedding coordinates colored by ClassyFire superclass or subclass
- Qualitative assessment of chemical class coherence (presence/absence of visual clustering by class)
- Optional: quantitative clustering metrics (e.g., silhouette score, purity, or Davies–Bouldin index computed against class labels)

## How to apply

For each spectrum in your test set, retrieve its InChIKey identifier from the spectrum metadata. Use the InChIKey to query ClassyFire chemical ontology annotations (superclass and subclass labels). Once annotations are retrieved or mapped, generate a scatter plot or similar visualization with your embedding coordinates (e.g., t-SNE 2D points) and color by ClassyFire superclass or subclass. Examine whether molecules of the same chemical class form visually coherent clusters. If coherence is high (same-class compounds group together without excessive intermingling with other classes), this provides evidence that the embedding learned chemically meaningful molecular features.

## Related tools

- **ClassyFire** (Chemical ontology resource for retrieving standardized superclass and subclass annotations by InChIKey lookup)
- **scikit-learn** (t-SNE dimensionality reduction implementation (metric='cosine', perplexity=100, learning_rate=200, iterations=1000) to convert 200-dim embeddings to 2D plottable coordinates) — https://scikit-learn.org
- **MS2DeepScore** (Base network component that computes 200-dimensional spectral embeddings from MS/MS spectra) — https://github.com/matchms/ms2deepscore
- **matchms** (Spectral data handling and metadata cleaning (e.g., extracting or validating InChIKey from spectrum objects)) — https://github.com/matchms/matchms
- **RDKit** (Optional: chemical structure parsing and validation when converting InChIKey to molecular fingerprints for additional structural analysis)

## Examples

```
from ms2deepscore.models import load_model
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

model = load_model('ms2deepscore_model.pt')
embeddings_200d = model.get_embedding_array(spectra)  # 3601 x 200 array
tsne = TSNE(n_components=2, metric='cosine', perplexity=100, learning_rate=200, n_iter=1000, random_state=42)
embeddings_2d = tsne.fit_transform(embeddings_200d)

# Retrieve ClassyFire superclass for each spectrum's InChIKey
superclasses = [classyfire_lookup(s.metadata['inchikey']) for s in spectra]
plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1], c=superclasses, cmap='tab20')
plt.xlabel('t-SNE 1')
plt.ylabel('t-SNE 2')
plt.title('MS2DeepScore Embeddings Colored by ClassyFire Superclass')
plt.show()
```

## Evaluation signals

- Visual inspection: molecules bearing the same ClassyFire superclass form tight, spatially localized clusters in the t-SNE scatter plot with minimal overlap from other classes.
- Class-level separation: finer chemical subclass labels also show coherent sub-clustering (hierarchical structure in the visualization), suggesting the embedding captures multi-scale chemical features.
- Quantitative coherence metric (optional): silhouette score or Davies–Bouldin index computed using ClassyFire labels as ground truth shows positive silhouette coefficient (>0.3) or low Davies–Bouldin index, indicating compact within-class and separated between-class structure.
- Metadata completeness: ≥95% of test-set spectra successfully map to ClassyFire annotations via InChIKey (no missing or ambiguous lookups).
- Absence of extreme outliers: no single compound class is scattered across the entire plot, and largest class-specific clusters contain >50% of class members.

## Limitations

- ClassyFire annotations depend on accurate InChIKey identifiers in spectrum metadata; missing or erroneous InChIKeys will result in failed mappings or incorrect class assignments.
- Chemical class coherence is a necessary but not sufficient condition for embedding quality; good class separation does not guarantee the embeddings encode subtle structural differences or are useful for downstream tasks.
- t-SNE is stochastic and parameter-sensitive (perplexity, learning_rate); different hyperparameter settings may produce different visual clustering patterns, so reproducibility requires fixed random seeds and documented parameters.
- The skill assumes ClassyFire ontology is comprehensive and stable; compounds not covered by ClassyFire or assigned to broad superclasses (e.g., 'organic compounds') may not provide discriminative signals.
- Visualization alone is qualitative; cluster coherence interpretation is subjective and may not scale to datasets with >500 unique classes or highly imbalanced class distributions.

## Evidence

- [other] research_question from task_005: "Do the 200-dimensional spectral embeddings learned by MS2DeepScore encode chemically meaningful information that enables molecules of the same chemical class to cluster together in low-dimensional"
- [other] finding from task_005: "Molecules of the same chemical superclass consistently cluster together in t-SNE visualizations of MS2DeepScore embeddings, and this pattern holds at finer resolution for chemical subclasses,"
- [other] workflow step 2 from task_005: "Compute 200-dimensional spectral embeddings for all 3,601 test-set spectra using the base network component."
- [other] workflow step 3 from task_005: "Apply t-SNE dimensionality reduction (scikit-learn implementation) with settings: metric='cosine', perplexity=100, learning_rate=200, iterations=1000 to generate 2D coordinates."
- [other] workflow step 4 from task_005: "Retrieve or map ClassyFire chemical superclass annotations for all test-set InChIKeys."
- [other] workflow step 5 from task_005: "Generate a scatter plot with t-SNE coordinates coloured by ClassyFire superclass and verify visual clustering of same-class compounds."
- [methods] Methods section on t-SNE from article: "we used the MS2DeepScore base network (Fig. 1) to compute the 200-dimensional spectral embeddings for all 3601 spectra in the test set. Using the t-SNE [28] implementation from scikit-learn [29] we"
