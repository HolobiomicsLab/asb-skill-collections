---
name: batch-corrected-data-visualization
description: Use when after doAnalysis() has been completed and batch correction applied
  (ratio_corrected assay populated), use this skill when you need to inspect the effect
  of batch correction on QC sample clustering, verify that study samples group appropriately
  by type or aliquot, or identify remaining.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - mzQuality
  - SummarizedExperiment
  - mzQualityDashboard
  license_tier: open
derived_from:
- doi: 10.1021/jasms.5c00073
  title: mzquality
evidence_spans:
- library(mzQuality)
- knitr::rmarkdown, library(mzQuality)
- mzQuality requires a specific format for the input data.
- mzQuality requires a specific format for the input data
- The `buildExperiment` function will then take the data and create an experiment
  object that can be used for analysis.
- Internally, mzQuality uses Bioconductors' *SummarizedExperiment* object to store
  the data
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzquality_cq
    doi: 10.1021/jasms.5c00073
    title: mzquality
  dedup_kept_from: coll_mzquality_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.5c00073
  all_source_dois:
  - 10.1021/jasms.5c00073
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# batch-corrected-data-visualization

## Summary

Generate publication-ready plots and interactive visualizations of batch-corrected metabolomics data to inspect data quality, compound distributions, and sample clustering. This skill transforms post-analysis SummarizedExperiment objects into diagnostic plots and dimensionality reduction views that reveal batch effects, outlier patterns, and compound reliability.

## When to use

After doAnalysis() has been completed and batch correction applied (ratio_corrected assay populated), use this skill when you need to inspect the effect of batch correction on QC sample clustering, verify that study samples group appropriately by type or aliquot, or identify remaining outliers or unreliable compounds before generating final reports. Apply this skill before subsetting compounds/samples or calling createReports() to validate analysis outcomes.

## When NOT to use

- Input SummarizedExperiment has not been processed by doAnalysis() (assay 'ratio_corrected' does not exist; use doAnalysis first).
- Goal is to export final reports and tab-delimited data tables (use createReports instead).
- Data is in raw, unbatched format with no QC samples available for batch correction assessment.

## Inputs

- SummarizedExperiment object with doAnalysis results (rowData, colData, and assay 'ratio_corrected' populated)
- Batch and sample type annotations in colData
- Compound quality flags (use=TRUE/FALSE) in rowData

## Outputs

- PCA plot showing aliquot/sample distribution per type and batch
- Compound scatterplots (ratio_corrected assay values across samples)
- Violin plots stratified by sample type
- Boxplots of all compound values across aliquots
- Interactive Shiny dashboard (mzQualityDashboard) with linked plots and data tables

## How to apply

Load the post-analysis SummarizedExperiment object (output of doAnalysis) into R. Select the appropriate assay slot—typically 'ratio_corrected' for batch-corrected compound/internal standard ratios. Call plotting functions such as pcaPlot() to visualize aliquot distribution per type and batch in PCA space, compoundPlot() to inspect individual compound intensities across samples, violinPlot() to compare distributions by sample type, and aliquotPlot() to create boxplots of all values across aliquots. These functions automatically extract colData and rowData annotations (sample type, batch, use flags) to color and stratify the plots. Inspect the plots to confirm that QC samples cluster tightly, study samples separate by expected phenotype/batch, and compounds marked use=TRUE show consistent signal and low variance relative to use=FALSE compounds. This visual inspection informs manual override of the automatic use flags if needed before subsetting.

## Related tools

- **mzQuality** (Provides SummarizedExperiment object structure, batch correction (ratio_corrected assay), and plotting functions (pcaPlot, compoundPlot, violinPlot, aliquotPlot)) — https://github.com/hankemeierlab/mzQuality
- **mzQualityDashboard** (Interactive Shiny application frontend for visualizing and inspecting batch-corrected metabolomics data without programming) — https://github.com/hankemeierlab/mzQualityDashboard
- **SummarizedExperiment** (Bioconductor container class storing assays (ratio_corrected), rowData (compound annotations), and colData (sample metadata))
- **R** (Programming environment for loading data, calling plotting functions, and iterating on visualization parameters)

## Examples

```
exp <- doAnalysis(exp = exp); pcaPlot(exp, assay = "ratio_corrected"); compoundPlot(exp, assay = "ratio_corrected"); violinPlot(exp)
```

## Evaluation signals

- PCA plot shows QC samples (Pooled or Pooled Study QC) clustering tightly in PCA space, indicating successful batch correction.
- Violin plots and boxplots for compounds marked use=TRUE show lower inter-quartile range and smaller outlier spread compared to use=FALSE compounds.
- Study samples separate visibly by expected type (e.g., disease vs. control) or batch in PCA; no large unexplained clustering by batch after correction.
- Compounds with high RSDQC values or low presence in QC samples are visually confirmed as noisy (high variance, low signal) in compoundPlot views.
- Sample outliers identified by doAnalysis (Rosner test, use=FALSE in colData) are visually confirmed as distant in PCA or extreme in aliquot boxplots.

## Limitations

- Plots reflect only the subset of compounds and samples currently in the SummarizedExperiment; subsetting must occur before plotting to visualize filtered data.
- PCA plots lose interpretability if the number of compounds with use=TRUE is very small (<5); consider retaining more marginal compounds temporarily for diagnostic plotting.
- Interactive mzQualityDashboard requires R/Shiny runtime; command-line plotting functions produce static images suitable for manuscripts but lack interactivity.
- Batch correction is performed only if SQC (pooled study quality control) samples are present; visualization of ratio_corrected assay without SQC will show uncorrected ratios.

## Evidence

- [readme] PCA visualization across samples showing batch-corrected aliquot distribution: "Principal Component Analysis plot showing the aliquot distribution per type and batch for batch-corrected ratios"
- [readme] Multiple plotting functions available post-doAnalysis for batch-corrected inspection: "Boxplot of all values in aliquots/samples; Scatterplot of the compound / IS ratio for the first compound; Violinplot showing the distribution for a given sample type"
- [readme] doAnalysis produces batch-corrected ratios stored in assay slot: "Perform batch correction using the pooled study quality control samples (SQC)"
- [readme] Compound and sample quality flags guide interpretation of batch-corrected plots: "mzQuality adds a column called `use` in both the `rowData` and `colData` slots of the SummarizedExperiment. These contain either a `TRUE` or `FALSE` value, indicating if the compound or sample is"
- [readme] SummarizedExperiment is the core object structure holding all assays and annotations: "The result is a SummarizedExperiment, which is the core object that mzQuality uses"
