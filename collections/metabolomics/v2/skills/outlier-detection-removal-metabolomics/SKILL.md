---
name: outlier-detection-removal-metabolomics
description: Use when after kNN imputation of metabolite measurements but before variance-stabilizing normalization, when you have a MultiAssayExperiment object with potentially problematic samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  tools:
  - MetaboDiff
  - R
  - MultiAssayExperiment
derived_from:
- doi: 10.1093/bioinformatics/bty344
  title: MetaboDiff
- doi: 10.1158/0008-5472.can-14-1490
  title: ''
evidence_spans:
- '`MetaboDiff` is available for all operating systems and can be installed via Github'
- met = knn_impute(met,cutoff=0.4)
- The `MetaboDiff` R package requires R version 4.0.2 or higher.
- The `MetaboDiff` R package requires R version 4.0.2 or higher
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metabodiff_cq
    doi: 10.1093/bioinformatics/bty344
    title: MetaboDiff
  dedup_kept_from: coll_metabodiff_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/bty344
  all_source_dois:
  - 10.1093/bioinformatics/bty344
  - 10.1158/0008-5472.can-14-1490
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Outlier Detection and Removal in Metabolomics

## Summary

Identifies and removes outlier samples in metabolomic assays using k-means clustering on imputed metabolite data to ensure downstream analysis robustness. This preprocessing step detects samples with anomalous metabolite profiles before normalization, improving the quality of differential metabolomic inferences.

## When to use

After kNN imputation of metabolite measurements but before variance-stabilizing normalization, when you have a MultiAssayExperiment object with potentially problematic samples. Use this step when: (1) you suspect batch effects or technical failures in specific samples, (2) you want to flag samples with unusually high imputation burdens, or (3) visual inspection of sample dendrograms reveals suspect clustering patterns that could inflate noise in correlation networks or differential abundance tests.

## When NOT to use

- Input metabolite table is not yet imputed—apply kNN imputation first with appropriate cutoff threshold.
- You have prior knowledge that specific samples are intentionally different (e.g., disease vs. control groups); ensure your k value and visual inspection do not conflate biological signal with technical outliers.
- Sample size is very small (n < 10 total)—k-means clustering becomes unreliable and manual review is preferable.

## Inputs

- MultiAssayExperiment object (with imputed metabolite assay, rowData annotations, and colData sample metadata)
- Imputed metabolite measurements (rows = metabolites, columns = samples)

## Outputs

- MultiAssayExperiment object with outlier samples removed
- Outlier heatmap visualization showing k-means cluster assignments
- Cluster membership vector identifying which samples belong to outlier cluster(s)

## How to apply

Apply k-means clustering (k=2 or higher based on visual inspection of dendrograms) using the outlier_heatmap function, which clusters samples based on their overall metabolite profile similarity in the imputed assay. Examine the heatmap output to identify clusters that represent outliers (typically small clusters with aberrant metabolite patterns or high missing-data content). Remove identified outlier clusters using remove_cluster, specifying the cluster number(s) to exclude. The rationale is that k-means clustering is more objective than ad-hoc sample filtering and leverages the entire metabolite measurement vector rather than univariate flags. Validate removal by re-running quality_plot after outlier removal to confirm that sample distributions are now more homogeneous across groups.

## Related tools

- **MetaboDiff** (R package providing outlier_heatmap and remove_cluster functions for k-means-based outlier detection in metabolomic MultiAssayExperiment objects) — https://github.com/andreasmock/MetaboDiff
- **MultiAssayExperiment** (Data container class that organizes assay (metabolite measurements), rowData (metabolite annotations), and colData (sample metadata) for integrated preprocessing and visualization)

## Examples

```
outlier_heatmap(met, k=2); met <- remove_cluster(met, cluster=1); quality_plot(met, group_factor="tumor_normal")
```

## Evaluation signals

- Outlier heatmap dendrogram shows clear cluster separation, with outlier cluster(s) visually distinct in color and/or distance from main cluster.
- After remove_cluster, quality_plot shows more uniform metabolite distributions across samples within each biological group (tumor vs. normal), with fewer extreme values.
- Sample annotation (colData) records the number of missing metabolites per sample before and after removal; outlier samples typically exhibit higher pre-imputation missingness.
- Principal component analysis (pca_plot) after outlier removal shows tighter grouping within biological groups and reduced unexplained variance in the first 1–2 PCs.
- Metadata reproducibility: removing the same cluster(s) on re-run with identical k value produces identical sample exclusions.

## Limitations

- k-means clustering is sensitive to the choice of k; no automatic method is provided; visual inspection of dendrograms is required to set k appropriately.
- Outlier detection is performed in the full metabolite measurement space; true biological outliers (e.g., patients with unusual metabolism) may be discarded if their signal is strong enough to form a separate cluster.
- Imputation cutoff (e.g., cutoff=0.4 for ≥60% non-missing metabolites) influences which samples are retained; highly imputed samples may dominate the 'outlier' cluster and should be reviewed before removal.
- The method does not account for known batch variables (e.g., MS run, operator, reagent lot); batch-driven outliers should ideally be removed or harmonized before outlier detection.

## Evidence

- [methods] To identify outliers, the dendrogram also displays the results of a k-means clustering. In the examplary data we set 2 clusters (k=2): "To identify outliers, the dendrogram also displays the results of a k-means clustering. In the examplary data we set 2 clusters (k=2)"
- [methods] the function `outlier_heatmap` is provided. The sample annotation shows the number of missing metabolites per sample as a proxy of the impact of imputation on clustering.: "the function `outlier_heatmap` is provided. The sample annotation shows the number of missing metabolites per sample as a proxy of the impact of imputation on clustering."
- [methods] met <- remove_cluster(met,cluster=1): "met <- remove_cluster(met,cluster=1)"
- [other] Detect and remove outlier samples via outlier_heatmap with k=2 k-means clustering, then apply remove_cluster to exclude identified outlier cluster(s).: "Detect and remove outlier samples via outlier_heatmap with k=2 k-means clustering, then apply remove_cluster to exclude identified outlier cluster(s)."
- [methods] quality_plot(met, group_factor="tumor_normal", label_colors=c("darkseagreen","dodgerblue")): "quality_plot(met, group_factor="tumor_normal", label_colors=c("darkseagreen","dodgerblue"))"
