---
name: normalization-quality-assessment
description: Use when after completing intra-batch and inter-batch normalisation steps on a SummarizedExperiment object containing metabolomics assays. Use it to confirm that a normalisation method (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3935
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - hRUV
  - R
  - dplyr
  - SummarizedExperiment
  - Metanorm
derived_from:
- doi: 10.1101/2020.12.21.423723
  title: hRUV
- doi: 10.1101/2025.09.30.679445v1
  title: ''
- doi: 10.1021/acs.analchem.5c06841
  title: ''
evidence_spans:
- '`hRUV` is a package for normalisation of multiple batches of metabolomics data'
- '`hRUV` is a package for normalisation of multiple batches of metabolomics data in a hierarchical strategy'
- Install the R package from GitHub using the `devtools` package
- we will load the hRUV package and other packages required for the demonstration... library(dplyr)
- The R package implements three (new) robust normalization methods
- Metanorm supports robust metabolomics data normalization across scales and experimental designs
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_hruv_cq
    doi: 10.1101/2020.12.21.423723
    title: hRUV
  - build: coll_metanorm_cq
    doi: 10.1101/2025.09.30.679445v1
    title: Metanorm
  dedup_kept_from: coll_hruv_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2020.12.21.423723
  all_source_dois:
  - 10.1101/2020.12.21.423723
  - 10.1101/2025.09.30.679445v1
  - 10.1021/acs.analchem.5c06841
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# normalization-quality-assessment

## Summary

Visual comparison of PCA plots before and after batch normalisation to assess whether unwanted variation (batch effect) has been effectively removed from metabolomics data. This skill validates the efficacy of hierarchical RUV-based normalisation by detecting absence of batch clustering post-treatment.

## When to use

Apply this skill after completing intra-batch and inter-batch normalisation steps on a SummarizedExperiment object containing metabolomics assays. Use it to confirm that a normalisation method (e.g., hRUV's loessShort_concatenate) has eliminated the strong batch-effect clustering visible in PCA of the raw imputed assay (rawImpute). This is particularly important when working with multi-batch metabolomics studies where batch effects obscure biological signal and sample replicates have been used for normalisation estimation.

## When NOT to use

- Input does not contain a pre-normalisation assay (rawImpute) for baseline comparison — assessment requires before/after contrast.
- Batch_info metadata is missing or incompletely assigned — colour-coding by batch is essential for detecting batch-driven clustering.
- Single-batch data or data without replicate structure — batch effects and their removal are undefined in single-batch studies.

## Inputs

- SummarizedExperiment object with rawImpute assay (log2-transformed, imputed)
- SummarizedExperiment object with loessShort_concatenate assay (hierarchically normalised)
- batch_info metadata column (factor indicating batch assignment for each sample)

## Outputs

- PCA plot of rawImpute assay coloured by batch_info
- PCA plot of loessShort_concatenate assay coloured by batch_info
- Qualitative assessment of batch-effect removal (absent/reduced/persistent)

## How to apply

Load two assays from the same SummarizedExperiment object: the pre-normalisation rawImpute assay and the post-normalisation loessShort_concatenate assay. Generate two PCA plots using hRUV::plotPCA, both coloured by batch_info metadata. In the rawImpute plot, you should observe tight clustering of samples by their batch identifier, indicating strong batch effect. In the loessShort_concatenate plot, samples should be distributed without batch-driven stratification, suggesting batch effect removal. Compare the two plots qualitatively: if batch-coloured clustering is absent or substantially reduced in the normalised assay while biological structure is preserved, normalisation has succeeded. Document any residual clustering as potential indication of incomplete normalisation or unremovable technical factors.

## Related tools

- **hRUV** (Provides plotPCA function for generating batch-coloured PCA visualisations and performs hierarchical normalisation generating the loessShort_concatenate assay.) — https://github.com/SydneyBioX/hRUV
- **SummarizedExperiment** (Container object storing both rawImpute and loessShort_concatenate assays along with batch_info metadata required for assessment.)
- **dplyr** (Supporting package for data wrangling and filtering within normalisation and visualisation workflows.)

## Examples

```
hRUV::plotPCA(dat, assay='rawImpute', color_by='batch_info'); hRUV::plotPCA(dat, assay='loessShort_concatenate', color_by='batch_info')
```

## Evaluation signals

- Pre-normalisation PCA (rawImpute) exhibits visually distinct, tight clustering when samples are coloured by batch_info identifier.
- Post-normalisation PCA (loessShort_concatenate) shows absence of batch-driven stratification; samples are intermixed across batch colours in the first two principal components.
- Variance explained by the first two PCs remains comparable or increases post-normalisation, indicating biological signal is retained while batch signal is removed.
- No systematic separation of batches along any visible principal component axis in the loessShort_concatenate plot.
- Biological covariates (e.g., disease status, treatment group) should be visually apparent or recoverable in post-normalisation PCA if present in the data.

## Limitations

- Visual assessment is qualitative and subjective; quantitative batch-effect metrics (e.g., silhouette coefficients, entropy of batch mixing) are not provided by this skill alone.
- PCA captures only linear variance; non-linear batch effects may not be visible and may persist in the normalised assay.
- Successful batch-effect removal in PCA does not guarantee removal across all metabolite features; individual features may retain batch-correlated signals.
- Requires sufficient sample replication within and between batches for hRUV normalisation to be effective; sparse replicate designs may result in incomplete batch correction.

## Evidence

- [intro] PCA visualisation of rawImpute assay shows strong batch effect, whereas PCA of the loessShort_concatenate normalised assay no longer displays batch effect when coloured by batch_info.: "PCA visualisation of rawImpute assay shows strong batch effect, whereas PCA of the loessShort_concatenate normalised assay no longer displays batch effect when coloured by batch_info."
- [intro] Generate a PCA plot using hRUV::plotPCA with rawImpute assay colored by batch_info to visualize the pre-normalization batch effect; Generate a second PCA plot using hRUV::plotPCA with loessShort_concatenate assay colored by batch_info to visualize the post-normalization batch structure; Compare the two plots to confirm batch clustering is absent in the normalized assay.: "Generate a PCA plot using hRUV::plotPCA with rawImpute assay colored by batch_info to visualize the pre-normalization batch effect. Generate a second PCA plot using hRUV::plotPCA with"
- [readme] Our novel tool is a novel hierarchical approach to removing unwanted variation by harnessing information from sample replicates embedded in the seequence of experimental runs/batches and applying signal drift correction with robust linear or non-linear smoothers.: "Our novel tool is a novel hierarchical approach to removing unwanted variation by harnessing information from sample replicates embedded in the seequence of experimental runs/batches and applying"
