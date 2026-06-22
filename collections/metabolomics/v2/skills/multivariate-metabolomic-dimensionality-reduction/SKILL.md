---
name: multivariate-metabolomic-dimensionality-reduction
description: Use when when you have a metabolite-pathway association table and per-sample metabolite abundance data (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3935
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_2269
  tools:
  - Lilikoi v2.0
  - R
  - pathtracer algorithm
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
---

# Multivariate Metabolomic Dimensionality Reduction

## Summary

Project per-sample metabolite abundances into a principal component space for each metabolic pathway, then fit a principal curve to capture the intrinsic low-dimensional structure of dysregulation. This enables quantification of pathway-level dysregulation scores (PDS) as deviations from normal phenotype baselines in a smoothed manifold.

## When to use

When you have a metabolite-pathway association table and per-sample metabolite abundance data (e.g., CSV with rows=samples, columns=metabolite abundances), and you need to compute sample-specific dysregulation scores across multiple pathways to enable personalized pathway-based classification or prognosis prediction in metabolomics studies.

## When NOT to use

- If metabolite-to-pathway mapping is unavailable or unreliable; the method requires valid biochemical associations.
- If your input is already a pre-computed feature table or classification matrix; PDSfun is designed specifically for raw metabolite abundance projection, not tabular features.
- If sample cohort lacks sufficient normal/reference controls to establish meaningful curve origin centroids; dysregulation is defined relative to phenotype-specific baselines.

## Inputs

- Metabolite-pathway association table (pathway assignment mapping)
- Per-sample metabolite abundance data (CSV: samples × metabolites)
- Sample metadata including phenotype labels or survival information

## Outputs

- PDSmatrix: matrix of pathway dysregulation scores (samples × pathways)
- Principal curve fit per pathway (optional: for visualization/validation)

## How to apply

For each pathway, extract the subset of metabolites assigned to that pathway from your abundance matrix. Project the extracted per-sample metabolite abundances onto a principal curve fitted in the metabolite-pathway principal component space using Lilikoi v2.0's pathtracer algorithm. Compute dysregulation scores as the Euclidean distance from each sample's projected point on the principal curve to the centroid of normal (reference) samples at the curve's origin. Organize all sample-pathway dysregulation scores into a matrix (PDSmatrix) with samples as rows and pathways as columns, ready for downstream feature selection and machine learning classification.

## Related tools

- **Lilikoi v2.0** (Implements lilikoi.PDSfun() for principal curve fitting and pathway dysregulation score computation; also provides lilikoi.MetaTOpathway() for metabolite-to-HMDB-id conversion) — https://github.com/lanagarmire/lilikoi2
- **R** (Programming environment for executing Lilikoi package and organizing metabolite-pathway matrices)
- **pathtracer algorithm** (Core dimensionality reduction algorithm within lilikoi.PDSfun that transforms metabolites into pathway principal curves) — https://github.com/lanagarmire/lilikoi2

## Examples

```
PDSmatrix=lilikoi.PDSfun(Metabolite_pathway_table)
```

## Evaluation signals

- PDSmatrix has correct shape (n_samples rows × n_pathways columns) and all dysregulation scores are non-negative real values (distances).
- Dysregulation scores for healthy/normal samples cluster near zero; diseased or dysregulated samples show elevated scores, indicating separation along the principal curve.
- Principal curve centroid (normal sample origin) aligns with expected biological reference phenotype; visual inspection or statistical tests confirm curve quality and goodness-of-fit.
- Downstream feature selection (e.g., lilikoi.featuresSelection with gain threshold) successfully identifies pathways with discriminative PDSmatrix columns for classification.
- PDSmatrix is suitable input for lilikoi.machine_learning or lilikoi.prognosis workflows without additional normalization or reformatting required.

## Limitations

- Requires valid, curated metabolite-pathway associations; incomplete or incorrect HMDB mappings propagate errors into PDS computation.
- Principal curve fitting depends on sufficient sample size per pathway; small cohorts or sparse metabolite data per pathway may produce unstable or over-fitted curves.
- Dysregulation scores are relative to normal sample centroid; studies without clear disease-free reference controls may yield uninformative or ambiguous PDS values.
- Method assumes metabolite abundances are commensurate and appropriately transformed (log, normalized); raw or unnormalized counts may bias principal component and curve projections.

## Evidence

- [other] Principal curve projection method for PDS computation: "The PDS computation maps samples into a high-dimensional principal component space per pathway, constructs and smooths a principal curve through samples, then quantifies each sample's dysregulation"
- [other] Workflow steps including pathway subset extraction and matrix organization: "For each pathway, extract the subset of metabolites assigned to that pathway. 3. Project the per-sample metabolite abundances onto a principal curve fitted to the metabolite-pathway space using"
- [readme] lilikoi.PDSfun function application in README example: "Transform metabolites into pathway using pathtracer algorithm
PDSmatrix=lilikoi.PDSfun(Metabolite_pathway_table)"
- [intro] Lilikoi v2.0 pathway analysis and visualization capabilities: "Lilikoi v2.0 supports data preprocessing, exploratory analysis, pathway visualization and metabolite-pathway regression."
- [readme] Primary tool role in metabolomics R environment: "The new Lilikoi v2 R package has implemented a deep-learning method for classification, in addition to popular machine learning methods."
