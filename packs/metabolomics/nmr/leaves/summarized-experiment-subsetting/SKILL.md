---
name: summarized-experiment-subsetting
description: Use when when you have a SummarizedExperiment containing metabolomic
  abundances and a corresponding vector of quality metrics (e.g., coefficient of variation
  computed across QC samples), and you need to filter to retain only features meeting
  a reproducibility threshold (e.g., CV ≤ 0.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - Bioconductor
  - MWASTools
  techniques:
  - NMR
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1093/bioinformatics/btx477
  title: MWASTools
evidence_spans:
- Assuming that R (>=3.3) and Bioconductor have been correctly installed
- Here, we present a package to perform MWAS using univariate hypothesis testing
- '"MWASTools" is an R package designed to provide an integrated and user-friendly
  pipeline'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mwastools_cq
    doi: 10.1093/bioinformatics/btx477
    title: MWASTools
  dedup_kept_from: coll_mwastools_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btx477
  all_source_dois:
  - 10.1093/bioinformatics/btx477
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# summarized-experiment-subsetting

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Subset a Bioconductor SummarizedExperiment object to retain only rows (metabolic features) meeting quality criteria, such as coefficient of variation thresholds. This skill is essential for removing non-reproducible or low-quality features from metabolomic datasets before downstream association analysis.

## When to use

When you have a SummarizedExperiment containing metabolomic abundances and a corresponding vector of quality metrics (e.g., coefficient of variation computed across QC samples), and you need to filter to retain only features meeting a reproducibility threshold (e.g., CV ≤ 0.30) to ensure robust downstream statistical inference.

## When NOT to use

- The input SummarizedExperiment has already been pre-filtered by the data provider or in a prior pipeline step — re-filtering may remove additional features unnecessarily.
- Quality metrics have not yet been computed (e.g., QC_CV has not been run) — subsetting without valid thresholds is arbitrary.
- The threshold value is not justified or validated for your analytical context (e.g., CV_th = 0.30 may be too stringent for some metabolite classes or platforms).

## Inputs

- SummarizedExperiment object (metabo_SE) with metabolic feature abundances in assay matrix (rows=features, columns=samples)
- Named numeric vector of quality metrics (metabo_CV) with one value per feature, indexed by feature name

## Outputs

- Filtered SummarizedExperiment object containing only features passing the quality threshold, with identical sample structure

## How to apply

Extract the quality metric vector (e.g., metabo_CV from QC_CV computation) corresponding to each feature in the SummarizedExperiment. Create a logical index by comparing each metric value against the threshold (e.g., CV_th = 0.30). Use this index to subset both the assay matrix (retaining columns for all samples) and the feature annotation rows. Return a new SummarizedExperiment object containing only the passing features, preserving sample metadata and assay structure. The rationale is that features with high coefficient of variation across QC samples indicate poor reproducibility and will introduce noise and false associations in metabolite-phenotype models.

## Related tools

- **MWASTools** (R package providing CV_filter() function to automate SummarizedExperiment subsetting by coefficient of variation threshold) — https://github.com/AndreaRMICL/MWASTools
- **Bioconductor** (Provides SummarizedExperiment class and subsetting methods for genomic/metabolomic data structures)
- **R** (Programming environment for executing subsetting operations and logical indexing)

## Examples

```
filtered_metabo_SE <- CV_filter(metabo_SE, metabo_CV, CV_th = 0.30)
```

## Evaluation signals

- Output SummarizedExperiment retains all original samples (same number of columns as input)
- Output contains only rows (features) where the corresponding quality metric is ≤ threshold; verify by comparing feature names and counts before/after
- Feature metadata (rowData) and sample metadata (colData) are preserved in the filtered object
- No data corruption in assay values; all retained feature abundances match the input assay matrix
- Downstream association models computed on filtered data show improved statistical stability and reduced false positive rate compared to unfiltered data

## Limitations

- Threshold selection (e.g., CV_th = 0.30) is data- and platform-dependent; overly strict thresholds may remove true signal, while lenient thresholds retain noise. Validation against reference metabolites or spike-in controls is recommended.
- CV computed only from QC samples may not fully capture feature variability across diverse biological samples or different analytical batches.
- Subsetting by a single metric (CV) ignores other quality dimensions such as signal-to-noise ratio, detection frequency, or batch effects; complementary QC steps may be necessary.
- Loss of features reduces statistical power; downstream association tests may be underpowered if filtering is too aggressive, particularly for rare or low-abundance metabolites.

## Evidence

- [other] CV_filter(metabo_SE, metabo_CV, CV_th = 0.30) retains only metabolic features with coefficient of variation below 0.30, removing non-reproducible features from the metabolic matrix to produce a filtered SummarizedExperiment object.: "CV_filter(metabo_SE, metabo_CV, CV_th = 0.30) retains only metabolic features with coefficient of variation below 0.30, removing non-reproducible features"
- [other] Subset the SummarizedExperiment to the passing features and return the filtered metabo_SE object.: "Subset the SummarizedExperiment to the passing features and return the filtered metabo_SE object"
- [other] Apply threshold filter retaining only features where CV ≤ 0.30 to remove high-variance, low-reproducibility metabolites.: "Apply threshold filter retaining only features where CV ≤ 0.30 to remove high-variance, low-reproducibility metabolites"
- [other] The QC_CV function calculates the coefficient of variation (sd/mean) for each NMR signal across the QC samples, producing a metabo_CV output vector that quantifies signal reproducibility.: "The QC_CV function calculates the coefficient of variation (sd/mean) for each NMR signal across the QC samples, producing a metabo_CV output vector"
