---
name: batch-effect-visualization
description: Use when you have multi-batch metabolomics data in SummarizedExperiment
  format and need to demonstrate that batch clustering or run-order signal drift persists
  in raw/imputed assays but is eliminated after hRUV normalisation (intra-batch loess
  + RUV-III, followed by inter-batch concatenation).
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
  - NormalizeMets
  - RStudio
  - Plotly
  license_tier: open
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
- we will load the hRUV package and other packages required for the demonstration...
  library(dplyr)
- The R software environment can be downloaded for free from the Comprehensive R Archive
  Network (CRAN)
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

# batch-effect-visualization

## Summary

Visualize batch effects and signal drift in metabolomics data before and after normalisation using PCA and run-order plots. This skill enables rapid assessment of whether hierarchical RUV normalisation has successfully removed unwanted variation across experimental batches.

## When to use

Apply this skill when you have multi-batch metabolomics data in SummarizedExperiment format and need to demonstrate that batch clustering or run-order signal drift persists in raw/imputed assays but is eliminated after hRUV normalisation (intra-batch loess + RUV-III, followed by inter-batch concatenation).

## When NOT to use

- Input is already batch-corrected or is single-batch data; batch effect may be imperceptible or trivial.
- rawImpute or loessShort_concatenate assays have not been generated following the prescribed hRUV workflow (log transformation, cleaning, loess+RUV-III, concatenation); comparison will be invalid.
- colData lacks batch_info or equivalent batch labelling; PCA colouring and interpretation becomes impossible.

## Inputs

- SummarizedExperiment object with rawImpute assay (log2-transformed, cleaned with threshold=0.5, intersect method)
- SummarizedExperiment object with loessShort_concatenate assay (intra-batch loess + RUV-III k=5 normalised, inter-batch concatenated)
- colData containing batch_info factor for grouping

## Outputs

- PCA plot of rawImpute assay coloured by batch_info (showing batch effect)
- PCA plot of loessShort_concatenate assay coloured by batch_info (showing batch removal)
- Run-order plot (hRUV::plotRun) for selected metabolite from rawImpute (showing signal drift)
- Run-order plot (hRUV::plotRun) for same metabolite from loessShort_concatenate (showing drift correction)

## How to apply

Generate PCA plots using hRUV::plotPCA on both the rawImpute assay (pre-normalisation) and loessShort_concatenate assay (post-normalisation), colouring by batch_info to reveal batch clustering. Simultaneously generate hRUV::plotRun diagnostic plots for individual metabolites (e.g., 1-methylhistamine, GlucosePos2) on both assays to reveal signal drift across run order. Visual comparison of before/after plots confirms success: rawImpute shows strong batch separation and metabolite run-order variation; loessShort_concatenate shows dispersed, batch-agnostic clustering and flat run-order profiles. Rationale: PCA reveals global batch structure; run plots reveal local metabolite-level drift within batch sequences, together providing evidence that both inter- and intra-batch unwanted variation has been removed.

## Related tools

- **hRUV** (Provides plotPCA and plotRun diagnostic plotting functions; used to generate before/after batch-effect visualisations) — https://github.com/SydneyBioX/hRUV
- **SummarizedExperiment** (Container for multi-assay metabolomics data (rawImpute, loessShort_concatenate) with sample metadata; enables assay subsetting and colData extraction for plotting)
- **R** (Execution environment for hRUV plotting functions and visual inspection)
- **dplyr** (Data manipulation for subsetting metabolites and samples prior to plotting)

## Examples

```
library(hRUV); plotPCA(dat_list[[1]], assay='rawImpute', colour_by='batch_info'); plotPCA(dat_list[[1]], assay='loessShort_concatenate', colour_by='batch_info'); plotRun(dat_list[[1]], assay='rawImpute', metabolite='1-methylhistamine'); plotRun(dat_list[[1]], assay='loessShort_concatenate', metabolite='1-methylhistamine')
```

## Evaluation signals

- PCA plot of rawImpute shows tight clustering of samples by batch_info (strong batch effect visible as distinct colour clusters); PCA of loessShort_concatenate shows dispersed, colour-mixed clustering (batch effect removed).
- Run-order plots for rawImpute display systematic increase or decrease in metabolite signal intensity across run order (signal drift); loessShort_concatenate run plots show flat, scattered profiles (drift corrected).
- Visual inspection confirms that batch-related principal components in rawImpute (typically PC1 or PC2) account for large variance; in loessShort_concatenate, batch no longer segregates samples on principal axes.
- Both before and after plots use identical metabolite selection, y-axis scaling, and batch colour scheme to enable fair visual comparison.
- No assay contains missing values or NA entries in the plotted metabolite/sample intersection; plotting functions execute without error.

## Limitations

- PCA visualisation is 2D projection; batch structure in higher-dimensional space may not be fully captured. Run plots reveal only single-metabolite drift and do not reveal multivariate batch interactions.
- Visual assessment is subjective; quantitative batch-effect metrics (e.g., silhouette width, inertia ratio, RLE) are not produced by this skill alone.
- Effectiveness depends critically on correct application of preceding hRUV workflow steps (log transformation, cleaning with threshold=0.5 and intersect method, loess smoothing, RUV-III k=5, hierarchical concatenation). Deviations will produce invalid or misleading plots.
- Requires multi-batch structure with embedded intra-batch and inter-batch replicates; single-batch or poorly replicated designs may not show batch effects warranting visualisation.
- Metabolite selection for run plots is manual; choice of 'representative' metabolites showing strong drift (e.g., 1-methylhistamine, GlucosePos2) may bias visual conclusions if drift is heterogeneous across metabolites.

## Evidence

- [intro] PCA visualisation shows batch clustering before and after normalisation: "PCA visualisation of rawImpute assay shows strong batch effect, whereas PCA of the loessShort_concatenate normalised assay no longer displays batch effect when coloured by batch_info."
- [intro] Generate hRUV::plotPCA with batch colouring: "Generate a PCA plot using hRUV::plotPCA with rawImpute assay colored by batch_info to visualize the pre-normalization batch effect."
- [intro] Run plots reveal metabolite-level signal drift: "Generate hRUV::plotRun diagnostic plots for the rawImpute assay showing run-order variation for 1-methylhistamine and GlucosePos2."
- [intro] Drift correction confirmed by comparing before/after run plots: "Generate hRUV::plotRun diagnostic plots for the loessShort_concatenate assay showing the same metabolites to confirm drift and batch effects are corrected."
- [readme] hRUV hierarchical normalisation with RUV-III: "hRUV is a package for normalisation of multiple batches of metabolomics data in a hierarchical strategy with use of samples replicates in large-scale studies. The tool utilises 2 types of replicates:"
