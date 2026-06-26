---
name: metabolomic-data-subsetting-by-phenotype
description: Use when you have a preprocessed MultiAssayExperiment with metabolite
  measurements across multiple phenotypic or disease subgroups, and you want to isolate
  one or more groups for comparison—for example, to compare AKT1-high versus MYC-high
  prostate tumor samples before applying diff_test for.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - MetaboDiff
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

# metabolomic-data-subsetting-by-phenotype

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Subset a MultiAssayExperiment object containing normalized metabolite measurements to retain only samples belonging to specific phenotypic groups (e.g., AKT1-high vs MYC-high tumor classes). This prepares cohort-stratified data for downstream differential abundance testing.

## When to use

You have a preprocessed MultiAssayExperiment with metabolite measurements across multiple phenotypic or disease subgroups, and you want to isolate one or more groups for comparison—for example, to compare AKT1-high versus MYC-high prostate tumor samples before applying diff_test for statistical significance.

## When NOT to use

- Input is raw, unnormalized metabolite data—normalize and impute first using normalize_met and knn_impute.
- Group factor does not exist or is not encoded in colData—first add phenotype annotations to the MultiAssayExperiment.
- You want to perform unsupervised clustering or correlation network analysis across all samples—subsetting by phenotype removes that diversity.

## Inputs

- MultiAssayExperiment object containing normalized and imputed metabolite measurements
- group factor name (string; e.g., 'tumor_groups')
- target phenotype/group levels (character vector; e.g., c('AKT1-high', 'MYC-high'))

## Outputs

- Subsetted MultiAssayExperiment object retaining only samples in the target groups
- Reduced sample count and corresponding metabolite measurement matrix

## How to apply

Identify the group factor stored in the sample metadata (colData) that encodes the phenotypic classes (e.g., 'tumor_groups' with levels 'AKT1-high' and 'MYC-high'). Use R's subsetting operators or a dedicated filtering method on the MultiAssayExperiment to retain only samples whose group factor matches your target classes. Verify that the subset operation preserves the assay (metabolite measurements), rowData (metabolite annotations), and colData (sample metadata) in the correct structure. The result is a reduced MultiAssayExperiment ready for statistical testing or network analysis.

## Related tools

- **MetaboDiff** (Provides the MultiAssayExperiment data structure and subsetting methods for metabolomic data stratification) — https://github.com/andreasmock/MetaboDiff
- **MultiAssayExperiment** (R/Bioconductor class that stores and organizes metabolite assays with linked sample metadata and row annotations)
- **R** (Language for executing subsetting operations via bracket notation and logical indexing on MultiAssayExperiment objects)

## Examples

```
# In R, after loading the preprocessed MAE object:
subset_mae <- mae[, mae$tumor_groups %in% c('AKT1-high', 'MYC-high')]
```

## Evaluation signals

- Subsetted object has fewer samples than the input (sample count equals length of target group levels multiplied by frequency in original data)
- All remaining samples have group factor values matching the specified target phenotypes
- Metabolite measurements (assay data) are preserved without modification; only row order or count may change if samples are removed
- colData and rowData structures remain intact with no loss of annotation columns or metabolite identities
- Subsequent diff_test applied to the subset produces significance results (p-values and effect sizes) for the specified comparison

## Limitations

- If group factor levels are imbalanced or very small (e.g., n < 2 per group), statistical testing on the subset may be underpowered.
- Subsetting by phenotype discards samples not in the target groups; pooling results across multiple subsets requires care to avoid multiple testing artifacts.
- If the group factor contains missing or ambiguous values, those samples will be excluded; check colData for NA or inconsistent encoding before subsetting.

## Evidence

- [other] task_005_workflow_step_2: "Subset samples to only AKT1-high and MYC-high groups using the group factor."
- [other] task_005_workflow_step_1: "Load the preprocessed human case1 MultiAssayExperiment object containing normalized and imputed metabolite measurements."
- [methods] article_methods_mae: "The function `create_mae` merges all objects into a so called `MultiAssayExperiment` object to simplify all downstream analysis."
- [readme] readme_overview: "The MetaboDiff packages aims to provide a low-level entry to differential metabolomic analysis with R by starting off with the table of metabolite measurements."
