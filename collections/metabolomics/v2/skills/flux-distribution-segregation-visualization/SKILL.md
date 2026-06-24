---
name: flux-distribution-segregation-visualization
description: Use when you have sampled feasible flux distributions from multiple constraint-based
  models (e.g., cell-line-specific variants of a metabolic model) and need to visually
  and quantitatively compare how well different constraint scenarios segregate biological
  samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3935
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_2259
  - http://edamontology.org/topic_3407
  tools:
  - Flux Variability Analysis
  - optGpSampler
  - COBRApy
  - t-SNE (scikit-learn or standalone)
  - scipy.stats.spearmanr
  - matplotlib / seaborn
  license_tier: restricted
derived_from:
- doi: 10.1371/journal.pcbi.1009337
  title: INTEGRATE
evidence_spans:
- We scaled metabolic fluxes relative to the maximum flux identified using Flux Variability
  Analysis, as in scFBA
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

# flux-distribution-segregation-visualization

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Apply t-SNE dimensionality reduction to sampled steady-state flux distributions from constraint-based metabolic models to visualize and quantify cell-line-specific segregation. This skill evaluates whether integrating multiple constraint types (nutrient availability, extracellular flux ratios, transcriptomics-derived reaction activity scores) improves inter-model separation and intra-model cohesion.

## When to use

Use this skill when you have sampled feasible flux distributions from multiple constraint-based models (e.g., cell-line-specific variants of a metabolic model) and need to visually and quantitatively compare how well different constraint scenarios segregate biological samples. Specifically, apply it when comparing constraint combinations (e.g., type 1 only, type 1+2, type 1+2+3) to determine which constraint integration strategy best distinguishes cell lines or phenotypes by their metabolic flux profiles.

## When NOT to use

- Input flux distributions are not sampled uniformly from the null space or have been filtered/biased by prior optimization; t-SNE may misrepresent the true feasible region geometry.
- Sample size is <1,000 solutions per model; insufficient sampling leads to spurious clustering and unreliable t-SNE topology.
- Models differ only in objective function or biomass coefficient, not in constraint structure; segregation differences will be minimal and the comparison uninformative.

## Inputs

- constraint-based metabolic models (SBML or COBRApy format) with multiple variants (e.g., ENGRO2_MCF102A.xml, ENGRO2_MDAMB231.xml, etc.)
- sampled feasible flux distributions (CSV files from optGpSampler; rows=solutions, columns=reaction fluxes; typically 10,000 samples per model)
- experimental phenotypic data (e.g., growth yield on glucose, YSI bioanalyzer measurements)
- constraint scenario definitions (binary flags or lists indicating which constraint types—nutrient availability, extracellular flux ratios, transcriptomics RAS scores—are active)

## Outputs

- t-SNE embedded flux distribution maps (2D coordinates for each solution, colored by cell line)
- visual comparison plots (one t-SNE plot per constraint scenario, aligned for side-by-side assessment)
- Spearman correlation coefficients and p-values between experimental and in silico predictions (per constraint scenario)
- segregation quality metrics (intra-model variance, inter-model separation distance, silhouette scores if computed)

## How to apply

First, sample 10,000 steady-state flux distributions from the null space of each constraint-based model using uniform sampling (e.g., optGpSampler in COBRApy). Apply t-SNE dimensionality reduction independently to each constraint scenario's combined flux distribution matrix, using default or optimized hyperparameters (perplexity, learning rate, n_iterations). Generate a two-dimensional map for each constraint condition and visually inspect intra-model clustering (tightness within cell line) and inter-model separation (distance between cell line clusters). Compute Spearman rank correlation between experimental phenotypic measurements (e.g., growth yield on glucose) and the in silico model predictions to quantify predictive power under each constraint scenario. Compare segregation quality across scenarios using visual assessment and statistical correlation p-values to identify which constraints best resolve biological heterogeneity.

## Related tools

- **optGpSampler** (uniform sampling of steady-state flux distributions from the null space of the stoichiometric matrix)
- **COBRApy** (constraint-based metabolic model loading, constraint application, and integration with Python sampling workflows) — https://github.com/opencobra/cobrapy
- **t-SNE (scikit-learn or standalone)** (nonlinear dimensionality reduction of flux distribution matrices to 2D for visualization)
- **scipy.stats.spearmanr** (computation of Spearman rank correlation between experimental phenotypes and in silico predictions to assess model predictive power)
- **matplotlib / seaborn** (rendering of t-SNE scatter plots and comparison visualizations across constraint scenarios)

