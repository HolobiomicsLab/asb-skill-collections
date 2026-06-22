---
name: run-order-diagnostic-plotting
description: Use when you have metabolomics data structured as a SummarizedExperiment with run-order metadata and need to diagnose whether signal intensity or abundance varies systematically with sample acquisition order (intra-batch drift) or batch assignment (inter-batch effects).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
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
derived_from:
- doi: 10.1101/2020.12.21.423723
  title: hRUV
evidence_spans:
- '`hRUV` is a package for normalisation of multiple batches of metabolomics data'
- '`hRUV` is a package for normalisation of multiple batches of metabolomics data in a hierarchical strategy'
- 'utilises 2 types of replicates: intra-batch and inter-batch replicates to estimate the unwanted variation within and between batches with RUV-III'
- Install the R package from GitHub using the `devtools` package
- we will load the hRUV package and other packages required for the demonstration... library(dplyr)
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
---

# run-order-diagnostic-plotting

## Summary

Generate run-order diagnostic plots to visualize signal drift and batch effects in metabolomics assays across experimental sequences. This skill detects temporal variation within and between batches that may obscure true biological signal before normalisation.

## When to use

Apply this skill when you have metabolomics data structured as a SummarizedExperiment with run-order metadata and need to diagnose whether signal intensity or abundance varies systematically with sample acquisition order (intra-batch drift) or batch assignment (inter-batch effects). Use it before and after normalisation to confirm that hRUV or similar batch-correction methods have eliminated these artefacts.

## When NOT to use

- Input data lacks run-order or batch metadata — diagnostic plots require explicit temporal/batch structure to be meaningful.
- Metabolite has <50% data completeness after cleaning — hRUV::clean filtering (threshold=0.5, method='intersect') should precede plotting to avoid spurious patterns from sparse features.
- Single-batch or single-run experiments with no inter-batch or intra-batch replicates — drift and batch effects cannot be distinguished without replicate structure.

## Inputs

- SummarizedExperiment object with log-transformed or cleaned assays (logRaw, rawImpute, or normalised assay)
- Metabolite feature names (character vector)
- Run-order metadata (sample acquisition sequence, batch assignments)

## Outputs

- hRUV run-order diagnostic plots (ggplot2 objects or static images)
- Visual comparison of pre- and post-normalisation drift/batch patterns
- Qualitative confirmation of signal correction efficacy

## How to apply

Load your metabolomics SummarizedExperiment object containing raw or log-transformed assays (e.g., rawImpute or loessShort_concatenate). Use hRUV::plotRun() to generate run-order plots for target metabolites, with the x-axis representing sample acquisition sequence within batch and the y-axis showing metabolite intensity. The loess trend line (default smoothing) reveals drift magnitude. Compare before-and-after plots visually: post-normalisation plots should show flattened trend lines and collapsed batch-specific offsets. Apply this to metabolites known to exhibit high missingness or batch sensitivity (flagged during data cleaning with threshold = 0.5). Repeat across multiple metabolites to ensure correction is systematic, not cherry-picked.

## Related tools

- **hRUV** (Provides plotRun() function to generate run-order diagnostic plots with loess smoothing for drift and batch-effect visualization) — https://github.com/SydneyBioX/hRUV
- **SummarizedExperiment** (Container class for storing metabolomics assays, feature metadata, and sample-level run-order/batch annotations) — https://bioconductor.org/packages/SummarizedExperiment/
- **ggplot2** (Underlying plotting backend for hRUV::plotRun visualization)
- **RUV-III** (Normalisation method (applied upstream) whose effectiveness is evaluated by run-order diagnostic plots)

## Examples

```
hRUV::plotRun(dat_list[['rawImpute']], feature='1-methylhistamine') # pre-normalisation; hRUV::plotRun(dat_list[['loessShort_concatenate']], feature='1-methylhistamine') # post-normalisation
```

## Evaluation signals

- Post-normalisation run-order plots show flattened or near-horizontal loess trend lines, compared to strong positive/negative slopes in pre-normalisation (rawImpute) plots for the same metabolites.
- Batch-specific offsets visible in rawImpute plots (e.g., distinct vertical separation between batches in GlucosePos2) are collapsed or eliminated in loessShort_concatenate plots.
- Signal variance around the trend line is reduced post-normalisation, indicating both drift and residual batch noise have been attenuated.
- Plots for multiple metabolites (e.g., 1-methylhistamine and GlucosePos2) show consistent correction patterns, not isolated to a single feature.
- Visual comparison of before/after plots confirms that no artificial structure or new systematic bias has been introduced by normalisation.

## Limitations

- Diagnostic plots are qualitative; no formal statistical test is applied. Visual judgment of 'flattening' or 'collapse' is subjective and may require domain expertise to interpret.
- Efficacy depends on upstream data cleaning (hRUV::clean with appropriate threshold and method); if too many metabolites are filtered or imputed incorrectly, plots may show apparent correction that is an artefact of reduced variance.
- Run-order plots assume monotonic or smooth drift; non-linear or cyclical artefacts may not be fully captured by loess smoothing or may appear overcorrected.
- Plots require explicit run-order and batch metadata; their absence or mislabelling will produce uninformative or misleading visualisations.
- Inter-batch normalisation (concatenation step) must be applied before plotting loessShort_concatenate assay; plots of intermediate assays (e.g., intra-batch loessShort only) will not reflect full batch correction.

## Evidence

- [intro] Generate hRUV::plotRun diagnostic plots for signal-drift and batch-effect visualization: "Generate hRUV::plotRun diagnostic plots for the rawImpute assay showing run-order variation for 1-methylhistamine and GlucosePos2"
- [intro] hRUV normalisation eliminates signal drift and batch effects visible in individual metabolites: "hRUV normalisation eliminates signal drift in 1-methylhistamine and strong batch effects in GlucosePos2 that were present in the rawImpute assay, as demonstrated by run plots comparing raw and"
- [readme] Hierarchical approach harnesses replicate information and applies signal drift correction: "Our novel tool is a novel hierarchical approach to removing unwanted variation by harnessing information from sample replicates embedded in the seequence of experimental runs/batches and applying"
- [intro] Data cleaning with threshold filtering precedes diagnostic plotting: "We have filtered metabolites with more than 50% of missing values per batch and selected metabolites that are quantified across all batches (intersect)"
- [intro] Run plots compare before and after normalisation to confirm correction: "Visually compare the before (rawImpute) and after (loessShort_concatenate) plots to confirm signal correction"
