---
name: dysregulation-score-computation
description: Use when you have per-sample metabolite abundance data (e.g., from LC-MS or GC-MS) and a metabolite-to-pathway assignment table, and need to generate a sample-by-pathway dysregulation matrix for downstream classification, prognosis prediction, or pathway-level phenotype association.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_3520
  tools:
  - Lilikoi v2.0
  - R
  - lilikoi.MetaTOpathway()
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

# dysregulation-score-computation

## Summary

Compute pathway dysregulation scores (PDS) for individual samples by projecting per-sample metabolite abundances onto principal curves fitted in metabolite-pathway space, then quantifying each sample's deviation from the normal centroid. This enables personalized, pathway-level quantification of metabolic dysregulation across cohorts.

## When to use

Apply this skill when you have per-sample metabolite abundance data (e.g., from LC-MS or GC-MS) and a metabolite-to-pathway assignment table, and need to generate a sample-by-pathway dysregulation matrix for downstream classification, prognosis prediction, or pathway-level phenotype association. Use when pathway-level summaries of individual sample dysregulation are required rather than simple fold-change or univariate metabolite tests.

## When NOT to use

- Input metabolite abundances are already aggregated at the pathway level or normalized to principal components; PDS computation requires raw or log-transformed per-metabolite abundances.
- Metabolite-to-pathway mapping is unavailable or unmapped metabolites comprise >50% of the data, as dysregulation scores require sufficient pathway-level metabolite coverage.
- Sample cohort has no well-defined control/normal group to serve as the curve origin centroid for dysregulation distance calculation.

## Inputs

- Per-sample metabolite abundance matrix (samples × metabolites; numeric, e.g., from plasma_breast_cancer.csv)
- Metabolite-pathway association table (metabolite IDs mapped to KEGG/HMDB pathway assignments)
- Sample metadata including phenotype labels and/or control/case assignments for centroid reference

## Outputs

- Pathway Dysregulation Score (PDS) matrix (samples × pathways; numeric; values ≥ 0 represent distance from normal centroid)
- Principal curve objects per pathway (used for pathway visualization and metabolite-pathway regression downstream)

## How to apply

First, load metabolite abundance data and metabolite-pathway assignments (e.g., KEGG or HMDB identifiers) into R. For each pathway, extract the subset of metabolites assigned to that pathway and construct a per-sample metabolite abundance submatrix. Use Lilikoi v2.0's principal-curve fitting algorithm to project samples into the high-dimensional principal component space of each pathway's metabolite subspace. Fit a smooth principal curve through the samples to capture the manifold of metabolite co-variation. Compute dysregulation scores as the Euclidean distance from each sample's projected point on the principal curve to the centroid of control (normal) samples at the curve's origin. Organize all computed scores into a matrix with samples as rows and pathways as columns to produce the PDSmatrix. This approach captures multivariate dysregulation patterns within each pathway rather than treating metabolites independently.

## Related tools

- **Lilikoi v2.0** (Implements principal-curve projection, PDS computation via lilikoi.PDSfun(), and pathway visualization; provides the primary algorithmic backend for dysregulation score calculation.) — https://github.com/lanagarmire/lilikoi2
- **R** (Programming environment for loading data, managing metabolite-pathway tables, and executing Lilikoi v2.0 functions.)
- **lilikoi.MetaTOpathway()** (Converts metabolite names to HMDB IDs and constructs the metabolite-pathway association table prior to PDS computation.) — https://github.com/lanagarmire/lilikoi2

## Examples

```
# Transform metabolites to pathway and compute PDSmatrix
convertResults=lilikoi.MetaTOpathway('name')
Metabolite_pathway_table = convertResults$table
PDSmatrix=lilikoi.PDSfun(Metabolite_pathway_table)
```

## Evaluation signals

- PDSmatrix dimensions match input (rows = number of samples, columns = number of unique pathways); all values are non-negative numeric.
- Control samples have consistently lower dysregulation scores (closer to origin) than case/disease samples in the same pathway, indicating the principal curve centroid is correctly anchored at normal phenotype.
- No NaN or infinite values in PDSmatrix; missing pathways or metabolites are handled with explicit imputation or exclusion documented in the workflow.
- Dysregulation scores show pathway-level variance correlated with phenotype in downstream machine learning or association tests; pathway selection by dysregulation (e.g., gain ratio threshold > 0.50) identifies pathways relevant to the phenotype.
- Reproducibility: the same input data and normal cohort definition yield identical PDSmatrix when re-run with identical principal-curve fitting parameters (e.g., smoothing bandwidth, number of components).

## Limitations

- PDS computation assumes metabolites within each pathway co-vary in a manner captured by principal curves; pathways with highly sparse or uncorrelated metabolite profiles may yield unstable principal curve fits.
- The choice of control/normal samples for centroid reference critically affects all dysregulation scores; misclassified or contaminated control samples will bias the entire matrix.
- Principal curve fitting in high-dimensional metabolite space becomes computationally and statistically challenging when pathways contain very few metabolites (< 3–5) or very many (> 100+), potentially requiring pathway-specific parameter tuning.
- The Euclidean distance metric in PDS assumes isotropic variance; metabolites with heterogeneous measurement error or dynamic ranges may require data normalization (e.g., z-score or quantile normalization) before PDS computation.
- No systematic guidance provided in the README or article for choosing smoothing hyperparameters or handling pathways with insufficient sample size relative to metabolite dimensionality.

## Evidence

- [other] Principal-curve projection and dysregulation distance computation: "Project the per-sample metabolite abundances onto a principal curve fitted to the metabolite-pathway space using Lilikoi v2.0's principal-curve projection method. Compute dysregulation scores as the"
- [other] Centroid reference and sample-level quantification: "quantifies each sample's dysregulation as the distance from its projected point on the curve to the centroid of normal samples at the curve's origin"
- [other] Workflow input and output structure: "Load the metabolite-pathway association table and per-sample metabolite abundance data into R. For each pathway, extract the subset of metabolites assigned to that pathway. Organize scores into a"
- [readme] Lilikoi v2.0 supports pathway analysis components: "Lilikoi v2 supports data preprocessing, exploratory analysis, pathway visualization and metabolite-pathway regression"
- [readme] Example R invocation of PDSfun: "PDSmatrix=lilikoi.PDSfun(Metabolite_pathway_table)"
