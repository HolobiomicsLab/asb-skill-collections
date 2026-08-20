---
name: hierarchical-clustering-euclidean-complete-linkage
description: Use when you have a normalized microbe-metabolite feature attribution
  score matrix (rows = microbes, columns = metabolites) and need to explore hierarchical
  structure and visually assess similarity patterns before determining the optimal
  number of clusters via consensus clustering.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3174
  - http://edamontology.org/topic_3407
  tools:
  - Seaborn clustermap
  - Hierarchical clustering (Euclidean distance, complete linkage)
  - Consensus clustering
  - Python
  - Cytoscape
  - scipy.cluster.hierarchy
  - scikit-learn linkage functions
  - MiMeNet
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1371/journal.pcbi.1009021
  title: MiMeNet
evidence_spans:
- linkage using Seaborn’s clustermap function in
- cluster microbes (rows) and metabolites (columns) separately based on the Euclidean
  distance and complete linkage
- for each fixed k, ranged from 2 to 20, a k-clustering of the rows using each normalized
  S was generated. Then a consensus matrix M(k) was calculated as the mean connectivity
  matrix across all
- using Python's sci-kit-learn package
- Networks showing microbe and metabolite modules and the interactions between them
  were constructed using Cytoscape
- Networks showing the modules and the interactions between them were constructed
  using Cytoscape
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mimenet_cq
    doi: 10.1371/journal.pcbi.1009021
    title: MiMeNet
  dedup_kept_from: coll_mimenet_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1009021
  all_source_dois:
  - 10.1371/journal.pcbi.1009021
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# hierarchical-clustering-euclidean-complete-linkage

## Summary

Hierarchical clustering using Euclidean distance and complete linkage to organize rows and columns of a normalized microbe-metabolite attribution score matrix into dendrograms, enabling identification of natural groupings before consensus-based optimal cluster selection.

## When to use

Apply this skill when you have a normalized microbe-metabolite feature attribution score matrix (rows = microbes, columns = metabolites) and need to explore hierarchical structure and visually assess similarity patterns before determining the optimal number of clusters via consensus clustering. Use it specifically after normalizing attribution scores by dividing by background distribution threshold and clipping to [-1, 1].

## When NOT to use

- Input attribution matrix is already manually clustered or pre-assigned to fixed k clusters; hierarchical clustering should precede consensus methods, not follow them.
- Score matrix contains missing values (NaN) or infinite values without prior imputation or removal.
- You have only a single microbe or metabolite feature; hierarchical clustering requires at least 2 observations per dimension to form meaningful dendrograms.

## Inputs

- Feature attribution score matrix S_i (unnormalized, dimensions: microbes × metabolites)
- Significant threshold score from background distribution (scalar, 97.5th percentile of null distribution)
- Background distribution of feature attribution scores (for threshold determination)

## Outputs

- Dendrograms for microbes (tree structure showing hierarchical relationships)
- Dendrograms for metabolites (tree structure showing hierarchical relationships)
- Clustered heatmap visualization (with row and column dendrograms)
- Normalized and clipped attribution score matrix S* (values in [-1, 1])

## How to apply

Normalize the feature attribution score matrix S_i by dividing each value by the significant threshold score derived from the background distribution and clip all values to the range [-1, 1]. Perform hierarchical clustering independently on microbe rows and metabolite columns using Euclidean distance as the distance metric and complete linkage as the agglomeration criterion. This produces dendrograms that visually organize microbes and metabolites by their similarity in attribution patterns. Use Seaborn's clustermap function to generate both dendrograms and a clustered heatmap simultaneously. The resulting dendrograms serve as input for subsequent consensus clustering analysis to determine optimal cluster numbers k₁* and k₂*.

## Related tools

