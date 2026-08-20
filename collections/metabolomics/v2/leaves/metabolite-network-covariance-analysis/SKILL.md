---
name: metabolite-network-covariance-analysis
description: Use when you have normalized metabolite abundance data from MetaboAnalyst
  or similar preprocessing and need to transition from univariate/pairwise correlation
  analysis to network-level inference that captures conditional dependencies (partial
  correlations) between metabolites under specific.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_2269
  tools:
  - R
  - MInfer
  - MetaboAnalyst
  license_tier: open
derived_from:
- doi: 10.1016/j.cmpb.2025.108672
  title: MInfer
evidence_spans:
- MInfer is an R package
- MInfer is an R package designed for analyzing metabolomics data
- transition from MetaboAnalyst to Jacobian analysis
- MInfer represents a novel computational framework that effectively facilitates the
  transition from MetaboAnalyst to Jacobian analysis
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_minfer_cq
    doi: 10.1016/j.cmpb.2025.108672
    title: MInfer
  dedup_kept_from: coll_minfer_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1016/j.cmpb.2025.108672
  all_source_dois:
  - 10.1016/j.cmpb.2025.108672
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-network-covariance-analysis

## Summary

Compute and validate covariance matrices from normalized metabolite abundance data, then derive Jacobian (precision) matrices to infer partial correlation structure and metabolite interaction networks. This bridges statistical preprocessing (MetaboAnalyst) to network-level metabolomic inference.

## When to use

You have normalized metabolite abundance data from MetaboAnalyst or similar preprocessing and need to transition from univariate/pairwise correlation analysis to network-level inference that captures conditional dependencies (partial correlations) between metabolites under specific experimental conditions (e.g., different carbon sources or time points).

## When NOT to use

- Input is already a feature table or distance matrix from a different normalization pipeline (e.g., CLR, log-ratio transforms); re-normalizing may introduce bias.
- Sample size is very small (n < number of metabolites); covariance matrix will be rank-deficient and inversion will fail or yield numerically unstable Jacobian estimates.
- Metabolite abundance data is non-continuous or heavily zero-inflated (e.g., count data); covariance assumptions may be violated without prior compositional or count-based transformation.

## Inputs

- Normalized metabolite abundance matrix (rows=metabolites, columns=samples)
- Experimental condition identifier (e.g., carbon source: 6, 16)
- Number of time points (integer)
- Metabolite interaction network or subset (KEGG IDs)

## Outputs

- Covariance matrix (symmetric, metabolite × metabolite)
- Jacobian (precision) matrix (symmetric, metabolite × metabolite, partial correlations)
- Matrix validation report (symmetry, dimensions, condition number)

## How to apply

Load the normalized metabolite abundance matrix and prepare it for the target condition(s) using prepare_data(). Generate the sample covariance matrix via generate_covariance(), specifying the number of time points (num_tp). Compute the matrix inverse using numerical linear algebra, negate it to obtain the Jacobian (precision) matrix, which encodes the partial correlation structure. Validate the result by checking symmetry, dimensions, and numerical stability (condition number, determinant sign). Export the validated Jacobian matrix as a structured file for downstream network visualization or statistical inference.

## Related tools

- **MInfer** (R package providing prepare_data(), generate_covariance(), and calculate_jacobian() functions for the complete workflow) — https://github.com/cellbiomaths/MInfer
- **MetaboAnalyst** (Upstream preprocessing and normalization platform that produces the normalized metabolite abundance matrix consumed by this skill)
- **R** (Programming environment for numerical linear algebra (matrix inversion, symmetry checks))

## Examples

```
data_6C <- prepare_data(met_input, 6); cov_6C <- generate_covariance(data_6C, num_tp = 1); jacobian_6C <- calculate_jacobian(cov_6C[[1]], interactions_fin, icount = 15)
```

## Evaluation signals

- Jacobian matrix is symmetric (J == t(J)) within numerical precision (≤ 1e-10 relative tolerance)
- Jacobian matrix dimensions match the number of metabolites (n × n) and covariance input dimensions
- Matrix determinant is non-zero and condition number is finite, indicating the covariance matrix was invertible and numerically stable
- Diagonal elements of the Jacobian are negative (reflecting variance constraints in precision matrices)
- Spot-check: partial correlations derived from Jacobian are bounded in [-1, 1] and differ meaningfully from raw Pearson correlations (indicating conditional dependence capture)

## Limitations

- Jacobian computation assumes the covariance matrix is positive-definite; rank-deficient or near-singular matrices (e.g., from over-parametrized or small-sample data) will produce numerical artifacts or fail inversion.
- The method assumes multivariate normality of metabolite abundances; violations (e.g., skew, heavy tails, compositionality) may lead to misleading partial correlation estimates.
- No changelog or version tracking documented; reproducibility and backward compatibility of MInfer releases are not tracked in the README.

## Evidence

- [other] Jacobian matrix computation rationale: "Compute the inverse of the covariance matrix using numerical linear algebra in R. 3. Negate the inverse to obtain the Jacobian (precision) matrix, representing partial correlation structure."
- [other] Validation of Jacobian matrix properties: "Validate matrix properties (symmetry, dimensions, numerical stability) and export as a structured output file."
- [readme] Workflow integration with MetaboAnalyst: "MInfer represents a novel computational framework that effectively facilitates the transition from MetaboAnalyst to Jacobian analysis, enhancing the exploration of metabolomic networks."
- [readme] Covariance generation step: "Generate covariance matrices for the prepared data. The parameter num_tp specifies the number of time points."
- [readme] MInfer provides end-to-end tools: "MInfer provides tools for data preparation, covariance matrix generation, Jacobian matrix computation, and visualization of metabolite interaction networks"
