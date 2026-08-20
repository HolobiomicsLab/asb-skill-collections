---
name: metabolite-correlation-network-construction
description: Use when after variance-stabilizing normalization and imputation of metabolomic
  data when you have a MultiAssayExperiment object containing normalized metabolite
  abundances and wish to identify groups of co-abundant metabolites that may share
  biochemical pathways or regulatory mechanisms.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - MetaboDiff
  - WGCNA
  - R
  - MultiAssayExperiment
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1093/bioinformatics/bty344
  title: MetaboDiff
- doi: 10.1158/0008-5472.can-14-1490
  title: ''
evidence_spans:
- '`MetaboDiff` is available for all operating systems and can be installed via Github'
- met = knn_impute(met,cutoff=0.4)
- install.packages("WGCNA")
- The core concept of the so called "weighted" correlation analysis by Langfelder
  and Horvarth
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Reconstruct the metabolic correlation network and module identification with WGCNA + Dynamic Tree Cut

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Build a weighted metabolic correlation network from normalized metabolite abundance data, then partition it into co-expression modules using hierarchical clustering and dynamic branch cutting. This skill enables discovery of functionally coherent metabolite groups and identification of sample trait associations within metabolic modules.

## When to use

Apply this skill after variance-stabilizing normalization and imputation of metabolomic data when you have a MultiAssayExperiment object containing normalized metabolite abundances and wish to identify groups of co-abundant metabolites that may share biochemical pathways or regulatory mechanisms. Use it as a precursor to trait association analysis or when exploring the modular structure of the metabolome.

## When NOT to use

- Input metabolite data has not been normalized (e.g., raw intensity values still contain batch effects or variance heterogeneity) — apply variance-stabilizing normalization first.
- Missing data prevalence exceeds the imputation tolerance — validate that k-nearest neighbor imputation with appropriate cutoff has already been performed.
- The research question requires single-metabolite differential abundance testing rather than co-expression discovery — use univariate statistical tests instead.

## Inputs

- MultiAssayExperiment object with normalized and imputed metabolite measurements (norm_imputed assay)
- Metabolite rowData with SUB_PATHWAY annotations

## Outputs

- Module color vector (dendrogram branch assignments)
- Metabolite-to-module membership table
- Named module assignments mapping metabolites to pathway-derived module labels

## How to apply

Load the normalized and imputed MultiAssayExperiment object (norm_imputed assay) containing metabolite abundance data. Compute a biweight midcorrelation similarity matrix across all metabolites, chosen for its robustness to outliers compared to absolute correlation. Apply soft thresholding with power β=3 to convert the similarity matrix to an adjacency matrix, then calculate dissimilarity as 1 − adjacency. Perform hierarchical clustering on the dissimilarity matrix to construct a dendrogram. Apply dynamic branch cutting (rather than fixed-height cutoffs, which perform suboptimally on complex dendrograms) with a minimum module size threshold of 5 metabolites to identify stable clusters. Extract the module color vector and metabolite-to-module assignments from the dendrogram. For interpretability, identify the most abundant SUB_PATHWAY annotation within each module and assign module names accordingly. Output the result as a table mapping metabolite IDs to module names or colors.

## Related tools

- **MetaboDiff** (Provides high-level wrapper functions and data structures (MultiAssayExperiment) for correlation network construction and module detection in metabolomic workflows) — https://github.com/andreasmock/MetaboDiff
- **WGCNA** (Supplies the underlying hierarchical clustering, soft thresholding, and adjacency computation algorithms for weighted correlation network analysis)
- **R** (Execution environment for all computational steps; requires version 4.0.2 or higher for MetaboDiff compatibility)
- **MultiAssayExperiment** (Unified data container that integrates assay matrices, row annotations (metabolite metadata), and column annotations (sample traits) for modular analysis)

## Examples

```
# After loading norm_imputed MAE object:
bicor_matrix <- bicor(t(assay(mae, "norm_imputed")));
adj_matrix <- (0.5 + 0.5 * bicor_matrix)^3;
diss_matrix <- 1 - adj_matrix;
hc <- hclust(as.dist(diss_matrix), method="average");
module_colors <- cutreeDynamic(dendro=hc, distM=diss_matrix, minClusterSize=5, method="hybrid");
```

## Evaluation signals

- Dendrogram structure is tree-like and readable; no single massive module dominates (absence of this suggests poor parameter choice or extreme data skew).
- Each identified module contains at least 5 metabolites (the hard minimum threshold) and is labeled with a consistent SUB_PATHWAY annotation, indicating biochemical coherence.
- Module membership is reproducible: re-running with the same parameters produces identical module colors and assignments.
- Modules show expected size distribution (neither fragmented into singletons nor merged into one giant cluster); visual inspection of the dendrogram confirms clean branch separation.
- Module-level trait associations (e.g., correlation of module eigenvector with sample phenotype) are stronger than random expectation, validating functional relevance.

## Limitations

- Soft thresholding power (β=3) is fixed in the described workflow; sensitivity to this parameter is not explored — practitioners may need to test alternative powers for their data.
- Minimum module size of 5 metabolites is a default choice; very small sample sizes or sparse networks may require adjustment, and very large networks may merge biologically distinct clusters.
- Dynamic branch cutting depends on dendrogram topology and can be sensitive to tied distances or numerical precision; results should be validated against prior knowledge or alternative clustering methods.
- Module naming by 'most abundant SUB_PATHWAY' is heuristic and may not capture all metabolites in a module or reflect their primary function — manual curation is recommended.
- No explicit handling of missing data within the correlation step; relies entirely on upstream k-nearest neighbor imputation, which assumes data are missing at random.

## Evidence

- [methods] biweight midcorrelation as a similarity measure robust to outliers: "Biweight midcorrelation was used as a similiarity measure as it is more robust to outliers than the absolute correlation coefficient"
- [methods] soft thresholding with power β=3 to convert similarity to adjacency: "Apply soft thresholding with power β=3 to convert similarity to adjacency, then compute dissimilarity as 1 − adjacency."
- [methods] dynamic branch cutting outperforms fixed-height cutoffs on complex dendrograms: "We employed the dynamic branch cut method developed by Langfelder and colleagues, as constant height cutoffs exhibit suboptimal performance on complicated dendrograms."
- [methods] minimum module size threshold of 5 metabolites: "modules are detected by applying a branch cutting method with a minimal module size of 5 metabolites"
- [readme] MetaboDiff offers exploration of sample traits in metabolic correlation networks: "As a key functionality, MetaboDiffs offers the exploration of sample traits in a data-derived metabolic correlation network."
