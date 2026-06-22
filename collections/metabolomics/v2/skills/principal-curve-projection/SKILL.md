---
name: principal-curve-projection
description: Use when you have per-sample metabolite abundance data and a metabolite-pathway association table, and you need to quantify dysregulation of individual samples across multiple metabolic pathways.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - Lilikoi v2.0
  - R
derived_from:
- doi: 10.1093/gigascience/giaa162
  title: Lilikoi V2.0
evidence_spans:
- The new Lilikoi v2.0 R package has implemented a deep-learning method for classification, in addition to popular machine learning methods.
- Lilikoi v2.0 is a modern, comprehensive package to enable metabolomics analysis in R programming environment.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lilikoi_v2_0_cq
    doi: 10.1093/gigascience/giaa162
    title: Lilikoi V2.0
  dedup_kept_from: coll_lilikoi_v2_0_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/gigascience/giaa162
  all_source_dois:
  - 10.1093/gigascience/giaa162
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# principal-curve-projection

## Summary

Project per-sample metabolite abundances onto a fitted principal curve within each metabolic pathway to map samples into a reduced dimensionality space, enabling subsequent dysregulation scoring and pathway-based classification. This skill is core to Lilikoi's personalized pathway analysis approach.

## When to use

Apply this skill when you have per-sample metabolite abundance data and a metabolite-pathway association table, and you need to quantify dysregulation of individual samples across multiple metabolic pathways. Specifically, use it after metabolite names have been converted to HMDB identifiers and pathway assignments are confirmed, and before computing pathway dysregulation scores or selecting pathway features for downstream machine learning or prognosis prediction.

## When NOT to use

- Input is already a pre-computed pathway dysregulation score matrix (PDSmatrix) — projection has already been applied.
- Metabolite data has not been assigned to pathways yet — run MetaTOpathway conversion first.
- Sample abundances have not been normalized or preprocessed — principal curve fitting assumes comparable scales and distributions across metabolites.

## Inputs

- per-sample metabolite abundance matrix (rows=samples, columns=metabolites; numeric)
- metabolite-pathway association table (rows=metabolites, columns=pathway assignments)
- pathway identifier or name (string)

## Outputs

- principal curve object (fitted curve in PC space per pathway)
- projected sample coordinates on the principal curve (per-pathway, per-sample)
- basis vectors / loadings for the principal curve projection

## How to apply

For each pathway in the metabolite-pathway association table, extract the subset of metabolites assigned to that pathway from your abundance matrix. Fit a principal curve through the per-sample metabolite abundances in the pathway's high-dimensional principal component space using Lilikoi v2.0's principal-curve projection method. Project each sample's point onto this smoothed curve. The projection captures the sample's position relative to the expected metabolic state within that pathway, with distance from the curve origin (centroid of normal samples) subsequently used to compute dysregulation scores. The principal curve method automatically smooths the manifold of sample variation, avoiding overfitting to individual sample noise.

## Related tools

- **Lilikoi v2.0** (Implements principal-curve projection method for metabolite-pathway data; provides lilikoi.PDSfun() function that wraps projection and dysregulation scoring) — https://github.com/lanagarmire/lilikoi2
- **R** (Programming environment in which Lilikoi v2.0 package executes principal curve fitting and projection operations)

## Examples

```
PDSmatrix=lilikoi.PDSfun(Metabolite_pathway_table)
```

## Evaluation signals

- Projected sample coordinates lie on a smooth 1-D manifold (the principal curve) within the pathway's PC space; verify by inspecting plot of samples against fitted curve.
- Dysregulation scores computed from projected distances are higher for disease/perturbed samples than for healthy controls at curve origin; compare score distributions between phenotypes.
- PDSmatrix output has dimensions (n_samples × n_pathways) with numeric dysregulation values ≥ 0; check for expected range and absence of NaN/Inf values.
- Pathways with known biological relevance to the phenotype yield higher dysregulation variance across samples; rank pathways by dysregulation score variance and validate against literature.
- Principal curve curvature is non-trivial but not excessive; extreme curvature or near-linearity may indicate poor pathway coherence or missing pathway-relevant metabolites.

## Limitations

- Principal curve fitting assumes pathway metabolites are non-independent and follow a smooth manifold in PC space; pathways with discontinuous or multi-modal sample distributions may yield misleading projections.
- Method requires adequate sample size per pathway to fit a reliable curve; small sample cohorts (n < 10) may result in overfitting or unstable projections.
- Dysregulation scores depend on correct metabolite-pathway assignment; errors in the MetaTOpathway conversion step will propagate through projection and scoring.
- No built-in handling of missing metabolite abundance values; imputation or removal of incomplete samples must occur before projection.

## Evidence

- [other] projection_method: "Project the per-sample metabolite abundances onto a principal curve fitted to the metabolite-pathway space using Lilikoi v2.0's principal-curve projection method."
- [other] dysregulation_quantification: "Compute dysregulation scores as the Euclidean distance or deviation from the principal curve for each sample-pathway combination."
- [other] workflow_context: "For each pathway, extract the subset of metabolites assigned to that pathway. 3. Project the per-sample metabolite abundances onto a principal curve fitted to the metabolite-pathway space"
- [other] pds_matrix_output: "Organize scores into a matrix with samples as rows and pathways as columns, generating the PDSmatrix output."
- [readme] readme_integration: "PDSmatrix=lilikoi.PDSfun(Metabolite_pathway_table)"
