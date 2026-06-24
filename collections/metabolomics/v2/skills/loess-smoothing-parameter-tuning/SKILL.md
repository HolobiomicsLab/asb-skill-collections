---
name: loess-smoothing-parameter-tuning
description: Use when your metabolomics SummarizedExperiment object shows signal drift
  across replicate measurements within individual batches (visible as systematic trends
  in PCA plots or replicate scatter), and you have intra-batch replicate samples available
  to estimate smooth drift corrections.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3391
  tools:
  - hRUV
  - RUV-III
  - R
  - SummarizedExperiment
  - NormalizeMets
  - RStudio
  - RlaPlots
  - PcaPlots
  license_tier: restricted
derived_from:
- doi: 10.1101/2020.12.21.423723
  title: hRUV
- doi: 10.1007/s11306-018-1347-7
  title: ''
evidence_spans:
- '`hRUV` is a package for normalisation of multiple batches of metabolomics data'
- '`hRUV` is a package for normalisation of multiple batches of metabolomics data
  in a hierarchical strategy'
- 'utilises 2 types of replicates: intra-batch and inter-batch replicates to estimate
  the unwanted variation within and between batches with RUV-III'
- Install the R package from GitHub using the `devtools` package
- The R software environment can be downloaded for free from the Comprehensive R Archive
  Network (CRAN)
- 'Install the NormalizeMets package by using the following function: `install.packages("NormalizeMets")`'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_hruv_cq
    doi: 10.1101/2020.12.21.423723
    title: hRUV
  - build: coll_normalizemets_cq
    doi: 10.1007/s11306-018-1347-7
    title: NormalizeMets
  dedup_kept_from: coll_hruv_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2020.12.21.423723
  all_source_dois:
  - 10.1101/2020.12.21.423723
  - 10.1007/s11306-018-1347-7
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# loess-smoothing-parameter-tuning

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Apply loess smoothing with optimized parameters (e.g., loessShort with k=5) to correct intra-batch signal drift in metabolomics assays. This non-linear smoothing technique removes unwanted variation within experimental batches while preserving true biological signal.

## When to use

Your metabolomics SummarizedExperiment object shows signal drift across replicate measurements within individual batches (visible as systematic trends in PCA plots or replicate scatter), and you have intra-batch replicate samples available to estimate smooth drift corrections. Use this when batch effects manifest as continuous signal degradation rather than discrete batch offsets.

## When NOT to use

- Input assay has not been log-transformed or imputed (rawImpute assay does not exist).
- Batch effects are discrete/offset-based rather than drift-based (consider robust linear smoothing instead).
- No intra-batch replicate samples are available to estimate smooth drift corrections.
- Metabolite data is already normalised by an orthogonal method (e.g., probabilistic quotient normalisation).

## Inputs

- SummarizedExperiment object with rawImpute assay (log-transformed, imputed metabolomics signals)
- batch metadata column identifying experimental run/batch membership
- replicate metadata column identifying intra-batch and inter-batch replicate samples

## Outputs

- loessShort_concatenate assay (normalised metabolomics signals with intra-batch drift corrected)
- SummarizedExperiment object with updated assay slot containing corrected signals

## How to apply

Within the hRUV hierarchical normalisation framework, apply loess smoothing as the intra-batch normalisation step by setting intra='loessShort' and intra_k=5 (the number of short replicate neighbors for RUV-III estimation). The loessShort variant applies non-linear smoothing to metabolite signals across the sequence of replicate samples within each batch, correcting for instrumental signal drift. The k=5 parameter controls the local neighborhood size for the RUV-III algorithm that estimates unwanted variation from replicate correlations. After smoothing, extract the resulting loessShort_concatenate assay from the returned SummarizedExperiment object. This approach is applied after log transformation and k-nearest neighbor imputation on the rawImpute assay.

## Related tools

- **hRUV** (Wrapper function implementing hierarchical RUV-based normalisation; calls loess smoothing as intra-batch normalisation step with parameter intra='loessShort') — https://github.com/SydneyBioX/hRUV
- **RUV-III** (Statistical algorithm for unwanted variation estimation using replicates; applied post-loess smoothing to refine intra-batch correction) — https://github.com/SydneyBioX/hRUV
- **SummarizedExperiment** (Bioconductor data structure holding metabolomics assay matrix, batch/replicate metadata, and output normalised assays) — https://bioconductor.org/packages/SummarizedExperiment

## Examples

```
hRUV::hRUV(dat, intra='loessShort', inter='concatenate', intra_k=5, inter_k=5)
```

## Evaluation signals

- PCA plot of loessShort_concatenate assay shows reduced within-batch scatter and replicate clustering compared to rawImpute assay.
- Replicate samples within each batch have correlated values in the loessShort_concatenate assay (Pearson r > 0.95 within replicates).
- Metabolite signal drift across batch sequence (e.g., time-ordered instrumental degradation) is visually attenuated or eliminated in smoothed assay.
- MA plots or Bland-Altman plots between intra-batch replicates show symmetric scatter around zero post-correction.
- Output assay dimensions match input rawImpute assay (same features × samples); no features or samples are dropped.

## Limitations

- loessShort parameter choice (k=5) is fixed empirically; no automatic parameter selection method is provided for datasets with different replicate spacing or batch sizes.
- Loess smoothing assumes monotonic or smooth drift; it may over-smooth sharp instrumental transitions or sample preparation artifacts.
- Effectiveness depends critically on intra-batch replicate density and placement; sparse or irregularly spaced replicates may yield poor drift estimates.
- No changelog is available; version stability and backward compatibility of loessShort implementation across hRUV releases are undocumented.

## Evidence

- [intro] For intra batch normalisation, we perform loess smoothing on samples and RUV-III using short replicates with parameter k set to 5: "For intra batch normalisation, we perform loess smoothing on samples and RUV-III using short replicates with parameter k set to 5"
- [full_text] Call the hRUV function with parameters: intra='loessShort' (intra-batch non-linear smoothing), inter='concatenate' (inter-batch hierarchical structure), intra_k=5 (short replicate neighbors for intra-batch RUV-III): "Call the hRUV function with parameters: intra='loessShort' (intra-batch non-linear smoothing), inter='concatenate' (inter-batch hierarchical structure), intra_k=5 (short replicate neighbors for"
- [full_text] After applying hruv normalisation with loessShort intra-batch and concatenate inter-batch parameters, the resulting loessShort_concatenate assay eliminates batch effects visible in PCA plots and corrects signal drift across experimental runs.: "After applying hruv normalisation with loessShort intra-batch and concatenate inter-batch parameters, the resulting loessShort_concatenate assay eliminates batch effects visible in PCA plots and"
- [readme] Our novel tool is a novel hierarchical approach to removing unwanted variation by harnessing information from sample replicates embedded in the seequence of experimental runs/batches and applying signal drift correction with robust linear or non-linear smoothers.: "Our novel tool is a novel hierarchical approach to removing unwanted variation by harnessing information from sample replicates embedded in the seequence of experimental runs/batches and applying"
- [full_text] Load the SummarizedExperiment object containing the rawImpute assay and batch/replicate metadata. Call the hRUV function with parameters... Extract the resulting normalised loessShort_concatenate assay from the returned SummarizedExperiment object.: "Load the SummarizedExperiment object containing the rawImpute assay and batch/replicate metadata. Call the hRUV function with parameters... Extract the resulting normalised loessShort_concatenate"
