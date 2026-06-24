---
name: dimensionality-reduction-and-clustering-evaluation
description: Use when you have high-dimensional feasible flux distributions sampled
  from constraint-based metabolic models for multiple biological samples (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3935
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_2259
  tools:
  - optGpSampler
  - COBRApy
  - t-SNE
  - Flux Variability Analysis (FVA)
  license_tier: restricted
derived_from:
- doi: 10.1371/journal.pcbi.1009337
  title: INTEGRATE
evidence_spans:
- We exploited the implementation of optGpSampler algorithm [71] available in COBRApy
  [72], and we sampled a million steady state solutions
- In this work, we exploited the implementation of optGpSampler algorithm [71] available
  in COBRApy [72], and we sampled a million steady state solutions
- We exploited the implementation of optGpSampler algorithm [71] available in COBRApy
  [72]
- the implementation of optGpSampler algorithm [71] available in COBRApy [72]
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_integrate_cq
    doi: 10.1371/journal.pcbi.1009337
    title: INTEGRATE
  dedup_kept_from: coll_integrate_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1009337
  all_source_dois:
  - 10.1371/journal.pcbi.1009337
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Dimensionality Reduction and Clustering Evaluation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Apply t-SNE dimensionality reduction to sampled metabolic flux distributions to visualize and evaluate the segregation quality of biological samples (cell lines or conditions) in two-dimensional space. This skill enables comparison of clustering fidelity across different constraint scenarios by measuring intra-sample cohesion and inter-sample separation.

## When to use

You have high-dimensional feasible flux distributions sampled from constraint-based metabolic models for multiple biological samples (e.g., cell lines, disease states, or conditions) and need to assess whether the samples cluster distinctly when constraints of different types (nutrient availability, extracellular flux ratios, transcriptomics-derived) are applied. Use this skill when you want to visualize and quantify whether additional constraint layers improve the biological segregation of samples compared to individual or paired constraint applications.

## When NOT to use

- Flux distributions have not been sampled or are sparse (<1000 samples per condition); t-SNE requires sufficient sample density for meaningful manifold learning.
- The biological samples are expected to be identical or very similar; this skill is designed to reveal differences, not confirm homogeneity.
- You are working with a single constraint scenario or a single cell line; comparative segregation analysis requires at least two distinct groups and multiple constraint conditions to be meaningful.

## Inputs

- Sampled flux distribution matrices (10,000 steady-state solutions per cell line, stored as CSV with reactions as columns and samples as rows)
- Multiple constraint-applied metabolic models (SBML format) representing the same biological samples under different constraint conditions
- Experimental phenotype data (e.g., growth yield on glucose, extracellular flux measurements) for correlation validation

## Outputs

- Two-dimensional t-SNE projection map (visualization file, e.g., PNG/PDF) showing cell line clustering under each constraint scenario
- Quantitative segregation comparison table summarizing visual quality across constraint types
- Spearman correlation coefficients and p-values between experimental and in silico phenotypes for each constraint scenario

## How to apply

Sample 10,000 steady-state flux distributions from each cell line model using uniform sampling (optGpSampler) to obtain a high-dimensional flux matrix per sample. Apply t-SNE dimensionality reduction to project all sampled flux distributions into two-dimensional space, treating each sampled flux vector as a point. Repeat this visualization across constraint scenarios (type 1 only, type 1+2, type 3 only, and type 1+2+3) to create comparable maps. Qualitatively assess the separation by visual inspection of intra-model clustering (points belonging to the same cell line should form tight, distinct clusters) and inter-model separation (clusters from different cell lines should not overlap). Complement visual evaluation with quantitative metrics such as Spearman correlation between experimental and in silico phenotypes (e.g., growth yield) to validate that superior visual segregation correlates with improved model predictive accuracy.

## Related tools

- **optGpSampler** (Uniform sampling of 10,000 steady-state flux distributions from the null space of each cell line metabolic model)
- **t-SNE** (Dimensionality reduction algorithm to project high-dimensional flux distributions into two-dimensional visualization space)
- **COBRApy** (Python package for constraint-based metabolic modeling, integration of constraints, and model manipulation) — https://github.com/opencobra/cobrapy
- **Flux Variability Analysis (FVA)** (Determines maximum feasible flux for each reaction to enable flux scaling normalization prior to t-SNE projection)

## Examples

```
python pipeline/randomSampling.py 10000 1 && python -c "import numpy as np; from sklearn.manifold import TSNE; fluxes = np.loadtxt('randomSampling_ENGRO2_nSol_10000_MCF102A.csv', delimiter=','); tsne = TSNE(n_components=2); projection = tsne.fit_transform(fluxes); np.savetxt('tsne_MCF102A.csv', projection, delimiter=',')"
```

## Evaluation signals

- Visual inspection of t-SNE maps shows tight, non-overlapping clusters for each cell line under the type 1+2+3 constraint scenario, indicating superior segregation compared to single or paired constraint conditions.
- Spearman correlation coefficient between experimental and in silico growth yield on glucose is statistically significant (p < 0.05) and highest under the type 1+2+3 constraint scenario, validating that visual segregation correlates with predictive accuracy.
- Intra-cell-line distance (average pairwise t-SNE distance between points of the same cell line) is minimized and inter-cell-line distance (average pairwise distance between points from different cell lines) is maximized under type 1+2+3 constraints compared to all other scenarios.
- No visual overlap or minimal overlap of cluster boundaries between distinct cell lines in the final two-dimensional projection, confirming that the constraint combination creates biologically meaningful separation.
- Reproducibility check: re-running the sampling and t-SNE projection with the same random seed produces visually identical cluster patterns and maintains the same ranking of constraint scenarios by segregation quality.

## Limitations

- t-SNE is a stochastic algorithm; results may vary between runs unless the random seed is fixed. Multiple runs with different seeds are recommended to assess stability of cluster assignments.
- Sample size limitation: visualization was restricted to 10,000 steady-state solutions per cell line for computational efficiency; increasing this number may refine the manifold but requires more computation time.
- The visual segregation metric is qualitative and subject to observer bias; complementary quantitative metrics (e.g., silhouette score, Davies-Bouldin index) should be computed to provide objective segregation quality scores.
- t-SNE does not preserve global distances—only local neighborhood structure is preserved—so absolute distances between clusters in the 2D plot do not reflect distances in the original flux space; interpretation must focus on qualitative separation patterns rather than quantitative distance metrics.
- Limited metabolite coverage in metabolomics datasets constrains the number of reactions that can be analyzed and may reduce the diversity of feasible flux solutions, affecting the quality of t-SNE separation.

## Evidence

- [other] Sample 10,000 steady-state flux distributions from the null space of the stoichiometric matrix for each cell line using uniform sampling (optGpSampler).: "Sample 10,000 steady-state flux distributions from the null space of the stoichiometric matrix for each cell line using uniform sampling (optGpSampler). 3. Apply t-SNE dimensionality reduction to the"
- [other] Apply t-SNE to visualize segregation of sampled flux distributions across constraint conditions.: "Apply t-SNE dimensionality reduction to the sampled flux distributions to produce a two-dimensional map and visualize the segregation of the five cell lines. 4. Repeat steps 2–3 for models with type"
- [other] Type 1+2+3 constraints together achieve superior segregation of flux distributions compared to individual or paired constraint applications.: "Type 1+2+3 constraints together achieve superior segregation of the five cell line flux distributions compared to individual or paired constraint applications, as demonstrated by t-SNE visualization"
- [other] Compute Spearman correlation between experimental and in silico phenotypes to validate constraint scenarios.: "Compute the Spearman correlation coefficient between experimental and in silico growth yield on glucose for each constraint scenario and report p-values."
- [results] For computational visualization reasons, only 10,000 steady-state solutions were plotted.: "For computational reasons, only 10000 steady-state solutions sampled within the feasible region of each model were plotted"
- [intro] We scaled metabolic fluxes relative to the maximum flux identified using Flux Variability Analysis, as in scFBA.: "We scaled metabolic fluxes relative to the maximum flux identified using Flux Variability Analysis, as in scFBA [38]"
