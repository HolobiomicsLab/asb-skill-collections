---
name: pathway-level-sample-stratification
description: Use when you have per-sample metabolite abundance data and a metabolite-to-pathway association table, and need to assign each sample a dysregulation score for each pathway to enable downstream pathway-level classification, feature selection, or survival analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3223
  edam_topics:
  - http://edamontology.org/topic_0208
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0602
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# pathway-level-sample-stratification

## Summary

Stratify individual samples into dysregulation states across metabolic pathways by computing Pathway Dysregulation Scores (PDS), which quantify each sample's deviation from normal metabolic state using principal curve projection within each pathway's metabolite space. This skill enables personalized, pathway-centric disease classification and prognosis prediction.

## When to use

Apply this skill when you have per-sample metabolite abundance data and a metabolite-to-pathway association table, and need to assign each sample a dysregulation score for each pathway to enable downstream pathway-level classification, feature selection, or survival analysis. Use it when biological interpretation at the pathway level is more relevant than individual metabolite abundance, or when samples must be stratified by their deviation from normal metabolic state.

## When NOT to use

- Input metabolite abundance data lacks pathway annotations or association table is unavailable.
- The goal is to identify individual dysregulated metabolites rather than pathway-level dysregulation patterns.
- Sample set contains no normal/healthy controls to establish the centroid of normal metabolic state for distance computation.

## Inputs

- Per-sample metabolite abundance data (CSV or data frame with metabolites as columns, samples as rows)
- Metabolite-pathway association table (mapping metabolite IDs or names to pathway identifiers)
- Metabolite identifiers (e.g., HMDB IDs) or names for pathway conversion

## Outputs

- PDSmatrix: matrix of Pathway Dysregulation Scores with samples as rows and pathways as columns
- Principal curve model for each pathway (internal representation)

## How to apply

For each metabolic pathway, extract the subset of metabolites assigned to that pathway from the abundance data. Project the per-sample metabolite abundances onto a principal curve fitted to the metabolite-pathway space using Lilikoi v2.0's principal-curve projection method. Compute dysregulation scores as the Euclidean distance from each sample's projected point on the principal curve to the centroid of normal samples at the curve's origin. Organize all sample-pathway dysregulation scores into a matrix with samples as rows and pathways as columns (PDSmatrix), which serves as the input for downstream pathway selection, machine learning classification, or Cox-based prognosis models.

## Related tools

- **Lilikoi v2.0** (Implements lilikoi.PDSfun() function for principal-curve-based PDS computation, metabolite-to-HMDB conversion via lilikoi.MetaTOpathway(), and subsequent pathway-level classification and survival analysis) — https://github.com/lanagarmire/lilikoi2
- **R** (Programming environment for loading data, executing lilikoi functions, and organizing outputs)

## Examples

```
PDSmatrix=lilikoi.PDSfun(Metabolite_pathway_table)
```

## Evaluation signals

- PDSmatrix dimensions match (# samples × # pathways) and contain no null/NaN values for complete pathway coverage.
- Dysregulation scores for normal/control samples cluster near or at zero; disease/case samples exhibit elevated scores, indicating proper distance calibration to the normal centroid.
- Principal curves converge and show smooth fitting through the metabolite-pathway space with no degenerate or singular configurations.
- Pathways selected downstream (via feature selection methods like gain ratio) using PDSmatrix scores correlate with known disease-associated pathways or phenotype labels.
- PDSmatrix scores remain stable and reproducible across repeated runs with fixed random seeds.

## Limitations

- Requires a well-characterized metabolite-pathway association table; incomplete or inaccurate pathway annotations propagate into dysregulation scores.
- Principal curve fitting assumes a smooth, one-dimensional latent structure within each pathway's metabolite space; highly branched or multi-modal metabolite distributions may violate this assumption.
- Dysregulation score interpretation depends critically on the definition and stability of the normal sample centroid; small or heterogeneous control groups may lead to unstable distance estimates.
- No explicit guidance provided in the article or README on handling missing metabolite abundance values or dealing with pathways containing very few metabolites.
- Computational cost scales with the number of pathways and sample size; large-scale metabolomics studies with hundreds of pathways may incur significant runtime.

## Evidence

- [other] Principal curve projection method for PDS computation: "Project the per-sample metabolite abundances onto a principal curve fitted to the metabolite-pathway space using Lilikoi v2.0's principal-curve projection method."
- [other] Distance-based dysregulation scoring from curve to normal centroid: "quantify each sample's dysregulation as the distance from its projected point on the curve to the centroid of normal samples at the curve's origin"
- [other] PDSmatrix output organization: "Organize scores into a matrix with samples as rows and pathways as columns, generating the PDSmatrix output."
- [readme] Lilikoi v2.0 pathway analysis capabilities: "Lilikoi v2 supports data preprocessing, exploratory analysis, pathway visualization and metabolite-pathway regression."
- [readme] PDSfun function in workflow example: "PDSmatrix=lilikoi.PDSfun(Metabolite_pathway_table)"
