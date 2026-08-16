---
name: dimensionality-reduction-visualization
description: Use when after generating large feasible flux distributions (e.g., 1
  million sampled solutions per cell line) from constrained metabolic models, apply
  t-SNE when you need to assess whether distinct biological samples (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3935
  edam_topics:
  - http://edamontology.org/topic_2259
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3307
  - http://edamontology.org/topic_0218
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3372
  tools:
  - eFlux
  - TRFBA
  - GX-FBA
  - scFBA
  - STAR aligner (v.2.6.1d)
  - HTSeq (v.0.6.1)
  - YSI2950 bioanalyzer
  - Agilent 1290 Infinity UHPLC system
  - optGpSampler algorithm
  - t-SNE (t-distributed Stochastic Neighbor Embedding)
  - COBRApy
  - Python scikit-learn or openTSNE
  - Python
  - Anaconda
  - Git
  - PyTorch
  - scikit-learn (t-SNE/UMAP)
  - Matplotlib
  - MSBERT
  license_tier: open
derived_from:
- doi: 10.1371/journal.pcbi.1009337
  title: INTEGRATE
- doi: 10.1021/acs.analchem.4c02426
  title: ''
evidence_spans:
- we set flux boundaries as a function of gene expression as done, among others, by
  eFlux [36]
- we set flux boundaries as a function of gene expression as done, among others, by
  eFlux [36] and TRFBA
- We scaled metabolic fluxes relative to the maximum flux identified using Flux Variability
  Analysis, as in GX-FBA [26]
- We scaled metabolic fluxes relative to the maximum flux identified using Flux Variability
  Analysis, as in scFBA [38]
- raw reads were mapped with STAR aligner (v.2.6.1d) to human reference genome (hg38)
- gene counts were calculated by HTSeq (v.0.6.1), using the hg38 Encode-Gencode GTF
  file (v28)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_integrate
    doi: 10.1371/journal.pcbi.1009337
    title: INTEGRATE
  - build: coll_msbert_cq
    doi: 10.1021/acs.analchem.4c02426
    title: MSBERT
  dedup_kept_from: coll_integrate
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1009337
  all_source_dois:
  - 10.1371/journal.pcbi.1009337
  - 10.1021/acs.analchem.4c02426
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# dimensionality-reduction-visualization

## Summary

Apply t-distributed Stochastic Neighbor Embedding (t-SNE) to high-dimensional feasible flux distributions (FFD) sampled from constraint-based metabolic models to visualize and segregate metabolic phenotypes across biological samples in two-dimensional space. This skill enables visual discrimination of metabolic differences driven by transcriptional vs. metabolic regulation.

## When to use

After generating large feasible flux distributions (e.g., 1 million sampled solutions per cell line) from constrained metabolic models, apply t-SNE when you need to assess whether distinct biological samples (e.g., five breast cancer cell lines with different metabolic profiles) cluster separately based on their flux phenotypes. Use this skill specifically when integrating multi-constraint metabolic models (transcriptomics-derived, extracellular flux ratio, and nutrient availability constraints) and you want to visualize the emergent segregation in low-dimensional space as a proxy for model discrimination power.

## When NOT to use

- Input FFD matrix has fewer than ~30 samples or reactions—t-SNE requires sufficient high-dimensional structure to preserve meaningful neighborhoods.
- Feasible flux region is not yet sampled or constraint-integration workflow is incomplete (t-SNE will not reveal meaningful biology from unconstrainedflux sampling).
- The goal is interpretable flux ranking or reaction importance—t-SNE is a visualization tool, not a feature selection or ranking method; use sensitivity analysis or RAS concordance instead.

## Inputs

- Feasible flux distributions (FFD) matrix: reactions × samples, dimensionality typically 1000s of reactions × millions of sample solutions
- Cell line or sample labels for each solution (metadata indicating which sample each solution originated from)
- Optionally, design matrix or experimental condition labels for color-coding or stratification

## Outputs

- 2D t-SNE embedding (points × 2 coordinates)
- Scatter plot visualization showing cell-line clusters colored by sample identity
- Optional: quantitative cluster separation metrics (silhouette scores, Davies–Bouldin index per pair)

## How to apply

Collect uniformly sampled feasible flux distributions for all input samples (generated via optGpSampler with parameters: 1 million samples, thinning=10, batch size 100,000). Aggregate the sampled flux vectors across all cell lines into a single matrix (reactions × total_samples). Apply t-SNE with standard hyperparameters to reduce to 2D space, preserving local neighborhood structure. Color-code points by their originating cell line and visualize the resulting scatter plot. Evaluate cluster separation qualitatively (visual distinctness of cell-line clusters) and quantitatively (e.g., silhouette score or Davies–Bouldin index across the five cell-line groups). The degree of separation serves as an indicator of whether the integrated constraint types (Type 1: nutrient availability; Type 2: extracellular flux ratios; Type 3: transcriptomics-derived via RAS scaling) successfully differentiate metabolic phenotypes.

## Related tools

- **t-SNE (t-distributed Stochastic Neighbor Embedding)** (Primary dimensionality reduction algorithm for visualizing feasible flux distributions in 2D space while preserving local neighborhood structure)
- **optGpSampler algorithm** (Generates the uniformly distributed feasible flux samples (1 million samples per cell-line model) that are then reduced and visualized by t-SNE)
- **COBRApy** (Python package for constraint-based metabolic model manipulation and interfacing with sampling algorithms) — https://github.com/opencobra/cobrapy
- **Python scikit-learn or openTSNE** (Provides t-SNE implementation and optional clustering evaluation metrics (silhouette score, Davies–Bouldin index))

## Examples

```
```python
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import numpy as np

# Load FFD matrix (reactions x samples) from sampled solutions
FFD = np.load('ffd_matrix.npy')  # shape: (reactions, total_samples)
sample_labels = np.load('sample_labels.npy')  # which cell line each sample came from

# Apply t-SNE to reduce to 2D
tsne = TSNE(n_components=2, random_state=42, perplexity=30)
ffd_2d = tsne.fit_transform(FFD.T)  # transpose: samples x reactions

# Visualize by cell line
for cell_line in ['MCF102A', 'MCF7', 'MDA-MB231', 'MDA-MB361', 'SKBR3']:
    mask = sample_labels == cell_line
    plt.scatter(ffd_2d[mask, 0], ffd_2d[mask, 1], label=cell_line, alpha=0.6)

plt.legend()
plt.xlabel('t-SNE 1')
plt.ylabel('t-SNE 2')
plt.savefig('ffd_tsne.png')
```
```

## Evaluation signals

- Visual inspection: five cell-line clusters are visually distinct (non-overlapping or minimally overlapping point clouds in 2D space) when all three constraint types are integrated, and less distinct or merged when constraints are selectively removed.
- Quantitative silhouette score or Davies–Bouldin index shows improvement (higher silhouette, lower DB index) when moving from single-constraint to multi-constraint models.
- Reproducibility: re-running t-SNE on the same FFD matrix (or resampling with identical random seed) yields visually similar cluster positions and separation, indicating stable manifold structure.
- Ablation signal: t-SNE on FFD from models lacking Type 2 (extracellular flux) or Type 3 (transcriptomics-derived) constraints shows degraded separation, confirming that multi-constraint integration drives phenotypic discrimination.
- Color-by-cellLine consistency: each cell line occupies a distinct region of the 2D space with minimal intrusion by other cell lines, indicating the constraints capture cell-line-specific metabolic properties.

## Limitations

- t-SNE is a stochastic algorithm sensitive to random seed and hyperparameter choices (perplexity, learning rate); results may vary between runs unless seed is fixed.
- t-SNE does not preserve global distances, only local neighborhoods; quantitative distance between clusters in 2D space is not interpretable as metabolic dissimilarity.
- Feasible flux distributions must be pre-sampled uniformly; if sampling is biased or incomplete, t-SNE will reflect sampling artifacts rather than true constraint-induced structure.
- The skill assumes sufficiently high sampling density (1 million samples per cell line) to adequately cover the feasible flux region; sparse sampling may yield incomplete or misleading clusters.

## Evidence

- [methods] Apply t-distributed Stochastic Neighbor Embedding (t-SNE) dimensionality reduction to the sampled FFD in two-dimensional space and visualize cluster separation for the five cell lines.: "Apply t-distributed Stochastic Neighbor Embedding (t-SNE) dimensionality reduction to the sampled FFD in two-dimensional space and visualize cluster separation for the five cell lines."
- [results] The combination of all three constraint types (type 1+2+3) applied to ENGRO2 achieves clear separation of the five cell-line FFD clusters in t-SNE space, with transcriptomics-derived constraints alone providing good segregation but extracellular flux constraints improving inter-model separation.: "The combination of all three constraint types (type 1+2+3) applied to ENGRO2 achieves clear separation of the five cell-line FFD clusters in t-SNE space, with transcriptomics-derived constraints"
- [methods] Uniformly sample the constrained null space of each cell-relative model using optGpSampler algorithm (1 million samples, thinning=10, batch size 100,000) to generate Feasible Flux Distributions (FFD) for all five cell lines.: "Uniformly sample the constrained null space of each cell-relative model using optGpSampler algorithm (1 million samples, thinning=10, batch size 100,000) to generate Feasible Flux Distributions (FFD)"
