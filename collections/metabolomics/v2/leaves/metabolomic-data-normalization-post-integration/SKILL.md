---
name: metabolomic-data-normalization-post-integration
description: Use when immediately after integrating multiple metabolomic datasets
  from different analytical experiments into a unified feature-by-sample matrix. Batch
  effects manifest as systematic unwanted variations correlated with analytical batch
  rather than biological sample groups;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0092
  tools:
  - LargeMetabo
  - Removal_Batch
  - Integrate_Data
  - Sample_Separation
  - R (≥ 3.5.0)
  license_tier: restricted
derived_from:
- doi: 10.1093/bib/bbac455
  title: LargeMetabo
evidence_spans:
- install_github("LargeMetabo/LargeMetabo", force = TRUE, build_vignettes = TRUE)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_largemetabo_cq
    doi: 10.1093/bib/bbac455
    title: LargeMetabo
  dedup_kept_from: coll_largemetabo_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bib/bbac455
  all_source_dois:
  - 10.1093/bib/bbac455
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomic-data-normalization-post-integration

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Remove unwanted batch effects from integrated multi-batch metabolomic datasets using algorithm-specific correction methods (BMC/PAMR, ComBat/EB, or GlobalNorm). This skill is essential after combining feature matrices from multiple analytical experiments to restore biological signal and enable valid downstream statistical and marker identification analyses.

## When to use

Apply this skill immediately after integrating multiple metabolomic datasets from different analytical experiments into a unified feature-by-sample matrix. Batch effects manifest as systematic unwanted variations correlated with analytical batch rather than biological sample groups; this skill is triggered when you have (1) an integrated dataset (e.g., output from Integrate_Data()), (2) knowledge of the number of batches (n), and (3) a need to remove batch-driven artifacts before marker identification, sample separation, or pathway enrichment.

## When NOT to use

- Input is not an integrated dataset: if individual batch datasets have not yet been combined by Integrate_Data(), apply integration first.
- Batch structure is unknown or samples are not stratified by analytical batch: batch effect removal requires explicit batch labels or counts.
- Downstream analysis is hypothesis-agnostic exploratory work where batch-driven clustering is of scientific interest rather than a confounder.

## Inputs

- Integrated feature-by-sample matrix (e.g., MutileAlign output from Integrate_Data)
- Batch assignment vector or count (n parameter: integer ≥ 2)
- Algorithm selection parameter (character: 'BMC/PAMR', 'ComBat/EB', or 'GlobalNorm')

## Outputs

- Batch-corrected feature-by-sample matrix with batch effects removed
- Numeric matrix: rows = metabolic features, columns = samples, values = normalized intensities

## How to apply

Call the Removal_Batch() function with three mandatory parameters: (1) the integrated feature matrix (e.g., MutileAlign output containing rows as features and columns as samples); (2) the number of distinct batches (n, typically 2–5); (3) an algorithm choice ('BMC/PAMR' for batch mean-centering, 'ComBat/EB' for empirical Bayes, or 'GlobalNorm' for global normalization). Each algorithm applies different statistical assumptions: BMC/PAMR centers batch means directly; ComBat/EB uses empirical Bayes priors to estimate batch location and scale; GlobalNorm applies global intensity scaling. Select the algorithm based on batch structure severity and downstream analysis assumptions. Extract the corrected feature matrix from function output and verify that batch-driven clustering (e.g., in PCA or sample separation plots) is reduced while biological sample grouping is preserved.

## Related tools

- **Removal_Batch** (Core function that executes batch effect removal using the specified algorithm (BMC/PAMR, ComBat/EB, or GlobalNorm)) — https://github.com/LargeMetabo/LargeMetabo
- **Integrate_Data** (Prerequisite function: produces the integrated feature matrix (MutileAlign) that serves as input to Removal_Batch) — https://github.com/LargeMetabo/LargeMetabo
- **Sample_Separation** (Downstream validation tool: visualizes whether batch clustering is reduced post-correction via HCA, PCA, or other sample separation methods) — https://github.com/LargeMetabo/LargeMetabo
- **R (≥ 3.5.0)** (Execution environment required to run LargeMetabo and Removal_Batch) — https://www.r-project.org

## Examples

```
DataAfterBatch <- Removal_Batch(MutileAlign, n = 3, algorithm = "BMC/PAMR")
DataAfterBatch[1:5,1:5]
```

## Evaluation signals

- Batch-driven clustering is eliminated or dramatically reduced in PCA/sample separation plots post-correction (inspect via Sample_Separation with method='HCA' or 'PCA')
- Corrected feature matrix retains the same dimensions and sample identities as input (rows = features, columns = samples unchanged)
- Biological sample grouping (e.g., case vs. control) is preserved or enhanced; marker identification results remain consistent or improve
- Feature intensity distributions across batches become homogeneous; inspect via density plots or box plots stratified by batch
- No systematic shift in feature values post-correction; mean and variance per feature should be consistent across former batch boundaries

## Limitations

- Batch effect removal assumes batch structure is known and correctly specified (n parameter); misspecification of batch count leads to over- or under-correction.
- Different algorithms make different statistical assumptions (e.g., BMC/PAMR assumes additive batch shifts; ComBat/EB models location and scale separately); selection depends on batch severity and experimental design.
- Over-correction can remove true biological signal if batches partially confound with biological groups; validation against external biological markers is recommended.
- GlobalNorm is most conservative but may be insufficient for large systematic batch differences; BMC/PAMR and ComBat/EB are more aggressive.

## Evidence

- [intro] After data integration, it was essential to remove the unwanted variations among different batches: "After data integration, it was essential to remove the unwanted variations among different batches"
- [other] Removal_Batch() function accepts integrated dataset, batch count, and algorithm parameter: "The Removal_Batch() function accepts a comprehensive integrated dataset (MutileAlign), the number of batches (n=3), and an algorithm parameter (BMC/PAMR) to produce a batch-corrected feature matrix"
- [readme] Multiple batch correction algorithms are available in LargeMetabo: "Various methods are provided in the LargeMetabo package for removing batch effects in different analytical experiments, including batch mean-centering (BMC/PAMR), the empirical Bayes method"
- [readme] Removal_Batch function call with parameters: "DataAfterBatch <- Removal_Batch(MutileAlign, n = 3, algorithm = "BMC/PAMR")"
