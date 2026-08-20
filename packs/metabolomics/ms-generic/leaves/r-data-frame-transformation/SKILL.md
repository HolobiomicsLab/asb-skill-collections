---
name: r-data-frame-transformation
description: Use when when you have autoQ output containing peak area measurements for isotopologues in data frame format and need to prepare data for metBarPlot visualization or cross-sample comparison. Specifically, use this skill when val.to.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - isoSCAN
  - R
  - autoQ
  - QTransform
  - metBarPlot
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1021/acs.analchem.0c02998
  title: isoSCAN
evidence_spans:
- install_github("jcapelladesto/isoSCAN") library(isoSCAN)
- install_github("jcapelladesto/isoSCAN")
- To Install from R console
- 'To Install from R console: ```` install.packages("devtools", dependencies=TRUE) library(devtools)'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_isoscan_cq
    doi: 10.1021/acs.analchem.0c02998
    title: isoSCAN
  dedup_kept_from: coll_isoscan_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.0c02998
  all_source_dois:
  - 10.1021/acs.analchem.0c02998
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# R Data Frame Transformation

## Summary

Transform mass spectrometry integration data frames from raw area values into percentage-normalized format suitable for downstream visualization and statistical analysis. This skill applies quantile normalization to isotopologue abundance measurements, enabling standardized comparison across samples.

## When to use

When you have autoQ output containing peak area measurements for isotopologues in data frame format and need to prepare data for metBarPlot visualization or cross-sample comparison. Specifically, use this skill when val.to.use='area' values need conversion to a percentage-normalized scale (val.trans='P') to account for differences in total ion current or sample loading.

## When NOT to use

- Input data is already in percentage or normalized format (applying val.trans='P' a second time will yield meaningless values).
- Peak areas are zero or missing across all samples for a given isotopologue (percentage normalization will produce NaN or invalid results).
- Raw area values have not been quality-filtered for signal-to-noise ratio or peak width anomalies (use rawPlot or meanRawPlot first to detect moving peaks, noisy spots, or saturated peaks).

## Inputs

- integrations data frame (output from autoQ function with columns for compound identifiers, isotopologue masses, and area values)

## Outputs

- percentage-normalized data frame (same structure as input, with area values replaced by quantile-normalized percentage values 0–100)

## How to apply

Load the integrations data frame output from the autoQ function, which contains raw area-based peak integrations for each isotopologue. Call QTransform with parameters val.to.use='area' to select area-based integration values and val.trans='P' to apply quantile (percentage) normalization. The function will transform raw area values into a 0–100 percentage scale where each isotopologue's contribution is expressed relative to the total across all isotopologues in that sample. The normalized output data frame can then be directly passed to metBarPlot for barplot visualization with standard deviation error bars, or used for downstream statistical comparisons. This normalization step is essential for isotope labelling experiments where absolute peak areas may vary across samples due to instrument or sample preparation factors, but relative isotopologue distributions are the biological signal of interest.

## Related tools

- **autoQ** (Peak integration and isotopologue abundance extraction from mz(X)ML files; produces the integrations data frame that is the input to QTransform) — github.com/jcapelladesto/isoSCAN
- **QTransform** (Applies quantile normalization and value selection; core transformation function that converts area values to percentage format) — github.com/jcapelladesto/isoSCAN
- **metBarPlot** (Visualization of transformed percentage-normalized data as barplots with error bars; downstream consumer of QTransform output) — github.com/jcapelladesto/isoSCAN
- **R** (Programming language runtime for executing QTransform and data frame operations)

## Examples

```
transformed_df <- QTransform(integrations, val.to.use='area', val.trans='P'); metBarPlot(transformed_df)
```

## Evaluation signals

- Output data frame has identical dimensions and column names as input, with only numerical values transformed.
- All percentage-normalized values fall within the range [0, 100] for each sample.
- Sum of percentage values for all isotopologues within a single sample equals 100 (or very close, accounting for floating-point precision).
- Relative rank order of isotopologue abundances is preserved after transformation (the most abundant isotopologue before transformation remains the most abundant after).
- metBarPlot produces a valid barplot with the transformed data without errors or warnings about invalid values.

## Limitations

- Percentage normalization assumes all isotopologues for a compound are present and quantifiable in all samples; missing or zero-area values may skew the normalization.
- The skill does not account for matrix effects or ion suppression specific to individual isotopologues; pre-normalization quality control (rawPlot, meanRawPlot) is essential.
- QTransform requires the integrations data frame to have expected column structure matching autoQ output; malformed or renamed columns will cause transformation to fail or produce incorrect results.
- Quantile normalization is appropriate for relative comparison across isotopologues within a sample but should not be used if absolute quantification (e.g., pmol/cell) is the analysis goal.

## Evidence

- [intro] autoQ output format and QTransform input specification: "Load the integrations data frame (output from autoQ function containing peak area measurements for isotopologues). 2. Apply QTransform function with val.to.use='area' to select area-based integration"
- [intro] QTransform parameter definitions and transformation output: "QTransform accepts the autoQ integrations data frame with parameters val.to.use='area' and val.trans='P', transforming raw area values into percentage-normalized format that can be directly passed to"
- [intro] Downstream use of transformed data: "The `metBarPlot` function is designed to plot values in a barplot including standard deviation error bars."
- [intro] Quality control prerequisites: "`rawPlot` and `meanRawPlot` functions should be used for quality control purposes. They are useful to check for moving peaks, noisy spots or saturated peaks."
