---
name: batch-effect-removal-metabolomic-data
description: Use when after integrating feature matrices from multiple analytical experiments or batches (e.g., n=3 or more batches). Use it when batch-related systematic variations are present in the integrated dataset before proceeding to sample separation, marker identification, or annotation steps.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  tools:
  - LargeMetabo
  - R
  - mixOmics
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

# Batch-Effect Removal in Metabolomic Data

## Summary

Remove unwanted batch variations from integrated multi-batch metabolomic datasets using algorithm-specific correction methods. This skill is essential after data integration to harmonize feature intensities across analytical experiments and enable unbiased downstream analysis.

## When to use

Apply this skill after integrating feature matrices from multiple analytical experiments or batches (e.g., n=3 or more batches). Use it when batch-related systematic variations are present in the integrated dataset before proceeding to sample separation, marker identification, or annotation steps.

## When NOT to use

- Input is a single-batch dataset with no cross-batch contamination
- Feature matrix has not yet been integrated across multiple analytical experiments
- Batch information or batch labeling is unavailable or ambiguous

## Inputs

- Integrated multi-batch feature-by-sample matrix (MutileAlign format)
- Number of batches as integer (n parameter)
- Algorithm selection string (BMC/PAMR, ComBat/EB, or GlobalNorm)

## Outputs

- Batch-corrected feature matrix (same dimensions as input)
- Harmonized intensities across all batches

## How to apply

Load the integrated feature-by-sample matrix (e.g., MutileAlign output containing mass, retention time, intensity, isotope, and adduct information) into R. Call the Removal_Batch() function with three key parameters: the integrated dataset, the number of batches (n parameter, e.g., n=3), and the algorithm parameter specifying the correction method (BMC/PAMR for batch mean-centering, ComBat/EB for empirical Bayes, or GlobalNorm for global normalization). The function returns a batch-corrected feature matrix where unwanted variations among different batches have been removed. Extract and validate the corrected output before downstream analysis.

## Related tools

- **LargeMetabo** (R package housing Removal_Batch() function and batch correction algorithms (BMC/PAMR, ComBat/EB, GlobalNorm)) — https://github.com/LargeMetabo/LargeMetabo
- **R** (Runtime environment (≥ 3.5.0) required to execute Removal_Batch() and dependent packages) — https://www.r-project.org
- **mixOmics** (Background package used for batch effect removal algorithms)

## Examples

```
DataAfterBatch <- Removal_Batch(MutileAlign, n = 3, algorithm = "BMC/PAMR")
DataAfterBatch[1:5,1:5]
```

## Evaluation signals

- Output feature matrix has same dimensions (rows, columns) as input integrated matrix
- Corrected intensities fall within expected physiological or analytical ranges (no NAs or infinities)
- Visualization of corrected data (e.g., PCA, hierarchical clustering) shows reduced batch-dependent clustering compared to pre-correction data
- Cross-batch coefficient of variation (CV) for reference or QC metabolites decreases after correction
- No systematic bias remains when comparing batch-specific feature distributions post-correction

## Limitations

- Algorithm choice (BMC/PAMR vs. ComBat/EB vs. GlobalNorm) must be specified a priori; no automated selection guidance is provided in the README
- Method assumes batch structure is known and correctly specified via the n parameter; misspecified batch count may produce artifacts
- Removal_Batch() assumes integrated data has been properly aligned (via Integrate_Data() step); garbage input produces garbage output
- Global normalization (GlobalNorm) may mask true biological differences if batch and treatment effects are confounded

## Evidence

- [readme] After data integration, it was essential to remove the unwanted variations among different batches: "After data integration, it was essential to remove the unwanted variations among different batches"
- [other] Removal_Batch() function accepts integrated dataset, number of batches, and algorithm parameter to produce batch-corrected feature matrix: "The Removal_Batch() function accepts a comprehensive integrated dataset (MutileAlign), the number of batches (n=3), and an algorithm parameter (BMC/PAMR) to produce a batch-corrected feature matrix"
- [readme] Multiple batch effect removal methods are provided: "Various methods are provided in the LargeMetabo package for removing batch effects in different analytical experiments, including batch mean-centering (BMC/PAMR), the empirical Bayes method"
- [readme] Example workflow for batch effect removal: "DataAfterBatch <- Removal_Batch(MutileAlign, n = 3, algorithm = "BMC/PAMR")"
