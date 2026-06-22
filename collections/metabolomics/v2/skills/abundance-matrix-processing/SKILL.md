---
name: abundance-matrix-processing
description: Use when you have multiple CSV files containing feature-by-sample matrices from different analytical experiments or batches, each with mass, retention time, intensity, isotope, and adduct information across different samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3801
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - LargeMetabo
  - ggplot2
  - mixOmics
  - ComBat (via sva Bioconductor package)
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# abundance-matrix-processing

## Summary

Transform raw feature-by-sample metabolomic intensity matrices into cleaned, batch-corrected, and integrated data ready for marker identification and statistical analysis. This skill encompasses data integration across multiple analytical experiments, batch effect removal, and sample separation visualization.

## When to use

You have multiple CSV files containing feature-by-sample matrices from different analytical experiments or batches, each with mass, retention time, intensity, isotope, and adduct information across different samples. Use this skill when you need to align features across datasets, remove unwanted batch variations, and prepare a unified matrix for downstream marker identification or statistical testing.

## When NOT to use

- Input is already a single, pre-integrated, and batch-corrected feature table; re-running integration will introduce redundant alignment steps.
- Data lacks consistent mass and retention time information across files; feature alignment will fail or produce spurious matches.
- Samples are not assigned to well-defined groups or batches; batch removal algorithms require batch metadata to function.

## Inputs

- Multiple CSV files, each containing a feature-by-sample matrix with mass, retention time, intensity, isotope, and adduct information
- Sample group labels (finalLabel): a vector assigning each sample to a group or condition
- Mass and retention time tolerances (numeric parameters in ppm or seconds)

## Outputs

- Integrated and batch-corrected feature-by-sample abundance matrix (finalData)
- Aligned feature metadata (mass, retention time, isotope, adduct)
- Sample separation visualization (PCA, HCA, or PLS-DA plot) confirming batch removal and group clustering

## How to apply

First, prepare input CSV files with feature-by-sample matrices ensuring the first two columns contain mass and retention time, with sample names in the first row and sample data in subsequent columns. Call Integrate_Data() with specified mass tolerance (e.g., mzTolerance = 0.1) and retention time tolerance (e.g., RTTolerance = 10) to align features across datasets. Next, apply Removal_Batch() using one of three algorithms—batch mean-centering (BMC/PAMR), empirical Bayes (ComBat/EB), or global normalization (GlobalNorm)—to remove batch effects. Finally, extract the finalData matrix and finalLabel vector and visualize sample separation using Sample_Separation() with one of four methods (HCA, PCA, PLS-DA, OPLS-DA) to confirm that samples cluster appropriately by group, indicating successful integration and batch correction.

## Related tools

- **LargeMetabo** (Primary R package providing Integrate_Data(), Removal_Batch(), and Sample_Separation() functions for data integration, batch effect removal, and visualization) — https://github.com/LargeMetabo/LargeMetabo
- **ggplot2** (Underlying visualization engine used by Sample_Separation() for generating publication-quality separation plots)
- **mixOmics** (Dependency for multivariate analysis methods (PLS-DA, OPLS-DA) used in sample separation)
- **ComBat (via sva Bioconductor package)** (Empirical Bayes batch correction algorithm available as Removal_Batch() option)

## Examples

```
AlignData <- Integrate_Data(MutileGroup, RTTolerance1 = 10, mzTolerance1 = 0.1, RTTolerance2 = 10, mzTolerance2 = 0.1); DataAfterBatch <- Removal_Batch(MutileAlign, n = 3, algorithm = "BMC/PAMR"); Sample_Separation(MarkerData$finalData, MarkerData$finalLabel, clusters = 2, method = "HCA")
```

## Evaluation signals

- Inspect integrated matrix dimensions: feature count and sample count should match expectations, and no duplicate samples or features should be present.
- Verify batch effect removal by comparing PCA or HCA plots before and after Removal_Batch(): batch-driven clustering should diminish and biological groups should become more distinct.
- Confirm retention time and mass alignment consistency: aligned features should have within-tolerance mass differences (e.g., < 0.1 Da) and retention time differences (e.g., < 10 s) across experiments.
- Check for missing values or zero-intensity artifacts: prevalence of zeros should be documented and below a dataset-specific threshold (often < 50% for metabolomic data).
- Validate sample separation results: samples from the same group should cluster together in visualizations, and replicate samples should be more similar to each other than to other groups.

## Limitations

- Batch effect removal effectiveness depends on batch structure and composition; if batches are confounded with biological groups, algorithms may remove legitimate biological signal.
- Mass and retention time tolerances must be tuned to the analytical platform and experiment design; overly loose tolerances risk false feature matches, while tight tolerances may miss true alignments.
- Sample separation visualization does not provide statistical significance testing; visual clustering confirmation should be supplemented with statistical tests (e.g., PERMANOVA, silhouette analysis) before publication.
- Integration assumes features are represented consistently across datasets; highly variable feature detection or instrumental drift across batches may produce incomplete or unreliable aligned matrices.

## Evidence

- [readme] Before data integration, the csv files containing a feature-by-sample matrix should be prepared in advance. Each dataset (csv file) contains five essential columns providing the information of mass, retention time, intensity, isotope and adduct.: "Before data integration, the csv files containing a feature-by-sample matrix should be prepared in advance. Each dataset (csv file) contains five essential columns providing the information of mass,"
- [readme] For data integration, multiple datasets from different analytical experiments can be used as the input of the LargeMetabo package.: "For data integration, multiple datasets from different analytical experiments can be used as the input of the LargeMetabo package."
- [readme] After data integration, it was essential to remove the unwanted variations among different batches.: "After data integration, it was essential to remove the unwanted variations among different batches."
- [readme] Various methods are provided in the LargeMetabo package for removing batch effects in different analytical experiments, including batch mean-centering (BMC/PAMR), the empirical Bayes method (ComBat/EB), and global normalization (GlobalNorm).: "Various methods are provided in the LargeMetabo package for removing batch effects in different analytical experiments, including batch mean-centering (BMC/PAMR), the empirical Bayes method"
- [readme] There are four sample separation methods for visualizing the clustering and separation of different samples.: "There are four sample separation methods for visualizing the clustering and separation of different samples."
- [other] The Marker_Identify() function with method='FC' accepts a data matrix (finalData) and corresponding sample labels (finalLabel), and returns a MarkerResult object containing an FC_table with ranked metabolic markers identified by fold change analysis.: "The Marker_Identify() function with method='FC' accepts a data matrix (finalData) and corresponding sample labels (finalLabel), and returns a MarkerResult object"