- **Seaborn clustermap** (Generates hierarchical clustering dendrograms and heatmap for visualization of microbe and metabolite relationships)
- **scipy.cluster.hierarchy** (Computes hierarchical clustering using Euclidean distance and complete linkage agglomeration)
- **scikit-learn linkage functions** (Provides alternative hierarchical clustering implementation with support for Euclidean distance and complete linkage)
- **MiMeNet** (Full pipeline that incorporates hierarchical clustering as a preparatory step before consensus clustering) — https://github.com/YDaiLab/MiMeNet

## Examples

```
import seaborn as sns; import pandas as pd; S_norm = pd.DataFrame(S_i / threshold).clip(-1, 1); g = sns.clustermap(S_norm, metric='euclidean', method='complete', figsize=(10, 8))
```

## Evaluation signals

- Dendrograms show logical hierarchical structure with interpretable groupings; microbes/metabolites with similar attribution patterns cluster together at lower merge heights.
- Normalized score matrix S* has all values strictly within [-1, 1]; spot-check confirms clipping was applied correctly.
- Seaborn clustermap visualization is generated without errors and displays both row (microbe) and column (metabolite) dendrograms with corresponding heatmap.
- Dendrogram structure is stable and reproducible across multiple runs with identical input data and random seed.
- Subsequent consensus clustering (k-means on dendrograms for k ∈ [2, 20]) produces meaningful variation in connectivity matrices that can be used to identify optimal cluster numbers.

## Limitations

- Complete linkage is sensitive to outliers; a single microbe or metabolite with extreme attribution scores can inflate distances between clusters.
- Euclidean distance in high-dimensional spaces (many features) can suffer from the 'curse of dimensionality'; results may be less interpretable if the attribution matrix is very wide.
- Hierarchical clustering does not explicitly optimize for any cluster quality metric; the resulting dendrograms are exploratory and require downstream consensus clustering to identify statistically robust cluster numbers.
- Method assumes normalized, clipped values; if input matrix contains features outside [-1, 1] or has unnormalized scales, clustering distances become incomparable across microbe–metabolite pairs.
- No internal stopping criterion; dendrograms extend to n clusters (where n = number of microbes or metabolites), requiring external methods (e.g. elbow method, silhouette analysis) to select interpretable cluster numbers.

## Evidence

- [methods] Perform hierarchical clustering separately on microbe rows and metabolite columns using Euclidean distance and complete linkage with Seaborn's clustermap.: "Perform hierarchical clustering separately on microbe rows and metabolite columns using Euclidean distance and complete linkage with Seaborn's clustermap"
- [methods] Normalize the feature attribution score matrix S_i by dividing by the significant threshold score from background distribution and clip values to range [-1, 1].: "Normalize the feature attribution score matrix S_i by dividing by the significant threshold score from background distribution and clip values to range [-1, 1]"
- [methods] For each fixed cluster number k ranging from 2 to 20, generate a k-clustering and compute a consensus matrix by averaging connectivity matrices across all 100 trained models.: "For each fixed cluster number k ranging from 2 to 20, generate a k-clustering and compute a consensus matrix"
- [methods] Bicluster the normalized score matrix S* using k₁* and k₂* to assign microbes and metabolites to their final module memberships.: "Bicluster the normalized score matrix S* using k₁* and k₂* to assign microbes and metabolites to their final module memberships"
- [results] MiMeNet then trains multiple network models using 10-fold cross-validation. The resulting models are then used to construct a score matrix of microbe-metabolite feature attributions between the microbes and well-predicted metabolites. Then MiMeNet biclusters the score matrix into microbial and metabolomic modules.: "MiMeNet then trains multiple network models using 10-fold cross-validation. The resulting models are then used to construct a score matrix of microbe-metabolite feature attributions"
- [discussion] the predictive model in MiMeNet distinguishes it from MelonnPan [26], which uses a regularized linear regression to model each metabolite separately.: "MiMeNet can group microbes and metabolites with similar interaction patterns and functions to illuminate the underlying structure of the microbe-metabolite interaction network"
