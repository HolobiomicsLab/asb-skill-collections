---
name: pre-post-normalisation-comparison
description: Use when after completing a hierarchical batch normalisation workflow
  (e.g., hRUV with intra-batch loess smoothing and inter-batch RUV-III correction)
  to verify that normalisation has eliminated run-order signal drift and batch-specific
  effects visible in raw or imputed assays.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - hRUV
  - RUV-III
  - R
  - dplyr
  - SummarizedExperiment
  license_tier: open
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

# pre-post-normalisation-comparison

## Summary

Visual comparison of metabolite signal characteristics before and after batch normalisation to confirm that unwanted variation (signal drift, batch effects) has been effectively removed. This skill uses diagnostic run plots to validate normalisation efficacy on individual metabolites across experimental batches.

## When to use

Apply this skill after completing a hierarchical batch normalisation workflow (e.g., hRUV with intra-batch loess smoothing and inter-batch RUV-III correction) to verify that normalisation has eliminated run-order signal drift and batch-specific effects visible in raw or imputed assays. Use when you need to demonstrate that systematic technical variation has been corrected before proceeding to downstream statistical analysis.

## When NOT to use

- Input assays have not completed both intra-batch and inter-batch normalisation steps; comparison will be incomplete or misleading.
- Run-order metadata is missing or unreliable; plotRun cannot stratify samples meaningfully.
- Comparing only raw assay to raw assay, or only normalised to normalised; the skill requires paired before/after assays to be interpretable.

## Inputs

- SummarizedExperiment object with rawImpute assay (log2-transformed, cleaned with threshold=0.5, method='intersect')
- SummarizedExperiment object with normalised assay (e.g., loessShort_concatenate after intra-batch loess + RUV-III and inter-batch concatenation)
- Metabolite identifiers (e.g., '1-methylhistamine', 'GlucosePos2')
- Run order metadata (sample column index or run_id variable)

## Outputs

- Pair of hRUV::plotRun diagnostic plots per metabolite (before and after normalisation)
- Visual assessment document or figure panel comparing signal drift and batch effects pre/post normalisation
- Confirmation that monotonic run-order trends and batch discontinuities are resolved

## How to apply

Generate hRUV::plotRun diagnostic plots for metabolites of interest on two assays: the rawImpute assay (pre-normalisation baseline) and the final normalised assay (e.g., loessShort_concatenate after intra-batch loess smoothing with RUV-III k=5 and inter-batch concatenation). For each metabolite, plot intensity values against run order, stratified by batch. Visually inspect the before plot for presence of monotonic drift trends or discontinuities at batch boundaries; inspect the after plot to confirm these patterns are eliminated and signal variance is homogeneous across run order and batches. Document the comparison by side-by-side examination of identical metabolite identities and run-order ranges across both plots.

## Related tools

- **hRUV** (Generates plotRun diagnostic plots and applies hierarchical normalisation (loess smoothing, RUV-III) to produce before/after assays for comparison) — https://github.com/SydneyBioX/hRUV
- **RUV-III** (Unwanted variation estimation method integrated into hRUV to remove batch effects using sample replicates (k=5 for intra-batch normalisation))
- **SummarizedExperiment** (Data container holding multiple assays (rawImpute, loessShort_concatenate) and metadata for comparison)
- **R** (Execution environment for hRUV and ggplot2/plotly visualisation of run plots)

## Examples

```
hRUV::plotRun(dat_list$rawImpute, metabolite='1-methylhistamine', assay='rawImpute') # before; hRUV::plotRun(dat_list$loessShort_concatenate, metabolite='1-methylhistamine', assay='loessShort_concatenate') # after
```

## Evaluation signals

- Pre-normalisation (rawImpute) plot shows visible monotonic intensity drift or step-like discontinuities across run order within batches
- Post-normalisation (loessShort_concatenate) plot shows flat or random scatter of intensities across run order with no systematic trend
- Batch boundaries in post-normalisation plot no longer exhibit sharp signal jumps; within-batch and between-batch variance are visually comparable
- Same metabolite identity and run-order range plotted on both axes in before/after comparison to ensure fair visual assessment
- No increase in variance or loss of true biological signal in normalised assay; signal should be 'centred' not eliminated

## Limitations

- Visual comparison is subjective; quantitative metrics (e.g., slope of run-order regression, batch variance ratio) may be needed for formal validation.
- Metabolites with very low abundance or high missingness (>50% filtered out during hRUV::clean with threshold=0.5) cannot be assessed in this comparison.
- Run plots are most informative for metabolites with strong pre-normalisation drift; metabolites with minimal baseline drift may appear unchanged, which is correct but uninformative.
- Comparison requires accurate run-order metadata; if samples are not sequenced in recorded run order, diagnostic plots will be misleading.
- Inter-batch normalisation via concatenation is sensitive to the choice and placement of batch replicate samples; poor replicate coverage may result in incomplete drift correction visible in post-normalisation plots.

## Evidence

- [intro] Finding: hRUV normalisation eliminates signal drift: "hRUV normalisation eliminates signal drift in 1-methylhistamine and strong batch effects in GlucosePos2 that were present in the rawImpute assay, as demonstrated by run plots comparing raw and"
- [intro] Workflow step: Generate before plots from rawImpute assay: "Generate hRUV::plotRun diagnostic plots for the rawImpute assay showing run-order variation for 1-methylhistamine and GlucosePos2."
- [intro] Workflow step: Generate after plots from normalised assay: "Generate hRUV::plotRun diagnostic plots for the loessShort_concatenate assay showing the same metabolites to confirm drift and batch effects are corrected."
- [intro] Comparison method: Visual inspection: "Visually compare the before (rawImpute) and after (loessShort_concatenate) plots to confirm signal correction."
- [readme] hRUV hierarchical normalisation approach: "Our novel tool is a novel hierarchical approach to removing unwanted variation by harnessing information from sample replicates embedded in the seequence of experimental runs/batches and applying"