## Examples

```
python pipeline/randomSampling.py 10000 1 && python -c "from sklearn.manifold import TSNE; import pandas as pd; flux_df = pd.read_csv('randomSampling_ENGRO2_nSol_10000_MCF102A.csv'); tsne = TSNE(n_components=2, random_state=42); coords = tsne.fit_transform(flux_df.iloc[:, 1:]); import matplotlib.pyplot as plt; plt.scatter(coords[:, 0], coords[:, 1]); plt.show()"
```

## Evaluation signals

- Intra-model cluster compactness: Solutions from the same cell line should cluster tightly in t-SNE space; visual inspection confirms reduced spread compared to inter-model distances under the type 1+2+3 constraint scenario.
- Inter-model separation: Cluster centroids for different cell lines should be maximally separated in the type 1+2+3 scenario relative to type 1, 1+2 scenarios; measure as minimum Euclidean distance between cluster centroids or silhouette coefficient > 0.3.
- Correlation with phenotype: Spearman ρ between experimental growth yield and in silico predictions should be statistically significant (p < 0.05) and highest under the type 1+2+3 constraint scenario, indicating constraint integration improves biological fidelity.
- Constraint monotonicity: Inter-model separation should monotonically increase (or plateau) as constraints are added incrementally (type 1 → type 1+2 → type 1+2+3); regression to type 1 performance when constraints are removed signals genuine constraint contribution.
- Solution diversity check: Sample size verification ensures 10,000 solutions per model were successfully sampled; histogram of flux values per reaction shows multimodal (not delta-function) distribution, confirming feasible region sampling rather than optimization convergence.

## Limitations

- t-SNE is stochastic and hyperparameter-dependent; results may vary across runs or perplexity settings. Use fixed random seed and report hyperparameters for reproducibility.
- Limited metabolite coverage in metabolomics dataset constrains the number of reactions that can be analyzed and constrained, potentially underutilizing type 2 and 3 constraints.
- Allosteric regulation, product inhibition, and cofactor/prosthetic group effects cannot be discriminated from flux distributions alone; type 3 constraints based on transcriptomics (RAS) may not capture post-transcriptional or allosteric control.
- Visual segregation is subjective; quantitative metrics (silhouette score, Davies-Bouldin index) should accompany qualitative t-SNE plots to avoid over-interpretation of minor clustering differences.
- Sample size limited to 10,000 steady-state solutions for computational visualization; larger sample sizes may reveal finer structure in the feasible region but require downsampling for t-SNE rendering.

## Evidence

- [other] Does the simultaneous application of all three constraint types (nutrient availability, extracellular fluxes, and transcriptomics-derived constraints) segregate the five breast cell lines better than any subset of constraints, as evaluated by t-SNE visualization of feasible flux distributions?: "research question defining the skill application scenario and evaluation criterion"
- [other] Type 1+2+3 constraints together achieve superior segregation of the five cell line flux distributions compared to individual or paired constraint applications, as demonstrated by t-SNE visualization showing decreased intra-model and increased inter-model separation of steady-state solutions.: "finding confirming expected outcome of the skill"
- [other] Sample 10,000 steady-state flux distributions from the null space of the stoichiometric matrix for each cell line using uniform sampling (optGpSampler).: "workflow step specifying sampling method and sample size"
- [other] Apply t-SNE dimensionality reduction to the sampled flux distributions to produce a two-dimensional map and visualize the segregation of the five cell lines.: "workflow step specifying dimensionality reduction and output"
- [other] Compute the Spearman correlation coefficient between experimental and in silico growth yield on glucose for each constraint scenario and report p-values.: "workflow step specifying quantitative evaluation metric"
- [results] For computational reasons, only 10000 steady-state solutions sampled within the feasible region of each model were plotted: "justification for sample size and computational constraint"
- [other] constraint-based stoichiometric metabolic models, Flux Variability Analysis, optGpSampler, COBRApy, t-SNE: "tools used in the skill application"
