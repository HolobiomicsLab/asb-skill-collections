---
name: gc-ms-abundance-preprocessing
description: Use when after autoQ has extracted isotopologue peak area measurements
  from mz(X)ML files and you need to prepare the integrations data frame for visualization
  with metBarPlot or comparative analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  tools:
  - isoSCAN
  - R
  - mzR
  - metBarPlot
  techniques:
  - GC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.0c02998
  title: isoSCAN
evidence_spans:
- install_github("jcapelladesto/isoSCAN") library(isoSCAN)
- install_github("jcapelladesto/isoSCAN")
- To Install from R console
- 'To Install from R console: ```` install.packages("devtools", dependencies=TRUE)
  library(devtools)'
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

# gc-ms-abundance-preprocessing

## Summary

Transform raw GC-CI-MS isotopologue peak area measurements into percentage-normalized format suitable for downstream visualization and statistical analysis. This skill converts autoQ integrations output using quantile normalization to enable fair cross-sample comparison of isotopologue abundances.

## When to use

After autoQ has extracted isotopologue peak area measurements from mz(X)ML files and you need to prepare the integrations data frame for visualization with metBarPlot or comparative analysis. Apply this skill when raw area values must be normalized to percentages to account for differences in total ion signal intensity across samples.

## When NOT to use

- Input is already a percentage-normalized or log-transformed feature table from another preprocessing pipeline
- You need to retain raw area values for instrument response curve calibration or absolute quantification
- Isotopologue abundances have already been collapsed or aggregated into summary statistics

## Inputs

- integrations data frame (output from autoQ function with peak area measurements for isotopologues)

## Outputs

- percentage-normalized integrations data frame ready for metBarPlot visualization

## How to apply

Load the integrations data frame output from autoQ (containing peak area measurements for each isotopologue of your targeted compounds). Apply the QTransform function with parameters val.to.use='area' to select area-based integration values and val.trans='P' to apply quantile normalization, converting raw areas into percentage format. The output is a transformed data frame where each isotopologue abundance is expressed as a percentage of the total signal for that compound within each sample, suitable for direct input to metBarPlot for barplot visualization with error bars or for downstream statistical comparison across treatment groups.

## Related tools

- **isoSCAN** (R package providing autoQ function to extract isotopologue abundances and QTransform function for percentage normalization) — https://github.com/jcapelladesto/isoSCAN
- **mzR** (Package used by isoSCAN to read mz(X)ML format mass spectrometry files)
- **metBarPlot** (Downstream function that accepts normalized integrations data frame to produce barplots with standard deviation error bars) — https://github.com/jcapelladesto/isoSCAN
- **R** (Programming environment for executing QTransform and data manipulation)

## Examples

```
QTransform(integrations_df, val.to.use='area', val.trans='P')
```

## Evaluation signals

- Output data frame has same dimensions (rows, compounds) as input but with abundance values scaled to 0–100 range or summing to 100 per sample
- Sum of isotopologue percentages for each compound within each sample equals 100 (or very close, accounting for rounding)
- Relative ranking of isotopologue abundances within each sample is preserved compared to raw area ratios
- No missing values or NaN entries introduced by the transformation
- Output can be directly passed to metBarPlot without error and produces interpretable barplots with error bars

## Limitations

- QTransform with val.trans='P' applies quantile normalization which assumes similar isotopologue distributions across samples; extreme outlier samples may distort the normalization
- Percentage normalization is relative and loses absolute abundance information; if absolute quantification is needed, raw area values must be retained separately
- Compounds with very low peak areas near noise threshold may show inflated percentage contributions after normalization due to signal-to-noise ratio effects
- The transformation assumes peak integration by autoQ was successful; missing or misidentified peaks will propagate as zero or incorrect percentages

## Evidence

- [other] QTransform converts isotopologue area values from autoQ output into percentage-normalized format: "QTransform accepts the autoQ integrations data frame with parameters val.to.use='area' and val.trans='P', transforming raw area values into percentage-normalized format that can be directly passed to"
- [intro] autoQ produces integrations data frame with peak area measurements: "Now we can call `autoQ` function that will process the files and look for the isotopologues for each compound found in the `formulaTable`."
- [intro] metBarPlot accepts transformed data frame for visualization: "The `metBarPlot` function is designed to plot values in a barplot including standard deviation error bars."
- [intro] isoSCAN uses mzR to read MS files in mz(X)ML format: "`isoSCAN` uses `mzR` package in order to read MS files. Therefore, you will have to transform the raw data from vendor format into __mz(X)ML__ format"
