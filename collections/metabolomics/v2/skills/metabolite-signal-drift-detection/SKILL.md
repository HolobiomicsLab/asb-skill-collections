---
name: metabolite-signal-drift-detection
description: Use when when you have multi-batch metabolomics data (SummarizedExperiment
  object with raw or log-transformed assays) and need to assess whether specific metabolites
  exhibit systematic signal drift across experimental run order or strong batch effects
  that would justify hierarchical normalisation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - hRUV
  - RUV-III
  - R
  - dplyr
  - SummarizedExperiment
  - ggplot2
  techniques:
  - LC-MS
  - GC-MS
  - NMR
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1101/2020.12.21.423723
  title: hRUV
evidence_spans:
- '`hRUV` is a package for normalisation of multiple batches of metabolomics data'
- '`hRUV` is a package for normalisation of multiple batches of metabolomics data
  in a hierarchical strategy'
- 'utilises 2 types of replicates: intra-batch and inter-batch replicates to estimate
  the unwanted variation within and between batches with RUV-III'
- Install the R package from GitHub using the `devtools` package
- we will load the hRUV package and other packages required for the demonstration...
  library(dplyr)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_hruv_cq
    doi: 10.1101/2020.12.21.423723
    title: hRUV
  dedup_kept_from: coll_hruv_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2020.12.21.423723
  all_source_dois:
  - 10.1101/2020.12.21.423723
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-signal-drift-detection

## Summary

Detect and visualize run-order signal drift and batch effects in individual metabolites across multiple LC-MS batches using diagnostic run plots. This skill identifies whether metabolite intensities vary systematically with instrument run order or batch identity, revealing normalisation targets before applying correction.

## When to use

When you have multi-batch metabolomics data (SummarizedExperiment object with raw or log-transformed assays) and need to assess whether specific metabolites exhibit systematic signal drift across experimental run order or strong batch effects that would justify hierarchical normalisation. Apply this skill after log transformation and data cleaning (threshold filtering and imputation) but before committing to a normalisation strategy.

## When NOT to use

- Input data lacks run-order or batch metadata in colData — drift detection requires explicit sequencing information.
- Assay has not been log-transformed and cleaned (threshold filtering and k-nearest neighbour imputation); run plots on uncleaned raw data will be dominated by missing-value artifacts rather than true drift.
- Metabolite has >50% missing values per batch — hRUV::clean will exclude it, and plotRun cannot visualize absent signals reliably.

## Inputs

- SummarizedExperiment object with rawImpute assay (log-transformed, cleaned metabolomics data)
- Metabolite identifiers (character vector or feature names from rowData)
- Run order metadata (vector of run positions per sample in colData)

## Outputs

- hRUV::plotRun diagnostic plot objects (ggplot/plotly) showing metabolite intensity vs. run order, colored or faceted by batch
- Visual assessment of signal drift trajectory (drift direction, magnitude, presence of batch discontinuities)

## How to apply

Load the metabolomics data as a SummarizedExperiment object and apply log transformation (log2(raw + 1)) followed by data cleaning with hRUV::clean (threshold = 0.5, method = 'intersect') to produce a rawImpute assay. Generate hRUV::plotRun diagnostic plots for individual metabolites of interest (e.g., 1-methylhistamine, GlucosePos2) from the rawImpute assay, inspecting for visual trends in intensity as a function of run order or batch grouping. Metabolites showing clear upward/downward drift trajectories, strong between-batch offsets, or systematic run-to-run variation are candidates for hierarchical normalisation with intra-batch loess smoothing and inter-batch RUV-III (k=5). Visual comparison between rawImpute and post-normalisation assays (e.g., loessShort_concatenate) confirms whether drift and batch effects are corrected.

## Related tools

- **hRUV** (Provides plotRun diagnostic function to generate run-order scatter plots; also provides clean function for upstream data curation (threshold filtering, imputation)) — https://github.com/SydneyBioX/hRUV
- **SummarizedExperiment** (Data container for multi-assay metabolomics data with row and column metadata; required input format for hRUV workflows) — https://bioconductor.org/packages/SummarizedExperiment
- **RUV-III** (Unwanted-variation estimation engine used downstream after drift detection to correct batch effects via hierarchical replicates)
- **dplyr** (Data manipulation and metadata filtering to subset metabolites or runs for focused drift analysis)
- **ggplot2** (Underlying plotting library for hRUV::plotRun diagnostic visualizations)

## Examples

```
library(hRUV); dat_clean <- hRUV::clean(dat_list, threshold=0.5, method='intersect', assay='logRaw', newAssay='rawImpute'); p1 <- hRUV::plotRun(dat_clean, assay='rawImpute', feature='1-methylhistamine'); p2 <- hRUV::plotRun(dat_clean, assay='loessShort_concatenate', feature='1-methylhistamine'); gridExtra::grid.arrange(p1, p2, ncol=2)
```

## Evaluation signals

- Visual inspection of plotRun output shows clear run-order trend (upward, downward, or cyclical) or sharp batch-to-batch offsets for target metabolites, consistent with instrumental drift or batch discontinuities.
- Comparison of rawImpute vs. post-normalisation (loessShort_concatenate) plotRun outputs shows attenuation or elimination of visual drift trajectories and batch offsets in the normalised assay.
- Metabolites with detected drift show systematic change in median intensity or variance across run quartiles (early vs. late runs), measurable as a non-zero slope or significant batch-level ANOVA effect.
- Absence of drift in control metabolites (QC pools or internal standards) should show flat, batch-independent intensity profiles in plotRun — if present, indicates drift detection is working.
- Reproducibility: the same set of metabolites flagged for drift in rawImpute should be consistently visualized across independent invocations of plotRun with identical parameters.

## Limitations

- plotRun is a visual diagnostic tool; it does not provide statistical hypothesis tests or p-values for drift significance — drift judgement is subjective and may require practitioner domain knowledge.
- Effectiveness depends critically on upstream data cleaning (hRUV::clean threshold = 0.5 and intersect method); if metabolites are not quantified consistently across batches, run plots will show sparse, uninformative point clouds.
- Run-order metadata must be accurate and complete in colData; if run order is miscoded or missing, plotRun cannot detect true drift patterns.
- hRUV normalisation (loess + RUV-III) may not fully eliminate drift if true instrumental degradation or calibration failure occurred; severe drift may indicate need for instrumental maintenance rather than computational correction.
- The skill applies to LC-MS metabolomics formatted as SummarizedExperiment; applicability to other assay platforms (GC-MS, NMR, or non-targeted lipidomics) is not demonstrated in the source material.

## Evidence

- [full_text] Research question and finding from task_004: "hRUV normalisation eliminates signal drift in 1-methylhistamine and strong batch effects in GlucosePos2 that were present in the rawImpute assay, as demonstrated by run plots comparing raw and"
- [full_text] Workflow step: generate diagnostic plots before normalisation: "Generate hRUV::plotRun diagnostic plots for the rawImpute assay showing run-order variation for 1-methylhistamine and GlucosePos2. Generate hRUV::plotRun diagnostic plots for the"
- [intro] Data cleaning prerequisite: "Clean the data using hRUV::clean with threshold = 0.5, method = 'intersect', on the logRaw assay to produce rawImpute."
- [readme] Tool capability description from README: "Our novel tool is a novel hierarchical approach to removing unwanted variation by harnessing information from sample replicates embedded in the seequence of experimental runs/batches and applying"
- [readme] Multi-batch data requirement: "hRUV is a package for normalisation of multiple batches of metabolomics data in a hierarchical strategy with use of samples replicates in large-scale studies."
