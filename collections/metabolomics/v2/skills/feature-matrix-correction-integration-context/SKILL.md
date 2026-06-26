---
name: feature-matrix-correction-integration-context
description: Use when after integrating feature matrices from multiple analytical
  experiments (batches) into a single MutileAlign matrix. Batch effects manifest as
  systematic differences in metabolite intensities across batches even when analyzing
  the same samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3406
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0091
  tools:
  - LargeMetabo
  - R
  - ggplot2
  - factoextra
  license_tier: restricted
  provenance_tier: literature
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

# Batch-effect correction on integrated multi-batch metabolomic feature matrices

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Remove unwanted batch variations from integrated metabolomic datasets using the Removal_Batch() function with batch mean-centering (BMC/PAMR), empirical Bayes (ComBat/EB), or global normalization (GlobalNorm) algorithms. This skill is essential after data integration to ensure that observed metabolite intensity differences reflect biological signal rather than analytical batch artifacts.

## When to use

Apply this skill after integrating feature matrices from multiple analytical experiments (batches) into a single MutileAlign matrix. Batch effects manifest as systematic differences in metabolite intensities across batches even when analyzing the same samples. Use this skill when you have: (1) an integrated feature-by-sample matrix from multiple batches, (2) known batch labels or count (n), and (3) a need to harmonize intensity scales before downstream analysis (marker identification, sample separation, annotation).

## When NOT to use

- Input is a single-batch dataset or already corrected: batch-effect removal is redundant and may introduce noise if no batch structure exists.
- Batch labels are unknown or inconsistent: Removal_Batch() requires accurate n parameter; incorrect batch assignment will produce meaningless corrections.
- Feature matrix has not yet been integrated: this skill requires a unified MutileAlign matrix; apply Integrate_Data() first to align features across batches.

## Inputs

- MutileAlign: integrated feature-by-sample matrix (rows=metabolite features, columns=samples) from multiple analytical experiments
- n: integer count of batches (e.g., 3)
- algorithm: character string specifying correction method ('BMC/PAMR', 'ComBat/EB', or 'GlobalNorm')

## Outputs

- DataAfterBatch: batch-corrected feature matrix with same dimensions as input, where unwanted batch variations have been removed

## How to apply

Load the integrated MutileAlign feature matrix into R and call the Removal_Batch() function, specifying the number of batches (n parameter, e.g., n=3) and the correction algorithm via the algorithm parameter. The LargeMetabo package provides three options: 'BMC/PAMR' (batch mean-centering with Partial Absolute Median Rule), 'ComBat/EB' (empirical Bayes), or 'GlobalNorm' (global normalization). BMC/PAMR centers batch means and applies a location/scale adjustment; empirical Bayes borrows strength across features to estimate batch effects; global normalization scales intensity by batch-specific factors. Select the algorithm based on your batch structure severity and feature count. Extract the corrected feature matrix from the function output and validate that batch-specific signal intensity distributions have converged (e.g., via PCA or heatmap inspection) before proceeding to marker identification or other downstream steps.

## Related tools

- **LargeMetabo** (R package containing Removal_Batch() function for batch-effect correction) — https://github.com/LargeMetabo/LargeMetabo
- **R** (Runtime environment (>= 3.5.0) for executing Removal_Batch() and supporting packages) — https://www.r-project.org
- **ggplot2** (Visualization of batch-corrected data distributions (e.g., PCA plots to verify correction))
- **factoextra** (PCA and clustering visualization to validate batch-effect removal)

## Examples

```
DataAfterBatch <- Removal_Batch(MutileAlign, n = 3, algorithm = "BMC/PAMR")
DataAfterBatch[1:5,1:5]
```

## Evaluation signals

- Batch-specific mean intensity differences are minimized: compare mean feature intensities before and after correction; corrected batch means should be statistically indistinguishable.
- PCA or t-SNE plot shows sample clustering by biological group rather than batch: visually inspect that batch separation has been removed while biological structure is preserved.
- Corrected feature matrix retains original dimensions and sparsity pattern: check that row count (features) and column count (samples) match input, and that zero entries remain zero.
- Algorithm-specific parameters are reasonable: BMC/PAMR should produce location and scale estimates within expected ranges; ComBat/EB posterior variances should be reduced relative to empirical estimates.
- Downstream marker identification results are reproducible: compare marker lists between correction algorithms; robust markers should appear consistently.

## Limitations

- Algorithm selection is user-dependent: the choice of BMC/PAMR, ComBat/EB, or GlobalNorm depends on batch severity, feature count, and sample size, but LargeMetabo does not automatically select the optimal algorithm.
- Assumes batch assignments are correct and complete: misspecified batch labels (wrong n or sample-to-batch mapping) will produce systematic bias in the corrected matrix.
- May over-correct if biological signal correlates with batch: if a treatment or phenotype is confounded with batch, correction may remove true biological effects.
- Designed for metabolomic data with BMC/PAMR as primary method: generalization to other omics platforms or extreme batch scenarios is not documented in the article or README.

## Evidence

- [readme] After data integration, it was essential to remove the unwanted variations among different batches: "After data integration, it was essential to remove the unwanted variations among different batches"
- [readme] Various methods are provided in the LargeMetabo package for removing batch effects in different analytical experiments, including batch mean-centering (BMC/PAMR), the empirical Bayes method (ComBat/EB), and global normalization (GlobalNorm).: "Various methods are provided in the LargeMetabo package for removing batch effects in different analytical experiments, including batch mean-centering (BMC/PAMR), the empirical Bayes method"
- [other] The Removal_Batch() function accepts a comprehensive integrated dataset (MutileAlign), the number of batches (n=3), and an algorithm parameter (BMC/PAMR) to produce a batch-corrected feature matrix: "The Removal_Batch() function accepts a comprehensive integrated dataset (MutileAlign), the number of batches (n=3), and an algorithm parameter (BMC/PAMR) to produce a batch-corrected feature matrix"
- [readme] DataAfterBatch <- Removal_Batch(MutileAlign, n = 3, algorithm = "BMC/PAMR"): "DataAfterBatch <- Removal_Batch(MutileAlign, n = 3, algorithm = "BMC/PAMR")"
